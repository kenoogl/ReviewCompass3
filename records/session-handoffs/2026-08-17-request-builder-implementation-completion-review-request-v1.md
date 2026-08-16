# 契約011実装 独立確認依頼record（headless起動対象・Claude→Reviewer）

- 作成日：2026-08-17
- 依頼元：Claude（操縦）
- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、許可model `gemini-3.1-pro-high`）
- 起動方式：`reviewcompass3-reviewer-launch launch`によるheadless機械起動（利用者の明示指示後）。fallbackは暫定手動体制
- レビュー種別：実装完了レビュー（読み取り専用・repositoryへの書込みなし）
- 実装基準commit：`4b5551f536774d402d6cbbed0c2ce3a7d6f3bb0c`

## 1. 対象と固定（SHA-256）

```text
146344498d7c5ce3c228a9eccb5f7a985f260691589688b6447385236273c6a1  records/task-contract/2026-08-17-request-builder-candidate-v3.md
993e255cf3b15934ea22b76e2394840df34aacf81870c464c91fcebf7c938f74  records/development/2026-08-17-request-builder-contract-adoption-decision-v1.md
939d54afb56d4a481b9ece80d926dfbc2cc83c19981b416c0580970f854fd6ba  records/development/2026-08-17-request-builder-implementation-evidence-v1.md
081bd8731d0762147c0b80d155b00c59aec29972a1149fa27628209a5b423b05  tools/request_builder/__init__.py
fce6f5b33d5d470260e5492605a09dc4426822d788db569cf8a2ca6c776aaeb6  tools/request_builder/core.py
cd8558cdc702b2a24f8ddfae69c2c51f7749ddb6536ddc551d5ecb038f6f1116  tools/request_builder/entry.py
2097ee5a61e03080719325ef2c43cb5c1adb40af100774f75879254291d00b3d  tests/test_request_builder.py
27e47832ddc52eeaccffacb73d152ef6ff74f9eaff8b2cfcee056d0766b1d933  tools/operations/operation_contract_run.py
a7b37a45c72ceba50e4ebf28c3f3039a9bc89dd1f1712d55bccb4ac764b2ef87  pyproject.toml
582ff9e3c43126ffbf7df193f3ed8ec3f53e6dbaba97352c6909667859f7281e  docs/development/prompts/request-builder-run.md
b657e917ad02a7464f395c968419839820891a9fda92cb2f6166ac652ff251e6  AGENTS.md
```

## 2. 開始時の鮮度検査

起動promptが本recordのpathと期待SHA-256を渡す。読取り道具で本recordを開き、対象であることを確認する。digestの機械計算がこの実行環境で行えない場合は、freshnessへ`not_computable`と理由を記載する（内容が明らかに別物ならmismatchとして判定せず停止）。§1のdigest表は本record作成時点の固定値である。

## 3. Reviewer（あなた）への依頼：反証点

あなたは独立したReviewerです。次の反証点をそれぞれ反証的に検査し、各findingへ根拠（節番号・file・行）を付けてください。

1. **受入条件と実物の対応**：契約011 v3の§9-1〜7が`tests/test_request_builder.py`（30試験）と実装実物で実際に固定されているか。試験が緩い・実装と未接続・形だけの検査になっている箇所がないか。特にcr-011-001所見の敵対試験3件（破損placeholder検知・空digest表拒否・既知すり抜け形の通過明示）が主張どおり存在し実効か。
2. **機械検査の抜け・騙され方**：`core.py`の`check`（7項目写像・`git check-ignore`・機微検査）に、契約§5.1-3・§7の取り決めからの逸脱や迂回可能な穴が残らないか（例：節見出しの偽装、digest表のfence外への記載、placeholder断片の別表記、機微検査の除外3形式定数の値の相違）。
3. **流用と保護の遵守**：核共有＋薄い包みの裁定（契約§6）どおり、redaction・digests・縦B公開部品を読取り流用しているか。保護対象へ変更が及んでいないか（許可された`operation_contract_run.py`の登録9行を除く）。除外3形式の同値性試験が実際に`send.py`実定数と比較しているか。
4. **Evidenceの主張と実物の相違**：実装Evidence（対象と固定の表の3行目）の記載——RED30失敗→全緑一発・別位置一巡実演・保護対象差分0——と実物（試験・コード・commit）に相違がないか。

## 4. 判定の形式

- headless起動時は、起動promptが指定するJSON schemaに完全に従う構造化出力だけで返す。`verdict`は5語彙（`verified`／`verified_with_findings`／`rejected`／`stale_target`／`unable`）、`blocking`は「採用・受入を止めるべき所見」の意味、実施できなかった検査は`unexamined`配列へ明示、`summary`は日本語で書く。
- 手動fallback時は同じ項目（判定・findings・未検査・要旨）を日本語の文章で返し、冒頭にmodel名を記載する。

## 5. 判断済み・範囲外（蒸し返し不要）

- 判断済み（蒸し返し不要）：契約v3はcr-011-001所見3件を利用者採用の上で反映済み。核共有＋薄い包みの流用方針と既存4製品の包み統合の不要は利用者裁定。2類型限定・自由文後続は利用者確認済み。雛形はcode内定数（契約§7.1に不採用理由つき）。
- 範囲外（「無い」という指摘は不要）：自由文類型・依頼内容の自動生成・`review_plan`出力の自動変換・縦C（監査・判定の多周自動化）・起動側（契約010成果）の変更・歴史的recordの書き換え。
- 事実の明示：本依頼record自体が契約011の`assemble`で機械生成され`check`合格を経ている（実運用E2Eの実証を兼ねる）。§7.4残余risk 4点の最終受容は利用者の製品受入判断事項であり、本レビューの範囲外（妥当性への懸念はfindingsで示してよい）。

## 6. 手順（Human・Claude向け）

1. 利用者が起動を明示指示する（起動は契約010 §2の承認境界に従う）。
2. Claudeが単体入口を実行する：

```text
reviewcompass3-reviewer-launch launch \
  --repository /Users/Daily/Development/ReviewCompass3 \
  --request records/session-handoffs/2026-08-17-request-builder-implementation-completion-review-request-v1.md \
  --expected-sha256 <本record commit後のSHA-256> \
  --private-root <repo外私有領域の絶対パス> \
  --run-id <実行識別子>
```

3. アダプタが判定recordを`records/session-handoffs/2026-08-17-request-builder-implementation-completion-review-verdict-v1.md`へ機械転記して単独commitし、事後照合4点を実行する。
4. `verified`系（blocking 0件）なら次のHuman判断へ進み、blocking所見があれば停止して利用者へ諮る。
