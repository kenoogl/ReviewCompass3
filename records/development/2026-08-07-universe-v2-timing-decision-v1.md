# universe record v2の作成時期 承認Decision v1

- decision ID：`DEC-UNIVERSE-RECORD-V2-TIMING-001`
- decision maker：Human
- decided at：2026-08-07
- 指示：本sessionのHuman文言「推奨案で対応。」（2026-08-07）

## 1. Humanの決定

`validate_current`停止の所見（`records/development/2026-08-07-work4b-d-ledger-first-operation-evidence-v1.md` §3）への処置として、推奨案を承認した。

1. いまは対処せず、**構成C（検索recordの外部化）を先に完了する**
2. C完了後、**universe record v2の作成を独立の小作業単位として実施する**。v2は既存の
   `write_source_universe`で機械生成し、開発方針の参照Digestを現行（Policy v5）へ更新する
3. v2作成後、既存Baseline v1（universe v1参照）に対する`validate_current`の挙動を機械確認してから
   コミットする。新たな停止が出た場合は所見として記録する
4. 恒久対策（参照Digestの恒久検査器）は`ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`の
   判断事項のままとし、本件はその3例目の実例として着手判断の材料に含める

## 2. この決定が承認していないこと

- 恒久検査器の実装（Issueの着手はHuman判断のまま）
- universe recordの意味的変更（include root等の範囲変更。v2は参照Digestの現行化のみ）
