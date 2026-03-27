# AHK IPC stdio 3workers latest report

- workflow: AHK IPC stdio 3workers report master v2
- run id: 23640294233
- run attempt: 1
- ref: refs/heads/master
- sha: 05c015e887761a51aeeed05b68bd5764b4ff1469

## summary.json
```json
{
  "passed": false,
  "error": "Timeout waiting for READY from worker-003 after 6.0s; child_exit=None stderr=''",
  "timeout_seconds": 6.0,
  "worker_count": 3,
  "worker_exit_codes": {
    "worker-001": 1,
    "worker-002": 1,
    "worker-003": 1
  },
  "transcript_line_count": 2,
  "transcript_preview": [
    "worker-001 < READY",
    "worker-002 < READY"
  ],
  "stderr_preview": []
}
```

## stdout-transcript.txt
```text
worker-001 < READY
worker-002 < READY
```

## stderr.txt
```text

```

## run-metadata.txt
```text
timestamp_utc=2026-03-27T09:43:02Z
ahk_exe=D:\a\_temp\AutoHotkey\AutoHotkey64.exe
child_path=D:\a\ahk-scratches\ahk-scratches\scripts\tests\stdio\child_echo_multiworker_v1.ahk
timeout_seconds=6.0
worker_count=3
worker-001.pid=1228
worker-002.pid=8280
worker-003.pid=8276
worker-001.exit_code=1
worker-002.exit_code=1
worker-003.exit_code=1
```
