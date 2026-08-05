# Work 5A Definition Challenge 設計承認Decision v1

- Decision ID：`DEC-WORK5A-DEFINITION-CHALLENGE-001`
- decision maker：Human
- decided at：2026-08-05
- 対象：Work 5Aの最小Definition Challenge

## 1. Human承認

Humanは、`docs/design/2026-08-05-work5a-definition-challenge-proposal.md`の第四版について
「推奨案で設計承認」と指示した。

## 2. 承認した意味的判断

1. 既存Review Task Contract version 1とそのaccepted artifactは、当時の有効な履歴として保持する。
   version 2の作成だけでversion 1を無効またはstaleにしない。version 2が完了した後、
   `superseded_by_v2`の関係をnew-onlyで記録する。
2. Definition ChallengeはConformance、Final Challenge、Human review acceptanceのいずれとも
   異なる論理ownerを持つ。判定はHumanによる都度の手作業ではなく、固定入力と承認済みの
   D1〜D8から決定的な機械処理で実行する。
3. Definition Challengeはcompileより前に実行する。`plan_bundle`、`compile_verdict`、
   Finding集合、Conformance verdict、Final Challenge verdictを入力に使わない。
4. 対象は後継する一つのdraft Review Task Contract version 2だけとし、汎用Challenge frameworkは
   作らない。

## 3. 承認した実施順序

```text
Requirement definition / binding → draft Contract v2 → material set
→ Definition Challenge verdict → Human Contract approval → compile / Plan bundle
→ Context Manifest → Workflow permit → Finding set → Conformance
→ Final Challenge → Human review acceptance → Provenance → accepted artifact
```

- TDDでG1〜G4、H1〜H11を先にREDとして固定する。
- 既存の関連Testを弱めない。
- 初回Definition Challenge実Runが`passed`でも、Contract version 2のHuman承認前にcompileへ進まない。

## 4. 承認範囲

- draft Contract version 2のnew-only作成
- `requirement_receivers`と`review_owners`の追加
- Definition Challenge material set、Finding、verdictの最小schemaとD1〜D8
- `compile_contract`のDefinition Challenge事前gate
- G1〜G4、H1〜H11のTest、GREEN実装、関連Test、全Test、初回実Run

## 5. 承認しないこと

- 初回Definition Challenge実Run後のContract version 2の自動承認
- Contract version 2承認前のcompile、Review Run、accepted artifact作成
- Contract version 1または既存recordの上書き、無効化、stale化
- Architecture Policy、Challenge Policy、risk catalog、隣接Contractの推測による新設
- Work 6A、汎用framework、LLM実行、外部送信、push、PR、CI
- Work 5Aまたは段の完了判断

## 6. 固定入力

| 種別 | path | SHA-256 |
| --- | --- | --- |
| 承認済み設計提案 | `docs/design/2026-08-05-work5a-definition-challenge-proposal.md` | `4d8f3fdf8d85b3513cc08575f12e92a80e617e51dff2329c02cf9d84399bfd4f` |
| Work 4設計提案 | `docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md` | `14901323a958d686ba0ad0aed62b20b7b7d79908afcced08dc90f72fdb3d2054` |
| `REQ-CONTRACT-004` | `records/requirements/definitions/req-contract-004--v1.json` | `5b0835fd9fb50eee64952575f3a98d9f1d2f43e4f9f82037c5a7abdc66985ebf` |
| Current Plan | `docs/current/reviewcompass3-plan-current.md` | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` |
| Development Policy | `docs/development/2026-08-02-development-policy.md` | `0d34880353f06f50c7623282c765717348c8776938dc3113e28fdad4e9f8ac18` |
| 既存version 1受理record | `records/development/2026-08-05-work5a-first-real-review-acceptance-v2-records.json` | `64d75f3568078ef419cf74c3b72632352d07e63449b98fdb1608b17257184e7b` |
| 循環訂正指示 | `records/session-handoffs/2026-08-05-codex-to-claude-work5a-definition-challenge-design-correction.md` | `53f77ac9f19378fe5174e4c8a3c6a42f1cf4b37d22ba22354d3d63c7b5e0cfbb` |

## 7. 次の停止境界

本Decisionを含むcommitとclean transitionの後、Contract version 2とRED Testの作成へ進める。
初回Definition Challenge実Runの結果をHumanへ提示し、Contract version 2の承認前に再度停止する。
