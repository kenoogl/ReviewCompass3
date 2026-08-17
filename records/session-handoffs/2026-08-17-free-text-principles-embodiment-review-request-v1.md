# 文字列理解の原則recordの体現整合 独立確認依頼record（headless起動対象・Claude→Reviewer）

- 作成日：2026-08-17
- 依頼元：Claude（操縦）
- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、許可model `gemini-3.1-pro-high`）
- 起動方式：`reviewcompass3-reviewer-launch launch`によるheadless機械起動（利用者の明示指示後）。fallbackは暫定手動体制
- レビュー種別：自由文レビュー（読み取り専用・repositoryへの書込みなし）

## 1. 対象と固定（SHA-256）

```text
4c80a56c2f66ffb0baef0a10aae1680e3a04d5c2b883371c826a8f2237bfbcaf  records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md
e61215eddc0e7f50468c87a9b17c2cba6825fd2470a80d0bac3eca72c0e3907d  tools/request_builder/core.py
ec056cd7dd3426d60bf1333c284d250e00c3b54cbce8be84d64bf46cc32ede3f  tools/reviewer_launch/core.py
998c31d726c3aa37bd5021d83495590ad49015916ab4ca0572890465e495db8d  tools/reviewer_launch/record.py
```

## 2. 開始時の鮮度検査

起動promptが本recordのpathと期待SHA-256を渡す。読取り道具で本recordを開き、対象であることを確認する。digestの機械計算がこの実行環境で行えない場合は、freshnessへ`not_computable`と理由を記載する（内容が明らかに別物ならmismatchとして判定せず停止）。§1のdigest表は本record作成時点の固定値である。

## 3. Reviewer（あなた）への依頼：依頼内容

あなたは独立したReviewerです。次の依頼内容を検査し、各findingへ根拠（節番号・file・行）を付けてください。

原則参照record（対象と固定の表の1行目）の§4「RC3での体現」が挙げる原則1〜8の体現主張を、現行実装（表の2〜4行目）に照らして検査してほしい。

1. 各主張の実装箇所が実在し、記載どおりに働いているか（誇張・陳腐化の検出）。
2. §4の記載が自由文類型の実装後の現状（類型推定の正準位置化＝「レビュー種別」行だけを正とする方式・自由記入節の敵対fixture追加）に照らして古くなっていないか。
3. §2の原則8項のうち、実装に体現が無いのに§4が体現済みと読める箇所がないか。

前提：§4は「2026-08-17時点」と明記された時点記載であり、古さの指摘は「訂正が必要な誤り」ではなく「更新候補」として扱ってよい。ただし実装と明確に矛盾する主張はfindingsで根拠（file・行）つきで示すこと。

## 4. 判定の形式

- headless起動時は、起動promptが指定するJSON schemaに完全に従う構造化出力だけで返す。`verdict`は5語彙（`verified`／`verified_with_findings`／`rejected`／`stale_target`／`unable`）、`blocking`は「採用・受入を止めるべき所見」の意味、実施できなかった検査は`unexamined`配列へ明示、`summary`は日本語で書く。
- 手動fallback時は同じ項目（判定・findings・未検査・要旨）を日本語の文章で返し、冒頭にmodel名を記載する。

## 5. 判断済み・範囲外（蒸し返し不要）

- 判断済み（蒸し返し不要）：原則record §5の系譜出典（初代ReviewCompass等の横repository）はこのrepositoryの外にあり、本レビューでは読めない（対象外）。§4-8「類型網羅の体系化は未了」の扱いは改善候補として仕分け確定済み。契約013自体の妥当性はcr-013-001で独立確認済み（本依頼は契約レビューではなく、参照recordと実装の整合検査である）。
- 範囲外（「無い」という指摘は不要）：repository外fileの読解・実装の変更の実施・契約013の受入条件判定（§9-7完了レビューの領分）・原則recordの書き換え。
- 事実の明示：本依頼recordは契約013 §9-5の実運用E2E（自由文類型`free_text`の初の実起動）を兼ねる。判定は§4「判定の形式」のJSON schemaに従う。

## 6. 手順（Human・Claude向け）

1. 利用者が起動を明示指示する（起動は契約010 §2の承認境界に従う）。
2. Claudeが単体入口を実行する：

```text
reviewcompass3-reviewer-launch launch \
  --repository /Users/Daily/Development/ReviewCompass3 \
  --request records/session-handoffs/2026-08-17-free-text-principles-embodiment-review-request-v1.md \
  --expected-sha256 <本record commit後のSHA-256> \
  --private-root <repo外私有領域の絶対パス> \
  --run-id <実行識別子>
```

3. アダプタが判定recordを`records/session-handoffs/2026-08-17-free-text-principles-embodiment-review-verdict-v1.md`へ機械転記して単独commitし、事後照合4点を実行する。
4. `verified`系（blocking 0件）なら次のHuman判断へ進み、blocking所見があれば停止して利用者へ諮る。
