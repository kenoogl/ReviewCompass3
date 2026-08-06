# Final Challenge 意図毀損検出（CL-6A-10） RED Evidence v1

- 承認正本：`docs/design/2026-08-06-final-challenge-intent-damage-proposal.md`
  （状態`approved`、2026-08-06、Human文言「承認」。§7の3点すべてを承認）
- 対応表：`records/development/2026-08-06-intent-damage-declaration-red-map-v1.json`
- 実行環境：Python 3.9.6、pytest 8.4.2、公式venv runner、fallback `false`
- 実行時刻：2026-08-06T15:56:14+09:00（公式全Test receiptの`recorded_at`）

## 0. 何を固定したのか（範囲の明示）

**固定したのはRED testと境界例だけである。GREEN実装は行っていない。**
`tools/`配下の実装コード（`task_contract/execution.py`を含む）は一切変更していない。
RED 7件はいずれも実装の不在（finding種別`kind`・発生元`origin`・Human採否
`human_ruling`の未対応、種別を見ないConformance、Conformanceを写すだけの
Final Challenge）で失敗しており、この記録はREDの成立を示すものであって、
対象振る舞いが実装されたことを示すものではない。GREEN側（提案§4の
`tools/task_contract/execution.py`への最小変更）は別作業である。

本fileのtestが事実上の契約として固定した最小語彙（提案§3の語に忠実）：

- finding単位の種別field `kind`：`contract`／`intent_damage`。省略時は`contract`
  （後方互換）。runtime定数`FINDING_KINDS == ("contract", "intent_damage")`。
- finding単位の発生元field `origin`：`{"route": <route種>, "identity": <str>}`。
  runtime定数`FINDING_ORIGIN_ROUTES == ("deterministic_stub", "subagent",
  "external_api", "human")`。
- finding単位のHuman採否field `human_ruling`：`accepted`／`rejected`／`pending`。
  `intent_damage`で省略時は未了として扱う（P4のfail-closed）。rejectの理由は
  `human_ruling_reason`に残す（P6）。
- blockingの表現は既存severity語彙の`error`を再利用する（新fieldを足さない）。
- P4のfail-closed停止は実装の流儀`ContractError`とし、codeは既存の閉じた
  stop code `human_decision_missing`を再利用する（STOP_CODESへの追加を要しない）。

## 1. 固定入力（機械計算したSHA-256）

`shasum -a 256`で計算した。

| path | SHA-256 |
| --- | --- |
| `docs/design/2026-08-06-final-challenge-intent-damage-proposal.md` | `7f8cd3bc6da61efbc1fbcef7b93007e1534e8b77d53e329fbcd8026bf143baf6` |
| `tests/test_final_challenge_intent_damage.py`（新規） | `25ce60f3d6893681776bb636baf7ff02ecb51556ed92b6159a5b2f3f75371391` |
| `tools/task_contract/execution.py`（未変更） | `606eaceae86857634a917526f28367c4d6b84a4033bbaf085eddb267ab80371f` |
| `tools/task_contract/identity.py`（未変更） | `a85f51617b8e9d04a5fed63b2bc8ba97af26118e26dc307cb02fe0633f551774` |
| `tools/task_contract/__init__.py`（未変更） | `605ce9c7ca6271f4e7d1fd6ebaabfcd958852ebe8bf171cd8d628a4becbb57a3` |
| `tests/test_first_review_task_contract_e2e.py`（未変更。fixture再利用元） | `cc99faaa4813aa629c9640431e31d4da635890bc5ec1e1f30c631d06c513661f` |
| `records/development/2026-08-06-intent-damage-declaration-red-map-v1.json` | `80decdaa37ac8a0f977128d7a7866c6e00c6defd58faacf32eceeeb2a90ae3d0` |

## 2. 追加した8 testと規範宣言P1〜P7の対応

すべて`tests/test_final_challenge_intent_damage.py`。fixtureは既存E2E test
（`_chain`・`run_stub_reviewer`の連鎖）を再利用し、意図毀損所見は固定fixtureとして
差し込む。LLMは呼ばない。

| P | test関数 | 種別 |
| --- | --- | --- |
| P1 | `test_p1_intent_damage_kind_and_origin_are_constructible` | RED |
| P1後方互換 | `test_p1_legacy_findings_without_kind_keep_passing` | 境界（いま成功） |
| P2 | `test_p2_blocking_intent_damage_does_not_fail_conformance` | RED |
| P3（中核） | `test_p3_accepted_blocking_intent_damage_fails_final_challenge` | RED |
| P4 | `test_p4_pending_intent_damage_stops_final_challenge_fail_closed` | RED |
| P5 | `test_p5_multiple_intent_damage_findings_are_kept_without_auto_merge` | RED |
| P6 | `test_p6_rejected_intent_damage_does_not_fail_final_challenge` | RED |
| P7 | `test_p7_origin_routes_are_formally_equivalent` | RED |

## 3. 実測した失敗内容（RED 7件）

`.venv/bin/python3 -m pytest tests/test_final_challenge_intent_damage.py -v`を
自分で実行して確認した実測値である。`7 failed, 1 passed in 0.07s`、collected 8 items、
error 0件、import error 0件。

| P | 失敗したassertion | 実測値 |
| --- | --- | --- |
| P1 | `assert runtime.FINDING_KINDS == ("contract", "intent_damage")`（134行） | `AttributeError: module 'tools.task_contract' has no attribute 'FINDING_KINDS'`（種別・発生元の語彙が未実装） |
| P2 | `assert conformance["status"] == "passed"`（214行） | `AssertionError: assert 'failed' == 'passed'`（`_severity_counts`が種別を見ず、`intent_damage`のerrorも数える。execution.py 277-281行） |
| P3 | `assert conformance["status"] == "passed"`（243行。中核負例の前提） | `AssertionError: assert 'failed' == 'passed'`（同上。P2実装後は`evaluate_final_challenge`がConformanceを写すだけである限り（execution.py 312行）`challenge["status"] == "failed"`（245行）で失敗し続ける） |
| P4 | `pytest.raises(runtime.ContractError)`（275-276行） | `Failed: DID NOT RAISE`（採否未了でも`evaluate_final_challenge`はverdictを返す。1件目のblocking-pending caseで失敗） |
| P5 | `assert conformance["status"] == "passed"`（323行） | `AssertionError: assert 'failed' == 'passed'`（保持のassert（317-319行、3件そのまま・統合なし）は成功済みで、判定のassertで失敗） |
| P6 | `assert conformance["status"] == "passed"`（353行） | `AssertionError: assert 'failed' == 'passed'`（rejected所見のerrorもConformanceが数える） |
| P7 | `assert conformance["status"] == "passed"`（404行） | `AssertionError: assert 'failed' == 'passed'`（1経路目`deterministic_stub`で失敗。経路identityの保持assert（401行）は成功済み） |

失敗原因は7件とも対象の振る舞いが未実装であること（語彙定数の不在、種別を見ない
Conformance、Conformanceの合否を写すだけのFinal Challenge、採否未了でも停止しない
Final Challenge）であって、import error、fixture不在、環境差ではない。

## 4. 境界例が成功する実測（1件）

同じ実行で`1 passed`を確認した。

| P | test | 成功の実測根拠 |
| --- | --- | --- |
| P1後方互換 | `test_p1_legacy_findings_without_kind_keep_passing` | 種別fieldの無い既存形finding（stub生成のwarning・error）が従来どおり扱われる。warningだけでconformance/challengeともpassed・`human_decision_required` True、errorでconformance failed。既存E2E happy path（test_a6・test_c2・test_b10）の再確認であり、「種別が無い既存findingは`contract`として扱う」（P1）を実装後も変えない境界固定である |

## 5. 公式全Testの実測

`.venv/bin/python3 -m tools.development.policy_test_runner --suite full --receipt <scratchpad>`
を実行した。receiptはscratchpad配下だけに置き、repositoryへは保存していない。

| 項目 | 実測値 |
| --- | --- |
| status | `failed`（exit code 1） |
| passed | 1033 |
| failed | 7 |
| errors | 0 |
| skipped | 0 |
| xfailed / xpassed | 0 / 0 |
| total | 1040 |
| command | `.venv/bin/python3 -m pytest -q` |
| python_version | 3.9.6 |
| pytest_version | 8.4.2 |
| fallback_used | `false` |
| config_digest | `890380460e063e508145450cf6e80865409d20035dfc2265b99c364f03b8b6ea` |
| source_state_digest | `f5f3df247ba36fb808fc1441a3fd08d11103a13ec9b3217d116430437bbb098c` |

失敗7件は新規file`tests/test_final_challenge_intent_damage.py`の7件だけである。
既存Testは1032件すべて成功しており（1033 passedの内訳は既存1032件＋新規境界例1件）、
既存の受入済み挙動を1件も壊していない。

test関数の機械計数（`tests/test_*.py`をASTで解析）は次である。

| 対象 | 新規を含む | 新規を除く |
| --- | --- | --- |
| testファイル | 143 | 142 |
| `test_`関数 | 847 | 839 |

## 6. 宣言→RED対応表の機械検査

`records/development/2026-08-06-intent-damage-declaration-red-map-v1.json`に、
P1〜P7それぞれの対応test、`red_now`、境界例を記録した。ASTで対象fileの
test関数名の実在を照合した結果、`missing_tests: []`、`unmapped_declarations: []`
（testの無いPは0件）、`red_now_inconsistent: []`、対応表に載っていないtest関数も
0件である。REDを持つ宣言は7件すべて（P1〜P7）で、P1は境界例
（後方互換の再確認）を併せ持つ。提案§4の関門（testの無いPが0件）を満たす。

## 7. 変更していない範囲

- 実装コード（`tools/`配下すべて。`task_contract/execution.py`、`identity.py`、
  `__init__.py`を含む。§1のSHA-256で未変更を固定した）。
- 既存Test（`tests/`配下の既存142 fileは1件も変更していない。fixture再利用元の
  `tests/test_first_review_task_contract_e2e.py`も未変更）。
- 既存記録、TODO、checklist、config、schema、Current Plan（上書き、削除、無効化、
  stale化はしていない）。
- STOP_CODESへの追加は要求していない（P4は既存の`human_decision_missing`を再利用）。
- commit、push、tag、PR、CI、外部送信は行っていない。作業終了時点の
  `git status --porcelain`は、未追跡3件（新規test 1件、記録2件）だけである。
