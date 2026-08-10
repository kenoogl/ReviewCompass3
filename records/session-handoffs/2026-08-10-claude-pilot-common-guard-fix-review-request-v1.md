# レビュー依頼：group A（共通正本）blocking 2件の修正

- 作成日：2026-08-10
- Pilot：Claude／Reviewer：Codex／Closer：Codex
- collaboration mode：`role_neutral_pilot_review`、risk：`high`

## 1. Human承認

- 2026-08-10「組A修正 risk highを確定、着手を承認する」
- 2026-08-10「組A RED開始を承認する」
- 修正順序の裁定：`records/development/2026-08-10-guard-backfill-fix-order-decision-v1.md`（`4bb1c9b`）

## 2. commit列

| SHA | 役割 | 内容 |
| --- | --- | --- |
| `3594172` | Pilot | SCOPE v1 |
| `867d0b1` | Reviewer | 範囲レビューv1（要修正・blocking 1件） |
| `35d2fe6` | Pilot | SCOPE v2（pin fileの扱いを追加） |
| `9fd43ba` | Reviewer | 範囲レビューv2（`verified`・blocking 0） |
| `a84b8ca` | Pilot | RED：test 2 fileのみ。15 failed / 110 passed、exit `1` |
| `b20d76b` | Pilot | GREEN：実装3 file＋pin値2箇所＋Evidence＋receipt |

本依頼書のcommit SHAは自己参照のため記載せず、Reviewerがgitから特定する。

## 3. Claim

- **F-A1**：Digest計算の前にJSON互換性をfail-closedで検査する
  （`require_json_compatible`・`canonical_json_bytes`を`tools/common/digests.py`へ新設、
  `allow_nan=False`）。非文字列key・tuple・set・bytes・非有限数は
  `DigestInputError`で拒否。`identity`側は`canonical_bytes`と`_content_digest_or_stop`で
  `ContractError("schema_violation")`へ変換し、`seal`・`validate_record`が使う。
  `identity.content_digest`は**共通正本への直結を維持**（写しの禁止）。
- **F-A2**：`within`に実体同一性（`os.path.samestat`によるdevice・inode照合）の
  経路を追加。case差・NFC/NFD差だけが違う実在pathで`os.path.samefile`と同じ判定に
  なる。root外の拒否と、存在しないpathの解決後path判定は不変。
- **正例の維持**：**実台帳`records/development/*.json`の宣言Digestと再計算値が一致し
  続けること**をTestで固定（Digest値の変化なし＝台帳の再計算不要）。
  JSON互換検査で拒否される実台帳recordは無かった。
- **結果**：targeted 57 passed、公式全Test **1451 passed**・status `passed`、
  `git diff --check`指摘なし、worktree clean。
- **未実施**：group B・C・Dの17件、TODO・checklist反映（Closer）、
  上流設計・config・schema・既存recordの変更。

## 4. 成果物SHA-256

| file | SHA-256 |
| --- | --- |
| `tools/common/digests.py` | `fc2d728c4c2cfd1b4e70b7eef6d0e6d4ce9a4a033712b93402bd2c7f984624f7` |
| `tools/common/paths.py` | `039512f579bf6e939d4086c1e75f848b0b4e5dba7f7170b63c21fd005b48e1ec` |
| `tools/task_contract/identity.py` | `fddffe6617c225e9fbedd33ea722316ea41f37c1f76c93cfbce3060ed55b5422` |
| `tests/test_common_digests.py` | `3f52229b177324cd463dc80e6cf031ac685598dab0d92bc9a4801e2cdf15364c` |
| `tests/test_common_errors_paths_output.py` | `61f21966c3488f73a66baa40d75c31720c1ecd2da08cab80832070025033028a` |
| `tests/test_common_module_pins.py` | `fc7dcde0b182b1ee0a8a57759f0c8bf240c5956e9258e63ae77e2c2d0cdd392e` |
| Evidence | `653106b0e9eabc48cfb716b0efa55eb08d6de18e0f8da7c586192b6a07a131a4` |
| 公式receipt | `429ca5d4ae990893837df90509837fc5f2e6f73ff83438e6fb87bda38cdb3fd5` |

## 5. Reviewerへの確認観点

- group A判定record（`17613d2`）の反証（D1のkey型・sequence型・非有限数、
  P1のcase差・NFC/NFD差）が**すべて不成立**になること。
- **正例側**：既存台帳recordのDigest値が修正前と変わっていないこと
  （独立に数件を再計算して照合）。`within`がroot外を通さないこと。
- pin更新が**値2箇所のみ**で、key構成・検査logicが不変であること
  （scope v2 §2で許した唯一の例外の範囲内か）。
- `identity.content_digest`が共通正本へ直結したままであること
  （`tests/test_shared_function_sweep.py`の要求）。
- 各commitが範囲固定§6（v2差し替え後）の変更file境界を守っていること。
- targeted・公式全Testの独立再実行とDigest再計算。
