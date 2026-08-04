# Work 4A v1 Revert Map v1

## Purpose

Work 4A v1の局所patchをhistoryを書き換えず撤回した実施範囲を、commit subjectではなくpathとsource commit群で示す。

| revert commit | 戻した対象 | 主な対象path | 保持したもの |
| --- | --- | --- | --- |
| `3bca31c` | `86726dd`から`90bc6fe`までのWork 4A source/index/candidate/ledger/policy patch群。ただしLayout v3三commitを除く | `tools/development/source_symbol_index.py`、`tools/development/reusable_routine_ledger.py`、関連test、`.reviewcompass/reuse/reusable-routine-ledger/`、Work 4A record、identity preflight template | `e215cea`、`f53eb51`、`6258aaf`のProject-first Runtime Layout v3 |
| `474a0d5` | `44fc5db`のSource Symbol Index RED test | `tests/test_source_symbol_index.py`、対応RED Evidence | Layout v3 |
| `7963039` | `2a23117`のSource Index開始境界 | Work 4A start boundary Evidence、旧TODO/checklist表示 | Layout v3 |

`04060d`から`90bc6fe`の各source commitは、上表の最初のentryに含む。`e215cea`、`f53eb51`、`6258aaf`は
範囲中に存在したが、独立承認済みdeployment/layout基盤のため意図して保持した。

外部`DATA_ROOT`への削除、移動、書込みはrevert commandの対象にしていない。過去の外部観測は保持するが、v2の
正本・freshness根拠には使わない。
