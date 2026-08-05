# Work 6A Current Work Projection negative path RED Evidence v1

- 承認Decision：`DEC-WORK5A-PROJECTION-ROUTING-001`
  （`records/development/2026-08-06-work5a-current-work-projection-routing-decision-v1.md`）
- 提案正本：`docs/design/2026-08-06-work5a-current-work-projection-routing-proposal.md`（案A）
- 対応inventory：`records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json`
- 実行環境：Python 3.9.6、pytest 8.4.2、公式venv runner、fallback `false`
- 実行時刻：2026-08-06T08:42:38+09:00（公式全Test receiptの`recorded_at`）

## 0. 何を固定したのか（範囲の明示）

**固定したのはRED testだけである。GREEN実装は行っていない。Current Work Projectionの
正式写像、正式projection schema、新module、新schemaも行っていない。**

案A §4の「Work 6Aでは、正式入力欠落、第二正本化、欠測推測、stale／競合の誤表示を
RED fixtureとして先に固定する。正式projection本体を同時に発明しない」に対応する。
追加した6 testはいずれもassertionで失敗しており、`tools/development/session_log_bootstrap.py`は
1 byteも変更していない。この記録はREDの成立を示すものであって、対象振る舞いが実装された
ことを示すものではない。

GREEN実装範囲は、案A §「非承認範囲」により別途Human判断で確定する。

## 1. 固定入力（機械計算したSHA-256）

`shasum -a 256`で計算した。

| path | SHA-256 |
| --- | --- |
| `records/development/2026-08-06-work5a-current-work-projection-routing-decision-v1.md` | `f084b471d3fe4ba40a9c6a7a5e3882fa78090da54c7e9b19b04547dde5307eda` |
| `docs/design/2026-08-06-work5a-current-work-projection-routing-proposal.md` | `c061be7d5abd1f428497f59d2b4ccc352b699d657d038d11f1d359a76e587809` |
| `tools/development/session_log_bootstrap.py` | `55a7c38b8d60101d709f21196f06db1943325e8d149b8c68aad69055158ac5c3` |
| `tests/test_work6a_current_work_projection_negative.py` | `25a76b7ba39dc032c3e30204cf9d83377129d9b530ab4eeb90dd0f5a199ade0f` |
| `tests/fixtures/development/session-log-bootstrap/projection-inputs.json` | `08d36c9db08ce8fd64c5810de45d71dedb3350e54aab35d14772d44f9666f936` |
| `tests/fixtures/development/session-log-bootstrap/projection-incomplete-inputs.json` | `b0291bf318ae611a4ffbf360b737e43666a4cda17edc56acbb73b10336058eb5` |
| `docs/development/2026-08-03-initial-development-checklist.md` | `1bd743b0fd110342900996199b2a81eaf2b42440f28318f931e43a78b039a550` |
| `docs/current/reviewcompass3-plan-current.md` | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` |
| `records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json` | `51674c143858b37608c7914c5bc2a8973be8221e2d5bde9707d89d082f995a16` |

対象実装は`tools/development/session_log_bootstrap.py`の次である。いずれも未変更。

| 対象 | 行 | 現行の振る舞い |
| --- | --- | --- |
| `_projection_missing_inputs` | 520-543 | Plan相当とevent stream相当が各1件あればmissingを空にする |
| `project_current_work` | 560-696（status判定は653-674） | conflictもmissingも無ければ`complete`。`freshness`は素通しで判定に使わない |
| `render_current_work` | 714-（分岐は722） | `status != "complete"`のときだけ`_render_diagnostic`へ切替える |

## 2. 追加した6 testと案A 4分類の対応

すべて`tests/test_work6a_current_work_projection_negative.py`にある。

| # | test関数 | 案Aの分類 |
| --- | --- | --- |
| 1 | `test_hand_editable_handoff_is_not_accepted_as_authority` | 第二正本化 |
| 2 | `test_stale_freshness_is_not_displayed_as_complete` | stale／競合の誤表示（stale） |
| 3 | `test_missing_freshness_is_not_guessed_as_current` | 欠測推測 |
| 4 | `test_fixed_input_without_valid_digest_is_not_ignored` | 正式入力欠落 |
| 5 | `test_conflicting_digests_for_one_identity_are_inconsistent` | stale／競合の誤表示（競合） |
| 6 | `test_stale_input_text_does_not_assert_a_normal_next_action` | stale／競合の誤表示（表示側） |

## 3. 実測した失敗内容

`.venv/bin/python3 -m pytest tests/test_work6a_current_work_projection_negative.py -v`を
自分で実行して確認した実測値である。`6 failed in 0.03s`、collected 6 items、
error 0件、fixture不在0件、import error 0件。

| # | 失敗したassertion | 実測値 |
| --- | --- | --- |
| 1 | `assert diagnostics["status"] != "complete"`（81行） | `AssertionError: assert 'complete' != 'complete'` |
| 2 | `assert projection["diagnostics"]["status"] != "complete"`（95行） | `AssertionError: assert 'complete' != 'complete'` |
| 3 | `assert diagnostics["status"] != "complete"`（108行） | `AssertionError: assert 'complete' != 'complete'` |
| 4 | `assert diagnostics["status"] != "complete"`（127行） | `AssertionError: assert 'complete' != 'complete'` |
| 5 | `assert diagnostics["status"] == "inconsistent"`（149行） | `AssertionError: assert 'complete' == 'inconsistent'`（`- inconsistent` / `+ complete`） |
| 6 | `assert "STATUS:" in detailed`（170行） | `AssertionError: assert 'STATUS:' in '…'` |

6番の`detailed`は実測で次の全文である（末尾改行あり）。

```text
ReviewCompass3 Current Work
generated_at: 2026-08-03T09:30:00+09:00
freshness: stale
inputs:
  - docs/current/reviewcompass3-plan-current.md 0ae6bef979192b008a8a71fc090f709279c4bd1f0db159f9faadf947e929156f
  - session-log-bootstrap/workflow-events.jsonl 8009712a3c673e935aa60434839acc104bae6ab606638538f172df1d43c4b024

PLAN
  stage: bootstrap
  work: Work 1B Session Log Bootstrapと現在位置text表示
  state: active

CURRENT ACTIVITY
  contract: none
  work_item: RC3-WORK1B-RED-TESTS
  tdd_state: red

NEXT
  Implement Session Log Bootstrap mapping

BLOCKERS
  none

HUMAN DECISIONS
  none

STALE / REVERIFY
  none
```

`freshness: stale`の一行を添えたまま、PLAN、CURRENT ACTIVITY、NEXTを正常な現在位置として
断定表示している。これが案Aの言う「stale入力の正常表示」である。

失敗原因は6件とも対象の振る舞いが未実装であることであって、import error、fixture不在、
環境差ではない。1から5は`diagnostics["status"]`が`complete`のままであること、
6は`render_current_work`が診断表示へ切替えないことに帰着する。

## 4. 既存負例と重複していないことの根拠

既存4件との対比は次である。入力、対象関数、assert対象のいずれかが必ず異なる。

| 既存test | 入力 | 既存が固定していること | 今回の6件との差 |
| --- | --- | --- | --- |
| `tests/test_session_log_bootstrap.py::test_projection_reports_missing_authority_without_guessing` | `projection-incomplete-inputs.json`（`fixed_inputs: []`） | 固定入力が**空**のときの`incomplete`と`missing` 2件の完全一致 | 今回は`fixed_inputs`が**非空**の場合。無効Digest混入、手編集source混入、identity競合、`freshness`欠落・`stale`を扱う |
| `tests/test_session_log_bootstrap.py::test_projection_reports_conflicting_active_work_as_inconsistent` | `workflow-events-conflict.jsonl` | **event側**の並行`work_started`競合による`inconsistent` | 今回の5番は**固定入力側**の同一identity・異Digest競合。event streamは正常fixtureのまま |
| `tests/test_session_bootstrap_e2e.py::test_display_failure_does_not_discard_valid_capture_or_authority` | renderer例外注入 | **表示器failure**で捕捉物とauthorityを破棄しないこと | 今回は表示器を壊さない。renderは正常に完走し、その**内容**が誤っていることを固定する |
| `tests/test_session_bootstrap_e2e.py::test_missing_authority_is_incomplete_not_a_display_failure` | `fixed_inputs: []` | authority欠落を表示器failureと混同しないこと | 今回はauthority欠落ではない。入力は揃っているが**無効・古い・競合している**場合 |

`freshness`の値（`stale`、キー欠落）を診断へ反映させる要求は既存4件のいずれにも無い。
手編集可能なsourceのauthority拒否も既存4件のいずれにも無い。

## 5. 公式全Testの実測

`.venv/bin/python3 -m tools.development.policy_test_runner --suite full --receipt <scratchpad>`
を実行した。receiptはscratchpad配下だけに置き、repositoryへは保存していない。

| 項目 | 実測値 |
| --- | --- |
| status | `failed`（exit code 1） |
| passed | 1007 |
| failed | 6 |
| errors | 0 |
| skipped | 0 |
| xfailed / xpassed | 0 / 0 |
| total | 1013 |
| command | `.venv/bin/python3 -m pytest -q` |
| python_version | 3.9.6 |
| pytest_version | 8.4.2 |
| fallback_used | `false` |
| config_digest | `890380460e063e508145450cf6e80865409d20035dfc2265b99c364f03b8b6ea` |
| source_state_digest | `bedd2cb0e42962a9f6936436aabfb593d3ef30cab51640adfaa4b80e7c0350d2` |

失敗6件は新規file`tests/test_work6a_current_work_projection_negative.py`の6件だけである。
既存Testの成功件数は承認Decision記載の`1007 passed`と一致し、既存の受入済み挙動を
1件も壊していない。

test関数の機械計数（`tests/test_*.py`をASTで解析）は次である。

| 対象 | 新規を含む | 新規を除く |
| --- | --- | --- |
| testファイル | 139 | 138 |
| `test_`関数 | 820 | 814 |

## 6. Work 6A項目との対応

`records/development/2026-08-06-work6a-negative-path-test-inventory-v1.json`に機械抽出した。
checklist 11件、plan 28件で、期待件数と一致した。区分の内訳は
`covered_by_existing_test` 17件、`red_added_now` 2件、`out_of_approved_scope` 20件である。

今回のRED 6件が対応するのは次の2項目だけである。

- `CL-6A-08`：Current Work Projectionの第二正本化、欠測推測、stale／競合の正常表示を検出する。
- `PL-6A-09`：Current Work Projectionが第二の状態正本になる、欠測を推測で埋める、
  またはstale／競合入力を正常表示する。

## 7. 変更していない範囲

- 実装コード（`tools/`配下すべて。`tools/development/session_log_bootstrap.py`を含む）。
- 既存Test（`tests/`配下の既存138ファイル）。
- fixture（`tests/fixtures/`配下すべて）。
- 既存記録（`records/`配下の既存file）。上書き、削除、無効化、stale化はしていない。
- Contract、Requirement、Plan、Policy、checklist、TODO。
- commit、push、tag、PR、CI、外部送信、LLM呼び出しは行っていない。作業終了時点で
  新規未追跡fileは3件（Test 1件、記録2件）だけである。

## 8. GREEN実装時の既知の制約（提案であって承認ではない）

**以下は今回の実測から判明した制約の記録であり、GREEN実装の承認でも、実装方針の
決定でもない。** GREEN実装範囲は別途Human判断で確定する。

1. `freshness`の判定を「`current`以外はすべて不完全」と一般化すると、既存fixture
   `tests/fixtures/development/session-log-bootstrap/projection-incomplete-inputs.json`の
   `freshness: unknown`が`missing`へ1件加わり、
   `test_projection_reports_missing_authority_without_guessing`の
   `assert projection["diagnostics"] == {...}`（`missing`が2要素の完全一致）を壊す。
   今回のREDが拘束しているのは「キー欠落」と「`stale`」の2つだけであり、
   `unknown`の扱いは拘束していない。

2. 「手編集可能なsource」の判定を拡張子（`.md`）や`docs/`配下といった一般規則にすると、
   Plan authority自身の`docs/current/reviewcompass3-plan-current.md`が拒否される。
   これは`projection-inputs.json`の`fixed_inputs`第1要素であり、
   `test_projection_renders_fixed_short_and_detailed_text`をはじめ複数の既存Testを壊す。
   拒否対象はidentityの限定列挙にする必要がある。今回のREDが要求しているのは
   `TODO_NEXT_SESSION.md`1件だけである。

3. `test_stale_input_text_does_not_assert_a_normal_next_action`は、short表示から
   `Implement Session Log Bootstrap mapping`が消えることを要求する。通常のshort表示は
   `next:{record['next']}`を出し、切替先の`_render_diagnostic`（697-711行）も`mode`を見ずに
   `next:`と`  - {projection['next']}`を出す。したがって診断表示へ切替えるだけでは足りず、
   stale時は`next`自体を修復指示へ差し替える実装が要る。
