# レビュー依頼：テストfixture重複の共通化（deferred #7）

- 作成日：2026-08-09
- Pilot：Claude／Reviewer：Codex／Closer：Codex
- collaboration mode：`role_neutral_pilot_review`、risk：`low`（Human確定
  「#7 risk lowを確定、実装開始を承認する」）
- 受け渡し：`docs/development/pilot-driven-record-handoff.md`（Pilot起動・record正本方式）

## 1. 対象

| 種別 | SHA | 内容 |
| --- | --- | --- |
| 裁定record | `ed79e5b8f6d72ef4c5166273346e4c78b9a6ab20` | Human仕分け（#7着手承認） |
| SCOPE | `91be5a9`（`git log`で全SHA特定） | 範囲固定v1（SHA-256 `4c9595d15195c5d3504bebcdb1f4b82fac282530a7e5e20d66b64c71beb86a36`） |
| REFACTOR | `7762c10`（同上） | helper新規＋対象7 file置換＋Evidence＋receipt |

REDなし（振る舞い変更なし。scope §5に根拠固定）。本依頼書のcommit SHAは自己参照のため
記載せず、Reviewerがgitから特定する。

## 2. Claim

- 実施：`tests/shared_fixtures.py`へ3系統（Manifest v2・Work 4A形manifest・合成会話record）を
  集約し、対象7 fileを薄い委譲へ置換。
- 結果：fixture同一性probe 9項目の前後hash一致、対象suite 129→129 passed、
  公式全Test 1338 passed（収集数不変＝helper誤収集なし）、`git diff --check`合格、
  commit後worktree clean。
- 未実施：product code・対象外file・TODO・checklist変更なし。#5・#1・#6は未着手。

## 3. 成果物SHA-256

| file | SHA-256 |
| --- | --- |
| `tests/shared_fixtures.py`（新規） | `6209ef0ddb6758b063378088816bc477d9a0a48f4f711d5ff41c82669b77b8a1` |
| `tests/test_work7a_local_integrated_root_separation.py` | `6bfcdb0a24df9fccf47e5f7f0f97a850240f72b28c5d86777b8876eefcbfc5cb` |
| `tests/test_work7a_checkout_relocation.py` | `c26aa5b8aff2f58a64bb6b46de33cfe721b83495bf14ec757f145198ec153175` |
| `tests/test_work4a_rebuild_v3_e2e.py` | `e188eeb11812a26893ac0e855e1df249af7c1ca548f1de2fdff57b3037ce9a3d` |
| `tests/test_work4a_rebuild_v3_1_e2e.py` | `094ab9283b1e168132d2280f57d8a6cf534220dcb2f89f744e88ce6d20c9da56` |
| `tests/test_work4a_rebuild_v3_2_e2e.py` | `e8efd391aa8bdac07844aed53a7aec63e901431d3492d4e785978b1bde9b617a` |
| `tests/test_preservation_migration.py` | `74317f9b8c30c8db4ec2f4f62266320a395b954113663a3a9f00a9e1c467ac5a` |
| `tests/test_session_log_eventual_preservation.py` | `9c753dc67143e40bb7016e0ed62a5f56f4ad84ed0d61aa60b7ba1ca482941b4a` |
| Evidence | `fc8863c8b56ea0078af1834efe2d0913de02cb1dc18574c24ff7329c2b46b8b2` |
| receipt | `cdd490b06c4f12d65c80e632d0674602554e53cf42eeffadc07d994cce55e4d7` |

## 4. Reviewerへの確認観点

- 差分がfixture抽出のみで、assert・関数名・parametrize・受入意味が不変であること
- fixture同一性probe（Evidence §2）の妥当性と、`low`分類が過小でないこと
- 収集数・結果の不変、公式receiptの再確認
- あわせてcommit `a109557`（起動promptひな型へのmodel provenance追記）の妥当性確認
