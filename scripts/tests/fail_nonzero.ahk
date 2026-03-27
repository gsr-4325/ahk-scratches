#Requires AutoHotkey v2.0
#SingleInstance Force

FileAppend("fail_nonzero: about to throw`n", "*")
throw Error("Intentional failure for CI plumbing")
