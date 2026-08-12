# 第2段 公式試験入口の正常化 開始判断 v1

- 判断ID：`DEC-STAGE2-OFFICIAL-TEST-ENTRY-RESTORATION-START-001`
- 判断日：2026-08-12
- 状態：`approved_to_start`
- 作業票：`docs/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-work-ticket-v1.md`
- 作業票SHA-256：`5af82a43c618481e08abf398abdc50d289388eb1388da9aa58ae0ee9a4d1d00f`
- 作業票コミット：`120ec5e3922fa7aaa886cb3aca647e93943ef016`
- 独立開始前レビュー：`records/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-start-review-v1.md`
- 開始前レビューSHA-256：`5dc23327f1072fd5438ca8ff2e2c22634f4257dd8970426471f69696be3a80ad`
- 開始前レビューコミット：`644391c3eeaae97f3b70593ef5827f071e664484`
- 開始前レビュー判定：`開始可`
- 危険度：`high`

## 1. 利用者判断

【記録】利用者は2026-08-12、独立開始前レビューの結果と承認対象を提示された後、「承認」と回答した。

【判断】次の一つの意味単位について、試験先行の作業を開始してよい。

1. 作業票が固定した変更可能pathと結果Evidence一件だけを扱う。
2. 版付き設定へ認証・接続用の環境変数名6個の除外欄を追加し、`runner_version`を2へ上げる。
3. 全試験を起動する子処理だけから6名を除外し、親処理、版確認、件数集計、結果記録、fallback禁止、
   製品側の認証禁止を変更しない。
4. 期限を終えた作業範囲確認3件だけを削除または縮小し、固定基準再生成、egress 6 file、使い捨てGitの
   禁止path検出を恒久検査として残す。
5. 試験3 fileだけのRED commitと、RED試験を変更しないGREEN commitを分ける。

## 2. 固定した変更範囲

REDで変更できるのは次の3 fileだけである。

- `tests/test_policy_test_runner.py`
- `tests/test_claude_bootstrap_entrypoints.py`
- `tests/test_pilot_collaboration_entrypoints.py`

GREENで追加変更できるのは次の3 pathだけである。RED commitの試験は変更しない。

- `config/development-test-runner.json`
- `tools/development/policy_test_runner.py`
- `records/development/2026-08-12-stage2-official-test-entry-restoration-evidence-v1.md`

## 3. 承認に含めない事項

- 第2段完了、テストコード管理候補の最終採用、第2段採用表の更新。
- Python 3.13移行、Python、仮想環境、依存関係、`pyproject.toml`の変更。
- 未修正の重大な欠陥12件、外部送信、認証、応答解析、配置、第3段以降。
- 3件以外の既存試験変更、skip、xfail、試験選択除外、結果記録の項目変更。
- push、tag、履歴書換え、管理範囲外への恒久書込み。

## 4. 停止条件

作業票第7.1節をそのまま適用する。特に、6名以外の環境変更、3件以外の既存試験変更、固定した15件以外の
新しい失敗、Pythonまたは結果記録項目の変更が必要になった時点で停止し、利用者へ三択を返す。

## 5. 次の一作業

試験3 fileだけを変更する。公式試験入口が6名を子処理へ渡す現行不具合を、新しい受入試験が修正前実装で
失敗することを単独実行で確認する。同時に、期限付き3件を作業票どおり恒久検査から分離する。

REDの失敗理由と、同じfile内の他試験が成功することを確認した後、試験3 fileだけを意味的に完結した
RED commitへ固定する。承認済みGREENへ進む前に作業単位移行検査を行う。
