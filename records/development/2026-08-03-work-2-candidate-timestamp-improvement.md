---
candidate_id: IC-WORK2-CANDIDATE-TIMESTAMP-001
observed_at: 2026-08-03T15:03:12+09:00
origin_stage: initial-development
origin_work: Work 2
origin_work_item: RC3-WORK2-INTENT-GLOSSARY-DECISION
candidate_kind: improvement_candidate
status: closed
suggested_route: current_work_repair_completed
confidentiality_class: project-internal
---

# Work 2判断候補の生成時刻不整合

## 1. 観測

Work 2のIntent／統合用語集Human判断候補を作成し、判断要求eventへ候補Digestを固定した。その後の
post-write確認で、候補frontmatterの`generated_at`がWork 2開始時刻ではなく、直前のWork 1完了承認時刻を
誤って再利用していることを検出した。

| identity | value |
|---|---|
| candidate | `records/development/2026-08-03-work-2-intent-glossary-candidate-v1.md` |
| candidate SHA-256 | `2666511bcf95a2fdc5237257b5c5e38fbc7dc1c80fd829064b02e34b759e6ab9` |
| recorded `generated_at` | `2026-08-03T14:35:03+09:00` |
| Work 2 session start | `2026-08-03T14:56:34+09:00` |
| Work 2 session raw SHA-256 | `7cc254470abd013b94df534cf4bea7b94394b4590154da746091a37171ae4277` |
| Work 2 Session Evidence SHA-256 | `456c9071781d5bbcddadd6cb2fa181274ba1930e34c5903c18eb96066719e5c6` |

session eventの`target_digest`は現行candidate SHA-256と一致するため、判断対象内容の取り違えはない。
一方、生成時刻は事後状態と一致せず、この候補を正確なProvenanceとして承認へ使用できない。

## 2. 影響

```yaml
classification_candidates:
  - execution_record_defect
  - provenance_metadata_defect
affected_authority:
  - Work 2 Human decision candidate identity
  - Work 2 Session Evidence decision target
acceptance_truth_changed: true
safety_or_security_impact: false
authority_impact: false
provenance_reconstructability_impact: true
source_test_verdict_identity_impact: true
current_work_can_continue: false
suggested_route: pause_and_triage
route_reason: Human判断対象の生成時刻が事実と異なり、修正すると対象Digestと保存済み判断要求eventが変わるため
duplicate_of: null
checkpoint: Work 2 Human decision gate
human_decision: option_1_approved
consumer_refs:
  - DEC-WORK2-CANDIDATE-TIMESTAMP-2026-08-03-V1
outcome_ref: RC3-WORK2-CANDIDATE-TIMESTAMP-REPAIR-2026-08-03-V1
```

Intent、利用者、非目標、authority境界、用語被覆の監査結果自体は変わらない。しかし候補fileを修正すると
SHA-256が変わり、保存済みsessionの`target_digest`は旧候補を指す。したがって、候補だけをin-place修正して
判断へ進めることはできない。

## 3. route proposal

### 選択肢1（提案）

意味不変のmetadata修復を承認する。候補の`generated_at`を実際のWork 2生成時刻へ訂正し、新Digestへ
更新する。旧候補Digestとsession `001`をsupersededとして保持し、新候補Digestを対象にsession `002`の
Human判断要求をdurable captureする。監査を再実行してからHuman判断候補を再提示する。

### 選択肢2

旧生成時刻の不一致riskをHumanが明示受容し、現行Digestを判断対象として維持する。この場合も、Decisionに
不一致、受容理由、影響範囲を記録する。Provenanceの正確性を弱めるため推奨しない。

## 4. 現在の状態

- Work 2を`pause_and_triage`する。
- 現行Human判断候補は`stale`として承認対象から外す。
- Intent、用語集、Plan本文は変更していない。
- metadata修復、再capture、Work 2承認、Work 3進行を自動承認しない。
- 再開条件はHumanが選択肢1、選択肢2または別処置を明示することである。

## 5. Human判断結果

Humanは2026-08-03T15:44:34+09:00に選択肢1を選択した。Decision正本は
`records/development/2026-08-03-work-2-candidate-timestamp-decision.json`、SHA-256
`9dcc7570d80bde8711049c688e5f03ec4a607457a96179fd146c512c288f271a`である。

承認範囲は生成時刻訂正、旧Digest保持、再監査、新Digestへのsession `002`再capture、checklist／TODO更新に
限定され、Intent／用語集の内容承認、promotion、Work 3開始、commit、pushは含まない。

## 6. Outcome

Work 2候補の`generated_at`を検証可能なsession境界へ訂正し、旧Digestをmetadataへ保持した。再監査は
Intent 8節、authority 3境界、canonical token 109件、必須13語、欠落・重複0で合格した。

session `002`は旧Digestをstale、新Digestをreverifiedとし、新DigestへHuman判断要求を束縛した。保存後rawと
3派生物を独立再読込してSession Evidenceと一致した。Outcomeは
`records/development/2026-08-03-work-2-candidate-timestamp-repair-evidence-v1.md`、SHA-256
`d1fb1e1f6f2ad0c794fdf36d74fa188ef068753a10f3e71c8428bf39a6c25ad0`である。

consumerとOutcomeが接続されたため本改善候補を`closed`とする。Work 2の現在地は訂正済み候補への
Human内容判断待ちである。
