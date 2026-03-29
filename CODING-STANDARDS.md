# AHK Coding Standards

This document records the coding standards used in this repository.
Items that are not yet agreed should not be codified until they are decided.

## 1. General principles

This repository adopts Hungarian notation for AutoHotkey code.
Prefixes should remain minimal and practical. Use generic type prefixes plus a small number of strong, established special forms.
Meaning hints should be included whenever they materially improve readability. This principle applies to all variable names, not only collections.

## 2. One file per class

Use one file per class as the default rule.
Exceptions may exist, but the default structure is one class per file.

## 3. Comment language

Write code comments in English.
This includes inline comments, block comments, and explanatory notes in source files.

## 4. Local variables

Local variables must start with `_`.
Function parameters do not use `_`.
This makes local variables visually distinct from parameters.

### Examples

```autohotkey
GetUserLabel(userId, sDefaultLabel := "") {
    local _sUserLabel := LoadUserLabel(userId)
    return _sUserLabel != "" ? _sUserLabel : sDefaultLabel
}
```

```autohotkey
BuildState() {
    local _mState := Map()
    local _iRetryCount := 0
    return _mState
}
```

## 5. Global variables

User-defined global variables must start with `g_`.
User-defined superglobals use the same `g_` form. They do not get a separate special notation.
Built-in superglobals such as `A_ScriptDir` keep their built-in names.

### Preferred

```autohotkey
g_mWorkersByID := Map()
g_sPathConfig := ""
g_fnOnMessage := 0
```

## 6. Local static variables

Function-local `static` variables also use `_`.
A `static` variable has a longer lifetime, but its scope is still local to that function.

### Example

```autohotkey
GetCacheValue(sKey) {
    static _mCache := Map()

    return _mCache.Has(sKey) ? _mCache[sKey] : ""
}
```

## 7. Constant-like values

AutoHotkey does not provide constants in the usual sense, but values treated as semantically immutable should use constant-like notation.
Avoid unexplained magic numbers and magic strings when the value has meaning or is reused.
Constant-like names use `UPPER_SNAKE_CASE`.

### Preferred

```autohotkey
MAX_RETRY_COUNT := 3
WM_APP_WORKER_READY := 0x8001
URL_BASE_DOCS := "https://example.com/docs"
```

### Avoid

```autohotkey
_iMaxRetryCount := 3
if ( 3 == _iRetryCount ) {
}
```

## 8. Keyword casing

Language keywords such as `if`, `for`, `return`, `loop`, `try`, `catch`, `class`, `static`, and `global` should be written in lowercase.
This improves consistency and makes keywords visually distinct from class, function, and method names.

### Preferred

```autohotkey
if ( 4 == iValue ) {
    return true
}

for _iIndex, _sItem in aItems {
    try {
        ProcessItem(_sItem)
    } catch _oErr {
        return false
    }
}
```

## 9. Nested functions

Nested functions must start with `_`.
Treat them as local implementation details of the enclosing function.

### Example

```autohotkey
GetSomething() {
    return _GetValue()

    _GetValue() {
        return "something"
    }
}
```

## 10. Pseudo-visibility for class methods

AutoHotkey does not provide `protected` or `private`, but method names should still communicate intended visibility.
Methods without a leading underscore are assumed public.
Methods with a single leading underscore are treated as protected-like.
Methods with a double leading underscore are treated as private-like.

### Example

```autohotkey
class Sample {
    GetSomething() {
    }

    _GetOverridden() {
    }

    __GetUsedOnlyInThisClass() {
    }
}
```

## 11. Ordering of words in names

When similar classes or variables appear together in the same directory or context, put the shared category first and the distinguishing trait later.
In class names, the common base concept should come first.
In variable names, after the Hungarian prefix, the common category should come first.

### Bad

```autohotkey
WindowMessageTransportProfile
StdIOTransportProfile
NamedPipeTransportProfile
```

```autohotkey
sFooUrl := ""
sFooPageAUrl := ""
sBarUrl := ""
sBarPageAUrl := ""
```

### Good

```autohotkey
TransportProfileWindowMessage
TransportProfileStdIO
TransportProfileNamedPipe
```

```autohotkey
sUrlFoo := ""
sUrlFooPageA := ""
sUrlBar := ""
sUrlBarPageA := ""
```

## 12. Function and method style

Function names and method names use PascalCase.
This keeps them visually distinct from variables and works naturally with forms such as `GetSomething()` and `SetSomething()`.

### Preferred

```autohotkey
GetWindowTitle()
SetWorkerState(sState)
RunWorker()
OnMessage(wParam, lParam, msg, hWnd)
```

## 13. Function and method semantics

Functions and methods that retrieve and return a value should use `Get` whenever it remains natural and readable.
Functions and methods that change object state should use `Set`.
Other actions should use a concrete verb rather than a generic `Do` prefix.
Event handlers and callback entry points may use `On`.
Natural English naming takes priority over mechanically forcing a `Get` form.
A name like `GetStringJoined()` is acceptable when it reads naturally, but `Get` is not mandatory if it makes the name awkward.

### Preferred

```autohotkey
GetWindowTitle()
GetWorkerState()
SetWindowTitle(sTitle)
SetRetryLimit(iLimit)
RunJob()
StartWorker()
StopWorker()
ParseConfig()
BuildWorkerMap()
OnMessage(wParam, lParam, msg, hWnd)
OnExit(ExitReason, ExitCode)
```

### Avoid

```autohotkey
WindowTitle()
WorkerState()
DoThing()
DoWork()
DoOnMessage()
```

## 14. Abbreviation casing

Established abbreviations such as `ID`, `PID`, `URL`, and `MS` keep their uppercase form inside identifiers.
This avoids drift such as `Id` vs `ID` or `Pid` vs `PID`.
For Win32 window handles, use the conventional `hWnd` form.

### Preferred

```autohotkey
iPIDWorker
sURLBase
GetSomethingByID()
iTimeoutMS
hWndMain
```

## 15. Prefix usage

### 15.1 Generic type prefixes

Use the following generic type prefixes.

- `s`: string
- `i`: integer
- `f`: float
- `b`: boolean
- `a`: array
- `m`: map
- `o`: object
- `v`: variant or mixed
- `fn`: function reference or callback reference

### 15.2 `cb`

`cb` means byte count, not callback.
Use it only for byte counts.
Do not use it for callback functions or callable references.

### Preferred

```autohotkey
cbWritten
cbBuffer
_fnOnMessage
_fnOnComplete
```

### 15.3 `Path` and `URL`

`Path` and `URL` are not special prefixes.
Most such values are strings, so use the string prefix first and then the meaning word.
For path-related names, put `Path` before finer-grained qualifiers.

### Preferred

```autohotkey
sPathConfig
sPathDirLog
sPathFileReport
sURLBase
sURLDownload
```

### Avoid

```autohotkey
sDirPathLog
sFilePathReport
```

### 15.4 Time units

`ms` is not a special prefix.
Represent the actual data type first, then place the time unit at the end of the identifier.

### Preferred

```autohotkey
iTimeoutMS
fElapsedMS
iRetryDelayMS
```

### 15.5 `PID`, handle, and pointer

Process IDs are treated as integers, so use the `iPID...` form.
Window handles use the Win32 conventional `hWnd...` form.
Pointers use `ptr...` and should not be shortened to `p...`.

### Preferred

```autohotkey
iPIDWorker
hWndMain
ptrData
ptrBuffer
```

### 15.6 Compound types

When the number of intended type combinations is small and a compound prefix remains readable, a compound prefix is allowed.
When the combinations become broad or the compound prefix becomes harder to read, use `v` instead.
No strict numeric threshold is imposed. Final choice is left to the coder's judgment.

### Examples

```autohotkey
_aiSelection
_asTokenOrList
vPayload
```

## 16. Meaning hints in names

Include concise meaning hints whenever they improve readability.
This applies to variable names in general, not only to collections.
For collections, it is recommended to include lookup keys, ordering, filtering, or selection meaning whenever practical, but this remains a recommendation rather than an absolute rule.

### Examples

```autohotkey
mUsersByID
aJobsPending
mHandlersByMessage
sPathDirLog
sUrlFooPageA
```

## 17. Braces

Do not omit `{}` for conditional blocks.
For classes, functions, methods, and conditional blocks, the opening brace must be on the same line as the declaration or condition.

### Bad

```autohotkey
if ( bSomething )
    DoSomething()
```

```autohotkey
class Something
{
}
```

```autohotkey
DoSomething()
{
}
```

### Good

```autohotkey
if ( bSomething ) {
    DoSomething()
}
```

```autohotkey
class Something {
}
```

```autohotkey
DoSomething() {
}
```

## 18. Comparison order in conditions

When comparing a fixed value and a variable with `==` or similar operators, place the fixed value on the left and the variable on the right.

### Bad

```autohotkey
if ( iValue == 4 ) {
}
```

### Good

```autohotkey
if ( 4 == iValue ) {
}
```

## 19. Combined naming pattern

For local variables, place `_` first and then the Hungarian prefix.
For global variables, place `g_` first and then the Hungarian prefix.

### Examples

```autohotkey
_sName
_iCount
_bPaused
_mUsersByID
_iPIDWorker
_sPathConfig
_iTimeoutMS
g_sURLBase
g_mWorkersByID
```

## 20. Not yet codified

The following topics are intentionally left undecided for now.

- error handling policy such as `throw` vs return-value-first
- naming rules for `DllCall` wrappers

Add them only after a concrete rule is agreed.
