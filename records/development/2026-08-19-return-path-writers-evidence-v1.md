# 復路writer（決定・issue登録・状態遷移）実行Evidence v1

- 記録日：2026-08-19。指示者：利用者（Human）「復路（決定・issue・verdictのwriterと状態遷移）の
  機械化をすぐに対応して」（chat。`IC-LEDGER-LANE-WRITER-MECHANIZATION-001`残scopeの前倒し）
- 範囲固定：作業票`docs/development/2026-08-19-return-path-writers-work-ticket-v1.md`／事前走査同
  prescan v1。基準`7761156`→文書・計画（writer）`d943aa0`→証明書`f3628b2`→実装は本record同一commit

## 1. 成果物

1. **決定writer**`triage_decision_writer.py`【新設】：草稿（意味欄のみ）→
   `build_human_triage_decision`→単体検証→new-only書き出し。時刻・指紋束縛・置き場は機械決定。
2. **issue writer**`issue_record_writer.py`【新設】：昇格決定（N1形式）→`build_v4_issue_record`→
   単体検証→new-only書き出し→**repository検証（不合格なら自file除去で原状復帰）**。
3. **状態遷移**`issue_state_transition.py`【新設】：`--issue-id --to-state`で版遷移
   （state更新・版＋1・`created_at`保存・digest再計算・旧file置換）。語彙外は即拒否、
   repository検証不合格は**rollback**（旧復元・新除去）。active上限1・重複拒否は既存検証が
   機械強制（rollbackは試験で実証）。
4. **一括検証の拡張**`workflow_ledger_verify.py`：issues-v4のrepository検証と状態別countsを
   勘定へ追加（既存欄不変）。
5. 試験13本【新設・拡張】：決定writer 4・issue writer 3・遷移4・verify拡張2
   （fixtureは候補→決定→issue→遷移の実連鎖）。

## 2. verdictの設計判断（案A採用・覆せる形）

事前走査§1-3の実測：**verdict record（旧`resolution_verdict`）には現行の検証器が存在しない**
（v2／v3／v4のどの設定にも欄定義なし・検証dispatchに種別なし。既存1件は歴史record）。検証器の
ないrecordを台帳へ書くのは原則違反のため、**閉じる操作は状態遷移（resolved／rejected＝config
既定の終端状態）で表現し、判定の意味内容（残余riskの受容・未解決項目の処置・承認文言）は従来
どおり`records/development/`のDecision recordへ記録する**（案A）。v4 verdict schemaの新設（案B）
は需要が実測されたら別候補として起こす。

## 3. RED→GREEN

RED＝新設13本のみ失敗（module未存在・`13 failed, 5 passed`・terminal転記）。GREEN・受入＝
**受入測定ブロック`records/development/2026-08-19-return-path-writers-evidence-measurements-v1.md`
参照**（writer系22本exit 0・台帳関連68本exit 0・実repo一括検証exit 0＝候補20・決定52・
**issue 8件（registered 8）**の勘定でfindings空・新設と拡張8 fileのdigest固定・全entry
二重実行一致）。`git diff --check`合格。

## 4. 効果（復路の機械化の完成）

- 台帳laneの全record種別（候補・仕分け決定・issue・状態遷移）が**writerコマンド経由・検証合格時
  のみ書き出し**になり、LLMの都度組み立てが構造的に消えた。
- 「実装済みでもregisteredのまま」を解消する道具（状態遷移）が揃い、issue実態の突合
  （checkpoint候補）は道具の初回実運用として実施できる。
- 一括検証は往路＋復路（候補・決定・issue）を1コマンドで覆う。

## 5. 未実施

TODO反映とcommit。push（利用者の運用に従う）。既存issue 8件の状態変更（突合作業の領分）。
AGENTS §4への復路writer反映（Human判断）。
