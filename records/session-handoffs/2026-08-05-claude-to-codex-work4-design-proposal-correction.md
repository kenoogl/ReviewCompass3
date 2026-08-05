# Claude → Codex：Work 4設計提案のRequirement対応表訂正 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-work4-design-proposal-correction.md`

## 1. commit SHA

`257e67c06bcc7a0d6618f630c3b869a2ab4f02be`（Correct requirement mapping count in Work 4 proposal）

proposalと`TODO_NEXT_SESSION.md`だけの単一commitである。

## 2. 訂正後Digest

| path | SHA-256 |
| --- | --- |
| `docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md` | `9314c82f0526c3a3a465f31184a29e0e3209c22f7b9655507985a124e4d53220` |

TODO内の当該proposal参照Digestだけを再計算して更新した。他の参照Digestは変更していない。

## 3. 実施した訂正

指示の5項目をそのまま適用した。

1. §7本文の直接束縛数を14件から**16件**へ訂正した。
2. §7対応表へ`REQ-WORKFLOW-004`を追加した。
   obligationは「ReviewCompass3自身の文書を、通常のContract、Context、Harness、Triage、Trace、
   Workflow関門でreviewする。自己対象の特例や関門迂回を許さない」、
   受入testは`A11 自己対象でも通常経路・関門を迂回しない`とした。
3. §8.1へ`A11：自己対象のreviewでも通常経路と関門を迂回せず、自己対象の特例を作らない。`を追加した。
4. 「残る35件」を**残る34件**へ訂正した。
5. TODOの当該Digestを再計算した。

あわせて、§7末尾にあった「`REQ-WORKFLOW-004`は本Contractが自身の文書を対象とすることで満たす。
受入testはA1〜A10全体で示す」という記述を削除した。同Requirementを対応表と`A11`へ明示したため、
残すと同じ内容が二箇所に別の形で存在することになるためである。
Requirementの意味、scope、実装範囲は変更していない。

## 4. 機械確認

| 検査 | 結果 |
| --- | --- |
| §7対応表のRequirement件数 | 16（重複0） |
| 本文の束縛件数表記 | 16 |
| 本文の残り件数表記 | 34 |
| 50 − 16 | 34（一致） |
| `A11`の対応表・受入条件への出現 | 双方に存在 |

## 5. 検証結果

- `tools/development/todo_handoff.py TODO_NEXT_SESSION.md`：`passed`
- TODO参照Digest検査：全参照が実fileと一致
- `git diff --check`：合格
- 全test：venv公式runner `739 passed`、Python 3.9.6、pytest 8.4.2、fallback false

## 6. 未実施範囲

次はいずれも変更・実行していない。

- 提案の他節、後続評価E1〜E7
- Current Plan、checklist、Requirement、code、test、schema、policy
- Decision Record、Task Contract、外部`DATA_ROOT`
- LLM呼出、レビュー実行、Human判断の代行

提案の状態は`awaiting_human_approval`のままである。Decisionや実装へは進んでいない。
