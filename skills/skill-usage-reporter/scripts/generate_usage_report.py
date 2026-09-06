#!/usr/bin/env python3
"""Generate a self-contained interactive HTML skill-usage report."""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import parse_qs, urlsplit


SUPPORTED_SUFFIXES = {".json", ".jsonl", ".ndjson"}
ACCESS_RE = re.compile(
    r'"(?P<method>GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+'
    r'(?P<target>\S+)\s+HTTP/[^\"]+"\s+(?P<status>\d{3})'
)
EVENTS = {"skill_started", "skill_completed", "skill_failed"}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze CloudWatch skill telemetry and create an interactive HTML report."
    )
    parser.add_argument("inputs", nargs="+", type=Path, help="JSON/JSONL file(s) or folder(s)")
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--output", type=Path, help="Exact .html output path")
    output.add_argument("--output-dir", type=Path, help="Directory for a timestamped report")
    parser.add_argument("--title", default="AI Skill Usage Report", help="Dashboard title")
    parser.add_argument(
        "--fail-on-no-telemetry",
        action="store_true",
        help="Exit with status 2 when no supported telemetry events are found",
    )
    return parser.parse_args(argv)


def discover_files(inputs: Iterable[Path]) -> list[Path]:
    files: set[Path] = set()
    for item in inputs:
        resolved = item.expanduser().resolve()
        if not resolved.exists():
            raise FileNotFoundError(f"Input does not exist: {item}")
        if resolved.is_file():
            if resolved.suffix.lower() not in SUPPORTED_SUFFIXES:
                raise ValueError(f"Unsupported input type: {resolved}")
            files.add(resolved)
        elif resolved.is_dir():
            for candidate in resolved.rglob("*"):
                if candidate.is_file() and candidate.suffix.lower() in SUPPORTED_SUFFIXES:
                    files.add(candidate.resolve())
    return sorted(files)


def aws_row_to_dict(row: Any) -> dict[str, Any] | None:
    if not isinstance(row, list):
        return None
    result: dict[str, Any] = {}
    for cell in row:
        if isinstance(cell, dict) and "field" in cell:
            result[str(cell["field"])] = cell.get("value")
    return result or None


def records_from_json(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        records: list[dict[str, Any]] = []
        for item in value:
            converted = aws_row_to_dict(item)
            if converted is not None:
                records.append(converted)
            elif isinstance(item, dict):
                records.append(item)
        return records
    if isinstance(value, dict):
        if isinstance(value.get("results"), list):
            return [row for item in value["results"] if (row := aws_row_to_dict(item))]
        if isinstance(value.get("events"), list):
            return [item for item in value["events"] if isinstance(item, dict)]
        return [value]
    return []


def load_records(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    warnings: list[str] = []
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        return [], [f"{path.name}: could not read file ({exc})"]
    if not text.strip():
        return [], [f"{path.name}: empty file"]
    try:
        return records_from_json(json.loads(text)), warnings
    except json.JSONDecodeError:
        records: list[dict[str, Any]] = []
        invalid = 0
        for line in text.splitlines():
            if not line.strip():
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                invalid += 1
                continue
            records.extend(records_from_json(value))
        if invalid:
            warnings.append(f"{path.name}: skipped {invalid} invalid JSON line(s)")
        if not records:
            warnings.append(f"{path.name}: no JSON records found")
        return records, warnings


def first_value(params: dict[str, list[str]], key: str) -> str:
    values = params.get(key, [])
    return values[0] if values else ""


def parse_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        seconds = float(value) / 1000 if float(value) > 10_000_000_000 else float(value)
        try:
            return datetime.fromtimestamp(seconds, tz=timezone.utc)
        except (OverflowError, OSError, ValueError):
            return None
    text = str(value).strip()
    if not text:
        return None
    if text.isdigit():
        return parse_datetime(int(text))
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return None


def isoformat(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def extract_telemetry(record: dict[str, Any], source: Path) -> dict[str, Any] | None:
    message = record.get("@message", record.get("message"))
    target = ""
    http_status: int | None = None
    if isinstance(message, str):
        match = ACCESS_RE.search(message)
        if not match:
            return None
        target = match.group("target")
        http_status = int(match.group("status"))
    elif isinstance(message, dict):
        target = str(message.get("target") or message.get("request_uri") or message.get("url") or "")
        raw_status = message.get("status") or message.get("status_code")
        try:
            http_status = int(raw_status) if raw_status is not None else None
        except (TypeError, ValueError):
            http_status = None
    if not target:
        return None
    split = urlsplit(target)
    params = parse_qs(split.query, keep_blank_values=True)
    event = first_value(params, "event")
    if event not in EVENTS:
        return None
    agent = first_value(params, "ai_agent")
    txn = first_value(params, "txn")
    status = first_value(params, "status")
    if not agent or not txn or not status:
        return None
    observed = parse_datetime(record.get("@timestamp", record.get("timestamp")))
    reported = parse_datetime(first_value(params, "timestamp"))
    return {
        "agent": agent,
        "event": event,
        "status": status,
        "txn": txn,
        "user_input": first_value(params, "user_input"),
        "ai_output": first_value(params, "ai_output"),
        "observed_at": observed,
        "reported_at": reported,
        "http_status": http_status,
        "source": source.name,
    }


def pair_invocations(events: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    events.sort(key=lambda item: item["observed_at"] or datetime.min.replace(tzinfo=timezone.utc))
    active: dict[tuple[str, str], deque[dict[str, Any]]] = defaultdict(deque)
    invocations: list[dict[str, Any]] = []
    orphans: list[dict[str, Any]] = []
    sequence = 0
    for event in events:
        key = (event["txn"], event["agent"])
        if event["event"] == "skill_started":
            sequence += 1
            invocation = {
                "id": sequence,
                "agent": event["agent"],
                "txn": event["txn"],
                "started_at": isoformat(event["observed_at"]),
                "completed_at": None,
                "reported_started_at": isoformat(event["reported_at"]),
                "request": event["user_input"],
                "output": "",
                "result": "incomplete",
                "duration_seconds": None,
                "start_http_status": event["http_status"],
                "terminal_http_status": None,
                "source": event["source"],
            }
            invocations.append(invocation)
            active[key].append(invocation)
            continue
        if not active[key]:
            orphans.append(
                {
                    "agent": event["agent"],
                    "txn": event["txn"],
                    "event": event["event"],
                    "observed_at": isoformat(event["observed_at"]),
                    "source": event["source"],
                }
            )
            continue
        invocation = active[key].popleft()
        invocation["completed_at"] = isoformat(event["observed_at"])
        invocation["output"] = event["ai_output"]
        invocation["terminal_http_status"] = event["http_status"]
        invocation["result"] = "failed" if event["event"] == "skill_failed" or event["status"] == "failed" else "success"
        start = parse_datetime(invocation["started_at"])
        end = event["observed_at"]
        if start is not None and end is not None:
            invocation["duration_seconds"] = max(0.0, round((end - start).total_seconds(), 3))
    return invocations, orphans


def percentile(values: list[float], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = (len(ordered) - 1) * fraction
    lower = int(index)
    upper = min(lower + 1, len(ordered) - 1)
    weight = index - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def safe_json(value: Any) -> str:
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        .replace("<", "\\u003c")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def build_html(dataset: dict[str, Any], title: str) -> str:
    data_json = safe_json(dataset)
    title_json = safe_json(title)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html_text(title)}</title>
<style>
:root{{--ink:#17212b;--muted:#647281;--paper:#f4f7f9;--card:#fff;--line:#dce4e9;--navy:#12324a;--teal:#087f8c;--green:#27864a;--red:#bf3b45;--amber:#b47300;--shadow:0 10px 30px rgba(18,50,74,.08)}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--paper);color:var(--ink);font:14px/1.45 ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
header{{background:linear-gradient(125deg,#102f46,#0d6670);color:white;padding:34px max(24px,calc((100vw - 1440px)/2));box-shadow:var(--shadow)}}
header h1{{margin:0 0 7px;font-size:clamp(25px,4vw,38px);letter-spacing:-.03em}} header p{{margin:0;color:#d6edf0}}
main{{max-width:1440px;margin:0 auto;padding:24px}} .panel{{background:var(--card);border:1px solid var(--line);border-radius:14px;box-shadow:var(--shadow);padding:18px;margin-bottom:18px}}
.filters{{display:grid;grid-template-columns:minmax(220px,2fr) repeat(4,minmax(140px,1fr)) auto;gap:12px;align-items:end}} label{{display:grid;gap:6px;color:var(--muted);font-size:12px;font-weight:700}}
input,select,button{{font:inherit;border:1px solid #bdcbd3;border-radius:8px;padding:9px 10px;background:white;color:var(--ink)}} button{{cursor:pointer;font-weight:700}} button:hover{{border-color:var(--teal);color:var(--teal)}}
.cards{{display:grid;grid-template-columns:repeat(7,minmax(130px,1fr));gap:12px;margin-bottom:18px}} .card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:15px;box-shadow:var(--shadow)}}
.card .value{{font-size:25px;font-weight:800;letter-spacing:-.03em}} .card .label{{color:var(--muted);font-size:12px;margin-top:2px}} .grid{{display:grid;grid-template-columns:1.4fr 1fr;gap:18px}}
h2{{font-size:17px;margin:0 0 14px}} .bars{{display:grid;gap:9px}} .bar-row{{display:grid;grid-template-columns:minmax(90px,160px) 1fr 44px;gap:10px;align-items:center}} .track{{height:18px;background:#edf2f4;border-radius:6px;overflow:hidden}} .fill{{height:100%;background:linear-gradient(90deg,var(--teal),#4cb8b3);border-radius:6px;min-width:2px}}
.legend{{display:flex;flex-wrap:wrap;gap:14px;color:var(--muted);font-size:12px;margin-top:12px}} .dot{{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px}} .empty{{color:var(--muted);padding:20px 0;text-align:center}}
.table-wrap{{overflow:auto;max-height:650px;border:1px solid var(--line);border-radius:10px}} table{{width:100%;border-collapse:collapse;min-width:1050px}} th,td{{padding:10px 11px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}} th{{position:sticky;top:0;background:#edf3f5;z-index:1;font-size:12px;cursor:pointer;white-space:nowrap}} td.summary{{max-width:360px}} tr:hover td{{background:#f8fbfc}}
.pill{{display:inline-block;border-radius:999px;padding:3px 8px;font-size:11px;font-weight:800}} .success{{background:#e1f4e7;color:var(--green)}} .failed{{background:#fde5e7;color:var(--red)}} .incomplete{{background:#fff0cf;color:var(--amber)}}
.meta{{display:flex;gap:18px;flex-wrap:wrap;color:var(--muted);font-size:12px}} details{{margin-top:10px}} .diagnostics{{display:grid;grid-template-columns:repeat(4,minmax(100px,1fr));gap:12px}} .diag strong{{font-size:19px;display:block}} .warning{{border-left:4px solid var(--amber);padding-left:10px;margin-top:12px;color:#6a4a0b}}
footer{{text-align:center;color:var(--muted);padding:8px 0 28px;font-size:12px}} @media(max-width:1050px){{.filters{{grid-template-columns:repeat(2,1fr)}}.cards{{grid-template-columns:repeat(3,1fr)}}.grid{{grid-template-columns:1fr}}}} @media(max-width:620px){{main{{padding:12px}}.filters,.cards,.diagnostics{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<header><h1 id="reportTitle"></h1><p id="subtitle"></p></header>
<main>
<section class="panel filters">
<label>Search summaries<input id="search" type="search" placeholder="Request, outcome, transaction…"></label>
<label>Agent<select id="agent"><option value="">All agents</option></select></label>
<label>Result<select id="result"><option value="">All results</option><option>success</option><option>failed</option><option>incomplete</option></select></label>
<label>From<input id="from" type="datetime-local"></label><label>To<input id="to" type="datetime-local"></label>
<button id="reset" type="button">Reset</button>
</section>
<section id="cards" class="cards"></section>
<section class="grid">
<div class="panel"><h2>Usage over time</h2><div id="timeline" class="bars"></div></div>
<div class="panel"><h2>Usage by skill</h2><div id="agents" class="bars"></div><div class="legend"><span><i class="dot" style="background:var(--green)"></i>success</span><span><i class="dot" style="background:var(--red)"></i>failed</span><span><i class="dot" style="background:var(--amber)"></i>incomplete</span></div></div>
</section>
<section class="panel"><h2>Top user intent summaries</h2><div id="intents" class="bars"></div><p class="meta">Themes are grouped by exact sanitized telemetry summary and may undercount differently worded requests with the same intent.</p></section>
<section class="panel"><div style="display:flex;justify-content:space-between;gap:12px;align-items:center"><h2 style="margin:0">Invocation details</h2><button id="csv" type="button">Export filtered CSV</button></div><p id="rowCount" class="meta"></p><div class="table-wrap"><table><thead><tr><th data-sort="started_at">Started</th><th data-sort="agent">Skill</th><th data-sort="result">Result</th><th data-sort="duration_seconds">Duration</th><th data-sort="request">User intent summary</th><th data-sort="output">Outcome summary</th><th data-sort="txn">Transaction</th><th data-sort="source">Source</th></tr></thead><tbody id="rows"></tbody></table></div></section>
<section class="panel"><h2>Data quality</h2><div id="diagnostics" class="diagnostics"></div><div id="warnings"></div><details><summary>Interpretation notes</summary><ul><li>Requests and outcomes are privacy-sanitized telemetry summaries, not complete conversations.</li><li>Durations use CloudWatch observation timestamps.</li><li>Incomplete means a start event had no matching completion or failure in the supplied logs.</li><li>Terminal events without a matching start appear in diagnostics but are not counted as invocations.</li></ul></details></section>
</main><footer>This self-contained report makes no network requests.</footer>
<script>
const DATA={data_json}; const TITLE={title_json}; let sortKey="started_at", sortDirection=-1;
const $=id=>document.getElementById(id); const esc=s=>String(s??"").replace(/[&<>\"']/g,c=>({{"&":"&amp;","<":"&lt;",">":"&gt;",'\"':"&quot;","'":"&#39;"}}[c]));
const dt=v=>v?new Date(v):null; const formatDate=v=>v?new Intl.DateTimeFormat(undefined,{{dateStyle:"medium",timeStyle:"medium"}}).format(new Date(v)):"—";
const formatDuration=v=>v==null?"—":v<60?`${{v.toFixed(1)}}s`:`${{Math.floor(v/60)}}m ${{Math.round(v%60)}}s`;
function filtered(){{const q=$("search").value.trim().toLowerCase(),agent=$("agent").value,result=$("result").value,from=$("from").value?new Date($("from").value):null,to=$("to").value?new Date($("to").value):null;return DATA.invocations.filter(x=>(!agent||x.agent===agent)&&(!result||x.result===result)&&(!from||dt(x.started_at)>=from)&&(!to||dt(x.started_at)<=to)&&(!q||[x.request,x.output,x.txn,x.agent,x.source].some(v=>String(v||"").toLowerCase().includes(q))))}}
function median(values){{if(!values.length)return null;values=[...values].sort((a,b)=>a-b);const m=Math.floor(values.length/2);return values.length%2?values[m]:(values[m-1]+values[m])/2}}
function renderCards(rows){{const successes=rows.filter(x=>x.result==="success").length,failed=rows.filter(x=>x.result==="failed").length,incomplete=rows.filter(x=>x.result==="incomplete").length,terminal=successes+failed,durations=rows.map(x=>x.duration_seconds).filter(x=>x!=null);const cards=[[rows.length,"Invocations"],[successes,"Successful"],[failed,"Failed"],[incomplete,"Incomplete"],[terminal?`${{(successes/terminal*100).toFixed(1)}}%`:"—","Success rate"],[new Set(rows.map(x=>x.txn)).size,"Sessions"],[formatDuration(median(durations)),"Median duration"]];$("cards").innerHTML=cards.map(([v,l])=>`<div class="card"><div class="value">${{esc(v)}}</div><div class="label">${{esc(l)}}</div></div>`).join("")}}
function group(rows,keyFn){{const out=new Map;rows.forEach(x=>{{const k=keyFn(x);out.set(k,(out.get(k)||0)+1)}});return [...out.entries()].sort((a,b)=>String(a[0]).localeCompare(String(b[0])))}}
function renderTimeline(rows){{const dates=rows.map(x=>dt(x.started_at)).filter(Boolean),span=dates.length?Math.max(...dates)-Math.min(...dates):0,chars=span<=21600000?16:span<=172800000?13:10,groups=group(rows,x=>(x.started_at||"unknown").slice(0,chars).replace("T"," ")),max=Math.max(1,...groups.map(x=>x[1]));$("timeline").innerHTML=groups.length?groups.map(([k,v])=>`<div class="bar-row"><span>${{esc(k)}}</span><div class="track"><div class="fill" style="width:${{v/max*100}}%"></div></div><strong>${{v}}</strong></div>`).join(""):'<div class="empty">No invocations match the filters.</div>'}}
function renderAgents(rows){{const names=[...new Set(rows.map(x=>x.agent))].sort(),max=Math.max(1,...names.map(n=>rows.filter(x=>x.agent===n).length));$("agents").innerHTML=names.length?names.map(n=>{{const subset=rows.filter(x=>x.agent===n),counts={{success:0,failed:0,incomplete:0}};subset.forEach(x=>counts[x.result]++);const total=subset.length;return `<div><div style="display:flex;justify-content:space-between"><strong>${{esc(n)}}</strong><span>${{total}}</span></div><div class="track" style="display:flex"><span style="width:${{counts.success/max*100}}%;background:var(--green)"></span><span style="width:${{counts.failed/max*100}}%;background:var(--red)"></span><span style="width:${{counts.incomplete/max*100}}%;background:var(--amber)"></span></div></div>`}}).join(""):'<div class="empty">No skill usage to display.</div>'}}
function renderIntents(rows){{const groups=group(rows,x=>x.request||"(no request summary)").sort((a,b)=>b[1]-a[1]).slice(0,10),max=Math.max(1,...groups.map(x=>x[1]));$("intents").innerHTML=groups.length?groups.map(([k,v])=>`<div class="bar-row" style="grid-template-columns:minmax(220px,2fr) 3fr 44px"><span title="${{esc(k)}}">${{esc(k.length>100?k.slice(0,97)+"…":k)}}</span><div class="track"><div class="fill" style="width:${{v/max*100}}%"></div></div><strong>${{v}}</strong></div>`).join(""):'<div class="empty">No user intent summaries to display.</div>'}}
function renderTable(rows){{rows=[...rows].sort((a,b)=>{{let av=a[sortKey],bv=b[sortKey];if(av==null)av="";if(bv==null)bv="";return (typeof av==="number"?av-bv:String(av).localeCompare(String(bv)))*sortDirection}});$("rowCount").textContent=`Showing ${{rows.length}} of ${{DATA.invocations.length}} invocation(s)`;$("rows").innerHTML=rows.map(x=>`<tr><td title="${{esc(x.started_at)}}">${{esc(formatDate(x.started_at))}}</td><td>${{esc(x.agent)}}</td><td><span class="pill ${{esc(x.result)}}">${{esc(x.result)}}</span></td><td>${{esc(formatDuration(x.duration_seconds))}}</td><td class="summary">${{esc(x.request||"—")}}</td><td class="summary">${{esc(x.output||"—")}}</td><td title="${{esc(x.txn)}}">${{esc(x.txn.slice(0,8))}}…</td><td>${{esc(x.source)}}</td></tr>`).join("")}}
function renderDiagnostics(){{const d=DATA.diagnostics,items=[[d.files_read,"Files read"],[d.records_read,"Records read"],[d.telemetry_events,"Telemetry events"],[d.orphan_terminal_events,"Orphan terminal events"]];$("diagnostics").innerHTML=items.map(([v,l])=>`<div class="diag"><strong>${{esc(v)}}</strong><span>${{esc(l)}}</span></div>`).join("");const warnings=[...DATA.warnings];if(d.orphan_terminal_events)warnings.push(`${{d.orphan_terminal_events}} terminal event(s) could not be paired with a start event.`);$("warnings").innerHTML=warnings.map(x=>`<div class="warning">${{esc(x)}}</div>`).join("")}}
function render(){{const rows=filtered();renderCards(rows);renderTimeline(rows);renderAgents(rows);renderIntents(rows);renderTable(rows)}}
function csvCell(v){{return `"${{String(v??"").replaceAll('"','""')}}"`}} function exportCsv(){{const cols=["started_at","completed_at","agent","result","duration_seconds","request","output","txn","source"],lines=[cols.join(","),...filtered().map(x=>cols.map(c=>csvCell(x[c])).join(","))],blob=new Blob([lines.join("\\n")],{{type:"text/csv;charset=utf-8"}}),a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="skill-usage-filtered.csv";a.click();URL.revokeObjectURL(a.href)}}
$("reportTitle").textContent=TITLE;$("subtitle").textContent=`Generated ${{formatDate(DATA.generated_at)}} • ${{DATA.coverage.start?formatDate(DATA.coverage.start):"No telemetry"}} to ${{DATA.coverage.end?formatDate(DATA.coverage.end):"No telemetry"}}`;
[...new Set(DATA.invocations.map(x=>x.agent))].sort().forEach(name=>{{const o=document.createElement("option");o.value=o.textContent=name;$("agent").appendChild(o)}});["search","agent","result","from","to"].forEach(id=>$(id).addEventListener("input",render));$("reset").addEventListener("click",()=>{{["search","agent","result","from","to"].forEach(id=>$(id).value="");render()}});$("csv").addEventListener("click",exportCsv);document.querySelectorAll("th[data-sort]").forEach(th=>th.addEventListener("click",()=>{{const next=th.dataset.sort;if(sortKey===next)sortDirection*=-1;else{{sortKey=next;sortDirection=1}}render()}}));renderDiagnostics();render();
</script>
</body></html>'''


def html_text(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def choose_output(args: argparse.Namespace) -> Path:
    if args.output:
        path = args.output.expanduser().resolve()
        if path.suffix.lower() != ".html":
            raise ValueError("--output must end in .html")
        return path
    if args.output_dir:
        directory = args.output_dir.expanduser().resolve()
    elif len(args.inputs) == 1 and args.inputs[0].expanduser().is_dir():
        directory = args.inputs[0].expanduser().resolve()
    else:
        directory = Path.cwd()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    return directory / f"skill-usage-report-{stamp}.html"


def generate(args: argparse.Namespace) -> tuple[Path, dict[str, Any]]:
    files = discover_files(args.inputs)
    if not files:
        raise ValueError("No supported .json, .jsonl, or .ndjson files found")
    events: list[dict[str, Any]] = []
    warnings: list[str] = []
    records_read = 0
    for path in files:
        records, file_warnings = load_records(path)
        warnings.extend(file_warnings)
        records_read += len(records)
        for record in records:
            telemetry = extract_telemetry(record, path)
            if telemetry is not None:
                events.append(telemetry)
    invocations, orphans = pair_invocations(events)
    timestamps = [event["observed_at"] for event in events if event["observed_at"] is not None]
    durations = [item["duration_seconds"] for item in invocations if item["duration_seconds"] is not None]
    dataset = {
        "generated_at": isoformat(datetime.now(timezone.utc)),
        "coverage": {
            "start": isoformat(min(timestamps)) if timestamps else None,
            "end": isoformat(max(timestamps)) if timestamps else None,
        },
        "invocations": invocations,
        "diagnostics": {
            "files_read": len(files),
            "records_read": records_read,
            "telemetry_events": len(events),
            "orphan_terminal_events": len(orphans),
            "completed_durations": len(durations),
            "p50_duration_seconds": round(statistics.median(durations), 3) if durations else None,
            "p95_duration_seconds": round(percentile(durations, 0.95), 3) if durations else None,
        },
        "warnings": warnings,
    }
    if args.fail_on_no_telemetry and not events:
        raise LookupError("No supported skill telemetry events found")
    output = choose_output(args)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_html(dataset, args.title), encoding="utf-8")
    return output, dataset


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        output, data = generate(args)
    except LookupError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except (FileNotFoundError, OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    results = [item["result"] for item in data["invocations"]]
    summary = {
        "report": str(output),
        "files_read": data["diagnostics"]["files_read"],
        "records_read": data["diagnostics"]["records_read"],
        "telemetry_events": data["diagnostics"]["telemetry_events"],
        "invocations": len(results),
        "successful": results.count("success"),
        "failed": results.count("failed"),
        "incomplete": results.count("incomplete"),
        "orphan_terminal_events": data["diagnostics"]["orphan_terminal_events"],
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
