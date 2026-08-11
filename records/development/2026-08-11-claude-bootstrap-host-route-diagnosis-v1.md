# 無工具Claude疎通 host経路診断 v1

- 日付：2026-08-11
- 対象停止：`2026-08-11-claude-bootstrap-real-run-host-safety-stop-v1.md`
- 調査範囲：外部送信を伴わない読取確認だけ

## 実測

1. 正本の公開入口は
   `reviewcompass3-pilot bootstrap --manifest-digest <sha256> --approval-id <id>`である。
2. `pyproject.toml`は`reviewcompass3-pilot`を
   `tools.development.pilot_collaboration_cli:main`へ接続すると宣言している。
3. 現在の`.venv/bin/`に`reviewcompass3-pilot`は存在しない。PATH上にも存在しない。
4. editable installの登録済みcommandは`reviewcompass3-session-logs`と
   `reviewcompass3-bootstrap-review`の二件だけである。
5. `.venv/bin/reviewcompass3-bootstrap-review`の更新時刻は2026-08-04である。
   `reviewcompass3-pilot`の宣言追加commitは2026-08-11の`0974769d`であり、venvのinstall metadataが
   その追加後に更新されていない。
6. 既存の入口試験は`pyproject.toml`内の宣言文字列だけを確認し、`.venv/bin/`の実行入口または
   install metadataを確認しない。
7. 開発環境の`verify_environment`はPython、pytest、必須package版だけを確認し、project scriptの
   宣言と実体の一致を確認しない。
8. 拒否された実要求は、正本の`reviewcompass3-pilot`ではなく、
   `.venv/bin/python -m tools.development.pilot_collaboration_cli`だった。

## 判断

【実測】正本で承認した公開入口は端末上に実体化されておらず、実要求は内部module直接起動へ置き換わっていた。
このため、実要求が正本の承認済み経路と一致しなかったことは確定である。

【推測】host安全審査が内部module直接起動を承認済みReviewCompass経路として認識できなかったことが、拒否の
主因である可能性が高い。ただし、host審査器の内部規則はリポジトリから読めないため、公開入口を実体化すれば
必ず許可されるとはまだ断定しない。

## 修復候補

1. 既存の開発環境bootstrapでeditable installを更新し、`reviewcompass3-pilot`を実体化する。
2. `verify_environment`へ、`pyproject.toml`で宣言したproject scriptとvenvの登録済みcommandの一致検査を追加する。
3. 正本の公開入口以外を実Runに使わない回帰試験を追加する。

本診断ではvenv更新、production変更、test変更、approval token変更、外部送信、再試行を行っていない。
