# 計画JSON writer（対策2）作業票 v1（範囲固定・軽量）

- 作成日：2026-08-18
- 指示者：利用者（Human）。文言「対策2（計画JSON writer）を再開してください」（2026-08-18 chat）
- 作成者：Claude
- 種別：範囲固定文書（軽量作業票）。開発支援toolの新設のみ（検索本体・計画schema・停止規約は
  不変）。契約は立てない
- 固定入力：事前走査record`records/development/2026-08-18-plan-writer-prescan-v1.md`
  （実測＝guard付き測定ブロック）

## 1. 目的

正式再利用検索の計画JSONの`content_digest`埋め込みを、LLMの手書きscript実行（本日までの全計画で
発生）から専用入口へ移し、**検索と同一の検証に合格した計画だけがcommitされる**形にする。

## 2. 正本範囲（成果物）

1. **`tools/development/reuse_search_plan.py`の新設**（事前走査§2の設計どおり）：
   `finalize`（digest機械埋め込み＋`_validate_plan`再利用・合格時のみ書換え・digest既存は
   `already_finalized`）・`verify`（構造とdigestの照合・attestation既存は正常として合格）。
   一行JSON・0／2／1・`--project-root`既定cwd。
2. **試験の新設（RED先行）**：`tests/test_reuse_search_plan.py`6本——(a) finalizeがdigestを
   埋め込み検証合格で書き換える、(b) digest既存で停止・file無変更、(c) 不正計画で停止・
   file無変更、(d) verifyが完成計画（attestation existing含む）を合格させる、(e) 改竄digestを
   検出して停止、(f) `-m`起動の疎通。
3. **手順書の追記**：`scope-prescan-run.md`手順5へ「作業別計画はfinalizeで仕上げる。手書き
   script・手計算digestを使わない」を1行。
4. **dogfooding**：committedの全計画record（`record_kind`で機械抽出）をverifyで一括照合し、
   測定ブロック（読み取り専用）で固定する。本作業単位の計画自身も含める。

## 3. 範囲外

- 検索本体（`formal_code_reuse_search.py`）・計画schema・`_validate_plan`の変更。
- 草稿内容（capability宣言）の生成支援（意味作業はLLMの役割のまま）。
- 対策3（review-planのcommit既定取得）。

## 4. 受入条件

1. RED：新設6本のみ失敗（単独終了コード非0）。
2. GREEN：新設6本＋`tests/test_formal_code_reuse_search.py`12本が各単独終了コード0。
3. dogfooding：全committed計画のverify一括照合が全件合格で測定ブロックに固定される。
4. 手順書に追記が入り、以後の手順から手書きdigest工程が消える。
5. 正式再利用検索の証明書（`start_allowed: true`。本計画のdigestは最後の手書きとし、GREEN後に
   verifyで機械照合する）。
6. `git diff --check`・意味単位commit・`work_unit_transition`合格。

## 5. Humanの確認が要る点（覆せる形）

1. verifyの`output_already_exists`許容（検索実施済みの正常扱い）と複数search計画での限界の明記。
2. 草稿の置き場運用（records/直下で作成→finalize→commitの現行のまま）。

## 6. 着手後の手続き

1. 作業別計画（schema 2・最後の手書きdigest）→本票・事前走査と同一commit。
2. 正式再利用検索（`--plan`のみ）→証明書commit。
3. RED→GREEN→手順書→dogfooding→Evidence→commit。
4. TODO・見取り図反映→検証→commit→`work_unit_transition`→完了報告。
