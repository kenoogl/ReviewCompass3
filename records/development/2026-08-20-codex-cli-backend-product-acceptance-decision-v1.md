# 利用者による契約015の製品受入判断（残余risk 6点の受容） v1

- 判断日：2026-08-20
- 判断者：利用者（Human）
- 記録者：Claude
- 判断の種別：Task Contractの製品受入（契約015 §9-11）。残余riskの最終受容と、採用済み改善候補の
  Outcome接続を含む

## 1. 承認文言【記録】

> 残余risk 6点を確認して受け入れる。契約015の製品処理を受け入れる。受入record・候補のOutcome接続・
> TODO更新まで進めて

（2026-08-20 chat。Claudeが提示した推奨文言と同一）

## 2. 判断対象の束縛

| 対象 | path | SHA-256 |
| --- | --- | --- |
| 契約015候補v2（受入対象） | `records/task-contract/2026-08-20-codex-cli-backend-candidate-v2.md` | `e2c8b5b1aeadb3d7e295f78e4b92ea8a6edd5f878180ffbccfa471c237b8dccc` |
| §7.2・§7.4訂正record（model観測＝rollout方式） | `records/development/2026-08-20-codex-model-observation-correction-decision-v1.md` | `d97b2839ba304cdf6fa1039cf448cac981d004c9028faa9e9d97e3e886f47372` |
| 採用・実装開始判断 | `records/development/2026-08-20-codex-cli-backend-contract-adoption-decision-v1.md` | `84204f4a7bb3952339f7f9448728db0ac80de626da75dc1b45d4e075824b129c` |
| 実装Evidence（RED→GREEN） | `records/development/2026-08-20-codex-cli-backend-implementation-evidence-v1.md` | `68e3511de7377584fd203ae1ac87f0eb5d3500b303b49dfbc74c90dd734cb48e` |
| E2E所見の是正Evidence（＋raw点検・保護対象差分0） | `records/development/2026-08-20-contract-015-e2e-findings-remediation-evidence-v1.md` | `ce05e817aa0beddb1c542b1fcb640d1a065960360b0da5c677fa9c179a241351` |
| GREEN測定v2（合否＝単独実行の終了コード） | `records/development/2026-08-20-contract-015-green-measurements-v2.md` | `f9baa23456de45030e76ceeaa7317ace78169a4561bc31afca1299bef752886c` |
| RED再現の生出力（git履歴から3 command再現） | `records/development/2026-08-20-contract-015-red-replay-output.txt` | `7171d84387ba763dc281fecf9de9798c114cbaffb35ae1b55a77dbbe35d167a1` |
| 正規全試験receipt（2,645件成功・exit 0） | `records/development/2026-08-20-contract-015-full-test-receipt-v1.json` | `65bca4012690d85beb84a260e91767ecc0cda4a8a171bfcb104a614d1d0e7446` |
| §9-8実E2E判定record（codex・rejected＝是正済み所見3件） | `records/session-handoffs/2026-08-20-codex-cli-backend-completion-codex-verdict-v1.md` | `2880a7541502ead6d581205eb67d95a656e4d1487323819e98c497e3e7ddc6c8` |
| §9-10完了レビュー判定record（agy・verified・所見0件） | `records/session-handoffs/2026-08-20-codex-cli-backend-completion-verdict-v1.md` | `c8acc33d1b9a381913a262885991395d1a366ae39bc5434262a6b35bf07050d5` |

## 3. 本判断が確定する事項

1. 契約`TC-RC3-PRODUCT-CODEX-CLI-BACKEND-015 / v2＋訂正record1件`を**製品として受け入れる**。
   受入条件§9-1〜10の充足はEvidence（§2の表）に固定済みであり、本判断により§9-11が成立、契約は
   完了する。
2. **§7.5残余risk 6点の受容**：(1) 対象repository内容がopenaiのレビュー役から読まれる（正式経路と
   しての常用化。緩和：利用者指示起点・path＋SHA-256のみ運搬・起動record台帳・raw完全保存）、
   (2) 都度承認方式下のheadless完走性——実E2Eで完走を実証済み、(3) codex CLI仕様変更への追随risk
   （緩和：安全側停止・raw保存。`--output-schema`拒否→fallback確定の追随実例が一巡済み）、
   (4) `gpt-5.6-terra`は許可済みだが起動選択機構なし（先頭`gpt-5.6-sol`固定。必要時は小改定）、
   (5) 登録簿改修の回帰risk——byte不変golden一致と既存試験無変更全緑で緩和を実証済み、
   (6) repo外読取りの機械遮断は未保証——実E2Eのraw点検で領域外読取り0件を実測（緩和の実効を確認）。
3. **正式経路化**：以後、`codex-cli`はレビュー起動の正式な第3 backend（provider openai・Tier 1）と
   する。3 backend体制＝agy（Tier 1既定）・claude-subagent（Tier 3明示受容）・codex-cli（Tier 1・
   `--backend codex-cli`）。model観測はrollout方式（訂正record）を正とする。
4. **採用済み改善候補のOutcome接続**：`IC-BACKEND-REGISTRY-DEEPENING-001`（backend登録簿の深化）は
   consumer＝契約015・Outcome＝本受入（name分岐6箇所の消滅を測定v2で機械確認）に接続され、
   **closed**とする。本候補は台帳writer整備（2026-08-19）以前の候補であり、正本は観測record
   `OBS-RC3-BACKEND-REGISTRY-SHALLOW-2026-08-17-V1`＋仕分けrecord（2026-08-17）＋本record（閉鎖）で
   構成される（台帳fileは存在しない。形式の作り直しはしない）。
5. **実E2Eの経緯の確定**：codex判定は`rejected`（証拠品質への所見3件）だったが、E2Eの機械経路
   （完走・raw保存・転記・事後照合4点・領域外読取り0件）は初回で成立し、所見3件は全て是正のうえ
   完了レビュー（agy・Tier 1）が`verified`・所見0件で十分性を確認した。実装した経路が初回運用で
   実のある指摘を返したことは、契約015の正式経路としての価値の実証と位置づける。

## 4. 持ち越し事項（本判断に含まれない）

- `IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`：(b)裁定どおり独立小作業単位（合図＝利用者指示。
  承認record 2026-08-20 §2-5）。
- codexによる再レビュー（rejected→是正後の再判定）は任意。実施の要否はHuman判断。
- 後続の順序選択：縦C合議（3判定役の材料が揃った）・外部API直接送信経路の後続・
  `CLAUDE_VERSION`更新（次回その経路使用時）。
- `gpt-5.6-terra`の起動選択機構（必要時の小改定）。

## 5. 未実施

- TODO・見取り図の更新（本record直後に共通手順で実施）。後続契約の定義・実装。
