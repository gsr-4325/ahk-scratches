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

## 3. global 変数

ユーザー定義の global 変数には `g_` を付ける。
ユーザー定義の superglobal も、特別な別表記にはせず、同じく `g_` を使う。
`A_ScriptDir` などの組み込み superglobal は、そのまま組み込み表記を使う。

### Preferred

```autohotkey
g_mWorkersByID := Map()
g_sPathConfig := ""
g_fnOnMessage := 0
```

## 4. ローカル static 変数

関数内の `static` 変数にも `_` を付ける。
`static` は寿命は長いが、スコープはその関数のローカルだからである。

### Example

```autohotkey
GetCacheValue(sKey) {
    static _mCache := Map()

    return _mCache.Has(sKey) ? _mCache[sKey] : ""
}
```

## 5. 定数的な値

AutoHotkey には一般的な意味での定数がないが、意味的に不変として扱う値は定数的な表記にする。
マジックナンバーやマジック文字列は、意味があるものや再利用されるものは名前を与える。
定数的な値の名前は `UPPER_SNAKE_CASE` を使う。

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

## 6. キーワードの大文字小文字

`if`、`for`、`return`、`loop`、`try`、`catch`、`class`、`static`、`global` などのキーワードは小文字で統一する。
関数名、メソッド名、クラス名との見分けを良くし、見た目の一貫性を保つためである。

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

## 7. ネストされた関数

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

## 8. クラス名と変数名の語順

同一ディレクトリや同一文脈で、同種のクラスや変数が並ぶことを想定し、共通の役割やカテゴリを先に置き、区別要素は後ろに置く。
クラス名では共通のベース概念を先頭に置き、差異となる特性は接尾に置く。
変数名でも、接頭辞の後ろでは `Url` や `Path` のような共通カテゴリを先に置く。

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

## 9. 関数名とメソッド名のスタイル

関数名とメソッド名は PascalCase を使う。
変数名とは見た目を分け、`GetSomething()` や `SetSomething()` の形を揃えやすくするためである。

### Preferred

```autohotkey
GetWindowTitle()
SetWorkerState(sState)
RunWorker()
OnMessage(wParam, lParam, msg, hWnd)
```

## 10. 関数名とメソッド名の意味分類

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

## 11. 略語の大文字表記

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

## 12. prefix の扱い

### 12.1 汎用型 prefix

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

### 12.2 `cb` の意味

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

### 12.3 Path と URL

`Path` と `URL` は専用 prefix にしない。
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

### 12.4 時間単位

`ms` は専用 prefix にしない。
時間値はまず実データ型を prefix で表し、単位は識別子の末尾に付ける。

### Preferred

```autohotkey
iTimeoutMS
fElapsedMS
iRetryDelayMS
```

### 12.5 PID, handle, pointer

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

### 12.6 複合型

複合型で、想定する型の組み合わせが少なく、複合 prefix に意味がある場合は、複合 prefix を使ってよい。
組み合わせが多い場合や、複合 prefix がかえって読みにくい場合は `v` を使う。
ただし、ここに厳密な数値基準は設けず、最終的にはコーダーの裁量に委ねる。

### Examples

```autohotkey
_aiSelection
_asTokenOrList
vPayload
```

## 13. ブレースの書き方

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

## 14. 条件式での比較順序

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

## 15. 命名の組み合わせ方

ローカル変数でハンガリアンノーテーションを使う場合は、`_` を最初に置き、その後ろにハンガリアンの接頭辞を続ける。
global 変数は `g_` を最初に置き、その後ろにハンガリアンの接頭辞を続ける。

### Examples

```autohotkey
_sName
_iCount
_bPaused
_mUsersByID
_iPIDWorker
_sPathConfig
_iTimeoutMS
g_sUrlBase
g_mWorkersByID
```

## 16. 現時点で未記載のもの

以下はまだ確定していないため、この版では規約化しない。

- collection 名に、lookup の基準や並び順の意味をどこまで含めるか

今後、合意できたものから順次このドキュメントへ追記する。
