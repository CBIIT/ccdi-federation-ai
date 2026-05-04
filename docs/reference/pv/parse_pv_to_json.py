"""Parse CCDI PV markdown files and emit structured JSON."""
import json
import re
import sys
from pathlib import Path


def parse_pv_table(lines: list[str]) -> list[dict] | None:
    """Parse a markdown PV table into a list of dicts. Returns None if no table."""
    header_idx = None
    for i, line in enumerate(lines):
        if line.startswith("| Permissible Value"):
            header_idx = i
            break
    if header_idx is None:
        return None

    headers_raw = [h.strip() for h in lines[header_idx].split("|") if h.strip()]
    # skip separator row
    rows = []
    for line in lines[header_idx + 2 :]:
        if not line.startswith("|"):
            break
        cols = [c.strip() for c in line.split("|")]
        # strip leading/trailing empty strings from split
        cols = [c for c in cols if c != ""]
        # remove backtick wrapping on first column
        if cols:
            cols[0] = cols[0].strip("`")
        row = dict(zip(headers_raw, cols))
        rows.append(
            {
                "value": row.get("Permissible Value", ""),
                "description": row.get("Description", ""),
                "vm_long_name": row.get("VM Long Name", ""),
                "vm_public_id": row.get("VM Public ID", ""),
                "concept_code": row.get("Concept Code", ""),
                "begin_date": row.get("Begin Date", ""),
            }
        )
    return rows if rows else None


def parse_pv_md(path: Path) -> dict:
    """Parse a PV markdown file and return a structured dict keyed by field name."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    result: dict[str, dict] = {}
    field_pattern = re.compile(r'^### \*\*`(.+?)`\*\*')
    cadsr_pattern = re.compile(
        r'\*\*Formal Name: `(.+?)`\*\*.*?\[Link\]\((.+?)\)'
    )
    cde_desc_pattern = re.compile(
        r'This metadata element is defined by the caDSR as "(.+?)"'
    )

    i = 0
    while i < len(lines):
        m = field_pattern.match(lines[i])
        if not m:
            i += 1
            continue

        field_name = m.group(1)
        block_start = i
        # find next field heading to know where this block ends
        j = i + 1
        while j < len(lines):
            if field_pattern.match(lines[j]):
                break
            j += 1
        block_lines = lines[block_start:j]
        block_text = "\n".join(block_lines)

        formal_name = None
        cadsr_link = None
        cm = cadsr_pattern.search(block_text)
        if cm:
            formal_name = cm.group(1)
            cadsr_link = cm.group(2)

        cde_description = None
        dm = cde_desc_pattern.search(block_text)
        if dm:
            cde_description = dm.group(1)

        pvs = parse_pv_table(block_lines)

        result[field_name] = {
            "formal_name": formal_name,
            "cadsr_link": cadsr_link,
            "cde_description": cde_description,
            "permissible_values": pvs,
        }
        i = j

    return result


def main():
    pv_dir = Path(__file__).parent
    md_files = sorted(pv_dir.glob("*-pv-metadata.md"))
    if not md_files:
        print("No PV markdown files found.", file=sys.stderr)
        sys.exit(1)

    for md_path in md_files:
        data = parse_pv_md(md_path)
        out_path = md_path.with_suffix(".json")
        out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Wrote {out_path} ({len(data)} fields)")


if __name__ == "__main__":
    main()
