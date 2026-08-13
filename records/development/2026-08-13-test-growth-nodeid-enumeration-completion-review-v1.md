# 第3段 試験増加候補の機械列挙 独立完了レビュー v1

- レビュー日：2026-08-13
- 列挙commit：`864e34d5fac1a0c1a279884e52c6bdc3431e1054`
- 基準commit：`7762c10b6daf3a10643fa00593c900d8f9c6c453`
- 直近作業前commit：`f254cfec48455ab6c317343633e97b81903d1ba3`
- 現在状態の比較commit：`13cef234c9d75d3c2763e959f963adb6b7dcc014`
- 対象一覧：`records/development/2026-08-13-test-growth-nodeid-candidates-v1.txt`
- 対象Evidence：`records/development/2026-08-13-test-growth-nodeid-enumeration-evidence-v1.md`

## 1. 判定

**verified**

【実測】公式全試験1,338件の基準から現在1,739件までの正味増加401件は、2件のmodule pinの
node ID置換を除いた個別一覧として過不足なく固定されていた。当初398件と直近作業3件も分離されている。

## 2. 止める指摘

**0件**。

【実測】上位方針矛盾、承認欠落、機械で示せる候補過不足または置換欠陥、境界違反または報告不一致の
いずれも確認されなかった。読み取り調査と二文書の列挙結果だけに範囲を限定しており、新しい仕組み、コード、
試験、設定、台帳は追加していない。

## 3. 報告不一致

**0件**。

【実測】固定対象のcommitはすべて実在した。対象一覧のSHA-256は
`11d383f82196e6d964340f83e085d4fd6c7f4e9b1fd3570de8830bafbffbecad`、対象Evidenceは
`dfa2ebb73a940daa527d3ceac8c502876bf13152bff940a24308411ab2a64f3f`で、申告値と一致した。基準受領証は
`cdd490b06c4f12d65c80e632d0674602554e53cf42eeffadc07d994cce55e4d7`、基準Evidenceは
`fc8863c8b56ea0078af1834efe2d0913de02cb1dc18574c24ff7329c2b46b8b2`で、これも一致した。

【実測】列挙commitの変更は対象一覧と対象Evidenceの追加だけだった。コード、試験、設定、台帳の変更はない。

## 4. 基準commitと三つの収集集合の独立照合

【記録】基準受領証はPython 3.9.6、pytest 8.4.2、1,338件成功、失敗・エラー・除外0、終了コード0を
記録する。基準Evidenceはcommit `7762c10`でfixtureを共通化した前後とも対象129件、全1,338件であり、
試験関数名、parametrize、assertの意味を変更していないと記録する。履歴は基準、直近作業前、現在、
列挙commitの順に連続していた。件数だけから基準commitを推測する説明ではない。

【実測】三commitを`git archive`でリポジトリ外へ展開し、成果物の収集器を使わず、新しく作成した一時的な
pytest pluginで`session.items`のnode IDを収集した。全収集は`--collect-only -q -p no:cacheprovider`を使い、
それぞれ単独で終了コード0だった。結果は次のとおりである。

| 収集点 | Python / pytest | 件数 | 重複 | 独立収集JSON SHA-256 |
| --- | --- | ---: | ---: | --- |
| 基準 | 3.9.6 / 8.4.2 | 1,338 | 0 | `aa8355e773f243ab1e94b42d4ee260a89d65907d5415f192000ff80edb98154f` |
| 基準対照 | 3.13.14 / 8.4.2 | 1,338 | 0 | `aa8355e773f243ab1e94b42d4ee260a89d65907d5415f192000ff80edb98154f` |
| 直近作業前 | 3.13.14 / 8.4.2 | 1,736 | 0 | `ae27ef5b0440d535ee92376189dc387a79ea780237fb3216382dc903043342dd` |
| 現在 | 3.13.14 / 8.4.2 | 1,739 | 0 | `77a2b705df0d25d5fcdf791c6ad2a7f3e2321fec241fae37b28f918d0f770ac8` |

【実測】基準のPython 3.9.6と3.13.14はnode ID一覧が完全一致した。成果物の集計値を読まず、上記四集合を
別の一時scriptで集合演算した結果は次のとおりだった。

| 比較 | 共通 | 追加 | 消失 | 正味 |
| --- | ---: | ---: | ---: | ---: |
| 基準→直近作業前 | 1,336 | 400 | 2 | +398 |
| 直近作業前→現在 | 1,736 | 3 | 0 | +3 |
| 基準→現在 | 1,336 | 403 | 2 | +401 |

## 5. 2件のnode ID置換と401件一覧の完全性

【実測】基準から消失した2件と現在側の対応する追加2件は次の置換だった。

- `tests/test_common_module_pins.py::test_common_module_is_pinned[tools/common/digests.py-db6b830592f5d57ef7b42b5ec32fd398f4c36957a978604166525fc54da3396f]`
  → `tests/test_common_module_pins.py::test_common_module_is_pinned[tools/common/digests.py-fc2d728c4c2cfd1b4e70b7eef6d0e6d4ce9a4a033712b93402bd2c7f984624f7]`
- `tests/test_common_module_pins.py::test_common_module_is_pinned[tools/common/paths.py-daa325791b5bead80c240eb298c7084f6c26ff2d96ca850cc65449686cc4826d]`
  → `tests/test_common_module_pins.py::test_common_module_is_pinned[tools/common/paths.py-039512f579bf6e939d4086c1e75f848b0b4e5dba7f7170b63c21fd005b48e1ec]`

【実測】commit `b20d76bf291d8e9487a7940f827d8c94a639b4ef`は`tools/common/digests.py`と
`tools/common/paths.py`の修正と同時に、この二つのpin値だけを更新していた。同じ試験と同じ対象pathの
parameter SHA-256更新であり、試験の削除・新設ではない。基準から現在までの`tests/test*.py`履歴にもrename・
deleteは0件だった。

【実測】現在側の追加403件から上記2件だけを除いた独立集合は401件だった。この集合と対象一覧を直接比較し、
欠落0件、余分0件、一覧内重複0件を確認した。

## 6. 31 file群と直近作業3件の分離

【実測】401件をnode IDのtest file部分から独立集計すると31群、合計401件となり、Evidenceの全群と
各件数に一致した。

| test file | 件数 | test file | 件数 |
| --- | ---: | --- | ---: |
| `tests/test_authority_reference_checker.py` | 19 | `tests/test_bootstrap_immutable_result_store.py` | 11 |
| `tests/test_claude_bootstrap.py` | 30 | `tests/test_claude_bootstrap_adversarial.py` | 11 |
| `tests/test_claude_bootstrap_cli.py` | 3 | `tests/test_claude_bootstrap_entrypoints.py` | 8 |
| `tests/test_claude_implementation_confirmation.py` | 8 | `tests/test_claude_implementation_executor.py` | 28 |
| `tests/test_claude_implementation_route.py` | 47 | `tests/test_claude_implementation_route_cli.py` | 12 |
| `tests/test_common_digests.py` | 19 | `tests/test_common_errors_paths_output.py` | 5 |
| `tests/test_declaration_red_map_check.py` | 3 | `tests/test_declaration_red_reason.py` | 5 |
| `tests/test_development_environment.py` | 1 | `tests/test_egress_adversarial.py` | 6 |
| `tests/test_egress_approval.py` | 19 | `tests/test_egress_gate.py` | 8 |
| `tests/test_egress_payload.py` | 2 | `tests/test_egress_prefilter.py` | 7 |
| `tests/test_issue_resolution_v4.py` | 24 | `tests/test_pilot_collaboration.py` | 65 |
| `tests/test_pilot_collaboration_cli.py` | 7 | `tests/test_pilot_collaboration_entrypoints.py` | 6 |
| `tests/test_policy_test_runner.py` | 5 | `tests/test_policy_test_runner_summary.py` | 4 |
| `tests/test_review_plan.py` | 9 | `tests/test_session_log_parse_codex_rollout.py` | 1 |
| `tests/test_session_log_preservation.py` | 4 | `tests/test_trusted_claude_transport.py` | 17 |
| `tests/test_work_unit_transition.py` | 7 | **合計** | **401** |

【実測】直近作業前集合との差は次の3件だけで、当初398件との重なりは0件だった。

- `tests/test_review_plan.py::test_classification_mismatches_warn_without_defaulting_to_code`
- `tests/test_review_plan.py::test_invalid_classification_documents_stop`
- `tests/test_review_plan.py::test_target_kinds_keep_their_own_review_processes`

## 7. 試した反証

【実測】中心判断を否定するため、基準の収集を当時と同じPython 3.9.6と現在のPython 3.13.14で別々に行い、
Python版によるnode ID差が出るかを試した。一覧はSHA-256まで一致し、反証は成立しなかった。

【実測】さらに、追加403件をそのまま候補とみなして対象一覧と比較すると、二つのmodule pin新SHAの分だけ
2件余ることを確認した。その二つが同一試験・同一対象pathの旧SHAと一対一に対応し、履歴差分とも一致する場合だけ
置換として除外すると、初めて対象一覧401件と完全一致した。置換の過剰除外または除外不足による反証も成立しなかった。

## 8. 未実施

【未実施】試験内容の分類、必要性判断、削除、統合、変異検査、第3段の整理単位選定、成果物・コード・試験・
設定・台帳・TODOの修正、外部送信、push、履歴書換え、段完了判断は行っていない。独立収集用script、Git archive、
収集JSONはリポジトリ外だけに作成した。
