# 開発venv 入口同期検証 GREEN Evidence v1

- 日付：2026-08-11
- 診断：`2026-08-11-claude-bootstrap-host-route-diagnosis-v1.md`
- RED commit：`0af94b5`
- 実装commit：`b4574aa`

## 変更

- `pyproject.toml`の`[project.scripts]`宣言を決定的に読み取る。
- editable installの登録済み`console_scripts`を仮想環境のPythonから取得する。
- 宣言と登録の名前・接続先が完全一致しなければ`project_scripts_mismatch`で停止する。
- 入口fileを手作業で作らず、既存の開発環境bootstrapでeditable installを更新する。

## 実測

1. RED試験：終了1。欠落した`reviewcompass3-pilot`を旧検証器が合格させ、`DID NOT RAISE`で失敗した。
2. 実装後の`tests/test_development_environment.py`：終了0、9 passed。
3. 実環境の更新前検証：終了1、`project_scripts_mismatch`。
4. 既存bootstrap：終了0、`status=updated`、Python 3.9.6、pytest 8.4.2。
5. 更新後の登録済み入口は次の4件で、`pyproject.toml`の宣言と一致した。
   - `reviewcompass3-session-logs`
   - `reviewcompass3-bootstrap-review`
   - `reviewcompass3-pilot`
   - `reviewcompass3-review-plan`
6. `.venv/bin/reviewcompass3-pilot`は実在し、
   `tools.development.pilot_collaboration_cli:main`へ接続している。
7. 関連試験のまとめ実行は18 passed、1 failed。失敗は
   `test_egress_existing_authority_workflow_and_tests_are_not_changed`で、旧base commit以降の全test file不変を
   要求する固定範囲試験が、今回承認済みの`tests/test_development_environment.py`変更を検出したものだった。
   入口同期の9試験と公開入口宣言試験は合格した。本作業では固定範囲試験を書き換えない。

## 外部境界

- Claude起動、認証確認、payload送信、実Run再試行：なし。
- approval token：`pending`に一件だけ存在。
- raw、launch、receipt：作成なし。
