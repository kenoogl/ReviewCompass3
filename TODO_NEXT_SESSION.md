# TODO_NEXT_SESSION

更新日：2026-08-11

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B〜5B、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baseline、共通関数掃討、TODO検証単一入口、伏字化規則の実保全入口接続、ReviewCompass3所属Codex session保存が完了。操縦者別連携の文書設計と第1機械処理縦切りがHuman段完了承認まで完了した。
- 現在作業：Humanは主担当gpt-5.6-sol、レビュー担当gpt-5.6-terraを固定した。範囲レビュー依頼の指示文監査はPA-CB-SR-001〜004を提示し、別の判定担当は全件採用を推奨した。範囲レビュー本体、test、実装、認証、実送信は未開始。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`：`registered / nonblocking（V4 resolve toolはverified、実Issueのresolveは未実施）`、影響：実Issue recordのstateはregisteredのままだが、本縦切りを妨げない、次：本作業と分け、後続候補としてHuman裁定を得てresolveする

## 最新のauthority／Evidence

- [範囲レビュー依頼 指示文判定 v1](records/session-handoffs/2026-08-11-no-tool-bootstrap-scope-review-prompt-judgment-v1.md) — SHA-256 `f1c92e44375e4c1aacc554c675bda6a3ae4b1fb3b2415624bbaf2f2ffaf72ad7`
- [範囲レビュー依頼 指示文監査 v1](records/session-handoffs/2026-08-11-no-tool-bootstrap-scope-review-prompt-audit-v1.md) — SHA-256 `0ba70036d413f28ede3d5cb5132a94afa4dbef4380ef2df4e0c88b889c8a615e`
- [範囲レビュー依頼 v1](records/session-handoffs/2026-08-11-no-tool-bootstrap-scope-review-request-v1.md) — SHA-256 `a087e9f8544c08eb3b63df8076fabf0812a123063c518370f06f62794e85c435`
- [範囲レビュー担当モデル Human裁定 v1](records/session-handoffs/2026-08-11-no-tool-bootstrap-review-model-human-decision-v1.md) — SHA-256 `5a709bff5f814595284b7540ebd842c2dec2c702ac47be9e822488f544c974c7`
- [無工具Claude疎通経路 範囲固定 v2](records/session-handoffs/2026-08-11-codex-pilot-approved-claude-send-path-scope-v2.md) — SHA-256 `aefa05876b38a5b192d923f43dc17609678053ca33a4936b992e8a6646845c82`
- [無工具疎通確認 選択Human裁定 v1](records/session-handoffs/2026-08-11-pilot-collaboration-no-tool-bootstrap-selection-human-decision-v1.md) — SHA-256 `3b29567232320f6751a2badd40d31b7f8ab321d731d7777f8fdd1b0f11afa0da`
- [外部実行経路 選択Human裁定 v1](records/session-handoffs/2026-08-11-pilot-collaboration-external-route-selection-human-decision-v1.md) — SHA-256 `58d7809b547b339c3641f336cc23b2729aca6e09d7d50a109ed4c7f984de7983`
- [先行範囲レビュー v1](records/session-handoffs/2026-08-11-claude-scope-review-approved-claude-send-path-v1.md) — SHA-256 `402b2f7af1b2b28c9dac497ec2624e6078e361cebf55730b12f8ee8784c1e1ff`
- [操縦者別のClaude／Codex連携方法](docs/development/pilot-specific-claude-codex-collaboration.md) — SHA-256 `aee8c8b72487e26395615c8442710b0695b035ec0aa129b4a777c6142864489d`
- [委譲作業の共通レビュープロトコル](docs/development/work-review-protocol.md) — SHA-256 `b7eb8f08c7b3f585d64d163a7a2f93e758e57e830bb973cc2441bfadbc98a3df`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `4bf42b4bce858bdc2e299a08582e94411698db2e143a0af4b47840712756f38c`
- [ReviewCompass3 開発方針](docs/development/2026-08-02-development-policy.md) — SHA-256 `08bea1f9d5937ba5c212512ad041a0d03583d743dcc27742ad77c8741a22ad1c`

## 次に行う一作業

HumanがPA-CB-SR-001〜004を所見ごとに採用、不採用、保留のいずれかで裁定する。

開始条件：

- 指示文監査と指示文判定が別のgpt-5.6-terraサブエージェントで実施されていること
- 監査4件が対象依頼SHA-256へ束縛され、判定担当が全件を一回ずつ照合していること
- 範囲レビュー本体をまだ開始していないこと

完了条件：

- PA-CB-SR-001〜004の全件へHuman裁定が一回ずつ対応すること
- 保留が一件でもあれば依頼文を修正せず停止すること
- 採用所見だけを反映した単一v2依頼を作り、新しい監査・判定周回へ戻ること

後続作業：修正した範囲レビュー依頼が品質関門に合格した後、gpt-5.6-terraの新しいレビュー用サブエージェントが範囲固定v2を独立レビューする。

## blocker・Human判断待ち

- blocker：範囲レビュー依頼の指示文監査所見4件がHuman裁定待ち。Claude Codeの未認証は後段の認証操作と実送信も停止する。
- Human判断待ち：PA-CB-SR-001〜004を所見ごとに採用、不採用、保留で裁定する必要がある。全件採用がモデルの推奨だが、確定ではない。

## stale・deferred

- stale：接続段階のHuman選択待ちという旧表示は、無工具の疎通確認を選択した裁定により古い状態。先行範囲v1は実装根拠に使わない。
- deferred：実送信、認証操作、限定道具を許可する実装委譲、第2縦切り、group C・D、実装後レビュー接続、既存保全データへの伏字化遡及適用、Work 7A後続、既存Issue resolveを保留する。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：文書・指示文品質確認段階のため新規testなし。対象と固定材料のDigestは監査担当が全件一致を確認。直近の操縦者別連携受入89件は終了0。
- 直近の全Test：直近の公式全Testは1559 passed、failed 0、errors 0、終了コード0。
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
