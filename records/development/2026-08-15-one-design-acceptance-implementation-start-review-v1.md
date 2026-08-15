# 一件の設計・受入条件照合 実装開始前独立確認 v1

- 実施日：2026-08-15
- 対象commit：`2a5391a8abeeff826c963b25a45e6a8065d28e6e`
- 対象作業票：`docs/development/2026-08-15-one-design-acceptance-implementation-work-ticket-v1.md`
- 対象SHA-256：`e67bf0f286c4bbfe79edd16fcab2b2f2b30f7d196f2ea54c0c65458061b7154a`
- 確認担当：契約作成・作業票作成担当とは別のAI実行単位
- 確認方法：読取り専用
- 判定：`correction_required`
- 止める原因：1件
- 未接続条件：12
- 欠番・重複：0件

## 1. 停止原因

採用契約は、設計fileだけに確定した読取不能を`source: design`、受入条件fileだけなら
`source: acceptance`、入力fileを特定できない読取失敗だけを`source: none`と定めている。

作業票v1の境界3は、size、UTF-8、schema不正を設計側・受入条件側に分け、特定不能の読取失敗と
内部失敗も持つ。しかし、設計側または受入条件側に確定した`unreadable_input`の失敗例がない。

【実測】`unreadable_input`を常に`source: none`へ変える欠陥分類を機械模擬した。この欠陥は作業票v1に
明記された境界3の全例を通過し、次の2例を誤分類した。終了コードは0だった。

```json
{
  "contract_counterexamples_missed": {
    "acceptance": true,
    "design": true
  },
  "mutant_passes_all_explicit_boundary3_witnesses": true
}
```

【判断】契約条件12の誤合格を許す。境界3の先行失敗試験へ次の2件だけを追加する。

1. 設計fileに確定したopen失敗は`reason: unreadable_input`、`source: design`。
2. 受入条件fileに確定したopen失敗は`reason: unreadable_input`、`source: acceptance`。

権限状態へ依存させず、対象fileのopen失敗を試験用差替えで起こす。

## 2. 問題がなかった箇所

【実測】

- 4境界全てに利用者向け意味、先行失敗試験、最小実装、不変条件がある。
- 契約条件1〜20は一度ずつ並び、欠番・重複0件。
- 4比較の成立・不成立と型違いは、4欠陥を全て検出。終了コード0。
- root、事実、条件、escape復号後のJSON同名項目反例は接続済み。終了コード0。
- 入力rootの親symlinkは`/`からの要素別読取りで拒否できる計画。終了コード0。
- 禁止作用と、禁止作用を検出する試験用差替えが接続済み。
- 失敗確認後の実装、境界別commit、戻せる地点が明記済み。
- 既存G08の4 fileは基準commitから差分0。
- 既存G08関連試験31件成功、終了コード0。
- 契約と採用判断の参照SHA-256一致。
- 終了時HEADは対象commitと一致し、作業場所は未変更。

## 3. 次

【判断】条件12の2失敗例だけを限定追加し、同じ独立担当が停止元表示だけを再確認する。
開始可になるまで境界1の製品試験と実装へ進まない。
