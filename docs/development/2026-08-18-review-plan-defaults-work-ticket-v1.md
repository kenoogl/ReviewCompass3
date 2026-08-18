# review-plan commit既定取得（対策3）作業票 v1（範囲固定・軽量）

- 作成日：2026-08-18
- 指示者：利用者（Human）。文言「対策3（review-planのcommit既定取得）に着手してください。
  事前走査から」（2026-08-18 chat）
- 作成者：Claude
- 種別：範囲固定文書（軽量作業票）。CLI入口の既定値化のみ（計画生成本体・schema・停止規約は
  不変）。契約は立てない
- 固定入力：事前走査record
  `records/development/2026-08-18-review-plan-defaults-prescan-v1.md`（実測＝guard付き測定ブロック）

## 1. 目的

レビュー計画生成のcommit引数手書きを減らす。`--target-commit`は機械既定（`HEAD`）へ、
`--base-commit`は意味情報として残し、ref式で渡せる事実を明文化してSHA手書きを不要にする。

## 2. 正本範囲（成果物）

1. **`tools/development/review_plan_cli.py`**：parserを「必須4（base-commit・risk・stage・
   classification）＋任意1（target-commit・既定`HEAD`）」へ。解決は既存`rev-parse`機構のまま
   （出力の解決済みSHA固定は不変）。
2. **試験の追加（RED先行）**：`tests/test_review_plan.py`へ2本——(a) `--target-commit`省略時に
   計画の`target_commit`がHEADの解決済みSHAになる、(b) `--base-commit`省略は従来どおり
   `input_invalid`・終了コード2（意味必須の固定）。既存9本は無変更。
3. **手順書の更新**：`review-plan-run.md`雛形から`--target-commit`行を外し、既定と
   「base-commitはref式可（SHA手書き不要）」を注記。

## 3. 範囲外

- `build_review_plan`本体・計画schema・`plan_sha256`束縛。`--base-commit`の既定化（意味情報）。

## 4. 受入条件

1. RED：追加2本のみ失敗・既存9本緑（単独終了コード非0）。
2. GREEN：`tests/test_review_plan.py`11本が単独終了コード0（決定的射影で測定ブロックへ固定）。
3. 手順書に`--target-commit`のplaceholder行が残らない。
4. 検索計画は新writerのfinalizeで仕上げる（手書きdigestゼロの初実戦）。
5. 正式再利用検索の証明書（`start_allowed: true`）。
6. `git diff --check`・意味単位commit・`work_unit_transition`合格。

## 5. Humanの確認が要る点（覆せる形）

1. `--base-commit`を必須のまま残す裁定（意味情報。既定化はしない）。

## 6. 着手後の手続き

1. 計画草稿→**finalize（新writer初実戦）**→本票・事前走査と同一commit。
2. 正式再利用検索→証明書commit。
3. RED→GREEN→手順書→Evidence→commit。
4. TODO・見取り図反映→検証→commit→`work_unit_transition`→完了報告。
