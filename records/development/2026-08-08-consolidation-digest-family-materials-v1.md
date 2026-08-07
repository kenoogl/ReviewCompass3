# digest系（系統A+C合流）統合判断の材料 v1

- 作成：2026-08-08。根拠：系統A手順4のHuman判断「イ」（A+C合流で再提示）と着手指示「候補1」
- 対象：A＝SHA-256計算7関数、C＝canonical digest計算4関数（計11関数、9file）

## 1. 照合（手順1）【実測】

- 統合除外・凍結：**11関数とも非該当**。凍結対象の全list（pilot内3symbol・configファイル1・
  unified_migration.py）と照合済み。凍結symbolと同居するfileはA系のissue_resolution_pilot.pyの
  1件のみ（実施時はdiffが凍結行範囲に触れない機械検査を条件とする）
- 守り役：A 4/7、**C 4/4**、合流で**8/11file**。実施時は反証レビュー`high`必須

## 2. 実測（手順2）

| 系統 | 本体 | 呼び出し | テスト直接参照 |
| --- | --- | --- | --- |
| A（_sha256系） | 2行×7、逐語同一 | module内31か所 | **0件** |
| C（canonical系） | 7行×4、逐語同一（`content_digest`keyを除外しcanonical JSONのSHA-256を返す） | module内16か所（1・8・4・3） | **公開2名に直接参照あり**：`ix.content_digest`（3行）、`intake.canonical_digest`（複数行。公開wrapper経由） |

- テスト側の自前重複（追加観測）：`_sha256`系14fileに加え、**canonical digest系の自前定義が12file**。
  登録済み`ISSUE-TEST-SHA256-FIXTURE-DUPLICATION-001`と同型の関連観測として本recordで固定する
  （issueの拡張はHumanトリアージ判断）

## 3. 統合案と効果見積り（手順3）

**形（仮案。置き場と命名はHuman決定事項）**：共通module `tools/common/digests.py` に2関数：

- `sha256_hex(data)`（2行）
- `canonical_content_digest(document)`（7行）

各fileの定義をimport 1行に置換する。**公開名・private名とも各moduleの既存名をaliasで維持**
（例：`content_digest = canonical_content_digest`）。これにより呼び出し47か所・既存テストは
一切変更なし（テスト修正3分類の「無修正」路線）。

**効果の実測見積り**：

- 行数：A（−14＋7）＋C（−28＋4）＋新module（約＋14）＝**約−17行、digest定義11→2**
- 質的効果：canonical形式（key除外・separators・sort_keys）の仕様が**1か所に固定**される。
  現在は4部が独立に存在し、将来の仕様変更で食い違い得る——台帳の指紋計算という守り役の
  中核仕様であり、単一化は保証面の改善でもある
- A単独（前回材料：効果中立）に対し、合流で削減・単一化とも実質化した

**挙動不変の検証計画**：統合前後で代表入力（実在record群・bytes列）への出力が
**1bitも変わらない**ことを機械比較する（反証レビュー観点に含める）

## 4. 手順4（Human判断）への提示

- **実施する／しない／保留**、実施の場合は共通moduleの**置き場と命名**の決定
- 所見：削減約17行・定義11→2・仕様の単一化により、効果基準（コード量減・見通し）を満たすと
  考える。**実施を推す**。実施時の条件は §1の凍結不可侵検査と反証レビュー`high`、
  §3のalias維持・bit一致比較
