# Claude向け Python 3.13一時cache補正・第三path確認指示 v3

あなたはReviewCompass3の独立修正後確認担当です。作業票v4からv5へ追加した第三の試験pathだけを確認して
ください。成果物は変更せず、読み取りと照合だけを行ってください。

## 対象

- 先行版：`docs/development/2026-08-13-python-313-development-environment-migration-bootstrap-work-ticket-v4.md`
- 先行版SHA-256：`e2b753d882803c1c1f655d32a6c0202e89108f7af6b2b307c11206e5f2e8fcfe`
- 対象版：`docs/development/2026-08-13-python-313-development-environment-migration-bootstrap-work-ticket-v5.md`
- 対象版SHA-256：`38284c7272398acebc2de8ff77b9dedbf88eb69eb56a0dc19f90d7dbb648ddd5`
- 対象試験：`tests/test_task_python_cache.py::test_environment_mapping_does_not_change_the_running_process`
- 対象試験fileの変更前SHA-256：`10550c3d453dbd741f6c4eefce4c02dee301417fd0b82c55731cd38559f62901`

## 確認する一点

公式runnerの子試験環境には`PYTHONPYCACHEPREFIX`が存在する。一方、対象試験は関数呼出し前から変数がない
ことを暗黙に仮定していた。v5は対象試験へ`monkeypatch`を受け取り、`before`取得前に
`monkeypatch.delenv("PYTHONPYCACHEPREFIX", raising=False)`を行う一変更だけを許可する。

次を確認してください。

1. 試験開始条件を試験自身が用意するだけで、対象関数が`os.environ`を変えないという検査を弱めないか。
2. 既存の「変数が存在しない」と「環境全体がbeforeと一致する」の二つのassertionを残すため、対象関数が
   変数を追加・削除・変更した場合は従来どおり検出できるか。
3. `monkeypatch`が試験終了後に親から受け取った値を復元し、後続試験へ影響を残さないか。
4. `PYTHONPYCACHEPREFIX`の全参照箇所に、同じ開始前提を持つ別の試験がないか。

## 過剰対応の禁止

- v4の公式runner実装、一時cache方式、`-B`、設定、結果記録を再レビューしない。
- `tools/development/task_python_cache.py`、共通fixture、他の環境変数を変更する案へ広げない。
- assertion削除、skip、xfail、一般化、別設計、将来改善を提案しない。
- 今回の一点で残る1失敗を解消できない具体的欠陥がある場合だけ、最小の止める指摘を示す。

## 禁止と出力

fileの作成・変更・削除、stage、commit、外部送信、ネット検索、全試験、段完了を行わないでください。
日本語で、`判定`（`開始可`または`修正要`）、`止める指摘`、`報告不一致`、四つの確認結果、未実施を
簡潔に示してください。これは変更点だけを見る一回限りの確認です。
