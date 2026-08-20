# codex-cli第3 backend（登録簿深化同時実施）事前走査 v1

- 記録日：2026-08-20
- 指示者：利用者（Human）。指示文言：「codex-cli第3系統の縦切りに着手してください。まず疎通の実測確認、
  次に事前走査（6手順）まで進めて、契約候補の範囲案を見せてください」（2026-08-20 chat）
- 記録者：Claude
- 種別：契約候補定義前の事前走査（6手順。`docs/development/prompts/scope-prescan-run.md`）＋
  疎通の実測確認（§7）。契約定義・実装・既存文書の改定は含まない
- 範囲の基準：休止record §3-2（codex-cli第3 backend＝疎通回復が合図）、改善候補仕分けrecord
  2026-08-17（`IC-BACKEND-REGISTRY-DEEPENING-001`＝採用・本縦切りと同時実施、
  `IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`＝同時機に再評価）、契約012 §5.2（codex-cli backendは
  範囲外＝追加縦切りと明記）
- 基準commit：`4d699c334bdb0cab583e46f25cdd3c47f3310401`（検索計画の先行commit。事前走査の生成物は
  本recordを含むcommitで固定）
- 実測の正本：測定ブロック
  `records/development/2026-08-20-codex-cli-backend-prescan-measurements-v1.md`（宣言
  `records/development/2026-08-20-codex-cli-backend-prescan-commands-v1.json`）。本文の数値は
  同fileへの参照で示し、転記しない（例外は§7の疎通1回のみ）

## 0. 一枚要約（人向け）

疎通は回復している（§7実測：最小実行が終了コード0で完走）。第3縦切り＝「backend登録簿の深化
（採用済み改善候補）を同時に行い、`codex-cli`（provider openai・Tier 1）を追加する」。主要な発見は4つ。

1. 【実測】現行の登録簿は4項目だけで、name分岐が起動核に6箇所残る（§1）。codexを分岐追加で足すと
   3分岐目が並ぶ構造悪化になるため、**登録簿へ関数・一覧を吊るす一般化（契約012 §5.1-1が記述した
   水準の完成）が本縦切りの本体**である。
2. 【実測】codex execは`--output-schema`（判定schemaの直接指定）と`--json`（JSONL stream）を持ち、
   **agyに近い型**で組める見込み。claude-subagentで必要だったprompt指示＋本文抽出のfallbackが
   不要になる可能性がある（RED段の実測で確定）。
3. 【実測】この端末は`/etc/codex/requirements.toml`が承認方式を`OnRequest`（都度承認）に固定している。
   疎通の最小実行は承認要求なしで完走したが、**読取り道具を使う実レビューがheadlessで完走するかは
   RED段のE2Eで確定**が必要（危険旗`--dangerously-*`・`--approve-for-me`の不在両向き試験も必要）。
4. 【実測】codexのprovider（openai）はpilot provider（anthropic）と異なるため、既存の機械判定で
   **Tier 1**になる。tier受容機構（契約012）の変更は不要。正式再利用検索は`start_allowed: true`（§5）。

## 1. 手順1：所在特定【実測】

行番号・一致行の正本は測定ブロック「起動核のname分岐とbackend別定数の所在」節。

| 部品・結合点 | 所在 | 状態 |
| --- | --- | --- |
| backend登録簿（深化対象） | `tools/reviewer_launch/core.py`の`BACKENDS` | provider・executable・declared_tier・read_tool_nameの4項目のみ |
| name分岐（消す対象） | 同`launch_review`内5箇所＋`resolve_project_binding`呼出し分岐（測定ブロック参照：環境・許可model選択／agy専用一覧／project束縛／引数組み立て／model観測／判定抽出） | 観測record `OBS-RC3-BACKEND-REGISTRY-SHALLOW-2026-08-17-V1`の指摘どおり。登録形へ吊るす一般化が必要 |
| 引数組み立ての前例 | 同`build_arguments`（agy）・`build_claude_arguments`（claude） | codex用は`exec` subcommand形＝第3の組み立て関数を登録簿へ |
| stream解析の前例 | 同`_parse_stream`（共通JSONL）＋agy系`_observed_models`／`_extract_verdict`＋claude系`_claude_observed_models`／`_claude_extract_verdict` | codex系の観測・抽出関数を登録簿へ |
| codex起動の前例 | `docs/development/pilot-driven-record-handoff.md`（`codex exec --sandbox read-only`の運用実績）＋§7の疎通実測 | 起動形の直接前例あり |
| codex JSONL形式の前例 | `tools/session_logs/parse_codex.py`＋fixture `tests/fixtures/session_logs/codex-exec-public-shape.jsonl` | **lifecycle: provisional・non-normative**（file冒頭宣言）。importせず形式知識の参照に留める。fixtureはRED段の合成stream素材に流用可 |
| codex CLIの現況 | `codex-cli 0.147.0`（測定ブロック「codex CLIの版」） | 旗はhelp実測：`--json`・`--output-schema <FILE>`・`-m`・`-s read-only`・`-C`・`--skip-git-repo-check`・`--ephemeral`・`--ignore-user-config`・`-o`。危険旗`--dangerously-bypass-approvals-and-sandbox`・`--dangerously-bypass-hook-trust`・`--approve-for-me`が存在【実測・help表示のみ】 |
| 承認方式の端末要件 | `/etc/codex/requirements.toml`（§7の警告行で観測） | `approval_policy`は`OnRequest`のみ許可。headless完走性はRED段E2Eの確定事項 |
| 組み立て器のmodel照合 | `tools/request_builder/core.py`（測定ブロック「組み立て器のmodel照合箇所」：import・空検査・既定記載・照合の4箇所） | 和集合基準（契約012 §5.1-4の設計どおり）。再評価対象（§8-5） |

## 2. 手順2：import元【実測】

全一致行の正本は測定ブロック「reviewer_launchのimport元」節。

- import元は6 file：`tools/operations/operation_contract_run.py`（g30登録）・
  `tools/evaluation/rq2_paired_trial.py`（**契約012時点の4 fileから増加。RQ2実験装置がentryを使用**）・
  `tools/request_builder/core.py`・`tools/reviewer_launch/`内部・`tests/test_reviewer_launch.py`・
  `tests/test_request_builder.py`。
- 互換必須の公開記号（受入済み製品が使用）：`core.ALLOWED_RESPONSE_MODELS`（和集合tuple。
  request_builderの空検査・既定記載（先頭要素＝agy値）・照合の3用途＋試験2箇所）・
  `record.verdict_record_relative_path`。`record.py`は`core.BACKENDS`もimportする。
- 波及の見立て【推測・契約で確定】：深化はcore内部の構造変更であり、`entry.launch`の入口形と公開記号の
  名称・意味を変えなければ、RQ2装置・g30・組み立て器は無変更で保てる。

## 3. 手順3：Digest固定の全文検索【実測】

- 主題語（codex・codex-cli・openai・gpt-・BACKENDS）の一致file数は測定ブロック
  「主題語の一致file数（tracked全体）」節を正とする。意味の読み：`codex`の一致はsession-log系の
  既存資産（保全・解析・fixture）に厚く、**code層の一致（同「code層のcodex一致file一覧」節）に
  `tools/reviewer_launch/`は含まれない**。よってcodex文字列の新規導入は縦B内に局所化できる。
- 自己言及の明記（規律6）：本record・検索計画・証明書・測定ブロック自身が主題語を含み、以後の
  同種検索に現れる。

## 4. 手順4：接続点【実測】

1. **拡張契約の形**：受入済み縦B製品（契約010→012）の第3拡張縦切り。前例と同じく「現行値の
   不変移設＋既存試験の無変更全緑」を機械証明の柱にする。
2. **登録簿深化**：backend定義へ「引数組み立て関数・stream解析（model観測・判定抽出）関数・
   許可model一覧・禁止環境変数一覧・通過変数一覧・子環境注入・project束縛要否」を吊るし、
   name分岐6箇所を登録参照へ置換する。`IC-BACKEND-REGISTRY-DEEPENING-001`のconsumer＝本契約
   （受入でOutcomeへ接続し、候補をclosedへ）。
3. **codex-cli追加**：provider `openai`・executable `codex`・宣言Tier 1（機械判定`_resolve_tier`が
   provider相違で1を返す既存経路。受容入力・受容根拠は不要）。
4. **起動固定形の候補**（RED段実測で確定）：`exec` subcommand・`--json`・`--output-schema`（判定
   schemaの直接指定を第一候補、不成立ならprompt指示＋抽出のfallback＝claude型）・`--sandbox read-only`・
   `--skip-git-repo-check`・`--ephemeral`・`--ignore-user-config`（利用者config・hooksの影響排除。
   認証はCODEX_HOMEのログイン状態を使用）・作業dir＝対象repository・**stdin遮断**（§7でexecがstdinを
   読む挙動を観測。subprocess側でstdinを閉じて渡す）。
5. **認証遮断・環境**：openai系API鍵環境変数（`OPENAI_API_KEY`等）の禁止一覧を契約の直書き定数で
   新設し、`_child_environment`の型（起動前検査＋最小通過）を流用する。
6. **許可model**：空の直書き定数で開始し（空の間は`allowed_models_unfixed`停止）、実E2E前に利用者
   承認recordで確定（契約010・012と同型）。§7実測の既定model表示は承認の参考値。
7. **g30 prepare**：`--backend`任意引数は既に一般化済み（`entry.py`）。codexの読取り道具名
   （prompt雛形への差し込み値）だけが契約論点（codexはshell系読取りで、道具名がagy/claudeと型が違う）。
8. **組み立て器**：和集合`ALLOWED_RESPONSE_MODELS`へのcodex許可model追加（末尾追加なら既定記載＝
   先頭要素は不変。試験で固定）。`IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`の再評価は§8-5。
9. **回帰**：reviewer_launch・request_builderの既存試験の無変更全緑（収集件数は測定ブロック末尾
   2節）。正規全試験は契約の受入条件で扱う。

## 5. 手順5：正式再利用検索【実測】

- 作業別計画（schema 2・能力5件：codex起動・codex stream解析・登録簿深化・openai認証遮断・
  model対応検査）：`records/development/2026-08-20-codex-cli-backend-reuse-search-plan-v1.json`
  （先行commit `4d699c3`。SHA-256は§6のdigest表＝測定ブロックを正とする）
- 一操作入口の結果：`status: completed`・HEAD `4d699c33…`・**`start_allowed: true`**。一致件数・
  内訳の正本は証明書record
  `records/development/2026-08-20-codex-cli-backend-reuse-search-attestation-v1.json`
  （SHA-256は§6のdigest表）。lifecycle・再利用方法の裁定はHumanに残る（契約候補で扱う。特に
  `parse_codex.py`はprovisional＝参照のみ、importしない方針を§8-6で提示）。

## 6. digest表（契約候補v1の固定入力）【実測】

測定ブロック「契約候補が参照するfileのdigest固定」節（16 file）を正とし、本文へ複製しない。

## 7. 疎通の実測確認【実測・例外転記】

測定ブロックに載せない例外：外部送信・課金を伴う1回実行のため、二重実行guard付きの測定ブロックに
含めず、規律2（再現コマンド併記・全出力転記）で固定する。

- 再現コマンド（作業dirはrepo外の一時領域・repo内容を含まない最小固定文）：

```text
codex exec -C /private/tmp/claude-501/-Users-Daily-Development-ReviewCompass3/06d87532-ebc0-4c3c-944a-dca76440737a/scratchpad --sandbox read-only --skip-git-repo-check "Reply with exactly: OK"
```

- 終了コード：0（実行harnessの成功報告。非0時はerror表示になる）
- stdout（全出力）：

```text
Reading additional input from stdin...
OpenAI Codex v0.147.0
--------
workdir: /private/tmp/claude-501/-Users-Daily-Development-ReviewCompass3/06d87532-ebc0-4c3c-944a-dca76440737a/scratchpad
model: gpt-5.6-sol
provider: openai
approval: on-request
sandbox: read-only
reasoning effort: high
reasoning summaries: none
session id: 01a01e4b-d20d-7763-8a68-b3e6f01f37c2
--------
user
Reply with exactly: OK
warning: Configured value for `approval_policy` is disallowed by requirements; falling back to required value OnRequest. Details: invalid value for `approval_policy`: `Never` is not in the allowed set [OnRequest] (set by /etc/codex/requirements.toml)
hook: UserPromptSubmit
hook: UserPromptSubmit Completed
codex
OK
hook: Stop
hook: Stop
hook: Stop Completed
hook: Stop Completed
tokens used
7,008
OK
```

- 読み：トークン枯渇は解消（応答が返り完走）。既定model表示は`gpt-5.6-sol`・承認方式は端末要件で
  `OnRequest`固定・利用者configのhooksが動く（→`--ignore-user-config`の採用候補理由）・execは
  stdinを読みにいく（→stdin遮断の固定事項化）。

## 8. 契約候補v1へ渡す論点（発見事項と推奨）

1. 【実測】構造化判定：codexは`--output-schema`を持つため、**schema直接指定（agy型）を第一候補**、
   不成立時はprompt指示＋抽出（claude型）をfallbackとし、どちらで固定するかはRED段の実測で確定する。
2. 【実測】headless完走性：承認方式が端末要件で`OnRequest`固定。read-only sandbox内の読取りが承認
   要求なしで完走することをE2Eで確定する（完走しない場合は停止条件）。危険旗3種の不在は両向き試験へ。
3. 【判断】許可model：空開始→利用者承認recordで確定（契約010・012と同型。参考値＝§7の既定model表示）。
4. 【実測】tier：provider相違により機械判定Tier 1。受容機構・引数は変更不要。
5. 【判断】`IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`の再評価：登録簿深化でbackend別一覧が参照可能に
   なるが、契約011成果物（request_builder）は契約012から続く保護対象。選択肢＝(a)本契約内で契約011の
   最小改定を併せて行う／(b)本契約後の独立小作業単位に切る／(c)保留継続。**推奨は(b)**（本契約の変更
   上限を縦Bに保ち、保護境界を跨がない。実害は限定的＝起動側照合が最終防衛、の実測が根拠）。
6. 【実測】`parse_codex.py`はprovisional・非正本のため**importせず**、event形式の知識とfixtureだけを
   RED段の合成stream試験に流用する（正規化・昇格はlifecycle棚卸し（deferred）の領分に残す）。
7. 【実測】登録簿深化の完成基準：name分岐6箇所が登録参照へ置き換わり、**agy・claude-subagentの
   既存試験が無変更で全緑**（現行値の不変移設の機械証明。契約012 §9-2と同型）。
8. 【記録】E2Eの型：実E2E 1回（利用者の明示指示。Tier 1のため受容手続きなし）。完了レビューは
   正式経路の既定（agy・Tier 1）で行う。

## 9. 未実施

- 契約候補v1（契約015相当）の作成、5段手続き、実装、codexの実レビューE2E（契約内の承認付き実測へ）。
- `IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`の再仕分け（§8-5の選択はHuman判断）。
- TODO・見取り図の反映（blocker欄のcodex記載は本記録によりstale。次のTODO更新で書き換え）。
