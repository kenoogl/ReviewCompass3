# 契約012 §7.2固定引数の訂正（--verbose列挙漏れ）Human判断record v1

- 判断日：2026-08-17
- 状態：`adopted`
- 対象：採用中の契約012候補v2 §7.2「claude-subagentの起動固定形」の固定引数列挙
  （`records/task-contract/2026-08-17-claude-subagent-backend-candidate-v2.md`。
  歴史的recordは書き換えず、本recordを訂正overlayとする）
- 実測根拠：契約012 subagent許可model承認record §2.1・§4-1
  （`records/development/2026-08-17-subagent-allowed-models-approval-v1.md`）

## 1. 承認文言【記録】

> §7.2の--verbose列挙漏れを契約訂正として承認する。訂正record→実装→試験追随まで進めて」（E2E前提の解消①

（2026-08-17 chat。Claudeが前報の文言例として提示した「§7.2の`--verbose`列挙漏れを契約訂正として
承認する。訂正record→実装→試験追随まで進めて」の採用による承認。末尾の「」（E2E前提の解消①」は
文言例の引用記号の写り込みであり、判断内容は同一）

## 2. 事象と原因【実測】

1. claude CLI 2.1.220は`--print`＋`--output-format=stream-json`の組で`--verbose`を必須とし、
   契約§7.2の列挙どおりの固定引数では起動が成立しない（承認record §2.1。stderr：
   `Error: When using --print, --output-format=stream-json requires --verbose`）。
2. §7.2は実行器`_arguments`の設計流用を宣言するが、流用元
   `tools/development/claude_implementation_executor.py`の引数列に存在する`--verbose`
   （`stream-json`直後）が契約の列挙から漏れていた。原因は契約起草時の列挙漏れである。

## 3. 訂正内容【判断】

1. 契約012 §7.2の固定引数列挙へ`--verbose`を追加する。位置は`--output-format stream-json`の直後
   （流用元実行器と同位置）。
2. 実装`build_claude_arguments`（`tools/reviewer_launch/core.py`）へ同位置で`--verbose`を追加する。
3. 契約v2本文は書き換えず、以後の契約参照はv2＋本recordとする。

## 4. 安全性評価【判断】

- `--verbose`は出力の冗長度（stream-jsonの全イベント出力を成立させる旗）だけに作用し、道具一覧・
  書込み許可・権限mode・認証遮断・promptへ影響しない。読み取り専用性（§7.2）は不変。
- 訂正後の起動成立は実測済み（承認record §2.3：`--verbose`補いの診断起動が終了コード0・
  応答model表記`claude-opus-5`）。§10停止条件「claude CLIのheadless起動が読み取り専用の固定引数で
  成立しない」の該当事象は本訂正で解消する。

## 5. 試験追随【判断】

- `tests/test_reviewer_launch.py::test_subagent_arguments_fixed`の期待引数列へ`--verbose`を
  同位置で追加し、先に失敗（RED）を確認してから最小実装を行う。
- 契約012対象51件・契約011対象32件（無変更）・G30運用75件・layout 13件・正規全試験
  （禁止認証隔離条件）の緑を確認する。

## 6. 未実施

- 実E2E（利用者の明示指示待ち。承認record §4-2「操縦環境の認証・起動文脈」の確認を含む）、
  §9-10完了レビュー、§9-11製品受入。
