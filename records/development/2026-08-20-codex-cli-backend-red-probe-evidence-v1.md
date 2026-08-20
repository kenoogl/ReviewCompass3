# 契約015 RED段実測（codex実挙動プローブ3回）Evidence v1

- 実施日：2026-08-20
- 担当：Claude
- 種別：契約015 v2 §7.2・§7.4がRED段実測へ留保した事項の確定と、契約が予定したfallback発動の記録
- 外部送信の根拠：採用判断record `DEC-CODEX-CLI-BACKEND-CONTRACT-ADOPTION-2026-08-20-V1`
  （「RED先行で実装へ進めてください」＝契約が予定するRED段実測を含む）。送信は3回・いずれも
  repo内容を含まないscratchpadの固定材料のみ
- 実測方法：scratchpad固定対象file（`probe-target.md`、SHA-256
  `d1f8dde6d98bf069c6e15915fb37130c83482cfa92a0c46d38c9fe3bd5ac1a3f`）に対し、(1) 契約固定引数
  どおり（`--output-schema`つき）、(2) fallback形（schema旗なし・prompt指示）、(3) 最小文言・
  `--ephemeral`なし（rollout生成確認）の3回を実行。rawは下記4 fileへ複写・抜粋（例外転記の代替
  として**未加工fileごと固定**する。測定ブロックに載せない理由：外部送信を伴い二重実行guardと
  両立しないため）

## 1. raw（本recordと同時commit）【実測】

```text
records/development/2026-08-20-codex-red-probe1-schema-raw.jsonl      （5 event行）
records/development/2026-08-20-codex-red-probe2-fallback-raw.jsonl    （9 event行）
records/development/2026-08-20-codex-red-probe3-rollout-raw.jsonl     （最小実行の公開stream）
records/development/2026-08-20-codex-red-probe3-rollout-excerpt.jsonl （rolloutのturn_context行の抜粋）
```

再現コマンドの形（probe2）：

```text
codex exec --json --sandbox read-only --skip-git-repo-check --ephemeral --ignore-user-config \
  -m gpt-5.6-sol "<固定prompt>" </dev/null
```

## 2. 確定事項【実測】

1. **`--output-schema`は既存schemaのままでは不成立**：openai側のstrict検査が
   `invalid_json_schema`（`findings.items`に`additionalProperties: false`が必須）で実行前拒否
   （probe1 raw 4行目。文字列理解の失敗類型(6)「server非対応schema語彙」の実例）。
   → **契約§7.2のfallback節を発動し、判定取得は「prompt指示＋出力からのJSON抽出（`_parse_json_text`
   設計流用）＋既存`validate_verdict`」で固定する**。`--output-schema`とschema一時fileは固定引数
   から除く。これは契約が事前に予定した分岐であり契約訂正を要しない（§7.2「どちらで固定したかを
   実装Evidenceへ記す」の履行が本record）。
2. **公開stream（`--json`）の正準位置**：thread識別＝`thread.started`の`thread_id`（1行目）。
   最終応答＝`item.completed`かつ`item.type == "agent_message"`の`item.text`（probe2 raw 8行目。
   JSON本文が裸で入る）。途中の道具実行は`item.started`／`item.completed`の
   `item.type == "command_execution"`として全commandが記録される（§7.5-6の領域外読取り点検は
   この記録で機械実施できる）。
3. **公開streamにmodelを載せるイベントは存在しない**：probe2全9行・probe3・2026-08-03固定の
   公開形fixture（`tests/fixtures/session_logs/codex-exec-public-shape.jsonl`＝model一致0件）の
   いずれにも無い。応答本文の自己申告model欄は「GPT-5」で実際（`gpt-5.6-sol`）と**不一致＝信頼
   不可**（probe2 raw 8行目）。→ §7.4「stream正準位置からのmodel観測」は公開streamでは成立
   しない。**対処は契約訂正のHuman判断へ**（本recordは実測の固定のみ。3案と推奨は同日の報告
   および訂正判断recordを参照）。
4. **rolloutにはmodelが機械記録される**：`--ephemeral`を外すと
   `$CODEX_HOME/sessions/YYYY/MM/DD/rollout-<時刻>-<thread_id>.jsonl`が生成され、
   `turn_context`の`payload.model`に`"gpt-5.6-sol"`、`session_meta`の`payload.model_provider`に
   `"openai"`が入る（probe3＋抜粋raw。pathはthread_idで一意に機械特定できる）。
5. **headless完走性**：read-only sandbox内で`cat`・`shasum`が承認要求なしで実行され完走
   （probe2終了コード0。承認方式OnRequest固定の端末でも読み取り実行は止まらない）。§7.5-2の
   懸念は縮小（repo対象での最終確定は§9-8実E2E）。
6. **`--ignore-user-config`**：認証（ログイン状態）は維持され完走。利用者hooksの発火なし
   （疎通実測2026-08-20＝事前走査§7ではhook行が出ていた）。意図どおり。
7. **stdin**：`/dev/null`遮断で正常進行（「Reading additional input from stdin...」は情報表示で、
   EOFで即続行）。契約§7.2のstdin遮断（全backend共通）で確定。

## 3. 未実施

- §7.4 model観測の契約訂正の裁定（Human）。RED試験の固定・最小実装・実E2E（明示指示待ち）。
