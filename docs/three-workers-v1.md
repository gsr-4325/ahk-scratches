# Three workers v1

## Goal

Prove that one parent process can manage three AutoHotkey child workers over StdIO without involving any GUI.

## What this scratch validates

- all three workers start
- each worker emits `READY`
- direct messages can target one worker at a time
- a simple broadcast-style loop can send `ping` to all workers
- each worker can return a `time=` response
- all workers can cleanly shut down with exit code `0`

## Files

- `scripts/tests/stdio/child_echo_v2.ahk`
- `tools/test_stdio_three_workers_py_v1.py`
- `.github/workflows/ahk-ipc-stdio-3workers-report-master-v1.yml`

## Expected transcript shape

```text
worker-001 < READY
worker-002 < READY
worker-003 < READY
worker-001 > hello one
worker-001 < echo=hello one
worker-002 > hello two
worker-002 < echo=hello two
worker-003 > hello three
worker-003 < echo=hello three
worker-001 > ping
worker-001 < pong
...
worker-003 > exit
worker-003 < bye
```

## Published report

The reporting workflow writes the latest result under:

- `reports/ahk-ipc-stdio-3workers-v1/latest.md`
- `reports/ahk-ipc-stdio-3workers-v1/latest.json`
- `reports/ahk-ipc-stdio-3workers-v1/lessons-latest.md`
