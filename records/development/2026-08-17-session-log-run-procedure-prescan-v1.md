# セッションログ記録run手順書の事前走査 v1

- 記録日：2026-08-17
- 指示者：利用者（Human）。観察指摘「セッションログの記録処理を指示すると、ファイル検索、
  コマンドの使い方調べ、コマンドの使用前歴調べ、などを行っている。また、解釈の非対応あり。
  これは、導線と機械処理手続きができていないためと考えられる」→確認報告の後、選択文言
  「対処を進める」（推奨案＝run手順書作成の範囲固定文書。いずれも2026-08-17 chat）
- 記録者：Claude
- 種別：作業単位定義前の事前走査（6手順。`docs/development/prompts/scope-prescan-run.md`の
  適用第4号）。範囲固定文書の起草・手順書本体の作成・導線改定は含まない
- 範囲の基準【実測】：2026-08-16セッション（`e8ff36d9-7e9d-405e-8115-17d3c3066dc9`）で、
  指示「まず、セッションログを記録」（02:02:37Z）から次の利用者発言（02:12:37Z）まで10分00秒・
  道具呼び出し45回（Bash 42・Read 3）。内容はファイル検索、実装ソースからの使い方逆算、
  過去セッション記録からの実行コマンド発掘、解釈非対応68件の正体再調査
- 必読入力：文字列理解の失敗類型と対策原則（§5 digest表に固定）——本主題は実行コマンドと
  機械出力転記を含む手順書の新設であり、原則1（fail-closed）・原則6（raw先行保存・解釈不能の
  正直な申告）が実装済み部品の挙動として関わる
- 基準commit：`ab78054`（作業tree clean）

## 0. 一枚要約（人向け）

セッションログの全件保全は`collect-eventual`（実装済み・試験あり）で機械化済みだが、**実行手順書と
導線が存在しない**ため、指示のたびにゼロから再発掘している。主要な発見は3つ。
(1) 実行の正しい形は2026-08-16の成功前歴で確定できる（3系統×必須4引数）。
(2) 「解釈の非対応」は仕様どおりの既知状態（先頭recordが本文形式でないfileは解釈対象外・生ログの
保全自体は完了）で、手順書に位置づけを書けば毎回の再調査は不要になる。
(3) 変更はコードなし・文書のみ（手順書新設＋AGENTS.md §1へ導線1行）で、正式再利用検索（手順5）は
適用外（実装がないため。§4）。

## 1. 手順1：所在特定【実測】

| 部品・結合点 | 所在 | 状態 |
| --- | --- | --- |
| 実行入口 | `tools/session_logs/entry.py` 77-81行 | 第1引数`collect-eventual`で`eventual_preservation.run`へ委譲 |
| 本体と引数 | `tools/session_logs/eventual_preservation.py` 832-841行 | 必須4（`--source-root`・`--private-root`・`--repository-root`・`--tool-version`）・任意4（`--source-relative-path`・`--run-id`・`--observed-at`・`--config`） |
| 機微削除規則の接続 | 同 852-856行 | `--config`指定時のみ削除規則を読込。2026-08-16実行は未指定 |
| 解釈非対応の判定 | `tools/session_logs/source_kind.py`（`identify_auxiliary_kind`） | 先頭recordが`queue-operation`→`claude_queue`・`started`→`claude_agent`。本文形式（先頭に`uuid`・`sessionId`）以外は解釈対象外 |
| 成功前歴 | 2026-08-16セッション記録（repo外`~/.claude/projects/-Users-Daily-Development-ReviewCompass3/e8ff36d9-….jsonl`） | 3系統実行。Claude系統はpartial（成功475・失敗0・解釈非対応68。非対応でも生ログ保全は完了） |
| 実行後の記録の前歴 | `records/development/2026-08-10-all-reviewcompass3-codex-session-capture-receipt-v1.json` | 受領recordあり。2026-08-16実行分は未作成（揺れ） |
| 保全先配置の権威系譜 | `2026-08-04-…-storage-decision.json`→`2026-08-06-preservation-layout-v3-migration-decision-v1.md`→`2026-08-07-…-migration-evidence-v1.md`・`…-receipt-v1.json`（いずれも`records/development/`） | private-root＝repo外私有領域（Layout v3）の根拠 |
| 手順書の型 | `docs/development/prompts/todo-handoff-update.md` | 導線＋LLM/機械分担＋実行コマンド明記の型。prompts/配下は7本既設 |
| 導線の正本 | `AGENTS.md` §1「入口」（手順書5本接続済み）・`CLAUDE.md`（2本） | セッションログ記録の導線なし |
| 既存文書の記載 | `docs/development/2026-08-03-initial-development-checklist.md` 271-277行 | Evidence記述のみ（実行手順書ではない） |

## 2. 手順2：import元【実測】

変更対象コードなし（成果物は文書のみ）。手順書が参照する部品の依存は
`entry.py`→`eventual_preservation.py`→`source_kind.py`・`redaction`（`--config`指定時のみ）。
既存試験（`tests/test_session_log_eventual_preservation.py`ほかsession_logs系）は無変更。

## 3. 手順4：接続点【実測】

1. `AGENTS.md` §1「入口」——追記1行が本作業の導線変更点。既設5本（todo-handoff・
   pilot-collaboration・reviewer-launch・scope-prescan・request-builder）と同じ形式にする。
2. `CLAUDE.md`——現在2導線のみ。追加の要否は範囲固定文書の論点。
3. `docs/development/prompts/`——手順書の配置先。
4. G30操作登録——対象外。G30の言及はレビュー基盤側（`tests/test_request_builder.py`・
   `tests/test_reviewer_launch.py`）のみで、session_logs系コマンドはG30運用契約に登録されていない。
5. 既存契約の保護境界——活動中契約なし（契約013完了・レビュー基盤module休止中）。本作業は
   同moduleの再開ではなく、文書のみの別作業単位。
6. 範囲外の隣接機構——`hook`・`preserve`サブコマンド（自動記録の既設入口）と一件用安全保存
   （safe storage系）は本手順書の対象にしない（言及のみ）。

## 4. 手順5：正式再利用検索——適用外【記録】

開発方針（`docs/development/2026-08-02-development-policy.md`）123行の適用条件「新しい処理の追加
または既存処理の変更を予定する場合」に該当しない（新規コード0・既存コード変更0。成果物は手順書
1点と導線追記のみ）。scope-prescan-run.md手順5は「実装開始の根拠」であり、本作業単位に実装は
ない。この適用外判断は範囲固定文書でHuman確認を受ける。

## 5. digest表（範囲固定文書の固定入力）【実測】

```text
ddffc769cd683ffeed8b1474d9e599c9ce1283f1ed875d460b6b0953f019bc3e  tools/session_logs/entry.py
9a22242f64b3137849f3d39d25e2b450a7dce65938ed8e6f9f41379e329f3c18  tools/session_logs/eventual_preservation.py
1d59c0eec54a68eeee6cb8dfa93d4dee963a0e29662cf3e9ce5ee89648ae2cd7  tools/session_logs/source_kind.py
9c753dc67143e40bb7016e0ed62a5f56f4ad84ed0d61aa60b7ba1ca482941b4a  tests/test_session_log_eventual_preservation.py
b657e917ad02a7464f395c968419839820891a9fda92cb2f6166ac652ff251e6  AGENTS.md
46b1fb9f066c1b4baca4fcdd37874a71c8ac1ca515b2b8fbc6f3ca9edf2bca69  CLAUDE.md
4a8e3cab0a7a304864de09b38f683b31efb1479f8730ffb6fde25faf2bc5b463  docs/development/prompts/scope-prescan-run.md
e71565c795de3911f0ae95d929c0c6bd485f86ab67c380f2ea13d88eeefd70eb  docs/development/prompts/todo-handoff-update.md
e3e6b0d2c7a1265f7cde2c2e00cc888f43d63ce0d1945c300b2b2e5f7730b559  docs/development/2026-08-02-development-policy.md
79c9e7aa781d09cb4afe477919889e12583ae1d8e57b15317046cff5c1e74953  records/development/2026-08-04-session-transcript-eventual-preservation-storage-decision.json
b9aa5bc3bc2f6324e42032d3537e3b96f48a63e44c19f530dddafbcf0054843e  records/development/2026-08-06-preservation-layout-v3-migration-decision-v1.md
7e5f8b3701d9df8498d972f42a528552ee96d88eca92845f197ad86df812653f  records/development/2026-08-07-preservation-layout-v3-migration-evidence-v1.md
29a3af432c408e8f479a747706cc8ce406c9c7d123c95d02cbb4f02719235914  records/development/2026-08-07-preservation-layout-v3-migration-receipt-v1.json
01772320b3575c13d1244254c6adac848b8b7ea7c45cbdbbf65b1ee9a84fd767  records/development/2026-08-10-all-reviewcompass3-codex-session-capture-receipt-v1.json
ea482a3c7653b0966316012f43cc87ae426cdd5e429348a7f96c4e7f05ecd7b6  records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md
```

## 6. 範囲固定文書へ渡す論点【記録】

1. 手順書に載せる実行の形（2026-08-16成功前歴の転記）：共通値＝
   `--private-root /Users/keno/.reviewcompass3/projects/reviewcompass3/development/sensitive/eventual-preservation`・
   `--repository-root /Users/Daily/Development/ReviewCompass3`。系統別＝
   claude（`--source-root /Users/keno/.claude/projects`・`--tool-version reviewcompass3-historical-claude-capture-v1`）・
   codex現行（`/Users/keno/.codex/sessions`）・codex保管（`/Users/keno/.codex/archived_sessions`）
   （codex 2系統とも`reviewcompass3-historical-codex-capture-v1`）。
2. 解釈非対応（unsupported）の位置づけの明記：先頭recordが本文形式でないfile（待ち行列操作・
   下請けagent開始等）は解釈対象外だが、**生ログの保全は完了する**（保全を先に済ませる実装順）。
   既知状態であり、件数の急変時以外は再調査不要——という説明を手順書へ置く。
3. `--config`（機微削除規則）の要否：2026-08-16実行は未指定。保全先はrepo外私有領域であり、
   削除規則の適用要否はHuman裁定。
4. 実行後の記録の要否：受領record作成が2026-08-10あり・2026-08-16なしと揺れている。作るか、
   作るなら軽量な形をどうするか。
5. 成功判定の機械化：JSON出力の`status`・件数の読み方を手順書に固定（LLMは転記のみ。合否は
   単独実行の終了コードで確認——AGENTS.md §3）。
6. 導線：`AGENTS.md` §1へ1行（推奨）。`CLAUDE.md`への追加要否。
7. 手順書の型：`todo-handoff-update.md`準拠（番号手順・LLM/機械分担・実行コマンド明記）。

## 7. 未実施

- 範囲固定文書の起草、手順書本体の作成、導線追記。
