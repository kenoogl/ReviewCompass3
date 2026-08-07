# 出口設計 段階1 GREEN Evidence v1

- 実施：2026-08-07
- 根拠：v4（SHA-256 `3a82b3973f8abc947782c4bbf8e2d54713043e8e8591a543089a5824c57bcacd`）と
  `DEC-EGRESS-GATE-V3-JUDGMENTS-001`。着手指示はHuman「次へ」（2026-08-07、v4提示後）
- 進め方：TDD（テスト先行→RED確認→コミット→実装→GREEN→コミット）を2巡

## 1. 実装した物（すべて新規。codeのコピーなし、送信機能なし）

| module | 内容 | v4対応 |
| --- | --- | --- |
| `tools/egress/prefilter.py` | ローカル事前分類（字句token・Jaccard・特徴一致・3帯分類。閾値はHuman承認済み初期値0.85／0.45、重み0.6/0.2/0.2） | §3.1 |
| `tools/egress/payload.py` | 3種構成payload（行範囲からの機械切り出し・特徴量allowlist 8field・定型文template 1件）、正準JSONとdigest、由来照合 | §3、§5条件1・2 |
| `tools/egress/approval.py` | 承認recordの7項目機械検証、送信物一覧digest（順序に依らず決定的）、秘密値・個人識別子の走査、消費の排他claimと恒久consumed | §4 |
| `tools/egress/gate.py` | 関門の単一実装（条件1〜6・8）。fail-closed、理由と復旧手順を全数返す、自動修正なし | §5 |
| `tools/egress/sender.py` | 段階1送信係。関門合格でも必ず`EgressSendingNotApproved`で停止（送信は型として不可能） | §8 |

## 2. 関門9条件の実装位置

- 条件1（構成）・2（由来）・3（一覧照合）・4（伏字化適用＝変化したら停止信号）・
  5（承認record結線）・6（単一実装・規模上限・digest一致）・8（復旧経路の全数印字）：
  `gate.py`で検査、テストで固定
- 条件7（trusted経路・content-addressed目録）・9（応答不全エスカレート）：**送信を持つ段階4の
  対象**として本段階では未実装（v4の段階分けどおり。送信自体が`sender.py`で型として不可能）

## 3. テスト

- 新規4file・56件：`test_egress_prefilter.py`（13）、`test_egress_payload.py`（13）、
  `test_egress_approval.py`（17）、`test_egress_gate.py`（10、送信不能の確認2件を含む）
- RED確認：26 failed（`160f63d`）、30 failed（`68d8f17`）をそれぞれコミットで固定
- GREEN：新規56 passed。全suite **1196 passed**（baseline 1140＋56）、`git diff --check`合格
- 実装コミット：`d779e9e`（prefilter・payload）、`a9d59ee`（approval・gate・sender）

## 4. 残作業（本Evidenceの範囲外）

- 反証レビュー（守り役code、`work-review-protocol` §3既定`high`。v4 §10の6観点）
- 段階2：dry-run（曖昧59組のpayload一式組み立てとHuman目視）
- 段階3：承認record形式の正式schema化
- 伏字化hookの結線（規則登録は実施順序2番目のため、gateは未結線を拒否する状態が現在の正）
