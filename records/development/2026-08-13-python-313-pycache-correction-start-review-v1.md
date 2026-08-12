# Python 3.13 bytecode cache補正 開始前レビュー v1

- 日付：2026-08-13
- 対象：`docs/development/2026-08-13-python-313-development-environment-migration-bootstrap-work-ticket-v3.md`
- 対象SHA-256：`8a9b5d1a04428ebf906b060a397ac2934d4dd408d06bf608542aa818af9d821d`
- 対象commit：`f015c75`
- 先行版SHA-256：`1d5836efed25fd049ce35772c6de60aaf4e40a952bfe8c580e7004a5ab5c5d16`
- レビュー範囲：v2から変わった第2節から第6節だけ
- 判定：`修正要`

## 1. 固定材料の照合

【実測】指定された固定材料を再読込し、SHA-256を機械照合した。

| 材料 | SHA-256 |
| --- | --- |
| `tools/development/policy_test_runner.py` | `d749685737f09c301cfb9f118a8fe4688ad1d864d47f7c7e1ff9ef44bd7df076` |
| `tests/test_policy_test_runner.py` | `0319df8f16ae76353e67b33013371cb28a0e1c7dd1b07882760d17bf9a17df7f` |
| `tests/test_task_python_cache.py` | `10550c3d453dbd741f6c4eefce4c02dee301417fd0b82c55731cd38559f62901` |
| `tools/development/claude_implementation_route.py` | `a931039f81b4831f2a397646bddc13681b0c45d0a12c9a6459fce3d83310272e` |
| `/private/tmp/reviewcompass-stage2-python313-migration-green-v1.json` | `f537dae22206f325967324388fda62a72dba4c4cc249ae080763f04b91d7ef36` |
| `/private/tmp/reviewcompass-stage2-python313-migration-green-v2.json` | `eeb4ed725095b7c569b9fc222c14ef5f23ae2579193ee3a8a11e9a1cc0c4fd42` |

【実測】二つの結果記録は作業票の記載と一致した。v1はPython 3.13.14で1件失敗、
1,735件成功、終了コード1、v2は6件失敗、1,730件成功、終了コード1、いずれもpytest 8.4.2、
fallbackなしだった。

## 2. 中心判断と反証

【判断】子のpytestへproject外の一時`PYTHONPYCACHEPREFIX`を渡す2 path案は、結果記録v2の
6失敗を直接除く方向として妥当である。親環境を変更せず、一時directoryの存在期間と終了後の削除を
既存の偽processで確認するREDも作成可能である。既存のbytecode cache作成試験は子processの環境指定を
自ら上書きするため、作業票が想定する一時pathと両立する。

【実測】一方、中心判断への反証として、追跡済みfileだけから作った使い捨てのrepository複製で、
`PYTHONPYCACHEPREFIX`と`PYTHONDONTWRITEBYTECODE`を外し、正式`.venv`のPython 3.13.14で次を実行した。

```text
.venv/bin/python3 -m tools.development.policy_test_runner --help
```

終了コードは0だったが、子のpytestを起動する前に次の2 fileがproject内へ生成された。

```text
tools/development/__pycache__/policy_test_runner.cpython-313.pyc
tools/development/__pycache__/pytest_summary.cpython-313.pyc
```

【実測】別の使い捨て複製でrunner起動時に`-B`を付けた対照実験は終了コード0で、project内に
`__pycache__`を生成しなかった。

```text
.venv/bin/python3 -B -m tools.development.policy_test_runner --help
```

【判断】`tools/development/policy_test_runner.py`内で子processの環境を設定する時点では、runner自身と
`pytest_summary.py`の読込みが既に終わっている。このため、現v3の2 path実装だけでは第6節の
「実行後にproject内へ未追跡`__pycache__`が残らない」を満たせない。

## 3. 止める指摘

1件。公式runnerの起動側で、runner自身のbytecode cache生成を止める条件が不足している。

最小の修正方向は、作業票第6節の公式commandだけを次の形にすることである。

```text
.venv/bin/python3 -B -m tools.development.policy_test_runner \
  --suite full \
  --receipt /private/tmp/reviewcompass-stage2-python313-migration-green-v3.json
```

子のpytestへproject外の一時`PYTHONPYCACHEPREFIX`を渡す既存の2 path案は維持する。新設定、結果記録項目、
他の環境変数、`.gitignore`、Git検査、task cache、fixture全般へは広げない。

## 4. 報告不一致

0件。対象SHA、固定材料SHA、二つの結果記録の版・件数・終了コードは申告と一致した。

## 5. 未実施

v2で確認済みのHomebrew取得、依存固定、正式`.venv`の退避・復旧、設定変更は再レビューしていない。
製品code、試験、設定、作業票、結果記録は変更していない。実装、全試験、外部送信、Claude送信、
第2段完了、第3段は実施していない。
