# Snyk PR Security Scan

This document explains how the automated Snyk security scan works for Pull Requests in the CCDI Federation AI repository, including required configuration and expected behavior.

---

## Overview

A GitHub Actions workflow (`.github/workflows/snyk-security-scan.yml`) runs Snyk security scanning automatically on every Pull Request targeting the `main` or `release/**` branches. The workflow can also be triggered manually via **workflow_dispatch**.

Snyk scans check for:

- **Dependency vulnerabilities** — known CVEs in third-party packages (e.g., Node.js packages in `mcp/`).
- **Code-level security issues** — insecure coding patterns, exposed secrets, and misconfigurations across JavaScript and Python source files (Snyk Code / SAST).

High- or critical-severity findings cause the workflow to fail and block merging until they are resolved.

---

## Required GitHub Secret

| Secret name | Description                                                  |
| :---------- | :----------------------------------------------------------- |
| `SNKYAPI`   | Snyk API token used to authenticate with the Snyk platform. |

The workflow reads this secret as `${{ secrets.SNKYAPI }}` and passes it to Snyk as the `SNYK_TOKEN` environment variable. The token value is **never printed in workflow logs**.

### How to add the secret

1. Obtain a Snyk API token from your [Snyk account settings](https://app.snyk.io/account).
2. In the GitHub repository, go to **Settings → Secrets and variables → Actions**.
3. Click **New repository secret**.
4. Set the name to `SNKYAPI` and paste the token value.
5. Click **Add secret**.

> **Note:** If your organization uses environment-level secrets, add `SNKYAPI` to the environment that the workflow uses and update the `environment:` field in the workflow file accordingly.

---

## Workflow Jobs

### `snyk-deps` — Dependency Scan

- Installs Node.js dependencies from `mcp/` using `npm ci`.
- Runs `snyk test --all-projects` to discover and scan all supported dependency manifests in the repository (currently `mcp/package.json`).
- Fails the job when any finding reaches **high** or **critical** severity.
- Uploads results as a SARIF file to GitHub Code Scanning so findings appear on the **Security → Code scanning** tab and in the PR checks.

### `snyk-code` — SAST Scan

- Runs `snyk code test` on the entire repository.
- Covers all supported languages (JavaScript/TypeScript, Python).
- Detects insecure patterns, hardcoded credentials, and configuration issues.
- Fails the job when any finding reaches **high** or **critical** severity.
- Uploads results as a SARIF file to GitHub Code Scanning.

---

## Viewing Results

After the workflow runs:

1. Open the Pull Request on GitHub.
2. Scroll to the **Checks** section to see the `Snyk — Dependency Scan` and `Snyk Code — SAST Scan` check results.
3. For detailed findings, go to the repository's **Security → Code scanning alerts** tab.

---

## Severity Thresholds

The workflow uses `--severity-threshold=high`, which means:

| Severity | Workflow result |
| :------- | :-------------- |
| Critical | ❌ Fails         |
| High     | ❌ Fails         |
| Medium   | ✅ Passes        |
| Low      | ✅ Passes        |

To adjust the threshold, edit the `--severity-threshold` argument in `.github/workflows/snyk-security-scan.yml`.

---

## Manual Trigger

The workflow can be triggered at any time from the **Actions** tab:

1. Go to **Actions → Snyk Security Scan**.
2. Click **Run workflow**.
3. Select the branch and click **Run workflow**.

---

## Maintenance Notes

- The Snyk GitHub Action is pinned to `snyk/actions/node@v1.0.0`. Monitor [Snyk Actions releases](https://github.com/snyk/actions/releases) and update this tag when a new stable version is published.
- When new language ecosystems or dependency manifests are added to the repository, the `--all-projects` flag ensures they are automatically discovered without changes to the workflow.
- If the `SNKYAPI` token expires, regenerate it in the Snyk dashboard and update the GitHub secret.
