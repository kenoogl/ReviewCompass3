# 契約011実装（所見2修正後） 独立確認依頼record（headless起動対象・Claude→Reviewer）

- 作成日：2026-08-17
- 依頼元：Claude（操縦）
- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、許可model `gemini-3.1-pro-high`）
- 起動方式：`reviewcompass3-reviewer-launch launch`によるheadless機械起動（利用者の明示指示後）。fallbackは暫定手動体制
- レビュー種別：実装完了レビュー（読み取り専用・repositoryへの書込みなし）
- 実装基準commit：`442b05f43cf535c83dcb6f2c09166507bba9386f`

## 1. 対象と固定（SHA-256）

```text
146344498d7c5ce3c228a9eccb5f7a985f260691589688b6447385236273c6a1  records/task-contract/2026-08-17-request-builder-candidate-v3.md
993e255cf3b15934ea22b76e2394840df34aacf81870c464c91fcebf7c938f74  records/development/2026-08-17-request-builder-contract-adoption-decision-v1.md
939d54afb56d4a481b9ece80d926dfbc2cc83c19981b416c0580970f854fd6ba  records/development/2026-08-17-request-builder-implementation-evidence-v1.md
8463b01cf2c501e0b4b39302012de6eb6ccac5a12a76c70d26f64096da29db0d  records/session-handoffs/2026-08-17-request-builder-implementation-completion-review-verdict-v1.md
081bd8731d0762147c0b80d155b00c59aec29972a1149fa27628209a5b423b05  tools/request_builder/__init__.py
8e0b5b9fb3422845b95771b69aecdb2734e3636f2ae694a751539c25ccdf1ef4  tools/request_builder/core.py
cd8558cdc702b2a24f8ddfae69c2c51f7749ddb6536ddc551d5ecb038f6f1116  tools/request_builder/entry.py
d75f59a2f731e0c00ff69025ff703d835d469ac073806dcbcc269fae05c70a6e  tests/test_request_builder.py
27e47832ddc52eeaccffacb73d152ef6ff74f9eaff8b2cfcee056d0766b1d933  tools/operations/operation_contract_run.py
a7b37a45c72ceba50e4ebf28c3f3039a9bc89dd1f1712d55bccb4ac764b2ef87  pyproject.toml
582ff9e3c43126ffbf7df193f3ed8ec3f53e6dbaba97352c6909667859f7281e  docs/development/prompts/request-builder-run.md
b657e917ad02a7464f395c968419839820891a9fda92cb2f6166ac652ff251e6  AGENTS.md
```

## 2. 開始時の鮮度検査

起動promptが本recordのpathと期待SHA-256を渡す。読取り道具で本recordを開き、対象であることを確認する。digestの機械計算がこの実行環境で行えない場合は、freshnessへ`not_computable`と理由を記載する（内容が明らかに別物ならmismatchとして判定せず停止）。§1のdigest表は本record作成時点の固定値である。

## 3. Reviewer（あなた）への依頼：反証点

あなたは独立したReviewerです。次の反証点をそれぞれ反証的に検査し、各findingへ根拠（節番号・file・行）を付けてください。

1. **所見2修正の実効**：前回判定（e2e-011-001。対象と固定の表の4行目）のblocking所見「fence内外を区別しない節・digest行解析」が実際に修正されているか。`core.py`の`_classified_lines`／`_section_lines`によるfence状態追跡、fence外digest行の`digest_row_outside_fence`停止、敵対試験2件（`test_check_fake_heading_inside_fence_does_not_count`・`test_check_digest_row_outside_fence_stops`）の実在と実効を確認する。
2. **修正の回帰**：fence対応の変更が既存の検査意味を変えていないか（必須節・placeholder断片・反証点番号・記入内容・空表拒否・機微検査の各停止理由が従前どおり働くか）。また修正自体が新たな騙され方（例：fence標識の変形、節見出しの別表記）を生んでいないか。
3. **前回の非blocking確認の維持**：試験が30→32件へ増えた後も、受入条件と実物の対応・核共有＋薄い包みの遵守・保護対象差分0（許可されたG30登録9行を除く）・Evidence記載との整合が維持されているか。

## 4. 判定の形式

- headless起動時は、起動promptが指定するJSON schemaに完全に従う構造化出力だけで返す。`verdict`は5語彙（`verified`／`verified_with_findings`／`rejected`／`stale_target`／`unable`）、`blocking`は「採用・受入を止めるべき所見」の意味、実施できなかった検査は`unexamined`配列へ明示、`summary`は日本語で書く。
- 手動fallback時は同じ項目（判定・findings・未検査・要旨）を日本語の文章で返し、冒頭にmodel名を記載する。

## 5. 判断済み・範囲外（蒸し返し不要）

- 判断済み（蒸し返し不要）：前回判定の所見1・3・4（受入対応・流用保護・Evidence整合）は確認済み。所見2は利用者採用の下で本修正により対処済み。契約v3・核共有裁定・2類型限定は従前どおり。
- 範囲外（「無い」という指摘は不要）：自由文類型・依頼内容の自動生成・`review_plan`出力の自動変換・縦C・起動側（契約010成果）の変更・歴史的recordの書き換え。
- 事実の明示：本依頼record自体が修正後の`assemble`・`check`合格を経ている（fence対応後の実運用実証を兼ねる）。今回の穴は文書形式解析の再発類型であり、前例（ReviewCompass2の`fence_unshielded`・正準単一fence規則）と同一原則で修正した。§7.4残余riskの最終受容は利用者の製品受入判断事項。

## 6. 手順（Human・Claude向け）

1. 利用者が起動を明示指示する（起動は契約010 §2の承認境界に従う）。
2. Claudeが単体入口を実行する：

```text
reviewcompass3-reviewer-launch launch \
  --repository /Users/Daily/Development/ReviewCompass3 \
  --request records/session-handoffs/2026-08-17-request-builder-implementation-completion-rereview-request-v1.md \
  --expected-sha256 <本record commit後のSHA-256> \
  --private-root <repo外私有領域の絶対パス> \
  --run-id <実行識別子>
```

3. アダプタが判定recordを`records/session-handoffs/2026-08-17-request-builder-implementation-completion-rereview-verdict-v1.md`へ機械転記して単独commitし、事後照合4点を実行する。
4. `verified`系（blocking 0件）なら次のHuman判断へ進み、blocking所見があれば停止して利用者へ諮る。
