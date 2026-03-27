# AHK IPC stdio 3workers latest report

- workflow: AHK IPC stdio 3workers report master v3
- run id: 23641278927
- run attempt: 1
- ref: refs/heads/master
- sha: 40a58eec5495e0ec0ced77086a11819a9ce88181

## summary.json
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

## stdout-transcript.txt
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
worker-002 > ping
worker-002 < pong
worker-003 > ping
worker-003 < pong
worker-001 > time
worker-001 < time=10:10:04
worker-002 > time
worker-002 < time=10:10:04
worker-003 > time
worker-003 < time=10:10:04
worker-001 > exit
worker-001 < bye
worker-002 > exit
worker-002 < bye
worker-003 > exit
worker-003 < bye
```

## stderr.txt
```text

```

## run-metadata.txt
```text
timestamp_utc=2026-03-27T10:10:03Z
ahk_exe=D:\a\_temp\AutoHotkey\AutoHotkey64.exe
child_template_path=D:\a\ahk-scratches\ahk-scratches\scripts\tests\stdio\child_echo_multiworker_v2.ahk
timeout_seconds=8.0
worker_count=3
worker-001.pid=2084
worker-001.script=D:\a\ahk-scratches\ahk-scratches\artifacts-ipc-3workers-report-master-v3\runtime-workers\worker-001.ahk
worker-001.log=D:\a\ahk-scratches\ahk-scratches\artifacts-ipc-3workers-report-master-v3\runtime-workers\worker-001.log
worker-002.pid=2948
worker-002.script=D:\a\ahk-scratches\ahk-scratches\artifacts-ipc-3workers-report-master-v3\runtime-workers\worker-002.ahk
worker-002.log=D:\a\ahk-scratches\ahk-scratches\artifacts-ipc-3workers-report-master-v3\runtime-workers\worker-002.log
worker-003.pid=8560
worker-003.script=D:\a\ahk-scratches\ahk-scratches\artifacts-ipc-3workers-report-master-v3\runtime-workers\worker-003.ahk
worker-003.log=D:\a\ahk-scratches\ahk-scratches\artifacts-ipc-3workers-report-master-v3\runtime-workers\worker-003.log
worker-001.exit_code=0
worker-002.exit_code=0
worker-003.exit_code=0
```

## child-logs.txt
```text
[worker-001]
﻿2026-03-27 10:10:03 | START pid=2084 worker=worker-001
2026-03-27 10:10:03 | STDIN_OPENED
2026-03-27 10:10:03 | READY_SENT
2026-03-27 10:10:04 | RECV hello one
2026-03-27 10:10:04 | RECV ping
2026-03-27 10:10:04 | RECV time
2026-03-27 10:10:04 | RECV exit
2026-03-27 10:10:04 | EXIT_CMD
[worker-002]
﻿2026-03-27 10:10:04 | START pid=2948 worker=worker-002
2026-03-27 10:10:04 | STDIN_OPENED
2026-03-27 10:10:04 | READY_SENT
2026-03-27 10:10:04 | RECV hello two
2026-03-27 10:10:04 | RECV ping
2026-03-27 10:10:04 | RECV time
2026-03-27 10:10:04 | RECV exit
2026-03-27 10:10:04 | EXIT_CMD
[worker-003]
﻿2026-03-27 10:10:04 | START pid=8560 worker=worker-003
2026-03-27 10:10:04 | STDIN_OPENED
2026-03-27 10:10:04 | READY_SENT
2026-03-27 10:10:04 | RECV hello three
2026-03-27 10:10:04 | RECV ping
2026-03-27 10:10:04 | RECV time
2026-03-27 10:10:04 | RECV exit
2026-03-27 10:10:04 | EXIT_CMD
```
