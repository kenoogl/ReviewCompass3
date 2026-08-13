# 第3段 試験増加候補の機械列挙 Evidence v1

- 記録日：2026-08-13
- 状態：`enumerated_pending_independent_review`
- 対象Issue：`ISSUE-TEST-GROWTH-STATE-PINNING-001`
- 作業種別：文書・読み取り調査
- 個別一覧：`records/development/2026-08-13-test-growth-nodeid-candidates-v1.txt`
- 個別一覧SHA-256：`11d383f82196e6d964340f83e085d4fd6c7f4e9b1fd3570de8830bafbffbecad`

## 1. 目的と範囲

【記録】`TODO_NEXT_SESSION.md`は、第3段の最初の一作業を、公式全試験が1,338件だった固定状態と
現在の1,739件を機械比較し、当初398件と直近作業の3件を区別して401件の候補を列挙する
読み取り調査としている。

【判断】本記録は試験内容の良否、重複、到達可能性、削除可否を判定しない。件数を品質指標や削除目標にも
しない。コード、試験、設定、台帳は変更せず、後続の内容分類へ渡す母集団だけを固定する。

## 2. 基準と観測点

| 役割 | commit | 根拠・状態 |
| --- | --- | --- |
| 基準 | `7762c10b6daf3a10643fa00593c900d8f9c6c453` | fixture共通化後。Evidenceは変更前後とも対象129件、全1,338件で試験名・parametrize・assertの意味を維持したと記録 |
| 直近作業前 | `f254cfec48455ab6c317343633e97b81903d1ba3` | 対象分類・工程分離作業の試験追加前。収集1,736件 |
| 現在 | `13cef234c9d75d3c2763e959f963adb6b7dcc014` | 対象分類・工程分離完了後。収集1,739件 |

基準の固定材料は次の二件である。

- `records/development/2026-08-09-test-fixture-dedup-receipt-v1.json`、SHA-256
  `cdd490b06c4f12d65c80e632d0674602554e53cf42eeffadc07d994cce55e4d7`
- `records/development/2026-08-09-test-fixture-dedup-evidence-v1.md`、SHA-256
  `fc8863c8b56ea0078af1834efe2d0913de02cb1dc18574c24ff7329c2b46b8b2`

【実測】受領証はPython 3.9.6、pytest 8.4.2、1,338 passed、failed・error・skipped 0、終了コード0を
記録する。commit `7762c10`は受領証、Evidence、fixture共通化を同時に固定したため、受領証の
`source_state_digest`をcommit treeのDigestだとは扱わない。基準との結び付きは、同commitのEvidenceが
変更前後の収集・合格数不変と試験識別子を変えない範囲を記録していること、および同commitを再収集して
1,338件だったことによる。

## 3. 収集と照合方法

【実測】各commitを`git archive`でリポジトリ外の使い捨てdirectoryへ展開し、pytest pluginの
`pytest_collection_finish`で`session.items`の`nodeid`を取得した。実行引数は
`--collect-only -q -p no:cacheprovider`で、全三点とも終了コード0、重複node ID 0件だった。
収集器SHA-256は`1d071589eb24eea93c7665aba14a6970b5d518d333c78a45e2079532a9a213a7`、
集合比較器SHA-256は`9b53c64e0f1b17b3a420c7bacbd223fc629edbcbda6d17ad81558a5df6e6422d`である。

| 収集点 | Python / pytest | 件数 | 収集結果JSON SHA-256 |
| --- | --- | ---: | --- |
| 基準 | 3.9.6 / 8.4.2 | 1,338 | `148767a3a05564c5c67c7c86b1525cfb32ed7130d1fb9162a5abe203ed479389` |
| 基準対照 | 3.13.14 / 8.4.2 | 1,338 | `148767a3a05564c5c67c7c86b1525cfb32ed7130d1fb9162a5abe203ed479389` |
| 直近作業前 | 3.13.14 / 8.4.2 | 1,736 | `443330c5fcf61b882c6892fa45347b18329e23be9f4c7ddf3ee09f70085bada7` |
| 現在 | 3.13.14 / 8.4.2 | 1,739 | `12755c09a1467d8d77d6331029f7b142004e2837cfd89a43ce56c2cce74f6f20` |

【実測】基準のPython 3.9.6と3.13.14の収集結果はSHA-256まで一致した。したがって今回の集合差は
Python移行による収集差ではない。

## 4. 集合差と見かけの増減

| 比較 | 左 | 右 | 共通 | 追加ID | 消失ID | 正味 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 基準→直近作業前 | 1,338 | 1,736 | 1,336 | 400 | 2 | +398 |
| 直近作業前→現在 | 1,736 | 1,739 | 1,736 | 3 | 0 | +3 |
| 基準→現在 | 1,338 | 1,739 | 1,336 | 403 | 2 | +401 |

【実測】基準から消えた2 IDと追加側の2 IDは、いずれも
`tests/test_common_module_pins.py::test_common_module_is_pinned`の同じ二pathで、parameterに埋め込まれた
SHA-256だけが変わっていた。commit `b20d76bf291d8e9487a7940f827d8c94a639b4ef`の差分は、
`tools/common/digests.py`と`tools/common/paths.py`の修正と、それに対応する二つのpin値更新を同時に示す。
試験の削除・新設ではなくnode IDの置換であるため、追加403件からこの2件を除外した。

【実測】`git diff --name-status --find-renames=50%`では、基準から現在までのtest fileにrename・deleteは0件だった。
以上により、内容分類へ渡す候補は、当初398件と直近作業の3件を合わせた401件である。

直近作業の3件は次のとおりである。

- `tests/test_review_plan.py::test_classification_mismatches_warn_without_defaulting_to_code`
- `tests/test_review_plan.py::test_invalid_classification_documents_stop`
- `tests/test_review_plan.py::test_target_kinds_keep_their_own_review_processes`

## 5. 意味のある列挙単位

個別401件は別紙へ一行一node IDで固定した。次の表は内容をまだ判定せず、保守・参照単位であるtest fileごとに
機械集計した入口である。

| test file | 候補数 |
| --- | ---: |
| `tests/test_authority_reference_checker.py` | 19 |
| `tests/test_bootstrap_immutable_result_store.py` | 11 |
| `tests/test_claude_bootstrap.py` | 30 |
| `tests/test_claude_bootstrap_adversarial.py` | 11 |
| `tests/test_claude_bootstrap_cli.py` | 3 |
| `tests/test_claude_bootstrap_entrypoints.py` | 8 |
| `tests/test_claude_implementation_confirmation.py` | 8 |
| `tests/test_claude_implementation_executor.py` | 28 |
| `tests/test_claude_implementation_route.py` | 47 |
| `tests/test_claude_implementation_route_cli.py` | 12 |
| `tests/test_common_digests.py` | 19 |
| `tests/test_common_errors_paths_output.py` | 5 |
| `tests/test_declaration_red_map_check.py` | 3 |
| `tests/test_declaration_red_reason.py` | 5 |
| `tests/test_development_environment.py` | 1 |
| `tests/test_egress_adversarial.py` | 6 |
| `tests/test_egress_approval.py` | 19 |
| `tests/test_egress_gate.py` | 8 |
| `tests/test_egress_payload.py` | 2 |
| `tests/test_egress_prefilter.py` | 7 |
| `tests/test_issue_resolution_v4.py` | 24 |
| `tests/test_pilot_collaboration.py` | 65 |
| `tests/test_pilot_collaboration_cli.py` | 7 |
| `tests/test_pilot_collaboration_entrypoints.py` | 6 |
| `tests/test_policy_test_runner.py` | 5 |
| `tests/test_policy_test_runner_summary.py` | 4 |
| `tests/test_review_plan.py` | 9 |
| `tests/test_session_log_parse_codex_rollout.py` | 1 |
| `tests/test_session_log_preservation.py` | 4 |
| `tests/test_trusted_claude_transport.py` | 17 |
| `tests/test_work_unit_transition.py` | 7 |
| **合計** | **401** |

## 6. 反証と限界

【実測】中心判断「見かけの増減を除いた現在候補は401件」への反証として、(1)基準を当時と同じ
Python／pytestで再収集、(2)別Pythonでの同一性比較、(3)重複node ID検索、(4)test fileのrename・delete検索、
(5)消失2 IDの履歴差分確認を行った。Python差、重複、file移動、試験削除による反証は成立しなかった。

【判断】parameterの値変更が別の意味を持つ試験も一般にはあり得るため、すべてのparameter差を一律に
置換扱いしていない。今回除外したのは、履歴差分で同じ二つのmodule pin更新だと確認できた2件だけである。

【判断】401件は内容未分類の母集団である。個々が必要、不要、重複、到達不能、作業限定、実験用の
どれかは未判定であり、この記録から削除数を導かない。

## 7. 未実施

【未実施】試験内容の分類、試験・製品コード・設定・台帳の変更、削除、統合、変異検査、公式全試験、
第3段の最初の整理単位の選定、外部送信、push、履歴書換えは行っていない。収集用archiveと中間JSONは
リポジトリ外に作成した。
