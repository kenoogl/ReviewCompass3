# 契約013候補v2（自由文類型） 独立確認依頼record（headless起動対象・Claude→Reviewer）

- 作成日：2026-08-17
- 依頼元：Claude（操縦）
- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、許可model `gemini-3.1-pro-high`）
- 起動方式：`reviewcompass3-reviewer-launch launch`によるheadless機械起動（利用者の明示指示後）。fallbackは暫定手動体制
- レビュー種別：実装開始前の契約定義反証（読み取り専用・repositoryへの書込みなし）

## 1. 対象と固定（SHA-256）

```text
a8d11bb9b25829449ade68fc754c1caa013f9432407b6332573a25fe4e036d06  records/task-contract/2026-08-17-free-text-request-type-candidate-v2.md
7d52ce6eb8794de412def5dea9cf62f3d49ef27d35f26cd3154709983da0cb8f  records/development/2026-08-17-free-text-request-type-v1-self-review-v1.md
aad68904a58f8ac79a8d99b1075636e1691684fde911fc83e15edc30437d9b55  records/development/2026-08-17-free-text-request-type-prescan-v1.md
a8e48d66217774a45623c7a663b9538754b7fe514e7d1f920798780959215519  records/development/2026-08-17-free-text-request-type-reuse-search-attestation-v1.json
4c80a56c2f66ffb0baef0a10aae1680e3a04d5c2b883371c826a8f2237bfbcaf  records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md
```

## 2. 開始時の鮮度検査

起動promptが本recordのpathと期待SHA-256を渡す。読取り道具で本recordを開き、対象であることを確認する。digestの機械計算がこの実行環境で行えない場合は、freshnessへ`not_computable`と理由を記載する（内容が明らかに別物ならmismatchとして判定せず停止）。§1のdigest表は本record作成時点の固定値である。

## 3. Reviewer（あなた）への依頼：反証点

あなたは独立したReviewerです。次の反証点をそれぞれ反証的に検査し、各findingへ根拠（節番号・file・行）を付けてください。

1. **類型追加の互換保証**：契約§7.1「既存2類型の値・雛形出力を一切変えない」の受入条件（§9-3のgolden固定試験＝生成結果SHA-256の試験定数固定・契約011対象試験の無変更緑・類型推定の正準位置化後も正当な既存recordの推定不変）が、雛形共通骨格・検査共通入口の変更を確実に検出できるか。検出できない変更経路（例：共通骨格の書式ゆれ・節名の揺れ）が残らないか。
2. **自由記入節の検査設計の十分性**：§5.1-3の検査分岐（正準位置による類型推定・必須節の類型分岐・非空・placeholder不在・fence規律共通適用）と§9-1の敵対fixture（fence内偽見出し・fence外digest行・他類型labelの本文混入）で、自由文がもたらす騙され面を覆えているか。対象と固定の表の5行目（文字列理解の失敗類型と対策原則）の§2・§3に照らして欠けている類型・原則がないか。
3. **適用範囲と規律の設計妥当性**：§7.2の適用範囲・機構上の非適用5種・規律4点（既存2類型の代用禁止・起動承認境界の不変・規模の節度は運用注意・合議は範囲外）が、機械で強制する層と文書規律に留める層を明確に分けているか。規律の実効性（labelによる事後監査可能性・迂回の検出）に穴がないか。特に「規模の節度を機械上限にしない」判断（§7.4残余risk3）の緩和が十分か。
4. **受入条件・停止条件の一意性と網羅**：§9の8項（RED列挙→最小実装→golden互換→共通検査の両向き→実運用E2E→既存試験→agy完了レビュー→製品受入）が一意に実装可能で、§6保護対象・契約011の受入済み試験と矛盾しないか。§7.4残余risk 4点に欠けている重要riskがないか。

## 4. 判定の形式

- headless起動時は、起動promptが指定するJSON schemaに完全に従う構造化出力だけで返す。`verdict`は5語彙（`verified`／`verified_with_findings`／`rejected`／`stale_target`／`unable`）、`blocking`は「採用・受入を止めるべき所見」の意味、実施できなかった検査は`unexamined`配列へ明示、`summary`は日本語で書く。
- 手動fallback時は同じ項目（判定・findings・未検査・要旨）を日本語の文章で返し、冒頭にmodel名を記載する。

## 5. 判断済み・範囲外（蒸し返し不要）

- 判断済み（蒸し返し不要）：自由文類型への着手は利用者選択（2026-08-17）。類型追加は契約011候補v3が予約済み（「後続の類型追加で足す・利用者確認済み」）。適用範囲・機構上の非適用・規律4点は利用者了解済み（事前走査record §6へ固定）。拡張契約の形（契約012による010拡張の前例）。起草側自己レビューの所見3件（SR-C13-1〜3：類型推定の正準位置化・必須節分岐の明記・golden固定試験）は候補v2へ反映済み。完了レビューはagy（Tier 1）で実施。正式再利用検索は`start_allowed: true`（証明書は対象と固定の表の4行目）。
- 範囲外（「無い」という指摘は不要）：既存2類型の雛形・検査規則の変更・起動側（reviewer_launch）の変更・縦C合議・codex-cli backend・自由文内容の自動生成・`review_plan`出力の自動変換・外部API直接送信経路の後続・歴史的recordの書き換え。
- 事実の明示：本依頼record自体が契約011の正式経路（assemble→LLM記入→check合格）で組み立てられている（自由文類型は未実装のため`contract_review`類型を使用）。§7.4残余risk 4点の最終受容は利用者の製品受入判断事項（妥当性への懸念はfindingsで示してよい）。

## 6. 手順（Human・Claude向け）

1. 利用者が起動を明示指示する（起動は契約010 §2の承認境界に従う）。
2. Claudeが単体入口を実行する：

```text
reviewcompass3-reviewer-launch launch \
  --repository /Users/Daily/Development/ReviewCompass3 \
  --request records/session-handoffs/2026-08-17-free-text-request-type-contract-review-request-v1.md \
  --expected-sha256 <本record commit後のSHA-256> \
  --private-root <repo外私有領域の絶対パス> \
  --run-id <実行識別子>
```

3. アダプタが判定recordを`records/session-handoffs/2026-08-17-free-text-request-type-contract-review-verdict-v1.md`へ機械転記して単独commitし、事後照合4点を実行する。
4. `verified`系（blocking 0件）なら次のHuman判断へ進み、blocking所見があれば停止して利用者へ諮る。
