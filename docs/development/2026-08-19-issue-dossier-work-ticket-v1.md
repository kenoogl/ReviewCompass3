# issue実態調書tool 作業票 v1（範囲固定・軽量）

- 作成日：2026-08-19
- 指示者：利用者（Human）。文言「その内容で改善候補を登録して、すぐに対応」（2026-08-19 chat）
- 種別：範囲固定文書（軽量作業票）。読み取り専用の調書生成tool新設＋試験。台帳record・schema・
  検証器は不変。契約は立てない
- 固定入力：事前走査record`records/development/2026-08-19-issue-dossier-prescan-v1.md`
- 対象候補：`IC-ISSUE-RECONCILIATION-DOSSIER-001`（current_work）

## 1. 正本範囲

1. `tools/development/issue_reconciliation_dossier.py`【新設】：issueごとの機械調書
   （台帳欄・登録後の活動＝records／git言及計数・problem参照pathの生存・TODO拘束flag）を
   一行JSONで出力。全件と`--issue-id`単独の両対応。判断欄なし・決定的出力。
2. 試験（RED先行）4本：fixture調書の欄／未知IDの拒否（exit非0）／拘束flag真（fixture TODO）／
   実repo実行（8件・`ISSUE-TEST-GROWTH-STATE-PINNING-001`の拘束flag真を固定）。
3. Evidence（guard付き測定ブロック・決定的射影）。

## 2. 範囲外

治癒確認probeの宣言・実行（将来拡張）／充足判断・受容・裁定の自動化（Humanのまま）／
issue状態の変更・schema変更。

## 3. 受入条件

1 RED：新設試験のみ失敗／2 GREEN：新設4本＋writer系＋台帳関連試験群の単独0／3 実repoで
`issue_reconciliation_dossier`単独exit 0（8件・拘束flag検出を含む）／4 計画writer仕上げ・
証明書`start_allowed: true`／5 `git diff --check`・意味単位commit・`work_unit_transition`合格。

## 4. Humanの確認が要る点（覆せる形）

1. 調書の欄構成（活動・生存・拘束の3種＋台帳欄。probeなし）。
2. 拘束flagの検出方式＝TODOへのissue_id言及（行抜粋つき。意味解釈はLLM／Humanに残す）。
