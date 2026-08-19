# 候補writer・台帳一括検証入口 実行Evidence v1

- 記録日：2026-08-19。指示者：利用者（Human）「current_workで採用。候補writerと一括検証入口だけ
  先に作って」（chat。仕分けrecord＝`records/development/2026-08-19-ledger-writer-mechanization-triage-decision-v1.md`）
- 範囲固定：作業票`docs/development/2026-08-19-ledger-writer-work-ticket-v1.md`／事前走査同
  prescan v1。基準`b79797b`→文書・計画（writer）`563b21c`→証明書`7610cee`→実装は本record同一commit
- 対象候補：`IC-LEDGER-LANE-WRITER-MECHANIZATION-001`（current_work・先行2部品）

## 1. 成果物

1. **候補writer**`tools/development/improvement_candidate_writer.py`【新設】：草稿（意味欄のみ）
   から出所SHA-256・時刻・正準content_digest・置き場（id小文字＋版）を機械埋め込みし、
   **v3検証器の合格時のみ**台帳へ書き出す（new-only・上書き拒否・不合格は書き出さない）。
   一行JSON・exit 0／1。
2. **一括検証入口**`tools/development/workflow_ledger_verify.py`【新設】：候補置き場の全JSONを
   保護試験N7と同型の3分岐（validator合格／歴史allowlist／V4決定の指紋束縛）で勘定し、V4仕分け
   決定台帳の全件検証を一操作で実行。`{findings, status, counts}`一行JSON・exit 0＝passed／
   1＝failed（`todo_handoff`型）。
3. 試験9本【新設】：writer 4本（合格書き出し・無効語彙の拒否＝書き出さない・上書き拒否・`-m`疎通）
   ／verify 5本（fixture緑・破損候補の失敗列挙・allowlist分岐・実repo緑・`-m`疎通）。

## 2. RED→GREEN

RED＝新設9本のみ失敗（module未存在・terminal転記`9 failed`）。GREEN・受入＝**受入測定ブロック
`records/development/2026-08-19-ledger-writer-evidence-measurements-v1.md`参照**（新設9本exit 0・
台帳関連試験群68本exit 0・実repoでの一括検証`-m`単独exit 0＝候補20件の勘定が
validator 13＋allowlist 1＋決定束縛6・決定台帳52件全件合格・findings空・新設4 fileのdigest固定・
全entry二重実行一致）。`git diff --check`合格。

## 3. 効果（候補の問題への対応）

- 候補登録の「雛形の記憶頼み」が消える：欄集合・語彙・値規則の適合は検証器が、digest・時刻・
  置き場は機械が決める。本日実測した形式不合格2回（分類語彙・section欄・version規則）の型は
  writerでは構造的に発生しない（草稿段階で検証器不合格＝書き出されない）。
- 台帳の健全性が1コマンドで確認できる：2026-08-18型の「検証器を通さない登録が3日間気づかれない」
  事象は、`workflow_ledger_verify`を作業単位の受入や定期確認に組み込めば即日検出できる。
- 残scope（決定・issue登録のwriter入口・verdict writer・状態遷移）は仕分けrecord §3どおり
  突合checkpoint枠で再仕分け。

## 4. 未実施

TODO反映とcommit。push（利用者の運用に従う）。残scopeの再仕分け（突合checkpoint枠）。
手順書（AGENTS §4の登録手順）へのwriter反映は次回の台帳作業時に確認する。
