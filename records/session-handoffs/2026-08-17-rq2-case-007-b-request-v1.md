# 実験ケースcase-007（条件B）の妥当性レビュー 独立確認依頼record（headless起動対象・Claude→Reviewer）

- 作成日：2026-08-17
- 依頼元：Claude（操縦）
- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、許可model `gemini-3.1-pro-high`）
- 起動方式：`reviewcompass3-reviewer-launch launch`によるheadless機械起動（利用者の明示指示後）。fallbackは暫定手動体制
- レビュー種別：自由文レビュー（読み取り専用・repositoryへの書込みなし）

## 1. 対象と固定（SHA-256）

```text
0b1c065cf94514b3d9e0da56829d84353f78066d5905458276d450c09726c579  docs/evaluation/rq2-cases/case-007/contract-approval-boundary.md
```

## 2. 開始時の鮮度検査

起動promptが本recordのpathと期待SHA-256を渡す。読取り道具で本recordを開き、対象であることを確認する。digestの機械計算がこの実行環境で行えない場合は、freshnessへ`not_computable`と理由を記載する（内容が明らかに別物ならmismatchとして判定せず停止）。§1のdigest表は本record作成時点の固定値である。

## 3. Reviewer（あなた）への依頼：依頼内容

あなたは独立したReviewerです。次の依頼内容を検査し、各findingへ根拠（節番号・file・行）を付けてください。

次の対象materialを読み、記述の妥当性を検査してください。

- 対象material：
- `docs/evaluation/rq2-cases/case-007/contract-approval-boundary.md`（SHA-256 `0b1c065cf94514b3d9e0da56829d84353f78066d5905458276d450c09726c579`）

検査の問い：対象materialの記述に、**内部矛盾**（同じ事柄が別々の箇所で食い違う）・**事実の誤り**（数や識別子が他の記載と合わない）・**必要な記述の欠落**・**判定できない曖昧さ**が無いかを検査してください。材料が複数ある場合は材料間の整合も見てください。
各findingには根拠（fileのpathと行）を必ず付けてください。問題が無ければfindingsを空にしてください。

## 4. 判定の形式

- headless起動時は、起動promptが指定するJSON schemaに完全に従う構造化出力だけで返す。`verdict`は5語彙（`verified`／`verified_with_findings`／`rejected`／`stale_target`／`unable`）、`blocking`は「採用・受入を止めるべき所見」の意味、実施できなかった検査は`unexamined`配列へ明示、`summary`は日本語で書く。
- 手動fallback時は同じ項目（判定・findings・未検査・要旨）を日本語の文章で返し、冒頭にmodel名を記載する。

## 5. 判断済み・範囲外（蒸し返し不要）

1. 本依頼はTask Contract実験（RQ2 paired trial）の1ケースである（評価データ取得計画v1）。
2. 範囲外：材料の書き換えの実施・対象material以外の文書の参照・実験そのものの是非。
3. 対象materialは運用recordの**複製**である。複製であること・複製元の所在・版の新旧は検査対象ではない（それらを理由とする指摘は範囲外）。
4. 事実の明示：対象materialのdigestは本record §1の表に固定済みである。

## 6. 手順（Human・Claude向け）

1. 利用者が起動を明示指示する（起動は契約010 §2の承認境界に従う）。
2. Claudeが単体入口を実行する：

```text
reviewcompass3-reviewer-launch launch \
  --repository /Users/Daily/Development/ReviewCompass3 \
  --request records/session-handoffs/2026-08-17-rq2-case-007-b-request-v1.md \
  --expected-sha256 <本record commit後のSHA-256> \
  --private-root <repo外私有領域の絶対パス> \
  --run-id <実行識別子>
```

3. アダプタが判定recordを`records/session-handoffs/2026-08-17-rq2-case-007-b-verdict-v1.md`へ機械転記して単独commitし、事後照合4点を実行する。
4. `verified`系（blocking 0件）なら次のHuman判断へ進み、blocking所見があれば停止して利用者へ諮る。
