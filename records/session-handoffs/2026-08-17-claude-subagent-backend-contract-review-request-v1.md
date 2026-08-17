# 契約012候補v2 独立確認依頼record（headless起動対象・Claude→Reviewer）

- 作成日：2026-08-17
- 依頼元：Claude（操縦）
- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、許可model `gemini-3.1-pro-high`）
- 起動方式：`reviewcompass3-reviewer-launch launch`によるheadless機械起動（利用者の明示指示後）。fallbackは暫定手動体制
- レビュー種別：実装開始前の契約定義反証（読み取り専用・repositoryへの書込みなし）

## 1. 対象と固定（SHA-256）

```text
f95446a96b132c9dda5e225460cc4ab0214e535ebbc7ef9b79fdc953d936994d  records/task-contract/2026-08-17-claude-subagent-backend-candidate-v2.md
092bfc37997c1a6cd723cbfbe47364f5936fee615f2cbe09dacee72fdaa913bc  records/development/2026-08-17-claude-subagent-backend-v1-self-review-v1.md
2939237e6e2435ba05561281a4dcf09c977bb77ee5e136d9f1802ab47bd548e2  records/development/2026-08-17-claude-subagent-backend-prescan-v1.md
bc37a5be2e2e182cd76985114f5ae9156039e5475282b1f2adf35c41feba230b  records/development/2026-08-17-claude-subagent-backend-reuse-search-attestation-v1.json
```

## 2. 開始時の鮮度検査

起動promptが本recordのpathと期待SHA-256を渡す。読取り道具で本recordを開き、対象であることを確認する。digestの機械計算がこの実行環境で行えない場合は、freshnessへ`not_computable`と理由を記載する（内容が明らかに別物ならmismatchとして判定せず停止）。§1のdigest表は本record作成時点の固定値である。

## 3. Reviewer（あなた）への依頼：反証点

あなたは独立したReviewerです。次の反証点をそれぞれ反証的に検査し、各findingへ根拠（節番号・file・行）を付けてください。

1. **tier受容機構の保証**：契約§7.3の機構（Tier 1許可／Tier 2・3は`--accept-tier`一致時のみ許可・欠落と不一致は従来どおり停止・宣言と受容根拠のrecord記載）が「機械が黙って独立性を緩めない」を本当に保証するか。受容の欠落・不一致・宣言の偽装・受容根拠fileの不在といった穴が残らないか。
2. **互換の受入条件の十分性**：agy値の不変移設の証明として「agy経路の既存試験case無変更で全緑」（§9-2）と「契約011対象32件無変更で全緑」（§9-7）が十分か。`ALLOWED_RESPONSE_MODELS`の和集合化が契約011の検査意味（依頼recordの許可model照合）を変えないか。
3. **claude起動固定形の読み取り専用性**：§7.2の道具集合（Read・Glob・Grepのみ）・`--permission-mode dontAsk`・認証遮断6種（実行器定数との同値試験つき）・prompt共通雛形＋道具名差し込み（SR-C12-1反映）に、書込み・外部接続・権限昇格の抜けがないか。
4. **E2E設計の一意性**：SR-C12-2反映後の§9-8（同一対象集合の別名依頼による2 oracle比較・判定record衝突の回避・権威はアダプタ刻印・完了レビューはagy Tier 1）が一意に実装でき、work-review-protocol §5の不変制約（Tier 2／3を`high`の唯一の独立oracleにしない）と矛盾しないか。受入条件11項とRED一覧に不足がないか。

## 4. 判定の形式

- headless起動時は、起動promptが指定するJSON schemaに完全に従う構造化出力だけで返す。`verdict`は5語彙（`verified`／`verified_with_findings`／`rejected`／`stale_target`／`unable`）、`blocking`は「採用・受入を止めるべき所見」の意味、実施できなかった検査は`unexamined`配列へ明示、`summary`は日本語で書く。
- 手動fallback時は同じ項目（判定・findings・未検査・要旨）を日本語の文章で返し、冒頭にmodel名を記載する。

## 5. 判断済み・範囲外（蒸し返し不要）

- 判断済み（蒸し返し不要）：第2縦切り＝claude-subagent（利用者選択）。拡張契約の形（前例：契約009による008送信核の精密化）。宣言Tier 3の保守的扱い（別modelでもTier 3）。`--accept-tier`の起動ごと明示方式（常時受容への緩和は将来のHuman判断）。互換記号2件の維持。完了レビューはagy（Tier 1）で実施。認証遮断6種の自前定数＋同値試験（契約011の除外定数と同じ型）。
- 範囲外（「無い」という指摘は不要）：codex-cli backend・縦C合議（判定不一致の機械裁定を含む）・自由文類型・転記／照合／保存／G30登録の変更・契約011成果物の変更・外部API直接送信経路の後続。
- 事実の明示：本依頼record自体が契約011の正式経路（assemble→記入→check合格）で組み立てられている。候補v2はcr相当の自己レビュー（SR-C12-1〜3：prompt道具名の差し込み化・E2E衝突回避・受容根拠入力）を反映済み。§7.4残余risk 4点の最終受容は利用者の製品受入判断事項（妥当性への懸念はfindingsで示してよい）。

## 6. 手順（Human・Claude向け）

1. 利用者が起動を明示指示する（起動は契約010 §2の承認境界に従う）。
2. Claudeが単体入口を実行する：

```text
reviewcompass3-reviewer-launch launch \
  --repository /Users/Daily/Development/ReviewCompass3 \
  --request records/session-handoffs/2026-08-17-claude-subagent-backend-contract-review-request-v1.md \
  --expected-sha256 <本record commit後のSHA-256> \
  --private-root <repo外私有領域の絶対パス> \
  --run-id <実行識別子>
```

3. アダプタが判定recordを`records/session-handoffs/2026-08-17-claude-subagent-backend-contract-review-verdict-v1.md`へ機械転記して単独commitし、事後照合4点を実行する。
4. `verified`系（blocking 0件）なら次のHuman判断へ進み、blocking所見があれば停止して利用者へ諮る。
