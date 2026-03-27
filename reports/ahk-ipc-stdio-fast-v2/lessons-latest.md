# Latest lessons snapshot

- latest workflow: AHK IPC stdio report master v2
- latest run id: 23636989703
- latest result path: reports/ahk-ipc-stdio-fast-v2/latest.md

## Stable pitfalls to remember
- The default branch is `master`, not `main`.
- Empty stderr or other empty files in PowerShell can lead to null-valued expressions if methods like `.TrimEnd()` are called directly.
- Use the already working StdIO pair in `scripts/tests/stdio/child_echo_v2.ahk` and `tools/test_stdio_echo_py_v2.py` as the reference path before experimenting with new transport code.
- Reporting workflows should write under `reports/` and avoid triggering on `reports/**` changes.

## Current run summary
```json
{
  "passed": true,
  "timeout_seconds": 4.0,
  "child_exit_code": 0,
  "transcript_line_count": 9,
  "checks": [
    "READY",
    "ping/pong",
    "echo",
    "time",
    "exit"
  ],
  "transcript_preview": [
    "< READY",
    "> ping",
    "< pong",
    "> hello CI",
    "< echo=hello CI",
    "> time",
    "< time=08:05:32",
    "> exit",
    "< bye"
  ],
  "stderr_preview": []
}
```
