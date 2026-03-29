# AHK Coding Standards

このドキュメントは、このリポジトリで採用する AutoHotkey のコーディング規約を記録する。
未確定の論点は、確定するまで規約化しない。

## 1. 基本方針

このリポジトリでは、AutoHotkey コードにハンガリアンノーテーションを採用する。
ただし、prefix は必要最小限に絞り、汎用型 prefix と本当に意味の強い専用表記だけを使う。

## 2. ローカル変数

ローカル変数には必ず先頭に `_` を付ける。
関数パラメーターにはこのルールを適用しない。
これにより、ローカル変数とパラメーターを視覚的に区別しやすくする。

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

## 3. ローカル static 変数

関数内の `static` 変数にも `_` を付ける。
`static` は寿命は長いが、スコープはその関数のローカルだからである。

### Example

```autohotkey
GetCacheValue(sKey) {
    static _mCache := Map()

    return _mCache.Has(sKey) ? _mCache[sKey] : ""
}
```

## 4. ネストされた関数

関数内に定義するネスト関数にも先頭に `_` を付ける。
ネスト関数は外側の関数のローカルな実装要素として扱う。

### Example

```autohotkey
GetSomething() {
    return _GetValue()

    _GetValue() {
        return "something"
    }
}
```

## 5. 関数名とメソッド名のスタイル

関数名とメソッド名は PascalCase を使う。
変数名とは見た目を分け、`GetSomething()` や `SetSomething()` の形を揃えやすくするためである。

### Preferred

```autohotkey
GetWindowTitle()
SetWorkerState(sState)
RunWorker()
OnMessage(wParam, lParam, msg, hWnd)
```

## 6. 関数名とメソッド名の意味分類

値を取得して返す目的の関数名は、可能な限り `Get` で始める。
クラスのプロパティや内部状態を変更する関数名は `Set` で始める。
それ以外の処理は、`Do` のような総称 prefix を規約として強制せず、具体的な動詞で始める。
イベントハンドラやコールバックの受け口は `On` で始めてよい。

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

## 7. 略語の大文字表記

`ID`、`PID`、`URL`、`MS` のような定着した略語は、識別子の中でも大文字を維持する。
これにより、`Id` と `ID`、`Pid` と `PID` のような表記ゆれを防ぐ。

### Preferred

```autohotkey
iPIDWorker
sURLBase
GetSomethingByID()
iTimeoutMS
```

Win32 の window handle については、慣用表記として `hWnd` を使う。

### Preferred

```autohotkey
hWndMain
```

## 8. prefix の扱い

### 8.1 汎用型 prefix

現時点で採用する汎用型 prefix は次とする。

- `s`: string
- `i`: integer
- `f`: float
- `b`: boolean
- `a`: array
- `m`: map
- `o`: object
- `v`: variant / mixed
- `fn`: function reference / callback reference

### 8.2 `cb` の意味

`cb` は callback ではなく、byte count を意味する。
バイト数を表す識別子にだけ使う。
コールバック関数や関数参照には使わない。

### Preferred

```autohotkey
cbWritten
cbBuffer
_fnOnMessage
_fnOnComplete
```

### 8.3 path と URL

`path` と `URL` は専用 prefix にしない。
どちらも多くの場合 string なので、string の `s` を先頭に置き、意味語として `Path` や `URL` を続ける。
パス系の語順は `sPathDirSomething` のように、`Path` を先に置く。

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

### 8.4 時間単位

`ms` は専用 prefix にしない。
時間値はまず実データ型を prefix で表し、単位は識別子の末尾に付ける。

### Preferred

```autohotkey
iTimeoutMS
fElapsedMS
iRetryDelayMS
```

### 8.5 PID, handle, pointer

process ID は integer として扱うため、`iPID...` の形を使う。
window handle は Win32 慣用に合わせて `hWnd...` を使う。
pointer は `ptr...` を使い、`p...` には省略しない。

### Preferred

```autohotkey
iPIDWorker
hWndMain
ptrData
ptrBuffer
```

## 9. ブレースの書き方

条件ブロックでは `{}` の省略を禁止する。
クラス、関数、メソッド、条件ブロックの開始ブレースは、宣言や条件式と同じ行に置く。

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

## 10. 条件式での比較順序

`==` などで固定値と変数を比較する時は、固定値を左側、変数を右側に置く。

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

## 11. 命名の組み合わせ方

ローカル変数でハンガリアンノーテーションを使う場合は、`_` を最初に置き、その後ろにハンガリアンの接頭辞を続ける。

### Examples

```autohotkey
_sName
_iCount
_bPaused
_mUsersById
_iPIDWorker
_sPathConfig
_iTimeoutMS
```

## 12. 現時点で未記載のもの

以下はまだ確定していないため、この版では規約化しない。

- collection 名にアクセス方法をどこまで必須化するか
- 複合型を複合 prefix で表すか、`v` で表すかの最終方針

今後、合意できたものから順次このドキュメントへ追記する。
