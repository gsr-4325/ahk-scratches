# Agent pitfalls

This file records practical issues that repeatedly caused avoidable failures in this repository.

## Branch name

The default branch is `master`.

Do not assume `main`.

This matters for:

- workflow checkout expectations
- push targets in report publishing steps
- links shown in summaries

## Empty stderr / empty files in PowerShell

`Get-Content -Raw` on an empty file can behave like a null-valued expression in later method calls.

If you call `.TrimEnd()` directly on such a value, the publish step can fail even when the test itself passed.

Safer pattern:

```powershell
[string]$stderrText = if (Test-Path -LiteralPath $stderrPath) {
  (Get-Content -LiteralPath $stderrPath -Raw)
} else {
  ''
}
```

## AutoHotkey stdout / console output

Console and stdout behavior is a common stumbling point.

For CI, prefer the patterns that have already been proven in this repo instead of inventing a new output method each time.

For the current working StdIO child test, see:

- `scripts/tests/stdio/child_echo_v2.ahk`
- `tools/test_stdio_echo_py_v2.py`

## Keep test surfaces small

When an AHK script fails, the first stable milestone is usually:

- syntax is valid
- child starts
- READY is emitted
- a tiny transcript succeeds

Build from there.

## Report publishing should be boring

Publishing the latest report should:

- write to `reports/...`
- avoid null-sensitive string handling
- commit only when files changed
- push to `master`
- avoid path filters that would recursively trigger itself
