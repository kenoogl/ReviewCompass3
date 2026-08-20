# codex-cli backend 契約候補v1 自己レビューと文脈整理 v1

- 実施日：2026-08-20
- 担当：Claude（契約作成者による起草側の事前検討。独立確認の代替ではない）
- 方法：Definition Challenge型の固定4質問（定義の欠落・境界の過小・禁止の漏れ・依存の忘れ）を全条項へ
  適用し、重要な主張は機械検証で反証を試した
- 位置づけ：外部レビュー5段手続きの第1段・第2段。契約v2への訂正根拠および依頼promptの文脈材料
- 対象：`records/task-contract/2026-08-20-codex-cli-backend-candidate-v1.md`（commit `e587214`）

## 1. 発見（修正要級——契約v2で訂正する）

### SR-C15-1 読取り指示の差し込み単位が未定義（定義の欠落）

v1 §7.2は「読取り指示節をbackend別差し込みへ一般化する（共通骨格は不変・byte不変golden）」と定める
が、prompt雛形のどの文が差し込み対象なのかを定義していない。機械確認：現行`build_prompt`
（`tools/reviewer_launch/core.py`）の固定文のうち、(a) 実行環境の説明（「この実行環境は読み取り専用
です。端末commandの実行…行わず、fileの読取り道具だけを使ってください」）、(b) path制約（「読取り
道具のpath引数には…絶対pathだけを渡し…領域外アクセスは自動拒否され…」）、(c) 最初の操作と
freshness指示（「最初の操作として、読取り道具%sで…digestの機械計算がこの環境で行えない場合…」）の
**連続3文ブロックが読取り方式に依存**し、agy・claudeでは道具名（`view_file`／`Read`）の差し込み
だけで共通、codexでは(a)が唯一の読取り手段（shell command）を禁止する文になってしまい流用不能。
**訂正**：差し込み単位を「この連続3文の読取り指示ブロック」と定義し、agy・claudeは現行文言を
**逐語移設**（生成promptのbyte不変goldenで機械証明）、codex用ブロックの全文を§7.2へ契約固定する。

### SR-C15-2 repository外読取りの遮断が未保証（境界の過小）

v1の残余riskはrepo内容のopenai露出（§7.5-1）だけを挙げ、**codexのread-only sandboxがrepository外の
読取りを機械遮断する保証が無い**ことを計上していない。agy雛形の「領域外アクセスは自動拒否され」は
agyのE2E実測由来の文であり、codexのhelpからは読取り範囲の遮断は確認できない（書込み・承認迂回の
遮断が主）。**訂正**：残余riskへ6点目として明示し、codex用差し込みブロックへrepo外読取り・network
アクセスの禁止指示を含め、実E2Eのraw（道具実行の記録が残る）で領域外読取りの有無を点検する。

## 2. 発見（軽微——契約v2で明確化する）

### SR-C15-3 stdin遮断の適用範囲が不明確（定義の欠落）

v1はstdin遮断をcodex固定形の中に書いており、起動核の共通処理（`subprocess.run`は3 backend共有）へ
どう適用するかが読み取れない。機械確認：試験のprocess偽装は`def run(self, arguments, **keywords)`
（`tests/test_reviewer_launch.py`）でstdin引数の追加に耐え、`stdin`への言及は実装・試験のどこにも
無い。**訂正**：stdin遮断は**起動核の共通固定事項（全backend）**として明記する（headless起動の
前提。既存試験・引数byteへ影響しないことを本自己レビューで機械確認済み）。

### SR-C15-4 schema一時fileの置き場・寿命が未定義（定義の欠落）

**訂正**：OSの一時領域（`tempfile`）へ機械書き出しし、内容は既存`VERDICT_SCHEMA`の正準JSON
（毎回同一byte）、pathは起動recordの`arguments`欄に残る（run毎の可変部はこのpathのみ）と明記する。

## 3. 点検して問題なしと判断した点（機械検証つき）

- §3のdigest表12件は機械照合で全件一致（照合scriptの実測。2026-08-20）。
- codex execの採用旗（`--json`・`--output-schema`・`--ephemeral`・`--ignore-user-config`・
  `--sandbox read-only`・`--skip-git-repo-check`・`-m`）と危険旗（`--dangerously-bypass-approvals-
  and-sandbox`・`--dangerously-bypass-hook-trust`・`--approve-for-me`・`--add-dir`）はhelp出力に実在
  （事前走査時の実測・起動なし）。
- 和集合の互換：`tools/request_builder/core.py`の既定記載は`ALLOWED_RESPONSE_MODELS[0]`（268行）で
  あり、codex 2値の**末尾追加**なら先頭（agy値）は不変。所属検査（442行）は4値の和集合でterra記載も
  合格するが、backend対応検査の穴は利用者裁定(b)で範囲外に固定済み（起動側照合が最終防衛＝観測
  record記載の実害限定根拠）。
- 判定record転記の依存：`record.py`の`_backend_provider`は`BACKENDS[name]["provider"]`だけを使う
  （機械確認）。登録簿深化で`provider`鍵を保てばrecord.pyは無変更で済む（§8-3は保険の位置づけ）。
- Tier判定：`_resolve_tier`は現行実装がprovider相違（openai≠anthropic）でTier 1を返す。codexに
  受容手続きは不要（コード実測）。
- E2Eの判定record名衝突：slug別名方式（012 SR-C12-2で確立）を§9-8が踏襲済み。
- 実験装置への波及：`tools/evaluation/rq2_paired_trial.py`は`entry`入口だけをimport（事前走査§2）。
  entry入口形と公開記号を変えない本契約では無変更（§6保護対象に明記済み）。

## 4. 文脈整理（依頼promptへ含める判断済み事項・範囲外）

- **判断済み（蒸し返し不要）**：第3縦切り＝codex-cli（利用者指示2026-08-20）。登録簿深化の同時実施
  （仕分けrecord 2026-08-17の裁定）。許可model 2値`gpt-5.6-sol`・`gpt-5.6-terra`（承認record・
  起動は先頭固定）。`IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`は(b)別作業単位（利用者裁定）。
  Tier 1の機械判定（受容手続きなし）。完了レビューはagy（Tier 1・唯一oracle禁止の不変制約）。
- **採用判断で諮る事項**：§7.5残余risk（v2で6点：openai露出の常用化・OnRequest下の完走性・CLI追随・
  terra選択機構なし・登録簿改修の回帰・repo外読取り遮断の未保証）。
- **範囲外（「無い」という指摘は不要）**：request_builder変更・terraの起動選択機構・縦C合議・
  session_logs系の変更／import・転記／照合／保存／G30登録の変更・外部API後続。
- **レビュアへ特に依頼する深掘り**：(1) 登録簿深化の互換保証（byte不変golden＋既存試験無変更）が
  「値の移設だけ」の証明として十分か。(2) codex起動固定形の読み取り専用性（危険旗不在・認証遮断・
  sandbox実効性・stdin遮断）に抜けが無いか。(3) `--output-schema`第一候補＋prompt指示抽出fallbackの
  二段構えがfail-closed原則に反しないか（fallbackが「自動変形による救済」に当たらないか）。
  (4) 残余risk 6点の緩和策が妥当か。
