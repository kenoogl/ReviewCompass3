# Codex → Claude：既存機械対策で閉じた5候補のHuman triage記録指示

## 誰が何をするか

- **Human**は、次の5候補を、現在残る未解決問題ではなく、既存の機械検査または恒久対策で閉じていると判断した。
  新しい正式Issueにはしないことを承認した。
- **Codex**は、承認内容をV4 Human triage decisionとして保存するよう指示する。
- **Claude**は、5件のdecision record、test receipt、TODO更新だけを作成してcommitする。

## 対象候補とHuman判断

候補bundle：`records/development/2026-08-05-historical-todo-intake-candidates-v1.json`

| candidate ID | Human判断 |
| --- | --- |
| `HTC-3AFBA652` | 一時スクリプトのfield名推測は失敗したが、既存の`resolve_effective_requirement_ids()`へ切替済みである。共通readerを使う既存の機械対策で解決済み。 |
| `HTC-75C717E1` | 不正UTF-8の扱いを変える回帰は既存Testが検出し、既存契約へ復旧済みである。 |
| `HTC-E7E2F692` | 文書化作業で手戻り、手入力転記訂正、失敗は発生していない。独立して追跡する問題はない。 |
| `HTC-5C059B48` | TODOのコミット後追加修正は、commit前に安定handoffを検査するvalidatorで恒久対策済みである。 |
| `HTC-E183A02B` | current Issue改定recordの誤配置は既存の単一subject Testが検出し、正しい版付き経路へ修正済みである。 |

上記5件すべてに、次のschema version 2 V4 Human triage decisionを作成する。

- `unresolved: false`
- `recurrence: false`
- `impact: not_applicable`
- `priority: not_applicable`
- `promote_to_issue: false`
- `disposition: historical_completed`
- `blocking: false`
- `issue_promotion: {"approved": false, "issue_id": null}`
- `supersedes: null`

`rationale`には、何が既存の機械対策で閉じているのかを平易に書く。
`historical_completed`は経緯を捨てる意味ではなく、現在の独立Issueとして追跡しない意味である。
元のPlan、Decision、Evidence、code、testは変更しない。

## 実施範囲

1. V4 decision directoryに、5candidateのdecision recordを各一件作る。
2. 各record、decision集合、V4 Issue集合をV4 validatorで検証する。
3. 候補bundleのSHA-256が`e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e`のまま、
   `human_fields`が全件`null`のままであることを確認する。
4. `.venv/bin/python3 -m pytest -q`を実行し、test receiptを
   `records/development/2026-08-05-triage-existing-machine-closure-test-receipt-v1.json`へ作る。
5. TODOを現在位置だけに更新する。判断済み22件、残り19件、正式Issue 2件、active Issue 0件とし、
   次の一作業を残り19候補のHuman triageとする。両Issueはregistered／nonblockingのままと書く。

## 禁止事項

- 正式Issue、Plan、Work、実装を作らない。
- 残る19候補、既存17 decision、既存2 Issue、候補bundle、Plan、Decision、Evidence、code、test、configを変更しない。
- push、PR、外部送信、Work 4B、Work 6A、E2以降を開始しない。

## コミットと完了報告

- 5 decision record、TODO更新、作成後のtest receiptだけを一つのcommitにする。
- 完了報告はcommitに混ぜず、次へ未追跡で保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-triage-existing-machine-closure.md`

報告にはcommit SHA、5 decision ID、候補bundle不変確認、V4 Issue数、active Issue数、全test結果、未実施事項を記す。
