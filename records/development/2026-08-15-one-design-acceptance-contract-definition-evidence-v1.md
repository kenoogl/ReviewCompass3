# 一件の設計・受入条件照合 契約定義Evidence v1

- 実施日：2026-08-15
- 対象：候補2「G08の設計・受入条件照合」
- 作業範囲：作業契約候補の定義だけ。実装、既存試験変更、契約採用は行わない
- 観測開始commit：`40b399d`

## 1. 既存対象の機械抽出

目録のG08節から次の2 pathを抽出した。

1. `tools/design/bootstrap_conformance.py`
2. `tools/design/design_contract.py`

【実測】2 fileは合計2,471行だった。SHA-256は次のとおり。

| path | 行数 | SHA-256 |
| --- | ---: | --- |
| `tools/design/bootstrap_conformance.py` | 898 | `100d46a4013c3cea3981d6a665d8cfda5f372d2a6e70ccc5fd3fde346bb58fcb` |
| `tools/design/design_contract.py` | 1,573 | `4678b9e16a5e4b02b3e065ab69c94ffacc10a975986c2d0c238039ea02ad3792` |

関連試験は次の2 fileだった。

1. `tests/test_bootstrap_conformance.py`
2. `tests/test_design_contract.py`

## 2. 現在の働き

【実測】`design_contract.py`は、設計、受入試験、境界、接続面、状態遷移、通信手順、失敗経路を検査する。
`bootstrap_conformance.py`は、要求と設計の対応、実装・試験証拠、未充足、依存、固定commitの内容を検査する。

【実測】`bootstrap_conformance.py`の645行以降は、固定commitの内容確認に`subprocess.run`を使う。
既存2 pathには、利用者が設計JSON一件と受入条件JSON一件を安全に読み、対応・欠落・矛盾だけを返す正式な
製品命令入口はない。

## 3. 反証と試験

### 3.1 既存関連試験

単独command：

`.venv/bin/python3 -m pytest -q tests/test_bootstrap_conformance.py tests/test_design_contract.py`

- 終了コード：0
- 結果：31件成功
- 失敗：0件

### 3.2 目録観測後の既存G08差分

単独command：

`git diff --exit-code 66d608e5b5d605ddaf387bbd75a507ac934800c6 -- tools/design/bootstrap_conformance.py tools/design/design_contract.py tests/test_bootstrap_conformance.py tests/test_design_contract.py`

- 終了コード：0
- 差分：0

【実測】「既存G08をそのまま使えば狭い製品処理になる」という見方への反証として、公開関数、関連試験、
外部process呼出しを確認した。既存処理は構造化された広い第5段検査であり、一件用の安全なfile入口、固定した
欠落・矛盾比較、入力値を出さない製品表示を一組では提供していない。

## 4. 定義した契約候補

- path：`records/task-contract/2026-08-15-one-design-acceptance-conformance-candidate-v1.md`
- SHA-256：`1640ebbfd1ff5d01e4410b43de6c503da8dd0b402bc47d4f96534cbcdf71f52f`
- 推奨案：案C。明示的な設計事実と受入条件だけを比較する狭い専用処理
- 実装状態：未開始

## 5. 判断

【判断】候補v1は、目的、入力、期待結果、範囲外、許可操作、停止条件、確認方法、3案比較を一件分に固定した。
採用または実装へ進む前に、別の実行単位による読取り専用の定義反証が必要である。

【未実施】独立定義確認、契約採用、実装開始、コード・試験・配布設定変更、外部送信、保存は行っていない。
