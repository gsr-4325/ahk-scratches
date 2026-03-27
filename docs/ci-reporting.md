# CI report publishing

## Goal

Avoid the slow loop of downloading artifacts just to read a small test result.

## What the reporting workflow does

The reporting workflow runs the AutoHotkey StdIO IPC test and then writes the latest result back into the repository on the `ci-reports` branch.

## Where to look

Branch:

- `ci-reports`

Paths:

- `reports/ahk-ipc-stdio-fast-v2/latest.md`
- `reports/ahk-ipc-stdio-fast-v2/latest.json`
- `reports/ahk-ipc-stdio-fast-v2/latest-transcript.txt`
- `reports/ahk-ipc-stdio-fast-v2/latest-stderr.txt`
- `reports/ahk-ipc-stdio-fast-v2/latest-metadata.txt`

## Intended usage

When the workflow finishes, open the `ci-reports` branch and read `latest.md` first.

That file is meant to be the human-friendly summary to paste back into chat when needed.

## Why keep artifacts too

The workflow still uploads artifacts as a fallback.

Use them only when the report branch is not enough.
