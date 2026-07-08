# CCDI Federation AI

[![Install via npx skills](https://img.shields.io/badge/npx%20skills-install-blue)](https://www.skills.sh/cbiit/ccdi-federation-ai/ccdi-federation-ai-copilot)

An AI agent skill for the [CCDI Data Federation API](https://ccdi.cancer.gov/data-federation-resource). This repository provides components for AI-ready CCDI Federation metadata, including an AgentSkill that standardizes AI interactions through workflows and routing.

## Skill Structure

Each skill directory contains:

- **SKILL.md** — Main instruction file with YAML frontmatter, routing rules, guardrails, and response style guidelines
- **scripts/** — Helper scripts and utilities (PV mapper, fallback API client)
- **references/** — OpenAPI spec, permissible-value metadata, and workflow references
- **agents/** — Agent-specific configuration

Repository layout:

- `skills/ccdi-federation-ai-copilot/` — AgentSkill docs, routing, and fallback scripts
- `docs/instructions/` — End-user and developer setup guides

## Getting Started

### For non-developers (using Codex)

Follow the step-by-step guide to install and use the skill inside Codex:

- [docs/instructions/codex-instruction.md](./docs/instructions/codex-instruction.md)

![Using the skill in Codex](./docs/instructions/images/9-codex-use-skill2.png)

### For developers

Install the skill bundle via [npx](https://docs.npmjs.com/cli/commands/npx):

```bash
npx skills add CBIIT/ccdi-federation-ai
```

## Links

- [CCDI Data Federation](https://ccdi.cancer.gov/data-federation-resource)
- [CCDI Data Federation API documentation](https://cbiit.github.io/ccdi-federation-api/overview.html)
- [Childhood Cancer Data Initiative (CCDI)](https://ccdi.cancer.gov/)

## Disclaimer

This software is provided as-is for research and data exploration purposes. It is maintained by the [Center for Biomedical Informatics and Information Technology (CBIIT)](https://cbiit.cancer.gov/) at the National Cancer Institute. All API calls made through this skill are read-only and access only publicly available CCDI Federation metadata.
