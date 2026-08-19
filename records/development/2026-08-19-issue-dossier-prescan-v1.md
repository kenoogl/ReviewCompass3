# issue実態調書tool 事前走査 v1

- 記録日：2026-08-19
- 指示者：利用者（Human）。文言「その内容で改善候補を登録して、すぐに対応」（2026-08-19 chat。
  仕分けrecord＝`records/development/2026-08-19-issue-dossier-triage-decision-v1.md`）
- 記録者：Claude
- 上位：`IC-ISSUE-RECONCILIATION-DOSSIER-001`（current_work）
- 基準commit：`2520c8c`（本走査の生成物2件を除きclean）
- 実測：測定ブロック`records/development/2026-08-19-issue-dossier-prescan-measurements-v1.md`
  （guard付き・全4entry二重実行一致）

## 1. 実測から確定した事実

1. 新設2 file（tool・試験）の名称衝突なし。
2. **TODOのissue言及は現在1行**（active欄の`ISSUE-TEST-GROWTH-STATE-PINNING-001`＝
   「Issue状態を変更せず…」の拘束つき）。拘束flagはこの行の機械検出で実現できる。
3. 台帳の現況＝一括検証passed（候補21・決定53・issue 8＝registered 5／resolved 3）。
4. 流用部品digest固定（intake・一括検証・状態遷移）。

## 2. 設計（作業票へ渡す論点）

1. `issue_reconciliation_dossier.py`【新設】：issues-v4の全件（または`--issue-id`）について
   機械調書を一行JSONで出す——(a) 台帳欄（state・版・created_at）、(b) **登録後の活動**＝
   `records/development/*.md`でissue_id／candidate_idへ言及するfileの計数と最新filename、
   git履歴の言及commit数（git不在時はnull）、(c) **参照の生存**＝problem文中のpath様tokenの
   存在確認（欠落一覧は上限つき）、(d) **拘束flag**＝`TODO_NEXT_SESSION.md`にissue_idの言及が
   あるか＋該当行の抜粋。判断欄は持たない（充足・受容・裁定はHuman）。
2. 出力は決定的（時刻・乱数を含まない）。`--project-root`任意（試験fixture用）。
3. 試験（RED先行）4本：fixture調書の欄・未知IDの拒否・拘束flag真・実repo実行
   （8件・TEST-GROWTHのflag真＝今回人手で気づいた拘束の機械検出を固定）。
4. 範囲外：治癒確認probeの宣言・実行（将来拡張）・充足判断の自動化・issue状態の変更。

## 3. 手順5：正式再利用検索

草稿→writer finalize→先行commit→`--plan`のみ。証明書は
`records/development/2026-08-19-issue-dossier-attestation-v1.json`。

## 4. 未実施

手順5、作業票の適用、RED、GREEN、Evidence、TODO反映。
