#Requires AutoHotkey v2.0
#SingleInstance Force

stdin := FileOpen("*", "r", "UTF-8")
if !IsObject(stdin) {
    throw Error("Failed to open stdin stream")
}

WriteStdoutLine("READY")

loop {
    line := stdin.ReadLine()
    if (line = "" && stdin.AtEOF) {
        ExitApp 0
    }

    line := RTrim(line, "`r`n")

    switch line {
        case "ping":
            WriteStdoutLine("pong")
        case "time":
            WriteStdoutLine("time=" FormatTime(, "HH:mm:ss"))
        case "exit":
            WriteStdoutLine("bye")
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
