# 測定ブロックの機械生成tool 事前走査 v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。選択文言「単位2（測定ブロックの機械生成）に着手してください。
  事前走査から」（2026-08-18 chat。方針＝手作業の構造的排除の本丸）
- 記録者：Claude
- 目的：事前走査recordの【実測】節で行っているLLMの出力転記（数値誤りの発生源）を廃し、
  宣言したコマンド列を機械が実行して「コマンド＋全出力＋時刻」を機械生成fileへ固定する
- 基準commit：`82089b4`（作業tree clean）
- 必読入力の適用：本件は**コマンド出力の機械取り込みとrecord生成を含む部品**であり、文字列理解の
  失敗類型原則（`records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md`）
  の**適用対象**。取り込み＝fail-closed（生成不能時は部分fileを残さない）・出力は無加工転写・
  規模上限（超過は明示printされた切り詰め印）・**敵対fixture＝出力がfence（```）を含む場合**を
  試験に標準で含める（fence構造解析の再発類型への対策：外側fenceを内容の最長backtick連より
  長くする）

## 1. 手順1〜2：類似部品と流用元【機械検索の実測】

- 「measurement」「capture」を名に持つ汎用の測定ブロック生成部品は**存在しない**（機械検索。
  `capture_committed_observation`はGit観測専用で責務が異なる）。新設が妥当。
- 流用元：subprocess実行と要約JSONの型＝`tools/session_logs/record_run.py`
  （SHA-256 `89c45318488cfcba9583f3626c3104803ea5b07d1f9a4284541cd350ff18e1c3`）。
  new-only書込み（既存fileへ上書きしない）の前例＝`O_EXCL`型6件（`tools/egress/approval.py`等・
  機械検索）。宣言fileのdigest埋め込み＝`tools.common.digests.file_sha256`を再利用。
- 呼び出し元となる手順書：`docs/development/prompts/scope-prescan-run.md`（本tool完成後、
  【実測】節の作り方を「測定ブロック生成物への参照」へ改定する——本作業単位内で実施）。

## 2. 手順3：digest表【実測】

```text
89c45318488cfcba9583f3626c3104803ea5b07d1f9a4284541cd350ff18e1c3  tools/session_logs/record_run.py
f9faab7074e0320d385937f27b52f9d387a6041e008a1723c62c0ac781af0077  tools/development/formal_code_reuse_search.py
```

## 3. 手順4：設計（作業票へ渡す論点）

1. 新設：`tools/development/measurement_block.py`。入力＝宣言JSON
   （`{"title": …, "entries": [{"label": …, "argv": […]}]}`）。shellを使わず`argv`配列で実行
   （文字列連結の注入余地を作らない）。
2. 出力＝**1つの機械生成markdown**（new-only。既存pathへは書かず停止）。各entryに
   label・argv・終了コード・所要秒・stdout／stderrの**無加工全文**を載せ、冒頭に
   captured_at・宣言fileのpathとSHA-256（機械計算）・「機械生成・手編集禁止」を明記。
3. fence対策：各出力の外側fenceは**内容中の最長backtick連＋1**（最低3）で囲む。
4. 規模上限：1 streamあたり100,000 byte。超過は切り詰め、**明示の印と切り詰めbyte数**を機械が
   記す（黙って欠けない）。
5. 終了コード：0＝全entry実行済み（コマンド自体の非0終了は**データとして記録**し、summaryの
   `failed_count`へ計上）／1＝実行不能entryあり（spawn失敗・timeout＝測定不完全）／2＝入力不備・
   出力path既存。stdoutへ一行JSON summary（status・output_path・entry_count・failed_count）。
6. 使い方（以後の事前走査）：LLMは宣言JSONを書く（意味の選定）→機械が実行・固定→recordは
   生成物のpathを参照し**意味の説明だけ**を書く。数値の転記という行為が消える。

## 4. 手順5：正式再利用検索

作業別計画の先行commit後、`--plan`のみで実行（前作業単位で引数廃止済み）。証明書は
`records/development/2026-08-18-measurement-block-attestation-v1.json`へ固定する。

## 5. 未実施

- 手順5の実行、作業票の適用、RED、GREEN、手順書改定、Evidence、TODO反映。
