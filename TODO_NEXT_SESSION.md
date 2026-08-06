# TODO_NEXT_SESSION

更新日：2026-08-06

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 5AのContract version 2 Review経路はaccepted artifactまで完了した。以降の開発はHumanの指示によりClaudeが継続する。
- 現在作業：Work 6A中核negative pathのGREENとchecklist CL-6A-08の完了反映まで終えた。恒久検査器は案1に従い、観測recordと改善候補をnew-onlyで作成した。Issue昇格とtriage判断は未実施である。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-HTC-C9F6C917`：`registered / nonblocking`、影響：shellによる決定的操作の手戻り候補を集約する既存Issue。現行のHuman判断を停止しない、次：現行route判断へ割り込ませず、既存Issueとして保持する

## 最新のauthority／Evidence

- [検査器の改善候補](.reviewcompass/workflow/improvement-candidates/ic-authority-reference-digest-check-001--v1.json) — SHA-256 `d4e801aa35e4bd1ad2c17917d0cfd57b60e7e1aec93e7d1259bf8321285824c6`
- [参照Digest driftの観測record](records/development/2026-08-06-authority-reference-digest-drift-observation-v1.json) — SHA-256 `6ccf3d15c28c56a5b74730a9ac056ef3abe13967da0427549e05308cc0ab3841`
- [CL-6A-08 完了承認Decision](records/development/2026-08-06-work6a-cl-6a-08-completion-decision-v1.md) — SHA-256 `ead257402defe2c26b99b3791a01ea66d7ba837e15d536be2e94e8b65f6f48f1`
- [非authority入力 拡大GREEN Evidence](records/development/2026-08-06-work6a-non-authority-input-green-evidence-v1.md) — SHA-256 `79c5783c6f759c631aeabc41916fcc93f914984e2278ab1acb29589e1119a5ac`
- [Evidence訂正record](records/development/2026-08-06-work6a-evidence-correction-v1.md) — SHA-256 `219eefc14dcda02d4ea72e70682bcaf0fe9ea98d752cb25aacc79dcee64871b7`
- [Work 6A項目と既存Testの対応inventory](records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json) — SHA-256 `51674c143858b37608c7914c5bc2a8973be8221e2d5bde9707d89d082f995a16`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `53226e7c7c743e145af6fa313e42c2fccdd66f5f41917399b445d8587f022676`
- [機械操作の根本原因Issue](.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json) — SHA-256 `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed`

## 次に行う一作業

Humanが改善候補IC-AUTHORITY-REFERENCE-DIGEST-CHECK-001のtriageを裁定する。

開始条件：

- 観測recordと改善候補を含むcommitがcleanであること
- 裁定直前にv3 validatorを再実行し、evidence_refsが現行bytesと一致することを確認すること

完了条件：

- 分類、blocking判定、routeがHuman triage decisionへ記録されること
- Issue昇格の可否が明示されること

後続作業：昇格する場合だけIssue recordをissues-v4へ作る。検査器、validator、test、configは裁定まで作らない。

## blocker・Human判断待ち

- blocker：なし。検査器の実装、Current Work Projection正式写像、正式Portfolio／Work Item／Workflow state、Work 6Aの残り10項目は開始しない。Codex側の指示書にある作業はHumanの指示により扱わない。
- Human判断待ち：改善候補IC-AUTHORITY-REFERENCE-DIGEST-CHECK-001の分類、blocking判定、route、Issue昇格の可否。

## stale・deferred

- stale：checklist CL-6A-08は完了へ変わった。改善候補のevidence_refsはchecklistを含むため、checklistが再改定されると検証に落ちる。
- deferred：Current Work Projection正式写像、同じTestを変更しないrefactor後再確認、Work 6Aのうち承認範囲外20項目、入力側へのauthority宣言方式、Work 4B、Work 5B、Work 7、Work 8、UI、automation。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：Issue Resolution Pilot関連54 passed、Work 6A negative 10 passed
- 直近の全Test：venv公式runner 1017 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
