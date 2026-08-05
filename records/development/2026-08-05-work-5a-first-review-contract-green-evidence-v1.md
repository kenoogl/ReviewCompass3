# Work 5A First Review Task Contract GREEN Evidence v1

## 対象

- 実装：`tools/task_contract/`（`identity.py`、`contract.py`、`execution.py`、`__init__.py`）
- Test：`tests/test_first_review_task_contract_e2e.py`（25件）
- 正本設計：`docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md`
- 承認：`DEC-WORK4-FIRST-REVIEW-CONTRACT-DESIGN-001`
- RED：`records/development/2026-08-05-work-5a-first-review-contract-red-evidence-v1.md`
- receipt：`records/development/2026-08-05-work-5a-first-review-contract-green-test-receipt-v1.json`

## 結果

- Work 5A acceptance：`25 passed`
- 全test：venv公式runner `764 passed`、Python 3.9.6、pytest 8.4.2、fallback false

既存testは変更していない。`tools/bootstrap/`と`tools/development/`へRuntime componentを足していない。

## 実装したrecord kind

閉じた12種とする。拡張ポイント、plugin、未定義の汎用schemaは作らない。

| record kind | 役割 |
| --- | --- |
| `requirement_binding` | 固定Requirementの束縛。定義fileが無いIDは受け付けない |
| `source_snapshot` | 読取りだけで観測した固定source treeとChange Set |
| `review_task_contract` | 設計§2の10節を持つ最小Contract |
| `compile_verdict` | `compiled`または`not_compilable` |
| `plan_bundle` | 1 bundleと6 typed view |
| `context_manifest` | 宣言7項目、材料束、Scope contract、実体化した材料 |
| `workflow_permit` | `single_active_leaf`の許可 |
| `finding_set` | deterministic stubのFinding |
| `conformance_verdict` | 適合判定 |
| `final_challenge_verdict` | 最終異議。Conformanceと別owner |
| `human_decision` | 対象Digestへ束縛したHuman判断 |
| `provenance_verdict` | 型付き辺とDigestによる来歴検証 |
| `accepted_artifact` | 受理成果物 |

すべてのrecordは`record_id`、`record_version`、`content_digest`、上流`record_ref`を持つ。
`record_ref`はrecord kind、ID、version、Digestを同時に持つ。

6 typed viewは`context_acquisition`、`review_execution`、`harness_and_capability`、
`verification`、`provenance_capture`、`human_interaction`とし、`REQ-CONTRACT-002`の列挙に合わせた。

## 実装した不変条件

| 不変条件 | 実装 |
| --- | --- |
| Contract 10節の必須化 | `CONTRACT_SECTIONS`。欠落は`contract_section_missing`または`not_compilable` |
| 決定的なcompile | 同じContractとbindingから同じ`content_digest`のverdictを返す |
| 順逆被覆 | `check_requirement_coverage`が未受領Requirementと孤立obligationを返す |
| 明示材料だけ | `build_context_manifest`が範囲外pathを`implicit_material_rejected`で拒否 |
| Context宣言7項目 | 欠落は`context_incomplete` |
| freshness | `assert_context_fresh`がDigest差を`stale`で停止 |
| active leaf 1件 | 二件目は待機候補へ記録し`not_permitted`。解放後に取得できる |
| LLM非使用 | `run_stub_reviewer`は固定ruleのみ。`calls_llm: False`をrecordへ残す |
| owner分離 | Conformance、Final Challenge、Human decisionを別ownerとし、兼務を`owner_separation_violated`で停止 |
| `warning`の扱い | `error`のみConformanceを`failed`にする。`human_decision_required`は常に`True` |
| Digest束縛 | Human decisionの`target_digest`はContext Manifestの`content_digest` |
| 来歴 | 9段の型付き辺。欠落は`provenance_edge_missing`、不一致は`decision_digest_mismatch` |
| 受理条件 | Human承認と`verified`が揃った場合だけ`accepted_artifact`を作る |

## 実装中に行った調整

`tests/test_first_review_task_contract_e2e.py`のfixtureで、B2が使う`REQ-EVAL-001`の定義fileを
生成するよう1行を追加した。B2は「定義は存在するが受け先が無いRequirement」を扱う負例であり、
定義fileが無いと別の停止（`schema_violation`）になってしまうためである。

受入条件そのもの（`not_compilable`になること、`unreceived_requirement_ids`に含まれること）は
変更していない。他24件は初回作成時のままである。

## 非対象

実文書に対するreview run、Human decision、accepted artifactの作成は行っていない。
testはすべて一時ディレクトリのfixtureに対して実行した。
LLM、外部送信、外部`DATA_ROOT`、Git write／push／PR／CIを使っていない。
Requirement、Requirement authority、既存bootstrap、Work 4A Evidence、Work 4B scopeも変更していない。
E2〜E7、Implementation Task Contract、台帳、リファクタリングは開始していない。
