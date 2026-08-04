# Work 4A v3.2 Actual Routine Profile v2 Evidence v1

## 承認

`DEC-WORK4A-REBUILD-DESIGN-005`の実施範囲。実sourceからProfile v2をnew-onlyで生成し、
機械抽出結果を提示するところまでを実施した。LLM生成は行っていない。

## 外部DATA_ROOTに作成したrecord

data root：`/Users/keno/.reviewcompass3/projects/reviewcompass3/development/data`

| 相対path | 内容 |
| --- | --- |
| `work4a/observations/7d9522de102de0a7f84ade4f1ef95487a3852f30c83f27129832a9d83dc0dbc4.json` | 再採取した観測 |
| `work4a/profiles/78f8b8733b3baf1bfe8bc46efaf77c498cf362eb1a44086d32f1f39efabef8e4.json` | Routine Profile v2 |

Profile v1（`5d1f174f…`）、既存Observation、既存Candidate Runは変更・削除・移動していない。

## 観測

| 項目 | 値 |
| --- | --- |
| `source_content_id` | `bfe081c2c865043c3db019bae689902084908679b221609c1e1cd6053f61e345` |
| `snapshot_id` | `7d9522de102de0a7f84ade4f1ef95487a3852f30c83f27129832a9d83dc0dbc4` |
| `profile_run_id` | `78f8b8733b3baf1bfe8bc46efaf77c498cf362eb1a44086d32f1f39efabef8e4` |
| `schema_version` | 2 |
| `extraction_rule_version` | 3 |

## 件数とcoverage

routine総数 **989**（v3.1のProfile v1は966。差は本作業でのsource増加による）。

除外した構文単位：import 489、`module_level_assignment` 241、lambda 71。件数と理由を記録している。

| feature | coverage |
| --- | --- |
| 直接callee 1件以上 | 560（56%） |
| 直接caller 1件以上 | 704（71%） |
| 未解決呼出を持つroutine | 244／未解決呼出の合計 327 |
| `raise`名あり | 403（40%） |
| `except`名あり | 176（17%） |
| bare except | 0件 |
| Test直接参照あり | 386（39%）／参照path延べ 1352 |
| 意味的比較候補あり | 987（99%）／上限10件到達 952／平均 9.84 |

## 指標の分布

`complexity_signal`（確認優先度。`split`の決定ではない）

| 値 | 件数 |
| --- | --- |
| `low` | 559 |
| `medium` | 325 |
| `high` | 105 |

`public_api_signal`（公開契約の証明ではない）

| 値 | 件数 |
| --- | --- |
| `medium` | 520 |
| `low` | 426 |
| `high` | 43 |

内訳の入力：`__all__`掲載 0件、CLI構文marker 40件、cross-package direct callerを持つroutine 6件。

## 読み取れること

- `__all__`を定義しているmoduleが現行sourceに無く、公開性の判定はCLI markerと
  cross-package呼出だけに依存している。`public_api_signal`が`high`の43件は、
  ほぼCLI入口である。この指標だけで公開契約を断定しない前提が、実データでも重要である。
- 未解決呼出327件は、別名import、動的属性、`getattr`／`globals`経由の呼出である。
  解決済みと偽装せず件数として残した。呼出関係の網羅を主張しない。
- bare exceptは0件であった。
- 意味的比較候補は99%のroutineで上限近くまで埋まった。現行sourceは構造の似た小さなroutineが
  多いため、候補集合は「読む対象を絞る」用途としては粗い。LLMへ渡す際は`complexity_signal`や
  `structural_match_group_id`との併用が要る。この観察はHuman判断の材料であり、
  設計の変更を伴わない。

## Test

- v3.2 acceptance `11 passed`、v3.1 `21 passed`、v3 `22 passed`
- 全test：venv公式runner `724 passed`、Python 3.9.6、pytest 8.4.2、fallback false

## 現在の停止点

LLMによるDisposition Proposalの生成は実施していない。別承認を待つ。
Operational Human Decision、Entry、Relation、Baseline、Attestationも作成していない。
