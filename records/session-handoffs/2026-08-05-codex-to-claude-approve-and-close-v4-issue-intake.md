# Codex → Claude：Issue Intake V4の限定承認・検証閉鎖指示

## 誰が何をするか

- **Human**は、Issue Intake V4を、複数の`registered` Issueを安全に保持し、`in_progress`だけを最大1件に
  制限する**開発用・限定機能**として承認した。V4検証を閉じることも承認した。
- **Codex**は、承認と閉鎖の範囲をここに固定する。
- **Claude**は、設計状態、承認record、閉鎖Evidence、現行Plan、checklist、TODO、test receiptだけを更新して
  commitする。

この承認は、3正式IssueのPlan化・実装、正式製品schema、UI、常駐hook、自動化、Work 8評価を承認しない。
`pilot_mode: development_only_provisional`は維持する。

## 現在の事実

- 旧Issue Resolution早期Pilotはすでに閉鎖済みである。今回閉じる対象は、その後に追加した**V4複数Issue受付の実地検証**である。
- V4は、設計§5 I1〜I9・J1〜J16をTestで固定済みで、Issue数は登録上限なし、`in_progress`だけ最大1件である。
- 過去TODO候補41件は全件Human triage済みで、V4 decision 41件に競合はない。
- V4 Issueは3件、すべて`registered`かつnonblocking、active Issueは0件である。
- 設計文書`docs/design/2026-08-05-historical-todo-issue-intake-proposal.md`だけが
  `awaiting_human_approval`のままで、実装・検証済みの事実と状態が不一致である。これを訂正する。

## 作成・更新する成果物

### 1. 設計状態の訂正

`docs/design/2026-08-05-historical-todo-issue-intake-proposal.md`を、本文の事前計画を歴史として残したまま、
状態`approved_for_development_use`へ更新する。冒頭に短い実施状態注記を追加し、次を明記する。

- HumanがV4をdevelopment-only provisionalとして承認したこと。
- 実装・GREEN Evidence・41候補のHuman triageを完了したこと。
- 現在のV4 Issueは3件、active Issueは0件であること。
- 正式製品schema、UI、automation、Work 8評価、3 IssueのPlan化・実装は承認範囲外であること。

既存節の過去形・将来形を一括書換えしない。元の提案時点の説明を改竄しない。

### 2. 承認record

`records/development/2026-08-05-historical-todo-issue-intake-v4-approval-decision-v1.md`を作る。

- decision ID：`DEC-HISTORICAL-TODO-ISSUE-INTAKE-001`
- Human承認の効力：V4をdevelopment-only provisionalとして使用すること、複数registered Issueの保持、
  active Issue最大1件、Human triageに基づくIssue昇格を許可する。
- 承認対象：V4設計、V4 config、V4 validator／test、GREEN Evidence、候補bundle、41 decision、3 Issue。
  各pathと実際のSHA-256を固定する。
- 明示的な対象外：3 IssueのPlan化・実装、正式製品schema、UI、hook、watcher、scheduler、background service、
  automation、Work 8評価、外部送信。

### 3. V4検証の閉鎖Evidence

`records/development/2026-08-05-historical-todo-issue-intake-v4-closure-evidence-v1.md`を作る。

閉鎖根拠として、少なくとも次を記録する。

- V4のI1〜I9・J1〜J16のGREEN Evidence。
- 候補bundle 41件と、そのbundleが不変であること。
- 有効decision 41件、未判断0件、競合0件。
- V4 Issue 3件、active Issue 0件。各Issueはregistered／nonblockingである。
- V4設計・config・validator／test・approval recordへのpath、Digest、参照関係。
- 残余riskと後続：3 IssueのPlan化はHumanが必要時に一件ずつ判断する。V4を正式製品機能へ拡張しない。

### 4. 現行Planとchecklistの整合

`docs/current/reviewcompass3-plan-current.md`のInter-work表と説明を更新する。

- ReviewCompass Issue Resolution early Pilotのstateを、旧bootstrapだけでなくV4限定拡張まで完了した
  `verified / limited_extension_completed`として正確に示す。
- scopeに、V4の複数Issue受付、Human triage、active Issue最大1件を追記する。
- 未完了境界に、正式製品schema、UI、automation、3 IssueのPlan化・実装、Work 8評価を残す。

`docs/development/2026-08-03-initial-development-checklist.md`の早期Pilot節には、V4限定拡張の承認・閉鎖を
短く追記し、承認recordと閉鎖Evidenceを固定する。既存の早期Pilot完了記録を消さない。

### 5. TODOとtest receipt

TODOを現在位置だけに更新する。

- V4 Human triage 41件完了、V4検証閉鎖済み。
- 3 Issueはregistered／nonblocking、active Issue 0件。
- 次の一作業は、3正式IssueのどれをPlan化するかのHuman判断とする。

公式Testは、外側のpolicy runnerを使って実行する。

```text
.venv/bin/python3 -m tools.development.policy_test_runner \
  --suite full \
  --receipt records/development/2026-08-05-historical-todo-issue-intake-v4-closure-test-receipt-v1.json
```

receiptは上記pathに作る。raw pytestを直接実行してreceiptを手書きしない。

## 必須の検証

1. V4 decision単体、decision集合、V4 Issue集合をvalidatorで検証する。
2. 候補bundleのSHA-256が`e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e`のまま、
   `human_fields`が全件`null`であることを確認する。
3. 41候補すべてに有効decisionがあること、3 Issueがregisteredでactive 0件であることを確認する。
4. 上記policy runnerによる全Testと、`git diff --check`を実行する。
5. Plan／checklist／TODOを書き換えた後に、参照Digestと関連validatorを再確認する。

## 禁止事項

- 3正式IssueのPlan化・実装、Issueのstate変更、V4 config・code・testの変更をしない。
- 正式製品schema、UI、hook、watcher、scheduler、background service、automation、Work 8評価を開始しない。
- 候補bundle、41 decision、既存3 Issue、旧Early PilotのVerdict・Evidenceを変更しない。
- push、PR、外部送信をしない。

## コミットと完了報告

次だけを一つのcommitにする。

- V4設計状態の訂正
- V4 approval decision
- V4 closure evidence
- Current Plan、checklist、TODO
- V4 closure test receipt

完了報告はcommitに混ぜず、次へ未追跡で保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-approve-and-close-v4-issue-intake.md`

報告にはcommit SHA、Decision ID、閉鎖Evidence path、41候補／3 Issue／0 active確認、
policy runnerの全Test結果、変更しなかった範囲を記す。
