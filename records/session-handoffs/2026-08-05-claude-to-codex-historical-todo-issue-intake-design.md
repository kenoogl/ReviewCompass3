# Claude → Codex：過去TODOからのIssue Intake設計 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-historical-todo-issue-intake-design.md`

## 1. commit SHA

`472c7ad5ffb67ec6e007b1779f03ec17148b8c77`（Propose historical todo issue intake）

設計文書一件だけのcommitである。config、validator、code、test、既存Issue、Plan、TODO、
checklist、Requirementを混ぜていない。

| file | SHA-256 |
| --- | --- |
| `docs/design/2026-08-05-historical-todo-issue-intake-proposal.md` | `80b9fbd42e0a0dd30a151ebea6e1ee3025018aa877feca232f43d4954cbe37b9` |

状態は`awaiting_human_approval`。Decision record、config、code、test、Issue recordは作っていない。

## 2. 先に報告する事実：全testが現在1件失敗している

改善候補record `ic-historical-todo-issue-intake-001--v1.json`の追加により、
一件限定Pilotの受入testが失敗している。

```text
FAILED tests/test_issue_resolution_pilot.py::test_repository_contains_only_the_single_valid_pilot_subject
1 failed, 776 passed
```

原因は`tests/test_issue_resolution_pilot.py:182`の`assert candidate_files == [CANDIDATE_PATH]`で、
候補directoryに1 fileだけを許す検査である。現在は2 fileある。

本提案が扱う問題が候補記録の追加時点で顕在化したものであり、局所修正で消さず、
新しいpilot versionの導入で解消する順序を提案§0と§6へ固定した。
本作業ではtestもconfigも変更していない。

## 3. 提案した複数Issue境界

現行の`maximum_issue_subjects: 1`は「登録できる件数」と「同時に着手できる件数」を
区別していない。`pilot_version` 4を新規に作り、三つへ分ける。v2とv3は変更しない。

| 設定 | 意味 | 提案値 |
| --- | --- | --- |
| `maximum_registered_issues` | 登録して保持できるIssue総数 | 12 |
| `maximum_active_issues` | 同時に着手できるIssue数 | **1** |
| `maximum_active_leaves` | 同時に開始できるWork Item数 | **1** |

登録だけを増やし、着手は一件のまま維持する。Work 5Aの`single_active_leaf`と矛盾しない。

早期Pilotの記録（`IC-PILOT-TODO-GROWTH-001`、`DEC-…`、`ISSUE-…`、`VERDICT-…`（`resolved`））は
旧versionの規則のまま履歴として保持し、上書きしない。新versionのvalidatorは旧記録を
新規則で再判定しない。

候補directoryの検査は、file数の固定ではなく「未triage候補が滞留していないか」へ置き換える。
testを緩めるのではなく、検査対象を契約に合った不変条件へ移す。

## 4. 機械抽出できる候補とHuman判断が必要な点

### 4.1 機械が出せるもの

固定sourceは`records/session-handoffs/2026-08-04-todo-before-compaction-001.md`（900行、85,219 bytes、
SHA-256 `16010a16…`、実fileと一致を確認済み）。Digest不一致は`intake_source_digest_mismatch`で停止する。

採用見出しは`### 未実施`、`### 残余risk`、`### 手戻り・機械化候補`（条件付き）、
`## blocker・Human判断待ち`。除外は`### verified`、`### reported_unverified／contradicted`、
`## 現在位置`、`## Git・Test`、`## 更新規則`。

除外規則はX1〜X5として決定的に固定した。特にX3は、本文に「実装済み」等があり
commit SHAまたはEvidence pathを伴う項目を落とす。実snapshotには
`commit f9adef4で実装済み`と明記された項目が複数あり、これらは履歴である。

候補ごとに、source path・Digest・見出しpath・行番号範囲・原文引用・適用した規則ID・
重複疑いを保存する。重複判定は「引用の正規化一致」と「Evidence pathの重なり」の二つだけで、
**疑いまでを出し断定しない。**

### 4.2 Human判断が必要な点

`human_fields`（`unresolved`、`recurrence`、`impact`、`priority`、`promote_to_issue`）は
機械が`null`のまま作る。埋めるのはHumanである。

一括判断してよいのは、同一見出し・重複疑いなし・完了Claimを含まない・昇格ではない処置の場合。
一件ずつ必要なのは、Issueへの昇格、重複疑いの解消、priority付与、既存Issueへの統合である。

提案§8で挙げた確認事項は三点。

1. §0の失敗をどう解消するか。推奨はv4導入で正しく解消する案。その間は全testがGREENでないため、
   他作業のcommit境界に影響する。
2. `maximum_registered_issues`を12としてよいか。
3. 候補IDの体系（`HTC-0001`形式）でよいか。

## 5. 未実施事項

- config、validator、test、既存Issue、TODO、Plan、checklist、Requirement：**変更していない**。
- 圧縮前TODOからのIssue自動昇格、候補recordの生成：**行っていない**。
- Decision record、code、test：**作っていない**。
- LLM、外部送信、外部`DATA_ROOT`、push、PR、CI、Work 4B、Work 6A、後続評価E2以降：
  **開始していない**。

検証は、固定材料7件の実在、snapshot Digestの一致、記載した事実（900行・85,219 bytes、
config v4が未作成であること、失敗test名と行番号、既存Verdictが`resolved`であること）の機械照合、
および`git diff --check`を実施し、いずれも合格した。

Human承認まで実装へ進まない。
