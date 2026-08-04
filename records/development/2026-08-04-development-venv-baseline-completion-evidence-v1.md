# Development venv Baseline Completion Evidence v1

- Evidence ID：`RC3-DEVELOPMENT-VENV-BASELINE-2026-08-04-V1`
- status：`verified / completed`
- scope：Work 4／4A開始前の独立した開発環境baseline

## 固定した境界

- `.venv/`はbootstrapが機械作成し、Git管理対象外とする。
- 開発用Pythonは`.venv/bin/python3`だけを公式Test runnerに使用し、system Pythonへfallbackしない。
- Pythonは`>=3.9,<3.10`、pytestは`8.4.2`に固定する。
- pip、setuptools、wheelを先に固定版へ更新し、同じlockを使った
  `--no-build-isolation` editable installを行う。
- 依存lockのSHA-256不一致、Python不適合、pytest不適合、必須package不適合では停止する。
- `.venv`と`*.egg-info`はsource state Digestから除外し、端末ローカル生成物でTest Evidenceを変化させない。

## 固定成果物

- `config/development-environment.json`：SHA-256
  `d310298bfb35c24c1ec5b8b2c2c4f73d8d19d68e2874e88814100da35166792d`
- `constraints/development-py39.txt`：SHA-256
  `1307ed9075ddcc312697d18114b8f5b594796f047ab5df586e7a7b448058c8f2`
- `tools/development/bootstrap_environment.py`：SHA-256
  `3f826d4dc8c8e1c35fbca3a052850e0eccbf0b45fa059c5a77bf65adc616c701`
- `config/development-test-runner.json`：SHA-256
  `179382b8462b92d502399ede89f4fbc110095cc353e530584f1f580b2e067208`
- RED receipt：`records/development/2026-08-04-development-venv-red-test-receipt-v1.json`、
  SHA-256 `c6998b6496706ef9b524804d6899b07e948c1543f1ee9ed3742d445d35f7ae11`
- TODO回帰RED receipt：`records/development/2026-08-04-development-venv-red-test-receipt-v2.json`、
  SHA-256 `05ab9f5582aa5a97623b6b1a200954b315e76f7028d1260a22172a4fb9922d84`
- GREEN receipt：`records/development/2026-08-04-development-venv-green-test-receipt-v1.json`

## 検証結果

1. build toolchain固定前のAcceptance Testは3件失敗し、固定不足と生成物Digest混入を検出した。
2. 最初のvenv全Testは`647 passed, 5 failed`だった。5件はすべて、既存実装がimportする
   `PyYAML`がproject依存へ未宣言だったためである。
3. `PyYAML>=6,<7`を実行時依存、`PyYAML==6.0.3`をlockとbootstrap検証へ追加した。
4. 関連Testは`22 passed`、公式全Testは`.venv/bin/python3 -m pytest -q`で
   `652 passed`、fallback `false`となった。
5. TODO更新後の再実行では、Pilot Testが過去時点の参照数`4`を固定していたため`1 failed`となった。
   全参照のDigest照合を維持し、現行TODOから参照数を機械算出する回帰Testへ修正した。
6. 回帰Testの初稿では非ASCII bytesリテラルを手書きし、collection errorになった。UTF-8 encodeを
   明示する形へ修正した。これは文章以外の定型変換を手作業にしたことによる手戻り候補である。
7. TODOから生成中のGREEN receiptを直接参照すると、Test終了後にreceiptを書くrunnerとの循環で
   `TODO reference is unresolved`になった。TODOは固定Completion Evidenceを参照し、生成中outputを
   直接参照しない境界へ修正した。

## 判断

system Pythonに偶然存在するpackageへ依存していた問題は、venvを手修復せず、依存宣言、exact lock、
bootstrap検証の三箇所を同時に固定して解消した。旧system PythonのTest receiptは削除せず履歴として保持する。
本作業は製品Work 4／4Aの着手または順序変更を意味しない。
