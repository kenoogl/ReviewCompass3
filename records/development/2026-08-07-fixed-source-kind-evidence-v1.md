# 固定sourceの参照種別（A案）実施Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-FIXED-SOURCE-KIND-001`、`DEC-RED-VERIFICATION-ADOPTION-001`

## 1. 経緯

承認済みの手順追記（RED固定commit前の実行照合）を`docs/development/work-review-protocol.md`へ
反映したところ、Work 5B Contractがその手順書を固定sourceとして指紋束縛していたため、
`tests/test_work5b_contract.py`が`digest drift`で失敗した。**testの期待が誤りであった**——
固定sourceは作業開始時点の参照記録であり、上流の可変文書が後に改定されれば一致しなくなるのが
正常である。現行設計のままでは手順書を二度と改定できない状態だった。

深掘り停止規則（既存testの書換えが必要と判明した時点で停止しHumanへ渡す）に従い作業を止め、
A案（参照種別の導入）の裁定を得てから再開した。

## 2. 実施

**Work 5B Contract v2**（`records/development/2026-08-07-work5b-implementation-task-contract-v2.json`）
を作成した。v1は歴史recordとして保持する。

- 固定source 7件へ`reference_kind`を付けた：
  - `immutable_record` 6件（承認Decision、検索recordの証明書、対応表、RED Evidence、固定test 2件）
    → **指紋の一致を要求する**
  - `pinned_at_start` 1件（レビュー手順書）→ **実在の確認までを要求する**。改定による不一致は
    正常として扱い、noteへその旨を記した
- `reuse_search_gate`の束縛を、外部化済みの証明書経由へ揃えた（構成Cの解決経路）
- 意味内容（Work Item、禁止事項、risk、rollback）は変更していない

**test修正**：`test_contract_fixed_sources_resolve_by_reference_kind`へ改称し、種別ごとの検証へ
訂正した。あわせて`test_contract_supersedes_the_first_version`を追加し、後継関係とv1の保持を
固定した。gate束縛のtestは証明書経由の解決へ更新した。**検証を弱める変更ではなく、種別に
応じた正しい検証への訂正である。**

## 3. 生成時の自己参照（記録）

Contract v2は自身を検証するtest fileを固定sourceに含むため、test修正→v2再生成の順で収束させた。
最初の生成ではv1の値を引き継いでいたため不一致となり、`immutable_record`はv2作成時点の実値で
再計算する処理へ直した。自己参照を含むrecordの生成順序として記録に残す。

## 4. 付随して解消したこと

裁定4（`DEC-FOUR-RULINGS-2026-08-07-001`）で**削除を保留していた検索record旧位置**
（`2026-08-07-declaration-red-map-checker-reuse-search-v1.json`）は、v2が証明書参照へ移行した
ことで機械参照が0件になり、削除した。外部本体と証明書は健在である。

## 5. Test結果

公式全Test `1102 passed`、exit `0`。Contract test 6件合格。既存testを弱めていない。

## 6. 残余

- `reference_kind`は Work 5B Contract のみに導入した。他のContract・recordへの適用は必要に
  なった時点で個別に判断する（`DEC-FIXED-SOURCE-KIND-001` §4）。
- この区別は`ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`（参照Digest driftの恒久検査器）の
  判別規則の先行事例であり、同Issueの着手時に材料として参照できる。
