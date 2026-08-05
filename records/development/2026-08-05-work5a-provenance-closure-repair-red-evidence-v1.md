# Work 5A Provenance Closure Repair RED Evidence v1

## 対象

- Test：`tests/test_first_review_task_contract_e2e.py`（追加13件、うちRED 11件）
- 正本設計：`docs/design/2026-08-05-work5a-provenance-closure-repair-proposal.md`（§5）
- 承認：`DEC-WORK5A-PROVENANCE-CLOSURE-REPAIR-001`（§6.3 案A）
- 無効化：`records/development/2026-08-05-work5a-provenance-closure-invalidation-v1.json`

## RED結果

```text
11 failed, 27 passed in 0.23s
E   AttributeError: module 'tools.task_contract' has no attribute 'validate_provenance_verdict'
E   KeyError: 'verified_nodes'
E   KeyError: 'verified_edges'
```

期待した失敗理由である。新形式のAPI（`validate_provenance_verdict`）と、
`verified_nodes`／`verified_edges`を持つ`provenance_verdict`が未実装のため失敗する。

既存Work 5A受入25件は変更しておらず、`25 passed`のままである。

## REDになった11件

| 設計§5 | test | 期待する拒否 |
| --- | --- | --- |
| P1 | `test_p1_provenance_has_nine_nodes_eight_edges_and_no_self_edge` | 9 node・8 edge・自己辺なし |
| N1 | `test_n1_legacy_terminal_edge_digest_is_rejected` | 旧形式（`to`と`to_digest`が別record） |
| N2 | `test_n2_edge_role_swap_is_rejected` | edge名称だけの差替え |
| N3 | `test_n3_node_kind_swap_is_rejected` | record kind差替え |
| N4 | `test_n4_node_id_swap_is_rejected` | record ID差替え |
| N5 | `test_n5_node_digest_swap_is_rejected` | Digest差替え |
| N6 | `test_n6_self_reference_is_rejected` | `from == to`と端点が自record |
| N7 | `test_n7_missing_or_duplicated_node_is_rejected` | node欠落・重複 |
| N8 | `test_n8_missing_or_extra_edge_is_rejected` | edge欠落・余分 |
| N10 | `test_n10_invalid_verdict_cannot_produce_accepted_artifact` | 不正verdictからの受理 |
| N11 | `test_n11_legacy_record_from_commit_9e8cf00_is_rejected` | `9e8cf00`の実recordを拒否 |

P2と N9 は既存実装でも通るため、追加時点でGREENであった。
P2は`accepted_artifact`の参照、N9は`target_digest`不一致の拒否であり、
いずれも既存の振る舞いを新形式でも維持することを固定する。

## N11の位置づけ

`records/development/2026-08-05-work5a-first-real-review-acceptance-records-v1.json`の
旧`provenance_verdict`を固定入力として読み、新validatorが拒否することを確認する。
実データによる回帰防止であり、この旧recordを正本として扱うものではない。
testは旧recordの最終edgeが`to: provenance_verdict`かつ`to_digest`が`human_decision`の
Digestであることも併せて確認する。

## 規律

実装中にこのtestの期待を緩めない。既存25件も弱めない。
旧形式を互換入力として受理しない。旧形式はN11の拒否fixtureに限る。
