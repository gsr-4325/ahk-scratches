# Latest lessons snapshot for three workers

- latest workflow: AHK IPC stdio 3workers report master v3
- latest run id: 23641278927
- latest result path: reports/ahk-ipc-stdio-3workers-v3/latest.md

## Stable pitfalls to remember
- Multi-worker tests should use a child script without `#SingleInstance` and may need per-worker script copies to avoid hidden collisions.
- Child startup logs are useful when READY never arrives and stderr is empty.
- Keep per-worker transcript lines explicit so it is obvious which child responded.
- Default branch in this repository is `master`.

## Current run summary
```json
{
  "passed": true,
  "timeout_seconds": 8.0,
  "worker_count": 3,
  "worker_exit_codes": {
    "worker-001": 0,
    "worker-002": 0,
    "worker-003": 0
  },
  "transcript_line_count": 27,
  "checks": [
    "all READY",
    "direct echo to worker-001",
    "direct echo to worker-002",
    "direct echo to worker-003",
    "broadcast ping",
    "per-worker time",
    "clean shutdown"
  ],
  "transcript_preview": [
    "worker-001 < READY",
    "worker-002 < READY",
    "worker-003 < READY",
    "worker-001 > hello one",
    "worker-001 < echo=hello one",
    "worker-002 > hello two",
    "worker-002 < echo=hello two",
    "worker-003 > hello three",
    "worker-003 < echo=hello three",
    "worker-001 > ping",
    "worker-001 < pong",
    "worker-002 > ping",
    "worker-002 < pong",
    "worker-003 > ping",
    "worker-003 < pong",
    "worker-001 > time",
    "worker-001 < time=10:10:04",
    "worker-002 > time",
    "worker-002 < time=10:10:04",
    "worker-003 > time",
    "worker-003 < time=10:10:04",
    "worker-001 > exit",
    "worker-001 < bye",
    "worker-002 > exit",
    "worker-002 < bye",
    "worker-003 > exit",
    "worker-003 < bye"
  ],
  "stderr_preview": [],
  "child_logs_preview": [
    "[worker-001]",
    "﻿2026-03-27 10:10:03 | START pid=2084 worker=worker-001",
    "2026-03-27 10:10:03 | STDIN_OPENED",
    "2026-03-27 10:10:03 | READY_SENT",
    "2026-03-27 10:10:04 | RECV hello one",
    "2026-03-27 10:10:04 | RECV ping",
    "2026-03-27 10:10:04 | RECV time",
    "2026-03-27 10:10:04 | RECV exit",
    "2026-03-27 10:10:04 | EXIT_CMD",
    "[worker-002]",
    "﻿2026-03-27 10:10:04 | START pid=2948 worker=worker-002",
    "2026-03-27 10:10:04 | STDIN_OPENED",
    "2026-03-27 10:10:04 | READY_SENT",
    "2026-03-27 10:10:04 | RECV hello two",
    "2026-03-27 10:10:04 | RECV ping",
    "2026-03-27 10:10:04 | RECV time",
    "2026-03-27 10:10:04 | RECV exit",
    "2026-03-27 10:10:04 | EXIT_CMD",
    "[worker-003]",
    "﻿2026-03-27 10:10:04 | START pid=8560 worker=worker-003",
    "2026-03-27 10:10:04 | STDIN_OPENED",
    "2026-03-27 10:10:04 | READY_SENT",
    "2026-03-27 10:10:04 | RECV hello three",
    "2026-03-27 10:10:04 | RECV ping",
    "2026-03-27 10:10:04 | RECV time",
    "2026-03-27 10:10:04 | RECV exit",
    "2026-03-27 10:10:04 | EXIT_CMD"
  ]
}
```
