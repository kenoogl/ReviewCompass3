# Claude実装委譲経路 RED開始 Human裁定 v1

- 日付：2026-08-12
- 裁定者：Human
- 裁定文言：`次へ`
- 裁定文言の出典：直前に提示した単一の次作業候補への応答
- 対象範囲：`2026-08-12-claude-implementation-route-scope-v2.md`
- 対象範囲SHA-256：`9881f7df526c3aef8c21e665f75927329608d1b0518e343db0ac5c89f954a024`
- 要求集合SHA-256：`ca2b28f5dc156fc45c1c20808fe16b1e89874bead52da34dc07688015a2a2d69`
- 危険度：`high`
- 裁定：`approve_red_test_start`

## 承認範囲

- 範囲固定v2の危険度、要求、変更範囲を受け入れる。
- 未実装なら失敗する受入試験の作成開始を認める。
- 承認された変更範囲の内側で、RED実作業の変更可能pathを
  `tests/test_claude_implementation_route.py`だけに狭める。
- RED指示、監査、判定、証拠の記録は`records/session-handoffs/`へ置く。

製品実装、既存試験の変更、管理者配置変更、Claude起動、認証変更、外部送信、段完了は認めない。
上流との矛盾または安全境界を満たせない事実が判明した場合は、試験作成前に停止してHuman判断を得る。
