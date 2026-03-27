# Three workers v3

## Why v3 exists

Even after removing `#SingleInstance Force`, the third worker still failed to reach `READY` on the hosted runner.

Version 3 makes each worker use:

- its own copied script file name
- its own child log file
- a small stagger between launches

This helps avoid hidden collisions and gives much better startup diagnostics.

## Files

- `scripts/tests/stdio/child_echo_multiworker_v2.ahk`
- `tools/test_stdio_three_workers_py_v3.py`
- `.github/workflows/ahk-ipc-stdio-3workers-report-master-v3.yml`

## Published report

- `reports/ahk-ipc-stdio-3workers-v3/latest.md`
- `reports/ahk-ipc-stdio-3workers-v3/lessons-latest.md`
