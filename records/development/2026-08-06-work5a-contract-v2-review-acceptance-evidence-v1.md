# Work 5A Contract version 2 Review結果 受理Evidence v1

- 対象Contract：`TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2`（version 2）
- 承認：`DEC-WORK5A-CONTRACT-V2-REVIEW-ACCEPTANCE-001`
  （`records/development/2026-08-06-work5a-contract-v2-review-acceptance-decision-v1.md`）
- 受理records：`records/development/2026-08-06-work5a-contract-v2-review-acceptance-records-v1.json`
- Review Run：`records/development/2026-08-06-work5a-contract-v2-review-run-records-v1.json`
- 指示：`records/session-handoffs/2026-08-06-codex-to-claude-work5a-contract-v2-review-acceptance.md`
- 実行時刻：2026-08-06T06:42:16+0900
- 開始基準commit：`88a68ae6119c3c7d6bcd3d50814bca790ded9fa3`（HEADの祖先であることを確認）

## 0. 何を受理したのか（範囲の明示）

**受理したのは最小Review経路の実行結果である。review対象文書の内容が完全であること、または
一般的な品質保証を与えるものではない。**

具体的には、deterministic stub reviewer（LLMを使わない固定ruleのreviewer）が返した
Finding 0件と、ConformanceおよびFinal Challengeの`passed`を、今回のReview Runの結果として
Humanが受理したという意味である。対象文書
`docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md`の内容について、
網羅的なreviewを行ったわけではない。

## 1. 固定入力の照合

指示§2の4件を全文読み、SHA-256を機械照合した。**4件すべて一致**である。

| path | 判定 |
| --- | --- |
| `records/development/2026-08-06-work5a-contract-v2-review-acceptance-decision-v1.md` | 一致 |
| `records/development/2026-08-06-work5a-contract-v2-review-run-records-v1.json` | 一致 |
| `records/development/2026-08-06-work5a-contract-v2-review-run-evidence-v1.md` | 一致 |
| `docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md` | 一致 |

## 2. 事前照合（指示§3の6項目）

Run bundleを再読込みし、**6項目すべて成立**した。不一致は0件である。

| # | 照合 | 結果 |
| --- | --- | --- |
| 1 | bundle内12 recordと`compile_verdict.plan_bundle`のcontent digest | 13件すべて再計算一致 |
| 2 | Definition ChallengeからFinal Challengeまでの上流参照 | 19本すべて一致 |
| 3 | `finding_set` 0件、Conformance `passed`、Final Challenge `passed` | 成立（error 0、warning 0、info 0） |
| 4 | Definition Challenge／Contract approval／Conformance／Final Challengeのowner分離 | 4件すべて別の論理owner |
| 5 | Source Snapshot内のtext・SHA-256と現在のtarget file | Digestとtextの両方が一致 |
| 6 | `human_decision`／`provenance_verdict`／`accepted_artifact`がRun bundleに不在 | 成立 |

Context Manifestのcontent digestは`149ae4a5f28d9ccd0378d31312b2b3965ed1d3aaa31599ed98b249f080348354`で、
承認Decisionが指定したtarget digestと一致する。

## 3. 作成した3 record

`tools.task_contract`の既存public APIだけを、指示§4の順で呼んだ。

```python
human      = record_human_decision(contract, context_manifest, finding_set,
                                   conformance_verdict, final_challenge_verdict,
                                   decision="approved", human_id="kenoogl",
                                   decided_at="2026-08-06T06:37:41+09:00")
provenance = verify_provenance(requirement_binding, contract,
                               definition_challenge_verdict=..., contract_approval=...,
                               compile_verdict=..., context_manifest=..., permit=...,
                               finding_set=..., conformance_verdict=...,
                               final_challenge_verdict=..., human_decision=human)
accepted   = accept_artifact(provenance_verdict=provenance, human_decision=human,
                             context_manifest=context)
```

| record | record_id | version | content digest |
| --- | --- | --- | --- |
| `human_decision` | `HD-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 1 | `0feea7519d0bd7c3362dc867282f0b866c26a0ec1eb0bd3f0cd7815e44371d1c` |
| `provenance_verdict` | `PV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 1 | `9e4a06cdaf83a1544c2308c4ebb620c4e04790a881157839b8c60e64c992df5d` |
| `accepted_artifact` | `AA-CM-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2` | 1 | `606df3638f02a8747417a32e51c0ee3c730732c4da0a394f65c079dde827261c` |

新しいContract identityの初回recordなので、3件とも`record_version: 1`である。
すべてnew-onlyで作成し、既存recordを上書き・削除・無効化・stale化していない。

`human_decision`は`decision: approved`、owner `human_decision_owner`、
`decision_class: review_acceptance`、`human_id: kenoogl`、
`decided_at: 2026-08-06T06:37:41+09:00`、
`target_digest: 149ae4a5…`（Context Manifestのcontent digest）である。

## 4. Provenanceの形

Contract version 2の経路として、Definition Challenge verdictとContract approvalを含む
**11 node・10 edge**を検証した。statusは`verified`である。

```text
requirement_binding → review_task_contract → definition_challenge_verdict
→ contract_approval → compile_verdict → context_manifest → workflow_permit
→ finding_set → conformance_verdict → final_challenge_verdict → human_decision
```

- 終端nodeは`human_decision`、`self_edge_present`は偽、`closed_by`は`accepted_artifact`である。
- `provenance_verdict`自身をnodeにも、edgeの端点にも含めていない。
- 自己辺は1本も無い。
- `verified_nodes`、`verified_edges`、`closure`を持つ循環のない現行形式である。

## 5. 保存後の独立照合

保存したbundleを読み直して機械照合した結果は次である。**全項目一致**。

| 検証 | 結果 |
| --- | --- |
| 3 recordのcontent digest再計算 | 全件一致 |
| node 11件・edge 10件 | 一致 |
| `validate_provenance_verdict()`を通る | 通過 |
| 自己参照・`provenance_verdict`の端点混入 | いずれも無し |
| 11 node全部のkind・identity・version・content digest vs 上流record | 全件一致 |
| `accepted_artifact.provenance_ref` == Provenance | 一致 |
| `accepted_artifact.decision_ref` == Human decision | 一致 |
| `accepted_artifact.target_paths` == Context Manifestの材料 | 一致（対象1件） |
| `human_decision.target_digest` == Context Manifestのcontent digest | 一致 |
| 3 recordの`record_version` | すべて1 |

accepted artifactが指す対象は
`docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md`の1件である。

## 6. Test

| 対象 | 結果 |
| --- | --- |
| `tests/test_work5a_definition_challenge.py` | `45 passed` |
| `tests/test_first_review_task_contract_e2e.py` | `38 passed` |
| 公式venv runnerの全Test | **`1007 passed`** |

## 7. 変更していない範囲

- `tools/task_contract/`、`tests/`、review対象文書、Contract、Requirement、Current Plan、checklist。
- Contract version 1、その既存accepted artifact、既存Provenance record、既存recordの一切。
  上書き・削除・無効化・stale化はしていない。
- LLM、外部送信、外部`DATA_ROOT`、push、PR、CIは使っていない。
- Work 4B、Work 6A、後続評価E2以降は開始していない。
