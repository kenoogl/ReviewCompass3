# Evidence：group B（公式検証oracle）blocking 5件の修正

- 範囲固定：`records/session-handoffs/2026-08-10-claude-pilot-official-oracle-fix-scope-v1.md`
  （`c5cd440`、範囲レビューv1 `verified`：`134fed4`）＋`…-scope-v2.md`（`4fda1a6`）
- Human承認（2026-08-10）：
  1. 「組BからDまで自律的に実行。停止条件に触れたときと、修正の承認が要るときだけ止めよ」
     （包括承認record `271826a`。risk `high`確定・着手・RED開始・GREEN着手）
  2. 「conftest.pyの追加と既存テスト1件の更新を承認する」（scope v2の2点）
  3. 「契約recordの照合値更新を承認する」（§5の停止事象への裁定）
- 作成日：2026-08-10
- executor：Claude（Pilot。Reviewer=codex、Closer=codex、risk `high`）

## 1. commit系列

| 種別 | SHA | 内容 |
| --- | --- | --- |
| 包括承認record | `271826a` | Human裁定の転記のみ |
| SCOPE v1 | `c5cd440` | 範囲固定のみ |
| 範囲レビューv1 | `134fed4` | Codex作成。`verified`・blocking 0 |
| RED | `34e8a59` | test 4 fileのみ。13 failed / 35 passed、exit `1` |
| SCOPE v2 | `4fda1a6` | 停止事象の記録と2点の承認要請のみ |
| 修正RED | `e07183d` | `tests/test_work_unit_transition.py`の既存test 1件の契約更新のみ |

## 2. RED（実装前・単独実行）

- command：`.venv/bin/python3 -m pytest tests/test_policy_test_runner.py
  tests/test_policy_test_runner_summary.py tests/test_policy_test_runner_receipt_identity.py
  tests/test_declaration_red_map_check.py tests/test_declaration_red_verification.py
  tests/test_work_unit_transition.py`
- 結果：**13 failed / 35 passed**、exit `1`
- 追加した反証：F-B1（実行前summaryの流用1件・実合格0件2態様）、F-B2（source上書き1件）、
  F-B3（重複計上2件・収集error 2件）、F-B4（空対応表・型偽装・root脱出の3件）、
  F-B5（HEAD差・clean維持・repository identityの3件）
- **修正RED**（`e07183d`）：既存`test_preflight_reads_git_state_mechanically`の
  呼び出し形のみを新契約へ更新。理由はF-B5の修正が`git rev-parse --show-toplevel`と
  `git diff --name-only HEAD`を要するため。**修正前実装に対して`1 failed`**、
  修正後実装で合格を機械確認した（`git checkout 34e8a59 -- tools/development/work_unit_transition.py`で
  当て、確認後に復元）。検査性質（機械的にGit状態を読みblockedを返す）は保持。

### 2.1 RED作成中の事故と復旧（記録）

F-B2の反証を実repositoryのpathで書いたため、**実欠陥が発火して
`tools/development/policy_test_runner.py`がreceipt JSONで上書きされた**。
即座に`git checkout HEAD --`で復元し、SHA-256が範囲固定§3の記載
（`64724e0f…`）と一致することを確認した。以後、当該反証は使い捨ての
project root（`tmp_path`）だけを対象とする形へ直した。commitはしていない。

## 3. GREEN実装

| finding | 実装 |
| --- | --- |
| F-B1 | `policy_test_runner.execute`が、集計file（`<receipt>.summary.json`）の**実行前存在を拒否**（`test_summary_stale`）。さらに`status == "passed"`かつ`test_summary["passed"] < 1`を`test_summary_inconsistent`で拒否し、skip・xfailだけのsuiteを公式合格にしない |
| F-B2 | `_require_receipt_outside_source`を新設。receipt pathがproject root内なら`records/`配下限定とし、既存`.py`への出力とdirectory指定を拒否する |
| F-B3 | `pytest_summary`に`_already_counted`（nodeid＋段階の組で一度だけ数える。nodeidを持たないreportは従来どおり）と`record_collect_report`（収集errorをerrorsへ算入）を新設。`conftest.py`へ`pytest_collectreport` hookを結線（Human承認済み） |
| F-B4 | `declaration_red_map_check`で、`scope.kind=complete`の空対応表（宣言・test_filesの同時省略）を拒否、`red_now`のbool型を強制、対象test fileの**解決後path**をproject root内へ束縛 |
| F-B5 | `work_unit_transition.evaluate_transition`へ`head_difference`を追加し、porcelainが空でもHEADとのbytes差があればblocked。`preflight_next_work`は`git rev-parse --show-toplevel`で**要求rootとGit rootの同一実体**を束縛し、別rootへの差し替えを拒否 |

上流設計・config・schema・receipt schemaは未変更。CLI引数の削除もしていない。

## 4. Test実行の記録

| 区分 | command | 結果 | exit code |
| --- | --- | --- | --- |
| RED（実装前） | 上記6 file | 13 failed / 35 passed | `1` |
| 修正RED（実装前・当該1件） | `pytest tests/test_work_unit_transition.py::test_preflight_reads_git_state_mechanically` | 1 failed | `1` |
| targeted GREEN | 上記6 file | **48 passed** | `0` |
| 全test（契約pin更新前） | `pytest tests/` | 1 failed（§5の1件のみ）/ 1464 passed | `1` |
| 公式全Test（pin更新後） | `policy_test_runner --suite full --receipt records/development/2026-08-10-official-oracle-fix-test-receipt-v1.json` | **1465 passed**、status `passed`（failed 0・errors 0・skipped 0） | `0` |
| `git diff --check` | 各commit前 | 指摘なし | `0` |

## 5. 停止事象と裁定（Work 5B契約recordの指紋）

`records/development/2026-08-07-work5b-implementation-task-contract-v2.json`は
`tests/test_declaration_red_map_check.py`を`immutable_record`として指紋固定していた。
F-B4の反証3件を同fileへ**追加**したため指紋が変わり、`tests/test_work5b_contract.py`が
失敗した（範囲レビューv1でも見落とされた。pinはmodule側ではなくtest file側にあった）。

- 既存recordの変更は範囲固定の禁止事項のため停止し、Humanが
  **「契約recordの照合値更新を承認する」**と裁定した。
- 更新は**v2の該当1箇所のみ**（`901a4ea1…` → `b2e42d3f…`）。契約本文・受入条件・
  v1は変更していない。当該契約の受入条件「検査器test 6件がtestを変更せずGREEN」は、
  既存6件を変更せず反証3件を追加した本修正でも意味が保たれている。

## 6. 受入条件の対応

1. 危険側：判定record §4の反証（P1・P2・P3・S1・S2・D1・D2・D3・W1・W2）は
   すべて拒否またはstatus `failed`になった（§2の各testで固定）。
2. 正例：本repositoryの`--suite full`は`passed`のまま、件数1465は実行実績と一致。
   既存の正例testは弱めていない（更新は§2の既存1件の呼び出し形のみ）。
3. 対象6 test file：**48 passed**（RED前は34 passed）。公式全Test 1465 passed。
4. 上流設計・config・schemaは未変更。既存recordの変更は§5の1箇所のみ（Human承認済み）。

## 7. SHA-256

| file | SHA-256 |
| --- | --- |
| `tools/development/policy_test_runner.py` | `0f7072ab8a7c4ab9093f394858c7629e2f60c1d2b774d5fd3b640622998e5b24` |
| `tools/development/pytest_summary.py` | `febbdc68d64048c2351a343f83e121b2d06823515741d33ee1216203533d22b4` |
| `tools/development/declaration_red_map_check.py` | `151d2ef80a3ebb0dad6999dc1db63c0790541575ef0e7d7efd9da9ac7a507a61` |
| `tools/development/work_unit_transition.py` | `91726ff02cc7f86318c139913ec75d464521d2d7f389ed26cc227a45c88cb97e` |
| `conftest.py` | `1705384a41206185c38bda731706bf3ada2a024dec6f6ba3eb9f207e2350bc16` |
| `records/development/2026-08-07-work5b-implementation-task-contract-v2.json` | `5123b778cb12b8cf23f353d9725c0598f9214fdcf66d625f9385ef2ebd8a20f0` |
| `tests/test_policy_test_runner.py` | `58e3b8d5014009a17b9553e8b57afce5c68a263df48240b03bca1271bb73163a` |
| `tests/test_policy_test_runner_summary.py` | `b786c011833c4fab7752c3e0c6b072e8e94c4184b40f0ddaf59cef820f8a9d86` |
| `tests/test_declaration_red_map_check.py` | `b2e42d3fe719744468f0710ea0de93fe1681f1f763a8a218106972c28d1720b2` |
| `tests/test_work_unit_transition.py` | `d4b4f63af8b820d06cfcbdf101b71d26f49bfe265fe4d739aa00ebe0c857ea40` |
| 公式receipt | `e3bf3347bdb094fde6831dff51eeda04dd64d4b2fe1e34a6db09c2e4a1c9cd3e` |

## 8. 未実施

group C（5件）・D（7件）の計12件は判定recordのまま保持。TODO・checklist反映はCloser。
push・履歴書換えは未実施。
