# 終了コード語彙の是正（候補3） 作業票 v1（範囲固定・軽量）

- 作成日：2026-08-18
- 指示者：利用者（Human）。選択文言「その後、候補3を対応」（2026-08-18 chat）
- 作成者：Claude
- 種別：範囲固定文書（軽量作業票）。**終了コードの値を1つ変えるが、判定の意味・schema・安全
  境界は不変**であり、影響範囲は変更1箇所＋固定試験1本と限定的（事前走査§2の実測）。契約は
  立てない
- 固定入力：事前走査record
  `records/development/2026-08-18-session-log-exit-code-vocabulary-prescan-v1.md`
- 対象候補：`IC-SESSION-LOG-EXIT-CODE-VOCABULARY-001`（仕分け＝採用）

## 1. 目的

`partial`（手順書自身が「既知の正常状態」と呼ぶ状態）に**失敗コード5**を返している箇所を直す。
この1箇所が原因で、包み役は終了コードを合否判断に使えず要約JSONを読む迂回を強いられ、その迂回を
説明する但し書きが手順書に必要になり、**独立レビュー4回中4回がそれを誤読した**（RQ2実験の実測）。

## 2. 正本範囲（成果物）

1. **`tools/session_logs/eventual_preservation.py` 898行の変更**：
   `return 0 if result.status == "ok" else 5` を、`partial`のとき`EXIT_UNSUPPORTED`（4）を返す形
   へ改める（事前走査§4の案A）。生の数字をやめ、`tools/session_logs/cli.py`の定数を取り込む。
   `ok`は0のまま。それ以外（例外経路の`error`）は`EXIT_FAILED`（5）のまま。
2. **試験の追加（RED先行）**：`partial`が4を返し`ok`が0を返すことを固定する試験。既存試験
   `tests/test_session_log_record_run.py` 157行の期待値（`exit_code == 5`）を4へ改める——
   **試験の意図は保存する**（partialの系統が包み役では成功扱いになる、という検査は不変）。
3. **手順書の追記**：`docs/development/prompts/session-log-record-run.md` §2の「系統ごとの
   `exit_code`はokで0・partialで5」を実装に合わせる。

## 3. 範囲外

- **`tools/session_logs/read_only_entry.py`の語彙（`EXIT_PARTIAL=3`）は触らない**。自分の語彙の
  中では正直な値であり、消費側（`safe_storage_entry.py` 76行）の分析が別途要る。統合するなら
  別の作業単位（事前走査§5-2）。
- `cli.py`の語彙の定義そのものの変更。
- 包み役（`record_run.py`）の合否判断の変更（要約JSONの`status`欄を読む現行のまま）。
- **RQ2実験のケース材料`docs/evaluation/rq2-cases/`の更新**（実験時点の複製。封緘済み）。

## 4. 受入条件

1. RED：新設試験が実装前に失敗（単独終了コード非0）。
2. GREEN：新設試験＋**session_logs系233本**（基準commit `70afe24`で実測）の全通過（単独終了
   コード0）。
3. `partial`の系統で包み役が引き続き0を返すこと（`overall_ok`が真）を試験で機械確認する。
4. 手順書§2の記述が実装と一致すること。
5. RQ2実験の材料`docs/evaluation/rq2-cases/`が無変更で、正解表v2のdigest表が全件一致すること。
6. 正式再利用検索の証明書（`start_allowed: true`）。
7. `git diff --check`・意味単位commit・`work_unit_transition`合格。

## 5. 着手後の手続き

1. 作業別計画（schema 2）作成→先行commit。
2. 正式再利用検索→証明書固定。
3. RED→失敗確認→commit。
4. GREEN→全緑→commit。
5. 手順書§2の追記→受入条件の機械確認→完了報告。
