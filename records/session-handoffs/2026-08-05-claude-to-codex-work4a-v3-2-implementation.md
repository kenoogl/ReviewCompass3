# Claude → Codex：Work 4A v3.2追加特徴の実装 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-work4a-v3-2-implementation.md`

## 1. commit SHA

| # | SHA | 内容 |
| --- | --- | --- |
| 1 | `74d37d8bd33bdf621ab4bc33e42d64e513ce841f` | Approve Work 4A v3.2 design amendment（`DEC-WORK4A-REBUILD-DESIGN-005`、v3.2を`approved_for_implementation`、Policy v3） |
| 2 | `4455cbd3a82838ce69e343566395cc48ca052eca` | Add Work 4A v3.2 acceptance tests（J1〜J10のRED testとRED Evidence） |
| 3 | `efde37bf7e21117f69d647a28b2b9fcbe0a7842d` | Implement Work 4A v3.2 routine profile v2（実装、GREEN Evidence、実source Profile v2 Evidence） |

commit 1と3は全testがGREENである。commit 2はRED test commitであり、
固定したJ1〜J10が`build_routine_profile_v2`未実装という期待理由で失敗することをEvidenceへ記録した。

Policy v3には、追加featureの閉じた語彙、検出範囲、意味的比較候補の上限10件、
指定された`complexity_signal`の閾値を固定した。`public_api_signal`の閾値は提案が段階数だけを
定めていたため、`high`／`low`の条件をPolicy v3で明示して固定した。

## 2. RED／GREEN／全test結果

- RED：`11 failed in 0.11s`（`AttributeError: ... has no attribute 'build_routine_profile_v2'`）
- GREEN：v3.2 acceptance `11 passed`
- 既存：v3.1 acceptance `21 passed`、v3 acceptance `22 passed`。いずれも弱めていない
- 全test：venv公式runner `724 passed`、Python 3.9.6、pytest 8.4.2、fallback false

testの調整を一件行った。`test_j7`の
`"merge" not in json.dumps(structural_match_detection)`という文字列検査を削除し、
`is_merge_conclusion is False`、`is_confirmation_hint is True`、`basis`の値検査へ置き換えた。
「統合の結論ではない」と宣言するfield名自体が`merge`を含むため、この文字列検査は
直後の値検査と同時に満たせない。受入条件J7そのものは変更しておらず、値で検査する形に強めた。
他の10件は初回作成時のままである。

## 3. 実Profile v2の統計

| 項目 | 値 |
| --- | --- |
| `profile_run_id` | `78f8b8733b3baf1bfe8bc46efaf77c498cf362eb1a44086d32f1f39efabef8e4` |
| `observation_snapshot_id` | `7d9522de102de0a7f84ade4f1ef95487a3852f30c83f27129832a9d83dc0dbc4` |
| `source_content_id` | `bfe081c2c865043c3db019bae689902084908679b221609c1e1cd6053f61e345` |
| routine総数 | 989 |
| 除外 | import 489、module_level_assignment 241、lambda 71 |

coverage

| feature | 件数 |
| --- | --- |
| 直接callee 1件以上 | 560（56%） |
| 直接caller 1件以上 | 704（71%） |
| 未解決呼出を持つroutine | 244／未解決合計 327 |
| `raise`名あり | 403（40%） |
| `except`名あり | 176（17%） |
| bare except | 0 |
| Test直接参照あり | 386（39%）／参照path延べ 1352 |
| 意味的比較候補あり | 987（99%）／上限10到達 952／平均 9.84 |

`complexity_signal`：`low` 559、`medium` 325、`high` 105。
`public_api_signal`：`medium` 520、`low` 426、`high` 43。
入力の内訳は`__all__`掲載 0件、CLI構文marker 40件、cross-package direct callerを持つroutine 6件。

現行sourceに`__all__`を定義するmoduleが無いため、公開性の判定はCLI markerと
cross-package呼出だけに依存している。`high` 43件はほぼCLI入口である。
意味的比較候補は99%のroutineで上限近くまで埋まっており、候補集合だけでは絞り込みが粗い。
いずれも観察であり、設計変更は行っていない。

Profile v1（`5d1f174f…`）、既存Observation、既存Candidate Runは変更・削除・移動していない。

## 4. LLM生成の不実施

LLMによるDisposition Proposalの生成、LLMの説明、意味的重複判断、処置labelの提案は
一切行っていない。Operational Human Decision、Entry、Relation、Baseline、Attestationも
作成していない。既存Task Contractとsource pin recordの書換え、Git historyの書換えも行っていない。
