# Work 4A v3.3 Acceptance GREEN Evidence v1

## 対象

- 実装：`tools/development/work4a_rebuild_v3.py`（v3.3差分を追加）
- Policy：`.reviewcompass/policies/work4a-freshness-policy-v4.json`
- Test：`tests/test_work4a_rebuild_v3_3_e2e.py`（15件）
- 正本設計：`docs/design/2026-08-05-work-4a-rebuild-design-v3-3-proposal.md`
- 承認：`DEC-WORK4A-REBUILD-DESIGN-006`
- RED：`records/development/2026-08-05-work-4a-v3-3-acceptance-red-evidence-v1.md`
- receipt：`records/development/2026-08-05-work-4a-v3-3-acceptance-green-test-receipt-v1.json`

## 結果

- v3.3 acceptance：`15 passed`
- 既存：v3.2 `11 passed`、v3.1 `21 passed`、v3 `22 passed`。いずれも変更していない
- 全test：venv公式runner `739 passed`、Python 3.9.6、pytest 8.4.2、fallback false

## 実装した不変条件

| 不変条件 | 実装 |
| --- | --- |
| 参照は一方向 | Profile v3の`comparison_discovery_reference.profile_references_discovery`は常に`false`。schemaに`comparison_discovery_ref`を許さない |
| Discoveryだけが固定参照 | `build_comparison_discovery`がProfileのrun ID、content digest、source content IDを固定。三つのいずれかが不一致なら`discovery_profile_mismatch` |
| bounded seedの廃止 | Profile v3のroutineから`semantic_comparison_candidate_ids`と`semantic_candidate_selection_reason`を除去。混入は`unknown_field` |
| bounded seedを根拠にしない | `reject_bounded_seed_basis`が`bounded_seed_not_a_basis`で停止 |
| memberを切り捨てない | 全memberを符号順で保持。件数不一致、重複、順序崩れ、代表の範囲外は`member_truncation_detected` |
| 代表は最大3件 | Policy v4の`representative_limit`から取り、超過を停止 |
| group は2件以上 | Policy v4の`minimum_group_member_count`。1件のkeyはgroup化しない |
| 閉じた根拠語彙 | Policy v4の`basis_kinds` 6種のみ。語彙外は`summary_vocabulary_violation` |
| package・引数個数だけでgroupを作らない | 6種のkey関数のいずれもpackageやarityを主keyにしない。両者は`basis_evidence`の補助情報としてのみ記録 |
| `call_neighborhood`は完全一致 | 空でないcaller/calleeの符号順集合が完全一致する場合だけgroup化。部分一致の閾値を持たない |
| 表示classは決定的 | `focused` 2〜12、`broad` 13〜50、`mass` 51以上。値の再計算と一致しなければ停止 |
| 意味的結論を出さない | record全体とgroupに`is_semantic_conclusion: false`、`produces_disposition: false`。`disposition`項目の混入を拒否 |
| LLM初期入力の範囲 | `build_llm_initial_input`は判断カードとgroup要約だけを返し、`member_symbol_ids`とsource本文を含めない |
| 追加読込のprovenance | `record_additional_read`が理由の空文字を`advisory_evidence_missing`、範囲外groupを`profile_reference_unresolved`で停止 |
| 併存と非書換え | Profile v2、Profile v3、Discoveryは別run IDで別fileへnew-only保存 |

## 実装中に行った調整

`build_decision_card`が固定リストで全fieldを要求していたため、bounded seedを持たない
Profile v3で`KeyError`になった。存在するfieldだけを載せる形へ変更した。
testの期待は変更していない。v3.2の判断カードのfieldはv2 Profileに存在するため影響しない。

testの期待を緩めた箇所はない。設計矛盾による停止も発生しなかった。

## 非対象

LLMによる説明生成、意味的比較、Disposition Proposal、処置labelの提案は行っていない。
Operational Human Decision、Entry、Relation、Baseline、Attestationも作成していない。
既存Profile v1／v2、Observation、Candidate Run、Task Contract、source pin recordは
書き換えていない。Git historyの書換えも行っていない。
