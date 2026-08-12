# 第2段 公式試験入口の正常化 軽量作業票 v2

- 作業票ID：`BTW-STAGE2-OFFICIAL-TEST-ENTRY-RESTORATION-002`
- 状態：`approved_scope_extension_pending_independent_review`
- 置換対象：`BTW-STAGE2-OFFICIAL-TEST-ENTRY-RESTORATION-001`
- v1：`docs/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-work-ticket-v1.md`
- v1 SHA-256：`5af82a43c618481e08abf398abdc50d289388eb1388da9aa58ae0ee9a4d1d00f`
- 基準コミット：`354c57e1d7dd28eaa6b2e271ea3dae60ce949720`
- 危険度：`high`
- 作業担当：操縦役が兼務できる。
- 開始前レビュー担当と完了レビュー担当：作業担当とは異なる実行単位と会話状態を使う。

## 1. 目的

v1のRED commit後に公式全試験で見つかった、要求と試験の対応表に残る削除済み試験名一件を解消する。
v1が承認した目的、6変数の環境分離、期限付き3件の整理、Python 3.13との分離は変えない。

本v2は、v1の変更可能範囲へ`tests/test_pilot_collaboration.py`一件を加え、同file内の`TRACEABILITY`に
残る削除済み試験名を3か所から除く変更だけを追加承認範囲とする。それ以外はv1をそのまま継承する。

## 2. 入力と根拠

| 入力 | SHA-256 | 用途 |
| --- | --- | --- |
| v1作業票 | `5af82a43c618481e08abf398abdc50d289388eb1388da9aa58ae0ee9a4d1d00f` | 元の目的、範囲、停止条件、完了条件 |
| RED commit | `354c57e1d7dd28eaa6b2e271ea3dae60ce949720` | 期限付き試験名を除いた試験3 file |
| `tests/test_pilot_collaboration.py` | `8157394b5d40222196253dba5aaf2a645282864a4860fb2a5efc108c2b2dcb22` | 削除済み試験名を参照する対応表 |
| 失敗結果記録 | `49c87a585b2f203ad8d8a7964cfbb19405ffaf55b973894679ad6c8b35296efe` | 1,735件中1件失敗の機械証拠 |

【実測】公式全試験は1,734件成功、1件失敗、終了コード1だった。唯一の失敗は
`tests/test_pilot_collaboration.py::test_requirement_traceability_covers_all_26_ids`であり、対応表が
`test_change_scope_contains_only_v6_allowlisted_paths`を参照する一方、その試験はRED commitで期限付き検査として
削除済みだった。

【記録】利用者は2026-08-12、事象、原因、未コミット状態と三択を提示された後、推奨案
「今対処する」を`1`で選択した。

## 3. 作業範囲と対象外

v1の変更可能path 6件へ、次の一件だけを追加する。

```text
tests/test_pilot_collaboration.py
```

変更できる箇所は`TRACEABILITY`の次の3 keyにある削除済み試験名だけである。

- `NG-PC-007`
- `ST-PC-001`
- `OUT-PC-006`

`NG-PC-007`と`ST-PC-001`は、既に同じ組へ含まれる次の2試験だけを残す。

- `test_change_scope_rejects_forbidden_commit_before_later_allowed_commit`
- `test_change_scope_does_not_hide_code_inside_handoff_directory`

`OUT-PC-006`は、削除済み試験名を上記2試験へ置き換える。要求ID、要求本文、対応表の他key、試験関数、
製品コードは変更しない。

次は対象外とする。

- 削除済み試験の復活、過去の許可path集合の更新、新しい試験の追加。
- `TRACEABILITY`の3 key以外、要求ID、v6指示書、過去記録の変更。
- 保持中の`config/development-test-runner.json`と`policy_test_runner.py`の実装内容変更。
- v1が対象外としたPython 3.13、重大な欠陥12件、外部送信、第2段完了。

## 4. 期待する成果

1. `tests/test_pilot_collaboration.py`の対応表3か所だけが、実在する恒久試験2件を参照する。
2. `test_requirement_traceability_covers_all_26_ids`が成功する。
3. 対応表修正を試験だけの補正commitへ固定する。
4. その後、保持中のGREEN実装へ戻り、v1の関連試験と公式全試験を実行する。
5. v1のEvidenceへ、停止事象、追加承認、v2、補正commit、修正前後の結果を含める。

## 5. 機械確認

対応表変更後、次を単独実行する。

```text
.venv/bin/python3 -m pytest -q \
  tests/test_pilot_collaboration.py::test_requirement_traceability_covers_all_26_ids
```

さらに、対応表の3 keyをPythonの構文木から機械抽出し、削除済み試験名0件、残した2試験名だけであることを
確認する。`git diff --check`、変更path、変更行、明示pathだけのstage、commit後の再読込みを確認する。

補正commit後はv1第5.2節へ戻り、関連試験4 file、開発環境の整合試験、公式全試験、独立収集件数、
結果記録を確認する。

## 6. レビューで判断する事項

開始前レビューは、追加pathが一件、変更箇所が対応表3 keyだけであること、残す2試験が実在し成功すること、
要求本文や試験関数を変えないこと、v1の安全境界を弱めないことを確認する。

完了レビューはv1と本v2を一続きで読み、RED commit、補正commit、GREEN commit、公式全試験、
変更path、利用者承認境界を一回だけ確認する。

## 7. 停止条件と完了条件

次の場合は停止する。

- 対応表3 key以外を変更しないと試験が成功しない。
- 残す2試験が要求との対応を維持できないと判明した。
- 新しい試験、要求本文、製品コード、他の既存試験の変更が必要になった。
- 公式全試験で、今回の対応表1件以外の新しい失敗が見つかる。

完了条件は次のとおりである。

- 対応表補正が一file、3 keyだけのcommitへ固定される。
- 対応表試験と残す2試験が成功する。
- v1が固定したRED試験を補正commitとGREENで変更しない。
- v1の関連試験、開発環境の整合試験、公式全試験がすべて終了コード0になる。
- Evidenceと独立完了レビューがv1とv2の固定材料へ結び付き、完了レビューが`verified`となる。

その後も、第2段完了とPython 3.13移行は別の利用者判断とする。
