# 実験ケースcase-001（条件A2）の妥当性レビュー 独立確認依頼record（headless起動対象・Claude→Reviewer）

- 作成日：2026-08-17
- 依頼元：Claude（操縦）
- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、許可model `gemini-3.1-pro-high`）
- 起動方式：`reviewcompass3-reviewer-launch launch`によるheadless機械起動（利用者の明示指示後）。fallbackは暫定手動体制
- レビュー種別：自由文レビュー（読み取り専用・repositoryへの書込みなし）

## 1. 対象と固定（SHA-256）

```text
f818d2c47a7899f8c5b2788d0cee06f67b5dba6951a8885172c1d0d0724c59e2  docs/evaluation/rq2-cases/case-001/contract-canonical-sequence.md
2de3b0e9914ef8eb04f769384ab4f815e66c8930e90f18f6e667a1df5d7f79a4  docs/evaluation/rq2-cases/case-001/observation-prefix-record-shapes.md
7fcc05822017ca0b79c59732b382dcb8d07c1d1cc31f3dffc4fd14d57701df6c  docs/evaluation/rq2-cases/case-001/pool-01.md
1f490bec67ea7d4f1c654c9c975048268b75ade2a57b475de540e122c1ae22a4  docs/evaluation/rq2-cases/case-001/pool-02.md
c0a336182dfd91288a70ec7d4783da9ec17677c6051d7941cdf49064f424df27  docs/evaluation/rq2-cases/case-001/pool-03.md
bb9ff7af54c4bc50e59e7a83a263cf83658cb23cf63226af326e6a55a252c464  docs/evaluation/rq2-cases/case-001/pool-04.md
70d62f5d1565f1ace241a058e7e817ffaf6e2a5d90b5750b85c08200a15f3214  docs/evaluation/rq2-cases/case-001/pool-05.md
f4cfe9af7925cee8fd3ec2cf023777a08f669d2e79f95cf42561caca77f5c479  docs/evaluation/rq2-cases/case-001/pool-06.md
c3e758b85e4300877ee8d5efae0a6dc1bd9202dfb2bedb9fd56398c1b7074a40  docs/evaluation/rq2-cases/case-001/pool-07.md
eca6751986d6a6327b972a8802cdcaaaa0c3aa08b4e1c8939f44022a77c885eb  docs/evaluation/rq2-cases/case-001/pool-08.md
9eb89e279288f570dd6f73cf149f1c1fb9dd9ee217b3e0508796ee4aeaa80949  docs/evaluation/rq2-cases/case-001/pool-09.md
ecb596d986e40ca40c8dc7ec22adc573f79d3c71b9247e747cb2aa0b935e6d0e  docs/evaluation/rq2-cases/case-001/pool-10.md
```

## 2. 開始時の鮮度検査

起動promptが本recordのpathと期待SHA-256を渡す。読取り道具で本recordを開き、対象であることを確認する。digestの機械計算がこの実行環境で行えない場合は、freshnessへ`not_computable`と理由を記載する（内容が明らかに別物ならmismatchとして判定せず停止）。§1のdigest表は本record作成時点の固定値である。

## 3. Reviewer（あなた）への依頼：依頼内容

あなたは独立したReviewerです。次の依頼内容を検査し、各findingへ根拠（節番号・file・行）を付けてください。

次の対象materialを読み、記述の妥当性を検査してください。

- 対象material：
- `docs/evaluation/rq2-cases/case-001/contract-canonical-sequence.md`（SHA-256 `f818d2c47a7899f8c5b2788d0cee06f67b5dba6951a8885172c1d0d0724c59e2`）
- `docs/evaluation/rq2-cases/case-001/observation-prefix-record-shapes.md`（SHA-256 `2de3b0e9914ef8eb04f769384ab4f815e66c8930e90f18f6e667a1df5d7f79a4`）
- `docs/evaluation/rq2-cases/case-001/pool-01.md`（SHA-256 `7fcc05822017ca0b79c59732b382dcb8d07c1d1cc31f3dffc4fd14d57701df6c`）
- `docs/evaluation/rq2-cases/case-001/pool-02.md`（SHA-256 `1f490bec67ea7d4f1c654c9c975048268b75ade2a57b475de540e122c1ae22a4`）
- `docs/evaluation/rq2-cases/case-001/pool-03.md`（SHA-256 `c0a336182dfd91288a70ec7d4783da9ec17677c6051d7941cdf49064f424df27`）
- `docs/evaluation/rq2-cases/case-001/pool-04.md`（SHA-256 `bb9ff7af54c4bc50e59e7a83a263cf83658cb23cf63226af326e6a55a252c464`）
- `docs/evaluation/rq2-cases/case-001/pool-05.md`（SHA-256 `70d62f5d1565f1ace241a058e7e817ffaf6e2a5d90b5750b85c08200a15f3214`）
- `docs/evaluation/rq2-cases/case-001/pool-06.md`（SHA-256 `f4cfe9af7925cee8fd3ec2cf023777a08f669d2e79f95cf42561caca77f5c479`）
- `docs/evaluation/rq2-cases/case-001/pool-07.md`（SHA-256 `c3e758b85e4300877ee8d5efae0a6dc1bd9202dfb2bedb9fd56398c1b7074a40`）
- `docs/evaluation/rq2-cases/case-001/pool-08.md`（SHA-256 `eca6751986d6a6327b972a8802cdcaaaa0c3aa08b4e1c8939f44022a77c885eb`）
- `docs/evaluation/rq2-cases/case-001/pool-09.md`（SHA-256 `9eb89e279288f570dd6f73cf149f1c1fb9dd9ee217b3e0508796ee4aeaa80949`）
- `docs/evaluation/rq2-cases/case-001/pool-10.md`（SHA-256 `ecb596d986e40ca40c8dc7ec22adc573f79d3c71b9247e747cb2aa0b935e6d0e`）

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
  --request records/session-handoffs/2026-08-17-rq2-case-001-a2-request-v1.md \
  --expected-sha256 <本record commit後のSHA-256> \
  --private-root <repo外私有領域の絶対パス> \
  --run-id <実行識別子>
```

3. アダプタが判定recordを`records/session-handoffs/2026-08-17-rq2-case-001-a2-verdict-v1.md`へ機械転記して単独commitし、事後照合4点を実行する。
4. `verified`系（blocking 0件）なら次のHuman判断へ進み、blocking所見があれば停止して利用者へ諮る。
