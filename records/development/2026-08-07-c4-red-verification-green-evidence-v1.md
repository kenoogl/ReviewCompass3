# 層1・C-4 `red_now`実行照合 GREEN Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-VERIFICATION-BOUNDARY-001`（層1、最優先）
- 対応表：`records/development/2026-08-07-c4-red-verification-declaration-red-map-v1.json`
- 実装前検索：`records/development/2026-08-07-c4-red-verification-reuse-search-attestation-v1.json`
  （gate `assessed_fresh`。既存の`policy_test_runner.execute`・`pytest_summary`を発見したが、
  いずれもsuite単位でありtest単位の結果を返さないため、参照はするが直接は再利用しなかった）

## 1. 塞いだ穴

宣言→RED対応表の関門は、その名に反して**`red_now`（宣言に結ばれたtestが実際に失敗するか）を
一度も確認していなかった**（反証C-4）。REDでないものをREDと称して通せる状態であり、
「テストの無い宣言0件」という保証の質に直結していた。

`check_declaration_red_map`に`verify_red=True`経路を追加した。

- `red_now: true`の宣言は、対象testが実際に失敗（failed／error）していることを要求する
- `red_now: false`の境界例は、対象testが実際に成功していることを要求する
- 結果を得られないtestは合格と見なさず、`red_outcome_unknown`でfail-closedに拒否する
- **既定は静的検査のまま**（V1で固定）。実行は明示指定時のみで、runnerは差し替え可能

- targeted：`tests/test_declaration_red_verification.py` 5 test。RED 5/5 → GREEN 5/5。
- 公式全Test：`1101 passed`、exit `0`。

## 2. 実装中の修正1件

既定runnerの出力解析が、pytestの実際の報告形式（`PASSED <node id>`の順）と逆になっていた。
実データで自己検査したところ全件`unknown`となり判明したため、正規表現を訂正した。
**fixtureだけで検証していたら見逃していた**種類の誤りであり、実データ照合の価値を示す。

## 3. 実行照合の時点意味論（重要な発見。運用規則の提案を含む）

GREEN後に既存の対応表13枚を実行照合したところ、**`red_now: true`の宣言はすべて不一致**と
判定された【実測】。これは欠陥ではなく必然である——`red_now`はRED固定時点の主張であり、
実装が済んだ後に同じtestを走らせれば成功するのが正しいからである。

| 判定 | 意味 |
| --- | --- |
| `red_now: true`が不一致 | GREEN後の正常な状態。RED時点でのみ検証できる |
| `red_now: false`（境界例）が一致 | GREEN後も検証可能。実際6枚で`verified`が出ている |
| `unknown` | test改名・削除に対応表が追随していない（Intake v1で13件。superseded済みの歴史record） |

**したがって実行照合は「RED作業単位のcommit前」に実施すべき道具である。** 事後の再検査で
使えるのは境界例の確認だけである。次の実装単位（層1のC-1 `scope`欄以降）から、RED固定時に
`verify_red=True`で照合し、結果をRED Evidenceへ記録する運用を提案する。**この運用規則の採否は
Human判断とし、本Evidenceでは提案にとどめる。**

## 4. stale閉包

静的検査の既定挙動は変更していないため、既存対応表の静的検査結果に変化はない（前回のstale
再検査時点と同じ：現行運用中は全枚`passed`）。実行照合は新設の任意経路であり、旧合格を
無効化しない。

## 5. 残余

- 層1の残り：C-1の`scope`欄、R-3のgate再検索、C-2空文字拒否＋I-2単調性
- 層2・層3は未着手
- 実行照合の運用規則（§3）はHuman判断待ち
