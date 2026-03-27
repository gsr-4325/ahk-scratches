#Requires AutoHotkey v2.0
#SingleInstance Force

stdout := FileOpen("*", "w")
stdout.WriteLine("smoke_stdout: ok")
stdout.Close()

ExitApp 0
