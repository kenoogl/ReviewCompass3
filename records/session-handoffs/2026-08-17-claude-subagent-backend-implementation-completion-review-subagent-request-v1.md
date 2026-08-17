# 契約012実装（claude-subagent第2 backend） 独立確認依頼record（headless起動対象・Claude→Reviewer）

- 作成日：2026-08-17
- 依頼元：Claude（操縦）
- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、許可model `gemini-3.1-pro-high`）
- 起動方式：`reviewcompass3-reviewer-launch launch`によるheadless機械起動（利用者の明示指示後）。fallbackは暫定手動体制
- レビュー種別：実装完了レビュー（読み取り専用・repositoryへの書込みなし）
- 実装基準commit：`6b2eacbb944f8f53f7e76ee16b63f5f278a2670f`

## 1. 対象と固定（SHA-256）

```text
f95446a96b132c9dda5e225460cc4ab0214e535ebbc7ef9b79fdc953d936994d  records/task-contract/2026-08-17-claude-subagent-backend-candidate-v2.md
5af17a1ede1f109d7f378af9457bc1d5f4e044107128c378599163167abc8959  records/development/2026-08-17-claude-subagent-backend-contract-adoption-decision-v1.md
979b48868bdc69751c60fec4bb3f5e9abdf910b4c7d30b941b5cd7fe0922a7de  records/development/2026-08-17-claude-subagent-backend-implementation-evidence-v1.md
d6f7420db1948f1755fd9db62453cc1f44e43427839d70408c30ee259b050703  records/development/2026-08-17-subagent-allowed-models-approval-v1.md
3e96a358ea21c7c8a7e08a2436d3546d16dfb6e577706de29ddb1c96e6645375  records/development/2026-08-17-claude-subagent-verbose-argument-correction-decision-v1.md
d80b03d55ea1a75b742aa51f89f3428429eba51fd5bb55986037e808b42b3175  records/development/2026-08-17-claude-subagent-passthrough-environment-correction-decision-v1.md
db84857854cda3bb8381535bd872653d5d82032d5f59d2a7799d023efad1d199  records/development/2026-08-17-claude-subagent-child-injection-correction-decision-v1.md
d0e97d3742319b6d0c1c63ef70171afda25d5193249203d1d3c4e37c512c996c  tools/reviewer_launch/core.py
0b7f569aae8f8b7f1b0668fcab3f9024ed3571d131e5cbb7fe3dc89bb61ff1db  tools/reviewer_launch/entry.py
998c31d726c3aa37bd5021d83495590ad49015916ab4ca0572890465e495db8d  tools/reviewer_launch/record.py
7363c3733cdba4e7276653cefcdfe9918be31c2f26308b59e80b63085bac99ef  tests/test_reviewer_launch.py
27e47832ddc52eeaccffacb73d152ef6ff74f9eaff8b2cfcee056d0766b1d933  tools/operations/operation_contract_run.py
```

## 2. 開始時の鮮度検査

起動promptが本recordのpathと期待SHA-256を渡す。読取り道具で本recordを開き、対象であることを確認する。digestの機械計算がこの実行環境で行えない場合は、freshnessへ`not_computable`と理由を記載する（内容が明らかに別物ならmismatchとして判定せず停止）。§1のdigest表は本record作成時点の固定値である。

## 3. Reviewer（あなた）への依頼：反証点

あなたは独立したReviewerです。次の反証点をそれぞれ反証的に検査し、各findingへ根拠（節番号・file・行）を付けてください。

1. **値移設の不変（agy互換）**：backend一般化（`BACKENDS`登録形、許可model・禁止環境変数・通過変数のbackend別分岐）でagy経路の値と挙動が一切変わっていないか。agy側の許可model定数（先頭underscoreつきの`core.py`冒頭定数）・`FORBIDDEN_AUTH_ENVIRONMENT`・`PASSTHROUGH_ENVIRONMENT`（7変数・注入なし）の不変、和集合`ALLOWED_RESPONSE_MODELS`の先頭要素がagy値のままである点、agy子環境に`USER`等や注入キーが入らないことの固定試験の実在と実効を、`tools/reviewer_launch/core.py`と`tests/test_reviewer_launch.py`で反証的に確認する。
2. **tier受容機構の実効**：契約§7.3どおりか——別プロバイダはTier 1で従来どおり許可、claude-subagent（宣言Tier 3）は`--accept-tier`欠落・不一致で`reviewer_not_independent_tier`停止、一致でも受容根拠pathの実在なしは`acceptance_reference_missing`停止、一致＋実在のときだけ起動へ進み、起動recordへ宣言tier・受容根拠が記載されるか。該当試験群の両向き（停止と許可）の実在を確認する。
3. **claude起動固定形と訂正3件の整合**：`build_claude_arguments`が読み取り専用（`Read,Glob,Grep`のみ・書込み道具や`dangerously-skip-permissions`類の危険旗の不在・両向き試験）であり、訂正record 3件——`--verbose`（stream-json直後）・通過変数（実行器`ALLOWED_CHILD_ENVIRONMENT`9変数と同値）・抑制注入（実行器注入9種と同値）——が契約v2＋訂正overlayどおり実装され、同値性が試験で固定されているか。認証遮断6種が実行器定数と同値で、存在時に起動前停止するか。
4. **stream解析と判定取り込みの両向き実効**：`_claude_observed_models`のmodel照合（許可外は`response_model_not_allowed`停止・raw保存後）、`_claude_extract_verdict`のJSON抽出と`validate_verdict`のschema検査（不適合は`verdict_schema_nonconforming`停止・raw保存済み）が、claude形式の合成streamによる両向き試験で固定されているか。

## 4. 判定の形式

- headless起動時は、起動promptが指定するJSON schemaに完全に従う構造化出力だけで返す。`verdict`は5語彙（`verified`／`verified_with_findings`／`rejected`／`stale_target`／`unable`）、`blocking`は「採用・受入を止めるべき所見」の意味、実施できなかった検査は`unexamined`配列へ明示、`summary`は日本語で書く。
- 手動fallback時は同じ項目（判定・findings・未検査・要旨）を日本語の文章で返し、冒頭にmodel名を記載する。

## 5. 判断済み・範囲外（蒸し返し不要）

- 判断済み（蒸し返し不要）：契約候補v2は独立確認`verified`（機械転記済み判定record）の上で利用者採用済み。subagent許可model（`claude-opus-5`の1値）は利用者承認済み。訂正3件（`--verbose`・通過変数・抑制注入）はいずれも利用者承認のHuman判断record（契約v2への訂正overlay）済み。claude本体2.1.224のpin更新は別recordで承認済みで、直近の正規全試験2,464件は終了コード0。
- 範囲外（「無い」という指摘は不要）：codex-cli backend・縦C（合議・判定record比較の上位層）・自由文類型・外部API直接送信経路（pending）・歴史的recordの書き換え・契約011成果物（`tools/request_builder/`）の変更。
- 事実の明示：本依頼recordは§9-8実E2E用の**別名依頼**（slug末尾`-subagent`）であり、§9-10のagy完了レビューと同一対象集合（同じdigest表）を持つ。冒頭の依頼先行は組み立て器の雛形既定（agy）の記載であり、**起動backend・tierの権威はアダプタが起動record・判定recordへ刻印する値**（契約010 SR-C10-1）。本起動はclaude-subagent（宣言Tier 3・`--accept-tier 3`・受容根拠record `records/development/2026-08-17-e2e-012-001-tier3-acceptance-v1.md`）で行う。§7.4残余risk 4点の最終受容は§9-11の利用者判断事項。

## 6. 手順（Human・Claude向け）

1. 利用者が起動を明示指示する（起動は契約010 §2の承認境界に従う）。
2. Claudeが単体入口を実行する：

```text
reviewcompass3-reviewer-launch launch \
  --repository /Users/Daily/Development/ReviewCompass3 \
  --request records/session-handoffs/2026-08-17-claude-subagent-backend-implementation-completion-review-subagent-request-v1.md \
  --expected-sha256 <本record commit後のSHA-256> \
  --private-root <repo外私有領域の絶対パス> \
  --run-id <実行識別子>
```

3. アダプタが判定recordを`records/session-handoffs/2026-08-17-claude-subagent-backend-implementation-completion-review-subagent-verdict-v1.md`へ機械転記して単独commitし、事後照合4点を実行する。
4. `verified`系（blocking 0件）なら次のHuman判断へ進み、blocking所見があれば停止して利用者へ諮る。
