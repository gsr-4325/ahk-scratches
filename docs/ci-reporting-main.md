# CI report publishing on main

## Why this exists

The repository recreation removed the dedicated `ci-reports` branch.

As a fallback, the latest machine-generated test report is now written back to the `main` branch under `reports/`.

## Where to look

Paths:

- `reports/ahk-ipc-stdio-fast-v2/latest.md`
- `reports/ahk-ipc-stdio-fast-v2/latest.json`
- `reports/ahk-ipc-stdio-fast-v2/latest-transcript.txt`
- `reports/ahk-ipc-stdio-fast-v2/latest-stderr.txt`
- `reports/ahk-ipc-stdio-fast-v2/latest-metadata.txt`

## Why this does not loop forever

The workflow that publishes these files only triggers on workflow, script, tool, and docs paths.

It does not trigger on `reports/**`, so a report commit does not recursively rerun the same workflow.

## Intended usage

Run the reporting workflow, then open `latest.md` first.
