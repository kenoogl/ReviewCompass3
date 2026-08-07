# 固定sourceの参照種別の区別（A案）承認Decision v1

- decision ID：`DEC-FIXED-SOURCE-KIND-001`
- decision maker：Human
- decided at：2026-08-07
- 指示：本sessionのHuman文言「A案」（2026-08-07。手順書追記がWork 5B Contract testを壊した
  報告への裁定）

## 1. 背景

`DEC-RED-VERIFICATION-ADOPTION-001`に基づき`docs/development/work-review-protocol.md`へ手順を
追記したところ、`tests/test_work5b_contract.py::test_contract_fixed_sources_resolve_and_match`が
`digest drift`で失敗した。Work 5B Contract（`TC-WORK5B-DECLARATION-RED-MAP-CHECK-001`）が
手順書を固定sourceとして指紋束縛し、testが「常に一致すること」を要求していたためである。

**testの期待が誤りであった。** 固定sourceは作業開始時点の参照記録であり、上流の可変文書が
その後改定されれば一致しなくなるのが正常である。現行設計のままでは手順書を改定できない。

## 2. Humanの決定（A案）

固定sourceに**参照種別**を導入し、種別ごとに検証を変える。

- `immutable_record`：不変record（Decision、Evidence、対応表、検索record、固定test）。
  作業後に変わったら異常であり、**指紋の一致を要求する**。
- `pinned_at_start`：時点固定の可変文書（手順書、方針、計画などの上流文書）。作業開始時点の
  姿を記録するだけであり、**実在の確認までを要求し、指紋の不一致は正常な改定として扱う**。
  現行の姿との差は、必要なときにHumanが確認する対象とする。

この区別は、`ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`が扱う「現在有効な参照」と
「生成時点の固定」の区別と同じ構造であり、恒久検査器の判別規則の先行事例となる。

## 3. 実施

1. Work 5B Contractの後継版**v2**を作成し、各固定sourceへ`reference_kind`を付ける。
   意味内容（結線先、Work Item、禁止事項）は変更しない。v1は歴史recordとして保持する。
2. `tests/test_work5b_contract.py`の期待を種別に沿って修正する。`immutable_record`は
   指紋一致、`pinned_at_start`は実在確認とする。**検証を弱める方向の変更ではなく、
   種別に応じた正しい検証への訂正である。**
3. Contract v2作成に伴い、v1が固定sourceとしていた検索record旧位置
   （`2026-08-07-declaration-red-map-checker-reuse-search-v1.json`、裁定4で削除保留したもの）は、
   v2では証明書参照へ置き換える。これにより保留していた削除が可能になる。

## 4. この決定が承認していないこと

- 恒久検査器の実装（`ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`の着手はHuman判断のまま）
- 他のContract・recordへの`reference_kind`の一括適用（必要になった時点で個別に判断する）
- Work 5Bの段完了の取り消し（v2はContract記録の形式訂正であり、完了判断を変えない）
