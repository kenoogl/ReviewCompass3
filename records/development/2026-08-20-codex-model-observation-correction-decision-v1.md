# 契約015 model観測方式の契約訂正判断record v1

- Decision ID：`DEC-CODEX-MODEL-OBSERVATION-CORRECTION-2026-08-20-V1`
- 判断日：2026-08-20
- 判断者：利用者（Human）
- 記録者：Claude
- 判断の種別：契約015 v2 §7.2（固定引数）・§7.4（model観測）の契約訂正（前例：契約012の
  `--verbose`訂正＝訂正recordを正とし候補本文は書き換えない）
- 訂正の根拠（実測）：`records/development/2026-08-20-codex-cli-backend-red-probe-evidence-v1.md`
  §2-3・§2-4——codexの公開stream（`--json`）にはmodelを載せるイベントが存在せず、応答本文の
  自己申告は実際と不一致（信頼不可）。一方、`--ephemeral`を外すとrollout（codexが端末へ残す
  内部記録）の`turn_context.model`へ実行modelが機械記録される

## 1. 承認文言【記録】

> 案1を承認する。訂正recordを固定して、RED先行で実装を続けて

（2026-08-20 chat。3案——案1 rollout観測・案2 要求model信頼・案3 停止条件発動——のうち推奨案1の承認）

## 2. 訂正内容

1. **§7.2 固定引数**：`--ephemeral`を固定引数から**除く**（rollout生成を許すため）。あわせて、
   同日のfallback発動（契約が予定した分岐＝RED実測Evidence §2-1）により`--output-schema`と
   schema一時fileも固定引数から除く。確定した固定引数列：
   `exec`・`--json`・`--sandbox read-only`・`--skip-git-repo-check`・`--ignore-user-config`・
   `-m <許可一覧先頭>`・prompt（末尾位置引数）。stdin遮断（全backend共通）は不変。
2. **§7.4 model観測**：codex-cliのmodel観測は、公開streamの`thread.started`から`thread_id`を
   機械取得し、`$CODEX_HOME/sessions/`（既定`~/.codex/sessions/`）配下の
   `rollout-*-<thread_id>.jsonl`を一意に機械特定して、`turn_context`の`payload.model`を読む
   方式へ訂正する。観測不能（thread_id欠落・rollout不在・model欠落）は従来どおり
   `response_model_unobserved`、許可外は`response_model_not_allowed`で停止する（守りの水準は
   不変）。
3. **副作用の受容**：codexのsession記録が`~/.codex/sessions`へ残る（codexを通常利用した場合と
   同一の既定挙動）。利用者は案1の承認をもってこれを受容した。
4. 判定取得はprompt指示＋JSON抽出＋既存`validate_verdict`で固定（fallback節の発動。正本は
   RED実測Evidence §2-1）。

## 3. 未実施

- RED試験の固定・最小実装・緑化（本record直後に実施）。実E2E（明示指示待ち）・完了レビュー・受入。
