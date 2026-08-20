# 利用者による契約016の製品受入判断（残余risk 4点の受容） v1

- 判断日：2026-08-20
- 判断者：利用者（Human）
- 記録者：Claude
- 判断の種別：Task Contractの製品受入（契約016 §9-9）。残余riskの最終受容と、消化した改善候補の
  Outcome接続を含む

## 1. 承認文言【記録】

> 残余risk 4点を確認して受け入れる。契約016の製品処理を受け入れる。受入record・候補のOutcome接続・
> TODO更新まで進めて

（2026-08-20 chat。Claudeが提示した推奨文言と同一）

## 2. 判断対象の束縛

| 対象 | path | SHA-256 |
| --- | --- | --- |
| 契約016候補v2（受入対象） | `records/task-contract/2026-08-20-model-selection-correspondence-candidate-v2.md` | `0a4a84032fc7470b88e923ec5508785f81abf6ad3f1bb87b30a3793f1943ddf2` |
| 採用・実装開始判断 | `records/development/2026-08-20-model-selection-correspondence-contract-adoption-decision-v1.md` | `ef4cd3f8407de6154a19885c854752066c9d89eba4ad944c2f045b5b3b841dc2` |
| 起草側自己レビュー（SR-C16-1〜3） | `records/development/2026-08-20-model-selection-correspondence-v1-self-review-v1.md` | `c9a30587a84545832c1d333941dc0ca5f5b253760a0be11d8777845497b7e52f` |
| 実装Evidence（RED→GREEN） | `records/development/2026-08-20-contract-016-implementation-evidence-v1.md` | `2a1fdee75254eabded8d6345330b11107e26018fa0698d9a35a03aa5216eab23` |
| GREEN測定（単独実行の終了コード） | `records/development/2026-08-20-contract-016-green-measurements-v1.md` | `73789230243c19a6fcf05f259049ab2d52c332c327bc43a607a757844d064624` |
| RED再現の生出力（3 command機械再現） | `records/development/2026-08-20-contract-016-red-replay-output.txt` | `fec327341cc852eae30b533ec5b8e9c1db9792d0dcb84f84ff9e149dc02ddc6b` |
| 正規全試験receipt（2,668件成功・exit 0） | `records/development/2026-08-20-contract-016-full-test-receipt-v1.json` | `33d68be720f19c2f5c75187e787acdf64da77e37dc6d7a4b54f562fb744d9581` |
| §9-7実E2E判定record（codex・gpt-5.6-terra・rejected＝是正済み所見2件） | `records/session-handoffs/2026-08-20-model-selection-correspondence-completion-codex2-verdict-v1.md` | `ca8c8b5a2404ac0b5760a650f6b04ee7c37a535bb98f955a857498733310132f` |
| E2E所見の是正Evidence（＋raw点検・手戻り2件の記録） | `records/development/2026-08-20-contract-016-e2e-findings-remediation-evidence-v1.md` | `994c41dffcd1b72768a6ae0b9843c0c56bcf7277e805fc8338d1eb5bdd34aeb0` |
| 是正のGREEN測定 | `records/development/2026-08-20-contract-016-remediation-measurements-v1.md` | `80b9ee4bc4c67b8e2e0790ccfd978c8016b6db6c622a043f47fbdca7b44f10d9` |
| §9-8完了レビュー判定record（agy・verified・blocking 0件） | `records/session-handoffs/2026-08-20-model-selection-correspondence-completion-verdict-v1.md` | `8fe30c1e60725373874e14667a56817f59521485e8046c4d44b2cbdf68910971` |

## 3. 本判断が確定する事項

1. 契約`TC-RC3-PRODUCT-MODEL-SELECTION-CORRESPONDENCE-016 / v2`を**製品として受け入れる**。
   受入条件§9-1〜8の充足はEvidence（§2の表）に固定済みであり、本判断により§9-9が成立、契約は
   完了する（是正2件＝抽出開始境界・手順書旧記載、互換復元1件＝`_render`旧引数、を含む）。
2. **§7.5残余risk 4点の受容**：(1) 受入済み2製品の同時改修による回帰risk——既定不変golden・
   後方互換・正規全試験2,668件で緩和を実証済み、(2) 旧型record運用の停止化（agy記載×他backend
   起動は`request_backend_mismatch`で停止。移行整理＝今後は組み立て時に`--backend`指定）、
   (3) terraの実性能・実挙動——実E2Eで初起動・完走・rollout観測`gpt-5.6-terra`を実証済み、
   (4) 正準抽出の騙されrisk——敵対fixture 5種（開始境界を含む）で機械固定。
3. **正式経路化**：以後、承認済み許可一覧の**内側**でのmodel選択（`assemble --backend/--model`・
   `launch --model`）と、起動前の記載照合（新設2語彙）を正式経路とする。model追加は定型
   （利用者承認record＋定義1行＋承認pin 1行＝手順書「モデル追加手続き」節）に従う。直書き原則は
   維持（実行時登録機構は作らない）。
4. **消化した改善候補のOutcome接続**：`IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`（依頼recordの
   model欄とbackendの対応検査）は consumer＝契約016・Outcome＝本受入（backend別所属検査＋
   起動時の記載照合の実装と全試験合格）に接続され、**closed**とする。本候補は台帳writer整備
   （2026-08-19）以前の候補であり、正本は観測record
   `OBS-RC3-REQUEST-BUILDER-UNION-CHECK-2026-08-17-V1`＋仕分けrecord（2026-08-17）＋(b)裁定
   （許可model承認record 2026-08-20 §2-5）＋本record（閉鎖）で構成される（台帳fileは存在しない。
   形式の作り直しはしない）。
5. **実E2Eの経緯の確定**：terra E2Eの機械経路（新経路での組み立て・check合格・起動・完走・raw保存・
   転記・事後照合4点・rollout観測terra・領域外読取り0件）は成立。codex判定は`rejected`で、うち
   1件は**実装の実欠陥（抽出開始境界）を初回運用で検出**した——是正のうえ完了レビュー（agy）が
   `verified`・blocking 0件で十分性を確認した。3判定役・複数modelのレビュー体制が実欠陥を
   捕まえた実例として位置づける。

## 4. 持ち越し事項（本判断に含まれない）

- codex（sol）による再レビューは任意。実施の要否はHuman判断。
- 後続の順序選択：縦C合議（3判定役×複数modelの材料が揃った）・外部API直接送信経路の後続・
  `CLAUDE_VERSION`更新（次回その経路使用時）・RQ2追試・運用集計v8。
- E2E実施中の運用手戻り2件（並行実行によるworktree汚れ・digest表陳腐化）の再発防止は運用規律
  として是正Evidence §4に記録済み（機構変更は不要と整理）。

## 5. 未実施

- TODO・見取り図の更新（本record直後に共通手順で実施）。後続契約の定義・実装。
