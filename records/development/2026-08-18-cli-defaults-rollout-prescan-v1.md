# 既定値化の横展開（reviewer-launch・request-builder）事前走査 v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。文言「精査結果をrecordに固定し、対策1（既定値化の横展開）に着手して
  ください。事前走査から」（2026-08-18 chat）
- 記録者：Claude
- 上位：精査record`records/development/2026-08-18-llm-machine-split-audit-v1.md` §4-1
- 基準commit：`ccf2edc`（作業tree clean）
- 実測：**測定ブロック2枚**（本作業単位から実測は機械生成を全面適用）
  - `records/development/2026-08-18-cli-defaults-rollout-prescan-measurements-v1.md`
  - `records/development/2026-08-18-cli-defaults-rollout-prescan-measurements-v2.md`

## 1. 実測から読み取った事実（意味の説明。数値・出力は測定ブロックが正）

1. 両CLIは**argparse不使用**の自前厳格parser（未知flag・required欠落→`invalid_arguments`・
   終了コード2）。`reviewer_launch`のparserはoptional対応済み、`request_builder`のparserは
   optional**未対応**（`optional=()`引数の追加が要る）。
2. `private_root`の使用は`tools/reviewer_launch/entry.py`のlaunch系1箇所。
3. **run-idは意味符号**（`cr-013-001`＝契約と連番・`rq2b2-case-001-b`＝実験ケースと条件・
   `…r`＝再実行）。機械採番すると意味が失われるため、**機械化の対象外と裁定**する（識別子の
   命名は意味選定＝LLM／操作者の正当な役割。精査record §2の「run-id命名も手作業」はこの趣旨へ
   訂正して読む）。
4. 既存試験（`test_reviewer_launch.py`・`test_request_builder.py`）は対象flagを**正常系の
   全引数渡しでのみ**使い、欠落時の`invalid_arguments`を固定していない——任意化しても既存緑は
   保たれる見込み（RED実行で機械確認する）。
5. 保護試験は3file（reviewer_launch・request_builder・reviewer_bridge）。

## 2. 設計（作業票へ渡す論点）

1. `reviewer_launch` launch：`--repository`・`--private-root`を任意化。既定＝**cwd**・
   `Path.home()/".reviewcompass3-private"/"reviewer-launch"`。`check`（G30登録形）は不変。
2. `request_builder`：parserへ`optional=()`を追加。assemble：`--date`・`--repository`を任意化
   （既定＝機械の当日日付・cwd）。単体check：`--repository`任意化（既定cwd）。G30の
   `--input-root`形は不変。
3. **束縛系（`--request`・`--expected-sha256`）と意味系（`--run-id`・`--slug`・`--title`・
   `--type`）は不変**（束縛は承認境界の一部・意味は正当なLLM役割）。
4. デプロイ整合：repository既定は**cwd**とする。`roots.repo_root()`はRC3自身のrootであり、
   pip導入後の対象アプリでは誤る（module起動は「repository根元から」の政策と整合）。
5. private基底（`~/.reviewcompass3-private`）の文字列は`formal_code_reuse_search`に続き2箇所目。
   共有化は`tools/common/roots.py`の指紋pin更新（状態固定試験の変更→Issue限定再開）を伴うため、
   本作業では行わず**Human後続選択肢**として残す。
6. 手順書2件のコマンド雛形から該当placeholder行を削り、自動解決の注記へ置き換える。

## 3. 手順5：正式再利用検索

作業別計画の先行commit後、`--plan`のみで実行。証明書は
`records/development/2026-08-18-cli-defaults-rollout-attestation-v1.json`へ固定する。
注記（正直な記載）：計画JSONの`content_digest`埋め込みは対策2（計画writer）未着手のため、
今回も手書きscript実行で行う（精査record §2の既知穴。**本作業単位を最後の実例とし、対策2で
排除する**）。

## 4. 未実施

- 手順5の実行、作業票の適用、RED、GREEN、手順書更新、Evidence、TODO反映。
