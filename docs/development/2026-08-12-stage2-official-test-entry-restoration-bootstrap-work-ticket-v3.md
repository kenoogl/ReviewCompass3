# 第2段 公式試験入口の正常化 軽量作業票 v3

- 作業票ID：`BTW-STAGE2-OFFICIAL-TEST-ENTRY-RESTORATION-003`
- 状態：`awaiting_scope_correction_review`
- 置換対象：`BTW-STAGE2-OFFICIAL-TEST-ENTRY-RESTORATION-002`
- v1 SHA-256：`5af82a43c618481e08abf398abdc50d289388eb1388da9aa58ae0ee9a4d1d00f`
- v2 SHA-256：`6cbb24eae0397198f48bb25ba6bd56874c020119a8f443b6d5251ca04266d018`
- v2開始前レビュー：`records/development/2026-08-12-stage2-official-test-entry-restoration-scope-extension-start-review-v1.md`
- v2開始前レビューSHA-256：`76fe16bda12de34727840cffde88b706e6ad56591e3fc2ce7641c2c6e375f133`
- 基準コミット：`aa8ed0ededac8acec2b431747ee7d91b98e546bb`
- RED commit：`354c57e1d7dd28eaa6b2e271ea3dae60ce949720`
- 危険度：`high`

## 1. 目的

v2開始前レビューの指摘`SR-SE-001`を解消し、削除済みの期限付き試験名を要求と試験の対応表から除く。
`OUT-PC-006`を変更範囲試験へ誤って付け替えず、Gitの書込み禁止を機械で検査する一件の恒久試験と、
完了時のGit・外部操作Evidenceを合わせて確認する。

v1の目的、6変数の環境分離、期限付き3件の整理、RED commit、保持中のGREEN実装は変更しない。

## 2. 入力と根拠

| 入力 | SHA-256 | 用途 |
| --- | --- | --- |
| v2開始前レビュー | `76fe16bda12de34727840cffde88b706e6ad56591e3fc2ce7641c2c6e375f133` | `OUT-PC-006`の虚偽対応を止めた指摘 |
| `tests/test_pilot_collaboration.py` | `8157394b5d40222196253dba5aaf2a645282864a4860fb2a5efc108c2b2dcb22` | 対応表、process検査、Git呼出し試験 |
| `tools/development/pilot_collaboration.py` | `86d7c6b3604e8a61976b9e793255dee44d8578d006672271a2e901b2d81b3eb6` | 現在の`_run_git`呼出し対象 |
| RED commit | `354c57e1d7dd28eaa6b2e271ea3dae60ce949720` | 修正前後を区別する固定試験 |
| 失敗結果記録 | `49c87a585b2f203ad8d8a7964cfbb19405ffaf55b973894679ad6c8b35296efe` | 対応表の未定義参照1件 |

【実測】現在の`_run_git`呼出しは`ls-tree`、`show`、`cat-file`の3件で、すべてGitの読取り操作である。
同じ抽出へ`push`呼出しを与える反証は違反として検出できた。現行の`_process_policy_violations`だけでは、
直接のliteral配列`git push origin main`を違反0で受理する。

## 3. 作業範囲と対象外

v1の変更可能path 6件へ、次の一件だけを追加する。

```text
tests/test_pilot_collaboration.py
```

同fileでは次だけを変更できる。

1. `TRACEABILITY`の`NG-PC-007`と`ST-PC-001`から削除済み試験名を除き、既存の変更範囲試験2件を残す。
2. `OUT-PC-006`は、新設する`test_pilot_git_processes_are_read_only`一件へ対応させる。
3. `_process_policy_violations`が、直接のliteral配列によるGit書込み副commandを拒否する最小検査を加える。
4. `test_pilot_git_processes_are_read_only`は、`tools/development/pilot_collaboration.py`の全`_run_git`呼出しを
   構文木で列挙し、第二引数がliteralで、次の読取り専用3種類だけであることを確認する。

```text
ls-tree
show
cat-file
```

Git書込み副commandには少なくとも`push`、`commit`、`reset`、`tag`を含め、直接の
`subprocess.run`と`_run_git`呼出しの両方で拒否する反例を置く。

次は対象外とする。

- `tools/development/pilot_collaboration.py`その他の製品コードの変更。
- `TRACEABILITY`の3 key以外、要求ID、要求本文、他の試験関数の期待変更。
- Git操作を実際に行う試験、network、外部送信、push、履歴書換え。
- 「意味的に完結したcommit」と「作業担当が停止したこと」を自動試験だけで証明済みと扱うこと。
- v1が対象外としたPython 3.13、重大な欠陥12件、第2段完了。

## 4. 期待する成果

1. 対応表の未定義参照が0件となり、3 keyは意味に合う実在試験だけを参照する。
2. 新しい恒久試験が現在の製品コードを正常例として成功し、Git書込み4種の反例を拒否する。
3. 対応表と恒久試験の追加を`tests/test_pilot_collaboration.py`一件だけの補正commitへ固定する。
4. 保持中GREENへ戻り、v1の関連試験、開発環境整合、公式全試験を正常終了させる。
5. Evidenceで、`OUT-PC-006`のうち自動試験が確認するGit書込み禁止と、Git履歴・作業単位移行・
   push、履歴書換え、外部送信なしの事後確認を分けて記録する。

## 5. 機械確認

補正後、次をそれぞれ単独実行する。

```text
.venv/bin/python3 -m pytest -q \
  tests/test_pilot_collaboration.py::test_requirement_traceability_covers_all_26_ids
.venv/bin/python3 -m pytest -q \
  tests/test_pilot_collaboration.py::test_pilot_git_processes_are_read_only
.venv/bin/python3 -m pytest -q \
  tests/test_pilot_collaboration.py::test_process_policy_rejects_alias_popen_check_and_dynamic_routes
```

構文木から3 keyと定義済み試験名を再抽出し、未定義参照0件を確認する。反証用sourceは一時文字列だけとし、
実Git操作を行わない。補正commit後はv1第5.2節へ戻る。

## 6. レビューで判断する事項

v2への一回の修正後確認として、異なる実行単位が次を確認する。

- `SR-SE-001`を解消し、`OUT-PC-006`を自動試験だけで全確認済みと偽らないか。
- 読取り専用3種類が現在の製品コードと一致し、将来のGit書込み追加を失敗させるか。
- 製品コード、要求本文、RED、保持中GREENへ変更を広げないか。
- Evidenceによる事後確認と試験による静的確認の責務が分かれているか。

判定が`開始可`でも、新規恒久試験と対応表の意味変更は利用者の明示承認後にだけ実施する。

## 7. 停止条件と完了条件

次の場合は停止する。

- 製品コードまたは要求本文を変えないとGit書込み禁止を検査できない。
- `OUT-PC-006`全体を自動試験だけで合格扱いにしないと対応表を維持できない。
- 追加file一件、対応表3 key、新しい恒久試験一件、process反例以外の変更が必要になる。
- 公式全試験で、対応表未定義参照以外の新しい失敗が見つかる。

完了条件は次のとおりである。

- v2の`SR-SE-001`が一回の修正後確認で解消する。
- 補正commitは`tests/test_pilot_collaboration.py`一件だけである。
- 対応表試験、新しいGit読取り限定試験、既存process反例、残す変更範囲試験2件が成功する。
- v1のRED試験を変えず、関連試験、開発環境整合、公式全試験が終了コード0になる。
- Evidenceと独立完了レビューが、試験で確認した範囲と事後Evidenceを区別して`verified`となる。

その後も、第2段完了とPython 3.13移行は別の利用者判断とする。
