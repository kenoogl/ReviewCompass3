# Work 6A 対応表訂正記録 v1

- 訂正対象：`records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json`
  （SHA-256 `51674c143858b37608c7914c5bc2a8973be8221e2d5bde9707d89d082f995a16`）
- 訂正の根拠：対応表の被覆主張に対する独立検証（2026-08-06）の判定と、
  Human承認済みの対処案。CL-6A-03についてはHumanの判断
  （2026-08-06「緩い読みでよい。」）による。
- 実行環境：Python 3.9.6、pytest 8.4.2

## 0. この記録の位置づけ

**旧inventoryをin-placeで書き換えていない。** 訂正内容を本記録にnew-onlyで固定し、
旧inventoryは当時の判断の記録として履歴に残す。削除、書換え、無効化のいずれも
行っていない（§6で機械確認）。

訂正は2件である。訂正1は3項目の分類の過大（`covered_by_existing_test`は検証に
耐えなかった）、訂正2は残余注記の非対称という記録形式の瑕疵である。あわせて、
検証で`fully_covered`が確認できた項目（CL-6A-09）と、本作業で閉じた残余を記す。

## 1. 訂正1：CL-6A-01・03・05の分類`covered_by_existing_test`は過大である

独立検証の結果、3項目とも引用testだけでは項目文の全要素を被覆しておらず、
検証時点の実態は`partially_covered`であった。各項目の未被覆要素と、その閉じ方を
次に列挙する（CL-6A-02は分類自体は維持だが、引用の欠落があったため併記する）。

### 1.1 CL-6A-01「Contract／Requirement／Plan／Context／Provenance欠落を検出する」

- 被覆済み：Contract節欠落、未受領Requirement義務、Context宣言欠落、
  Provenance辺破損（引用10件のとおり）。
- 未被覆だった要素：**「Plan欠落」だけ直接の負例が無かった。**
- 検出機構は実在する。Planは`plan_bundle`を内包する`compile_verdict`のnodeとして
  来歴に現れ、`tools/task_contract/execution.py`の汎用node検査loop
  （`validate_provenance_verdict`の451-453行付近、`verify_provenance`の546-548行付近）が
  `compile_verdict`も要求する。欠けていたのはtestによる固定だけである。
- 閉じ方：本作業の境界例
  `tests/test_work6a_coverage_boundaries.py::test_missing_compile_verdict_is_rejected_as_provenance_node_missing`
  で閉じた。生成側（`verify_provenance`へ`compile_verdict=None`）と検証側
  （完成済みverdictから`compile_verdict` nodeを除去して
  `validate_provenance_verdict`）の双方が`provenance_node_missing`
  （detail `compile_verdict`）で停止することを固定する。境界例であり
  **追加時点で成功した**（実測`1 passed`）。REDではない。

### 1.2 CL-6A-02「permission過剰、stale、crash、optional観測欠測を区別する」（分類維持・引用補充）

- 分類`covered_by_existing_test`は維持する。ただし引用に欠落があった。
- **permission過剰**：負例は実在するが対応表が引用していなかった。次を引用へ補う。
  - `tests/test_structured_argv_executor.py::test_preflight_failures_never_reach_the_runner`
    （286行付近。`granted_permissions: ["superuser"]`を`host_attestation_invalid`で拒否）
  - `tests/test_operation_routing_v2.py::test_host_attestation_is_an_input_not_a_permission_check`
    （362行付近。同上の拒否）
  - `tests/test_operation_routing_v2.py::test_standalone_preflight_with_inconsistent_missing_or_verdict_is_rejected`
    （660行付近。語彙外の取得済み権限`superuser`の申告を拒否）
- **optional観測欠測**：
  `tests/test_work4a_rebuild_v3_1_e2e.py::test_i10_missing_external_records_do_not_block_current`
  が近接被覆である（外部runtime recordを削除しても`validate_current`は
  baselineを無効にせず、`locator_unresolved`をannotationとして注記するだけである）。
  対応表はこれを引用していなかったため、本記録で引用へ補う。
- optional観測欠測への**参照用境界例は追加しなかった**。理由：i10の
  attestation→operational decision→baselineの構築は共有fixture化されておらず、
  「欠落が業務成果を無効にしない」ことの最小assertに絞っても、同じ構築手順と
  同じ最終assert（baseline保持と`locator_unresolved`注記）をほぼ全文複製することに
  なる。新しい検出は何も加わらず重複だけが増えるため、実在するi10の引用で
  閉じるのが適切と判断した。

### 1.3 CL-6A-03「validatorの既知違反見逃しと正常例誤停止を検出する」

- 被覆済み：見逃し側（独立checkが違反を検出しない場合のfailed）と、
  validator変更時の旧verdict stale化（引用4件のとおり）。
- 未被覆だった要素：**誤停止側**（正常例を誤って停止する不良）を対象にした
  専用の負例が無く、検証時点の実態は`partially_covered`であった。
- **Humanが緩い読みを採用した（2026-08-06「緩い読みでよい。」）。**
  - 採用した読み：正しい入力で合格する既存の緑テストが、誤停止の回帰検出を
    兼ねる。検査器が正常入力を誤って拒否し始めれば、当該テストが即座に失敗する。
  - したがって誤停止側は、専用の検出機構を新設せず、既存の正例テスト群を
    被覆根拠として引用する。
  - 誤停止率・既知違反検出率・変異検査の系統的測定は、Current Plan §10.2の
    評価指標（validator既知違反検出率、正常fixture誤停止率、mutation生存数。
    `docs/current/reviewcompass3-plan-current.md` 838-841行付近）として
    Work 8へ割当て済みであり、Work 6Aでは前倒ししない。
  - この読みの弱点：正例テストが1本も無い検査器が混ざっていても、現時点では
    それを数えていない。この弱点はWork 8の測定で拾う前提であることを明記する。

### 1.4 CL-6A-05「Source Snapshot、Change Set、Test Evidenceの不一致を拒否する」

- 被覆済み：Source Snapshot側の不一致（引用5件。snapshot不一致、Evidence欠落、
  code reference不一致、改ざんsnapshot、snapshot後のsource変更）。
- 未被覆だった要素：**Change SetとTest Evidenceの対象一致**。両者の正式artifactが
  未整備のため、その不一致を対象にした負例は現時点で書けない。
- 閉じ方：分類を`out_of_approved_scope`相当へ訂正する（CL-6A-04・06と同様、
  正式artifactの承認・整備を待つ扱い）。Source Snapshot側の引用5件は
  部分被覆の根拠として引き続き有効である。

## 2. 訂正2：残余注記の非対称は瑕疵である

旧inventoryは、CL-6A-02のrationaleにだけ「残余：optional観測欠測だけを対象にした
専用負例は未被覆」と注記し、同じく残余のあったCL-6A-01（Plan欠落）、
CL-6A-03（誤停止側）、CL-6A-05（Change Set・Test Evidence）には注記していなかった。
同じ判定規則（「部分被覆はrationaleへ残余を明記」）を宣言しながら適用が
非対称だったことは瑕疵である。本記録の§1が全項目の残余を明記することで訂正する。

## 3. CL-6A-09は独立検証で`fully_covered`が確認された

検証内容：引用テスト2件の本体を読み、次を直接assertしていることを確認した。

- rendererを失敗させてもcapture（raw・evidence）とprojection（`complete`）と
  authority（`valid`）が保持され、`display_status`だけが`failed`になること。
- authority欠落（`fixed_inputs`空）は`incomplete`と判定され、表示器のfailure
  （`display_error`）とは混同されないこと（`display_status`は`rendered`のまま）。

項目文「表示器だけのfailureで有効成果を破棄しないことを確認する」の中核を
直接assertしており、分類`covered_by_existing_test`は検証に耐えた。引用テストは
次の2件である。

- `tests/test_session_bootstrap_e2e.py::test_display_failure_does_not_discard_valid_capture_or_authority`
- `tests/test_session_bootstrap_e2e.py::test_missing_authority_is_incomplete_not_a_display_failure`

## 4. 本作業で追加した境界例

- `tests/test_work6a_coverage_boundaries.py`（新規1 file、1 test）。
  CL-6A-01のPlan欠落残余を閉じる境界例であり、追加時点で成功した
  （`1 passed`。REDではない）。実装（`tools/`配下）は変更していない。

## 5. 機械計算したSHA-256

| file | SHA-256 |
| --- | --- |
| `records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json`（旧inventory） | `51674c143858b37608c7914c5bc2a8973be8221e2d5bde9707d89d082f995a16` |
| `tests/test_first_review_task_contract_e2e.py` | `cc99faaa4813aa629c9640431e31d4da635890bc5ec1e1f30c631d06c513661f` |
| `tests/test_structured_argv_executor.py` | `9166e680d6c1b528163df23e5ecb0852c5fdf614875818737a265bc49760b9ff` |
| `tests/test_operation_routing_v2.py` | `369544e87bf673222ca6fec0306b55dc130b831094f51c93afa3e46c5fb075c5` |
| `tests/test_work4a_rebuild_v3_1_e2e.py` | `89b40a67b564cc37dea7158015d28371f4c0a6ef855317ada0e4694fd413a57d` |
| `tests/test_session_bootstrap_e2e.py` | `ca4486fb43b3e5f4bd32175b0e177efb1a8612c08e2b43edaa98206e453eaedb` |
| `tests/test_bootstrap_review_assurance.py` | `606c5ee30bbe69c50f86878dbacd6ef3631244c9a2f10d44154ae29b00f63bd1` |
| `tests/test_development_policy.py` | `2920252103af27ef905269de38ccab554cce7e51bf111d28f51371deb10b453a` |
| `tools/task_contract/execution.py` | `606eaceae86857634a917526f28367c4d6b84a4033bbaf085eddb267ab80371f` |
| `docs/current/reviewcompass3-plan-current.md` | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` |

旧inventoryのSHA-256は、先行の訂正記録
`records/development/2026-08-06-work6a-evidence-correction-v1.md` §4が記録した値と
一致しており、未変更である。`docs/current/reviewcompass3-plan-current.md`の値も
旧inventoryの`fixed_sources`が記録した値と一致している。

## 6. 旧記録を削除・書換えしていないこと

- `git status --porcelain`：`records/`配下および`tests/`配下に変更（`M`）は0件。
  未追跡は本作業でnew-onlyに作成した
  `tests/test_work6a_coverage_boundaries.py`と本記録の2件だけである。
- 実装（`tools/`配下）、既存test、既存記録、TODO、チェックリスト、configは
  変更していない。commit、push、外部送信は行っていない。
