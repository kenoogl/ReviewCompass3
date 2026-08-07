# 系統A（SHA-256計算）統合判断の材料 v1

- 作成：2026-08-08。根拠：`DEC-CONSOLIDATION-EVAL2-APPROVAL-001`（手順1〜3）。着手指示はHuman「着手」
- 対象：7fileの`_sha256`系関数（評価①same、B確定判定済み）

## 1. 照合（手順1）

- 統合除外・凍結レーン：**7関数とも該当なし**。ただし`issue_resolution_pilot.py`は凍結レーン
  対象symbol（`validate_implementation_task_contract_v2`等）と同居しており、**統合の差分が
  凍結symbolの行範囲に触れないこと**を実施時の機械検査条件とする
- 守り役：**4/7が守り役file**（issue_resolution_pilot、session_log_bootstrap、todo_compaction、
  eventual_preservation〔session_logs/配下〕）→ 実施時は反証レビュー`high`必須

## 2. 実測（手順2）

- 本体：7つとも**2行の逐語同一**（`return hashlib.sha256(引数).hexdigest()`。差は関数名
  `_sha256`／`_sha256_bytes`、引数名content/value/data、字下げ幅4/2のみ）
- 呼び出し：module内のみ計**31か所**（1・2・5・7・3・4・9件）。module外からの利用なし
- **テストからの直接参照：0件**（既存テストは無修正で通る。aliasはテストのためには不要）
- **テスト側の自前重複を発見**：`def _sha256`を自前定義するテストfileが**14件**存在する
  （tool側の7重複より多い）。承認済み経路（観測→改善候補→Humanトリアージ）でのissue化候補

## 3. 統合案と効果見積り（手順3）

**形（仮案。置き場と命名はHuman決定事項）**：

- 共通module `tools/common/digests.py` を新設：`def sha256_hex(data): ...`（2行＋docstring等で約10行）
- 7fileの各定義（2行）を `from tools.common.digests import sha256_hex as _sha256` の**1行に置換**
  （pilotは`as _sha256_bytes`）。**呼び出し31か所・既存テストは一切変更なし**（挙動不変）

**効果の実測見積り（正直に）**：

- 行数：−14（定義）＋7（import）＋約10（新module）＝**差し引きほぼ中立（+3行前後）**
- 「コード量が大幅に減る」効果は系統A単独では**生じない**。効果は定義の単一化・
  8個目の複製防止・見通しに限られる

## 4. 手順4（Human判断）への選択肢

- **ア：A単独で実施**——効果は中立。守り役4fileの反証レビューcostが相対的に重い
- **イ：C系統（canonical digest計算、4file・全て守り役・各5〜8行）と合流し、同じ共通module
  （digest系）として一括で設計・提示し直す**——新module新設costが償却され、削減が実質化する。
  1系統1単位の原則の変更にあたるためHuman承認事項
- **ウ：見送り**——効果基準（大幅減・見通し）に照らし統合しない。判定結果とこの材料は
  固定済みなので、いつでも再開できる

**所見**：効果基準を文字どおりに適用するなら、系統A単独（ア）は基準を満たさない。
イ（digest系として合流）が効果とcostの釣り合いで最も筋が良いと考えるが、決定はHumanによる。

## 5. あわせてトリアージを仰ぐ事項

- テスト側の`_sha256`自前定義14件（§2）。改善候補として挙げる：「テストの共通fixture化により
  重複を整理する」（着手はHuman判断、`registered / nonblocking`想定。blocker「テストの一斉整理は
  行わない」と整合させ、登録のみ）
