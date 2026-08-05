# 定型記録生成 Plan承認Decision v1

- decision ID：`DEC-RECORD-GENERATION-PLAN-001`
- decision maker：Human
- decided at：2026-08-05
- 対象Issue：`ISSUE-HTC-66C3E6CA`
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-implement-record-generation-todo-slice.md`

## 1. Humanが承諾した5点

Humanは、Plan提案`docs/design/2026-08-05-record-generation-issue-plan-proposal.md`の
Human判断項目について、次の5点を一括で承諾した。

1. **最初の対象はTODOだけに限定する。** 提案の案Aを採る。Evidence／Decisionへの一般化（案B）は
   この決定に含まない。
2. **Test件数はstdoutを正規表現で読むのではなく、公式Test receiptの構造化集計から得る。**
   提案§2.2の選択肢Aに相当する。
3. **自動生成したTODOは、作業本体と同じ意味単位commitへ含める。** TODOだけの追加commitを作らない。
4. **Evidence／Decisionへの拡張は、TODOで複数回の実運用が手入力訂正なしで通ってから**Humanが判断する。
5. **実装はTest先行**で、次の順に段階を分ける。
   1. 受領証の集計（公式Test receiptへ構造化`test_summary`を追加する）
   2. TODO用材料の収集・検証
   3. root TODOへの更新経路の切替

## 2. 承認対象と実Digest

| 種別 | path | SHA-256 |
| --- | --- | --- |
| Plan提案（承認対象） | `docs/design/2026-08-05-record-generation-issue-plan-proposal.md` | `79ed49831ebd9b69c9713fcd71becfaa1d85f7fd97759e5fff373f99126a2a7c` |
| 対象Issue | `.reviewcompass/workflow/issues-v4/issue-htc-66c3e6ca--v1.json` | `56e0911d6f565915ca0ad7737eae7befbb30d686d344eb5367ecc95598a8c732` |
| Human triage decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-66c3e6ca--v1.json` | `bb2cfbb618f5b1ee918018a1ae4ae78d74a25eccb26a7cd46e07685571c31e5f` |
| TODO手順 | `docs/development/prompts/todo-handoff-update.md` | `eff64878479ce82a48f8e5b4160dd7913364268c9e94d1a6f0a63087e7fb0f4d` |
| Test runner | `tools/development/policy_test_runner.py` | `21ad04f205855832c46d7b192c4fb3205c185c9fd3b7904eb42d8f064f4e3b69` |
| TODO renderer | `tools/development/todo_handoff_projection.py` | `e43982c5c3f0e7930e21995c380d81b998515acd545214ae6efe5a5ec2d5cc89` |
| TODO validator | `tools/development/todo_handoff.py` | `17077dde9953a93b316e600fe8762a2e4a42ef3f95b13f824a34b22a55a8d43d` |
| TODO compaction validator | `tools/development/todo_compaction.py` | `0e446f9aa100d8128c32a3ddbcaca601e66aead9548db349b11a9f5adde89a1f` |

Plan提案を除く7件は、Plan提案が固定入力として記録した値と作業開始時点で一致することを機械確認した。

## 3. この決定が承認していないこと

- Evidence／Decisionの定型欄への一般化（案B）。判断は承諾4の条件が満たされてからである。
- Evidence／Decisionの自動生成、既存Evidence／Decision／receiptの一括書換え。
- `ISSUE-HTC-66C3E6CA`を含むIssueのstate変更。3 Issueは`registered`のままである。
- V4の正式Issue Resolution Plan、Task Contract、Workflow permitの作成。
- UI、hook、watcher、scheduler、background service。
- Git／shell／外部toolの実行routing（`ISSUE-HTC-C9F6C917`の範囲）。
- push、PR、外部送信。

## 4. 実装の停止条件

次に達したら、局所patchで続けず停止してHumanへ報告する。

1. Planの固定input digestが作業開始時点で不一致である。
2. 構造化集計をmachine APIで得るために、承認範囲を超えるpolicy／config／外部依存の変更が要る。
3. root TODOを更新すると、自由文、link label、link path、順序など非機械管理部分も変わる。
4. 二段確認で二つの集計が不一致、または更新失敗時に原状復帰できない。
5. 既存Task Contractまたはauthorityの固定source整合が崩れ、新しいHuman判断が要る。
