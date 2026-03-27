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
        break
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

ExitApp 1

WriteStdoutLine(text) {
    static hStdout := DllCall("Kernel32\\GetStdHandle", "int", -11, "ptr")
    payload := text "`n"
    bytesToWrite := StrPut(payload, "UTF-8") - 1
    buffer := Buffer(bytesToWrite + 1, 0)
    StrPut(payload, buffer, "UTF-8")
    bytesWritten := 0
    ok := DllCall("Kernel32\\WriteFile", "ptr", hStdout, "ptr", buffer.Ptr, "uint", bytesToWrite, "uint*", &bytesWritten, "ptr", 0, "int")
    if !ok || bytesWritten != bytesToWrite {
        throw Error("WriteFile to stdout failed")
    }
}
