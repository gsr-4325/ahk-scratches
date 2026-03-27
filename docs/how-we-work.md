# How we work in `ahk-scratches`

## Purpose

This repository is the staging area for small AutoHotkey v2 experiments before they are promoted into `AoZMacros2`.

The main goal is to let AI iterate against a Windows execution environment more often, so the human loop becomes:

1. define a narrow repro
2. let AI change code in this repo
3. let GitHub Actions run it on Windows
4. inspect the artifact
5. repeat until the behavior is stable
6. only then move the result into `AoZMacros2`

## What belongs here

Good candidates:

- non-GUI prototypes
- parser / serializer experiments
- file-system behavior
- child process launch
- StdIO IPC
- retry / timeout logic
- structured logging
- tiny reproductions of a larger bug

Avoid as the first CI target:

- WebView2 GUI behavior
- tray icon workflows
- focus-sensitive automation
- coordinate / pixel dependent behavior
- anything that really needs an interactive desktop session

## Working loop

### 1. Create a narrow scratch

Keep each experiment small and self-contained.

Recommended layout:

- `scripts/experiments/<topic>/main.ahk`
- `scripts/experiments/<topic>/README.md`
- optional helper files next to it

### 2. Make sure it has a headless entry point

Each experiment should have one script that can run without manual clicking.

Examples:

- a parser that reads a fixture and prints JSON
- a parent script that launches one or more child processes and exits with a clear code
- a transport test that writes a deterministic log

### 3. Emit useful output

At minimum, make the script useful through:

- `stdout`
- `stderr`
- exit code
- optional log file inside a known output folder

A scratch is much easier for AI to debug when a failed run already explains:

- which phase failed
- what was expected
- what was actually observed

### 4. Run it through the `AHK smoke` workflow

Use the workflow inputs to choose:

- `script_path`
- `ahk_version`
- `timeout_seconds`

### 5. Read the artifact first

The first stop after every failed run should be the uploaded artifact:

- `stdout.txt`
- `stderr.txt`
- `run-metadata.txt`

Prefer reading those before trying to reason from memory.

## Conventions for future scratches

### Logging

Prefer deterministic log lines over prose.

Example shape:

```text
2026-03-26T13:45:12Z | parent | phase=spawn | child=worker-001 | ok=true
2026-03-26T13:45:12Z | child  | phase=ready | pid=12345
2026-03-26T13:45:13Z | parent | phase=send  | kind=ping
2026-03-26T13:45:13Z | child  | phase=recv  | kind=ping
```

### Exit codes

Use exit code `0` only for a real success.

Use non-zero exit codes for:

- assertion failures
- transport failure
- timeout
- missing dependency
- unsupported environment

### Scope control

One scratch should answer one question.

Bad:

- parser + GUI + IPC + logging rewrite in one folder

Good:

- `stdio-two-process-echo`
- `json-envelope-roundtrip`
- `timeout-kills-child`

## Promotion checklist for `AoZMacros2`

Move code out of `ahk-scratches` only after:

- the scratch has a clear purpose
- the run is repeatable
- the logs are readable
- at least one useful path runs in CI
- the artifact is enough to understand common failures

## What may be needed later

If the work shifts toward GUI / WebView2 issues, add a self-hosted Windows runner later.

That is the point where we can attempt:

- screenshots
- freeze reproduction runs
- desktop interaction
- UI-state capture
