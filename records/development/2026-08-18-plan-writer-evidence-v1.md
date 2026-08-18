# 計画JSON writer（対策2）実行Evidence v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。文言「対策2（計画JSON writer）を再開してください」（2026-08-18 chat）
- 記録者：Claude
- 範囲固定：作業票`docs/development/2026-08-18-plan-writer-work-ticket-v1.md`
- 事前走査：`records/development/2026-08-18-plan-writer-prescan-v1.md`
- 基準commit：`0c5d1eb`→文書・最終手書き計画commit `d338da4`→証明書commit `44486b1`→実装は
  本recordと同一commit

## 1. 成果物

- `tools/development/reuse_search_plan.py`【新設】：`finalize`（digest機械埋め込み＋検索側
  `_validate_plan`の丸ごと再利用・合格時のみ書換え）・`verify`（attestation既存を検索実施済みの
  正常として扱う照合）。一行JSON・0／2／1。
- `tests/test_reuse_search_plan.py`【新設】：6本（埋め込み・already_finalized・不正停止で
  無変更・verify合格・改竄検出・`-m`疎通）。
- `docs/development/prompts/scope-prescan-run.md`【追記】：手順5「計画はfinalizeで仕上げる。
  手書きscript・手計算digestを使わない」＋規律1「揺れる出力は宣言側で決定的な射影に整形」。
- 受入測定：宣言`…plan-writer-evidence-commands-v1.json`＋機械生成
  `…plan-writer-evidence-measurements-v1.md`（guard付き・全entry二重実行一致）。

## 2. RED→GREEN

- RED：`6 failed`・単独終了コード1（terminal転記）。
- GREEN・受入確認：**受入測定ブロックを参照**——writer 6本・検索側12本（決定的射影＝件数と
  終了コードのみ印字）各exit 0／**committed全22計画の一括verify全件合格**（schema 1の4計画を
  含む。歴史的な手書きdigestに誤りゼロを機械実証）／変更3fileのdigest固定。`git diff --check`合格。

## 3. guardの初実戦記録（正直な記載）

初回の受入測定で完全性guardが`non_deterministic` 1件を検出した。原因はpytestが出力へ実行時間
（`in 0.78s`等）を含むためで、**tool側は設計どおり厳格に働き、宣言側が不適切**だった。対処は
方針どおり宣言側で行い（pytestを「件数・終了コードのみ印字する決定的射影」へ包む）、この作法を
手順書規律へ追記した。両回出力の全文保存（法医学的記録）も同時に実証された。

## 4. 受入条件の照合

| # | 条件 | 結果 |
| --- | --- | --- |
| 1 | RED：新設6本のみ失敗 | 合格（§2） |
| 2 | GREEN：6本＋検索側12本 各単独0 | 合格（受入測定ブロック） |
| 3 | 全committed計画のverify一括合格の固定 | 合格（22／22） |
| 4 | 手順書追記＝手書きdigest工程の廃止 | 合格（§1） |
| 5 | 証明書`start_allowed: true` | 合格（commit `44486b1`・直接一致14件＝`_validate_plan`等の再利用根拠） |
| 6 | diff・意味単位commit・transition | diff合格。commit・transitionは本record commit後に実施 |

## 5. 効果（構造的に消えた手作業）

計画JSONのdigest手書きscript実行（本日6回発生）は行為として消滅。`d338da4`の計画が**最後の
手書き**であり、本計画自身もverify合格で機械照合済み（§2の22件に含まれる）。以後、検索の計画は
「LLMが草稿（意味宣言）を書く→finalizeが仕上げる→検索と同一検証に合格した計画だけがcommitされる」
の一本道になる。

## 6. 未実施

- TODO・見取り図反映とcommit。push（利用者の運用に従う）。
- 対策3（review-planのcommit既定取得）は候補のまま（着手はHuman指示ごと）。
