# review-plan commit既定取得（対策3）事前走査 v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。文言「対策3（review-planのcommit既定取得）に着手してください。
  事前走査から」（2026-08-18 chat）
- 記録者：Claude
- 上位：精査record`records/development/2026-08-18-llm-machine-split-audit-v1.md` §4-3
- 基準commit：`1b34f90`（作業tree clean）
- 実測：測定ブロック
  `records/development/2026-08-18-review-plan-defaults-prescan-measurements-v1.md`
  （guard付き・全entry二重実行一致）

## 1. 実測と読解から確定した事実

1. CLI（`review_plan_cli.py`）は5引数**全部必須**の厳格parser（件数一致まで検査）。
2. 本体（`review_plan.py`）は`_commit`が**git `rev-parse`でcommit値を解決**しており、ref式
   （`HEAD`等）を既に受け付け、計画出力へは**解決済みSHA**が載る（`base_commit`・
   `target_commit`欄）。→ 既定値を入れても計画の固定性（SHA束縛）は失われない。
3. 保護試験は`tests/test_review_plan.py`9本（基線緑・射影で固定）。

## 2. 設計（作業票へ渡す論点）

1. `--target-commit`を任意化し**既定＝`HEAD`**（確認対象＝現在のcommitが通常。解決は既存の
   `rev-parse`機構がそのまま行い、出力に解決済みSHAが固定される）。
2. `--base-commit`は**必須のまま**とする——作業開始commitは「どこからの差分をレビュー対象と
   するか」という**意味情報**であり、機械が推測しない（run-id・slugと同じ裁定。ref式が使える
   ため64桁SHAの手書きは今日から不要である点を手順書に明記）。
3. 手順書`review-plan-run.md`の雛形から`--target-commit`行を外し、既定と「base-commitはref式
   可・SHA手書き不要」の注記を加える。
4. 本作業単位の検索計画は**新writer（`reuse_search_plan finalize`）の初実戦**で仕上げる。

## 3. 手順5：正式再利用検索

草稿→finalize→先行commit→`--plan`のみで実行。証明書は
`records/development/2026-08-18-review-plan-defaults-attestation-v1.json`へ固定。

## 4. 未実施

- 手順5、作業票の適用、RED、GREEN、手順書、Evidence、TODO・見取り図反映。
