> 本fileはReviewCompass3の評価実験（RQ2 paired trial）で使う複製材料である。運用中の
> record・手順書ではないため、本fileを根拠に運用判断をしないこと。

# 契約010 実E2E第7試行（e2e-010-007）成功Evidence v1

- 記録日：2026-08-17
- 記録者：Claude
- 実施根拠：利用者の明示指示「e2e-010-007で再実施して」（chat）
- 結果：**成功（終了コード0）。契約§9-8（実E2E 1回）が成立し、同一起動で§9-10（独立完了レビュー）の
  判定`verified`を取得した**

## 1. 一往復の完走【実測】

入口の最終出力（verbatim）：

```json
{"backend":"antigravity-cli","model":"gemini-3.1-pro-high","raw_digest":"fc9d1be582fe3646e55afd21858eb0a6d1d429ba956c9f1709d917b55793ad3c","record_commit":"e87d9f60c35710f540162dd6cc4ac7ece48e0b49","record_relative_path":"records/session-handoffs/2026-08-16-reviewer-launch-adapter-implementation-completion-review-verdict-v1.md","run_id":"e2e-010-007","status":"succeeded","tier":1,"verdict":"verified","verification":{"checks":["freshness","single_record_commit","evidence","schema_form"],"status":"passed"}}
```

- 起動→読取り→構造化判定→判定recordの機械転記→**そのrecord 1件だけの単独commit**（`e87d9f68`。
  Claude側でも`git show --stat`により単独性を照合済み）→事後照合4点（鮮度・単独commit・根拠・形式）
  合格、まで全自動で完了した。**Human運搬0回**。
- 判定record：`records/session-handoffs/2026-08-16-reviewer-launch-adapter-implementation-completion-review-verdict-v1.md`。
  冒頭にReviewer（google／gemini-3.1-pro-high・アダプタ照合済み）・Tier 1（アダプタ判定）・起動方式・
  未加工出力の保存先種別とSHA-256を記載（契約§9-5どおり）。
- 未加工出力・起動record：私有領域`e2e-010-007/`へ不変保存（SHA-256 `fc9d1be5…93ad3c`）。

## 2. レビューの実施深度【実測】

- 所要79.99秒、入力132,972 token（cache読取り216,246の表示を含む）・出力9,453 token・道具error 0件。
- 読取り9件：依頼record・`tests/test_reviewer_launch.py`・`tools/reviewer_launch/`の3 module・
  `tools/operations/operation_contract_run.py`・実装Evidence record。反証4点の対象実物を実際に読んだ
  上での判定である。
- 鮮度はReviewer申告`not_computable`（理由：端末command不可）＋アダプタの二重再計算合格（設計どおり。
  自己レビューSR-C10-2の型）。
- findings 0件・unexamined空配列・verdict`verified`。対象commit `6f3d55d`を正しく参照。

## 3. 効いた訂正の連鎖（7試行の要約）

| 試行 | 停止／成果 | 確定した事実と訂正 |
| --- | --- | --- |
| 001 | 停止（model未観測） | `--print`は値旗（Go flag形式）→`--旗=値`形式へ |
| 002 | 停止（model未観測） | stream実形式（`init.model`／`result.response`）とheadless自動拒否の確定→解析訂正・prompt訂正 |
| 003 | 停止（構造不適合） | 作業領域内読取りは許可・領域外は拒否死→promptを領域内へ限定 |
| 004 | 停止（構造不適合） | 読取り道具は絶対path要求→絶対path明示 |
| 005 | 停止（構造不適合） | repository内でもread_fileは承認必須と確定 |
| 006 | 停止（構造不適合） | `--sandbox`は許可方式に影響しないと確定 |
| 007 | **成功** | 利用者の既存読取りgrantへの`--project`束縛が有効 |

7試行すべてで自動再試行0・権限迂回0・raw／起動record完全保存。停止の都度、保存rawの機械診断→
契約の留保範囲内の訂正→利用者承認→新識別子、の型を維持した。

## 4. 設定項目の記録【記録：利用者提供】

利用者のAgent設定には、本repositoryの読み取り許可のほかに「sandbox外のcommand実行のAllow/deny」
「特定の端末commandのAllow/deny」が存在する。現契約は最小権限（読み取り許可のみ）で成立しており
追加許可は使用しない。Reviewer側digest実計算を将来求める場合に特定command許可（例：`shasum`）を
契約改定として検討できる。

## 5. 受入条件の充足状況

- §9-1〜7：実装Evidence（2026-08-16）で充足済み。
- §9-8：**本試行で成立**（認証・headless挙動・schema強制・保存・転記・事後照合を実環境で実測）。
- §9-9：保護対象の差分0を最終状態で再確認（基準`41a705b`。許可された`operation_contract_run.py`
  +9行のみ）。全試験は本record commit後のTODO更新時に再実行して記録する。
- §9-10：**本試行の判定`verified`（findings 0件・blocking 0件）が独立完了レビューに相当**
  （依頼record §6-4の設計どおり）。
- §9-11：未実施。利用者の製品受入（§2承認境界と§7.4残余riskの最終受容）の判断待ち。
