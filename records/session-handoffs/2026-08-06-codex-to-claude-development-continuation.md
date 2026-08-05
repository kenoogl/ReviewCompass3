# Codex → Claude：ReviewCompass3開発継続引き継ぎ

## 1. 引き継ぎ目的

Codexの残りtokenが少ないため、Humanは以降のReviewCompass3開発をClaudeへ委譲する。
Claudeは本メモを現在地の入口として使用し、正本、固定Evidence、Git、Testを再確認してから作業する。

本委譲は、Humanに残された方針変更、意味的裁定、段完了、外部送信、不可逆操作などのauthorityを
Claudeへ移すものではない。未承認の案を実装許可として扱わない。

## 2. 最初に全文を読む文書

次の順で全文を読む。

1. `AGENTS.md`
2. `TODO_NEXT_SESSION.md`
3. `docs/development/prompts/todo-handoff-update.md`
4. `docs/development/2026-08-03-initial-development-checklist.md`
5. `docs/current/reviewcompass3-plan-current.md`
6. `docs/development/2026-08-02-development-policy.md`
7. `docs/design/2026-08-06-work5a-current-work-projection-routing-proposal.md`
8. `docs/development/work-review-protocol.md`
9. `docs/development/codex-claude-collaboration.md`

固定Digest：

| path | SHA-256 |
| --- | --- |
| `docs/development/2026-08-03-initial-development-checklist.md` | `1232acd3b51527fe04b917538aee7a02d35c991392b35bcaee5b8729f6551b1f` |
| `docs/current/reviewcompass3-plan-current.md` | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` |
| `docs/development/2026-08-02-development-policy.md` | `0d34880353f06f50c7623282c765717348c8776938dc3113e28fdad4e9f8ac18` |
| `docs/design/2026-08-06-work5a-current-work-projection-routing-proposal.md` | `c061be7d5abd1f428497f59d2b4ccc352b699d657d038d11f1d359a76e587809` |

## 3. GitとTestの基準状態

- branch：`main`
- 本引き継ぎ作成前の基準commit：`6644fe4d1190aa2dfb3764cdad7d739c7ccee552`
- upstream比較：behind 0、ahead 62（基準commit時点）
- push：行っていない
- 関連Test：`tests/test_work5a_definition_challenge.py`と
  `tests/test_first_review_task_contract_e2e.py`を合わせて`83 passed`
- 公式全Test：`1007 passed`
- Python：3.9.6、pytest：8.4.2、system Python fallback：false

本メモ、チェックリスト、TODOを含む引き継ぎcommit後は、SHAやahead件数を文書へ追記するための
自己参照commitを作らず、Gitからread-onlyで確認する。

## 4. 完了している現在地

Work 5Aの最小Review Task Contract happy pathは、Contract version 2でaccepted artifactまで完了した。

- Definition Challenge：`passed`、blocking Finding 0件
- Contract approval：`approved`
- compile：`compiled`、Plan bundle 6 view
- deterministic Finding：0件
- Conformance：`passed`
- Final Challenge：`passed`
- Human review acceptance：`approved`
- Provenance：11 node・10 edge、`verified`、自己参照なし
- accepted artifact：作成済み

固定Evidence：

| path | SHA-256 |
| --- | --- |
| `records/development/2026-08-06-work5a-contract-v2-review-acceptance-records-v1.json` | `151c63c838850a3da319b5f1eaa8cf0d02379aed85b0a592f124e3624c275354` |
| `records/development/2026-08-06-work5a-contract-v2-review-acceptance-evidence-v1.md` | `3edf6f88bd85619c9e75868f066ddc1d0b66c41e842d27cd05abffac64d9bed5` |
| `records/development/2026-08-05-work5a-definition-challenge-first-run-records-v1.json` | `aace8f35b79cbe4e3113433b55e903e86e0171f04738b180e1728eb83bd93ca6` |
| `records/development/2026-08-05-work5a-definition-challenge-first-run-evidence-v1.md` | `ad7b82ae74cec8655c205191feb4bf89801353eb8c7838f239f8b1c7da4c6658` |

CodexはClaudeの受理commit`d9d9a41c9c241ce455c9ad9c8530c6d5c2b8b419`を独立確認し、3 recordの
Digest、11 node・10 edge、accepted artifact参照、関連83件、全1007件、TODO検査、worktree cleanを
再確認して`verified`とした。

この引き継ぎcommitでは、上記Evidenceに基づきチェックリストの
`Definition Challengeを通し、Contractの粒度と依存を確認した`を完了へ反映する。

## 5. 未完了事項と現在の判断点

Work 5Aには次の二項目が未完了である。

1. bootstrap Current Work Projectionを正式recordへ写像し、textとmachine-readable出力の同値を確認する。
2. 同じTestを変更せずgreenにし、refactor後も再確認する。

調査の結果、現在の正式recordには、Current Work Projectionに必要なStage、開発Work、Work Item、
dependency／cycle、pause／resume、session lifecycle、次作業を権威的に表すrecordがない。
現在のReview Task Contractは一文書reviewの実行経路であり、開発全体の現在位置authorityではない。

したがって、現時点でProjectionを部分実装すると、TODOまたはbootstrap eventを第二正本にする、
未承認のPortfolio／Work Item／Workflow state schemaを追加する、または欠けた値を推測する危険がある。

この問題と選択肢は
`docs/design/2026-08-06-work5a-current-work-projection-routing-proposal.md`へ固定した。

### 推奨案A

- Current Work Projection正式写像とrefactor後再確認は、必要な正式recordが揃うまで未完了のままdeferする。
- defer理由と再開条件をチェックリストとTODOへ記録する。
- Current Plan §17の初期実装順11に従い、次をWork 6Aの中核negative pathとする。
- Work 6Aで正式入力欠落、第二正本化、欠測推測、stale／競合誤表示をRED fixtureへ固定する。
- 正式Portfolio／Work Item／Workflow stateの最小recordが承認された後にProjection写像を再開する。

**Humanはまだ案Aを承認していない。**説明を受けた後、開発継続をClaudeへ委譲すると指示した段階である。
委譲指示を案Aの承認と解釈しない。

## 6. Claudeが最初に行うこと

1. §2の文書と固定Evidenceを読み、Digest、Git、Test表示、チェックリスト、TODOの事後状態を照合する。
2. Humanへ、案Aを承認するか一度だけ明確に確認する。
3. 承認前はWork 6AのTestまたは実装、Projection schema、Portfolio／Work Item schemaを変更しない。

Humanが案Aを承認した場合：

1. 承認Decisionをnew-onlyで記録する。
2. チェックリストへProjectionのdefer理由と再開条件を反映する。
3. TODOを共通手順だけでWork 6A REDへ更新する。
4. Work 6A項目と既存Testの対応を機械的にinventory化する。
5. 既存Testで被覆済みの負例を重複させず、未被覆の中核項目だけRED testとして追加する。
6. 実装を変更せず、期待した停止codeまたは失敗理由でREDになることを確認する。
7. RED testと必要なRED Evidenceを意味的に完結した単位でcommitし、Humanへ結果とGREEN候補範囲を提示する。

案A承認だけではGREEN実装を開始しない。GREENの意味範囲に新しいschema、state、authority、Contract変更が
含まれる場合はHuman判断を得る。

Humanが案Aを承認しない場合は、Work 6Aへ進まず、選択されたrouteに合わせて提案とTODOを更新する。

## 7. 開発・レビュー規律

- TDDを維持し、振る舞い変更はREDを先に固定する。
- 実装中にRED testを都合よく弱めない。要求誤解または承認済み設計変更の場合だけ理由を記録して変更する。
- LLMは文章操作と意味分析に限定し、Digest、抽出、集計、照合、file操作、Test、Gitは機械処理する。
- 完了報告を完了Evidenceにせず、`docs/development/work-review-protocol.md`に従い、固定入力、差分、
  artifact、Test、workflow境界を別々に確認する。
- Claude自身が実装と確認を担う場合、独立性が限定されることを明記し、少なくとも保存後再読込み、
  別commandによるDigest再計算、対象Testと全Test、差分検査を行う。
- Evidenceなしは`reported_unverified`、報告と事後状態の競合は`report_execution_mismatch`として停止する。
- TODO更新は`docs/development/prompts/todo-handoff-update.md`だけに従う。
- 完了した作業単位から次へ移る前に`work_unit_transition.py --work-status completed`を実行する。
- 通常commitはAGENTS.mdの最小guardを満たす場合だけ行う。push、tag、rebase、reset、amend、force push、
  外部送信、不可逆操作、方針変更、意味的裁定、段完了はHumanの明示承認なしに行わない。

## 8. 非目標と停止境界

現時点で開始しないもの：

- Work 6AのGREEN実装
- Work 4B、Work 5B、Work 7、Work 8
- 正式Current Work Projection schema、UI、dashboard、automation
- Portfolio／Work Item／汎用Workflow stateの先行実装
- LLM reviewer、外部送信、push、PR、CI
- Contract、Requirement、Plan、Policyの無承認変更

activeな非blocking Issueは`ISSUE-HTC-C9F6C917`である。固定recordは
`.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json`、SHA-256
`66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed`。現行route判断へ割り込ませない。
