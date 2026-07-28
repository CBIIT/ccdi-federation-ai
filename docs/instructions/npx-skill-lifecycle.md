# npx Skill Lifecycle Management (Cross-Platform)

This guide explains how to install, update, and remove this repository's skill with the `skills` CLI (`npx skills ...`).

## Introduction to npx Skill

Using `npx skills` keeps skill lifecycle management consistent and low-friction:

- No permanent global CLI install required
- Same command surface for install, list, update, and remove
- Works for project-scoped and global skill usage

For this project, the skill source is:

- `CBIIT/ccdi-federation-ai`

## Installation

### macOS / Linux (bash, zsh)

Install to the current project:

```bash
npx skills add CBIIT/ccdi-federation-ai
```

Install globally (user-level):

```bash
npx skills add CBIIT/ccdi-federation-ai --global
```

Preview available skills without installing:

```bash
npx skills add CBIIT/ccdi-federation-ai --list
```

### Windows (PowerShell)

Install to the current project:

```powershell
npx skills add CBIIT/ccdi-federation-ai
```

Install globally (user-level):

```powershell
npx skills add CBIIT/ccdi-federation-ai --global
```

Preview available skills without installing:

```powershell
npx skills add CBIIT/ccdi-federation-ai --list
```

## Updating Skills

Update all installed project skills:

```bash
npx skills update
```

Update only global skills:

```bash
npx skills update --global
```

Update a specific skill by name:

```bash
npx skills update ccdi-federation-ai-copilot
```

## Uninstalling / Managing Skills

List installed project skills:

```bash
npx skills list
```

List installed skills as JSON (automation-friendly):

```bash
npx skills list --json
```

Remove a specific skill:

```bash
npx skills remove ccdi-federation-ai-copilot
```

Remove from global scope:

```bash
npx skills remove ccdi-federation-ai-copilot --global
```

## Add `ccdi-federation-ai-copilot` to ChatGPT or other AI agents

Install this skill for ChatGPT:

```bash
npx skills add CBIIT/ccdi-federation-ai --skill ccdi-federation-ai-copilot --agent chatgpt
```

Install this skill for another supported agent (example: Claude Code):

```bash
npx skills add CBIIT/ccdi-federation-ai --skill ccdi-federation-ai-copilot --agent claude-code
```

Use the skill in ChatGPT without installing it:

```bash
npx skills use CBIIT/ccdi-federation-ai@ccdi-federation-ai-copilot --agent chatgpt
```

If your local machine does not have the agent CLI installed, install that agent first, then re-run the command.

## Project-Specific Differences

Compared with generic examples, this project uses:

- Repository source: `CBIIT/ccdi-federation-ai`
- Primary skill name: `ccdi-federation-ai-copilot`

### Validation Notes

The commands in this guide were validated in this repository with:

- `npx skills --help`
- `npx skills add CBIIT/ccdi-federation-ai --list`
- `npx skills list --json`
