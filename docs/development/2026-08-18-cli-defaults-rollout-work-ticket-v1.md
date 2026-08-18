# 既定値化の横展開（reviewer-launch・request-builder）作業票 v1（範囲固定・軽量）

- 作成日：2026-08-18
- 指示者：利用者（Human）。文言「精査結果をrecordに固定し、対策1（既定値化の横展開）に着手して
  ください。事前走査から」（2026-08-18 chat）
- 作成者：Claude
- 種別：範囲固定文書（軽量作業票）。CLI入口の既定値化のみ——検索・起動・検査の本体挙動、
  安全境界（読み取り専用・byte上限・digest束縛・tier照合）、判定・schemaは不変。契約は立てない
- 固定入力：事前走査record
  `records/development/2026-08-18-cli-defaults-rollout-prescan-v1.md`（実測＝測定ブロック2枚）

## 1. 目的

引数の手組み立て（正準path・日付・repository絶対パス）を構造的に廃し、検索CLIで確立した
既定値化の型を反復適用する。束縛系・意味系の引数は変えない。

## 2. 正本範囲（成果物）

1. **`tools/reviewer_launch/entry.py`**：launchの`--repository`・`--private-root`を任意化。
   既定＝cwd・`Path.home()/".reviewcompass3-private"/"reviewer-launch"`（`default_private_root()`
   として切り出し）。`check`（G30登録形）は変えない。
2. **`tools/request_builder/entry.py`**：`_parse_flags`へ`optional=()`対応を追加。assembleの
   `--date`（既定＝機械の当日日付）・`--repository`（既定＝cwd）、単体checkの`--repository`
   （既定＝cwd）を任意化。G30の`--input-root`形は変えない。
3. **試験の追加（RED先行）**：両試験fileへ計4本——(a) launchが`--repository`・`--private-root`
   省略時に既定で解決する（coreへ渡る値の機械確認）、(b) `default_private_root()`の値、
   (c) assembleが`--date`・`--repository`省略時に当日日付とcwdで解決する、(d) 単体checkの
   `--repository`省略。既存試験は変更しない（事前走査§1-4の見込みをREDで機械確認）。
4. **手順書2件の更新**：`reviewer-launch-run.md`・`request-builder-run.md`のコマンド雛形から
   該当placeholder行を削り、「既定で自動解決（上書きは任意引数）」の注記へ置き換える。

## 3. 範囲外

- 束縛系（`--request`・`--expected-sha256`）・意味系（`--run-id`・`--slug`・`--title`・
  `--type`）の変更。G30登録形（`--input-root`）。契約010・011の本体。
- private基底文字列の`tools/common/roots.py`への共有化（指紋pin更新を伴うためHuman後続選択肢）。
- 対策2（計画JSON writer）・対策3（review-planのcommit既定取得）。

## 4. 受入条件

1. RED：追加4本のみ失敗・既存緑（単独終了コード非0）。
2. GREEN：`tests/test_reviewer_launch.py`・`tests/test_request_builder.py`・
   `tests/test_reviewer_bridge.py`が各単独終了コード0。
3. 機械確認：更新後の手順書2件に対象placeholder（`<repo外私有領域の絶対パス>`等）が残らない。
4. 既定値の実機確認（`default_private_root()`の返す値）を測定ブロックで固定。
5. 正式再利用検索の証明書（`start_allowed: true`）。
6. `git diff --check`・意味単位commit・`work_unit_transition`合格。

## 5. Humanの確認が要る点（覆せる形）

1. repository既定＝cwd（`roots.repo_root()`でなく。デプロイ後の対象アプリで正しい方）。
2. private基底の共有化（roots.py pin更新を伴う）を後日行うか。

## 6. 着手後の手続き

1. 作業別計画（schema 2）→本票・事前走査・測定ブロックと同一commit。
2. 正式再利用検索（`--plan`のみ）→証明書commit。
3. RED→GREEN→手順書更新→Evidence（測定ブロック）→commit。
4. TODO反映→検証→commit→`work_unit_transition`→完了報告。
