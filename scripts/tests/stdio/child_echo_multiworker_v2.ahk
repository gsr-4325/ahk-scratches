#Requires AutoHotkey v2.0

workerId := A_Args.Length >= 1 ? A_Args[1] : "worker-unknown"
logPath := A_Args.Length >= 2 ? A_Args[2] : ""

LogLine("START pid=" ProcessExist() " worker=" workerId)

stdin := FileOpen("*", "r", "UTF-8")
if !IsObject(stdin) {
    LogLine("STDIN_OPEN_FAILED")
    throw Error("Failed to open stdin stream")
}
LogLine("STDIN_OPENED")

WriteStdoutLine("READY")
LogLine("READY_SENT")

loop {
    line := stdin.ReadLine()
    if (line = "" && stdin.AtEOF) {
        LogLine("EOF_EXIT")
        ExitApp 0
    }

    line := RTrim(line, "`r`n")
    LogLine("RECV " line)

    switch line {
        case "ping":
            WriteStdoutLine("pong")
        case "time":
            WriteStdoutLine("time=" FormatTime(, "HH:mm:ss"))
        case "exit":
            WriteStdoutLine("bye")
            LogLine("EXIT_CMD")
            ExitApp 0
        default:
            WriteStdoutLine("echo=" line)
    }
}

WriteStdoutLine(text) {
    stdout := FileOpen("*", "w", "UTF-8")
    if !IsObject(stdout) {
        throw Error("Failed to open stdout stream")
    }
    stdout.Write(text "`n")
    stdout.Close()
}

LogLine(text) {
    global logPath
    if (logPath = "") {
        return
    }
    try {
        FileAppend(FormatTime(, "yyyy-MM-dd HH:mm:ss") " | " text "`n", logPath, "UTF-8")
    }
}
