# Claude向け Python 3.13一時cache補正・差分限定レビュー指示 v1

あなたはReviewCompass3の独立事前レビュー担当です。Python 3.13移行作業票v2からv3へ追加した
bytecode cache（Pythonが作る実行用の一時ファイル）補正だけを確認してください。成果物を変更せず、
読み取りと照合だけを行ってください。

## 1. 対象

- 先行版：`docs/development/2026-08-13-python-313-development-environment-migration-bootstrap-work-ticket-v2.md`
- 先行版SHA-256：`1d5836efed25fd049ce35772c6de60aaf4e40a952bfe8c580e7004a5ab5c5d16`
- 対象版：`docs/development/2026-08-13-python-313-development-environment-migration-bootstrap-work-ticket-v3.md`
- 対象版SHA-256：`8a9b5d1a04428ebf906b060a397ac2934d4dd408d06bf608542aa818af9d821d`
- 観測対象コミット：`f969dbd6cfe8d2516d9ce7982b81efe318586a59`
- 変更候補：`tests/test_policy_test_runner.py`と`tools/development/policy_test_runner.py`の2 pathだけ

## 2. 固定した観測

次は申告をそのまま信用せず、既存source、Git object、結果記録から可能な範囲で照合してください。

1. Homebrew Python 3.13.14では`sys.pycache_prefix=None`である。
2. 正規commandの公式全試験は、合成Git worktree内の`tests/__pycache__`を許可外変更として数え、
   6 failed / 1,730 passed、終了コード1になった。
3. project外の一時`PYTHONPYCACHEPREFIX`を明示した代表確認では、合成Git worktree試験とcache作成試験が
   同時に2件成功した。
4. `PYTHONDONTWRITEBYTECODE=1`を手で加えた別の失敗は作業担当の実行条件誤りであり、v3はその一般対策へ
   広げていない。

結果記録：

- `/private/tmp/reviewcompass-stage2-python313-migration-green-v1.json`
  - SHA-256：`f537dae22206f325967324388fda62a72dba4c4cc249ae080763f04b91d7ef36`
- `/private/tmp/reviewcompass-stage2-python313-migration-green-v2.json`
  - SHA-256：`eeb4ed725095b7c569b9fc222c14ef5f23ae2579193ee3a8a11e9a1cc0c4fd42`

一時結果記録を読めない場合は、そのことだけで不合格にせず、v3に固定された値とGit内のsourceから
レビューできる範囲を明示してください。

## 3. レビューする問い

v3の§2から§6について、次の4点だけを確認してください。

1. 公式試験本体の間だけproject外の一時directoryを作り、子processの`PYTHONPYCACHEPREFIX`を上書きする案で、
   観測された6件の直接原因を除けるか。
2. `tests/test_policy_test_runner.py`のRED条件は、pathが絶対・project外、実行中は存在、終了後は不存在、
   親環境不変、既存値の上書きを確認し、実装の取り違えを検出できるか。
3. この案は、独自のcache pathを明示する`tests/test_task_python_cache.py`を妨げず、合成Git worktreeへ
   `__pycache__`を残さないか。
4. 設定形式、結果記録形式、Git検査、task cache機構、他の環境変数へ変更を広げず、2 pathで完結するか。

中心判断を否定できる反証を最低一つ試してください。sourceやfileを変更せずに行える、既存処理順の追跡、
既存試験の読み取り、または一時領域だけを使う小さな再現に限ります。

## 4. 本質から外れた過剰対応の禁止

ここは特に厳守してください。

- v2で確認済みのHomebrew取得、依存固定、正式`.venv`退避・復旧、設定変更を再レビューしない。
- Python環境管理の一般化、複数版対応、新しい設定項目、結果記録の項目追加を提案しない。
- `.gitignore`、合成Git worktree、task cache機構、全試験fixtureの改善へ広げない。
- `PYTHONDONTWRITEBYTECODE`や他の環境変数を一般的に正規化する提案をしない。
- 将来の改善、表現改善、「念のため」の防御を止める指摘にしない。
- 修正案は、今回の2 path案では6件の原因を除けない具体的欠陥がある場合だけ、最小限を一文で示す。
- 指摘数や文書量をレビュー品質とみなさない。

## 5. 実行上の禁止

- fileの作成、変更、削除、stage、commitをしない。
- push、tag、amend、rebase、reset、force push、履歴書換えをしない。
- 外部送信、ネット検索、別repository探索をしない。
- 第2段完了を判断しない。

## 6. 出力形式

日本語で簡潔に、次の順で出力してください。

1. `判定`：`開始可`または`修正要`。
2. `変更点の照合`：上の4問に各一文。
3. `止める指摘`：0件なら`0件`。ある場合は根本原因ごとに一件へまとめ、証拠と影響を示す。
4. `報告不一致`：0件なら`0件`。ある場合は証拠と影響を示す。
5. `試した反証`：方法、終了コード、結果、判定への影響。
6. `未実施`：変更、外部送信、段完了をしていないこと。

余分な改善案、代替設計、長い将来計画は出力しないでください。
