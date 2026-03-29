# AutoHotkey Coding Standards

This document records the coding standards used in this repository.
Items that are not yet agreed should not be codified until they are decided.

## 1. General principles

This repository adopts Hungarian notation for AutoHotkey code.
Prefixes should remain minimal and practical. Use generic type prefixes plus a small number of strong, established special forms.
Meaning hints should be included whenever they materially improve readability. This principle applies to all variable names, not only collections.

## 2. One file per class

Use one file per class as the default rule.
Exceptions may exist, but the default structure is one class per file.

## 3. File naming

The file name should match the primary class name defined in that file.
Use the class name as the file name.

### Preferred

```text
TransportProfileStdIO.ahk
TransportProfileNamedPipe.ahk
WorkerSession.ahk
```

## 4. `#Include` order

Place `#Include` directives near the top of the file.
Order them from more external and foundational dependencies to more local and feature-specific ones.
Use blank lines between groups.
Within the same group, sort alphabetically whenever dependency order does not require something else.

Recommended grouping order:

1. third-party or external libraries
2. project-wide shared or core modules
3. local feature-specific modules

### Preferred

```autohotkey
#Include <ExternalLib\\JXON>
#Include <ExternalLib\\WebView2\\WebView2>

#Include Core\\Result.ahk
#Include Core\\Win32Helpers.ahk

#Include %A_ScriptDir%\\TransportProfileStdIO.ahk
#Include %A_ScriptDir%\\WorkerSession.ahk
```

## 5. Comment language

Write code comments in English.
This includes inline comments, block comments, and explanatory notes in source files.

## 6. Docblocks

Use `/** ... */` docblocks for public classes, public functions, and public methods.
Protected-like and private-like methods should use docblocks when their behavior is non-obvious or easy to misuse.
Use a lightweight tag-based format with `@` tags.
This format is concise, familiar, easy to scan, and easy to search.

The first non-empty line inside the docblock should be a short purpose statement.
Use the following tags when applicable:

- `@param`
- `@returns`
- `@throws`
- `@since`
- `@remarks` optional

Use `@since x.y.z` to record the first version that introduced the documented class, function, or method.
Use `@returns {Void}` when the routine does not return a meaningful value.
Use `@throws None.` only when explicit clarification is valuable. Otherwise omit `@throws` when no intentional exception contract exists.

### Preferred

```autohotkey
/**
 * Get the worker state for a given worker ID.
 *
 * @param {Integer} iWorkerID Worker ID.
 * @returns {String} Current worker state.
 * @throws {Error} Thrown when the worker registry is not initialized.
 * @since 1.2.4
 */
GetWorkerState(iWorkerID) {
    if ( !IsObject(g_mWorkersByID) ) {
        throw Error("Worker registry is not initialized.")
    }

    return g_mWorkersByID[iWorkerID].state
}
```

```autohotkey
/**
 * Transport profile for StdIO-based communication.
 *
 * @since 1.3.0
 * @remarks Thin transport profile for child-process I/O.
 */
class TransportProfileStdIO {
}
```

## 7. Local variables

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

## 8. Global variables

User-defined global variables must start with `g_`.
User-defined superglobals use the same `g_` form. They do not get a separate special notation.
Built-in superglobals such as `A_ScriptDir` keep their built-in names.

### Preferred

```autohotkey
g_mWorkersByID := Map()
g_sPathConfig := ""
g_fnOnMessage := 0
```

## 9. Local static variables

Function-local `static` variables also use `_`.
A `static` variable has a longer lifetime, but its scope is still local to that function.

### Example

```autohotkey
GetCacheValue(sKey) {
    static _mCache := Map()

    return _mCache.Has(sKey) ? _mCache[sKey] : ""
}
```

## 10. Constant-like values

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

## 11. Keyword casing

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

## 12. Nested functions

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

## 13. Pseudo-visibility for class methods

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

## 14. Ordering of words in names

When similar classes or variables appear together in the same directory or context, put the shared category first and the distinguishing trait later.
In class names, the common base concept should come first.
In variable names, after the Hungarian prefix, the common category should come first.

### Avoid

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

### Preferred

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

## 15. Function and method style

Function names and method names use PascalCase.
This keeps them visually distinct from variables and works naturally with forms such as `GetSomething()` and `SetSomething()`.

### Preferred

```autohotkey
GetWindowTitle()
SetWorkerState(sState)
RunWorker()
OnMessage(wParam, lParam, msg, hWnd)
```

## 16. Function and method semantics

Functions and methods whose primary purpose is to obtain and return a value should start with `Get` whenever practical.
Within that `Get`-based form, choose the remainder of the name so that it reads as naturally as possible.
Past participles may be used when they help keep a `Get` name natural and clear.
Functions and methods that change object state should use `Set`.
Other actions should use a concrete verb rather than a generic `Do` prefix.
Event handlers and callback entry points may use `On`.

`Get` is the default rule for value-returning methods, but there are two explicit exceptions.
The first exception is a thin wrapper around an external API, especially a Win32 or `DllCall` boundary, where preserving the original API verb is more important than forcing `Get`.
The second exception is an operation-centric method whose main meaning is the operation itself, such as `Read`, `Create`, `Open`, `Parse`, `Build`, `Join`, `Encode`, `Decode`, `Send`, or `Receive`, even when that operation returns a value.

### Preferred

```autohotkey
GetWindowTitle()
GetWorkerState()
GetStringJoined(sString)
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

## 17. Abbreviation casing

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

## 18. Prefix usage

### 18.1 Generic type prefixes

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

### 18.2 `cb`

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

### 18.3 `Path` and `URL`

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

### 18.4 Time units

`ms` is not a special prefix.
Represent the actual data type first, then place the time unit at the end of the identifier.

### Preferred

```autohotkey
iTimeoutMS
fElapsedMS
iRetryDelayMS
```

### 18.5 `PID`, handle, and pointer

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

### 18.6 Compound types

When the number of intended type combinations is small and a compound prefix remains readable, a compound prefix is allowed.
When the combinations become broad or the compound prefix becomes harder to read, use `v` instead.
No strict numeric threshold is imposed. Final choice is left to the coder's judgment.

### Examples

```autohotkey
_aiSelection
_asTokenOrList
vPayload
```

### 18.7 `DllCall` wrapper naming

Thin wrappers around Win32 or other external APIs should preserve the original API name as closely as practical.
Do not mechanically force `Get` onto a thin wrapper only because it returns a value.
Higher-level wrappers should be named by their primary meaning.
If the method is a true accessor or retrieval helper, prefer `Get`.
If the method is fundamentally an operation such as reading, creating, opening, parsing, building, encoding, decoding, sending, or receiving, keep the operation verb.

### Preferred

```autohotkey
_CreateNamedPipe()
_ReadFile()
_GetWindowThreadProcessID()
CreateWorkerPipe()
ReadPipeText()
ParseConfigText()
BuildWorkerMap()
GetWorkerState()
GetReadBufferSize()
```

## 19. Meaning hints in names

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

## 20. Braces

Do not omit `{}` for conditional blocks.
For classes, functions, methods, and conditional blocks, the opening brace must be on the same line as the declaration or condition.
This repository uses OTD/K&R style for opening braces.

### Avoid

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

### Preferred

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

## 21. Comparison order in conditions

When comparing a fixed value and a variable with `==` or similar operators, place the fixed value on the left and the variable on the right.
This repository adopts Yoda condition style for such comparisons.

### Avoid

```autohotkey
if ( iValue == 4 ) {
}
```

### Preferred

```autohotkey
if ( 4 == iValue ) {
}
```

## 22. Early return

For methods and functions that return a value, prefer early return and guard clauses.
Do not delay the return value unnecessarily by wrapping the main logic inside deep conditional blocks.
Use early return to keep the main path short and visible.

### Avoid

```autohotkey
GetUserLabel(userId) {
    if ( UserExists(userId) ) {
        if ( UserHasLabel(userId) ) {
            return LoadUserLabel(userId)
        }
    }

    return ""
}
```

### Preferred

```autohotkey
GetUserLabel(userId) {
    if ( !UserExists(userId) ) {
        return ""
    }

    if ( !UserHasLabel(userId) ) {
        return ""
    }

    return LoadUserLabel(userId)
}
```

## 23. Conditional nesting

Avoid nested conditional blocks whenever practical.
Keep `if` block depth to one level whenever possible.
If the logic would grow into two or more nested levels, extract a helper method or a nested function.

### Avoid

```autohotkey
DoSomething(sValue) {
    if ( bSomething ) {
        if ( bAnother ) {
            if ( bYetAnother ) {
                ; yet do other thing here
            }

            ; do another thing here
        }

        ; do something here
    }
}
```

### Preferred

```autohotkey
DoSomething(sValue) {
    if ( !bSomething ) {
        return
    }

    _DoAnother()
    ; do something here

    _DoAnother() {
        if ( !bAnother ) {
            return
        }

        if ( bYetAnother ) {
            ; yet do other thing here
        }

        ; do another thing here
    }
}
```

## 24. Error handling policy

Use `throw` for contract violations, internal inconsistencies, and Win32 or `DllCall` failures.
Use return values for expected absence, lookup misses, or other normal non-exceptional cases.
Do not use ambiguous sentinel values when they can be confused with a valid result.
When a return-value-based miss is used, choose a result that is natural for the API and document the behavior clearly.

### Preferred

```autohotkey
GetPipeHandle(sPipeName) {
    _hPipe := _CreateNamedPipe(sPipeName)
    if ( !_hPipe ) {
        throw Error("Failed to create named pipe.")
    }

    return _hPipe
}
```

```autohotkey
FindWorkerByID(iWorkerID) {
    if ( !g_mWorkersByID.Has(iWorkerID) ) {
        return ""
    }

    return g_mWorkersByID[iWorkerID]
}
```

## 25. Trailing commas

Trailing commas are allowed in multi-line `Array(...)`, `Map(...)`, and argument lists where the language syntax permits them.
Use them to keep diffs smaller and make future additions cleaner.

### Preferred

```autohotkey
_aItems := Array(
    "one",
    "two",
    "three",
)

_mOptions := Map(
    "timeout", 5000,
    "retry", 3,
)

RunTask(
    sName,
    iTimeoutMS,
    bForce,
)
```

## 26. Combined naming pattern

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

## 27. Not yet codified

The following topics are intentionally left undecided for now.

- none at the moment

Add new items here only when a topic is intentionally left open.
