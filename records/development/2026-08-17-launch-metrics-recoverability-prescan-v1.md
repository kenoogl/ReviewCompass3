# 計測メタ追記＋復元可能性表（データ取得順序1）事前走査 v1

- 記録日：2026-08-17
- 指示者：利用者（Human）。選択文言：「順序1（計測メタ＋復元可能性表）に着手。範囲固定文書
  から進めて」（2026-08-17 chat。上位計画＝評価データ取得計画v1 §4）
- 記録者：Claude
- 種別：作業単位定義前の事前走査（6手順。手順5＝正式再利用検索は作業票の着手後手続きへ
  委譲——コード変更を含むため適用・計画のHuman確認を経て実行）
- 基準commit：`cbcdaa1`（作業tree clean）

## 0. 一枚要約（人向け)

reviewer-launchの実行メタ置き場（repo外私有領域の`launch.json`・12項目）は既にあり、
**欠けているのは時間とprompt規模だけ**。トークン数はraw応答内に既に保存されている
（`usage`・`input_tokens`が現物に存在——追記不要・機械復元可能）。よってコード変更は
「時間計測＋prompt bytesの`launch.json`追記」に縮小でき、repo内の判定record schema・
事後照合4点・既存試験67件は不変で済む。復元可能性表は文書1本。

## 1. 手順1：所在特定【実測】

| 部品・結合点 | 所在 | 状態 |
| --- | --- | --- |
| 実行メタの置き場 | 私有領域`<private-root>/<run-id>/launch.json`（書込みは`tools/reviewer_launch/core.py` 582行） | 既存12項目（`accept_tier`・`arguments`・`backend`・`exit_code`・`prompt_sha256`・`provider`・`raw_digest`等）。**時間・prompt bytesなし** |
| トークン情報 | 同`<run-id>/reviewer.raw.json`の`raw_response`内 | **既に保存済み**（cr-014-001実物に`usage` 9箇所・`input_tokens` 9箇所——agy応答が含む。機械復元可能） |
| 時間計測 | なし（`core.py`・`entry.py`にtime系importなし） | 追記対象 |
| prompt構築 | `core.py` 242行`build_prompt` | byte長の計測点 |
| 判定record（repo内） | `record.py` 217行`_render_record`・286行`transcribe_verdict_record` | **無変更**（schema不変・事後照合4点不変） |

## 2. 手順2：import元【実測】

`reviewer_launch`のimport元：`tools/operations/operation_contract_run.py`（G30）・
`tools/request_builder/core.py`（model一覧・命名導出）・`tests/test_reviewer_launch.py`・
`tests/test_request_builder.py`。いずれも今回の変更（`launch.json`項目追加）の影響を
受けない見込み（launch.jsonを読む既存部品はない——書くだけの構造）。

## 3. 手順4：接続点【実測】

1. **契約010の保護境界**：変更は候補v2 §8変更上限の1（`tools/reviewer_launch/`）・2（対象試験）
   の範囲内。挙動・判定・安全境界・repo内schemaは不変の**後方互換の観測追加**。契約改定
   （新契約）は立てず軽量作業票で扱う——この判断は作業票のHuman確認点。
2. 既存試験：`test_reviewer_launch.py` 67件は無変更維持。新項目の検証試験を追加。
3. 手順書`reviewer-launch-run.md`：変更不要見込み（利用者手順に変化なし）。
4. 上位計画：評価データ取得計画v1 §4順序1。復元可能性表は同§3の指標群を行とする。

## 4. digest表【実測】

```text
ec056cd7dd3426d60bf1333c284d250e00c3b54cbce8be84d64bf46cc32ede3f  tools/reviewer_launch/core.py
998c31d726c3aa37bd5021d83495590ad49015916ab4ca0572890465e495db8d  tools/reviewer_launch/record.py
0b7f569aae8f8b7f1b0668fcab3f9024ed3571d131e5cbb7fe3dc89bb61ff1db  tools/reviewer_launch/entry.py
03f097886dfd90e8d4fbc68a3bb25eb09481cccfd2c3772f5934816a1c71a035  tests/test_reviewer_launch.py
7d159fdf093abad81481ae73eb3d95ad11efd04e2313d6df5a34c27fe583db0a  records/task-contract/2026-08-16-reviewer-launch-adapter-candidate-v2.md
e348964e16cd839ba795801e057f386dec0107cd727326a8c4a818fc79b65cbb  docs/development/prompts/reviewer-launch-run.md
c666bdd7d0b5c44a8fbb876238a19c1d05ee245e693a2b104ceee514cdad55cb  docs/development/2026-08-17-evaluation-data-acquisition-plan-v1.md
```

## 5. 作業票へ渡す論点【記録】

1. 追記項目の確定：`started_at`・`finished_at`（UTC）・`elapsed_seconds`・`prompt_bytes`の4項目
   （トークンはrawから復元可のため追記しない）。
2. 軽量作業票方式（新契約を立てない）の確認。
3. 復元可能性表の対象＝データ取得計画§3の全指標（RQ1/RQ2・H4/H5/H7・コスト）。

## 6. 未実施

- 作業票v1の承認、正式再利用検索（着手後手続き）、RED/GREEN、復元可能性表の作成。
