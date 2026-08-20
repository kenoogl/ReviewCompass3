# Reviewer launch run

契約の正本は`records/task-contract/2026-08-16-reviewer-launch-adapter-candidate-v2.md`（契約010）で
ある。安全境界（読み取り専用・認証遮断・固定引数・byte上限）と承認境界の規則は正本を参照し、
この入口には複製しない。

## 用途

commit済みの依頼recordを対象に、Reviewer（第1 backend：`antigravity-cli`＝`agy`）をheadlessで
読み取り専用起動し、未加工出力をrepo外私有領域へ不変保存し、構造化判定を判定recordへ機械転記・
単独commitし、事後照合4点（鮮度・単独commit・根拠・形式）を機械実行する。

- 起動の起点は利用者のchatによるレビュー実施指示である（契約§2）。
- 許可model一覧が空の間は`allowed_models_unfixed`で起動前に停止する（実E2E前に利用者承認で確定）。
- 失敗時に同じ起動を自動再試行せず、別model・別認証・別経路へ自動で切り替えない。
- fallbackは暫定手動体制（`records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md`）。

## 単体入口

一往復（起動→保存→転記→事後照合）：

```text
reviewcompass3-reviewer-launch launch \
  --request <依頼recordのrepo相対パス> \
  --expected-sha256 <依頼recordのSHA-256> \
  --run-id <実行識別子>
```

- `--repository`（既定＝現在のdirectory。repository根元から実行する）と`--private-root`
  （既定＝`~/.reviewcompass3-private/reviewer-launch`）は**機械既定で解決**する。上書きは
  任意引数（2026-08-18既定値化。手組み立てを不要にする）。
- `--run-id`は意味を担う識別子（契約・ケース等の符号）であり、操作者が命名する。

起動なしの事前検査（G30と同形式）：

```text
reviewcompass3-reviewer-launch check \
  --input-root <対象repositoryの絶対パス> \
  --request <依頼recordのrepo相対パス>
```

出力は正準JSON一行。終了コードは成功`0`、入力不備または安全境界による停止`2`、内部失敗`1`。

## G30操作

操作名`reviewer_launch_prepare`として`reviewcompass3-operation-run`へ登録済み（入力`request`、
束縛位置`request.sha256`）。G30経由の実行は起動なしの事前検査だけを行う（外部起動は単体入口
`launch`だけが行う）。

## claude-subagent backend（契約012）

同一プロバイダのTier 3 Reviewer。**Tier 2／3は明示受容がある場合だけ起動できる**：

```text
reviewcompass3-reviewer-launch launch \
  --request <依頼recordのrepo相対パス> \
  --expected-sha256 <依頼recordのSHA-256> \
  --run-id <実行識別子> \
  --backend claude-subagent \
  --accept-tier 3 \
  --acceptance-ref <受容根拠recordのrepo相対パス>
```

（`--repository`・`--private-root`の機械既定は上記launchと同じ。）

- `--accept-tier`が宣言tier（claude-subagentは3）と一致し、`--acceptance-ref`が実在する場合だけ
  起動する。欠落・不一致は`reviewer_not_independent_tier`で停止する（機械が黙って独立性を緩めない）。
- subagentの許可model一覧が空の間は`allowed_models_unfixed`で停止する（利用者承認recordで確定）。
- `high` risk作業でTier 2／3を唯一の独立oracleにしない（work-review-protocol §5）。完了レビューは
  Tier 1（agy）で行う。

## codex-cli backend（契約015）

第3 backend（provider `openai`・Tier 1＝機械判定。受容引数は不要）：

```text
reviewcompass3-reviewer-launch launch \
  --request <依頼recordのrepo相対パス> \
  --expected-sha256 <依頼recordのSHA-256> \
  --run-id <実行識別子> \
  --backend codex-cli
```

- 許可model一覧は利用者承認record
  （`records/development/2026-08-20-codex-allowed-models-approval-v1.md`）の2値で、起動は一覧先頭
  （`gpt-5.6-sol`）。`gpt-5.6-terra`は許可済みだが起動選択機構は範囲外（必要時は小改定）。
- 判定取得はprompt指示＋JSON抽出（`--output-schema`はserver側strict検査で既存schema非対応＝
  fallback確定。RED実測Evidence 2026-08-20）。
- **model観測はrollout**（`$CODEX_HOME/sessions/`配下の`turn_context`）から機械取得する
  （公開streamにmodelイベントが無いため。訂正record
  `records/development/2026-08-20-codex-model-observation-correction-decision-v1.md`）。
  このためcodexのsession記録が`~/.codex/sessions`へ残る（codexの既定挙動と同一）。
- 認証は利用者のcodexログイン状態のみ（openai系API鍵の環境変数は検出で起動前停止）。

## モデル選択と記載照合（契約016）

- `launch`の任意引数`--model`で、その系統の**許可一覧の内側**からmodelを選べる（既定＝一覧先頭。
  非所属は`model_not_allowed`で起動前停止）。例：`--backend codex-cli --model gpt-5.6-terra`。
- 起動前に依頼recordの正準依頼先行（backend・model記載）と実行値の一致を機械照合する。不一致は
  `request_backend_mismatch`／`request_model_mismatch`で停止する。依頼recordは組み立て時に
  `--backend`（と必要なら`--model`）を指定して作る（request-builder-run.md参照）。

## モデル追加手続き（契約016 §7.4の定型）

許可model一覧は直書きの契約固定定数であり、実行時に変更できない。追加は次の3点だけで閉じる：

1. 利用者承認record（対象backend・追加する値・理由）を`records/development/`へ作成する。
2. `tools/reviewer_launch/core.py`の該当backendの許可一覧定数へ**定義1行**を追加する。
3. `tests/test_reviewer_launch.py`の該当backendの**承認pin試験1行**を更新する
   （和集合・所属・先頭不変はdata-driven試験が登録簿から自動で検査する）。
