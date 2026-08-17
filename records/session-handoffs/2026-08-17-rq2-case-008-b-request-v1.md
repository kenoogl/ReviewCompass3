# 実験ケースcase-008（条件B）の妥当性レビュー 独立確認依頼record（headless起動対象・Claude→Reviewer）

- 作成日：2026-08-17
- 依頼元：Claude（操縦）
- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、許可model `gemini-3.1-pro-high`）
- 起動方式：`reviewcompass3-reviewer-launch launch`によるheadless機械起動（利用者の明示指示後）。fallbackは暫定手動体制
- レビュー種別：自由文レビュー（読み取り専用・repositoryへの書込みなし）

## 1. 対象と固定（SHA-256）

```text
c0c66a692bc14fada8e6643d34984c75c1fa38b3ebd24fc640e4177770ab0404  docs/evaluation/rq2-cases/case-008/session-log-record-run.md
```

## 2. 開始時の鮮度検査

起動promptが本recordのpathと期待SHA-256を渡す。読取り道具で本recordを開き、対象であることを確認する。digestの機械計算がこの実行環境で行えない場合は、freshnessへ`not_computable`と理由を記載する（内容が明らかに別物ならmismatchとして判定せず停止）。§1のdigest表は本record作成時点の固定値である。

## 3. Reviewer（あなた）への依頼：依頼内容

あなたは独立したReviewerです。次の依頼内容を検査し、各findingへ根拠（節番号・file・行）を付けてください。

次のTask Contract実験ケースについて、対象materialの内容がContractの責務に照らして妥当かを検査してください。

- 責務（goal）：固定した一件の文書変更が束縛Requirementへ適合するかを判定し、不適合を構造化Findingとして返す。文書を書き換えず、Requirementを改訂しない。
- 対象material：
- `docs/evaluation/rq2-cases/case-008/session-log-record-run.md`（SHA-256 `c0c66a692bc14fada8e6643d34984c75c1fa38b3ebd24fc640e4177770ab0404`）

検査の問い：対象の記述は責務・境界に整合するか。各findingへ根拠（file・行）を付けてください。

## 4. 判定の形式

- headless起動時は、起動promptが指定するJSON schemaに完全に従う構造化出力だけで返す。`verdict`は5語彙（`verified`／`verified_with_findings`／`rejected`／`stale_target`／`unable`）、`blocking`は「採用・受入を止めるべき所見」の意味、実施できなかった検査は`unexamined`配列へ明示、`summary`は日本語で書く。
- 手動fallback時は同じ項目（判定・findings・未検査・要旨）を日本語の文章で返し、冒頭にmodel名を記載する。

## 5. 判断済み・範囲外（蒸し返し不要）

1. 本依頼はTask Contract実験（paired trial）の1ケースである（評価データ取得計画v1）。
2. 範囲外：対象materialの書き換え・Contract自体の改定提案・repo外の参照。
3. 事実の明示：対象materialのdigestは本record §1の表に固定済み。

## 6. 手順（Human・Claude向け）

1. 利用者が起動を明示指示する（起動は契約010 §2の承認境界に従う）。
2. Claudeが単体入口を実行する：

```text
reviewcompass3-reviewer-launch launch \
  --repository /Users/Daily/Development/ReviewCompass3 \
  --request records/session-handoffs/2026-08-17-rq2-case-008-b-request-v1.md \
  --expected-sha256 <本record commit後のSHA-256> \
  --private-root <repo外私有領域の絶対パス> \
  --run-id <実行識別子>
```

3. アダプタが判定recordを`records/session-handoffs/2026-08-17-rq2-case-008-b-verdict-v1.md`へ機械転記して単独commitし、事後照合4点を実行する。
4. `verified`系（blocking 0件）なら次のHuman判断へ進み、blocking所見があれば停止して利用者へ諮る。
