# StdIO echo test

## Purpose

This is the first repeatable IPC test in `ahk-scratches`.

It proves that a parent process can:

- launch an AutoHotkey child process
- wait for a ready signal
- send commands over stdin
- receive responses over stdout
- observe stderr separately
- confirm a clean child exit

## Files

- `scripts/tests/stdio/child_echo.ahk`
- `tools/test_stdio_echo.ps1`
- `.github/workflows/ahk-ipc-stdio.yml`

## Expected transcript

```text
< READY
> ping
< pong
> hello CI
< echo=hello CI
> time
< time=HH:mm:ss
> exit
< bye
```

## Artifacts

The workflow uploads these files:

- `summary.json`
- `stdout-transcript.txt`
- `stderr.txt`
- `run-metadata.txt`

## What to paste back into chat on failure

Paste these in this order:

1. workflow name and run number
2. failing step name
3. `summary.json`
4. `stdout-transcript.txt`
5. `stderr.txt`
6. the last relevant lines of the failing step log

## Why this test matters

This test is intentionally small.

Before debugging multi-worker or GUI behavior, we first want one stable IPC path that runs on a fresh Windows runner every time.
