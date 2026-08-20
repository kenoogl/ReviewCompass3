# 契約015候補v2 独立確認 独立確認依頼record（headless起動対象・Claude→Reviewer）

- 作成日：2026-08-20
- 依頼元：Claude（操縦）
- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、許可model `gemini-3.1-pro-high`）
- 起動方式：`reviewcompass3-reviewer-launch launch`によるheadless機械起動（利用者の明示指示後）。fallbackは暫定手動体制
- レビュー種別：実装開始前の契約定義反証（読み取り専用・repositoryへの書込みなし）

## 1. 対象と固定（SHA-256）

```text
e2c8b5b1aeadb3d7e295f78e4b92ea8a6edd5f878180ffbccfa471c237b8dccc  records/task-contract/2026-08-20-codex-cli-backend-candidate-v2.md
d6871b9ecf9dd717cb78dac674615cb62849133c6f3a8d6545a04261e34582f1  records/development/2026-08-20-codex-cli-backend-v1-self-review-v1.md
601dde12cc154911f93fd1b4ce78bd06cfcc4f84ad869df8f2b00f2a4dc048a2  records/development/2026-08-20-codex-cli-backend-prescan-v1.md
dc0eaa5a963a586e8d381d6f16dbf7546ab27d7ad24038e8aa5f3bcae8c99bb0  records/development/2026-08-20-codex-cli-backend-reuse-search-attestation-v1.json
```

## 2. 開始時の鮮度検査

起動promptが本recordのpathと期待SHA-256を渡す。読取り道具で本recordを開き、対象であることを確認する。digestの機械計算がこの実行環境で行えない場合は、freshnessへ`not_computable`と理由を記載する（内容が明らかに別物ならmismatchとして判定せず停止）。§1のdigest表は本record作成時点の固定値である。

## 3. Reviewer（あなた）への依頼：反証点

あなたは独立したReviewerです。次の反証点をそれぞれ反証的に検査し、各findingへ根拠（節番号・file・行）を付けてください。

1. **登録簿深化の互換保証の十分性**：契約§5.1-1と§9-1〜3の機械証明（生成promptと組み立て引数のbyte不変golden・agy／claude-subagent既存試験caseの無変更全緑・name分岐6箇所の消滅確認）が「値の移設だけであること」の証明として十分か。登録簿の形の変更（§7.1）が公開記号の互換（`ALLOWED_RESPONSE_MODELS`の名称とtuple意味・`record.py`の`_backend_provider`が読む`provider`鍵）を壊す穴が残らないか。
2. **codex起動固定形の読み取り専用性**：§7.2の固定引数（read-only sandbox・危険旗の不在両向き試験・`--ephemeral`・`--ignore-user-config`・schema一時file・stdin遮断）と§7.3の認証遮断（openai系4種の直書き・起動前停止）・通過一覧（`CODEX_HOME`を含む10種）に、書込み・外部接続・権限昇格・承認迂回・API鍵混入の抜けがないか。
3. **判定取得の二段構えの安全性**：`--output-schema`を第一候補としprompt指示＋JSON抽出をfallbackとする§7.2の設計が、fail-closed原則（自動変形で救済しない）に反しないか。fallback採用の条件（RED段実測で第一候補の不成立が判明した場合のみ・採否を実装Evidenceへ記録・両方不成立は§10停止）は十分に固定されているか。§7.4のmodel観測（stream正準位置のみを正とする）に騙されの余地がないか。
4. **E2E設計と残余riskの妥当性**：§9-8の実E2E（別名依頼recordによる判定record衝突回避・rawの道具実行記録による領域外読取りの点検）が一意に実装できるか。§7.5残余risk 6点（openai露出の常用化・OnRequest下の完走性・CLI仕様追随・terra選択機構なし・登録簿改修の回帰・repo外読取り遮断の未保証）の緩和策が受入判断の材料として十分か。受入条件11項・§9-1のRED一覧・§10停止条件に不足がないか。

## 4. 判定の形式

- headless起動時は、起動promptが指定するJSON schemaに完全に従う構造化出力だけで返す。`verdict`は5語彙（`verified`／`verified_with_findings`／`rejected`／`stale_target`／`unable`）、`blocking`は「採用・受入を止めるべき所見」の意味、実施できなかった検査は`unexamined`配列へ明示、`summary`は日本語で書く。
- 手動fallback時は同じ項目（判定・findings・未検査・要旨）を日本語の文章で返し、冒頭にmodel名を記載する。

## 5. 判断済み・範囲外（蒸し返し不要）

- 判断済み（蒸し返し不要）：第3縦切り＝codex-cli backendの採用（利用者指示2026-08-20）。backend登録簿深化の同時実施（改善候補仕分けrecord 2026-08-17の裁定＝`IC-BACKEND-REGISTRY-DEEPENING-001`採用・単独着手しない）。許可model 2値`gpt-5.6-sol`・`gpt-5.6-terra`と起動model＝一覧先頭固定（利用者承認record 2026-08-20）。`IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`は(b)本契約受入後の独立小作業単位（利用者裁定・本契約の範囲外）。codex-cli＝Tier 1の機械判定（provider相違。受容手続き不要）。完了レビューはagy（Tier 1）で実施（唯一oracle禁止の不変制約）。拡張契約の形（前例：契約012による契約010の拡張）。
- 範囲外（「無い」という指摘は不要）：`tools/request_builder/`の変更・`gpt-5.6-terra`の起動時選択機構・縦C合議（判定不一致の機械裁定を含む）・`tools/session_logs/`の変更とimport（`parse_codex.py`はprovisionalのため形式知識の参照のみ）・転記／照合／保存／G30登録の変更・外部API直接送信経路の後続。
- 事実の明示：本依頼recordは契約011の正式経路（assemble→記入→check合格）で組み立てられている。候補v2は起草側自己レビュー（SR-C15-1〜4：読取り指示ブロックの差し込み単位の定義・repo外読取り遮断の未保証を残余riskへ計上・stdin遮断の起動核共通化・schema一時fileの詳細）を反映済み。§7.5残余risk 6点の最終受容は利用者の製品受入判断事項である（妥当性への懸念はfindingsで示してよい）。codexのheadless完走性・`--output-schema`の実挙動・model表記の正準位置は、契約自身がRED段実測での確定事項として留保している（「未確定である」という指摘は不要。留保の仕方の妥当性への指摘は歓迎）。

## 6. 手順（Human・Claude向け）

1. 利用者が起動を明示指示する（起動は契約010 §2の承認境界に従う）。
2. Claudeが単体入口を実行する：

```text
reviewcompass3-reviewer-launch launch \
  --repository /Users/Daily/Development/ReviewCompass3 \
  --request records/session-handoffs/2026-08-20-codex-cli-backend-contract-review-request-v1.md \
  --expected-sha256 <本record commit後のSHA-256> \
  --private-root <repo外私有領域の絶対パス> \
  --run-id <実行識別子>
```

3. アダプタが判定recordを`records/session-handoffs/2026-08-20-codex-cli-backend-contract-review-verdict-v1.md`へ機械転記して単独commitし、事後照合4点を実行する。
4. `verified`系（blocking 0件）なら次のHuman判断へ進み、blocking所見があれば停止して利用者へ諮る。
