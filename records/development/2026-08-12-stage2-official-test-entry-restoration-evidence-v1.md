# 第2段 公式試験入口の正常化 実施Evidence v1

- Evidence ID：`EVD-STAGE2-OFFICIAL-TEST-ENTRY-RESTORATION-001`
- 作成日：2026-08-12
- 危険度：`high`
- 最終作業票：`docs/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-work-ticket-v4.md`
- 最終作業票SHA-256：`8f6632ec7754b48d88c661682c76d6c8de5ee56c5b9d2997341aa45f99131bc8`
- RED commit：`354c57e1d7dd28eaa6b2e271ea3dae60ce949720`
- 対応表補正commit：`48076c1b754ca09f061fa8a949600c1792cd563f`
- 状態：`awaiting_independent_completion_review`

## 1. 固定した承認と範囲

【記録】最初の作業票v1は、公式試験入口の子処理だけから認証・接続用の環境変数名6個を除外し、
期限を終えた変更範囲試験3件を恒久検査から分離する作業を定めた。独立開始前レビューは`開始可`、
止める指摘0件であり、利用者は開始を明示承認した。

| 種別 | path | SHA-256またはcommit |
| --- | --- | --- |
| 作業票v1 | `docs/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-work-ticket-v1.md` | `5af82a43c618481e08abf398abdc50d289388eb1388da9aa58ae0ee9a4d1d00f`、commit `120ec5e3922fa7aaa886cb3aca647e93943ef016` |
| 独立開始前レビュー | `records/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-start-review-v1.md` | `5dc23327f1072fd5438ca8ff2e2c22634f4257dd8970426471f69696be3a80ad`、commit `644391c3eeaae97f3b70593ef5827f071e664484` |
| 開始判断 | `records/development/2026-08-12-stage2-official-test-entry-restoration-start-decision-v1.md` | commit `b97c95771bb8e88d63db0f74fa85d74f124110c9` |
| 作業票v4 | `docs/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-work-ticket-v4.md` | `8f6632ec7754b48d88c661682c76d6c8de5ee56c5b9d2997341aa45f99131bc8`、commit `a3f0b8f8500250539be17544e5e40a9760199b12` |
| 範囲修正判断 | `records/development/2026-08-12-stage2-official-test-entry-restoration-scope-correction-decision-v1.md` | `ecf1f713e8c5925556f15f2e6f8a10d42d8cfd923751955f43449eb4890cb816`、commit `a3f0b8f8500250539be17544e5e40a9760199b12` |

【実測】最終的な実装側変更は`config/development-test-runner.json`と
`tools/development/policy_test_runner.py`、結果記録は本file一件である。試験側はRED commitの3 fileと、
利用者が追加承認した対応表補正commitの1 fileである。製品側の認証禁止処理、Python、依存関係、要求本文、
結果記録schemaは変更していない。

## 2. REDと期限付き試験の分離

【実測】RED commit `354c57e1d7dd28eaa6b2e271ea3dae60ce949720`は次の試験3 fileだけを変更した。

- `tests/test_policy_test_runner.py`：親環境に6名があっても全試験の子処理へ渡さず、それ以外の名前を残し、
  親環境を変更しない受入試験を追加した。
- `tests/test_claude_bootstrap_entrypoints.py`：固定commitから基準を再生成する恒久検査を残し、過去の一作業だけの
  先端差分制限2件を除いた。
- `tests/test_pilot_collaboration_entrypoints.py`：使い捨てGitで許可外pathを検出する恒久検査2件を残し、
  過去v6の許可pathだけへ現在の先端を制限する1件を除いた。

【実測】実装前に`.venv/bin/python3 -m pytest -q tests/test_policy_test_runner.py`を単独実行し、終了コード1、
新規受入試験1件失敗、先行9件成功を確認した。失敗理由は、旧runnerが6名すべてを子処理へ渡したことであり、
実装がない状態とある状態を区別した。RED commit後から本Evidence作成直前まで、上記3 fileの
`git diff 354c57e -- <3 file>`は空、終了コード0であり、GREEN中にRED試験を変更していない。

## 3. 途中停止と対応表補正

【実測】保持中GREENで最初に公式全試験を実行した結果は、1,735件中1,734件成功、1件失敗、終了コード1だった。
失敗は`test_requirement_traceability_covers_all_26_ids`だけで、REDで削除した期限付き試験名が
`TRACEABILITY`に残っていた。結果記録SHA-256は
`49c87a585b2f203ad8d8a7964cfbb19405ffaf55b973894679ad6c8b35296efe`である。

【記録】利用者はこの事象、原因、保留中GREENと三択を確認し、範囲内での対処を選んだ。作業票v2の独立開始前
レビューは、`OUT-PC-006`を変更範囲試験へ付け替えると要求との虚偽対応になるとして`修正要`を返した。
作業票v3の一回限り修正後確認は、自動試験と事後Evidenceの責務分離を妥当とした一方、別名、大域名前表、
無名関数を介した`_run_git`書込みを見逃すとして`修正要`を返した。いずれも指摘時点で対応表を変更せず停止した。

| 段階 | 固定物 | SHA-256 | commit | 結果 |
| --- | --- | --- | --- | --- |
| v2 | `docs/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-work-ticket-v2.md` | `6cbb24eae0397198f48bb25ba6bd56874c020119a8f443b6d5251ca04266d018` | `53a49d65526766ab9e723c748ff39f510c3045b3` | 範囲追加案 |
| v2レビュー | `records/development/2026-08-12-stage2-official-test-entry-restoration-scope-extension-start-review-v1.md` | `76fe16bda12de34727840cffde88b706e6ad56591e3fc2ce7641c2c6e375f133` | `aa8ed0ededac8acec2b431747ee7d91b98e546bb` | `修正要` |
| v3 | `docs/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-work-ticket-v3.md` | `7dc25beaf1af7bb22cbb9a0f1a4401babcda53cce66d6e5c7c19793b9ec4d6b1` | `df7966b3d72f2e65d7e63a73532fe8697d818a5e` | 責務分離案 |
| v3確認 | `records/development/2026-08-12-stage2-official-test-entry-restoration-scope-correction-review-v1.md` | `bd09762fa42fede4254cc7f34d878f6c199c2fee1e453aed54ab3f3baac6668f` | `2fbab75ef9c41b85cd66c44af4c8fb1271fa00de` | `修正要` |

【記録】利用者は、作業票v4が限定した同一file・同一新規試験内の間接呼出し反例を選択肢`1`で承認した。

【実測】対応表補正commit `48076c1b754ca09f061fa8a949600c1792cd563f`は
`tests/test_pilot_collaboration.py`一件だけである。`NG-PC-007`と`ST-PC-001`は既存の恒久的な変更範囲試験
2件を参照し、`OUT-PC-006`は新規`test_pilot_git_processes_are_read_only`を参照する。4試験fileを横断した
構文木照合は、参照32件、未定義0件だった。同file全体は65件成功、終了コード0だった。

【実測】新規試験は、現行製品codeの`_run_git`直接呼出しが`ls-tree`、`show`、`cat-file`の3件だけであることを
確認する。一時sourceによる`push`、`commit`、`reset`、`tag`、別名化、`globals()`経由、無名関数経由、
wrapper外の`subprocess.run`を違反として検出する。実Git書込みは実行していない。正常例の`ls-tree`を`push`へ
変えた追加反証も拒否し、確認命令は終了コード0だった。

## 4. GREEN実装

【実測】`config/development-test-runner.json`は`runner_version`を2へ上げ、次の6名だけを
`test_environment_excluded_names`へ順序付きで固定した。fallback禁止、結果記録必須、Python・pytestの版範囲、
suite commandは変更していない。

```text
ANTHROPIC_API_KEY
ANTHROPIC_AUTH_TOKEN
ANTHROPIC_BASE_URL
ANTHROPIC_FOUNDRY_API_KEY
ANTHROPIC_VERTEX_PROJECT_ID
AWS_BEARER_TOKEN_BEDROCK
```

【実測】`tools/development/policy_test_runner.py`は設定のkey集合、runner版2、上記6名の完全一致を検証する。
全試験を起動する直前に親環境を複製し、その複製から6名だけを除き、件数集計用の名前を加えて子処理へ渡す。
親処理の`os.environ`、Python・pytestの版確認処理、結果集計、結果記録、fallback禁止は変更していない。

## 5. 検査結果

合否は各commandの終了コードを単独で確認した。

| 目的 | command | 終了コード | 結果 |
| --- | --- | ---: | --- |
| 公式入口の受入 | `.venv/bin/python3 -m pytest -q tests/test_policy_test_runner.py` | 0 | 10 passed |
| 固定基準再生成 | `.venv/bin/python3 -m pytest -q tests/test_claude_bootstrap_entrypoints.py` | 0 | 8 passed |
| 変更範囲の恒久検査 | `.venv/bin/python3 -m pytest -q tests/test_pilot_collaboration_entrypoints.py` | 0 | 6 passed |
| 開発環境整合 | `.venv/bin/python3 -m pytest -q tests/test_development_environment.py` | 0 | 9 passed |
| 製品側実行器・6名除外時 | `env -u <6 names> .venv/bin/python3 -m pytest -q tests/test_claude_implementation_executor.py` | 0 | 28 passed |
| 製品側認証禁止 | `env ANTHROPIC_API_KEY=<test marker> .venv/bin/python3 -m pytest -q tests/test_claude_implementation_executor.py::test_executor_rejects_api_key_environment_before_any_process` | 0 | 1 passed |
| 対応表補正file全体 | `.venv/bin/python3 -m pytest -q tests/test_pilot_collaboration.py` | 0 | 65 passed |
| 公式全試験 | `env <6 names=test marker> .venv/bin/python3 -m tools.development.policy_test_runner --suite full --receipt /private/tmp/reviewcompass-stage2-test-entry-restoration-receipt-v2.json` | 0 | 1,736 passed、failed 0、errors 0、skipped 0、fallbackなし |
| 独立収集件数 | `.venv/bin/python3 -m pytest --collect-only -q` | 0 | 1,736 collected |
| 差分形式 | `git diff --check` | 0 | 指摘なし |

【実測】公式全試験は、親処理へ6名すべてを値`stage2-presence`で与えた状態で実行した。値は結果記録の
標準出力・標準エラーに現れず、結果記録は`status=passed`、`exit_code=0`、`fallback_used=false`、
Python 3.9.6、pytest 8.4.2、runner版2を記録した。独立収集件数と結果記録の総数は1,736件で一致した。

## 6. 最終内容識別値

| file | SHA-256 |
| --- | --- |
| `config/development-test-runner.json` | `9bdf7bcc3c9f84e471b0caf80b0d56111012d569e3e34dd79375b8c4df88f64d` |
| `tools/development/policy_test_runner.py` | `d749685737f09c301cfb9f118a8fe4688ad1d864d47f7c7e1ff9ef44bd7df076` |
| `tests/test_policy_test_runner.py` | `1dac011460f232efd990bb3e300bba4d624fa4f63419f422f2d6c48d6f7a13b4` |
| `tests/test_claude_bootstrap_entrypoints.py` | `fefe377808e47d3dae1330bf708fba951522a8a6010411af97756b5842b1a2a5` |
| `tests/test_pilot_collaboration_entrypoints.py` | `2f5044d4ffd2ada76efbd2e05d689be3ccf99915c744984e94bc15bb77c53bd1` |
| `tests/test_pilot_collaboration.py` | `678e35e434a52a11c87776395e52e775a918bd0d867d24fe709e5ad21144f646` |
| `tools/development/pilot_collaboration.py`（不変確認） | `86d7c6b3604e8a61976b9e793255dee44d8578d006672271a2e901b2d81b3eb6` |
| `/private/tmp/reviewcompass-stage2-test-entry-restoration-receipt-v2.json` | `08b15d46c4a36ddd6abe894d9e11e21b8a2385852548c44adf6b3df852616f0f` |

【実測】結果記録の`source_state_digest`は
`7596dfd8dbdb9fffdecd8babc7a107e8308cc589f12f05c1714c768735a04dde`である。結果記録取得後に新規作成したのは
本Evidenceだけであり、実行対象のcode、設定、試験は変更していない。結果記録自身はリポジトリ外にあり、
リポジトリへ追加していない。完了レビューでは、本Evidence追加後も§6の実行対象SHAが一致することを再確認する。

## 7. 判断、操作境界、未実施

【判断】元の15件失敗は、公式入口の子処理へ親の認証・接続名を渡していた12件と、期限を終えた変更範囲試験
3件に原因分離できた。6名だけの子処理環境分離と期限付き3件の整理により、製品側の認証禁止を緩めず、公式入口の
全試験を正常化できた。途中で見つかった対応表1件も、要求との虚偽対応を避け、読取り専用Git検査と事後Evidenceを
分離して解消した。

【記録】本作業でrepository本体に実行したGit変更操作は、明示pathの`git add`と通常commitだけである。
push、tag、amend、rebase、reset、force push、履歴書換え、外部送信は実施していない。試験内のGit操作は
一時directoryのfixture構築または読取り専用検査であり、製品codeによるGit書込みも行っていない。

【実測】対応表補正commit後の作業単位移行検査は、保留中GREEN 2 fileがある状態で
`completed_work_unit_uncommitted`、終了コード1を返した。

【判断】補正commit自体は一fileへ固定済みであり、検出された2 fileは既に開始済みで検証途中だった次のGREEN
作業単位であるため、検査器が両者を区別できなかった。本GREENとEvidenceを意味的に完結したcommitへ固定した後、
同検査を再実行する。

【未実施】本Evidenceは、独立完了レビュー、第2段完了、テストコード管理候補の最終採用、第2段採用表の更新、
Python 3.13移行、重大な欠陥12件の修復、外部送信、第3段以降を実施済みまたは承認済みとしない。

【次】設定、runner、本EvidenceだけをGREEN commitへ固定し、異なる実行単位が作業票v1からv4、RED、対応表補正、
GREEN、結果記録、対象外維持を一回の独立完了レビューで確認する。技術判定が`verified`でも、第2段完了と
次候補の採用は利用者が別に判断する。
