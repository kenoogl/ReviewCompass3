# 一件の設計・受入条件照合 契約候補v1 内部反証 v1

- 実施日：2026-08-15
- 対象契約：`TC-RC3-PRODUCT-ONE-DESIGN-ACCEPTANCE-CONFORMANCE-004` version 1
- 対象path：`records/task-contract/2026-08-15-one-design-acceptance-conformance-candidate-v1.md`
- 対象SHA-256：`1640ebbfd1ff5d01e4410b43de6c503da8dd0b402bc47d4f96534cbcdf71f52f`
- 対象commit：`087f7b81d58abc13c0d25aa151119f31ae1b2546`
- 確認種別：作成担当による内部反証。独立確認の代わりにはしない
- 判定：`correction_required_before_independent_review`

## 1. 目的

別担当の独立確認へ渡す前に、固定した判定規則へ具体的な反例を当て、実装者の後決め、誤分類、
利用者が直し方を判断できない停止表示を減らす。

## 2. 止める原因

### 原因1：同じsubjectの条件同士が矛盾できる

候補v1は、同じ`subject`へ複数条件を許している。次の二条件は同時に成立しない。

- `C-1`: `mode equals safe`
- `C-2`: `mode equals fast`

`.venv/bin/python3 -c`で設計値を`safe`、`fast`、`other`に変えて全条件成立の有無を列挙した。

- 終了コード：0
- `safe`で成立：`C-1`だけ
- `fast`で成立：`C-2`だけ
- `other`で成立：0件
- 全条件を同時に満たす設計値：なし

【判断】この入力では受入条件集合自身が競合している。しかし候補v1は、どの設計値でも一部条件を
`contradicted`として設計側の照合結果へ混ぜ、条件集合の競合を区別しない。最初の一件では
`subject`を受入条件内でも一意にし、競合する複数条件を入力不正として止めるのが最小である。

### 原因2：symlink非追跡読取りの利用時点が未固定

候補v1は、rootからfileまでにsymlinkがないことと、symlinkを追跡しない読取りを要求する。しかし、
各構成要素をdirectory file descriptorから相対的に開くこと、`O_NOFOLLOW`相当、open後の通常file・size確認、
読取り前後の同一性確認を受入条件へ固定していない。

【判断】文字列pathの事前確認後に対象を差し替える競合を実装者が見逃し得る。既に一件レビュー処理で使った
狭い読取り境界を、本契約の前提、許可能力、受入条件へ明記する必要がある。

### 原因3：停止結果だけでは安全な修正先が分からない

候補v1の停止結果は`reason: invalid_schema`までしか返さない。同じ理由が設計JSONと受入条件JSONの
どちらにも生じるため、利用者は入力値やpathを表示しなくても、どちらを直すべきか判断できない。

【判断】停止結果へ閉じた語彙の`source`を追加し、`arguments`、`design`、`acceptance`、`none`のいずれかだけを
返すべきである。値、項目名、path、例外本文は返さないため、情報露出を増やさず裁定負荷を下げられる。

## 3. 限定訂正

候補v2では次だけを変える。

1. 受入条件の`subject`を一意にし、重複を`invalid_schema`で停止する。
2. rootからfileまでの全構成要素をdirectory file descriptorから相対的かつsymlink非追跡で開き、open後と
   読取り前後に種類、size、同一性を確認する。
3. 停止結果へ閉じた`source`を追加し、安全な4値と理由の対応を固定する。
4. 上記3件に対応する失敗試験を受入条件へ追加する。

設計事実、4比較、正常結果、案C、既存G08非変更、通信・保存・外部process禁止は変えない。

## 4. 未実施

【未実施】本記録は独立確認ではない。契約採用、実装、既存G08変更、外部送信、保存、製品受入は行っていない。
