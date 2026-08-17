# 契約013実装（自由文類型） 独立確認依頼record（headless起動対象・Claude→Reviewer）

- 作成日：2026-08-17
- 依頼元：Claude（操縦）
- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、許可model `gemini-3.1-pro-high`）
- 起動方式：`reviewcompass3-reviewer-launch launch`によるheadless機械起動（利用者の明示指示後）。fallbackは暫定手動体制
- レビュー種別：実装完了レビュー（読み取り専用・repositoryへの書込みなし）
- 実装基準commit：`1f34c84be75a8a3d0eee092c98bc485ce723bd81`

## 1. 対象と固定（SHA-256）

```text
73a287c137a73c617e25655c35377b88a7ffc033b89e4be68d63d3b0ce245ffc  records/task-contract/2026-08-17-free-text-request-type-candidate-v3.md
83894a4ea18fa23fa382ac0f90bc86e6d0bf01d0aedc6a99cb07becdcd237528  records/development/2026-08-17-free-text-request-type-contract-adoption-decision-v1.md
7d52ce6eb8794de412def5dea9cf62f3d49ef27d35f26cd3154709983da0cb8f  records/development/2026-08-17-free-text-request-type-v1-self-review-v1.md
dcfffbec261db38ba7c58dc8b92b9c5fa3b4d708940198abedaade29ae7112a6  records/session-handoffs/2026-08-17-free-text-request-type-contract-review-verdict-v1.md
bae1ad478742e6963e5d5ae92016027d7da30eed0a8ed35a403f2f7e69442c64  records/session-handoffs/2026-08-17-free-text-principles-embodiment-review-verdict-v1.md
13135f5cd3b9865f868733ce7e1ef6d9316bbd32582db1f779250d3eaaa1fe43  records/development/2026-08-17-free-text-request-type-implementation-e2e-evidence-v1.md
ea482a3c7653b0966316012f43cc87ae426cdd5e429348a7f96c4e7f05ecd7b6  records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md
e61215eddc0e7f50468c87a9b17c2cba6825fd2470a80d0bac3eca72c0e3907d  tools/request_builder/core.py
cd8558cdc702b2a24f8ddfae69c2c51f7749ddb6536ddc551d5ecb038f6f1116  tools/request_builder/entry.py
70848852b71a77f769cc2651e3dfd84a0ba822cb20772eabd123ea9e7337cf79  tests/test_request_builder.py
9b3aa44e211d63c5386130d0f4d9d7eaf9772a4641740f4239d0489f5a8949bc  docs/development/prompts/request-builder-run.md
```

## 2. 開始時の鮮度検査

起動promptが本recordのpathと期待SHA-256を渡す。読取り道具で本recordを開き、対象であることを確認する。digestの機械計算がこの実行環境で行えない場合は、freshnessへ`not_computable`と理由を記載する（内容が明らかに別物ならmismatchとして判定せず停止）。§1のdigest表は本record作成時点の固定値である。

## 3. Reviewer（あなた）への依頼：反証点

あなたは独立したReviewerです。次の反証点をそれぞれ反証的に検査し、各findingへ根拠（節番号・file・行）を付けてください。

1. **既存2類型のbyte不変（golden）の実効**：契約§7.1「既存2類型の値・雛形出力を一切変えない」が実装で守られているか。golden固定試験（正規化した生成結果のSHA-256を試験定数へ固定・実装前実測の機械転記）の実在と、雛形共通骨格の変更を検出できる作りかを確認する。類型推定の正準位置化（冒頭「レビュー種別」行だけを正とする）が正当な既存2類型recordの推定結果を変えていないか。
2. **自由記入節の検査の両向き実効**：`free_text`の検査分岐——必須節の類型分岐（「反証点」に代えて「依頼内容」）・固定説明文を除いた非空検査・placeholder不在・fence外digest行の拒否・反証点番号検査の非適用——が両向き（停止と合格）の試験で固定されているか。敵対fixture（自由記入節のfence内偽見出し・fence外digest行・他類型labelの本文混入）の実在と実効を確認する。
3. **E2E所見採用の整合**：e2e-013-001（対象と固定の表の5行目）の所見`SEC4-OUTDATED-FREE-TEXT`の採用として行われた原則参照record（表の7行目）§4の追記更新が、現行実装と一致し、他の記載との矛盾を生んでいないか。
4. **受入条件の充足と差分の範囲限定**：契約候補v3（表の1行目）§9の受入条件1〜6がEvidence（表の6行目）どおり充足され、実装差分が§8変更上限（core.py・entry.py・対象試験・入口文書・Evidence等）に限定されているか。入口文書の使い分け規律（§7.2）の記載が契約と一致するか。

## 4. 判定の形式

- headless起動時は、起動promptが指定するJSON schemaに完全に従う構造化出力だけで返す。`verdict`は5語彙（`verified`／`verified_with_findings`／`rejected`／`stale_target`／`unable`）、`blocking`は「採用・受入を止めるべき所見」の意味、実施できなかった検査は`unexamined`配列へ明示、`summary`は日本語で書く。
- 手動fallback時は同じ項目（判定・findings・未検査・要旨）を日本語の文章で返し、冒頭にmodel名を記載する。

## 5. 判断済み・範囲外（蒸し返し不要）

- 判断済み（蒸し返し不要）：契約候補v3は独立確認cr-013-001（`verified_with_findings`・blocking 0件。対象と固定の表の4行目）を経て利用者採用済み。§9-5実運用E2Eはe2e-013-001で成立済み（同表5行目。所見は利用者指示で採用済み）。適用範囲・規律4点・残余risk 5点（prompt注入の明文化を含む）は候補v3に固定済みで、最終受容は§9-8の利用者判断事項。改善候補の仕分け（敵対fixture類型網羅＝縦C RED段へ組み込み等）は確定済み。
- 範囲外（「無い」という指摘は不要）：既存2類型の雛形・検査規則の変更・起動側（reviewer_launch）の変更・縦C合議・codex-cli backend・自由文内容の自動生成・外部API直接送信経路の後続・歴史的recordの書き換え。
- 事実の明示：本依頼recordは契約013 §9-7の完了レビュー（agy・Tier 1・既定backend）であり、契約011の正式経路（assemble→LLM記入→check合格）で組み立てられている。直近の正規全試験は2,482件成功・終了コード0（Evidence §1）。

## 6. 手順（Human・Claude向け）

1. 利用者が起動を明示指示する（起動は契約010 §2の承認境界に従う）。
2. Claudeが単体入口を実行する：

```text
reviewcompass3-reviewer-launch launch \
  --repository /Users/Daily/Development/ReviewCompass3 \
  --request records/session-handoffs/2026-08-17-free-text-request-type-implementation-completion-review-request-v1.md \
  --expected-sha256 <本record commit後のSHA-256> \
  --private-root <repo外私有領域の絶対パス> \
  --run-id <実行識別子>
```

3. アダプタが判定recordを`records/session-handoffs/2026-08-17-free-text-request-type-implementation-completion-review-verdict-v1.md`へ機械転記して単独commitし、事後照合4点を実行する。
4. `verified`系（blocking 0件）なら次のHuman判断へ進み、blocking所見があれば停止して利用者へ諮る。
