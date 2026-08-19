# issue実態調書tool 実行Evidence v1

- 記録日：2026-08-19。指示者：利用者（Human）「その内容で改善候補を登録して、すぐに対応」（chat）
- 範囲固定：作業票`docs/development/2026-08-19-issue-dossier-work-ticket-v1.md`／事前走査同
  prescan v1。基準`2520c8c`→文書・計画（writer）`a58ccb7`→証明書`03c7c39`→実装は本record同一commit
- 対象候補：`IC-ISSUE-RECONCILIATION-DOSSIER-001`（current_work・候補と決定は**writer経由で登録**）

## 1. 成果物

`tools/development/issue_reconciliation_dossier.py`【新設】：issueごとの機械調書——台帳欄・
登録後の活動（`records/development`とgit履歴の言及計数）・problem参照pathの生存・**TODO active
拘束flag**——を一行JSONで出力（全件／`--issue-id`単独・決定的・判断欄なし）。試験4本【新設】
（fixture調書・未知ID拒否・拘束flag・実repo 8件で`ISSUE-TEST-GROWTH-STATE-PINNING-001`の
拘束flag機械検出を固定）。

## 2. RED→GREEN（受入で別件2本を検出）

RED＝新設4本のみ失敗（`4 failed`・terminal転記）。**受入1回目**
（`…-evidence-measurements-v1.md`・失敗の記録として保存）で、本tool群とは別の**状態固定の
焼き込み2本**が検出された：

1. 自作`test_real_repository_counts_issues`（同日新設）の`registered>=8`——突合の正当な遷移で
   破綻。内訳を焼き込まない整合式へ意図保存修正。
2. `test_l6`（既存）の`保存数==有効数`——「保存された全issueは非終端」という当時状態の焼き込み。
   既裁定に従い**対象限定再開record**
   （`records/development/2026-08-19-state-pinning-limited-reopen-test-l6-decision-v1.md`）を
   固定のうえ「保存数＝有効＋終端」へ意図保存修正（Issue状態は`registered`のまま・再開は同record
   で閉止）。

**受入2回目**（`…-evidence-measurements-v2.md`）＝lane系26本exit 0・台帳関連68本exit 0・
実repo調書exit 0（8件・拘束flag検出）・全entry二重実行一致。`git diff --check`合格。

## 3. 手戻りの記録（正直な記載）

`test_l6`の赤は突合commit（`17d7b1f`）時点から潜在していた。突合の受入で台帳一括検証は回したが
**intake試験群まで回していなかった**のが原因（1 commit間の潜在）。教訓＝台帳を変更する作業単位の
受入にはintake試験群を含める（本受入の宣言JSONがその実例）。

## 4. 効果

- 突合の裁定材料の機械部分（活動・生存・拘束）が調書として機械生成でき、LLMの都度調査と
  見落としriskが消えた。今回人手で偶然気づいた拘束（TODO active欄）は、**実repo試験で機械検出を
  固定**した。
- 候補登録から仕分けまで**writerのみで完了**（使い捨てscriptゼロ）＝lane機械化の実運用実証2件目。

## 5. 未実施

TODO反映とcommit。push（利用者の運用に従う）。治癒確認probe拡張（将来・候補scope外出し済み）。
