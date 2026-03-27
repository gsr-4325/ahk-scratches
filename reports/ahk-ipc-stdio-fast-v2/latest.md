# AHK IPC stdio latest report

- workflow: AHK IPC stdio report master v2
- run id: 23636989703
- run attempt: 1
- ref: refs/heads/master
- sha: ce1875f8580621ddecf1289ac566eddc770dd64a

## summary.json
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

## stdout-transcript.txt
```text
< READY
> ping
< pong
> hello CI
< echo=hello CI
> time
< time=08:05:32
> exit
< bye
```

## stderr.txt
```text

```

## run-metadata.txt
```text
timestamp_utc=2026-03-27T08:05:32Z
ahk_exe=D:\a\_temp\AutoHotkey\AutoHotkey64.exe
child_path=D:\a\ahk-scratches\ahk-scratches\scripts\tests\stdio\child_echo_v2.ahk
timeout_seconds=4.0
pid=3884
exit_code=0
```
