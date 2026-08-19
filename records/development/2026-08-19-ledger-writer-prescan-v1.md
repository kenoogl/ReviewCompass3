# 候補writer・台帳一括検証入口 事前走査 v1

- 記録日：2026-08-19
- 指示者：利用者（Human）。文言「current_workで採用。候補writerと一括検証入口だけ先に作って」
  （2026-08-19 chat。仕分けrecord＝`records/development/2026-08-19-ledger-writer-mechanization-triage-decision-v1.md`）
- 記録者：Claude
- 上位：`IC-LEDGER-LANE-WRITER-MECHANIZATION-001`（current_work採用・scope限定＝先行2部品のみ）
- 基準commit：`b79797b`（本走査の生成物2件を除きclean）
- 実測：測定ブロック`records/development/2026-08-19-ledger-writer-prescan-measurements-v1.md`
  （guard付き・全3entry二重実行一致）

## 1. 実測から確定した事実

1. **台帳の現況**：候補置き場のJSONは21 file（歴史allowlist 1 fileを含む）・V4仕分け決定52件・
   allowlist掲載1件。
2. **新設名の衝突なし**：`improvement_candidate_writer.py`・`workflow_ledger_verify.py`と
   対応試験2 fileはいずれも不存在。既存の語ヒット1件は無関係（pilot協調試験の
   「workflow台帳へ書かない」検査の名前）。
3. **流用部品はすべて実在・digest固定済み**：検証器（`pilot.validate_candidate`／
   `validate_record_file`／`load_config`）・決定台帳の全件検証（`intake.
   validate_triage_decision_repository`）・正準digest（`digests.canonical_content_digest`／
   `file_sha256`）・writer前例（`reuse_search_plan`＝草稿→finalize→合格時のみ書き換えの型）。
4. **保護試験N7の勘定3分岐**（validator合格／allowlist／V4決定の指紋束縛）が仕様の正本。
   一括検証入口は同じ勘定を**運用コマンド**として提供する（N7試験自体は変更しない）。

## 2. 設計（作業票へ渡す論点）

1. **候補writer**`tools/development/improvement_candidate_writer.py`：`--draft <path>`。
   草稿は意味欄のみ（`source_identity.sha256`・`evidence_refs[].sha256`・`created_at`・
   `content_digest`の省略を許す）。writerがSHA-256機械計算・時刻機械記録・digest正準埋め込み・
   置き場解決（id小文字＋`--v{version}.json`）を行い、**v3検証器の合格時のみ**書き出す
   （new-only・既存fileは拒否）。出力は一行JSON・exit 0／1。
2. **一括検証入口**`tools/development/workflow_ledger_verify.py`：引数省略時＝実repo。
   候補置き場の全JSONをN7同型の3分岐で勘定（不充足＝finding）し、V4決定台帳の全件検証を実行。
   出力は`{findings, status, counts}`の一行JSON・exit 0=passed／1=failed（`todo_handoff`型）。
   `--project-root`任意（試験fixture用）。
3. **試験（RED先行）**：writer 4本（正常草稿の合格書き出し・無効語彙は書き出さない・
   上書き拒否・`-m`疎通）／verify 4〜5本（fixture緑・破損候補の失敗と列挙・allowlist分岐・
   実repo緑・`-m`疎通）。
4. **範囲外**（決定record §3どおり）：仕分け決定・issue登録のwriter入口、verdict writerと
   状態遷移、record schemaの変更、N7試験・検証器の変更。残scopeは突合checkpoint枠で再仕分け。

## 3. 手順5：正式再利用検索

草稿→writer finalize→先行commit→`--plan`のみ。証明書は
`records/development/2026-08-19-ledger-writer-attestation-v1.json`。

## 4. 未実施

手順5、作業票の適用、RED、GREEN、Evidence、TODO反映。
