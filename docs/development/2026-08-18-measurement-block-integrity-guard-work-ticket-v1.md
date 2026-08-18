# 測定ブロック完全性guard 作業票 v1（範囲固定・軽量）

- 作成日：2026-08-18
- 指示者：利用者（Human）。文言「(a)で進めてください。完全性guardを先に」→根因調査後
  「コストを了解。guardの実装を再開してください。注意点として、デプロイ先の環境依存の点を
  考慮しなければならない」（2026-08-18 chat）
- 作成者：Claude
- 種別：範囲固定文書（軽量作業票）。測定tool自身の完全性強化のみ（測定対象・記録形式の互換は
  保つ。既存試験7本は無変更）。契約は立てない
- 固定入力：事前走査record
  `records/development/2026-08-18-measurement-block-integrity-guard-prescan-v1.md`・
  根因調査`records/development/2026-08-18-measurement-block-nondeterminism-investigation-v1.md`

## 1. 目的

下層（OS走査層）の一過性・希少・無音の欠落を、tool層で**検出して止める**。あわせて環境依存
（実行体・OS）を生成物が自己申告する形にし、デプロイ先での測定記録の解釈を機械可能にする。

## 2. 正本範囲（成果物）

1. **`tools/development/measurement_block.py`の強化**：
   - **二重実行guard**：各entryを2回実行し（終了コード・stdout・stderr）の完全一致を比較。
     一致→1回分を記録し「完全性：二重実行一致」。不一致→`non_deterministic`として**両回の
     出力を全文記録**し、summaryへ`non_deterministic_count`を追加、状態`incomplete`・終了
     コード1。1回目がspawn失敗・timeoutなら2回目は行わない。elapsedは1回目の値（比較しない）。
   - **実行体記録**：`shutil.which(argv[0])`の絶対pathを各entryへ機械記載（未解決は「未解決」）。
   - **実行環境記録**：headerへ`platform.platform()`を機械記載。
2. **試験の追加（RED先行）**：3本——(a) 決定的entryが「二重実行一致」と実行体絶対pathを持ち
   `non_deterministic_count`が0、(b) 非決定的entry（乱数出力）が`non_deterministic`と両回出力
   （1回目／2回目）を持ち終了コード1、(c) headerに実行環境が機械記載される。既存7本は無変更。
3. **手順書の追記**：`scope-prescan-run.md`規律1の注記へ「二重実行の完全性guard・実行体と
   実行環境の機械記録つき。**測定コマンドは読み取り専用に限る**」。
4. **事故実例での実証（dogfooding）**：欠落を起こした宣言file（SHA-256 `c474a388…`）をguard付き
   toolで再実行し、不完全な未commit生成物を完全版（二重一致・22件以上）へ差し替えてcommitする。

## 3. 範囲外

- 根因（OS層）の恒久観測・修正。三重以上の実行・timeout上限の変更。宣言schemaの変更。
- 対策2（計画JSON writer）の本体（本guard完了後に再開）。

## 4. 受入条件

1. RED：追加3本のみ失敗・既存7本緑（単独終了コード非0）。
2. GREEN：`tests/test_measurement_block.py`10本が単独終了コード0。
3. dogfooding：事故宣言fileの再実行が終了コード0・全entry「二重実行一致」・計画record数が
   22件以上（自己言及増分を含む）で固定される。
4. 手順書に読み取り専用限定とguardの注記が入る。
5. 正式再利用検索の証明書（`start_allowed: true`）。
6. `git diff --check`・意味単位commit・`work_unit_transition`合格。

## 5. Humanの確認が要る点（覆せる形）

1. 実行環境記録の粒度（v1はOS種別と版のみ。locale・PATH全体等は含めない）。
2. 三重実行など強度の引き上げ（v1は二重で確率的に十分と判断）。

## 6. 着手後の手続き

1. 作業別計画（schema 2）→本票・事前走査と同一commit。
2. 正式再利用検索（`--plan`のみ）→証明書commit。
3. RED→GREEN→手順書→dogfood差し替え→Evidence→commit。
4. TODO反映→検証→commit→`work_unit_transition`→完了報告。
