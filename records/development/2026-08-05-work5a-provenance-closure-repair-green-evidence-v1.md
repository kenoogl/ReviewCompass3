# Work 5A Provenance Closure Repair GREEN Evidence v1

## 対象

- 実装：`tools/task_contract/identity.py`、`tools/task_contract/execution.py`、`tools/task_contract/__init__.py`
- Test：`tests/test_first_review_task_contract_e2e.py`（38件）
- 正本設計：`docs/design/2026-08-05-work5a-provenance-closure-repair-proposal.md`
- 承認：`DEC-WORK5A-PROVENANCE-CLOSURE-REPAIR-001`（§6.3 案A）
- RED：`records/development/2026-08-05-work5a-provenance-closure-repair-red-evidence-v1.md`
- receipt：`records/development/2026-08-05-work5a-provenance-closure-repair-green-test-receipt-v1.json`

## 結果

- 対象test：`38 passed`（既存25件＋追加13件）
- 全test：venv公式runner `777 passed`、Python 3.9.6、pytest 8.4.2、fallback false

## 実装した形式

`provenance_verdict`から`edges`（`to`と`to_digest`の平坦な形）を廃止した。

| field | 内容 |
| --- | --- |
| `verified_nodes` | 9件。`node_role`、`record_kind`、`record_id`、`record_version`、`content_digest` |
| `verified_edges` | 8件。両端を`node_role`だけで指す。identityとDigestは`verified_nodes`が一元的に持つ |
| `closure` | `terminal_node_role: human_decision`、`self_edge_present: false`、`closed_by: accepted_artifact` |

**`provenance_verdict`自身を端点とするedgeを内容へ含めない。**閉包は`accepted_artifact`が担う。
同じrecordを二箇所へ書かないため、名前とDigestが別recordを指す不整合が構造から消えた。

## 検証規則

`validate_provenance_verdict`がV1〜V8を照合する。`verify_provenance`は生成時に自ら呼び、
`accept_artifact`も受理前に呼ぶ。**辺数だけでは判定しない。**

| 停止code | 条件 |
| --- | --- |
| `provenance_node_missing` | 必須nodeまたは上流recordの欠落 |
| `provenance_node_duplicated` | nodeの重複、想定外node |
| `provenance_node_kind_mismatch` | `record_kind`が`node_role`と一致しない |
| `provenance_node_identity_mismatch` | `record_id`または`record_version`の不一致 |
| `provenance_node_digest_mismatch` | 上流recordのDigestとの不一致 |
| `provenance_edge_missing` | 必須edgeの欠落、`verified_edges`の不在（旧形式） |
| `provenance_edge_unexpected` | 余分なedge、順序不一致 |
| `provenance_edge_endpoint_unresolved` | 端点が`verified_nodes`に無い |
| `provenance_self_reference` | `from == to`、端点が`provenance_verdict`、`closure`の不整合 |
| `decision_digest_mismatch` | Human decisionの`target_digest`不一致 |
| `owner_separation_violated` | Conformance・Final Challenge・Human decisionのowner重複 |

旧形式を互換入力として受理しない。旧形式はN11の拒否fixtureに限る。

## 既存testの新形式への追随

新形式の承認に伴い、旧形式を前提としていた既存3件の記述を新形式へ合わせた。
**受入の意味を弱めたものは無い。**いずれも検出力が上がる方向である。

| test | 変更前 | 変更後 | 理由 |
| --- | --- | --- | --- |
| A9 | `len(provenance["edges"]) >= 9` | `verified_nodes`が9件、`verified_edges`が8件、`edges`が無い | 旧記述は「辺数だけを見る」という、今回の不整合を見逃した当の検査である |
| A11 | `edge["to"]`から関門名を取得 | `edge["to"]["node_role"]`から取得 | edge両端が`node_role`参照になったため |
| B8 | 期待code `provenance_edge_missing` | `provenance_node_missing` | 上流recordの欠落は、新形式ではnodeの欠落として停止する（設計V1） |

追加testのうちN1は、期待codeを`provenance_edge_missing`へ確定した。
旧形式は`verified_edges`を持たないため、edge欠落として拒否される。
RED時は`provenance_edge_unexpected`または`provenance_self_reference`を想定していたが、
実装で「nodeの欠落」と「edgeの欠落」を別codeへ分けた結果、より正確な停止codeになった。
拒否されるという受入の意味は変わっていない。

## record versionの扱い

`verify_provenance`と`accept_artifact`は`record_version`を引数で受ける。既定は1のままとし、
正しい受理recordの再作成では2を指定する。旧version 1のrecordを上書きしない。

## 非対象

`9e8cf00`のrevert、既存recordの削除・上書きは行っていない。
設計提案、review対象文書、Requirement、Current Plan、checklistも変更していない。
正しい受理recordの再作成は次の作業単位で行う。
