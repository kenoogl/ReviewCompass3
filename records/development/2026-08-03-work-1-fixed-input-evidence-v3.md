---
evidence_id: RC3-WORK1-FIXED-INPUT-2026-08-03-V3
evidence_version: 3
recorded_at: 2026-08-03T15:54:36+09:00
work_id: Work 1
work_name: 固定入力と開発入口
status: verified
workflow_state: completed
confidentiality_class: project-internal
---

# Work 1 固定入力Evidence V3

## 1. 再検証理由と結果

HumanがWork 2でIntentと統合用語集の固定内容Digestを承認した。Work 1 Evidence V2のstale規則は
authority文書のpromotion状態変更を再検証条件としているため、V2を上書きせずV3を作成した。

promotionは承認済みcontent Digestを変えない外部Decision方式である。corrective snapshot commit
`ee60e3b4baf74c60da949a9d04d793fb83a61e69`から13 artifactを再読込し、manifestのSHA-256と全件一致した。
承認対象2文書のworktree内容、snapshot Digest、Plan current refsも一致した。結果は
`verification: passed`、内容変更は`false`である。

## 2. 入力とDecision

| role | identity | SHA-256／結果 |
|---|---|---|
| prior Evidence | `records/development/2026-08-03-work-1-fixed-input-evidence-v2.md` | `7997b203935a9e53c56ed2556b4598773cd9d7b13c43079fcf8524b5e06bc9be` |
| corrective snapshot | `records/development/2026-08-03-work-1-corrective-snapshot-v1.json` | `08365d976f020b428c46d1f83b14d7b0861beb335103493cf81823a144cc25c4` |
| post-commit verification | `records/development/2026-08-03-work-1-corrective-snapshot-v1-post-commit-verification.json` | `a1cfb19122c94d7e0edbf37b61e30f0ecd69c2aca461f7aba66b4e7e60ff6ad8` |
| Work 2 Approval | `records/development/2026-08-03-work-2-intent-glossary-approval.json` | `068ff06132dfcd24685d4a626d9107cf65b37456eebcd567dc72b9f6b27c7b78` |
| Intent | `docs/current/reviewcompass3-intent-current.md` | `1950f5a37fb5d0d0554f56343b39bbca7fc635523409f10ee761d8cef68f9ec6` |
| 統合用語集 | `docs/current/reviewcompass3-glossary-current.md` | `f1e7e9a9c57292fe911217d9b4f5d5b8ed99a881d6f113f9b60db1f0d01b19fa` |
| 現行Plan候補 | `docs/current/reviewcompass3-plan-current.md` | `0ae6bef979192b008a8a71fc090f709279c4bd1f0db159f9faadf947e929156f` |

## 3. promotion状態

| authority | state | authority source |
|---|---|---|
| Intent | `approved_normative_source` | `DEC-WORK2-INTENT-GLOSSARY-2026-08-03-V1` |
| 統合用語集 | `approved_normative_source` | `DEC-WORK2-INTENT-GLOSSARY-2026-08-03-V1` |
| 現行Plan | `provisional`、Human承認前 | Plan fileと後続の新しい第5段相当gate |

Intentと用語集のcandidate fileは承認時のcontent Digestを保持するため変更しない。frontmatterは
pre-promotion snapshotとして解釈し、現行promotion authorityは外部Decision Recordとする。

## 4. 再検証内容

```text
snapshot_artifacts: 13 / 13 matched from commit ee60e3b
approved_materials: 2 / 2 matched current worktree and snapshot
Plan current refs: matched
content_changed_by_promotion: false
verification: passed
```

source catalog、前身baseline、Work 1 scope、非目標、Deferred境界はV2から変更されていない。承認Decisionは
AI判断委譲、Plan、Requirements、Design、製品実装開始を承認していない。

## 5. stale閉包

- V2はpromotion前状態の正確なEvidenceとして保持する。
- V3がpromotion後のcurrent Work 1 Evidenceを引き継ぐ。
- 固定contentとPlan Digestは変わっていないため、Work 1A Layout、Work 1B bootstrap実装とTestをstaleにしない。
- Work 2 session `001`と旧candidate Digestはtimestamp不整合の履歴としてsupersededである。
- Work 2 session `002`と訂正済みcandidateは現行判断関門としてcurrentである。

今後、承認Decision、承認対象Digest、Plan ref、snapshot commit、source catalogまたはpromotion状態が変わる場合は
V3をstaleとし、新versionで影響閉包を再検証する。

## 6. 完了判定

Work 1の固定入力はpromotion後もGitから再構築可能で、blockingなProvenance不一致はない。Work 1は
`verified / completed`を維持する。Work 2のHuman content gateを閉じることができ、次の未完了工程はWork 3である。
