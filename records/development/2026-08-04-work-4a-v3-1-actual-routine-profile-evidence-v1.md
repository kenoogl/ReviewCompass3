# Work 4A v3.1 Actual Routine Profile Evidence v1

## 承認

`DEC-WORK4A-REBUILD-DESIGN-004`の自律実行範囲。実sourceでRoutine Profileを生成し、
機械抽出結果を提示するところまでを実施した。LLMによるDisposition Proposalは実施していない。

## project内に作成したartifact

| path | content_digest |
| --- | --- |
| `.reviewcompass/policies/work4a-freshness-policy-v2.json` | Policy v2。三軸語彙、痕跡語彙と検出規則、group条件文法、抽出規則v2を固定 |

Policy v1は履歴として残し、書き換えていない。

## 外部DATA_ROOTに作成したrecord

data root：`/Users/keno/.reviewcompass3/projects/reviewcompass3/development/data`

| 相対path | 内容 |
| --- | --- |
| `work4a/observations/6e8fae1323a61690bd63a3b1cbf21fe0dce0f827fc376177eaaa738da6f9f345.json` | 再採取した観測 |
| `work4a/profiles/5d1f174fc2941a7ee57ce27663c07030e21db0db88d4429b63b7806773e47db6.json` | Routine Profile |

`ee12e9b`で固定した旧Observationと旧Candidate Runは書き換えていない。

## 観測

| 項目 | 値 |
| --- | --- |
| `source_content_id` | `f35d5312f9e5d0412b9839415546ec90ece87a00df688a1d3746b2d141682110` |
| `snapshot_id` | `6e8fae1323a61690bd63a3b1cbf21fe0dce0f827fc376177eaaa738da6f9f345` |
| `profile_run_id` | `5d1f174fc2941a7ee57ce27663c07030e21db0db88d4429b63b7806773e47db6` |
| 抽出規則version | 2 |

`source_content_id`が前回（`6c0d9ab2…`）と異なるのは、v3.1実装で`tools/`配下のsourceが
変わったためである。universeは同一（`SRCU-WORK4A-TOOLS-PY-V1` v1）。

## 機械抽出の結果

routine 966件。前回の候補922件との差は、method 20件とnested function 3件の収録、
およびv3.1実装で追加したroutineによる。

| symbol_kind | 件数 |
| --- | --- |
| function | 668 |
| class | 275 |
| method | 20 |
| nested_function | 3 |

除外した構文単位（件数を記録し、黙って落としていない）：

| construct | 件数 | 理由 |
| --- | --- | --- |
| import | 488 | routineではない |
| module_level_assignment | 226 | routineではない |
| lambda | 70 | 安定した識別子を持たない |

`responsibility_class`の機械初期値：

| 値 | 件数 |
| --- | --- |
| `ownership_unclear` | 354 |
| `public_responsibility` | 328 |
| `implementation_detail` | 284 |

構文的痕跡（検出できたものだけ。未検出は副作用なしを意味しない）：

| marker | 件数 |
| --- | --- |
| 痕跡なし | 817 |
| `file_read` | 108 |
| `file_write` | 49 |
| `process_spawn` | 16 |
| `environment` | 1 |
| `network` | 0 |
| `global_mutation` | 0 |

規模：行数の中央値10、最大1181、5行以下287。docstringあり136。被参照0件421。

構造一致group：653 group。うち2件以上を含むのは59 groupで、372 routineが属する。
上位は例外classの空定義85件、dataclass様の小さなclass 28件と28件、23件、22件などである。
これらは構文が一致しただけであり、統合の結論ではない。

## 判断材料として見えたこと

- 例外classの空定義85件が同一構造groupにまとまる。group条件
  `structural_match_group_id equals STRUCT-MATCH-0000`で一括処置の候補になる。
- 痕跡なしが817件と多い。これは副作用が無いことの証明ではなく、構文一致で検出できなかった
  というだけである。判断根拠に使う場合はこの限界を明示する必要がある。
- 「痕跡2種以上かつ100行以上」に該当するroutineは0件であった。設計§9.2で例示した
  巨大かつ複数痕跡群は、現行sourceには存在しない。
- classの275件中178件が`ownership_unclear`初期値である。決定3（例外classは`ownership_unclear`）と
  被参照0件の規則が重なった結果である。

## Test

- v3.1 acceptance `21 passed`、v3 acceptance `22 passed`
- 全test：venv公式runner `702 passed`、Python 3.9.6、pytest 8.4.2、fallback false

## 現在の停止点

LLMによるDisposition Proposalの生成は実施していない。別承認を待つ。
Candidate Runの規則v2での再生成、Attestation、Operational Human Decision、Entry、Relation、
Baselineの作成も行っていない。
