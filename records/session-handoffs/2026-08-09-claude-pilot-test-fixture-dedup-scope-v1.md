# 範囲固定：テストfixture重複の共通化（deferred #7）

- 作成日：2026-08-09
- 作成者：Claude（Pilot）
- 状態：Humanのrisk確定・実装開始確認待ち

## 1. mode宣言と役割

```text
collaboration_mode: role_neutral_pilot_review
pilot: claude
reviewer: codex
closer: codex
work_item: deferred #7 テストfixture重複の共通化
           （裁定record：records/development/2026-08-09-deferred-items-triage-decision-v1.md）
```

受け渡しは`docs/development/pilot-driven-record-handoff.md`（Pilot起動・record正本方式）による。

## 2. risk提案

- 提案：`low`
- 根拠：テストfileと新helper moduleだけを変更し、product code・守り役code・schema・
  recordへ一切触れない。oracleは「fixture内容の同一性」と「テスト収集数・結果の不変」で
  機械判定できる。§3の`low`規定により、Humanがriskと実装開始を確認すれば範囲レビューなしで
  実装可能（過小分類の検査は完了レビューでReviewerが行う）。

## 3. 開始状態

- branch：`main`
- base commit：`ed79e5b8f6d72ef4c5166273346e4c78b9a6ab20`（裁定record commit）
- 開始時worktree：clean

## 4. 固定入力

| role | path | SHA-256 |
| --- | --- | --- |
| 対象（manifest fixture重複） | `tests/test_work7a_local_integrated_root_separation.py` | `7ec546a5aa6784cbce1c126f2950a80ee21d43459780aae8f267b7dbdd8b1d88` |
| 同上 | `tests/test_work7a_checkout_relocation.py` | `ab8f311dd6099085acec942c8e956523209756e4bcdc585be5e5b89e84b19258` |
| 同上 | `tests/test_work4a_rebuild_v3_e2e.py` | `1b6ee11c89c92e66c5c143e0f79919fc7f0e24adaf5ff79d6f93fd4aa1841476` |
| 同上 | `tests/test_work4a_rebuild_v3_1_e2e.py` | `89b40a67b564cc37dea7158015d28371f4c0a6ef855317ada0e4694fd413a57d` |
| 同上 | `tests/test_work4a_rebuild_v3_2_e2e.py` | `f980397da355a5634f540a192b244753f852f680261c6a010fabc0f2cc34c752` |
| 対象（session record fixture重複） | `tests/test_preservation_migration.py` | `bcaaf788c24723a7f239affc0733c997838a5189232a994f3a0572993cf15cf2` |
| 同上 | `tests/test_session_log_eventual_preservation.py` | `a4f704c4ac267e983c0831b2f1a6a97a64c6db335b8eae9d3efa032e897b3999` |
| mode手順書 | `docs/development/role-neutral-pilot-review-collaboration.md` | `762580c54ad830895f029d87eb1a7b1b062bf7de4ac780cfd30ae57ec508279e` |
| 受け渡し方式 | `docs/development/pilot-driven-record-handoff.md` | `93c84dd6ddd86af12175a4e844334ec9d62633f9be5ba9e97bcfbe3a435e92f0` |
| 共通レビュー基準 | `docs/development/work-review-protocol.md` | `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772` |

重複の実測：Project Manifest v2生成helperが5 file（`_write_manifest`／`_write_project`／
`_manifest`）、session会話record生成helper（`_write_jsonl`／`_claude_records`）が2 fileに
複製されている（grepで機械確認済み）。

## 5. 今回の作業

1. 新helper module `tests/shared_fixtures.py`（テストとして収集されない名前）に、
   Project Manifest v2生成とsession会話record生成の共通関数を定義する。
2. 対象7 fileの重複定義をhelper利用へ置き換える。**各fileが生成するfixtureの内容
   （manifest dict・jsonl bytes）は置換の前後で同一**とする。fileごとの差異（project_id、
   artifact_rootsの値、secret文字列等）はhelperの引数で表現し、意味を変えない。
3. assert文・テスト関数名・受入条件の意味は一切変更しない（fixture抽出のみ）。

TDDのRED commitは作らない。振る舞いの変更がなく「失敗すべき新Test」が存在しないため
（mode手順書§5「文書、試作、調査へRED／GREENを強制しない」の趣旨）。oracleは次節の
不変条件で代替する。

## 6. 受入条件（機械判定）

1. 置換前後で、対象7 fileの各テストが生成するfixture内容が同一である（実装Evidenceに
   同一性の確認方法と結果を記録する）。
2. 置換前後で、対象suiteの収集数・合格数が不変である（置換前の実測を記録してから着手）。
3. 公式全Test（policy_test_runner --suite full）が全件合格する。
4. 対象7 fileの差分がfixture定義の削除とhelper呼出しへの置換だけである
   （assert・関数名・parametrize不変）。
5. `git diff --check`合格、worktree clean。

## 7. 変更可能path

- `tests/shared_fixtures.py`（新規）
- §4の対象7 test file
- `records/development/2026-08-09-test-fixture-dedup-evidence-v1.md`（新規）
- `records/development/2026-08-09-test-fixture-dedup-receipt-v1.json`（新規）
- `records/session-handoffs/2026-08-09-claude-pilot-test-fixture-dedup-review-request-v1.md`（新規）

上記以外の変更が必要になったら停止する。product code・`tools/`配下・他のtest file・
TODO・checklist・Decision・既存Evidenceは変更しない。

## 8. 停止条件

1. fixture内容の同一性が保てない（fileごとの意味差をhelperで表現できない）と判明。
2. §7以外のpathの変更が必要。
3. 置換後にテスト収集数・結果が変わる。
4. 公式全Test・diff check・Digest照合の不合格。

## 9. commit境界

1. **SCOPE**（本commit）：本文書のみ。Humanのrisk確定・実装開始確認まで停止。
2. **REFACTOR**：helper新規＋対象7 file置換＋Evidence＋receipt。
3. **review request**：依頼書のみ（ignore検査exit 1確認のうえ）。完了レビューは
   Pilotがcodex CLIで起動し、判定recordの鮮度検査後にHumanへ報告する。
