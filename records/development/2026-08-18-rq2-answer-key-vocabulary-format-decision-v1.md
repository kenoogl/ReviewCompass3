# RQ2採点語彙（7語彙）の正式反映 形式判断record v1

- 判断日：2026-08-18
- 判断の根拠：利用者文言「案Bで確定。判断recordを書いてcommitまで進めてください」（2026-08-18 chat）
- 記録者：Claude
- 判断対象：裁定record v2 §7の残件「正解表の採点基準（§4の7語彙）の正式反映——正解表v3を
  起こすか、集計側の派生として持つかの判断」
- 関係record：
  - 裁定record v2 `records/development/2026-08-18-rq2-adjudication-and-byproducts-v2.md`
    （SHA-256 `f4191636ea1ee701b3fbc29f42a24e0860afd3c81633a5bb543215777134a152`）
  - 正解表v2 `records/development/2026-08-17-rq2-case-answer-key-v2.md`
    （封緘SHA-256 `0d290876110440df6ac5f14bd2efcc3d3d8f244b66f5d19354c4e7bb98f8cb64`）
  - 事前登録record `records/development/2026-08-17-rq2-preregistration-v1.md`
    （SHA-256 `1d276fe4a270ecff96c455bb5b39ef15ae75282bbbb635bd1425d7af1f353de3`）

## 1. 裁定【確定】

**案B＝集計側の派生として持つ。正解表v3は今は起こさない。**

7語彙（detected／material_defect／false_positive／request_gap／off_subject／out_of_scope／
non_counting）とケース再分類の正本は、既に固定済みの次の4点とする。

| 対象 | 正本 | 機械照合 |
| --- | --- | --- |
| 7語彙の定義（人向け） | 裁定record v2 §4の定義表 | 同recordのSHA-256（上記・TODO Evidence欄でも固定済み） |
| 7語彙の機械形 | `tools/evaluation/rq2_paired_trial.py`の`JUDGMENTS`定数（SHA-256 `890996191d60ec6ea49742345ac60599071aa88ea3cbc5070e051d2f6d4dbd25`） | `tests/test_rq2_paired_trial.py` 14件（SHA-256 `f00ef74c3014197e1affe49e69d2236f2accb7a2991b31d41664adc07da37ca2`） |
| 全44指摘への適用値 | `records/development/2026-08-17-rq2-scoring-judgments-v1.json` | SHA-256 `082af4aa9cc29e92c60d53c0ad0b5922d8a40f3bee0c0da8057887b1841b0b18` |
| case-008・case-010の欠陥ケースへの再分類 | 裁定record v2 §1（裁定#1・#3） | 同recordのSHA-256 |

## 2. 理由

1. 正解表v2ヘッダ規則「実起動後の正解の事後変更は行わない（変更が必要になったら理由をrecordして
   別版を立てる）」の趣旨は**黙って書き換えないこと**であり、理由と第一次→確定の全差分を公開した
   裁定record v2（§1〜§2.3）が既に満たしている。
2. 現時点でケース集の再利用予定は無く、転記だけの新版は**照合コストと誤転記の危険を増やすだけ**で
   得るものが無い（7語彙は既に上記4箇所で固定済み。新版は5箇所目の重複を作る）。
3. 事前登録版（v2）と裁定（record v2）の2層構造は、「第一次採点と確定採点の差を公開できる」という
   論文の主張（裁定record v2 §6-2）と整合する。事後に書いた正解表は、事前登録版との区別を厳密に
   表示しない限り「後出しの正解」と誤読される危険がある。

## 3. 機械的事実【実測・2026-08-18】

- 正解表v2の現物SHA-256は事前登録record §2の封緘値と**一致**した。`shasum -a 256`出力の転記：

  ```text
  0d290876110440df6ac5f14bd2efcc3d3d8f244b66f5d19354c4e7bb98f8cb64  records/development/2026-08-17-rq2-case-answer-key-v2.md
  ```

- 事前登録の取り決め（同record §2）により、封緘後のv2改変は実験無効を意味する。よって
  **v2の現物へ7語彙を書き足す選択肢は最初から存在しない**（本判断は「新版か派生か」の二択である）。

## 4. 正解表v3を起こす合図【判断】

ケース集（`docs/evaluation/rq2-cases/`）を新たな実験・比較（例：codex-cli第3 backend回復後の
比較、他モデル比較）へ**再利用する決定が出た時**、その作業単位の中で正解表v3を起こす。v3は
「事後裁定を反映した再利用版」であることを冒頭で明示し、事前登録版v2と区別する。反映内容は
本record §1の表から機械でたどれる。

## 5. 本判断に含まれない（持ち越しのまま）

- `read_only_entry`独自語彙の統合（TODOどおり別作業単位）。
- 裁定record v2 §1.1の一覧外適用4件の確認（利用者の取り消し余地は残置のまま）。

## 6. 未実施

- push（従前どおり利用者の運用に従う）。
- §4の合図が出た時のv3起草。
- 全体見取り図の更新は**不要**（状態欄に該当行が無く、既存行の状態語彙も変わらないため）。
