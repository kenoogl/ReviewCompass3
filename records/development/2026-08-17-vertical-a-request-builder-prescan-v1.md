# 縦A（依頼組み立て器）事前走査 v1

- 記録日：2026-08-17
- 指示者：利用者（Human）。選択文言：「縦A（依頼組み立て器）に取り組む。まず、実施内容を説明して」→
  説明後「方針了解。事前走査から進めて」（いずれも2026-08-17 chat）
- 記録者：Claude
- 種別：契約候補定義前の事前走査（5手順：所在特定・import元・Digest固定の全文検索・接続点・一覧の一元化）。
  契約定義・実装・既存文書の改定は含まない
- 範囲の基準：統合検討record §5-A・§6、設計方針メモ§1（機微検査の縦A持ち越し）・§4
- 事前確定した方針（利用者確認済み）：最初の縦切りは**2類型**（契約レビュー依頼・完了レビュー依頼）に
  限定し、類型は登録形として自由文類型を後続で足す
- 基準commit：`507b80fa2cf5bb15cc94bd29a624d446ef2a9d47`（HEAD・作業tree clean）

## 0. 一枚要約（人向け）

縦A（依頼recordの雛形生成＋機械検査）の流用部品を機械走査で固定した。主要な発見は3つ。
(1) **機械検査7項目の正式仕様が既にある**（pilot-specific §5.1.1。第7項に外部送信時の秘密情報検査を
含み、設計方針メモで持ち越した機微検査は新発明でなく既存仕様の履行になる）。(2) **`review_plan`という
既存道具がgit差分からレビュー対象・確認項目を決定的生成し、段も`scope|completion`で当方の2類型と対応**
——重複ではなく完了レビュー類型の対象列挙の流用候補である。(3) 機微検知の部品（redaction）は15 fileが
import済みの共有部品で、縦Aが加わる形は前例どおり。雛形系のcodeは存在せず新設領域である。

## 1. 手順1：所在特定【実測】

| 部品 | 所在 | 役割・状態 |
| --- | --- | --- |
| 機械検査7項目の仕様 | `docs/development/pilot-specific-claude-codex-collaboration.md` §5.1.1（173-195行） | 存在・commit済み・digest一致／必須項目と識別子／参照実在／明記事項／model対応と量上限／囲み記号／**外部送信時の秘密情報検査＋束縛Human承認**。「依頼種別ごとに検査処理を複製しない」「CLI方式では材料全文の埋め込みを要求しない」も明記 |
| 機微検知の部品 | `tools/session_logs/redaction.py` | `default_pattern_rules()`（既定5 pattern）・高乱雑性検知・`allow_patterns`対応・rules digest計算。共有部品 |
| 除外3形式（契約009固定） | `tools/external_review/send.py` 54行 `_HIGH_ENTROPY_ALLOW_PATTERNS` | X1a/X1b/X2の3形式が**送信核の私的定数**として直書き。縦Aからの参照方法は契約論点（§6-1） |
| レビュー計画の決定的生成 | `tools/development/review_plan.py`・`review_plan_cli.py`・`docs/development/prompts/review-plan-run.md` | git差分から対象・確認項目・担当数・最大周回数を生成。`--stage scope|completion`。実行名`reviewcompass3-review-plan`登録済み。完了レビュー類型の対象列挙の流用候補 |
| 実測済みの雛形基準（2類型） | `records/session-handoffs/2026-08-16-reviewer-launch-adapter-v2-review-gemini-request-v1.md`（契約レビュー型）・同`-implementation-completion-review-request-v1.md`（完了レビュー型） | 契約010で実運用・E2E完走済みの実例。構造要素：対象と固定（digest表）／開始時鮮度検査／反証4点／判定の形式／判断済み・範囲外／手順 |
| 依頼recordの実例数 | `records/session-handoffs/`の`-request-`名 | 65通（命名規約の実績母集団） |
| 起動側の接続規約 | `tools/reviewer_launch/core.py`・`record.py` | 起動は「path＋期待SHA-256」を要求。判定record名は`-request-`→`-verdict-`の機械導出（builderの命名は`-request-`を含む必要がある） |
| G02材料固定 | `tools/reviews/one_item_review.py` `prepare_material`（261行） | bytes入力から決定的材料を生成（材料同梱が要る将来類型の接続先。今回2類型はCLI自読型のため参照のみ） |
| G30操作登録・導線 | `tools/operations/operation_contract_run.py` `_OPERATIONS`・`pyproject.toml`・`docs/development/prompts/`・`AGENTS.md` §1 | 縦Bで確立した受入形式そのまま |
| 雛形の置き場の前例 | `docs/development/templates/TODO_NEXT_SESSION.template.md` | template fileの前例1件。雛形をfileにするかcode内定数にするかは契約論点（§6-6） |

## 2. 手順2：import元【実測】

- `redaction`のimport元：15 file（egress gate・send・session_logs系8・requirements・operations・
  reviews・試験1）。**広く共有された検知部品**であり、縦Aが利用者に加わる形は前例どおり。変更は不要。
- `review_plan`の参照：`review_plan_cli.py`と試験3 file（`test_review_plan.py`ほか）。自己完結しており、
  縦Aからは出力（JSON）経由の疎な流用が可能。
- 確認コマンド：`grep -rln --include="*.py" "from tools.session_logs.redaction import|..." tools/ tests/`ほか。

## 3. 手順3：Digest固定の全文検索【実測】

コマンド：`grep -ril --exclude-dir={.git,.venv,__pycache__,node_modules} -- "<語>" .`

| 語 | 一致file数 |
| --- | --- |
| 依頼record | 69 |
| 雛形 | 8 |
| template | 85 |
| 機微 | 204 |
| 組み立て | 105 |

- code層（`tools/`・`tests/`）の「雛形」一致は0（新設領域。既存名と衝突しない）。「機微」のcode層一致は
  `redaction.py`と試験4 fileのみ。
- 含意：縦Aの新設code（雛形生成・機械検査入口）は既存実装と名前衝突せず、契約候補が参照すべきfileは
  §5のdigest表で閉じた。

## 4. 手順4：接続点【実測】

1. **雛形生成→LLM記入→機械検査の二段構え**：builderは(a)雛形生成（機械欄：digest表・鮮度検査文・
   判定形式・手順・命名）と(b)機械検査（7項目＋`git check-ignore`＋機微検査）の2入口。LLM記入欄
   （反証点の文案・判断済みの選定）は生成と検査の間に挟まる。
2. **機械検査の適応**：§5.1.1の7項目を依頼record構造（対象と固定／鮮度／反証点／判定形式／判断済み・
   範囲外／手順の必須節）へ写像する。検査は1入口で2類型共通（§5.1.1「複製しない」）。
3. **機微検査**：§5.1.1第7項の履行として、依頼record内容へ既定5 pattern＋高乱雑性検知（除外3形式つき）を
   適用（headless起動は実質外部送信のため必須）。
4. **起動側との契約**：出力recordは`records/session-handoffs/`へ置き、名前に`-request-`を含める
   （adapterの判定record導出規約）。commit後のSHA-256が起動の`--expected-sha256`になる。
5. **完了レビュー類型の対象列挙**：`review_plan`（base/target commit＋riskから対象生成）の出力を
   材料にできる（流用候補。結合は出力JSON経由）。
6. **G30登録**：検査入口をprepare型操作として`_OPERATIONS`へ1 entry（前例`reviewer_launch_prepare`）。
7. **導線**：`pyproject` scripts→prompts run入口→`AGENTS.md` §1の1行（縦Bと同形式）。

## 5. digest表（契約候補v1の固定入力）【実測】

`shasum -a 256`の出力（基準commit時点）：

```text
aee8c8b72487e26395615c8442710b0695b035ec0aa129b4a777c6142864489d  docs/development/pilot-specific-claude-codex-collaboration.md
aa49774a447d84422ec885a908bb52c7a3732eb67ddb53dcc1c03fbc149245bd  tools/session_logs/redaction.py
fcecb2e35ffca0b6341cd7e102c4e6f0dc8b7b5871c36d87b8eae0a07a8d0197  tools/external_review/send.py
7b067d28994b2d4c4590646a56df975eefcdad42b3e5a16000ee034ba64d1c3f  tools/development/review_plan.py
f9877687c46f1294d5d3f3a4e5e73211b5a4acf2c86c1f91b85276f2138525d0  tools/development/review_plan_cli.py
5712357ba17086055a0808a48d9259229cdee0764e4d75e0ff656856709cb0cb  docs/development/prompts/review-plan-run.md
de658b6e96b804af393d106cbc11c39d7452e9cb54c24c5157853bc5dcd9ad57  tools/reviews/one_item_review.py
2cc7a1160adac78f71898f34e5f348ba70e4554880c4ed09b79b300be1317556  tools/operations/operation_contract_run.py
d2c8130a0e6d3a8aab351225e7218931d405463f24ed3e84a06e835e421bd913  tools/reviewer_launch/core.py
998c31d726c3aa37bd5021d83495590ad49015916ab4ca0572890465e495db8d  tools/reviewer_launch/record.py
390bc32868a2ee99f11e68d6bb9489826681674786d64b93ea207592399ac995  records/session-handoffs/2026-08-16-reviewer-launch-adapter-v2-review-gemini-request-v1.md
29819b3fd33b934ed51ced3b4f4d3982939e9b5498ed3a5fd43c0c079fddb13c  records/session-handoffs/2026-08-16-reviewer-launch-adapter-implementation-completion-review-request-v1.md
8e6a3668107b6bef114c2073c445092be1c54919decc65484e9a3def4b20648e  records/development/2026-08-17-review-path-design-principles-memo-v1.md
46a415eb630266e23a87562e6083f873e2fe9790acd34a6699f59b30aee0b45e  records/development/2026-08-16-external-review-preparation-mechanization-goal-v1.md
00b294afefa90de8cc8dc5141e9d08c23d40971d4338b9ca5021fe857f2daae0  records/development/2026-08-16-review-tooling-formalization-study-v1.md
```

## 6. 契約候補v1へ渡す論点（発見事項と推奨）

1. 【実測】除外3形式は`send.py`の私的定数。**縦Aは同値を自前の契約固定定数として宣言する**ことを推奨
   （由来を契約009へ明記。受入済み製品の私的定数へのimport結合を避け、各契約が自分の定数を所有する。
   値の同一性は試験で固定できる）。採否は契約定義で確定。
2. 【記録】機微検査は§5.1.1第7項の履行として機械検査へ含める（設計方針メモ§1の持ち越し論点の解決案）。
3. 【実測】`review_plan`は完了レビュー類型の対象列挙の流用候補。結合は出力JSON経由の疎な形とする。
4. 【記録】識別子体系：§5.1.1はAC-/NG-/ST-/OUT-接頭辞を定めるが、実測済み雛形2通は節構造＋反証点番号で
   運用実績がある。最小適応（必須節の存在検査＋反証点への固定識別子）を推奨し、全面導入は見送る。
5. 【判断】雛形の置き場：code内定数（契約固定・試験で変更管理）とtemplate file（TODO前例）の2案。
   契約の3案比較で確定する。
6. 【実測】builderの出力命名は`-request-`を含める（adapterの判定record導出`-request-`→`-verdict-`と
   整合させる機械検証項目）。
7. 【記録】2類型限定・類型登録形・自由文後続は利用者確認済みの前提（本record冒頭）。

## 7. 未実施

- 契約候補v1（契約011）の作成、5段手続き、独立確認（正式経路：agy headless起動）、実装。
- `review_plan`出力形式の詳細確認（契約定義時のRED段で実測）。
