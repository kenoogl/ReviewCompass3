# レビュー依頼 v2：Work 7A第2項 前駆slice — 独立レビューv1 Findings修正後の再レビュー

- 作成日：2026-08-09
- Pilot：Claude／Reviewer：Codex／Closer：Codex
- collaboration mode：`role_neutral_pilot_review`、risk：`high`
- 先行依頼書：`review-request-v1`（SHA-256
  `d759e59c5388b80ed6d009e6c84ca585dce63e79023be540b4e34848a87a1932`。完了Claimは
  独立レビューv1によりstale。変更せず保持）

## 1. 経緯と対象

独立レビューv1（`records/session-handoffs/2026-08-09-codex-review-result-work7a-checkout-relocation-v1.md`、
SHA-256 `ba5703edda25b73fb6251b73839367d2c9d7b12c5fd28a7109e9df06d7c8c0c6`、判定
`report_execution_mismatch`）の3 Finding（RR-P1-001／002、RR-P2-003）について、Humanが
修正を承認（2026-08-09「3件の独立反証を固定してください…」）。scope・schema境界は
scope v2（SHA-256 `f127351d05bc621af95a042506dc726790ca59ecc928cec4c34257ee23d473a8`）の
まま変更していない。

## 2. 修正commit列（review request v1 commit以後）

| SHA | 役割 | 内容 |
| --- | --- | --- |
| `6167fb64fba9661bfd6200342a21b19e0fee8d28` | Pilot | review request v1（先行） |
| （Reviewer記録） | Reviewer | 独立レビューv1 result record |
| `2b27b4d4a00a7ee6989d29fc6a35e92ef01d8b56` | Pilot | 修正RED：3反証のTestのみ追加（116行） |
| `af8e005f8844520042eec16252d48ef64ccee368` | Pilot | 修正GREEN：実装修正・GREEN Evidence更新・receipt更新のみ |

本依頼書のcommit SHAは自己参照になるため記載せず、Reviewerがgitから特定する。

## 3. Claim（修正分）

- **実施**：修正REDを単独実行し、新規3件のみが反証どおり（空Change Set・DID NOT RAISE・
  clean偽装）失敗し先行19件が合格、exit `1`を確認してcommit。既存Testは弱めず、実装のみ
  修正してGREEN化。
- **修正内容**：
  - RR-P1-001：Change Setをcommit間delta＋両Snapshotのindex・worktree・対象untracked
    状態差の合成（`_combined_change_items`）で導出・照合。`tracked_changes`の各entryへ
    `content_identity`を追加（in-memory値schema内の表現追加。承認済みtop-level identity
    fieldsは不変。新永続schema・`RECORD_KINDS`追加なし）。
  - RR-P1-002：捕捉時に実HEADを機械取得し、caller指定`head_commit`との一致を必須化。
    不一致は新安定stop code `head_commit_mismatch`。
  - RR-P2-003：`GIT_CONFIG*`環境変数を全て除去（COUNT／KEY_*／VALUE_*含む）してから
    file configをdevnullへ固定し、`GIT_DIR`等のrepository位置差替え変数も除去。
- **結果**：targeted 22 passed（exit `0`）、関連回帰83 passed（exit `0`）、公式全Test
  1337 passed・status `passed`（exit `0`、receipt再読込みでfailed 0確認）、
  `git diff --check`指摘なし。
- **未実施**：scope変更、新schema、耐久Binding、Verification Run、TODO／checklist更新、
  Work 7A第2項checkbox完了（いずれもHuman指示どおり未実施）。

## 4. 成果物のpathとSHA-256（修正後）

| file | SHA-256 |
| --- | --- |
| `tests/test_work7a_checkout_relocation.py`（22 Test。修正RED以後未変更） | `2a5c32ae22104217219e26a5c82b0de26b56de9dd3226a06e07765de0e273eda` |
| `tools/deployment/checkout_relocation.py` | `5c353c6f2815dbe434d5fab5374ac3af2d6996eddc417b9fa30930402778f589` |
| `records/development/2026-08-09-work7a-checkout-relocation-green-evidence-v1.md`（修正節§7追記） | `176f089dc9da544eab4116231f32856afe825472d00761e4d9589103b28b0932` |
| `records/development/2026-08-09-work7a-checkout-relocation-green-test-receipt-v1.json`（更新） | `e653387a9f35eb04fe7951c670b9c21a6bdefbe699f70871e0a0d2e94e27684e` |

## 5. 禁止操作の未実施・worktree・停止地点

- 固定入力実装・TODO・checklist・Plan・Decision・scope v1／v2・先行レビューrecord：未変更。
- production APIはread-only Gitのみ。fixture Git操作はTest内・`tmp_path`限定。
- 実ホーム・既存利用者repository・既存保全data：accessなし。
- push・tag・PR・amend・rebase・reset・履歴書換え・`git add -A`／`git add .`：未実施。
- 本依頼書のignore検査：`git check-ignore --no-index` exit `1`（続行可）。
- worktree：本依頼書commit時点でclean。
- 停止地点：本依頼書のcommitをもってPilotは停止し、Codexの再レビュー（元19 Test・
  独立反証3件・関連・公式全Testの再実行）まで次の作業へ進まない。

## 6. Reviewerへの確認観点（依頼）

- 3 Findingの修正が独立反証3件（SHA-256
  `ab45c847930ab85b9381463f52ad83b6108288a3977452ffa768e44870a66507`）で不成立になること
- 修正REDの失敗理由が反証そのものであること、既存Testを弱めていないこと
- `content_identity`追加がscope v2 §9のschema境界（in-memory値・top-level fields不変）に
  収まっているか
- targeted・関連回帰・公式全Testの独立再実行と、Digest再計算
