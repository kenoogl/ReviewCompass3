# Reviewer起動アダプタ（第1 backend：Antigravity CLI） 作業契約候補 v2

- 契約ID：`TC-RC3-PRODUCT-REVIEWER-LAUNCH-ADAPTER-010`
- 契約版：2
- 契約種別：レビュー実行体制の正式ツール化（統合検討の縦B）・第1縦切り
- 状態：`candidate_pending_independent_review`
- 作成日：2026-08-16
- 直前の製品契約：`TC-RC3-PRODUCT-EXTERNAL-SEND-SCAN-REFINEMENT-009 / v2`（受入済み）
- supersedes：`records/task-contract/2026-08-16-reviewer-launch-adapter-candidate-v1.md`、
  SHA-256 `3fc6d20fb4f7c22201c3065d0e17c0cd8db799ab2d669dbd59e07f1437655bea`
- 訂正根拠：起草側自己レビュー
  `records/development/2026-08-16-reviewer-launch-adapter-v1-self-review-v1.md`の
  SR-C10-1（schemaの`tier`二重定義の解消）、SR-C10-2（鮮度の硬い関門をアダプタ二重再計算へ）、
  SR-C10-3（許可model・禁止環境変数一覧の直書き定数化）、SR-C10-4（timeout値の契約固定）
- 入力：統合検討record（利用者確定・agy訂正済み）、縦B事前走査v1＋追補v1、利用者指示
  「縦Bを採用する。事前走査から進めて」「追補recordを作成し、統合検討recordもagyへ訂正して。
  契約候補v1は第1 backend＝agyで作成に進んで」（いずれも2026-08-16 chat）
- 実装状態：未開始
- 危険度：高
- 危険の理由：repositoryを読めるagentのheadless起動は実質の外部送信（課金・repository内容の送出）で
  ある。また判定recordの機械転記・単独commitは独立確認の信頼の中心（判定の正本）に触れる

## 1. 位置と縮小境界

【記録】暫定体制はGemini手動利用・Human運搬であり、本sessionで8回実運用した（統合検討§3）。残る空白は
起動の機械化だけである。事前走査＋追補により、agy（1.1.13）は導入済みで、headless起動・stream-json・
`--json-schema`による構造化出力の強制を備えることを実測した。

【判断】本契約は縦Bの第1縦切りとして、**agy backend 1本による読み取り専用レビュー一往復**だけを機械化する。

- Reviewerに書込み・commitをさせない。判定は構造化出力（JSON）で受け取り、判定recordの生成・単独commitは
  アダプタ側の機械処理が行う（暫定体制の「Claudeが転記・commit」を機械へ置き換える形。handoff方式の
  Reviewer書込みは範囲外）。
- backend抽象は最小骨格（登録形1つ＋agy 1本。第2縦切りでclaude-subagentを追加できる形）。
- 独立性tierはTier 1（別プロバイダ）の機械判定＋宣言だけを実装し、Tier 1以外は停止する
  （Tier 2／3の宣言・Human受容機構は第2縦切り）。
- LLM／機械の分担（統合検討§6.1の(5)(6)）：起動・保存・転記・照合は完全機械。LLMに残るのは判定要旨の
  確認だけ。

## 2. Human承認境界

- 起動の起点は**利用者のchatによるレビュー実施指示**とし、起動ごとの追加承認手続きは設けない。
  根拠：(1) 暫定体制でも利用者が毎回手動でGeminiへ渡しており、repository内容のGoogleへの露出は利用者
  自身の操作として既に実績がある、(2) 契約008 v5 §2の前例（行為の起点は利用者の指示・機械層が内容の
  守りの実体）。
- 機械層の守り：読み取り専用（書込み権限・承認自動化を渡さない。`--dangerously-skip-permissions`の使用
  禁止）・固定形式の起動prompt（自由文を含めない）・対象はcommit済み依頼recordだけ・起動promptの
  byte上限検査（§7.1）・起動record台帳・自動再試行なし・別model／別認証／別経路への自動切替なし。
- 契約内の初回実起動（§9-8のE2E）は、利用者の明示指示を得てから行う。
- 本境界の採否自体を採用判断で確認する（「起動ごとにHuman承認」へ厳格化する選択肢を含む）。

## 3. 権威、証拠

| 役割 | path | SHA-256 |
| --- | --- | --- |
| 統合検討（利用者確定・agy訂正済み） | `records/development/2026-08-16-review-tooling-formalization-study-v1.md` | `00b294afefa90de8cc8dc5141e9d08c23d40971d4338b9ca5021fe857f2daae0` |
| 縦B事前走査v1（流用部品・接続点・digest表） | `records/development/2026-08-16-vertical-b-reviewer-launch-adapter-prescan-v1.md` | `736b9d58227cdb8b66f41abe9b6b0ab1b54515f415e5ccb69170c97bab7cb33a` |
| 事前走査追補v1（agy実測・論点差し替え） | `records/development/2026-08-16-vertical-b-prescan-agy-addendum-v1.md` | `2f5cdec3c2470ed54cd0df58cd46afa47353c6d159ba97c7494b19f65bf760f8` |
| 暫定体制の決定（転記・commitの現行規約） | `records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md` | `1a5fffc5792d17791f5c275b40183a0d4d076233d6d1b7a267cd91cf92174792` |
| 機械化目標（(5)(6)の定義） | `records/development/2026-08-16-external-review-preparation-mechanization-goal-v1.md` | `46a415eb630266e23a87562e6083f873e2fe9790acd34a6699f59b30aee0b45e` |
| 起草側自己レビュー（v1→v2の訂正根拠SR-C10-1〜4） | `records/development/2026-08-16-reviewer-launch-adapter-v1-self-review-v1.md` | 固定commit時点の値を独立確認依頼recordへ記載 |

流用部品のcode・文書のdigestは事前走査v1 §5の表を正とする（本候補の固定commit時点で差分0を§9-9で確認する）。

## 4. 実装方法の3案

| 案 | 内容 | 判断 |
| --- | --- | --- |
| A 最小（既存機能のみ） | 暫定手動体制を続け、固定起動文面の文書化だけ行う | 新規実装0だが運搬が残り、機械化目標(5)(6)に達しない。blocker（codexCLI停止）の回避にもならない。不採用 |
| B 読み取り専用起動＋構造化判定＋機械転記 | agyを`--print`＋`stream-json`＋`--json-schema`で起動し、判定JSONをアダプタが検証して判定recordへ機械転記・単独commit・事後照合する | 書込み権限を外部agentへ渡さず、暫定体制の転記規約をそのまま機械化する。実行器の起動設計を流用できる。推奨 |
| C handoff方式の移植 | Reviewer自身が判定recordを書いてcommitする（codex exec方式） | agyへの書込み許可とheadless書込み挙動の実測が必要で、外部agentの権限が最大になる。第2段以降の候補として保留。不採用 |

## 5. 範囲

### 5.1 範囲内

1. backend抽象の最小骨格：backend定義（名・provider・model指定・起動関数）の登録形と、agy backendの登録。
2. agy起動部：固定引数（§7.1）による1回起動、認証遮断（§7.1の禁止環境変数）、最小環境渡し、
   終了コード・stream出力の機械取得。
3. 固定形式の起動prompt生成：役割宣言・対象依頼recordのpathとSHA-256・開始時鮮度検査の指示・
   判定schemaの指示だけを含む（依頼record本文の組み立ては縦A。本契約は既存の依頼recordを対象とする）。
4. 独立性tierの機械判定＋宣言：pilot provider（`anthropic`固定）とbackend providerの比較。Tier 1以外は
   `reviewer_not_independent_tier`で停止。判定結果（tier・model）を起動recordと判定recordへ記録する
   （tierの真実の源はアダプタ判定だけ。SR-C10-1）。
5. 起動record・未加工出力の不変保存：`tools/bootstrap/raw_review_store.py`の`store_raw_executions`を
   再利用し、repo外私有領域へ保存（保存処理を複製しない。実行補助`execute_review_assignments`は
   経由しない——同関数の「両route必須」は本用途に適さないことを自己レビューで機械確認済み）。
6. 判定recordの機械転記：schema適合JSONから`records/session-handoffs/`へ判定recordを生成し（着地先は
   統合検討§6.3の利用者確定どおり）、そのrecord 1件だけを単独commitする。冒頭へReviewer（provider・
   model）・tier（アダプタ判定値）・起動方式（headless機械起動）・未加工出力の保存先種別とSHA-256を
   記載する。
7. 事後照合（§7.3）の機械実行。不備は停止。
8. 導線配備：単体入口（`pyproject` scripts `reviewcompass3-reviewer-launch`）、G30操作登録
   （`_OPERATIONS`へ1 entry。前例`one_item_review_prepare`）、`docs/development/prompts/`のrun入口、
   `AGENTS.md` §1への入口1行。
9. 対象試験（RED先行・subprocess差替えの単体試験）と、利用者指示による実E2E 1回（§9-8）。

### 5.2 範囲外

- claude-subagent／codex-cli backendの実装、Tier 2／3の宣言・Human受容機構（第2縦切り以降）。
- Reviewer書込み方式（handoff方式のheadless移植）。
- 依頼組み立て器（縦A）、prompt品質gate（縦C）、監査・判定の多周自動化。
- 外部API直接送信経路の後続（pendingのまま）。暫定手動体制の廃止（fallbackとして残す）。
- 実行段階台帳（pilot-specific §5.2）の一括実装。
- 歴史的record・台帳・Evidenceの書き換え。

## 6. 固定再利用部品と保護基準

保護基準commitは本候補の固定commitとする。次を変更しない：`tools/bootstrap/raw_review_store.py`・
`tools/bootstrap/review_execution.py`・実行器4 file（`claude_implementation_*`。設計流用のみで本体不変）・
`tools/external_review/send.py`・egress 7 module・受入済み製品群とその試験。
`tools/operations/operation_contract_run.py`は`_OPERATIONS`への1 entry追加（と必要最小の分岐）だけを行う。

## 7. 中心的な取り決め

### 7.1 起動の固定形

- 固定引数：`--print`・`--output-format stream-json`・`--json-schema <判定schema>`・`--model <許可model>`・
  `--disable-slash-commands`・`--print-timeout 600s`（契約固定値。SR-C10-4）。
  `--dangerously-skip-permissions`と書込みを許す`--mode`は使用禁止。sandbox・作業ディレクトリの扱いは
  RED段の実測で確定し、読み取り専用相当が成立しない場合は停止する（§10）。
- 認証遮断：子環境から`GEMINI_API_KEY`・`GOOGLE_API_KEY`・`GOOGLE_GENAI_API_KEY`・
  `GOOGLE_APPLICATION_CREDENTIALS`を検出したら起動前に停止する（実行器`FORBIDDEN_AUTH_ENVIRONMENT`の
  型を流用）。認証は利用者のagyログイン状態だけを使う。
- 一覧の格納先（SR-C10-3）：禁止環境変数一覧と許可model一覧はアダプタ内へ直書きする契約固定の定数とし、
  設定file・環境変数・引数・送信指示のいずれからも追加・変更できない。禁止一覧はRED段の実測で追加だけを
  許して確定する（削除・緩和はしない）。許可model一覧の値は実E2E前の利用者承認recordで確定して定数へ
  固定し、以後の変更は契約改定とする。応答streamのmodel表示を許可一覧と照合する（実行器の型）。
- 起動promptのbyte上限：16,384 byte。超過は起動前に停止する。起動promptは§5.1-3の固定要素だけで、
  自由文・依頼内容の複製を含めない。

### 7.2 判定schema（構造化出力の固定形）

5段手続き2周の実測で確立した構造要素（統合検討§3）を機械形式にする。必須項目：

- `reviewer`（provider・model。応答streamのmodel表示との照合はアダプタが行う）
- `freshness`（期待SHA-256・観測値・`match|mismatch|not_computable`。`observed`は機械計算値、
  計算できない場合は`not_computable`と理由。`mismatch`なら判定せず停止報告。SR-C10-2）
- `target`（依頼record path・対象commit）
- `findings[]`（識別子・重大度・`blocking`真偽・主張・根拠path・根拠の位置）
- `unexamined[]`（未検査事項の明示。空なら空配列を明示）
- `verdict`（`verified|verified_with_findings|rejected|stale_target|unable`の5語彙だけ）
- `summary`（判定要旨）

`tier`はschemaに含めない（アダプタが判定・記録する。SR-C10-1）。

### 7.3 事後照合（機械実行4点）

1. 鮮度（硬い関門はアダプタの二重再計算。SR-C10-2）：アダプタが起動直前に依頼recordのSHA-256を
   再計算して依頼record記載の固定値と照合し、事後照合でも再計算して一致すること。Reviewerの
   `freshness`が`mismatch`の場合は停止。`not_computable`の場合は判定recordへ理由つきで明記する。
2. 単独commit：判定record commitが対象commitより後にあり、変更pathがそのrecord 1件だけである。
3. 根拠照合：`findings[]`の根拠pathが実在し、判定recordへ転記した未加工出力SHA-256が保存実物と一致する。
4. 形式：schema必須項目が揃い、`findings`識別子が一意で、`verdict`が5語彙内である。

### 7.4 残余risk（明示的に受容を諮る）

1. repository読取り＝Googleへの内容送出である。暫定体制（利用者の手動Gemini利用）と同じ露出だが、
   機械起動により頻度が上がり得る。緩和：起点は利用者指示（§2）・対象はcommit済み依頼recordだけ・
   起動record台帳が事後監査線。
2. agyの認証・課金・headless実挙動（読み取り専用相当の成立・`--json-schema`の実効・終了コード）は
   §9-8の実E2Eまで不確実である。不成立なら停止し（§10）、別経路へ自動で切り替えない。
3. 判定品質はTier 1でもmodelに依存する。緩和：`high` risk作業では機械反証・決定的検査を併用する
   既存protocol（work-review-protocol §5）が不変のまま適用される。

## 8. 変更上限

1. 新規：`tools/reviewer_launch/`（backend登録形・agy起動部・prompt生成・転記・事後照合・入口）。
2. 新規：`tests/`の対象試験（`test_reviewer_launch*.py`）。
3. `pyproject.toml`の`[project.scripts]`へ1行追加。
4. `tools/operations/operation_contract_run.py`の`_OPERATIONS`へ1 entry追加（と必要最小の分岐）。
5. 新規：`docs/development/prompts/reviewer-launch-run.md`。`AGENTS.md` §1へ入口1行。
6. Evidence、独立確認、受入判断、TODO更新。

## 9. 受入条件

実装開始後は失敗試験を先に固定し、期待どおり失敗してから最小実装を行う。

1. RED：認証遮断・tier判定（Tier 1以外の停止）・固定引数・byte上限・保存・転記・事後照合4点の失敗試験を
   subprocess差替え（実行器試験の型）で先に固定する。
2. 認証遮断：§7.1の禁止環境変数が存在すると起動前に停止する。
3. tier判定：`google`×`anthropic`でTier 1が宣言され、起動recordと判定recordへtier・modelが記録される。
   同一provider指定は停止する。
4. 保存：起動recordと未加工出力が上書き禁止で保存され、commitされる判定recordには保存先種別・SHA-256・
   参照権限だけが載る（repo内へ未加工出力を置かない）。
5. 転記：schema適合の判定JSONから判定recordが生成され、そのrecord 1件だけの単独commitになり、冒頭に
   Reviewer（provider・model）・tier（アダプタ判定値）・起動方式が載る。schema不適合は転記せず停止し、
   未加工出力は保存される。
6. 事後照合：§7.3の4点のいずれかが不成立の場合に停止する（成立・不成立の両向き試験）。
7. 導線：単体入口が別の現在位置から実行でき、G30操作として登録実行でき、prompts入口と`AGENTS.md` §1の
   1行が存在する。
8. 実E2E 1回：利用者の明示指示の下で、利用者が指定する実対象1件（commit済み依頼record）のレビュー
   一往復を実環境で行い、認証・headless挙動・schema強制・保存・転記・事後照合を実測する。不成立なら
   停止して報告し、同じ起動を黙って繰り返さない。
9. 既存試験：対象試験、G30基盤e2e 38件相当、正規全試験（禁止認証隔離条件）が各単独終了コード0。
   §6保護対象が基準commitから差分0。
10. 独立確認（暫定体制：Gemini手動・Human中継）：誤合格・未接続・禁止作用・上位目的への悪影響0件、
    および§2承認境界と§7.4残余riskの受容妥当性の確認。
11. 利用者が§2の承認境界と§7.4の残余riskを確認して製品処理を受け入れる。

## 10. 停止条件

- agy headlessが読み取り専用相当＋構造化出力で成立しない（書込み権限・承認自動化・
  `--dangerously-skip-permissions`が必要になる）。
- 認証・課金上の理由でheadless起動が成立しない。
- §6保護対象の変更が必要になる。
- 対象・関連・正規全試験または独立確認が不合格になる。

## 11. 影響、未実施、次作業

【判断】受入後は、レビュー一往復（起動→保存→判定record生成→単独commit→事後照合）がHuman運搬0回で
回り、暫定体制の手動運搬が解消する。判定の正本はcommitted recordのまま、転記の実行者がClaude（手動）から
機械処理へ替わるだけである。縦A・縦C、第2 backend（claude-subagent）は本契約のbackend登録形の上に載る。

【未実施】契約採用、実装、agyの実起動、既存成果物の変更。

次は本候補の固定commit後、独立確認（暫定体制：Gemini手動・Human中継）を受け、利用者の採用判断を求める。
