# 正式再利用検索CLIの引数廃止 作業票 v1（範囲固定・軽量）

- 作成日：2026-08-18
- 指示者：利用者（Human）。選択文言「1（引数の廃止）から着手してください。事前走査から。」
  （2026-08-18 chat）
- 作成者：Claude
- 種別：範囲固定文書（軽量作業票）。CLI入口の既定値化のみ——検索本体
  （`execute_formal_search`）の挙動・判定・停止規約は不変。契約は立てない
- 固定入力：事前走査record
  `records/development/2026-08-18-reuse-search-cli-defaults-prescan-v1.md`

## 1. 目的

検索コマンドの引数手組み立て（保存先path・方針fileの版選び・時刻）を構造的に廃し、
`--plan`だけで正しく動く入口にする。規則やメモリで「気をつける」対象そのものを消す。

## 2. 正本範囲（成果物）

1. **`tools/development/formal_code_reuse_search.py`のCLI変更**：
   - `default_runtime_root()`新設＝`Path.home() / ".reviewcompass3-private" / "reuse-search"`。
   - `latest_policy_file(policies_dir, stem)`新設＝`<stem>-v<N>.json`の**数値最大版**を返す
     （該当なしは`None`）。
   - `--runtime-root`・`--universe`・`--policy`を任意化し、未指定時は上記で解決。解決不能は
     `{"status": "stopped", "reason": "policy_resolution_missing"}`・終了コード1。
   - `--captured-at`旗を削除（関数引数`captured_at`は残す）。
2. **試験の追加（RED先行）**：`tests/test_formal_code_reuse_search.py`へ4本追加
   （既存8本は変更しない）：(a) `latest_policy_file`が数値最大版を選ぶ（v9とv10を並べ
   辞書順の誤りを否定）、(b) `default_runtime_root`の値、(c) 方針解決不能時のmain停止
   （reason固定）、(d) `--captured-at`が拒否される（旗の廃止を固定）。
3. **手順書の縮小**：`docs/development/prompts/scope-prescan-run.md`の手順5コマンド雛形を
   `--plan`のみへ。正準値転記のbulletを「保存先・方針版はツールが自動解決する（上書きは
   任意引数）」へ置き換え、数値の記録規律の節の第5項を同旨へ縮める。

## 3. 範囲外

- `execute_formal_search`本体・停止規約・出力形の変更。方針writer（`write_source_universe`等）。
- 測定ブロックの機械生成（提案の単位2。別作業）。
- `records/`既存recordの書き換え。開発方針123行（入口名のみで引数記載なし＝変更不要）。

## 4. 受入条件

1. RED：追加4本のみ失敗・既存8本緑（単独終了コード非0）。
2. GREEN：`tests/test_formal_code_reuse_search.py`12本＋`tests/test_layout_baseline.py`が
   各単独終了コード0。
3. 機械確認：本機で`default_runtime_root()`の返す値が従来の正準値
   `/Users/keno/.reviewcompass3-private/reuse-search`と一致（機械出力転記）。
   方針既定解決が現在の最新（universe v8・freshness v11）を返す。
4. 手順書のコマンド雛形が`--plan`のみになる。
5. 正式再利用検索の証明書（`start_allowed: true`。変更前CLIで実行）。
6. `git diff --check`・意味単位commit・`work_unit_transition`合格。

## 5. Humanの確認が要る点（覆せる形）

1. 既定保存先を`Path.home()`基準にする設計（利用者固有pathの文字列をコードに残さない）。
2. `--captured-at`旗の完全削除（決定性が要る場面は関数引数で足りるという判断）。

## 6. 着手後の手続き

1. 作業別計画（schema 2）→本票・事前走査と同一commit。
2. 正式再利用検索（変更前CLI）→証明書commit。
3. RED→GREEN→手順書縮小→Evidence→commit。
4. TODO反映→検証→commit→`work_unit_transition`→完了報告。
