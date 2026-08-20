# 転記のみ再実行入口の不在 観測record v1

- 記録日：2026-08-20
- 記録者：Claude
- 種別：観測record（改善候補`IC-REVIEWER-TRANSCRIBE-REPLAY-ENTRY-001`の出所）
- 提起：利用者（Human）。文言【記録】
  > 実装した契約016は全て機械化できているか
  > （棚卸し報告の後）機械化の穴2件を観測record＋改善候補としてwriterで登録してください（仕分けは後日）

## 1. 観測（根拠となる実測・記録）

1. **事象**【実測・2026-08-20】：契約016のterra実E2E（run `contract-016-e2e-codex-terra-2`）で、
   codexのレビューは完走し未加工出力はrepo外私有領域へ保存済み（raw先行保存）だったが、判定record
   転記段が`worktree_not_clean`（並行実行した正規全試験のreceipt生成による汚れ）で停止した。
2. **復旧経路の不在**【実測】：保存済みrawとlaunch記録から**転記・事後照合だけを再実行する機械
   入口が存在しない**。復旧はレビューの全再実行（run `-3`・外部送信と課金の重複）となった。
   経緯の正本＝`records/development/2026-08-20-contract-016-e2e-findings-remediation-evidence-v1.md` §4。
3. **設計上の非対称**【記録】：raw先行保存（文字列理解の原則6）は「解釈に失敗しても実物を持ち帰って
   再解析・裁定できる」ためにあるが、正式経路の転記はrawへ接続されておらず、原則の価値が復旧に
   使えていない。

## 2. 機械化候補の骨子

保存済みraw（`reviewer.raw.json`）とlaunch記録（`launch.json`）を入力に、転記・schema検証・
事後照合4点だけを再実行する単体入口（外部送信なし・既存判定recordがある場合は衝突停止）。

## 3. route

改善候補`IC-REVIEWER-TRANSCRIBE-REPLAY-ENTRY-001`としてHuman仕分けへ（仕分けは後日＝利用者指示）。
