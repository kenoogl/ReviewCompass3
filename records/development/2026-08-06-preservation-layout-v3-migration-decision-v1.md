# セッションログ書庫のLayout v3移行 承認Decision v1

- Decision ID：`DEC-PRESERVATION-LAYOUT-V3-MIGRATION-001`
- decision maker：Human
- decided at：2026-08-06（Humanの移行指示による）
- decision：`approved`
- decision class：`migration_decision`

## 1. 経緯（記録から確認済みの時間関係）

1. 2026-08-04T00:51:19+09:00、最初のセッション保存で旧Storage Decision
   （`records/development/2026-08-04-session-transcript-eventual-preservation-storage-decision.json`）が
   OS標準data root（`option_1_os_standard_limited_pilot`）を承認した。
2. 2026-08-04T15:30:44+09:00、Layout v3
   （`records/development/2026-08-04-layout-baseline-v3-project-first-approval-decision.json`、
   `effective_layout_version: 3`）が承認された。同承認は「既存v2 dataを本承認では移行しない」と
   明記しており、既存書庫の移行は当時の承認対象外だった。
3. 2026-08-06T09:13:46+09:00、再記録Decision
   （`records/development/2026-08-06-session-transcript-repair-and-recapture-decision-v1.json`）は
   旧Storage Decisionを`prior_decision_path`として再利用し、
   `logical_path: reviewcompass3_user_data/eventual-preservation`（旧OS標準配置）を再承認した。
   結果、ログは旧配置へ追記された。
4. ログ内容とDigest検証は有効である（本Decision §3）。配置だけが現行Layout v3ではない。

## 2. 承認範囲

- 既存書庫（raw・verbatim・cursor・Provenance・ledgerの全体）を、**byte-exactに**現行Layout v3の
  development profileのsensitive root配下へ移行する。論理path：
  `<runtime_root>/projects/reviewcompass3/development/sensitive/eventual-preservation/`
  （`<runtime_root>`はLayout v3の`~/.reviewcompass3`。repository recordには絶対pathを書かない）。
- rawとverbatimが会話内容を含むため、**archive全体をsensitive root配下へ置く**。cursor・Provenance・
  ledgerも同じbundleとして保持し、今回の移行で別rootへ分解しない。
- 移行・検証後、**今後の保存先を新配置へ切り替える**。
- **旧配置は削除しない。** rollback copyとして保持し、削除は別のHuman判断とする。

## 3. 移行前の固定事実（2026-08-06実測）

- 旧書庫：file 5件、合計93,878,980 bytes。file permission全件0600、directory全28個が0700、
  lock・一時file残留0件、`redacted/`は不存在（receiptの`redacted_transcript_absent: true`と整合）。
- 5件すべてのSHA-256が、既存receipt
  （`records/development/2026-08-06-session-transcript-current-codex-recapture-receipt-v1.json`）と
  Evidenceの記載に**全件一致**（停止条件「Digest不一致」に非該当）。
- 移行先のv3 sensitive root（`.../development/sensitive/`）は**未作成**であり、
  異なる既存データは存在しない（停止条件「target衝突」に非該当）。
- 移行先は既存resolver`tools.layout.baseline.resolve_project_runtime_layout`
  （`runtime_root`・`project_id`・`profile`から各rootを導出、副作用なし）で導出可能
  （停止条件「resolver導出不能」に非該当）。
- 保存処理`tools/session_logs/eventual_preservation.py`は保存先を引数`private_root`で受け取り、
  `deployment_paths`へ依存しない。したがって`tools/session_logs/deployment_paths.py`の
  OS標準path定義は変更しない（他consumer 5 moduleに影響を与えない）。

## 4. 実施方法の枠

- 実装変更はTDDで行う。現行Layout v3のdevelopment/sensitive rootから書庫のprivate rootを
  導出するテストを先に作り、失敗を確認してから実装する。既存resolverを再利用し、
  別のresolverを重複実装しない。
- 移行はdry-run（衝突・容量・permission・rollback可能性）→一時領域へのbyte-exact copy→
  全件照合（file数・相対path・size・SHA-256・rawのUTF-8 JSONL妥当性・rawから再生成した
  verbatimとのbyte一致・cursor/Provenance/ledgerのidentity一致・directory 0700・file 0600・
  一時／lock残留0）→active切替→冪等再実行`unchanged`確認、の順とする。
- targetに異なる内容が存在する場合は上書きせず停止する。
- Migration ReceiptとEvidenceはvalue-safe（会話本文・private絶対pathを含まない）とする。

## 5. 承認範囲外

- 旧配置の削除（別のHuman判断）。
- `deployment_paths.py`のOS標準path定義の変更。
- 他projectまたはruntime profileへの適用の一般化。
- push、PR、外部送信。

## 6. 既存recordへの影響

new-onlyで作成した。旧Storage Decision、Layout v3承認、再記録Decision、Task Contract v2、
receipt、Evidenceは書き換えない。本Decisionが今後の保存先authorityの正本となり、
旧Storage Decisionと再記録Decisionの`logical_path`は歴史として保持される。
