# GREEN Evidence：Work 7A第2項 前駆slice — read-only Git捕捉とcheckout移動後照合

- 範囲固定：`records/session-handoffs/2026-08-09-claude-pilot-work7a-checkout-relocation-scope-v2.md`
  （SHA-256 `f127351d05bc621af95a042506dc726790ca59ecc928cec4c34257ee23d473a8`）
- 再評価record（条件付きverified・blocking 0）：
  `records/session-handoffs/2026-08-09-codex-scope-reevaluation-work7a-checkout-relocation-v1.md`
- 作成日：2026-08-09
- executor：Claude（Pilot。mode `role_neutral_pilot_review`、Reviewer=Codex、Closer=Codex、risk `high`）

## 1. commit系列

| 種別 | SHA | 内容 |
| --- | --- | --- |
| scope v2 base | `3970e1ebd2e8cb9346f9169091eff2986493468c` | 範囲レビューv1 record |
| SCOPE v2 | `4990ba64c7035d06fa77e1e3a68fb5a8d36a59f6` | 範囲固定v2のみ |
| 範囲レビューv2 record | `eb4b59b31f0a9f0f0f173e0d6430569b3f2c82cf` | Codex作成 |
| 再評価record | `3ef814034ab7823c591a41df0ad3bf6d6a01cc41` | Codex作成。verified・条件付き・blocking 0 |
| RED | `a7e58eb2f212c78e2c62e95947718fcf4da3ad9f` | `tests/test_work7a_checkout_relocation.py`のみ追加（589行、19 Test） |

Human再開承認（「再評価record追加を確認した。RED開始を承認する。」）をRED着手前に受領。
RED着手前にscope v2の固定入力22件のSHA-256を全件再照合し一致を機械確認した。

## 2. RED（実装前・単独実行）

- command：`.venv/bin/python3 -m pytest tests/test_work7a_checkout_relocation.py`
- 結果：19件収集、19件全てが新module `tools.deployment.checkout_relocation` の未実装
  （`ModuleNotFoundError`、該当メッセージ19件を機械確認）だけを理由に失敗
- exit code：`1`
- environment：Python 3.9.6、pytest 8.4.2、git 2.50.1（fixture構築用。`tmp_path`内のみ）
- RED時点のTest digest：`db68cc42b4020ff7e5ad6ee485aa7ad401df5ccd18fd6f57dae93ef5378586e1`
  （GREENでもTestは未変更のため現digestと同一）

## 3. GREEN実装

新規`tools/deployment/checkout_relocation.py`のみ（4スペースindent、namespace package、
`__init__.py`なし）。公開API：`RelocationError`（安定stop code）、
`capture_repository_binding`、`capture_source_snapshot`、`derive_change_set`、
`rebind_relocated_checkout`、`verify_source_snapshot`、`verify_change_set`。

- **read-only Git限定**：production APIは`rev-parse`・`rev-list`・`status --porcelain -z`・
  `diff --name-status -z`・`ls-tree`・`ls-files`だけを使い、objects・refs・index・worktreeを
  変更しない。fixture構築のGit変更操作はTest側helperだけが行い、`tmp_path`内に限定。
- **実Gitからの取得**：base・head commitは`rev-parse --verify <rev>^{commit}`で存在検証つき
  解決。staged／dirty／untrackedは`status --porcelain -z --untracked-files=all`から機械取得。
- **暫定lineage ID（再評価条件1）**：`repository_id`はHEAD履歴のroot commit群の辞書順連結の
  SHA-256。module docstringに「本前駆slice限定の暫定lineage IDであり耐久repository identity
  ではない」と明記し、耐久保存・checkbox完了の根拠に使わない。
- **Snapshot束縛（再評価条件2）**：Change Setは`base_snapshot_id`／`candidate_snapshot_id`を
  2つのSnapshot recordの`content_digest`へ束縛し、束縛先と異なるSnapshotでの照合を
  `change_set_binding_mismatch`で拒否する。
- **record整合**：全捕捉recordは`canonical_content_digest`（共通正本）でdigestを持ち、
  改竄は`record_digest_mismatch`で拒否。
- **fail-closed**：予期しない`OSError`・`RuntimeError`・subprocess例外は、連鎖
  （`__cause__`／`__context__`）を残さずhandler外で安定stop codeへ変換する
  （第1項の例外連鎖修正の契約を踏襲）。例外文はstop codeのみで、host path・未検査内容を
  含めない。

### 非blocking実装時確認事項（再評価record §3）の反映

1. `--no-optional-locks`は**global option**としてsubcommandの前に配置（全production呼出し
   共通の`_run_git`で一元化）。あわせて`GIT_OPTIONAL_LOCKS=0`も設定。
2. path出力は`-z`（NUL区切り）を明示し、rename検出は`--find-renames=50%`をcommand上で
   明示（利用者configの`status.renames`等に依存しない）。renameのTestは同一内容の
   `git mv`（類似度100%）で決定的に固定。
3. identity導出への利用者Git config混入を、`GIT_CONFIG_GLOBAL`／`GIT_CONFIG_SYSTEM`を
   `os.devnull`へ向ける環境隔離で遮断（production・fixture両方）。

## 4. Test実行の記録

| 区分 | command | 結果 | exit code |
| --- | --- | --- | --- |
| RED（実装前・単独） | `.venv/bin/python3 -m pytest tests/test_work7a_checkout_relocation.py` | 19 failed（全件ModuleNotFoundError） | `1` |
| targeted GREEN | 同上command | 19 passed | `0` |
| 関連回帰 | `.venv/bin/python3 -m pytest tests/test_layout_baseline.py tests/test_work7a_local_integrated_root_separation.py tests/test_first_review_task_contract_e2e.py` | 83 passed | `0` |
| 公式全Test | `.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt records/development/2026-08-09-work7a-checkout-relocation-green-test-receipt-v1.json` | 1334 passed、status `passed` | `0` |
| `git diff --check` | RED commit前・GREEN commit前 | 指摘なし | `0` |

公式receiptは再読込みし、status `passed`・exit `0`・1334件全合格・failed 0を機械確認済み。
RED commit後、Testは未変更。

## 5. 受入条件の対応（scope v2 §8 → Test）

- 正例1〜5：実Gitからのidentity・状態取得／決定性／clone・worktreeのBinding区別／
  移動後のrebindとSnapshot照合／A/M/D/R区別とSnapshot束縛 — 各1 Test（束縛の不一致拒否は
  追加1 Test、再評価条件2）。
- 負例6〜11：無効commit（×2）／symlink逸脱（外部内容の非取込みと連鎖非漏洩を含む）／
  untracked欠落／index・dirty不一致（×2）／Manifest欠落・改変（×2）／branch名・pathの
  非identity — 計8 Test。
- 境界12〜13：clean clone間のmanifest digest一致／record改竄拒否（×3） — 計4 Test。

合計19件（parametrize展開後）、全て合格。

## 6. SHA-256

| file | SHA-256 |
| --- | --- |
| `tools/deployment/checkout_relocation.py` | `e48d65dbb1ef39420c44e2c05fcf55da3100bba92a5b5d6d7a185340b00b434c` |
| `tests/test_work7a_checkout_relocation.py` | `db68cc42b4020ff7e5ad6ee485aa7ad401df5ccd18fd6f57dae93ef5378586e1` |
| 公式receipt（同上JSON） | `b1084387a999b9dc3349e503bf0bb4748eb8dc33ca1bb3f28ada61b15495446d` |

## 7. 修正版（独立レビューv1のFindings反映）

独立レビューv1（`records/session-handoffs/2026-08-09-codex-review-result-work7a-checkout-relocation-v1.md`、
判定`report_execution_mismatch`）の3 Findingについて、Humanの修正承認を受けて次を修正した。
**§1〜§6の初版Claim・Digestのうち、実装・Test・receiptに関するものは本節で置換される
（stale）。** 修正RED commitは`2b27b4d4a00a7ee6989d29fc6a35e92ef01d8b56`
（Test 3件追加のみ。実装前は3件とも反証どおり失敗、先行19件合格、exit `1`）。

- **RR-P1-001**：Change Set導出・照合を、commit間delta（A/M/D/R）に加えて、両Snapshotが
  記録したindex・worktree・対象untrackedの状態差を合成する`_combined_change_items`へ変更。
  同一pathはcommit側kindを優先。これに伴い`tracked_changes`の各entryへ
  `content_identity`（index=blob oid、worktree=現内容SHA-256）を追加した。これは
  in-memory値schema内の表現追加であり、承認済みidentity fields（top-level）は不変。
  同一HEADのdirty・staged・対象untrackedが空Change Setにならないことを新Testで固定。
- **RR-P1-002**：捕捉時に実HEADを機械取得し、caller指定`head_commit`を期待値として
  一致必須にした。不一致は新stop code `head_commit_mismatch`で拒否（新Testで固定）。
- **RR-P2-003**：`_git_environment`で`GIT_CONFIG*`全て（COUNT／KEY_*／VALUE_*含む）を
  除去してからfile configをdevnullへ固定し、`GIT_DIR`等のrepository位置差替え変数も
  除去した。`core.fileMode=false`注入でdirtyを隠せないことを新Testで固定。

修正後のTest実行（全て単独command）：

| 区分 | 結果 | exit code |
| --- | --- | --- |
| 修正RED（実装前・単独） | 3 failed（新規のみ・反証どおり）／19 passed | `1` |
| targeted GREEN | 22 passed | `0` |
| 関連回帰（同§4のcommand） | 83 passed | `0` |
| 公式全Test（同§4のcommand・receipt更新） | 1337 passed、status `passed`（再読込みでfailed 0確認） | `0` |
| `git diff --check` | 指摘なし | `0` |

修正後のSHA-256（§6を置換）：

| file | SHA-256 |
| --- | --- |
| `tools/deployment/checkout_relocation.py` | `5c353c6f2815dbe434d5fab5374ac3af2d6996eddc417b9fa30930402778f589` |
| `tests/test_work7a_checkout_relocation.py` | `2a5c32ae22104217219e26a5c82b0de26b56de9dd3226a06e07765de0e273eda` |
| 公式receipt（更新済み） | `e653387a9f35eb04fe7951c670b9c21a6bdefbe699f70871e0a0d2e94e27684e` |

## 8. 禁止境界と未実施範囲

- `tools/layout/baseline.py`・`tools/task_contract/`配下・
  `tools/deployment/local_integrated_roots.py`・TODO・checklist・Plan・Decision・
  既存Evidence・scope v1／v2：未変更。
- Project Manifestの書換えによる移動表現、Bindingの耐久保存・binding directory新設、
  `RECORD_KINDS`追加・新永続schema・外部依存：なし。
- 実ホーム・既存利用者repository・既存保全data：accessなし。Testは`tmp_path`のみ。
- push・tag・PR・amend・rebase・reset・履歴書換え・`git add -A`／`git add .`：未実施
  （repository本体への操作。fixture内tmp repositoryの構築操作はscope §7-4の許可範囲）。
- **未実施（後続slice、scope v2 §12）**：Project Bindingの耐久保存・復元、
  Verification Run復元。**本sliceのGREENではWork 7A第2項checkboxを完了にしない**
  （Human裁定「分割案1」）。
