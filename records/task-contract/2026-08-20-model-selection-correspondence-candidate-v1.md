# モデル選択・記載照合・登録定型化（全backend） 作業契約候補 v1

- 契約ID：`TC-RC3-PRODUCT-MODEL-SELECTION-CORRESPONDENCE-016`
- 契約版：1
- 契約種別：受入済み2製品（縦B＝契約010〜015のreviewer_launch・契約011成果物＝request_builder）の
  統合小改定。保留候補`IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`（依頼recordのmodel欄とbackendの
  対応検査）を消化する
- 状態：`candidate_pending_independent_review`
- 作成日：2026-08-20
- 直前の製品契約：`TC-RC3-PRODUCT-CODEX-CLI-BACKEND-015 / v2＋訂正record1件`（受入済み）
- 入力：契約015受入record §4（terra起動選択機構＝小改定・IC＝(b)独立小作業単位）、統合の利用者裁定
  「統合1本（契約016：モデル選択＋照合＋登録手続き定型化・全backend対象）で進めてください。
  事前走査から入り、契約候補の範囲案まで見せてください」、範囲確定「範囲案どおり契約候補v1を
  作成してください。停止語彙は新設2つの案で」（いずれも2026-08-20 chat）、事前走査v1（6手順）、
  正式再利用検索（`start_allowed: true`）
- 実装状態：未開始
- 危険度：中
- 危険の理由：外部送信の対象は増えないが、受入済み2製品を同時に改修する。誤実装は依頼組み立て・
  機械検査・起動の正式経路全体の回帰に直結する

## 1. 位置と縮小境界

【記録】現状、(1) 起動時のmodelは各backendの許可一覧の先頭固定で、承認済みの`gpt-5.6-terra`を
選べない。(2) 依頼recordの「依頼先」行はbackend名がagy直書き・modelは和集合先頭の差し込みで、
検査は文書全体からの正規表現検索＋和集合所属のみ——系統と不対応の記載が合格する（観測record
`OBS-RC3-REQUEST-BUILDER-UNION-CHECK-2026-08-17-V1`）。実際、契約015の実E2Eも「agy記載のまま
codex起動」の不一致状態で走った（起動側照合が最終防衛のため実害なし＝実測）。(3) model追加の
手続きは定型化されていない。

【判断】本契約は統合小改定として、次だけを行う。

- **組み立ての選択入力**：`assemble`へ`--backend`（既定`antigravity-cli`）・`--model`（既定＝
  そのbackendの許可一覧先頭）の任意引数を追加し、依頼先行をbackend別の機械差し込みにする。
- **検査の強化**：依頼先行を**正準位置**から機械抽出し、backend・model対の所属をそのbackendの
  許可一覧で検査する。
- **起動の選択入力と対応照合**：`launch`へ`--model`任意引数を追加し、起動前に「recordの記載」と
  「実際の起動値」の一致を検査する（不一致は新設2語彙で停止）。
- **登録手続きの定型化**：直書き原則を維持したまま、model追加の差分を最小定型に固定する。
- 判定・転記・事後照合・保存・G30・命名導出は既存のまま流用する（新設しない）。

## 2. Human承認境界

- 組み立て・検査は完全local処理（外部送信なし）。起動の起点は従来どおり利用者のchatによる
  レビュー実施指示（契約010 §2）。
- 契約内の実E2E（§9-7＝terra指定の初起動）は利用者の明示指示を得てから行う。
- 許可model一覧の値は本契約で変更しない（一覧変更は従来どおり承認record＋契約改定）。
- requested modelの権威は従来どおりアダプタが起動record・判定recordへ刻印する値（契約010
  SR-C10-1）。選択入力は許可一覧の**内側**の選択に限る。

## 3. 権威、証拠

| 役割 | path | SHA-256 |
| --- | --- | --- |
| 事前走査v1（6手順・接続点・論点） | `records/development/2026-08-20-model-selection-correspondence-prescan-v1.md` | `e89adcd8085ce5bd46f62ed432aa15c3ec15b87de71edb289b77f81dc9294ad3` |
| 実測の正本（測定ブロック9項目） | `records/development/2026-08-20-model-selection-correspondence-prescan-measurements-v1.md` | `adcd1bd289b1fc32cb1ab8a9457b120fb7b81a8d92e3427953f34db77504baa3` |
| 正式再利用検索の作業別計画 | `records/development/2026-08-20-model-selection-correspondence-reuse-search-plan-v1.json` | `90ae5d5c77efe41d344e99147aab017c8b41dd0ccdb151289ad6fbb822a80086` |
| **正式再利用検索の証明書（start_allowed: true）** | `records/development/2026-08-20-model-selection-correspondence-reuse-search-attestation-v1.json` | `52a8c157a3b3698b62b7dd7fe72438238793dce00e1024e7c28d4ab6e4870c1a` |
| 契約015の製品受入判断（§4＝本契約の合図） | `records/development/2026-08-20-codex-cli-backend-product-acceptance-decision-v1.md` | `482e2dbae54c6a576f5a692b9c3e5c171a38778128cf6f9c182c9e014a1695d6` |
| 許可model承認record（codex 2値・(b)裁定） | `records/development/2026-08-20-codex-allowed-models-approval-v1.md` | `f0f0536ccda07d942e06c1d96fa75c2781387763f63afd0439a5d9c9f7d67c99` |
| model照合の観測record（IC出所） | `records/development/2026-08-17-request-builder-union-model-check-observation-v1.json` | `ea3cdc0d048d9604272c7c918287856e8ec3a6013856b5cde66410b262432517` |
| 改善候補仕分けrecord（候補2＝再評価の系譜） | `records/development/2026-08-17-improvement-candidates-triage-decision-v1.md` | `34f7ca163645fe50770734f92b48ad41b6415983ab1eda61c57efc104be8a162` |
| 文字列理解の失敗類型（必読・起草時照合済み） | `records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md` | `ea482a3c7653b0966316012f43cc87ae426cdd5e429348a7f96c4e7f05ecd7b6` |

流用部品のcode・文書のdigestは事前走査の測定ブロック「契約候補が参照するfileのdigest固定」節
（15 file）を正とする（固定commit時点の差分0を§9-8で確認する）。

## 4. 実装方法の3案

| 案 | 内容 | 判断 |
| --- | --- | --- |
| A 最小（機構を作らない） | terraを使いたい時に許可一覧の順序を契約改定で入れ替える運用 | 変更ゼロだが恒久切替になり「1回だけterra」ができず、改定手続きが毎回重い。IC（対応検査の穴）も残る。不採用 |
| B 統合（依頼先行を軸にした3点セット＋登録定型化） | 依頼先行のbackend別差し込み・正準位置検査・起動時照合を同じ1行を軸に実装し、選択入力と登録定型化を併せる | 記載と実行の不一致という過渡状態を作らない。正準行解析・fence状態追跡・許可一覧callable（契約013・015の成果）をそのまま流用。既定は全て現行値で互換。推奨 |
| C 分割2本（選択のみ先行→照合は後日） | `--model`だけ先に入れ、記載のbackend別化・照合を別契約にする | 選択導入の期間中「記載と実行の不一致」が常態化する。手続き（独立確認・完了レビュー）が2回になり合計工数増。不採用 |

## 5. 範囲

### 5.1 範囲内

1. **組み立ての選択入力**：`assemble`へ`--backend`（既定`antigravity-cli`。`BACKENDS`のkey以外は
   `backend_unknown`停止）・`--model`（既定＝そのbackendの許可一覧先頭。一覧非所属は
   `model_not_allowed`停止＝既存語彙）の任意引数を追加する。**両方省略時の生成recordは現行と
   byte同一**（既定不変golden）。
2. **依頼先行のbackend別差し込み**（§7.2）：`--backend`既定（agy）は現行文言をbyte不変で維持し、
   agy以外を指定した場合だけbackend別の固定文言で差し込む。
3. **検査の強化**：`check`の依頼先行検査を「正準位置（冒頭メタ行ブロック・fence外）の依頼先行
   から最初のbacktick対＝backend名・`許可model`のbacktick対＝model名を機械抽出→backend名は
   `BACKENDS`のkeyと照合→modelはそのbackendの許可一覧と照合」へ強化する。文書全体検索
   （現行`_MODEL_PATTERN.search`）は廃止し正準位置だけを正とする。和集合記号
   `ALLOWED_RESPONSE_MODELS`は互換のため維持する（名称・tuple意味不変）。
4. **起動の選択入力と対応照合**（§7.3）：`launch`へ`--model`任意引数（既定＝一覧先頭・backend
   一覧の所属検査つき）。起動前に依頼recordの正準依頼先行を抽出し、記載backend≠起動backendは
   `request_backend_mismatch`、記載model≠requested modelは`request_model_mismatch`で停止する
   （新設2語彙。利用者裁定2026-08-20）。
5. **登録手続きの定型化**（§7.4）：許可一覧の直書き原則は維持。試験を「登録簿走査のデータ駆動
   （所属・先頭・網羅）＋backendごとの承認pin 1本（literal）」へ整理し、model追加の差分を
   「定義1行＋承認pin 1行＋承認record」に固定。`reviewer-launch-run.md`へ「モデル追加手続き」
   節を追記する。
6. **対象試験（RED先行）**と、利用者指示による**実E2E 1回**（§9-7＝`--backend codex-cli
   --model gpt-5.6-terra`指定の組み立て→起動。選択機構の実証とterra初起動データの同時取得）。
7. 導線2手順書（`request-builder-run.md`・`reviewer-launch-run.md`）への使い方追記。

### 5.2 範囲外

- 許可model一覧の値の変更（一覧変更は承認record＋契約改定の従来規律）。実行時の設定file・
  環境変数・引数によるmodel**登録**（直書き原則の変更は行わない。選択は許可一覧の内側のみ）。
- `record.py`（判定record命名・転記）・G30登録・`tools/session_logs/`・egress・保存・事後照合の
  変更。RQ2装置・運搬部品（`rq2_paired_trial.py`・`reviewer_bridge.py`）の変更（明示旗列起動の
  ため任意旗追加は無影響＝事前走査実測。無影響は§9-6の試験全緑で機械確認）。
- 縦C合議。過去に組み立て済みの依頼recordの書き換え（歴史的record不変。§7.5-2の移行整理を参照）。

## 6. 固定再利用部品と保護基準

保護基準commitは本候補の固定commitとする。次を変更しない：`tools/reviewer_launch/record.py`・
`tools/bootstrap/`・`tools/session_logs/`・`tools/common/digests.py`・
`tools/development/claude_implementation_*`・`tools/external_review/send.py`・egress・
`tools/operations/operation_contract_run.py`・`tools/evaluation/`（rq2_paired_trial・
reviewer_bridge・operational_metrics）。変更してよいのは§8の上限だけである。

## 7. 中心的な取り決め

### 7.1 選択入力の固定形

- 選択は**許可一覧の内側**に限る（一覧非所属は組み立て段`model_not_allowed`・起動段は既存の
  所属検査で停止）。既定は全箇所で「そのbackendの許可一覧の先頭」＝現行挙動と同一。
- requested modelの権威はアダプタが起動record・判定recordへ刻印する値。依頼recordの記載は
  「宣言」であり、§7.3の照合で実行との一致を機械保証する。

### 7.2 依頼先行の正準形とbackend別差し込み

- 正準位置＝冒頭メタ行ブロック（先頭見出し直後の`- `行群・fence外）内の「依頼先：」行だけを
  正とする。抽出は「最初のbacktick対＝backend名」「`許可model`直後のbacktick対＝model名」。
  fence内・本文中の同形行では判定しない（文字列理解の原則2。敵対fixtureを§9-1で固定）。
- 既定（agy）の行は現行文言をbyte不変で維持する：
  `- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、許可model `<model>`）`
- agy以外の差し込み形（契約固定文言）：
  `- 依頼先：Reviewer（backend `<backend名>`、許可model `<model>`）`
- 既存のcommit済み依頼record（agy記載）は上記抽出仕様でそのまま読める（後方互換。§9-3で
  実recordを固定して機械確認する）。

### 7.3 起動時の対応照合と新設停止語彙

- 起動核は依頼recordのbyte（digest束縛済み）から§7.2の正準抽出を行い、次を検査する：
  1. 記載backend名が起動backendと不一致 → **`request_backend_mismatch`** で起動前に停止。
  2. 記載modelがrequested model（`--model`解決値）と不一致 → **`request_model_mismatch`** で
     起動前に停止。
  3. 依頼先行が正準位置から抽出できない → fail-closedとして`request_backend_mismatch`に含める
     （曖昧な救済をしない）。
- 停止語彙は新設2つだけとし、既存語彙の意味を変えない（利用者裁定2026-08-20「停止語彙は新設
  2つの案で」）。
- 移行整理：契約015以前の別名E2E型record（agy記載のまま他backendで起動する型）は本契約以後
  再起動しない。多判定役の運搬は従来どおり「同一対象集合・別名record」で、以後は組み立て時に
  `--backend`を指定する。

### 7.4 登録手続きの定型化（直書き原則の維持）

- model追加の定型＝(1) 利用者承認record（対象backend・値・理由）→(2) 該当backendの許可一覧へ
  定義1行追加→(3) 承認pin試験の1行更新。データ駆動試験（登録簿走査：全backendの一覧非空・
  先頭＝既定・和集合＝各一覧の連結・所属検査の網羅）は変更不要のまま新modelを覆う。
- 実行時に一覧を変更できる経路（設定file・環境変数・引数）は作らない（契約010〜015 §7.1の
  後決め排除の原則を維持）。

### 7.5 残余risk（明示的に受容を諮る）

1. **受入済み2製品の同時改修による回帰risk**。緩和：既定不変golden（省略時の組み立て出力byte
   一致・起動requested不変）＋両suite無変更部分の全緑＋正規全試験。
2. **旧型record運用の停止化**：agy記載のまま他backendで起動する従来の別名E2E型は新検査で停止
   する（運用変更）。緩和：§7.3の移行整理・今後の組み立てで`--backend`指定。
3. **terraの実性能・実挙動は未実測**（初起動はE2Eで取得。rollout観測がterra表記を返すことも
   同時に確認する）。
4. **正準抽出の騙されrisk**。緩和：敵対fixture（fence内偽依頼先行・本文中の同形行・backtick
   欠落）を§9-1で標準固定。

## 8. 変更上限

1. `tools/request_builder/core.py`（依頼先行のbackend別差し込み・正準位置検査・`--backend`／
   `--model`受領）。
2. `tools/request_builder/entry.py`（assemble任意旗2つ）。
3. `tools/reviewer_launch/core.py`（`--model`受領＝requested解決・記載照合・新設2語彙）。
4. `tools/reviewer_launch/entry.py`（launch任意旗`--model`）。
5. `tests/test_request_builder.py`・`tests/test_reviewer_launch.py`（既存caseを維持したまま拡張。
   既定不変golden・後方互換・敵対fixture・データ駆動化とpin整理）。
6. `docs/development/prompts/request-builder-run.md`・`docs/development/prompts/
   reviewer-launch-run.md`への追記（選択の使い方・モデル追加手続き）。
7. Evidence、独立確認、受入判断、TODO更新。

## 9. 受入条件

実装開始後は失敗試験を先に固定し、期待どおり失敗してから最小実装を行う。

1. RED：選択入力（既定・所属外停止）・依頼先行のbackend別差し込み・正準位置抽出（敵対fixture：
   fence内偽行・本文中同形行・backtick欠落）・起動時照合（新設2語彙の両向き）・後方互換・
   既定不変goldenの失敗試験を先に固定する。
2. **既定不変**：`--backend`／`--model`省略時の組み立て出力が現行実装とbyte同一（golden）、
   起動のrequested model解決が現行と同一。
3. **後方互換**：commit済みの既存依頼record（agy記載の実record 1件以上を固定）が新checkで
   従来どおり合格し、agy起動の照合も通る。
4. 新設2語彙：`request_backend_mismatch`・`request_model_mismatch`が該当条件だけで発火し、
   正常経路では発火しない（両向き）。
5. 登録定型化：データ駆動試験＋backendごとの承認pin 1本へ整理され、model追加の差分が
   「定義1行＋pin 1行」で閉じることを試験構造で確認。手順書追記。
6. 既存試験：両suiteの無変更部分・G30系・RQ2装置系・正規全試験（禁止認証隔離条件）が各単独
   終了コード0。§6保護対象が基準commitから差分0。
7. 実E2E 1回：利用者の明示指示の下、`--backend codex-cli --model gpt-5.6-terra`で組み立てた
   別名依頼recordをcodex-cliで起動し、一往復（完走・raw保存・判定record転記・事後照合4点・
   rollout観測がterra表記）を確認する。不成立なら停止し、自動再試行・自動切替をしない。
8. 完了レビュー：正式経路の既定（agy・Tier 1）で実施し、`verified`系（blocking 0件）を得る。
9. 利用者が§7.5残余risk 4点を確認して製品処理を受け入れる。受入をもって
   `IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`はconsumer（本契約）とOutcomeへ接続され、
   closed条件が揃う。

## 10. 停止条件

- 既定不変（組み立て出力のbyte一致・起動既定の同一）が保てない。
- 後方互換（既存recordの合格）が保てない。
- 公開記号（`ALLOWED_RESPONSE_MODELS`・`verdict_record_relative_path`）の名称・意味の変更が
  必要になる。§6保護対象の変更が必要になる。
- 対象・関連・正規全試験または独立確認が不合格になる。

## 11. 影響、未実施、次作業

【判断】受入後は、承認済み一覧の内側でのmodel選択（terraを含む）が組み立て・起動の両方で機械
検査つきで可能になり、「recordの記載＝実行」の対応が経路全体で保証される。model追加は最小定型
（承認record＋2行差分）になる。terraが判定役に加わることで、縦C合議の判定役多様化（同一系統内
の別model比較）の材料も増える。

【未実施】契約採用、実装、terra初起動の実E2E、既存成果物の変更。

次は本候補の固定commit後、自己レビュー（5段手続き第1・2段）→依頼record組み立て（契約011の
正式経路）→機械検査→独立確認（agy headless起動。起動は利用者の明示指示による）→採用判断の
順で進める。
