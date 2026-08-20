# 機械化の穴2候補の仕分け Human判断record v1

- 判断日：2026-08-20
- 判断者：利用者（Human）
- 記録者：Claude
- 判断の種別：改善候補の仕分け（採用・route・時機条件の確定。AIの分類とrouteは提案であり、
  本recordの裁定が正）

## 1. 承認文言【記録】

> 両候補ともcheckpoint採用・同枠・合図は縦C着手前で承認する。仕分けrecordを作成して

（2026-08-20 chat。Claudeが提示した推奨文言と同一。判断材料＝同日の1画面比較：実害の有無・
再発頻度・対処の性質・規模）

## 2. 仕分け

| 候補 | 正本（観測record） | 仕分け | 実施時機・条件 |
| --- | --- | --- | --- |
| `IC-REVIEWER-TRANSCRIBE-REPLAY-ENTRY-001`（転記のみ再実行入口） | `records/development/2026-08-20-reviewer-transcribe-replay-gap-observation-v1.md` | **checkpoint採用** | **縦C合議の着手前**に、下記候補と**同枠**（縦Bの小改定契約1本に束ねる）で実施 |
| `IC-LAUNCH-DIGEST-TABLE-RECHECK-001`（起動直前のdigest表現物照合） | `records/development/2026-08-20-launch-digest-recheck-gap-observation-v1.md` | **checkpoint採用** | 上記候補と**同枠**。案a（launch内蔵）／案b（check再実行の必須化）の選択は契約候補の実装3案比較で確定する |

## 3. 帰結

- 新しい作業単位は本仕分けでは開始しない。両候補は「合図が来たら同枠で動く」状態に置かれた。
- 合図＝**縦C合議の着手前**：縦Cはレビュー起動の回数を増やすため、起動経路の穴（復旧不能な転記
  停止・表の陳腐化見逃し）を先に塞ぐ順序を利用者が承認した。次に縦C着手の指示が出た時点で、
  まず本2候補の同枠縦切り（事前走査→小改定契約）から入る。
- それまでの運用注意（機構が入るまでの暫定）：起動中はworktreeを汚す操作をしない・起動直前に
  checkを再実行する（正本＝是正Evidence
  `records/development/2026-08-20-contract-016-e2e-findings-remediation-evidence-v1.md` §4）。
- 台帳上の候補file（`.reviewcompass/workflow/improvement-candidates/`の2件）は変更しない。仕分けの
  正本は本recordである。採用候補はconsumerとOutcomeへ接続されるまでclosedにしない。

## 4. 未実施

- 両候補の実施そのもの（合図＝縦C着手前の同枠縦切り）。TODOのdeferred欄への合図の反映
  （本record直後に共通手順で実施）。
