# Three workers v2

## Why v2 exists

The first three-worker attempt reused a child script that had `#SingleInstance Force`.

That is not compatible with running several instances of the same script at the same time.

Version 2 uses a dedicated multi-worker-safe child script instead.

## Files

- `scripts/tests/stdio/child_echo_multiworker_v1.ahk`
- `tools/test_stdio_three_workers_py_v2.py`
- `.github/workflows/ahk-ipc-stdio-3workers-report-master-v2.yml`

## Expected result

- all three workers emit `READY`
- each worker answers its direct echo message
- each worker answers `ping` with `pong`
- each worker answers `time` with `time=...`
- each worker exits with code `0`

## Published report

- `reports/ahk-ipc-stdio-3workers-v2/latest.md`
- `reports/ahk-ipc-stdio-3workers-v2/lessons-latest.md`
