# Work 5B 宣言→RED対応表検査器 GREEN Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-WORK5B-START-001`、`DEC-WORK5B-IMPLEMENTATION-READY-001`
- Contract：`TC-WORK5B-DECLARATION-RED-MAP-CHECK-001`
  （`records/development/2026-08-07-work5b-implementation-task-contract-v1.json`）
- RED Evidence：`records/development/2026-08-07-work5b-red-map-checker-red-evidence-v1.md`

## 1. WI-5B-1：GREEN実装

`tools/development/declaration_red_map_check.py`を新設した。対応表JSONとtest fileを読み、
(1)列挙test関数の実在（AST解析）、(2)testの無い宣言0件、(3)宣言に結ばれないtest 0件を
機械判定し、fail-closed（対応表・test fileの欠落・解析不能は不合格）で決定的な結果を返す。
hook・自動実行・commit連動は無い。既存moduleは変更していない。

実装中の修正1回：宣言側とtest_files側の両方に載るtest名を二重に数えていた欠陥をtargeted REDで
検出し、file×名前で一度だけ数える形へ修正した（固定testは変更していない）。

- targeted：`tests/test_declaration_red_map_check.py` `6 passed`、exit `0`
- Contract結線：`tests/test_work5b_contract.py` `5 passed`（RED時に固定、Contract作成で成立）
- 公式全Test：`1066 passed`、exit `0`。既存Testは弱めていない。

## 2. WI-5B-2：第一実運用（既存4枚のread-only検査）

結果recordは`records/development/2026-08-07-work5b-checker-first-run-v1.json`
（`RC3-WORK5B-CHECKER-FIRST-RUN-001`）。4枚中3枚`passed`、1枚`failed`。

**自己検査**：検査器自身の対応表（C1〜C4）は`passed`。Contract受入条件を満たす。

**実在の所見2件（Intake V4対応表、2026-08-06作成）**：

1. `listed_test_missing`：対応表が列挙する
   `test_n9_authority_reference_candidate_passes_the_v3_validator`は現存しない。N7-N9修正
   （`DEC`記録：`records/development/2026-08-06-intake-v4-n7-n9-amendment-decision-v1.md`）に
   伴う改名後の実test名は`test_n9_authority_reference_candidate_binding_stays_pinned`であり、
   不変recordである対応表は改名へ追随していない。
2. `test_file_listing_invalid`：同対応表の`tests/test_issue_intake_v4.py`欄はlist形式でなく
   dict形式（`changed_tests_only`）の別形であり、検査器はfail-closedで不合格とした。

所見への対処（対応表v2でのsupersede、または検査器の別形対応）は本作業単位で行わない。
レビュー結果と修正作業の分離（work-review-protocol §2-5、§7）に従い、Human判断へ渡す。
対応表4枚は一切書き換えていない。

## 3. WI-5B-3：post-write verification・Provenance・分割commit

- post-write：実装module、first-run record、本Evidenceを再読込し、first-run record内の
  対応表4枚のSHA-256が実fileと一致することを確認した（record生成時に機械転記）。
- Provenance結線：開始承認`DEC-WORK5B-START-001`→実装前検索record（gate `start_allowed`）→
  Contract→RED（対応表C1〜C4、testの無い宣言0件）→議論証跡
  `DEC-WORK5B-DISCUSSION-OUTCOMES-001`→`DEC-WORK5B-IMPLEMENTATION-READY-001`→GREEN→
  第一実運用record。各段は独立commitに分割されている（開始承認`8f27428`、検索record`abe689f`、
  RED`7da65e2`、Contract`4f0976b`、議論・ready`73ea7cb`、GREEN・実運用は本Evidenceのcommit）。
- 恒久tool化の成立：本検査器のGREENにより、5枚目以降の宣言→RED対応表の照合はその場AST照合
  ではなく本検査器で行う（`DEC-WORK5B-START-001` §1-3の完了）。

## 4. 残余と限界

- Intake V4対応表の所見2件の処置はHuman判断待ち。
- 検査器はtestの実在と対応の全射・単射だけを見る。`red_now`主張（現在失敗するか）の実行照合は
  承認範囲外であり、必要になれば別途Human判断とする。
- 本検査器は守り役codeであり、`ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001`の反証レビュー対象に
  含まれる（Contract `risk_basis`のとおり）。
