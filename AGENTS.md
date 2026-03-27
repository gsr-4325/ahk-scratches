# AGENTS.md

This repository is a staging area for small AutoHotkey v2 experiments before they move into a larger project.

## Read this first

Before editing scripts or workflows, also read:

- `docs/agent-pitfalls.md`
- `docs/how-we-work.md`
- `docs/ci-reporting-main.md`
- `docs/stdio-echo.md`

## Important repository facts

- The default branch is currently `master`, not `main`.
- GitHub Actions that push generated reports back into the repo must push to `master`.
- Generated machine reports live under `reports/`.
- Reporting workflows should not trigger on `reports/**` changes, otherwise they may loop.

## AutoHotkey-specific guidance

- Prefer very small, headless entry points for CI.
- Separate GUI experiments from transport / parser / process experiments.
- For CI output, keep deterministic text transcripts and JSON summaries.
- Avoid assuming that console/stdout helpers behave identically across all AHK environments without testing.
- Empty files can become null-ish values in PowerShell pipelines, so publishing steps should coerce text safely.

## When adding a new scratch

- One scratch should answer one question.
- Add a small README or note for how it is expected to run.
- Make the success condition explicit.
- Emit a transcript and a structured summary when practical.

## When updating report workflows

- Use `contents: write` only when the workflow really publishes files.
- Publish latest human-readable output to `reports/.../latest.md`.
- Keep JSON, transcript, stderr, and metadata files next to it.
- Ensure the publish step handles empty stderr/stdout files safely.
