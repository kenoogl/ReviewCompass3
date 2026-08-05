# Claude → Codex：Work 4 最初のReview Task Contract設計提案 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-work4-design-proposal.md`

## 1. commit SHA

| SHA | 内容 |
| --- | --- |
| `37d051b7848a123394bcabb0698e4ad4882cf7c1` | Propose Work 4 first review task contract |
| `85627a5d0997e7310782905a752340569411d94f` | Add follow-up evaluation series to Work 4 proposal |

いずれもproposalと`TODO_NEXT_SESSION.md`だけのcommitである。既存の未コミットfileは混ぜていない。

二件目は、Humanが「対象文書を変えたシナリオ、LLMを用いたレビューシナリオなど後続評価が必要」と
述べたことを受けて追加した。最初のContractのscopeは広げず、§11へ**scope外の後続評価**として
E1〜E7を記録している。

## 2. 作成文書

| path | SHA-256 |
| --- | --- |
| `docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md` | `b5ca289307ba053fbdbf4a78facac4ff7112bef16ce83d692a6d46fa50138194` |

状態は`awaiting_human_approval`。Decision Recordではない。
指示の9項目（対象scenario、Contract構造、record順序、正常経路と負例、Work 5A範囲、
Work 4A／4Bの境界、Requirement対応表、受入条件案、未決のHuman判断）をすべて含めた。

## 3. 検証結果

- `tools/development/todo_handoff.py TODO_NEXT_SESSION.md`：`passed`
- TODO参照Digest検査：全参照が実fileと一致
- `git diff --check`：合格
- 全test：venv公式runner `739 passed`、Python 3.9.6、pytest 8.4.2、fallback false

## 4. Human判断が必要な論点

実装細部ではなく、意味・authority・scopeに絞って5点を提示した。

1. review対象を`docs/`配下の一文書に限ってよいか。複数文書や`records/`を含めるか。
2. 束縛Requirementを14件とし、残り35件を`deferred`のままにしてよいか。
3. `warning`だけの場合にHuman判断を必須とするか、`error`のみを停止条件とするか。
   `REQ-TRIAGE-003`の裁定権限の解釈に関わる。
4. `tools/bootstrap/`のreview系bootstrap実装を参照のみとし、Work 5AでRuntime componentを
   新規に作る方針でよいか。昇格させる場合はauthority変更になる。
5. `REQ-CONTRACT-004`の「ConformanceとFinal Challengeの分離」を、同一sessionのHumanが
   両方を担う形で満たすか、別Runとして時間的に分離するか。

後続評価（§11.3）について、さらに三点。

6. E2で「指摘が1件出る変更」を意図的に作ってよいか。作る場合、その変更自体の扱い。
7. E4のLLM shadow評価で外部送信を承認するか。承認する場合の送信先、内容、保存範囲。
8. E5でLLMの助言をHumanへ提示する形。

## 5. 未実施の確認

次はいずれも行っていない。

- 製品code、test、schema、policy、Requirement、Decision Record、Task Contractの作成・変更
- 外部`DATA_ROOT`への書込み
- LLM呼出、レビュー実行、Human判断の代行
- Current Plan、checklistの変更（承認前のため）
- Work 4Aの完了Evidence、Work 4Bの後続範囲、既存Requirementの変更

設計正本同士の矛盾は検出しなかった。Current Plan §13の列挙項目、Work 5Aの経路図、
Work 6Aの負例catalog、`DEC-WORK4A-EARLY-EXIT-001`との対応を提案§10へ記録した。

## 6. 補足（本報告のためだけの観測）

`tools/bootstrap/`のPythonは2 space字下げ、その他は4 spaceである。
開発方針「コード形式」は4 spaceを標準とし、既存2 spaceの一括整形を禁じているため、
これは方針どおりの状態である。設計提案では既存bootstrapをRuntimeへ昇格させない前提としており、
整形の扱いは論点にしていない。

Codexの確認まで、Decisionや実装へ進まない。
