# Python 3.13 bytecode cache補正 修正後レビュー v1

- 日付：2026-08-13
- 対象：`docs/development/2026-08-13-python-313-development-environment-migration-bootstrap-work-ticket-v4.md`
- 対象SHA-256：`e2b753d882803c1c1f655d32a6c0202e89108f7af6b2b307c11206e5f2e8fcfe`
- 対象commit：`d98bb59`
- 先行版SHA-256：`8a9b5d1a04428ebf906b060a397ac2934d4dd408d06bf608542aa818af9d821d`
- 先行レビューSHA-256：`966613b7aee69c23c912793bb8adccb522c6e7bb2c669c92fb74e98dea026cd6`
- 確認範囲：先行レビューが止めた1件だけ
- 判定：`開始可`

## 1. 修正の照合

【実測】対象、先行版、先行レビューを再読込し、三つのSHA-256を機械照合した。申告値と一致した。

【実測】v4は公式runnerの起動commandだけを次へ変更した。

```text
.venv/bin/python3 -B -m tools.development.policy_test_runner \
  --suite full \
  --receipt /private/tmp/reviewcompass-stage2-python313-migration-green-v3.json
```

【実測】子pytest側の一時`PYTHONPYCACHEPREFIX`、実装対象の
`tests/test_policy_test_runner.py`と`tools/development/policy_test_runner.py`、設定、結果記録形式、
runner版、公式試験集合はv3から変えないと明記されている。

## 2. 止める指摘の解消

【記録】先行レビューの使い捨て複製では、通常起動がrunner自身と`pytest_summary.py`の`.pyc`を
project内へ2個生成し、`-B`付き起動は終了コード0で`__pycache__`を生成しなかった。

【判断】`-B`は公式runnerを起動するPython process自身のbytecode cache作成を、runnerのmodule読込み前から
止める。子pytestのcommandには`-B`を加えず、runner起動後にproject外の一時`PYTHONPYCACHEPREFIX`を渡すため、
子pytest内のcache出力検査も無効化しない。先行レビューが止めた1件を直接解消している。

## 3. 判定

`開始可`。止める指摘は0件、報告不一致は0件である。v3第5節のREDから、v4が維持する2 pathの範囲で
開始できる。

## 4. 未実施

新しい反証、一般化、別案、将来改善は追加していない。成果物、試験、実装、設定、結果記録は変更していない。
外部送信、Claude送信、全試験、第2段完了、第3段は実施していない。
