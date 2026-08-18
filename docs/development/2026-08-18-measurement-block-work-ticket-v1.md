# 測定ブロックの機械生成tool 作業票 v1（範囲固定・軽量）

- 作成日：2026-08-18
- 指示者：利用者（Human）。選択文言「単位2（測定ブロックの機械生成）に着手してください。
  事前走査から」（2026-08-18 chat）
- 作成者：Claude
- 種別：範囲固定文書（軽量作業票）。読み取り実行・新規file生成のみの開発支援tool新設
  （既存の挙動・判定・安全境界の変更なし）。契約は立てない
- 固定入力：事前走査record
  `records/development/2026-08-18-measurement-block-prescan-v1.md`

## 1. 目的

事前走査等の【実測】節から**LLMの出力転記を構造的に排除**する。宣言したコマンド列を機械が実行し、
「コマンド＋全出力＋時刻」を機械生成markdownへ固定。recordは生成物を参照し意味の説明だけを書く。

## 2. 正本範囲（成果物）

1. **`tools/development/measurement_block.py`の新設**（事前走査§3の設計6点のとおり）：
   宣言JSON入力・argv実行（shell不使用）・機械生成markdown（new-only）・fence長の自動決定
   （内容の最長backtick連＋1）・stream上限100,000 byte（明示の切り詰め印）・終了コード0／1／2・
   一行JSON summary。宣言fileのSHA-256は`tools.common.digests.file_sha256`で機械埋め込み。
2. **試験の新設（RED先行）**：`tests/test_measurement_block.py`。(a) 実行と生成物の内容
   （argv・終了コード・全文）、(b) new-only停止（既存出力pathで2・上書きなし）、(c) 入力不備2、
   (d) コマンド非0終了はデータとして記録されtoolは0・`failed_count`計上、(e) **敵対fixture＝
   出力が```を含む場合**に外側fenceが伸び内容が無加工で残る、(f) 上限超過の切り詰め印、
   (g) spawn失敗でtoolは1。
3. **手順書の改定**：`scope-prescan-run.md`の数値の記録規律に「実測はまず測定ブロック
   （宣言JSON→機械生成file）で行い、recordは生成物を参照する。転記は生成物が使えない場合の
   例外」を加え、規律1〜2項をその従属へ縮める。

## 3. 範囲外

- 過去recordの【実測】節の書き換え（以後の新規作業から適用）。
- 測定ブロックの自動commit・TODO連動。宣言JSONの雛形生成器。sandbox・権限制御
  （実行者は従来どおり操作者自身。toolはshell注入の余地を作らないだけ）。

## 4. 受入条件

1. RED：新設試験が実装前に失敗（単独終了コード非0）。
2. GREEN：新設試験＋`tests/test_session_log_record_run.py`（流用元の保護）＋
   `tests/test_shared_function_sweep.py`が各単独終了コード0。
3. 実地確認：本作業単位のEvidence用測定を**本tool自身で生成**し（dogfooding）、生成物を
   Evidenceから参照する。
4. 敵対fixture（fence偽装）試験が含まれること（事前走査の必読入力適用）。
5. 正式再利用検索の証明書（`start_allowed: true`）。
6. `git diff --check`・意味単位commit・`work_unit_transition`合格。

## 5. Humanの確認が要る点（覆せる形）

1. 生成物の置き場の既定（本作業では`records/development/`配下へ`…-measurements-v1.md`として
   commitする運用。別置き場が良ければ次版で変更可能）。
2. stream上限100,000 byteの値。

## 6. 着手後の手続き

1. 作業別計画（schema 2）→本票・事前走査と同一commit。
2. 正式再利用検索（`--plan`のみ）→証明書commit。
3. RED→GREEN→dogfooding測定→手順書改定→Evidence→commit。
4. TODO反映→検証→commit→`work_unit_transition`→完了報告。
