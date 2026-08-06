# Final Challenge 意図毀損検出（CL-6A-10） GREEN Evidence v1

- 正本設計：`docs/design/2026-08-06-final-challenge-intent-damage-proposal.md`
  （`approved`、2026-08-06 Human承認済み。規範宣言P1〜P7、§7の3点すべてを承認）
- 宣言→RED対応表：`records/development/2026-08-06-intent-damage-declaration-red-map-v1.json`
  （testの無いP 0件を機械確認済み）
- RED Evidence：`records/development/2026-08-06-intent-damage-red-evidence-v1.md`
- 実行環境：Python 3.9.6、pytest 8.4.2、公式venv runner、fallback `false`
- 実行時刻：2026-08-06T16:05:29+09:00（公式全Test receiptの`recorded_at`）
- RED基準commit：`275a877`（RED 7件＋境界1件を固定。公式全Test `1033 passed / 7 failed`）

## 0. 何を行ったのか（範囲の明示）

**同じTestを弱めずGREENにした。** RED基準commit `275a877`が固定した
`tests/test_final_challenge_intent_damage.py`（RED 7件＋境界1件）は1文字も変更しておらず
（§3参照。file SHA-256はRED Evidence記載値と現在で同一の`25ce60f3…`）、実装2 fileの
変更だけで8件すべてを通した。skip・xfail・assertion緩和・fixture変更は0件である。

**LLM呼び出しは実装していない。** 意図毀損所見は固定fixtureとして差し込まれる前提の
形式（`kind`・`origin`・`human_ruling`）だけを実装した。`run_stub_reviewer`は
`reviewer: deterministic_stub`・`calls_llm: False`のまま無変更であり、外部API・
サブエージェントのLLMレビュー導入は提案§3 P7・§5のとおり外部送信承認を伴う
別Task Contractである。

**後方互換を維持した。** `kind` fieldの無い既存形findingは`contract`として扱われ
（P1）、既存Test 1032件は無変更で合格し続けている（§3。提案§6の完了条件）。

変更fileは次の2件だけである（`git diff --stat`：`2 files changed, 44 insertions(+),
3 deletions(-)`）。

| file | 変更内容 |
| --- | --- |
| `tools/task_contract/execution.py` | P1〜P7の最小実装（+40/-3行。§2参照） |
| `tools/task_contract/__init__.py` | 定数2名（`FINDING_KINDS`・`FINDING_ORIGIN_ROUTES`）のexport追加のみ（+4行：import節42-43行、`__all__` 85-86行）。関数・ロジックの変更はない |

### 当初指示との差分と承認の経緯

当初の実装指示は「変更してよいのは`tools/task_contract/execution.py`の1 fileだけ」で
あった。しかしP1テスト（134-137行）はpackage `tools.task_contract`の属性として
定数2名を要求し（RED Evidence §3のP1実測`AttributeError: module 'tools.task_contract'
has no attribute 'FINDING_KINDS'`が固定した契約）、`__init__.py`は明示的なimport列と
`__all__`でexportを閉じているため、`execution.py`単独では清潔に達成できない
（前例`SEVERITY_CLASSES`・`ORIGIN_CLASSES`・`PROVENANCE_EDGE_ORDER`も定義module＋
`__init__.py` exportの2 file構成である）。実装担当は`sys.modules`への属性注入という
迂回を行わず、`execution.py`実装完了・7/8 passedの時点で**停止して報告**し、
organizerが「`__init__.py`への定数2名のexport追加」を明示承認した
（2026-08-06。承認文言：「`__init__.py`への2行のexport追加を承認します」。
`sys.modules`注入は不可の指示つき）。本Evidenceの変更範囲2 fileはこの承認に基づく。

**行っていないこと**は次である。

- `tests/`配下の変更（既存143 fileとも0件。対象test fileも1文字も変更していない）。
- `execution.py`・`__init__.py`以外の実装変更（`identity.py`・`contract.py`・
  `definition_challenge.py`は無変更。§1のSHA-256で固定）。
- STOP_CODES・RECORD_KINDSへの追加（P4は既存の`human_decision_missing`を再利用）。
- 既存記録、TODO、checklist、config、schema、Current Planの変更。
- commit、push、外部送信、LLM呼び出し。

`git status --porcelain`は実装2件の変更（` M`）と、本Evidence 1件の未追跡（`??`）
だけを示す。

## 1. 固定入力（機械計算したSHA-256）

`shasum -a 256`で計算した。実装2 fileは**変更後**の値である。

| path | SHA-256 |
| --- | --- |
| `docs/design/2026-08-06-final-challenge-intent-damage-proposal.md` | `7f8cd3bc6da61efbc1fbcef7b93007e1534e8b77d53e329fbcd8026bf143baf6` |
| `records/development/2026-08-06-intent-damage-declaration-red-map-v1.json` | `80decdaa37ac8a0f977128d7a7866c6e00c6defd58faacf32eceeeb2a90ae3d0` |
| `records/development/2026-08-06-intent-damage-red-evidence-v1.md` | `9950c141e5dcb6bd485857fcf3e34ae2372f61bee705a84cf92aa3fafedde047` |
| `tests/test_final_challenge_intent_damage.py`（RED時＝現在。無変更） | `25ce60f3d6893681776bb636baf7ff02ecb51556ed92b6159a5b2f3f75371391` |
| `tests/test_first_review_task_contract_e2e.py`（無変更。fixture再利用元） | `cc99faaa4813aa629c9640431e31d4da635890bc5ec1e1f30c631d06c513661f` |
| `tools/task_contract/execution.py`（変更後） | `32035909a96e6ce28f19792716b5d3e49b7132f6f8e316c1287679c9da291cd0` |
| `tools/task_contract/__init__.py`（変更後） | `ba556e79e15221f55c4e59d1f90ce6e8fff879da0183f19b8d35bb3f6c4e623d` |
| `tools/task_contract/identity.py`（無変更） | `a85f51617b8e9d04a5fed63b2bc8ba97af26118e26dc307cb02fe0633f551774` |

提案SHA `7f8cd3bc…`と対応表SHA `80decdaa…`はRED Evidence §1の記載値と一致した。
test file SHA `25ce60f3…`も同記載値と一致し、GREEN実装がtestを変更していないことを
機械的に示す。実装2 fileのRED時の値（`execution.py` `606eacea…`、`__init__.py`
`605ce9c7…`）はRED Evidence §1に固定されている。

## 2. P1〜P7のRED→GREEN対比

行番号はすべて変更後の`tools/task_contract/execution.py`のものである
（`__init__.py`のみ明記）。RED時の失敗はRED基準commit `275a877`での実測
（RED Evidence §3）に基づく。

| P | test（対応表どおり） | RED時 | GREEN後の実装箇所 |
| --- | --- | --- | --- |
| P1 | `test_p1_intent_damage_kind_and_origin_are_constructible`（RED） | `AttributeError`（`FINDING_KINDS`不在） | 語彙定数`FINDING_KINDS`（26行）・`FINDING_ORIGIN_ROUTES`（28行）、`__init__.py`でのexport（42-43行・85-86行）。`kind`・`origin`つきfindingは`validate_record`（最小不変条件のみ検査。無変更）とConformance・Final Challengeの評価経路で受理され、fieldは保持される |
| P1後方互換 | `test_p1_legacy_findings_without_kind_keep_passing`(境界） | 成功 | `_finding_kind`（282-285行）が`kind`省略時`contract`を返す。stub生成findingは無変更（`run_stub_reviewer` 249-274行、非変更）で従来どおりpassed/failedになる |
| P2 | `test_p2_blocking_intent_damage_does_not_fail_conformance`（RED） | `conformance failed`（種別を見ず全errorを計数） | `_severity_counts`（288-295行）が`contract`種別のfindingだけを計数。`evaluate_conformance`（298-315行）は判定式無変更でこれに追随し、`intent_damage`のerrorでは落ちない |
| P3（中核） | `test_p3_accepted_blocking_intent_damage_fails_final_challenge`（RED） | 前提のconformance passedで失敗（P2未対応）。P2実装後もConformanceを写すだけで失敗 | `evaluate_final_challenge`（318-349行）：`human_ruling: accepted`かつseverity `error`の`intent_damage`が1件でもあれば（342-346行）、Conformance passedでも`status`を`failed`へ（347-349行）。「Contract適合なのに最終審査で落ちる」中核負例が成立 |
| P4 | `test_p4_pending_intent_damage_stops_final_challenge_fail_closed`（RED） | `DID NOT RAISE`（採否未了でもverdictが返る） | `human_ruling`省略時は`pending`として扱い（340行、fail-closed）、`pending`が1件でもあれば`ContractError("human_decision_missing", finding_id)`で停止（339-341行）。severity `error`・`warning`とも同様に停止する |
| P5 | `test_p5_multiple_intent_damage_findings_are_kept_without_auto_merge`（RED） | 判定のassert（conformance passed）で失敗。保持は成功済み | findingの統合・書換え・多数決の実装は一切無い。重複・競合3件はfinding_setにそのまま残り、rejected 2件対accepted 1件でもaccepted 1件（342-346行）でfailedになる |
| P6 | `test_p6_rejected_intent_damage_does_not_fail_final_challenge`（RED） | conformance passedのassertで失敗 | `rejected`は`pending`検査（339-341行）を通過し、`accepted_blocking`（342-346行）にも入らないため判定に影響しない。`human_ruling_reason`はfindingに保持されたままfinding_setに残る |
| P7 | `test_p7_origin_routes_are_formally_equivalent`（RED） | conformance passedのassertで失敗（1経路目） | 判定（339-349行）は`origin.route`を参照せず、4 route種は形式上等価。`origin`（routeとidentity）はfindingに保持される。route種の語彙は`FINDING_ORIGIN_ROUTES`（28行）で宣言 |

REDテストが要求していない拒否（未知`kind`・未知`origin.route`・不正`human_ruling`値の
runtime検証）は追加していない（当初指示「要求されている検証だけを入れる」に従う。
§5の限界4参照）。

## 3. Testの実測

いずれも自分で実行して確認した。

| 対象 | command | 結果 |
| --- | --- | --- |
| 対象Test | `.venv/bin/python3 -m pytest -q tests/test_final_challenge_intent_damage.py` | **`8 passed in 0.06s`** |
| 隣接する既存Test | `.venv/bin/python3 -m pytest -q tests/test_first_review_task_contract_e2e.py tests/test_work5a_definition_challenge.py` | **`83 passed in 0.37s`**（RED時と同件数） |
| 公式全Test | `.venv/bin/python3 -m tools.development.policy_test_runner --suite full --receipt <scratchpad>` | **`1040 passed`**（failed 0） |

公式全Test receiptの内訳は次である。receiptはscratchpad配下だけに置き、
repositoryへは保存していない。

| 項目 | 実測値 |
| --- | --- |
| status | `passed`（exit code 0） |
| passed / failed / errors / skipped | 1040 / 0 / 0 / 0 |
| xfailed / xpassed | 0 / 0 |
| total | 1040 |
| command | `.venv/bin/python3 -m pytest -q` |
| python_version / pytest_version | 3.9.6 / 8.4.2 |
| fallback_used | `false` |
| config_digest | `890380460e063e508145450cf6e80865409d20035dfc2265b99c364f03b8b6ea` |
| source_state_digest | `af1cc151bea84dbeec3fd2398823495b6cd36d4102995e511743c65944ffabaa` |
| recorded_at | `2026-08-06T16:05:29+09:00` |

RED基準の`1033 passed / 7 failed`（total 1040）から、totalは変わらず失敗7件がすべて
GREENになった。`config_digest`はRED時と同一である。既存Test 1032件は無変更で
合格し続けている（1040の内訳＝既存1032＋新規8）。

### 既存Testを弱めていないこと

| 検証 | 結果 |
| --- | --- |
| 変更fileの数 | 実装2件のみ（`execution.py`・`__init__.py`。§0の承認経緯参照） |
| GREEN実装時の`tests/`変更 | 0件（対象test fileのSHA-256はRED時と現在で同一の`25ce60f3…`） |
| fixture変更 | 0件 |
| skip／xfail／assertion緩和 | 0件 |
| 既存record変更 | 0件（本Evidenceはnew-only） |

## 4. 変更していない範囲

- `tests/`配下すべて。1 byteも触っていない。
- `tools/`配下のうち`task_contract/execution.py`・`task_contract/__init__.py`以外
  すべて（`identity.py`・`contract.py`・`definition_challenge.py`を含む。
  `identity.py`は§1のSHA-256で無変更を固定）。
- `__init__.py`の変更は定数2名のexport追加（4行）だけであり、既存のimport・
  `__all__`の既存項目・docstringは無変更である。
- finding生成経路`run_stub_reviewer`の出力（既存findingは`kind`省略のまま＝
  `contract`扱い）、`record_human_decision`、Provenance検証、accept_artifact。
- STOP_CODES（`human_decision_missing`を再利用）、RECORD_KINDS、severity語彙
  （blockingは既存の`error`を再利用。新fieldを足していない）。
- 既存記録（`records/`配下の既存file）、TODO、checklist、config、schema、
  Current Plan。上書き、削除、無効化、stale化はしていない。
- commit、push、tag、PR、CI、外部送信、LLM呼び出しは行っていない。

## 5. 残っている限界

1. **LLMレビューの実導入は別Task Contractである。** 今回実装したのは所見を受け取る
   形式（`kind`・`origin`・`human_ruling`）と判定だけであり、`intent_damage`所見を
   実際に生成する担い手（外部API・サブエージェントのLLM、Human）は未接続である。
   導入は外部送信承認を伴う別Task Contractとし、Capability Adapterとして交換可能に
   する（提案§3 P7・§5）。
2. **複数reviewer・複数roundのharnessは範囲外である**（REQ-EXEC-004の全体。提案§5）。
   P7で固定したのはfixture所見のroute種の形式等価な受理と保持までである。
3. **意図毀損の意味判定は機械が行わない。** 機械は種別・採否・blockingの形式だけを
   判定する（提案§6）。所見の意味の当否はHuman採否（`human_ruling`）に属し、
   採否をrecordとして残す仕組み（採否の記録形式・Provenanceへの載せ方）は
   finding内のfieldにとどまる。
4. **語彙のruntime検証は最小である。** `FINDING_KINDS`・`FINDING_ORIGIN_ROUTES`は
   宣言された閉じた語彙だが、未知の`kind`・未知の`origin.route`・語彙外の
   `human_ruling`値を`ContractError`で拒否する検査は、REDテストが要求していないため
   追加していない（未知の`human_ruling`値は`pending`でも`accepted`でもない値として
   判定に影響しない）。必要になれば改善候補として既存の経路（観測記録→改善候補→
   Human仕分け）へ載せる。
5. **`warning_count`は`contract`種別の計数である。** `_severity_counts`の種別分離
   （P2）に伴い、`final_challenge_verdict`の`warning_count`は`contract`種別の
   warningだけを数える。`intent_damage`のwarningはHuman採否（P4のfail-closed）で
   扱われるため二重計上しない。既存Testはこの点を含め全件無変更で合格している。
