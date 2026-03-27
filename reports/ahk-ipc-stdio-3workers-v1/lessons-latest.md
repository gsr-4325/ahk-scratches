# Latest lessons snapshot for three workers

- latest workflow: AHK IPC stdio 3workers report master v1
- latest run id: 23638036258
- latest result path: reports/ahk-ipc-stdio-3workers-v1/latest.md

## Stable pitfalls to remember
- Keep the child transport script stable and reuse the known-good StdIO child before changing multiple layers at once.
- Worker orchestration should fail fast if a single worker misses READY or exits early.
- Keep per-worker transcript lines explicit so it is obvious which child responded.
- Default branch in this repository is `master`.

## Current run summary
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
