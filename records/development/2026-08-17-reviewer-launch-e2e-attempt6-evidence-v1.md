# 契約010 実E2E第6試行（e2e-010-006）Evidence v1

- 記録日：2026-08-17
- 記録者：Claude
- 実施根拠：利用者の明示指示「e2e-010-006で再実施して」（chat）
- 結果：**停止（`verdict_schema_nonconforming`・終了コード2）。§9-8は未成立のまま**

## 1. 実施と停止【実測】

- 起動：同一対象・同一期待SHA-256、run-id `e2e-010-006`、第5試行の訂正済み引数（`--sandbox`追加）。
- 事象は第5試行と同一：`permission_mode: request-review`のまま、Reviewerが正しい絶対pathへ
  `view_file`→`User denied permission for read_file(…)`→会話終了→`result.response`空→構造不適合停止。
- 消費：入力21,025 token・出力722 token。raw・起動recordは`e2e-010-006/`へ不変保存。

## 2. 確定した事実【実測】

1. **`--sandbox`は許可方式に影響しない**（`--mode=plan`と同様）。
2. これにより、契約§7.1の範囲内のCLI旗（`--mode=plan`・`--sandbox`）では、headlessでのfile内容
   読取り許可を得られないことが確定した。禁止旗`--dangerously-skip-permissions`は契約上使用しない。
3. 6試行の停止はすべて安全型（外部agentへの権限付与なし・raw/起動record完全保存・自動再試行なし・
   判定record生成なし）。

## 3. 残る経路の評価

1. **利用者の対話sessionでの事前許可（推奨・未実測)**：agyを対話modeで開いて読取り道具へ
   「常に許可」相当を与え、規則が保存されてheadlessへ効くかを確認する。暫定手動体制でGeminiが
   権限許可後に読取り・書込みを実証した実績（統合検討§3）と整合する仮説である。
2. `--add-dir`によるworkspace明示（未実測・効果は疑わしい）：許可はdirectoryでなく道具単位に
   見えるため、期待薄。
3. 契約§10の停止条件該当としての契約改定（第1 backendの変更等）：経路1が不成立の場合の後段。

## 4. 残り

- §9-8実E2Eは未成立。次は経路1（利用者の対話事前許可の実験）の結果を待ち、成立すれば
  `e2e-010-007`で再実施する。
