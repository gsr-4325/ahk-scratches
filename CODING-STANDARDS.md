# AHK Coding Standards

このドキュメントは、現時点で合意できた事項だけを記録する初版です。
未確定の命名辞書や細部ルールは、ここにはまだ書かない。

## 1. 基本方針

このリポジトリでは、AutoHotkey コードにハンガリアンノーテーションを採用する。
ただし、具体的な prefix 辞書や細分類は未確定のものがあるため、現時点では確定済みのルールだけを適用する。

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

## 3. ネストされた関数

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

## 4. 値を返す関数名

値を取得して返す目的の関数名は、可能な限り `Get` で始める。
読み手に「状態変更ではなく取得である」ことを明示するためである。

### Preferred

```autohotkey
GetWindowTitle()
GetWorkerState()
GetConfigPath()
```

### Avoid when the intent is simple retrieval

```autohotkey
WindowTitle()
WorkerState()
ConfigPath()
```

## 5. 状態を変更する関数名

クラスのプロパティや内部状態を変更する関数名は `Set` で始める。
読み手に「取得ではなく変更である」ことを一目で伝えるためである。

### Preferred

```autohotkey
SetWindowTitle(sTitle)
SetWorkerState(sState)
SetRetryLimit(iLimit)
```

## 6. 命名の組み合わせ方

ローカル変数でハンガリアンノーテーションを使う場合は、`_` を最初に置き、その後ろにハンガリアンの接頭辞を続ける。

### Examples

```autohotkey
_sName
_iCount
_bIsPaused
_mUsersById
```

## 7. 現時点で未記載のもの

以下はまだ確定していないため、この版では規約化しない。

- boolean 命名の細部
- `cb` と `fn` の使い分け
- `pid` / `hWnd` / `ptr` などの専用 prefix の最終表記
- 複合型や variant 系の prefix
- ローカル `static` の扱い
- collection 名にアクセス方法をどこまで必須化するか

今後、合意できたものから順次このドキュメントへ追記する。
