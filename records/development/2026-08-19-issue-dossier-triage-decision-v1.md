# issue実態調書（dossier）候補の登録・仕分け Human判断record v1

- 判断日：2026-08-19
- 判断者：利用者（Human）
- 記録者：Claude
- 対象候補：`IC-ISSUE-RECONCILIATION-DOSSIER-001`

## 1. 承認文言【記録】

> その内容で改善候補を登録して、すぐに対応

（2026-08-19 chat。裁定材料＝同日の突合工程分解表：機械化可能＝実態信号の収集・参照の生存・
拘束flag・治癒probe／機械化しない＝充足判断・受容・最終裁定）

## 2. 機械record【実測】

- 候補：`ic-issue-reconciliation-dossier-001--v1.json`（**候補writerで登録**・content_digest
  `2439f6cc…`・検証器合格）。
- 仕分け決定：`dec-ic-issue-reconciliation-dossier-001--v1.json`（**決定writerで書き出し**・
  disposition=`current_work`・content_digest `aa9edd29…`）。
- 台帳一括検証＝passed（候補21・決定53・issue 8＝registered 5／resolved 3）。
- 本件は往路・復路writerの**初の実運用**（使い捨てscriptなしで登録から仕分けまで完了）。

## 3. 次の一手

範囲固定文書（軽量作業票＋事前走査）→issue実態調書toolの実装（本日）。scope＝登録後の活動
（records・git言及の計数）・problem参照pathの生存・TODO active拘束flag。治癒確認probeは
将来拡張。判断はHumanのまま。

## 4. 未実施

作業単位の着手（本record直後）。TODO反映は完了時にまとめて。
