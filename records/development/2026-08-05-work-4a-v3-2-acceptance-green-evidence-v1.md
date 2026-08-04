# Work 4A v3.2 Acceptance GREEN Evidence v1

## 対象

- 実装：`tools/development/work4a_rebuild_v3.py`（v3.2差分を追加）
- Test：`tests/test_work4a_rebuild_v3_2_e2e.py`（11件）
- 正本設計：`docs/design/2026-08-05-work-4a-rebuild-design-v3-2-proposal.md`
- 承認：`DEC-WORK4A-REBUILD-DESIGN-005`
- RED：`records/development/2026-08-05-work-4a-v3-2-acceptance-red-evidence-v1.md`
- receipt：`records/development/2026-08-05-work-4a-v3-2-acceptance-green-test-receipt-v1.json`

## 結果

- v3.2 acceptance：`11 passed`
- v3.1 acceptance：`21 passed`、v3 acceptance：`22 passed`（いずれも変更していない）
- 全test：venv公式runner `724 passed`、Python 3.9.6、pytest 8.4.2、fallback false

## 実装した不変条件

| 不変条件 | 実装 |
| --- | --- |
| 直接呼出は同一universe内で構文解決できたものだけ | `_add_v2_features`が短縮名の一意解決に限って`direct_callee_symbol_ids`へ入れる |
| 未解決を解決済みと偽装しない | 同名が複数、`eval`／`exec`／`getattr`／`globals`／subscript呼出は`unresolved_direct_call_count`へ計上 |
| caller/calleeはProfile内のsymbolのみ | `validate_routine_profile_v2_document`が範囲外を`profile_reference_unresolved`で停止 |
| 例外は構文上の名前のみ | `_exception_names`が`raise`と`except`に現れる名前だけを取る。伝播例外と実行時型を推測しない |
| 分割度は構文指標のみ | `_branch_and_depth`ほか。`complexity_signal`はPolicy v3の閾値から決定的に算出 |
| Test参照は`tests/**/*.py`の直接AST参照のみ | `_test_references`が`tests`外を`test_reference_out_of_scope`で停止。検証側でも範囲を再確認 |
| 公開API指標は宣言した入力のみ | `__all__`、cross-package direct caller、CLI構文markerから算出。公開契約を断定しない |
| 構造一致は結論ではない | `structural_match_detection.is_merge_conclusion`は常に`false`、`is_confirmation_hint`は`true` |
| 意味的比較候補は同一Profile内・上限10件 | 決定的スコアで選び、超過・重複・自己参照・範囲外を停止 |
| Profile v1とv2は併存 | 別`profile_run_id`で別fileへnew-only保存。v1は書き換えない |
| 判断カードは全source treeを渡さない | `select_additional_context`が対象・直接caller/callee・比較候補・関連Testのpathだけを返す |

## testの調整

`test_j7_structural_match_group_is_not_a_merge_conclusion`のうち、
`"merge" not in json.dumps(structural_match_detection)`という文字列検査を削除し、
`is_merge_conclusion is False`、`is_confirmation_hint is True`、`basis`の値検査へ置き換えた。

この文字列検査は、直後の`is_merge_conclusion`検査と同時に満たせない。
「統合の結論ではない」と宣言するfield名自体が`merge`を含むためである。
受入条件J7（構造一致groupだけで`merge`を確定しない）そのものは変更しておらず、
むしろ値で検査する形に強めた。他の10件は初回作成時のままである。

## 非対象

LLMによるDisposition Proposalの生成、LLMの説明・意味的重複判断・処置labelの提案は行っていない。
Operational Human Decision、Entry、Relation、Baseline、Attestationも作成していない。
既存Routine Profile v1、Observation、Candidate Run、Task Contract、source pin recordは
書き換えていない。Git historyの書換えも行っていない。
