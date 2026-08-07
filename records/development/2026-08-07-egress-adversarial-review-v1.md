# 出口関門 反証レビュー結果 v1

- 実施：2026-08-07。着手指示はHuman「次へ」
- 対象：`tools/egress/`（段階1実装。GREEN Evidence SHA-256
  `ba75438bb22815783b6f5a52cae9f842b1672a5816fa8d52feb678664fb5f081`）
- 方法：v4 §10の6観点で反証を新作し（`tests/test_egress_adversarial.py`）、実行して確かめた。
  的中はRED commitで固定してから処置した（`work-review-protocol` §4.4、risk `high`）

## 1. 発見と処置

| ID | 観点 | 結果 | 内容 |
| --- | --- | --- | --- |
| I-1 | 一覧外payload／構成規則の迂回 | **的中→処置済み** | gateがpayloadの`digest`と`content`の一致を再計算しておらず、**承認済みdigestを名乗る改ざん内容が通過した**（反証1）。処置：gateでSHA-256を再計算し不一致を拒否。承認済みdigest＝承認済み内容そのもの、という結線が成立した |
| I-2 | allowlist外の自由文 | 防御済み＋深化 | digestを揃えた自由文の混入（反証2）は一覧照合で拒否された。処置I-1に加え、gateで特徴量keyのallowlist再検査を追加（多層化） |
| I-3 | 定型文の差し替え | 防御済み＋深化 | 問い文の差し替え（反証3）も一覧照合で拒否。gateで`question_text`とtemplateの一致検査を追加（多層化） |
| I-4 | runner迂回の直接送信 | 防御済み | `tools/egress/`全fileに通信手段（socket・http・urllib・requests・httpx・subprocess）が存在しないことを機械検査で固定（反証4） |
| I-5 | 排他claimの回避 | 防御済み | claim保持中の例外でも解放され恒久lockにならない（反証5） |
| I-6 | 承認recordの真正性 | **境界として記録** | gateはrecordの内部整合を検証するが、「Humanが本当に書いたか」は検証しない。真正性の担保（置き場所の固定・書込み手順）は段階3（承認recordの正式schema化）の設計事項として持ち越す |

## 2. 検証

- 反証テスト5件：的中1（I-1、RED commit `37c0f8c`で固定）→処置commit `a7fc60e`で全通過
- 全suite **1201 passed**（1196＋反証5）。既存テストの変更なし
- 目録偽造の観点（v4 §10）は、content-addressed目録が段階4の実装対象のため本レビューでは
  digest結線（I-1）として検査した。目録そのものの反証は段階4実装後に行う

## 3. 境界

- 本recordは段階1実装への反証レビューの固定であり、段階2以降の可否を決めない
- I-6の持ち越しは段階3の設計に含めることをTODOの後続作業で追跡する
