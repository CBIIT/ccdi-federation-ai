# CCDI Federation AgentSkill

Reusable AgentSkill workspace for CCDI federation workflows, with a packaged skill, API references, and permissible value mapping artifacts.

## What This Repository Contains

- `skills/ccdi-federation-helper/`
  - Main skill package (`SKILL.md`) for:
    - Cohort query planning
    - Endpoint/response explanation
    - Metadata sanity guidance
  - Supporting references, schemas, and helper scripts
- `docs/`
  - Design and reference materials for API behavior and sample responses
  - PV (permissible value) metadata examples and parsing utilities
- `skills-lock.json`
  - Skill lock metadata used by the workspace

## Quick Start

1. Review the high-level design in `docs/agentskill-design.md`.
2. Open the skill router in `skills/ccdi-federation-helper/SKILL.md`.
3. Check usage and scope notes in `skills/ccdi-federation-helper/README.md`.
4. Use API and payload references under `docs/reference/` and `skills/ccdi-federation-helper/references/`.

## Install With npx

Use `npx skill add` to install the packaged skill.

From this repository root:

```bash
npx skill add ./skills/ccdi-federation-helper
```

If you are installing from a remote repository, use the repo URL and skill path as supported by your `skill` CLI version.

Example using the repo shorthand format:

```bash
npx skills add CBIIT/ccdi-federation-agentskill@ccdi-federation-helper
```

Example using the full GitHub URL:

```bash
npx skill add "https://github.com/CBIIT/ccdi-federation-agentskill/tree/main/skills/ccdi-federation-helper"
```

## Current Skill Scope

The packaged skill is optimized for metadata-level federation tasks:

- Build cohort query plans from natural language
- Explain endpoints and payload shapes
- Apply permissible value mappings where available
- Keep execution constrained to read-only metadata interactions when explicitly requested

## Repository Notes

- This workspace is documentation and skill-definition heavy.
- Scripts currently included in the packaged skill live in:
  - `skills/ccdi-federation-helper/scripts/ccdi_client.py`
  - `skills/ccdi-federation-helper/scripts/pv_mapper.py`
