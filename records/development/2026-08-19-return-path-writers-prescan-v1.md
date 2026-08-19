# 復路writer（決定・issue登録・状態遷移）事前走査 v1

- 記録日：2026-08-19
- 指示者：利用者（Human）。文言「復路（決定・issue・verdictのwriterと状態遷移）の機械化をすぐに
  対応して」（2026-08-19 chat）
- 記録者：Claude
- 上位：`IC-LEDGER-LANE-WRITER-MECHANIZATION-001`（current_work）。前仕分けrecord §3の
  「残scopeは突合checkpoint枠で再仕分け」は、本指示による**前倒し**（処置＝current_workは不変・
  着手順のみ変更）
- 基準commit：`7761156`（本走査の生成物2件を除きclean）
- 実測：測定ブロック`records/development/2026-08-19-return-path-writers-prescan-measurements-v1.md`
  （guard付き・全5entry二重実行一致）

## 1. 実測から確定した事実

1. **issue側・決定側の組み立てと検証は既存**：`build_v4_issue_record`／`validate_v4_issue_record`／
   `validate_v4_issue_repository`（同一issue_idのfile重複と同一candidateへの有効Issue重複を拒否）、
   `build_human_triage_decision`／`validate_human_triage_decision`／
   `validate_triage_decision_repository`。**不足はコマンド入口と状態遷移だけ**。
2. **issueの状態語彙はconfig v4に固定**：registered／untriaged／deferred／in_progress／
   suspended／resolved／rejected。active＝in_progress（**上限1**）・終端＝resolved／rejected。
   欄は10欄固定で**verdict参照欄は存在しない**。fileは`issues-v4/`にissue_id小文字＋
   `--v{version}.json`。repositoryは同一issue_idの複数fileを拒否するため、**版遷移は旧fileの
   置換**（新版書き出し＋旧版除去。履歴はgitが保持）になる。
3. **verdict検証器は不在**：v2／v3／v4のいずれの設定にも`issue_resolution_verdict`の欄定義が
   なく、検証dispatchにも`resolution_verdict`種別がない。既存verdict（旧Pilot 1件・
   `record_kind: resolution_verdict`）は歴史recordで、現行検証器では検証できない。
4. 新設3 module・3試験のfile名衝突なし。
5. 流用部品（intake・pilot・既設writer・一括検証・config v4）のdigest固定済み。

## 2. 設計（作業票へ渡す論点）

1. **verdictの扱い3案**：**案A（採用）＝閉じる操作は状態遷移**（resolved／rejected）で表現し、
   判定の意味内容（残余riskの受容・未解決項目の処置・承認文言）は従来どおり
   `records/development/`のDecision recordへ記録する。検証器のあるrecordだけを台帳へ置く原則を
   守り、schema新設をしない。案B＝v4 verdict schemaの新設（欄設計のHuman承認・設定改定が必要。
   需要が実測されたら別候補として起こす）。案C＝検証器なしの旧形で書く（原則違反・却下）。
2. **決定writer**`triage_decision_writer.py`：草稿（candidate_id・candidate_record_path・
   human_fields・disposition・blocking・rationale・next_action。`decided_at`省略時は機械時刻）
   →`build_human_triage_decision`→単体検証→new-only書き出し→一行JSON・exit 0／1。
3. **issue writer**`issue_record_writer.py`：`--decision <path>`（N1形式のみ。bundle形式は歴史）
   から候補・決定を読み、`build_v4_issue_record`→単体検証→`v4_issue_path`へnew-only書き出し→
   **repository検証（失敗時は書いたfileを除去して戻す）**→一行JSON。
4. **状態遷移**`issue_state_transition.py`：`--issue-id --to-state`。語彙外は即拒否。現record
   を読み、state更新・`issue_version`＋1・`created_at`保存・digest再計算→新pathで単体検証→
   新file書き出し→旧file除去→repository検証。**失敗時はrollback**（新を除去し旧を復元）。
   active上限1・終端の扱いはrepository検証が機械強制する。
5. **一括検証の拡張**：`workflow_ledger_verify`へissues-v4のrepository検証と状態別countsを追加
   （既存欄は不変・追加のみ）。
6. 試験（RED先行）12本前後：決定writer 3・issue writer 3・遷移4・verify拡張2。

## 3. 手順5：正式再利用検索

草稿→writer finalize→先行commit→`--plan`のみ。証明書は
`records/development/2026-08-19-return-path-writers-attestation-v1.json`。

## 4. 未実施

手順5、作業票の適用、RED、GREEN、Evidence、TODO反映。
