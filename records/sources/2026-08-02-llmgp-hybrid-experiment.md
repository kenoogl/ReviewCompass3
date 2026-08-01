---
source_id: SRC-LLMGP-HYBRID-001
captured_at: 2026-08-02
source_kind: external-project-empirical-reference
normative_status: non-normative-evidence
confidentiality_class: project-internal
raw_snapshot_retained: false
---

# LLMGP SDD/TDD折衷運用の参照記録

## 1. 位置付け

WindTurbineWake/LLMGPで試行されたSDD/TDD折衷運用を、ReviewCompass3のTask Contract
中心化に対する先行実験として参照する。参照元はReviewCompass3の規範文書ではなく、
採用候補の妥当性、運用上の失敗、規則調整の必要性を示す経験的Evidenceである。

## 2. 参照元identity

2026-08-02に次の内容を読み取った。外部projectのraw snapshotは本repositoryへ複製せず、
観測時の絶対pathとSHA-256を固定する。後日path上の内容が変わった場合、同一sourceとして
扱わない。

| artifact | observed path | SHA-256 |
|---|---|---|
| Agent entryと調整履歴 | `/Users/Daily/Development/WindTurbineWake/LLMGP/.reviewcompass/AGENT_ENTRY.md` | `a0166de3ca51aa7fa3fe3ef7401a5079863c927ad93dd2eabe03a0d1a796f2e0` |
| Task ledger | `/Users/Daily/Development/WindTurbineWake/LLMGP/tasks/TASKS.md` | `3d8e8bafe5db04ebc5d6f13941807383f54a81cb3f0a958dbf51a3d2a98d774b` |
| Feature dependency | `/Users/Daily/Development/WindTurbineWake/LLMGP/.reviewcompass/feature-dependency.yaml` | `bae497e2322bb991d95ff022c3d2eb1094b995a40bd52ada76c41b9c965d259a` |

## 3. 観測した先行実験

参照版の`AGENT_ENTRY.md`は、uniformなSDD stage gateから、Intent、Feature Partitioning、
Requirementsを上流に残し、それ以降をtask-driven SDD/TDD hybridへ移す方針を記録して
いる。Requirementsをtest oracleとし、task本文をID、目的、入力、出力、完了条件に絞り、
実行Contextをruntimeで構成する。`TASKS.md`には、red testとImplementationを分けた作業例が
保持されている。

調整履歴からは次を観測した。

- 一律の独立三者reviewは高コストであり、riskに応じたreview強度へ変更された。
- commit guardは三回のdeadlockを起こし、目的を阻害したため撤回された。
- 記録訂正までreopen停止点へ含めると、人工的な状態遷移と訂正が発生した。
- 軽微修正と意味的reopenは、Acceptance Criteriaの真偽または義務が変わるかで区別された。
- Requirementsの意味変更は、TDDだけでは誤ったoracleを検出できないため、独立reviewの
  対象として維持された。

## 4. ReviewCompass3へ採用するもの

- Taskの最小核をIdentity、Responsibility、Input、Output、Completionとし、Task Contractで
  Boundary、Capabilities、Provenance、Escalation、Dependencyを明示的に補強する。
- 同じ入力とEvidenceに対するaccept/reject、義務、scopeが変わるかを
  `acceptance_truth_changed`として判定し、意味的reopenの境界にする。
- 変更を意味分類とstate effectに分け、承認、stale、review、停止点を選択する。
- review強度を一律gateではなく、意味分類、risk、side effectから導出する。
- project固有の方針調整を、理由、Evidence、適用範囲、置換規則とともに版付きで残す。

## 5. そのまま採用しないもの

- 線形な`TASKS.md`だけを唯一のschedulerまたは依存正本にしない。
- 端末固有の絶対pathをdeployment contractまたは永続identityにしない。
- test-only commit、独立三者review、二段階commit gateを全変更へ一律に要求しない。
- Agent entry末尾への追記だけでproject policyを永続管理しない。

これらはTask Contract Portfolio、Deployment Manifest、risk-based Verification Profile、
版付きProject Policy Overlayで置き換える。

## 6. Evidenceの限界

本記録は参照版文書から得た定性的Evidenceである。工数、文書行数、実装行数、review回数、
deadlock回数などを比較評価の定量値として使用する場合は、対応するgit履歴、Run記録、
Task成果を別途固定して照合する。参照元raw snapshotを本repositoryへ保持していないため、
外部pathからdigest一致の内容を再取得できない場合、原文全体は
`non_reconstructable`として扱う。
