# 範囲固定：Codex起動のtoken消費を独立再計算できる形で記録する

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 状態：Humanのrisk確定・着手承認待ち

## 1. mode宣言と役割

```text
collaboration_mode: role_neutral_pilot_review
pilot: claude
reviewer: codex
closer: codex
work_item: Codex起動のtoken受領証（rollout由来の機械可読集計）
```

## 2. Human指示と本単位の位置づけ

- Human指示（2026-08-10）：「提案1について実施。ただし、token記録方式の範囲固定を作れ。
  rolloutファイルからは数値と照合値だけを写し、会話内容は写すな」
- 動機：試行計測record（`records/development/2026-08-09-role-neutral-mode-trial-metrics-v1.md`）
  §4.2が、token消費をCLI画面の転記に頼っており
  「repository内に独立再計算できるreceiptが無いため`reported_unverified`として扱う」と
  記している。本単位はこの未決事項を閉じる。
- 本単位は守り役後追い修正（group C・D）とは**別の作業単位**であり、
  group Cの完了後に着手する（作業単位の同時進行はしない）。

## 3. risk提案

- 提案：`medium`
- 根拠：対象は**記録生成**であり、他成果物の合否を決める守り役codeではない
  （`work-review-protocol.md` §3の既定`high`には当たらない）。一方で、
  repository外（利用者home）のfileを読むため、**機微情報の取り扱い境界**を持つ。
  Humanのrisk確定を要する。

## 4. 固定入力

| role | path | SHA-256 |
| --- | --- | --- |
| 受け渡し方式（未決事項の出典） | `docs/development/pilot-driven-record-handoff.md` | `93c84dd6ddd86af12175a4e844334ec9d62633f9be5ba9e97bcfbe3a435e92f0` |
| 試行計測record（§4.2の未決事項） | `records/development/2026-08-09-role-neutral-mode-trial-metrics-v1.md` | `f3fd74caa9c7e960e138c3c0e34f581ec67b62d0ca3c1da1d915c2cfc2f72652` |
| 既存解析器（再利用対象） | `tools/session_logs/parse_codex_rollout.py` | `41d22bc863736e5d584e1d6c14d3adf8b3343210b3bad762dae54ad5048b6ebc` |
| 同test | `tests/test_session_log_parse_codex_rollout.py` | `0d28bb76b38cdd4b38ece64a98fd3abe53914b32d0fea2734df1e3ee10c92a49` |
| 共通レビュー基準 | `docs/development/work-review-protocol.md` | `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772` |

- base commit：group C完了時のHEAD（着手時に確定して本文書へ追記する）

## 5. 実測にもとづく前提（調査済み）

`codex exec`は起動ごとにrollout JSONL（`~/.codex/sessions/<年>/<月>/<日>/rollout-<日時>-<UUID>.jsonl`）を残す。
2026-08-10の実file 1件を読み、次を機械確認した。

- 1行目は`type: "session_meta"`で、`payload.id`（起動の識別子）と`payload.cwd`を持つ。
- `payload.type == "token_count"`のeventが複数あり、`info.total_token_usage`に
  `input_tokens`・`cached_input_tokens`・`cache_write_input_tokens`・`output_tokens`・
  `reasoning_output_tokens`・`total_tokens`の6値が入る（`last_token_usage`も同形）。
- 実測例：`total_tokens` 75,482（`input` 73,635／`output` 1,847／`reasoning_output` 560）。

既存の`parse_codex_rollout.py`はmessageとtool呼出しを解析するが、
**token欄は扱っていない**。

## 6. 今回の作業

### 6.1 抽出（既存解析器の拡張）

`tools/session_logs/parse_codex_rollout.py`へ、rollout JSONLから
**session識別子と最終の`total_token_usage` 6値だけ**を取り出す関数を追加する。
新しい解析器は作らない（写しの禁止）。

### 6.2 受領証の生成（新規tool）

`tools/development/invocation_token_receipt.py`（新規）が、指定されたrollout fileから
次の内容だけを持つJSON受領証を`records/development/`へ**new-only**で作る。

| field | 内容 |
| --- | --- |
| `receipt_kind` | 固定文字列 |
| `session_id` | `session_meta.payload.id` |
| `rollout_path` | 絶対path（利用者homeを含むため、**環境role名へ置換して記録する**。§7参照） |
| `rollout_sha256` | rollout fileのbytes SHA-256（再計算の照合子） |
| `rollout_bytes` | file size |
| `token_usage` | `total_token_usage`の6値（整数のみ） |
| `model` / `reasoning_effort` | 起動時の実効値（呼出し側が渡す。判定recordの来歴行と同じ値） |
| `related_records` | この起動が作った判定record path（呼出し側が渡す） |

### 6.3 機微情報の境界（Human指示の実装）

**rollout fileから受領証へ写してよいのは、§6.2の表の値だけ**とする。

- 会話文・prompt・tool引数・tool出力・file内容・commit message等は**一切写さない**。
- `rollout_path`の実pathは利用者homeを含むため、既存の環境role置換
  （`tools/session_logs/redaction.py`の`home_directory`等）を適用した形で記録する。
- 受領証の生成時に、出力JSONを機械検査し、**整数・固定語彙・path・64桁hex以外の
  自由文が含まれていないこと**をfail-closedで確認する（違反時は書かずに停止）。

### 6.4 取得不能時の扱い

rollout fileが見つからない、`session_meta`が無い、`token_count`が1件も無い、
SHA-256が一致しない場合は、**数値を書かずに`unavailable`と理由codeだけを記録する**。
CLI画面からの転記値で埋めない。

## 7. 受入条件

1. 実rollout file 1件（一時複製）から、`session_id`と6値を取り出せる。
2. 生成された受領証に、§6.2の表以外のkeyが無い。会話文・prompt・tool出力が
   含まれていないことを機械検査で確認できる。
3. `rollout_path`に利用者homeの実文字列が現れない（環境role置換の適用）。
4. rollout fileが欠落・改竄（SHA不一致）の場合、数値を書かずに停止する。
5. 既存の`parse_codex_rollout.py`の契約を弱めない（既存test合格）。
6. 公式全Test合格・status `passed`。
7. **実rollout原本を変更・移動・削除しない**（読み取りのみ）。

## 8. 変更可能path

実装：`tools/session_logs/parse_codex_rollout.py`（token抽出の追加）、
`tools/development/invocation_token_receipt.py`（新規）

Test：`tests/test_session_log_parse_codex_rollout.py`、
`tests/test_invocation_token_receipt.py`（新規）

記録（新規）：
- `records/development/2026-08-10-invocation-token-receipt-evidence-v1.md`
- `records/development/2026-08-10-invocation-token-receipt-test-receipt-v1.json`
- `records/session-handoffs/2026-08-10-claude-pilot-invocation-token-receipt-review-request-v1.md`

これ以外（config・schema・上流設計・既存record・TODO・他tool）は変更しない。
**`docs/development/pilot-driven-record-handoff.md`の記録手順への反映は、
本tool `verified`後の別単位**とする（未決事項の解消を先に実証する）。

## 9. commit境界

1. **SCOPE**（本commit）：本文書のみ。Humanのrisk確定・着手承認待ちで停止。
2. **RED**：§8のtest 2 fileのみ。
3. **GREEN**：§8の実装2 file、Evidence、receipt。
4. **review request**：依頼書のみ（ignore検査exit `1`確認のうえ）。

反証・testは、**実rollout原本を複製した一時fileだけ**を対象にする。
`~/.codex/`配下へは書き込まない。

## 10. 停止条件（該当時はHumanへ）

1. base・worktree・固定入力Digestの不一致。
2. §8以外のpath変更が必要になった場合。
3. §6.3の境界を保ったままでは受領証が成立しないと判明した場合。
4. rollout形式がCodex CLIの版差で異なり、固定できないと判明した場合。
5. 受領証に機微情報が入り得ると判明した場合（設計をHumanへ諮る）。

## 11. Humanへの確認事項

1. risk `medium`の確定と着手承認。
2. §6.3の境界（数値・識別子・照合値・path置換形だけを写す）の承認。
3. 着手時期——group C完了後（提案）でよいか。

## 付記：サブエージェント実行の可否についての所見

Humanの問い「サブエージェントで実行させるか」への回答。

- **推奨しない**（本単位の実装・記録作成について）。理由は、
  (a) `role_neutral_pilot_review`は`pilot`・`reviewer`・`closer`の3役だけを定義しており、
  第4のagentを置く規定が無い。無断で増やすと**commitとrecordの帰属**が曖昧になる。
  (b) 本方式の中核は「committed recordだけが内容の正本」であり、
  agentが増えるほど「誰の主張か」の追跡が難しくなる。
  (c) 本単位の規模は小さく（実装2 file）、分割の利得が薄い。
- **限定的に有用な使い方**：repository外の調査（rollout形式の版差調査など）を
  読み取り専用で行わせ、**結論だけをPilotが自分の記録として書く**用途。
  この場合もsubagentの出力は正本にせず、Pilotが機械確認した事実だけを記録する。
- 第4のagentを恒常的な役として置くなら、それ自体が方式変更であり、
  `role_neutral_pilot_review`の改定とCodexの独立レビューを要する。
