# レビュー依頼：Work 7A第2項 前駆slice — read-only Git捕捉とcheckout移動後照合

- 作成日：2026-08-09
- Pilot：Claude（本依頼書の作成者）
- Reviewer：Codex
- Closer：Codex
- collaboration mode：`role_neutral_pilot_review`
- risk：`high`（Human確定）
- 判定依頼：`work-review-protocol.md`と下記範囲固定文書に基づく独立レビュー

## 1. 範囲固定文書と範囲レビュー

| 文書 | path | SHA-256 |
| --- | --- | --- |
| 範囲固定v2（有効） | `records/session-handoffs/2026-08-09-claude-pilot-work7a-checkout-relocation-scope-v2.md` | `f127351d05bc621af95a042506dc726790ca59ecc928cec4c34257ee23d473a8` |
| 範囲レビューv1（scope v1対象・保持） | `records/session-handoffs/2026-08-09-codex-scope-review-work7a-checkout-relocation-v1.md` | `76d4084194da1d412a30126c4d1813bfd5e0c958833468650cebf6ecaf93c590` |
| 再評価record（verified・条件付き・blocking 0） | `records/session-handoffs/2026-08-09-codex-scope-reevaluation-work7a-checkout-relocation-v1.md` | （Reviewer自作recordのためcommit `3ef81403…`から照合） |

Human承認：risk `high` 確定とmode宣言（2026-08-09）、裁定「分割案1」（前駆slice化・
耐久Binding／Verification Run後続化・checkbox未完了維持）、再開承認
「再評価record追加を確認した。RED開始を承認する。」（再評価record commit後）。

## 2. commit列（baseから最新実装commitまで）と各役割

| SHA | 役割 | 内容 |
| --- | --- | --- |
| `3970e1ebd2e8cb9346f9169091eff2986493468c` | Reviewer | 範囲レビューv1 record（scope v2のbase） |
| `4990ba64c7035d06fa77e1e3a68fb5a8d36a59f6` | Pilot | SCOPE v2（範囲固定文書のみ） |
| `eb4b59b31f0a9f0f0f173e0d6430569b3f2c82cf` | Reviewer | 範囲レビューv2 record |
| `3ef814034ab7823c591a41df0ad3bf6d6a01cc41` | Reviewer | 再評価record（verified・条件付き） |
| `a7e58eb2f212c78e2c62e95947718fcf4da3ad9f` | Pilot | RED：`tests/test_work7a_checkout_relocation.py`のみ（19 Test） |
| `86f0f63cb24feda35de740f835a04b8c0782eb68` | Pilot | GREEN：実装・GREEN Evidence・公式receiptのみ |

本依頼書のcommit SHAは（自己参照になるため）記載せず、Reviewerがgitから特定する。

## 3. Claim

- **実施**：RED着手前にscope v2固定入力22件のSHA-256全件再照合（一致）。REDを単独実行し
  19件全てが新module未実装（`ModuleNotFoundError`×19を機械確認）だけを理由に失敗・
  exit `1`を確認してcommit。実装は新規`tools/deployment/checkout_relocation.py`のみで
  GREEN化し、Testは未変更。
- **結果**：targeted 19 passed（exit `0`）、関連回帰83 passed（exit `0`）、公式全Test
  1334 passed・status `passed`（exit `0`、receipt再読込みでfailed 0確認）、
  `git diff --check`指摘なし。
- **判断（Pilotの実装内裁定）**：`repository_id`導出＝HEAD履歴root commit群の辞書順
  `"\n"`連結のSHA-256（暫定lineage ID限定、再評価条件1をdocstringへ明記）。
  checkout識別＝`rev-parse --absolute-git-dir`のcanonical path。Snapshot束縛＝
  `content_digest`参照で、束縛不一致は`change_set_binding_mismatch`で拒否
  （再評価条件2のTestあり）。
- **未実施**：耐久Binding保存・復元、Verification Run復元、binding directory新設、
  `RECORD_KINDS`追加、TODO・checklist反映（Closer担当）、Work 7A第2項checkbox完了
  （Human裁定により本sliceでは行わない）。
- **提案（完了扱いにしない）**：Closerの完了projectionは、checkboxを開けたまま
  TODO「次の一作業」を耐久Binding後続sliceへ向ける（scope v2 §12）。

## 4. 成果物のpathとSHA-256

| file | SHA-256 |
| --- | --- |
| `tests/test_work7a_checkout_relocation.py`（RED以後未変更） | `db68cc42b4020ff7e5ad6ee485aa7ad401df5ccd18fd6f57dae93ef5378586e1` |
| `tools/deployment/checkout_relocation.py` | `e48d65dbb1ef39420c44e2c05fcf55da3100bba92a5b5d6d7a185340b00b434c` |
| `records/development/2026-08-09-work7a-checkout-relocation-green-evidence-v1.md` | `2d6f2e6daa579d9445c7ce67a853989c6fddabe8e7cd4ecb23b7849ebf89c8cd` |
| `records/development/2026-08-09-work7a-checkout-relocation-green-test-receipt-v1.json` | `b1084387a999b9dc3349e503bf0bb4748eb8dc33ca1bb3f28ada61b15495446d` |

## 5. 禁止操作の未実施・worktree・停止地点

- 固定入力実装（`tools/layout/baseline.py`・`tools/task_contract/`配下・
  `tools/deployment/local_integrated_roots.py`）・TODO・checklist・Plan・Decision・
  既存Evidence・scope v1／v2：未変更。
- production APIはread-only Gitのみ（`--no-optional-locks` global option、NUL区切り、
  `--find-renames=50%`明示、config隔離）。fixtureのGit構築操作はTest内・`tmp_path`限定。
- 実ホーム・既存利用者repository・既存保全data：accessなし。
- push・tag・PR・amend・rebase・reset・履歴書換え・`git add -A`／`git add .`：未実施
  （stageは全て明示path。repository本体への操作について）。
- 各handoff commit前に`git check-ignore --no-index`を単独実行し、exit `1`のみ続行
  （SCOPE v2・本依頼書とも exit `1`）。
- worktree：本依頼書commit時点でclean。
- 停止地点：本依頼書のcommitをもってPilotは停止する。Reviewerの独立レビュー
  （`high`のためPilot fixtureに無い反証を最低1件含む）と、その後のCloser完了projection・
  Human判断まで次の作業へ進まない。

## 6. Reviewerへの確認観点（依頼）

- commit列・変更path・範囲外変更なし・worktree確認
- 成果物・Evidence・receiptの再読込みとDigest再計算
- scope v2受入条件13件と再評価条件2件のTest対応、targeted・関連・公式全Testの独立再実行
- 上流authority（Work 3承認identity fields・stale trigger）からの独立導出による受入判定
- 非blocking実装時確認事項3件（`--no-optional-locks`位置、NUL区切り・rename threshold、
  config隔離）の実装確認
- Pilot fixtureに無い新しい反証の機械実行（`high`）
