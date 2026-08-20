# codex-cli第3 backend（登録簿深化同時実施） 作業契約候補 v1

- 契約ID：`TC-RC3-PRODUCT-CODEX-CLI-BACKEND-015`
- 契約版：1
- 契約種別：受入済み縦B製品（契約010→012）の第3拡張縦切り。採用済み改善候補
  `IC-BACKEND-REGISTRY-DEEPENING-001`（backend登録簿の深化）を同時に消化する
- 状態：`candidate_pending_independent_review`
- 作成日：2026-08-20
- 直前の製品契約：契約014（セッションログ前置record解釈）v3（受入完了）
- 入力：休止record §3-2（疎通回復が合図＝事前走査§7で実測済み）、改善候補仕分けrecord 2026-08-17
  （「codex-cli疎通回復時は、第3 backend追加の縦切りに候補1を含め、候補2を再評価する」）、
  codex-cli第3 backend事前走査v1（6手順）、正式再利用検索（計画・証明書・`start_allowed: true`）、
  許可model承認record v1、利用者指示「codex-cli第3系統の縦切りに着手してください。まず疎通の実測確認、
  次に事前走査（6手順）まで進めて、契約候補の範囲案を見せてください」「範囲案どおり契約候補v1を
  作成してください。保留候補の再評価は(b)別作業単位のままにします。codexの許可モデルは
  gpt-5.6-sol, gpt-5.6-terra」（いずれも2026-08-20 chat）
- 実装状態：未開始
- 危険度：高
- 危険の理由：headless起動（実質の外部送信・課金）の対象を第3の会社（openai）へ広げ、対象repository
  内容がopenaiのレビュー役から読まれる。加えて、受入済み縦B起動核の内部構造（backend登録簿）を
  全backend分作り替えるため、誤実装は既存2経路の回帰に直結する

## 1. 位置と縮小境界

【記録】縦Bは現在2 backend体制（agy＝Tier 1既定・claude-subagent＝Tier 3明示受容）。codex-cli backendは
契約012 §5.2が「疎通回復後の追加縦切り」として範囲外に明記した残件であり、休止record §3-2の合図
（トークン枯渇の疎通回復）は2026-08-20の実測（事前走査v1 §7・最小実行が終了コード0で完走）で満たされた。
現行のbackend登録簿は4項目のみで、環境変数・許可model・引数組み立て・stream解析・判定抽出の選択が
name分岐6箇所に残る（観測record `OBS-RC3-BACKEND-REGISTRY-SHALLOW-2026-08-17-V1`＝e2e-012-001判定F-6。
この構造は実際にF-1の取り違えを誘発した）。

【判断】本契約は第3縦切りとして、次だけを行う。

- **backend登録簿の深化**：backend定義へ「引数組み立て関数・stream解析（model観測・判定抽出）関数・
  許可model一覧・禁止環境変数一覧・通過変数一覧・子環境注入・project束縛要否・読取り指示差し込み」を
  吊るし、name分岐6箇所を登録参照へ置換する。agy・claude-subagentの現行値は**不変のまま移設**する。
- **`codex-cli` backendの追加**：provider `openai`・executable `codex`・宣言Tier 1（既存の機械判定
  ＝provider相違と一致。受容入力・受容根拠は不要）。
- **openai系の認証遮断**（§7.3）と**許可model 2値の固定**（承認record確定済み。空開始を省略）。
- RED先行の対象試験と、利用者指示による実E2E 1回（§9-8）。
- 判定schema・転記・事後照合・保存・G30登録・導線は既存のまま流用する（新設しない）。

## 2. Human承認境界

- 起動の起点は利用者のchatによるレビュー実施指示（契約010 §2の踏襲。起動ごとの追加承認手続きなし）。
  codex-cliはTier 1のため、契約012の明示受容手続きは適用されない（機械判定の既存経路）。
- 契約内の初回実起動（§9-8実E2E）は利用者の明示指示を得てから行う。
- 機械層の守り：読み取り専用（read-only sandbox・書込み許可を渡さない）・固定引数・commit済み
  依頼recordだけ・byte上限・自動再試行なし・別model／別認証／別経路への自動切替なし（契約010の型）。

## 3. 権威、証拠

| 役割 | path | SHA-256 |
| --- | --- | --- |
| 事前走査v1（6手順・接続点・論点） | `records/development/2026-08-20-codex-cli-backend-prescan-v1.md` | `601dde12cc154911f93fd1b4ce78bd06cfcc4f84ad869df8f2b00f2a4dc048a2` |
| 実測の正本（測定ブロック10項目） | `records/development/2026-08-20-codex-cli-backend-prescan-measurements-v1.md` | `da1a13b5bfd255073b65557fd6b8382d73644125c941aa32715c9dc527894af3` |
| 正式再利用検索の作業別計画 | `records/development/2026-08-20-codex-cli-backend-reuse-search-plan-v1.json` | `005c86b3c095041ea0ca42690c617e709394023951adb4e54d4ef5aa43efcd2b` |
| **正式再利用検索の証明書（start_allowed: true）** | `records/development/2026-08-20-codex-cli-backend-reuse-search-attestation-v1.json` | `dc0eaa5a963a586e8d381d6f16dbf7546ab27d7ad24038e8aa5f3bcae8c99bb0` |
| 許可model承認record（2値・(b)裁定） | `records/development/2026-08-20-codex-allowed-models-approval-v1.md` | `f0f0536ccda07d942e06c1d96fa75c2781387763f63afd0439a5d9c9f7d67c99` |
| 拡張対象の契約012候補v2（受入済み） | `records/task-contract/2026-08-17-claude-subagent-backend-candidate-v2.md` | `f95446a96b132c9dda5e225460cc4ab0214e535ebbc7ef9b79fdc953d936994d` |
| 契約012の製品受入判断 | `records/development/2026-08-17-claude-subagent-backend-product-acceptance-decision-v1.md` | `dad40e6c88a5c46dd4008806ab0e94c797d4c5f55aefd4f0d3d08891d343afb8` |
| 休止record（§3-2＝本縦切りの合図） | `records/development/2026-08-17-review-tooling-module-pause-decision-v1.md` | `9b4d184f378d5dc8dad203caba5daf6b6e58b2471dd387187d5c5ede971cfd6c` |
| 改善候補仕分けrecord（候補1同時実施・候補2再評価） | `records/development/2026-08-17-improvement-candidates-triage-decision-v1.md` | `34f7ca163645fe50770734f92b48ad41b6415983ab1eda61c57efc104be8a162` |
| 登録簿深化の観測record（IC出所） | `records/development/2026-08-17-backend-registry-shallow-generalization-observation-v1.json` | `b09c397744e81db5936cef14f29aa9e15ceb41e0bbcfb60c815a57873639893a` |
| model照合範囲の観測record（範囲外裁定の対象） | `records/development/2026-08-17-request-builder-union-model-check-observation-v1.json` | `ea3cdc0d048d9604272c7c918287856e8ec3a6013856b5cde66410b262432517` |
| 文字列理解の失敗類型（必読・起草時照合済み） | `records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md` | `ea482a3c7653b0966316012f43cc87ae426cdd5e429348a7f96c4e7f05ecd7b6` |

流用部品のcode・文書のdigestは事前走査の測定ブロック「契約候補が参照するfileのdigest固定」節
（16 file）を正とする（固定commit時点の差分0を§9-9で確認する）。

## 4. 実装方法の3案

| 案 | 内容 | 判断 |
| --- | --- | --- |
| A 最小（既存機能のみ） | codexレビューを従来の人手起動（pilot-driven-record-handoff方式）で運用する。または現行のname分岐へcodex分岐を追記するだけの浅い追加 | 前者は機械統制（raw先行保存・model照合・転記照合）が手作業へ戻る。後者は観測record F-6の構造悪化を3系統へ拡大し、同型の取り違え再発余地を広げる。不採用 |
| B 登録簿深化＋codex追加 | backend定義へ関数・一覧を吊るす一般化を先に行い、codex-cliを登録定義の追加として載せる。互換記号は和集合として維持 | 変更が縦B内に局所化し、agy・claude経路は値の移設だけで無変更（byte不変golden＋既存試験で機械証明）。正式検索の直接一致（起動・解析・遮断の前例）をそのまま流用。仕分けrecordの裁定（候補1同時実施）とも一致。推奨 |
| C codex専用アダプタの新設 | 実行器設計を流用したcodex専用アダプタを縦Bと並置する | 保存・転記・照合・導線が複製になり、登録簿の設計意図に反する。不採用 |

## 5. 範囲

### 5.1 範囲内

1. **backend登録簿の深化**：backend定義を「provider・executable・宣言tier・読取り指示差し込み・
   引数組み立て関数・stream解析（model観測・判定抽出）関数・許可model一覧・禁止環境変数一覧・
   通過変数一覧・子環境注入・project束縛要否」へ一般化し、`launch_review`等のname分岐6箇所
   （事前走査§1の測定固定点）を登録参照へ置換する。agy・claude-subagentの現行値は不変のまま
   移設し、**生成promptと組み立て引数のbyte不変をgolden試験で機械証明**する。
2. **codex-cli backendの追加**：provider `openai`・executable `codex`・宣言Tier 1。読取り指示は
   shell読取り（§7.2の差し込み文）。
3. **起動固定形**（§7.2）：`exec` subcommand・`--json`・`--output-schema`（第一候補）・
   `--sandbox read-only`・`--skip-git-repo-check`・`--ephemeral`・`--ignore-user-config`・
   `-m <許可一覧先頭>`・prompt末尾位置引数・stdin遮断・作業dir＝対象repository。
4. **openai系認証遮断**（§7.3）：直書き禁止一覧＋起動前検査・最小通過環境。
5. **許可model**：承認record確定済みの`("gpt-5.6-sol", "gpt-5.6-terra")`を直書き固定（空開始を
   省略）。requested modelは一覧先頭（既存規則）。和集合`ALLOWED_RESPONSE_MODELS`は末尾追加で
   先頭（agy値＝依頼recordの既定記載）不変。
6. **対象試験（RED先行）**と、利用者指示による**実E2E 1回**（§9-8）。
7. `docs/development/prompts/reviewer-launch-run.md`へのcodex起動の使い方追記。

### 5.2 範囲外

- `tools/request_builder/`の変更。`IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`（model欄とbackendの
  対応検査）は利用者裁定(b)により**本契約受入後の独立小作業単位**（承認record §2-5。台帳上の
  候補状態は変更しない）。
- `gpt-5.6-terra`の起動時選択機構（許可のみ。必要時は小改定＝承認record §2-2）。
- 縦C（合議・判定record比較の上位層）。判定不一致の自動裁定（不一致はHuman裁定）。
- `tools/session_logs/`の変更・import（`parse_codex.py`はprovisional・非正本。event形式の知識と
  fixture `tests/fixtures/session_logs/codex-exec-public-shape.jsonl`を合成stream試験の参考素材と
  して使うのみ）。
- 転記・事後照合・保存・G30登録・導線の変更（既存流用）。外部API直接送信経路の後続（pendingのまま）。
  歴史的recordの書き換え。prompt雛形の共通骨格の文言変更（読取り指示節の差し込み一般化を除く）。

## 6. 固定再利用部品と保護基準

保護基準commitは本候補の固定commitとする。次を変更しない：`tools/request_builder/`（契約011成果）・
`tools/bootstrap/`・`tools/session_logs/`（`parse_codex.py`を含む）・`tools/common/digests.py`・
`tools/development/claude_implementation_*`（実行器4 file。設計流用のみで本体不変）・
`tools/external_review/send.py`・egress・`tools/operations/operation_contract_run.py`・
`tools/evaluation/rq2_paired_trial.py`（entry入口を使用する実験装置）・受入済み製品試験のうち
`tests/test_request_builder.py`。変更してよいのは§8の上限だけである。

## 7. 中心的な取り決め

### 7.1 backend登録簿の固定形

backend定義は直書きの契約固定定数とし、設定file・環境変数・引数・送信指示から追加・変更できない。
agy・claude-subagent定義の値（引数・prompt・許可model・禁止環境変数・通過変数・注入）は本契約で
一切変えない（移設のみ）。第4以降のbackend追加は登録定義の追加＋対象試験で足りる形を完成させる。

### 7.2 codex-cliの起動固定形

- 固定引数：`exec`・`--json`・`--output-schema <schema一時file>`・`--sandbox read-only`・
  `--skip-git-repo-check`・`--ephemeral`・`--ignore-user-config`・`-m <許可一覧先頭>`・
  prompt（末尾位置引数）。**stdinは遮断**して渡す（疎通実測§7でexecがstdinを読む挙動を観測）。
  作業dirは対象repository（`-C`は使わない）。
- **schema一時file**：既存`VERDICT_SCHEMA`（無変更・共用）の正準JSONを、起動核がrepo外一時領域へ
  機械書き出しし、そのpathを渡す。内容は契約固定で毎回同一byteである。
- **危険旗の禁止**：`--dangerously-bypass-approvals-and-sandbox`・`--dangerously-bypass-hook-trust`・
  `--approve-for-me`・`--add-dir`・`workspace-write`／`danger-full-access`系の値を組み立てに
  含めない（両向き試験で固定）。
- `--ignore-user-config`の意図：利用者config・hooksの影響排除（疎通実測でhooks発火を観測）。認証は
  `CODEX_HOME`のログイン状態を使い、この旗が認証へ影響しないことをRED段の実測で確認する。
- **読取り指示の差し込み**：prompt雛形の共通骨格は不変とし、読取り指示節をbackend別差し込みへ
  一般化する（agy・claudeの生成promptは**byte不変**＝golden試験）。codex用差し込み文（v1案。RED段
  実測後の微修正は契約訂正として扱う）：「この実行環境では読み取り専用のshell command（cat・
  shasum等）だけを使い、書込み・変更・対象repository外へのアクセスを行わないでください。最初の
  操作としてcatで対象依頼recordの絶対pathを開き、可能なら`shasum -a 256`で期待SHA-256との一致を
  確認してください」。digest計算はcodexの利点であり、freshness実測（match）が初めて成立し得る。
- **fallback**：`--output-schema`で判定JSONが取得できないことがRED段実測で判明した場合は、
  prompt指示＋出力からのJSON抽出（claude型。`_parse_json_text`の設計流用）へ切り替える。どちらで
  固定したかを実装Evidenceへ記す。両方が不成立なら§10で停止する。

### 7.3 認証遮断と環境

- 禁止（直書き定数。検出時は`api_key_environment_forbidden`で起動前停止）：`OPENAI_API_KEY`・
  `OPENAI_BASE_URL`・`OPENAI_ORGANIZATION`・`OPENAI_PROJECT`。一覧はRED段の実測による**追加だけ**を
  許す（agyの規律と同じ）。認証は利用者のcodexログイン状態だけを使う。
- 通過：`PATH`・`HOME`・`USER`・`TMPDIR`・`LANG`・`LC_ALL`・`LC_CTYPE`・`TERM`・`NO_COLOR`・
  `CODEX_HOME`（ログイン状態の置き場。未設定なら渡さない）。
- 注入：なし（agyと同じ。codex固有の抑止が必要とRED段実測で判明したら契約訂正で追加する）。

### 7.4 model観測と判定抽出

- stream（`--json`のJSONL）の**正準位置**からmodel表記を機械取得し、許可一覧と照合する（観測不能は
  `response_model_unobserved`・許可外は`response_model_not_allowed`で停止）。正準位置はRED段実測で
  確定し、合成stream fixtureへ固定する（既存fixtureを参考素材に。正準位置以外のmodel様文字列では
  判定しない＝文字列理解の原則2）。
- 判定は最終応答のschema準拠JSON（§7.2）。抽出不能・schema不適合は`verdict_schema_nonconforming`で
  停止する（raw先行保存済み）。schema検証は既存`validate_verdict`を共用する。

### 7.5 残余risk（明示的に受容を諮る）

1. **対象repository内容がopenaiのレビュー役に読まれる**。露出先としては従来のcodex独立レビュー運用
   （pilot-driven-record-handoff）と同一だが、RC3の正式経路として常用化する。緩和：起点は利用者
   指示のみ・promptはpath＋SHA-256だけを運ぶ・起動record台帳・raw完全保存。
2. **headless完走性が未確定**：この端末は承認方式が`OnRequest`（都度承認）に固定されている
   （`/etc/codex/requirements.toml`）。read-only sandbox内の読取りは承認不要見込みで、疎通の最小
   実行は完走したが、読取り道具を使う実レビューの完走はE2Eで確定する。不成立は§10停止（自動迂回
   しない）。
3. codex CLI仕様変更への追随risk（agy・claudeと同型。実挙動は実測が正）。緩和：安全側停止・raw保存。
4. `gpt-5.6-terra`は許可済みだが起動選択機構がない（先頭`gpt-5.6-sol`固定）。必要時は小改定。
5. 登録簿深化はagy・claude経路の内部構造変更を含む。緩和：生成prompt・引数のbyte不変golden＋
   既存試験の無変更全緑の機械証明（§9-2）。

## 8. 変更上限

1. `tools/reviewer_launch/core.py`（登録簿深化・codex-cli追加・openai遮断・schema一時file書き出し）。
2. `tools/reviewer_launch/entry.py`（必要最小。`--backend`引数は既存一般化済み）。
3. `tools/reviewer_launch/record.py`（codex backend名の転記対応が必要な場合の最小変更）。
4. `tests/test_reviewer_launch.py`（既存caseを維持したまま拡張。byte不変golden・codex系試験の追加）。
5. `docs/development/prompts/reviewer-launch-run.md`への追記（codex起動の使い方）。
6. Evidence、独立確認、受入判断、TODO更新。

## 9. 受入条件

実装開始後は失敗試験を先に固定し、期待どおり失敗してから最小実装を行う。

1. RED：登録簿一般化（name分岐の消滅）・codex固定引数（読み取り専用・危険旗不在の両向き）・
   openai遮断・stdin遮断・schema一時file・合成streamのmodel照合と判定抽出・和集合互換（先頭不変・
   所属検査）・prompt byte不変goldenの失敗試験を先に固定する。
2. agy・claude互換：一般化後も**両経路の既存試験caseが無変更で全緑**、かつ生成promptと組み立て
   引数の**byte不変golden**が合格する（値の移設だけであることの機械証明）。
3. name分岐の消滅：起動核のbackend名によるif分岐（事前走査の測定固定点6箇所）が登録参照へ置換
   されたことを機械確認する。
4. codex固定引数：§7.2の危険旗・書込み系値が組み立てに存在しない（両向き試験）。
5. 認証遮断：§7.3の4種が存在時に起動前停止する。
6. stream解析：codex形式の合成streamでmodel照合（許可外停止）と判定抽出・schema検証（不適合停止）が
   両向きで働く。
7. 互換：`ALLOWED_RESPONSE_MODELS`が4値の和集合として維持され（先頭＝agy値不変）、**契約011対象
   試験（`tests/test_request_builder.py`）が無変更で全緑**。
8. 実E2E 1回：利用者の明示指示の下、codex-cliで実対象1件のレビュー一往復を実環境で行う。対象は
   契約011の正式経路で組み立てた依頼record（slug末尾`-codex`等の別名とし、判定record名の1対1導出に
   よる衝突を回避＝契約012 SR-C12-2の型）。完走・raw保存・判定record転記・事後照合4点合格。
   不成立なら停止し、自動再試行・自動切替をしない。
9. 既存試験：縦B拡張後の対象試験・契約011対象試験・G30系・正規全試験（禁止認証隔離条件）が各単独
   終了コード0。§6保護対象が基準commitから差分0。
10. 完了レビュー：正式経路の既定（**agy・Tier 1**）で実施し、`verified`系（blocking 0件）を得る。
11. 利用者が§7.5残余risk 5点を確認して製品処理を受け入れる。受入をもって
    `IC-BACKEND-REGISTRY-DEEPENING-001`はconsumer（本契約）とOutcomeへ接続され、closed条件が揃う。

## 10. 停止条件

- codexのheadless起動が読み取り専用の固定引数で完走しない（承認要求での停止を含む）。
- `--output-schema`とfallback抽出の両方で判定JSONが取得できない。
- 互換が保てない（agy・claude既存case・byte不変golden・契約011対象試験の変更が必要になる）。
- §6保護対象の変更が必要になる。
- 対象・関連・正規全試験または独立確認が不合格になる。

## 11. 影響、未実施、次作業

【判断】受入後は3 backend体制（Tier 1×2＝agy・codex-cli、Tier 3×1＝claude-subagent）となり、
同一依頼recordへの3判定役比較——縦C（合議）の前提材料——が揃う。登録簿深化により、以後のbackend
追加は登録定義の追加＋対象試験で済む形になる。

【未実施】契約採用、実装、codexの実E2E、既存成果物の変更、`IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`の
独立小作業単位の定義（本契約受入後）。

次は本候補の固定commit後、自己レビュー（5段手続き第1・2段）→依頼record組み立て（契約011の正式経路）→
機械検査→独立確認（agy headless起動。起動は利用者の明示指示による）→採用判断の順で進める。
