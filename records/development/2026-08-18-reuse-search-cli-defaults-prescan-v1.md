# 正式再利用検索CLIの引数廃止（既定値・自動解決）事前走査 v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。選択文言「1（引数の廃止）から着手してください。事前走査から。」
  （2026-08-18 chat。方針＝「手作業の余地がないように機械化するのが正しいアプローチ」）
- 記録者：Claude
- 動機：`--runtime-root`の手組み立て誤指定事故
  （`records/development/2026-08-18-placement-root-resolution-evidence-v1.md` §5）。規則で防ぐ
  のではなく引数自体を消す
- 基準commit：`8c9b29b`（作業tree clean）

## 1. 手順1〜2：所在・呼び出し元・波及【実測】

- 対象：`tools/development/formal_code_reuse_search.py`の`main()`（400〜427行）。現引数＝
  `--project-root`（既定`.`）・`--runtime-root`（**必須**）・`--profile`（既定`development`）・
  `--universe`（**必須**）・`--policy`（**必須**）・`--plan`（必須）・`--captured-at`（任意）。
- 呼び出し元：**コードからの呼び出しなし**（機械検索）。文書2件のみ——
  `docs/development/prompts/scope-prescan-run.md`（コマンド雛形＝本作業で縮小）と
  `docs/development/2026-08-02-development-policy.md` 123行（入口名のみで引数記載なし＝変更不要）。
- 既存試験：`tests/test_formal_code_reuse_search.py` 8本はすべて`execute_formal_search`の
  関数直呼びで**CLIに依存しない**。`captured_at`は関数のキーワード引数として試験が使用
  （`tests/test_layout_baseline.py`含む）——**CLI旗を消しても関数引数を残せば影響なし**。

## 2. 手順3：digest表【実測】

```text
5f9e8054cbd70bb5be3e21e9359b8cbd9f86ea4ddfa38dc41f0c0089ee665b6d  tools/development/formal_code_reuse_search.py
f417c6d524b5ba579082271a0030e8cb8e57420d63719d882ce4597fade46edb  tests/test_formal_code_reuse_search.py
```

## 3. 手順4：設計（作業票へ渡す論点）

1. `--runtime-root`：任意化し、既定＝`Path.home() / ".reviewcompass3-private" / "reuse-search"`
   （機械導出。本機では従来の正準値と同一。文字列の転記をどこにも残さない）。
2. `--universe`・`--policy`：任意化し、既定＝`<project-root>/.reviewcompass/policies/`から
   **数値最大版**を自動解決（`work4a-source-universe-v<N>.json`・
   `work4a-freshness-policy-v<N>.json`）。**辞書順は不可**（v9＞v10と誤る。freshnessは現に
   v11まで存在し、辞書順ならv9を選ぶ実害がある）。解決不能は既存の停止規約
   （`{"status": "stopped", "reason": …}`・終了コード1）で止める。
3. `--captured-at`：**旗ごと削除**（時刻は機械が記す。手書き時刻の注入口を消す）。関数引数
   `captured_at`は試験の決定性のため残す。
4. 解決処理は純関数helper（`default_runtime_root()`・`latest_policy_file()`）として切り、
   単体で試験固定する。
5. 手順書`scope-prescan-run.md`：コマンド雛形を`--plan`のみへ縮小し、正準値の転記指示
   （2026-08-18追記の一部）を「ツールが自動解決する」旨へ**置き換えて縮める**（規則を減らす）。

## 4. 手順5：正式再利用検索

作業別計画の先行commit後に実行し、証明書を
`records/development/2026-08-18-reuse-search-cli-defaults-attestation-v1.json`へ固定する
（本検索自体は変更前のCLIで実行する＝現行引数を明示する最後の実行）。

## 5. 未実施

- 手順5の実行、作業票の適用、RED、GREEN、手順書縮小、Evidence、TODO反映。
