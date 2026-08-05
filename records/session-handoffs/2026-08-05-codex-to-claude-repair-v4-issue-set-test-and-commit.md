# Codex → Claude：V4 Issue集合テストの根本修正とIssue登録完了指示

## 誰が何をするか

- **Human**は、V4設計の「登録済みIssue数は無制限、`in_progress`だけ最大1件」という規則を優先し、
  `test_l6_repository_issue_set_is_consistent`の1件決め打ちを一般則へ直すことを承認した。
- **Codex**は、今回の承認範囲をここに固定する。
- **Claude**は、指定されたテスト1か所、既に作成済みの5 decision record・V4 Issue・test receipt・TODOだけを
  完成させてcommitする。

## 修正するテスト（唯一の既存test変更）

対象：`tests/test_issue_intake_v4.py`の`test_l6_repository_issue_set_is_consistent`。

現行の次の決め打ちを置き換える。

```python
assert list(effective) == [SESSION_POLICY_CANDIDATE]
issue = effective[SESSION_POLICY_CANDIDATE]
assert issue["issue_id"] == SESSION_POLICY_ISSUE_ID
assert issue["problem"] == SESSION_POLICY_PROBLEM
```

置換後は、次を検証する形にする。

```python
assert SESSION_POLICY_CANDIDATE in effective
issue = effective[SESSION_POLICY_CANDIDATE]
assert issue["issue_id"] == SESSION_POLICY_ISSUE_ID
assert issue["problem"] == SESSION_POLICY_PROBLEM
```

意味は「既存の会話記録Issueが残り、内容が変わらない」である。
追加Issueを禁止してはならない。すでに同じtest前半が、すべてのIssueについて候補・decisionとの結線と
`registered`状態を確認し、active Issue数が0であることを確認している。その検査は変えない。

これは`ISSUE-HTC-C9F6C917`だけを例外にするパッチではない。V4の無制限登録規則へテストを一致させる修正である。

## 既に作成済みの成果物を完成させる

前の指示書
`records/session-handoffs/2026-08-05-codex-to-claude-triage-machine-operation-root-issue.md`
に従って作成済みの、次の未追跡成果物を使用する。

- V4 Human triage decision 5件（`DEC-HTC-C9F6C917`と残る4件）
- V4 Issue：`ISSUE-HTC-C9F6C917`（`registered`、nonblocking）
- test receipt：`records/development/2026-08-05-triage-machine-operation-root-issue-test-receipt-v1.json`

receiptは、前回の実行失敗を正確に記録した未追跡の暫定ファイルである。
テスト修正後の実行結果へ**同一pathで置き換え**、`passed`、実際の件数・exit code・stdout・source state digestを記録する。
失敗receiptをcommitに残さない。

TODOは次に更新する。

- 判断済み17件、残り24件
- 正式Issue 2件、active Issue 0件
- `ISSUE-HTC-BEB5E0BD`と`ISSUE-HTC-C9F6C917`はともに`registered`かつnonblocking
- 次の一作業：残り24候補のHuman triage

## 必須の検証

1. V4 decision単体、decision集合、V4 Issue集合をvalidatorで検証する。
2. 候補bundleがSHA-256 `e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e`のまま不変であることを確認する。
3. `ISSUE-HTC-BEB5E0BD`が残り、そのcontentが変わらないことを確認する。
4. `.venv/bin/python3 -m pytest tests/test_issue_intake_v4.py -q`を実行する。
5. `.venv/bin/python3 -m pytest -q`を実行する。
6. `git diff --check`を実行する。

## 禁止事項

- 上記1か所以外の既存test、code、runner、config、policy、Plan、Decision、Evidenceを変更しない。
- IssueのPlan化、Git／shell／Python cache自動化の実装、push、PR、外部送信をしない。
- 既存12 decision、既存Issue、候補bundleを変更しない。
- Claude完了報告をcommitに入れない。

## コミットと完了報告

次だけを一つのcommitにする。

- `tests/test_issue_intake_v4.py`の上記1か所
- V4 decision record 5件
- `.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json`
- test receipt 1件
- `TODO_NEXT_SESSION.md`

完了報告はcommitに含めず、次へ未追跡で保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-repair-v4-issue-set-test-and-commit.md`

報告にはcommit SHA、変更したtestの意味、5 decision ID、正式Issue ID、候補bundle不変確認、
2 Issue／0 active Issue確認、対象testと全test結果、未実施事項を記す。
