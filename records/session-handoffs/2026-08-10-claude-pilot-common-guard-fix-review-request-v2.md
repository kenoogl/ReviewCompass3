# レビュー依頼 v2：group A（共通正本）— F-CG-COMP-001修正後の再レビュー

- 作成日：2026-08-10
- Pilot：Claude／Reviewer：Codex／Closer：Codex
- collaboration mode：`role_neutral_pilot_review`、risk：`high`
- 先行依頼書：v1（完了Claimは完了レビューv1によりstale。変更せず保持）

## 1. 経緯

完了レビューv1（`records/session-handoffs/2026-08-10-codex-review-result-common-guard-fix-v1.md`、
SHA-256 `4be0042f9ef22475921749013a1ec21d1912b2b51db5d14db3dcb783a74e99f5`、
判定`reported_unverified`・blocking 1件 F-CG-COMP-001）に対し、Humanが
2026-08-10「テスト修正を承認する」と裁定した。実装は変更せず、test入力のみを修正した。

## 2. commit列（review request v1以後）

| SHA | 役割 | 内容 |
| --- | --- | --- |
| `e63649c` | Pilot | review request v1（先行） |
| `fb0e2ea` | Reviewer | 完了レビューv1 result record |
| `9461f34` | Pilot | 修正RED：`tests/test_common_digests.py`のみ（当該test 1件の入力Digestを修正前仕様の自己整合値へ） |
| `bf2163c` | Pilot | Evidence §7追記＋公式receipt v2 |

本依頼書のcommit SHAは自己参照のため記載せず、Reviewerがgitから特定する。

## 3. Claim（修正分）

- **F-CG-COMP-001**：`test_validate_record_rejects_non_json_compatible_record`の
  NaN recordへ、**修正前のcanonical仕様（`allow_nan`既定）で計算した自己整合Digest**を
  与えるよう変更した。Digest不一致という別理由での合格経路を断ち、JSON互換検査の
  有無だけが合否を決める形にした。
- **反証の機械確認**：修正後のtestを**修正前実装**（`a84b8ca`の3 file）へ当てると
  `1 failed`（`DID NOT RAISE`）、`HEAD`の実装で合格。欠陥がある状態で失敗し、
  修正済みで合格することを固定した。
- **範囲**：test 1 fileの当該test 1件のみ。実装3 file・pin・他のtestは不変
  （SHA-256はEvidence §6のまま）。testの追加・削除・緩和はしていない。
- **結果**：targeted 57 passed、公式全Test **1451 passed**・status `passed`、
  `git diff --check`指摘なし、worktree clean。

## 4. 成果物SHA-256（修正後）

| file | SHA-256 |
| --- | --- |
| `tests/test_common_digests.py` | `c5b23a77222693afece6f38848a6c111d5f7d9428fa806116952c15760972b2c` |
| Evidence（§7追記後） | `37d3618f4a2d252f6142c4111120a253ef5c1f54fd967272d0396d4517bf823a` |
| 公式receipt（v2） | `614866bfefdc830c521c46d99ab05421b1f26858a4775344be8186f3a22bb892` |
| `tools/common/digests.py`（不変） | `fc2d728c4c2cfd1b4e70b7eef6d0e6d4ce9a4a033712b93402bd2c7f984624f7` |
| `tools/common/paths.py`（不変） | `039512f579bf6e939d4086c1e75f848b0b4e5dba7f7170b63c21fd005b48e1ec` |
| `tools/task_contract/identity.py`（不変） | `fddffe6617c225e9fbedd33ea722316ea41f37c1f76c93cfbce3060ed55b5422` |

## 5. Reviewerへの確認観点

- F-CG-COMP-001の反証（修正前仕様で自己整合するNaN recordが`validate_record`を
  通過すること）が、修正後testで**確実に検出される**こと。修正前実装に対する
  独立再実行で失敗することを自ら確認する。
- 修正が当該test 1件の入力に閉じており、他のtestを弱めていないこと。
- 完了レビューv1で確認済みの事項（F-A1・F-A2反証の不成立、台帳Digestの不変、
  pin更新の範囲、`identity.content_digest`の直結）が維持されていること。
- 公式全Testの独立再実行とDigest再計算。
