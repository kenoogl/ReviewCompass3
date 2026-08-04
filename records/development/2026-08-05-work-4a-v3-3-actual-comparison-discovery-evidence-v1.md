# Work 4A v3.3 Actual Comparison Discovery Evidence v1

## 承認

`DEC-WORK4A-REBUILD-DESIGN-006`の実施範囲。実sourceを再観測し、Profile v3と
Comparison Discoveryをnew-onlyで生成して機械抽出結果を提示するところまでを実施した。
LLM処理は行っていない。

## 再観測の理由

v3.3の実装で`tools/development/work4a_rebuild_v3.py`が変わったため、v3.2の
ObservationとProfile v2は実装前sourceを表す。設計§8に従い、同一source universeを
再観測してProfile v3を先に確定し、その後にDiscoveryを確定した。

## 外部DATA_ROOTに作成したrecord

data root：`/Users/keno/.reviewcompass3/projects/reviewcompass3/development/data`

| 相対path | 内容 |
| --- | --- |
| `work4a/observations/3ecb6a8b629706c990d47a7683d5beef238057274f7105fb916b75e45e308e5f.json` | 再観測 |
| `work4a/profiles/55fdacd5aec93a857b7c4900eb895488f77b5f57419c25af5309fdafe10ad8c1.json` | Routine Profile v3 |
| `work4a/comparison-discoveries/4dabb03b820bfbbac01c5d6e38e7e208f19703b617d7cd7376f38a82bea0293d.json` | Comparison Discovery |

Profile v1、Profile v2、既存Observation、既存Candidate Runは変更・削除・移動していない。
外部recordの絶対pathは本Evidenceへ保存せず、data root相対で示している。

## identity

| 項目 | 値 |
| --- | --- |
| `source_content_id` | `978da3d1bcc6a2f49cf22e90fa32799daf6f6a1da493397c91f3e0eaa16265a2` |
| `snapshot_id` | `3ecb6a8b629706c990d47a7683d5beef238057274f7105fb916b75e45e308e5f` |
| `profile_run_id` | `55fdacd5aec93a857b7c4900eb895488f77b5f57419c25af5309fdafe10ad8c1` |
| Profile `schema_version` / `extraction_rule_version` | 3 / 4 |
| `discovery_run_id` | `4dabb03b820bfbbac01c5d6e38e7e208f19703b617d7cd7376f38a82bea0293d` |
| Discovery `schema_version` / `grouping_rule_version` | 1 / 1 |

DiscoveryはProfileのrun ID、content digest、source content IDを固定参照する。
Profile側はDiscoveryを参照しない。

## 件数

- routine：1003（v3.2のProfile v2は989。差は本実装によるsource増加）
- group：682
- いずれかのgroupに属するroutine：994（1003件中）
- group memberの延べ数：4729

### basis_kind別group数

| `basis_kind` | group数 |
| --- | --- |
| `shared_direct_callee` | 286 |
| `shared_test_reference` | 119 |
| `shared_exception_contract` | 87 |
| `call_neighborhood` | 86 |
| `structural_exact_match` | 59 |
| `interface_shape_match` | 45 |

### presentation class別group数

| class | group数 |
| --- | --- |
| `focused`（2〜12） | 602 |
| `broad`（13〜50） | 72 |
| `mass`（51以上） | 8 |

### member_count分布

| 範囲 | group数 |
| --- | --- |
| 2 | 268 |
| 3〜5 | 249 |
| 6〜12 | 85 |
| 13〜50 | 72 |
| 51以上 | 8 |

中央値3、最大276。

## 最大groupの代表表示

全member一覧は外部recordにあり、本Evidenceへ複製しない。各group最大3件の代表だけを示す。

| group | 根拠 | member数 | class | 代表 |
| --- | --- | --- | --- | --- |
| `CG-IFACE-0001` | `interface_shape_match` | 276 | `mass` | `bundle_verification.py:BundleIntegrityError`、`:BundleVerification`、`:BundleVerificationError` |
| `CG-IFACE-0036` | `interface_shape_match` | 220 | `mass` | `bundle_verification.py:_safe_identifier`、`:_verify_bundle_integrity`、`closed_payload.py:_material_document` |
| `CG-IFACE-0030` | `interface_shape_match` | 118 | `mass` | `bundle_verification.py:_original_matches`、`closed_payload.py:_verify_closure`、`evidence_closure.py:_unique_identifiers` |
| `CG-STRUCT-0003` | `structural_exact_match` | 85 | `mass` | `bundle_verification.py:BundleIntegrityError`、`:BundleVerificationError`、`closed_payload.py:ClosedPayloadError` |
| `CG-EXC-0010` | `shared_exception_contract` | 79 | `mass` | `bundle_verification.py:_original_matches`、`material_bundle.py:_read_material`、`migration_candidates.py:_commit_tree_paths` |

## 読み取れること

- `mass` classは8 groupだけで、うち3件は`interface_shape_match`である。引数0〜1個の
  小さな関数やclass定義が同じ形に集まったもので、機械的共通性が広すぎることを示す。
  設計どおり削除せず保持し、LLMへ全member本文を渡さない対象とする。
- 全1003 routineのうち994件が少なくとも1 groupへ属する。v3.2の上限10件による
  切り捨ては解消され、group memberの延べ数は4729になった。
- `focused`が602 groupで全体の88%を占める。初期表示で全member IDと代表3件を渡せる範囲である。
- いずれの数値も機械的共通性の観測であり、`merge`や`split`の結論ではない。

## Test

- v3.3 acceptance `15 passed`、v3.2 `11 passed`、v3.1 `21 passed`、v3 `22 passed`
- 全test：venv公式runner `739 passed`、Python 3.9.6、pytest 8.4.2、fallback false
- 実データ生成後の再実行結果も同じである。

## 現在の停止点

LLMによるDisposition Proposalの生成、意味的比較、処置labelの提案は実施していない。別承認を待つ。
Operational Human Decision、Entry、Relation、Baseline、Attestationも作成していない。
