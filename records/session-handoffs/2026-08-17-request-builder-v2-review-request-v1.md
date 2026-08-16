# 契約011候補v2 独立確認依頼record v1（headless起動対象・Claude→Reviewer）

- 作成日：2026-08-17
- 依頼元：Claude（操縦・契約候補v2の作成担当）
- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、許可model `gemini-3.1-pro-high`）
- 起動方式：`reviewcompass3-reviewer-launch launch`によるheadless機械起動（利用者の明示指示後）。
  fallbackは暫定手動体制（`records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md`）
- レビュー種別：実装開始前の契約定義反証（契約011。読取り専用・repositoryへの書込みなし）

## 1. 対象と固定（SHA-256）

```text
1ef08e6861276c60166255008bf7a86447a7191e12c81fc6b9827d24b5537319  records/task-contract/2026-08-17-request-builder-candidate-v2.md
7fef594b4bd4048fc4efdfa5368cb74e88d5be073a4526357827a0c1302030f3  records/development/2026-08-17-request-builder-v1-self-review-v1.md
8aa156c82653b6d873bbcf1195064f14a1a1aba3913b996225af7b2dad17a03c  records/development/2026-08-17-vertical-a-request-builder-prescan-v1.md
```

参考（契約の入力。鮮度検査は上記3件だけでよい）：正式再利用検索の証明書
`records/development/2026-08-17-vertical-a-request-builder-reuse-search-attestation-v1.json`、
設計方針メモ`records/development/2026-08-17-review-path-design-principles-memo-v1.md`、
流用元（本契約では変更しない）`tools/session_logs/redaction.py`・`tools/common/digests.py`・
`tools/reviewer_launch/record.py`・`tools/external_review/send.py`（54-58行の除外3形式定数）。

## 2. 開始時の鮮度検査

起動promptが本recordのpathと期待SHA-256を渡す。読取り道具で本recordを開き、対象であることを確認する。
digestの機械計算がこの環境で行えない場合は、freshnessへ`not_computable`と理由を記載する（内容が明らかに
別物ならmismatchとして判定せず停止）。§1のdigest表は本record作成時点の固定値である。

## 3. Reviewer（あなた）への依頼：反証4点

あなたは独立したReviewerです。対象契約候補v2を読み、次の4点をそれぞれ反証的に検査し、判定を返して
ください。各findingには根拠（契約の節番号、必要なら流用元fileの関数名・行）を付けてください。

1. **機械層の一意性**：§5.1（assemble・checkの2入口）・§7（雛形固定・7項目写像・機微検査・停止理由）・
   §8（変更上限）に、実装者が後決めできる曖昧さ・矛盾・漏れがないか。自己レビューの明確化3件
   （SR-C11-1 new-only停止、SR-C11-2 checkの再実行性と最終合格の定義、SR-C11-3 許可model定数の流用）の
   反映後、一意に実装できる書き方になっているか。
2. **検査の抜け・騙され方**：機微検査（§7.3）の除外3形式（40／64桁小文字hex・可読連結名）を装って
   実鍵形式が通り抜ける形、placeholder検査（`<<記入:`残存停止）の迂回、digest表検査（§5.1-3-3）の穴
   （存在しないfileへの参照・表の改竄・囲み記号による誤解釈）が残らないか。発見した形は受入条件の
   敵対試験への追加として提案してよい。
3. **縮小境界と流用の妥当性**：核共有＋薄い包みの流用（§6。利用者裁定verbatim転記）が保護対象の
   完全性と両立するか。除外3形式を自前定数＋同値性試験とする方式（§7.3・§9-5）が、契約009側との
   乖離リスクへの対処として妥当か。2類型限定・自由文後続の縮小が上位目的（機械化目標(1)(2)(3)）と
   整合するか。
4. **受入条件の充足性**：§9の11項とRED一覧が§5.1の範囲を網羅するか。特に§9-8のE2E
   （本契約自身の完了レビュー依頼を本toolで組み立て、受入済みの起動アダプタで起動する接続実証）の
   設計に不足がないか。

## 4. 判定の形式

- headless起動時は、起動promptが指定するJSON schemaに完全に従う構造化出力だけで返す。`verdict`は
  5語彙（`verified`／`verified_with_findings`／`rejected`／`stale_target`／`unable`）、`blocking`は
  「採用を止めるべき所見」の意味、実施できなかった検査は`unexamined`配列へ明示、`summary`は日本語。
- 手動fallback時は同じ項目（判定・findings・未検査・要旨）を日本語の文章で返し、冒頭にmodel名を記載する。

## 5. 判断済み・範囲外（蒸し返し不要）

- 判断済み：縦Aの採用と2類型限定・類型登録形・自由文後続（利用者確認済み）。核共有＋薄い包みの
  流用方針と既存4製品の包み統合の不要（利用者裁定）。除外3形式の自前定数＋同値性試験。雛形のcode内
  定数化（§7.1に不採用理由つき）。機微検査を機械検査第7項として含める（設計方針メモ§1の解決）。
  正式再利用検索の証明書掲載（AGENTS §4規則の適用第1号）。
- 範囲外（「無い」という指摘は不要）：自由文類型・依頼内容（反証点文案）の自動生成・`review_plan`出力の
  自動変換・縦C（監査・判定の多周自動化）・起動側（契約010成果）の変更・歴史的recordの書き換え。
- 残余risk（§7.4の3点）を0にすることは本契約の目的ではない。最終の受容判断は利用者が行う。

## 6. 手順（Human・Claude向け）

1. 利用者が独立確認の起動を明示指示する（起動は契約010 §2の承認境界に従う）。
2. Claudeが単体入口を実行する（外部起動はこの1回。停止時は同じ起動を繰り返さず報告する）：

```text
reviewcompass3-reviewer-launch launch \
  --repository /Users/Daily/Development/ReviewCompass3 \
  --request records/session-handoffs/2026-08-17-request-builder-v2-review-request-v1.md \
  --expected-sha256 <本record commit後のSHA-256> \
  --private-root /Users/keno/.reviewcompass3-private/reviewer-launch \
  --run-id cr-011-001
```

3. アダプタが未加工出力と起動recordを私有領域へ不変保存し、判定recordを
   `records/session-handoffs/2026-08-17-request-builder-v2-review-verdict-v1.md`へ機械転記して
   単独commitし、事後照合4点を実行する。
4. `verified`系（blocking 0件）なら利用者へ縮小境界の採用と実装開始を一判断として求める。blocking所見が
   あれば停止して利用者へ諮る。
