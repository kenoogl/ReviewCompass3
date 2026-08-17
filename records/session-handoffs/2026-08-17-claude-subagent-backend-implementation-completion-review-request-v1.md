# 契約012実装（claude-subagent第2 backend） 独立確認依頼record（headless起動対象・Claude→Reviewer）

- 作成日：2026-08-17
- 依頼元：Claude（操縦）
- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、許可model `gemini-3.1-pro-high`）
- 起動方式：`reviewcompass3-reviewer-launch launch`によるheadless機械起動（利用者の明示指示後）。fallbackは暫定手動体制
- レビュー種別：実装完了レビュー（読み取り専用・repositoryへの書込みなし）
- 実装基準commit：`3cab229c4f291a70fe493569fe7dfa528a04622a`

## 1. 対象と固定（SHA-256）

```text
f95446a96b132c9dda5e225460cc4ab0214e535ebbc7ef9b79fdc953d936994d  records/task-contract/2026-08-17-claude-subagent-backend-candidate-v2.md
5af17a1ede1f109d7f378af9457bc1d5f4e044107128c378599163167abc8959  records/development/2026-08-17-claude-subagent-backend-contract-adoption-decision-v1.md
979b48868bdc69751c60fec4bb3f5e9abdf910b4c7d30b941b5cd7fe0922a7de  records/development/2026-08-17-claude-subagent-backend-implementation-evidence-v1.md
d6f7420db1948f1755fd9db62453cc1f44e43427839d70408c30ee259b050703  records/development/2026-08-17-subagent-allowed-models-approval-v1.md
3e96a358ea21c7c8a7e08a2436d3546d16dfb6e577706de29ddb1c96e6645375  records/development/2026-08-17-claude-subagent-verbose-argument-correction-decision-v1.md
d80b03d55ea1a75b742aa51f89f3428429eba51fd5bb55986037e808b42b3175  records/development/2026-08-17-claude-subagent-passthrough-environment-correction-decision-v1.md
db84857854cda3bb8381535bd872653d5d82032d5f59d2a7799d023efad1d199  records/development/2026-08-17-claude-subagent-child-injection-correction-decision-v1.md
9cde9965fbd120cc30a20c9af6cc45061b153e3d3172691974d5a2ac548c7bcc  records/session-handoffs/2026-08-17-claude-subagent-backend-implementation-completion-review-subagent-verdict-v1.md
7f5533027462e79b517beadc638d24a7602db4801bae39534e5fadefed47b7a6  tools/reviewer_launch/core.py
0b7f569aae8f8b7f1b0668fcab3f9024ed3571d131e5cbb7fe3dc89bb61ff1db  tools/reviewer_launch/entry.py
998c31d726c3aa37bd5021d83495590ad49015916ab4ca0572890465e495db8d  tools/reviewer_launch/record.py
58cc7f40f31d348e8d942a90e886ca8af177c679120c4327aba888a7d7472c70  tests/test_reviewer_launch.py
27e47832ddc52eeaccffacb73d152ef6ff74f9eaff8b2cfcee056d0766b1d933  tools/operations/operation_contract_run.py
```

## 2. 開始時の鮮度検査

起動promptが本recordのpathと期待SHA-256を渡す。読取り道具で本recordを開き、対象であることを確認する。digestの機械計算がこの実行環境で行えない場合は、freshnessへ`not_computable`と理由を記載する（内容が明らかに別物ならmismatchとして判定せず停止）。§1のdigest表は本record作成時点の固定値である。

## 3. Reviewer（あなた）への依頼：反証点

あなたは独立したReviewerです。次の反証点をそれぞれ反証的に検査し、各findingへ根拠（節番号・file・行）を付けてください。

1. **F-1修正の実効**：先行E2E判定（e2e-012-001。対象と固定の表の8行目）のblocking所見「agy経路の応答model照合が和集合を使う」が実際に修正されているか。agy分岐の照合がagy専用一覧定数（先頭underscoreつきの`core.py`冒頭定数）へ差し替わり、和集合`ALLOWED_RESPONSE_MODELS`は契約011互換の記号（和集合の組み立て・import基準）に限定されたか。固定試験`test_agy_model_check_uses_agy_list_not_union`（和集合にだけ入るmodel名をstreamに流し`response_model_not_allowed`停止を確かめる）の実在と実効を確認する。
2. **修正の回帰**：試験側の差し替え対象4箇所（agy起動補助1・個別試験3）がagy専用一覧定数へ変わったことで、既存agy試験の検査意味（値・停止理由・要求modelが一覧先頭のままである点）が変わっていないか。また本修正が新たな穴（例：agy専用一覧が空のときの停止挙動の変化）を生んでいないか。
3. **F-3対処の実効**：claude経路の判定取り込みの両向き固定——結果本文にJSONが無い場合と、JSONだがschema必須鍵を欠く場合の双方が`verdict_schema_nonconforming`で停止し、未加工出力の保存が停止前に完了していること——の試験2件の実在と実効（契約§9-6「JSON抽出・schema検証が両向きで働く」の充足）を確認する。
4. **実装全体の成立の維持**：tier受容機構（`--accept-tier`欠落・不一致・受容根拠不在での起動前停止と、一致＋実在時だけの許可・起動record記載）、claude起動固定形（`Read,Glob,Grep`のみ・書込み道具や`dangerously-skip-permissions`類の危険旗の不在・両向き試験）、訂正3件（`--verbose`位置・通過変数9種・抑制注入9種の実行器同値）と認証遮断6種の実行器同値が、修正後の現行実装でも維持されているか。実装差分がF-1〜F-3対処（照合1行・試験追加3件・差し替え対象4箇所）に限定されているかを確認する。

## 4. 判定の形式

- headless起動時は、起動promptが指定するJSON schemaに完全に従う構造化出力だけで返す。`verdict`は5語彙（`verified`／`verified_with_findings`／`rejected`／`stale_target`／`unable`）、`blocking`は「採用・受入を止めるべき所見」の意味、実施できなかった検査は`unexamined`配列へ明示、`summary`は日本語で書く。
- 手動fallback時は同じ項目（判定・findings・未検査・要旨）を日本語の文章で返し、冒頭にmodel名を記載する。

## 5. 判断済み・範囲外（蒸し返し不要）

- 判断済み（蒸し返し不要）：§9-8実E2Eは2往復で成立済み（e2e-012-001＝`rejected`・blocking F-1検出→利用者採用でF-1〜F-3修正→e2e-012-002＝`verified_with_findings`・blocking 0件）。F-4〜F-7・R-1〜R-2（非blocking）はHuman仕分けへ回すことが利用者承認済みであり、本レビューでの再指摘は不要。契約候補v2の独立確認`verified`・subagent許可model（`claude-opus-5`1値）の承認・訂正3件（`--verbose`・通過変数・抑制注入）・claude本体2.1.224のpin更新は判断済み。直近の正規全試験2,467件は終了コード0。
- 範囲外（「無い」という指摘は不要）：codex-cli backend・縦C（合議・判定record比較の上位層）・自由文類型・外部API直接送信経路（pending）・歴史的recordの書き換え・契約011成果物（`tools/request_builder/`）の変更。
- 事実の明示：本依頼recordは契約012 §9-10の**完了レビュー**（agy・Tier 1・既定backend。受容入力は不要）である。§9-8のE2E別名依頼（slug末尾`-subagent`）と**同一対象集合・同じdigest表13行**を持ち、同一対象へのclaude-subagent判定（e2e-012-002・対象と固定の表の8行目は一往復目判定record）と本レビューのagy判定が並ぶ**初の2 oracle比較**を成立させる。§7.4残余risk 4点の最終受容は§9-11の利用者判断事項。

## 6. 手順（Human・Claude向け）

1. 利用者が起動を明示指示する（起動は契約010 §2の承認境界に従う）。
2. Claudeが単体入口を実行する：

```text
reviewcompass3-reviewer-launch launch \
  --repository /Users/Daily/Development/ReviewCompass3 \
  --request records/session-handoffs/2026-08-17-claude-subagent-backend-implementation-completion-review-request-v1.md \
  --expected-sha256 <本record commit後のSHA-256> \
  --private-root <repo外私有領域の絶対パス> \
  --run-id <実行識別子>
```

3. アダプタが判定recordを`records/session-handoffs/2026-08-17-claude-subagent-backend-implementation-completion-review-verdict-v1.md`へ機械転記して単独commitし、事後照合4点を実行する。
4. `verified`系（blocking 0件）なら次のHuman判断へ進み、blocking所見があれば停止して利用者へ諮る。
