# 初期開発checklist 改定r1 record

- 作成：2026-08-08。指示はHuman「今」（checklist更新の必要性確認と提案の後）
- 手順：checklist §18の改定規則に従う。適用開始はHuman判断待ち

## 1. 改定理由と利用中に見つかった不足（§18-1）

1. **Work 4Bの未追随**：構成A-1〜Dおよびreuse-search attestationの実運用（2026-08-07固定）により
   1・4項目目は完了済みだが、checkboxとEvidenceが追随していなかった
2. **統合レーンの居場所の明示不足**：進行中の評価②（統合可否）はWork 4Bの3項目目の実行形で
   あるのに、checklist上で対応が読めなかった
3. **機密レーンのowner不在**：`DEC-CONFIDENTIALITY-WORK-ORDER-001`の残項目（規則登録・C/D定義・
   遡及適用）がどの節にも属していなかった。§18の規則（新しい大域Stageを増やさず既存ownerへ
   割り当てる）に従い、機密分離を敷いたWork 1Bの後続として追加

## 2. 参照Digestの再確認（§18-2）【実測】

front matterの8参照（authority 3・policy 2・related_design 3）を現行bytesと照合し、**8件すべて一致**。

## 3. 変更内容（owner割り当て・§18-3、削除の保全・§18-4）

- Work 4B：1項目目[x]（構成B GREEN・attestation実運用）、4項目目[x]（Work 5B検査器GREEN・
  構成D台帳初回実運用）、2・3項目目へ現在の実行形の注記とrecord参照を追加
- Work 1B末尾：「Work 1B後続：機密の扱い」を新設し、残3項目を未checkで追加。出口設計の完結
  （A2中止・資産保持）を注記
- §18のEvidence欄：本recordを参照
- **削除した項目は無い**（追加とcheck・注記のみ。停止・復旧・Evidence・後継Testの喪失なし）

## 3b. 追補（Human判断「選択肢1で」2026-08-08）

改定によりchecklistのDigestを固定参照していた既存候補
`IC-CHECKLIST-APPROVAL-SCOPE-STATEMENT-DRIFT-001`の照合が破れた。候補の指摘（承認範囲外の列挙が
2026-08-05の承認3件に追随していない）自体が本文の古さであるため、r1に修復を含めた：承認・実装済み
3項目（Decision ID 3件参照）と、引き続き範囲外の3項目へ列挙を書き分けた。候補には正規tool組み立ての
triage decision（`DEC-IC-CHECKLIST-APPROVAL-SCOPE-STATEMENT-DRIFT-001`、disposition:
`current_work`、promote_to_issue: false）で決着を固定した。候補が提起した反映の時点規則は
別件のHuman判断として保留。

## 4. 適用開始（§18-5）

Humanが本改定の順序と適用開始を判断する。承認までコミットしない。
