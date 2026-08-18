# review-plan commit既定取得（対策3）実行Evidence v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。文言「対策3（review-planのcommit既定取得）に着手してください。
  事前走査から」（2026-08-18 chat）
- 記録者：Claude
- 範囲固定：作業票`docs/development/2026-08-18-review-plan-defaults-work-ticket-v1.md`
- 事前走査：`records/development/2026-08-18-review-plan-defaults-prescan-v1.md`
- 基準commit：`1b34f90`→文書・計画commit `356b866`（**計画は新writerのfinalize初実戦・手書き
  digestゼロ**）→証明書commit `9e24f13`→実装は本recordと同一commit

## 1. 成果物

- `tools/development/review_plan_cli.py`【変更】：parserを必須4＋任意1へ。`--target-commit`
  省略時は`HEAD`（解決は既存`rev-parse`機構・計画出力の解決済みSHA固定は不変）。
- `tests/test_review_plan.py`【拡張】：追加2本（HEAD既定の解決・base必須の固定）＝計11本。
  既存9本は無変更。
- `docs/development/prompts/review-plan-run.md`【更新】：雛形から`--target-commit`行を除去。
  「ref式可・64桁SHAを手書きしない」「base-commitは意味情報で既定化しない」を明記。

## 2. RED→GREEN

- RED：追加2本のうち**(a) HEAD既定のみ失敗**（`1 failed, 10 passed`・単独終了コード1）。
  (b) base必須の固定は変更前後で観測が同一（引数欠落→`input_invalid`）のため**RED不能**——
  挙動保存の固定として追加した（正直な記載）。
- GREEN・受入確認：**受入測定ブロック
  `records/development/2026-08-18-review-plan-defaults-evidence-measurements-v1.md`を参照**——
  11本 exit 0（決定的射影）／手順書のplaceholder残存なし（grep該当なし＝合格側exit 1）／
  変更3fileのdigest固定。全entry二重実行一致。`git diff --check`合格。

## 3. 受入条件の照合

| # | 条件 | 結果 |
| --- | --- | --- |
| 1 | RED：追加分のみ失敗 | 合格（(b)のRED不能は§2の正直な記載どおり） |
| 2 | GREEN：11本単独0の測定ブロック固定 | 合格 |
| 3 | 手順書にtarget-commit placeholder残存なし | 合格 |
| 4 | 検索計画をwriterで仕上げ（手書きdigestゼロ） | 合格（`356b866`） |
| 5 | 証明書`start_allowed: true` | 合格（commit `9e24f13`・直接一致9件） |
| 6 | diff・意味単位commit・transition | diff合格。commit・transitionは本record commit後に実施 |

## 4. 効果と裁定

- 精査record §4の対策1〜3が**すべて完了**。レビュー計画のcommit指定は「baseの意味指定（ref式可）
  だけ」になり、64桁SHAの手書き工程は消滅。
- `--base-commit`は**意味情報として既定化しない**裁定（run-id・slug・typeと同型）。

## 5. 未実施

- TODO・見取り図反映とcommit。push（利用者の運用に従う）。
