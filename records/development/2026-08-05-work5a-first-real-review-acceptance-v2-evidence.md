# Work 5A First Real Review Acceptance Evidence v2

## この受理が意味すること

**今回受理したのは、最小Review経路の実行結果である。対象文書の品質保証ではない。**

deterministic stub reviewerの指摘0件を、この最小Review Runの結果として受理する判断であり、
review対象文書の設計内容が完全であることを保証するものではない。対象文書は変更していない。

## v1との違い

v1（commit `9e8cf00`）の`provenance_verdict`は、最終edgeで`to: provenance_verdict`と書きながら
`to_digest`に`human_decision`のDigestを持っていた。recordが自分自身のDigestを内容へ含めることは
不動点になり構造上成立しないため、局所修正ではなく形式を変えた。

- v1の`provenance_verdict`と`accepted_artifact`は
  `records/development/2026-08-05-work5a-provenance-closure-invalidation-v1.json`で
  `invalidated_not_authoritative`とした。
- **Humanの承認判断は有効であり、失われていない。**`DEC-WORK5A-PROVENANCE-CLOSURE-REPAIR-001`の
  §6.3案Aにより、既存の`human_decision` version 1をそのまま参照する。
  新しいHuman判断は行っていない。判断は一度だけである。

## 作成したrecord

| record kind | record ID | version | content digest |
| --- | --- | --- | --- |
| `human_decision` | `HD-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | 1（再利用） | `a240921a70a40837efa2d45ee83def0059c125a2a343b7eb415841ddce65d8af` |
| `provenance_verdict` | `PV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | **2** | `7db7e9521d19ce958ab6e88b5d493c4e28c3ca9af1a5f08db30b0e17ab76bf12` |
| `accepted_artifact` | `AA-CM-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | **2** | `c33242c401f72e648a5a4674589adbf1622c6007b59a89e91dbc44d421f3c540` |

新しいrecordはnew-onlyである。version 1を上書きしていない。
保存先は`records/development/2026-08-05-work5a-first-real-review-acceptance-v2-records.json`。

`provenance_verdict` version 2は`verified_nodes` 9件と`verified_edges` 8件を持ち、
`edges` fieldを持たない。自己辺は無く、端点に`provenance_verdict`が現れない。
`closure`は終端が`human_decision`、閉包は`accepted_artifact`であることを明示する。

## 参照とDigest

| 参照 | path | SHA-256 |
| --- | --- | --- |
| 上流record bundle | `records/development/2026-08-05-work5a-first-real-review-run-records-v1.json` | `658e5ba98d602308…` |
| 上流Evidence | `records/development/2026-08-05-work5a-first-real-review-run-evidence-v1.md` | `cdc4c4d8ad08a6f0…` |
| 無効化record | `records/development/2026-08-05-work5a-provenance-closure-invalidation-v1.json` | 実fileから照合済み |
| 設計承認Decision | `records/development/2026-08-05-work5a-provenance-closure-repair-approval-decision-v1.md` | 実fileから照合済み |
| 既存Human decisionの出所 | `records/development/2026-08-05-work5a-first-real-review-acceptance-records-v1.json` | 実fileから照合済み |
| review対象 | `docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md` | `14901323a958d686…` |

## 読み戻し照合

保存後にfileを読み戻し、23項目を機械照合して全一致を確認した。

- 三recordのDigest再計算が一致した。
- `human_decision`がversion 1のままで、v1と同一recordであった。
- `provenance_verdict`と`accepted_artifact`がversion 2であった。
- 新validatorを通り、`edges` fieldが無く、node 9件・edge 8件・自己辺なし・
  端点にverdict自身が無いことを確認した。
- 各nodeのDigestが上流recordおよび既存Human decisionと一致した。
- `accepted_artifact`が`provenance_verdict`と`human_decision`を参照し、対象pathが一致した。
- 参照5件とtargetのfile Digestが実fileと一致した。

## 経路の完結

Requirement bindingからaccepted artifactまでの最小Review経路が、循環の無い形で完結した。

```text
Requirement binding → Source Snapshot → Review Task Contract → compile / 6 typed view
→ Context Manifest → permit → deterministic stub review → Conformance → Final Challenge
→ Human decision → Provenance verdict(v2) → accepted artifact(v2)
```

## 変更していない範囲

`9e8cf00`をrevertせず、既存recordを削除・上書きしていない。
設計提案、review対象文書、Requirement、Current Plan、checklistを変更していない。
LLM、外部送信、外部`DATA_ROOT`、push、PR、CIを使っていない。
Work 4B、Work 6A、後続評価E2以降を開始していない。
