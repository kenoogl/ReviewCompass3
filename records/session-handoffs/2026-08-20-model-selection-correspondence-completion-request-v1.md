# 契約016実装（モデル選択・記載照合・登録定型化）完了レビュー 独立確認依頼record（headless起動対象・Claude→Reviewer）

- 作成日：2026-08-20
- 依頼元：Claude（操縦）
- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、許可model `gemini-3.1-pro-high`）
- 起動方式：`reviewcompass3-reviewer-launch launch`によるheadless機械起動（利用者の明示指示後）。fallbackは暫定手動体制
- レビュー種別：実装完了レビュー（読み取り専用・repositoryへの書込みなし）
- 実装基準commit：`e93b9cd957c1f2ba4b1062922e3150d687891bd4`

## 1. 対象と固定（SHA-256）

```text
0a4a84032fc7470b88e923ec5508785f81abf6ad3f1bb87b30a3793f1943ddf2  records/task-contract/2026-08-20-model-selection-correspondence-candidate-v2.md
ef4cd3f8407de6154a19885c854752066c9d89eba4ad944c2f045b5b3b841dc2  records/development/2026-08-20-model-selection-correspondence-contract-adoption-decision-v1.md
c9a30587a84545832c1d333941dc0ca5f5b253760a0be11d8777845497b7e52f  records/development/2026-08-20-model-selection-correspondence-v1-self-review-v1.md
2a1fdee75254eabded8d6345330b11107e26018fa0698d9a35a03aa5216eab23  records/development/2026-08-20-contract-016-implementation-evidence-v1.md
73789230243c19a6fcf05f259049ab2d52c332c327bc43a607a757844d064624  records/development/2026-08-20-contract-016-green-measurements-v1.md
fec327341cc852eae30b533ec5b8e9c1db9792d0dcb84f84ff9e149dc02ddc6b  records/development/2026-08-20-contract-016-red-replay-output.txt
33d68be720f19c2f5c75187e787acdf64da77e37dc6d7a4b54f562fb744d9581  records/development/2026-08-20-contract-016-full-test-receipt-v1.json
ca8c8b5a2404ac0b5760a650f6b04ee7c37a535bb98f955a857498733310132f  records/session-handoffs/2026-08-20-model-selection-correspondence-completion-codex2-verdict-v1.md
994c41dffcd1b72768a6ae0b9843c0c56bcf7277e805fc8338d1eb5bdd34aeb0  records/development/2026-08-20-contract-016-e2e-findings-remediation-evidence-v1.md
80b9ee4bc4c67b8e2e0790ccfd978c8016b6db6c622a043f47fbdca7b44f10d9  records/development/2026-08-20-contract-016-remediation-measurements-v1.md
04a25bd07c43364dbe6282545e86007c4e22e7c9305ce15c1559104266eeb69c  tools/reviewer_launch/core.py
ccaa9b96f1e27d30e014b67cfefb3a17978c6c5c5106def82b95d2a4c438f151  tools/reviewer_launch/entry.py
ef2d6efcea54aa2bdc2c9e5a3cf9d48e9410747252916afeddae97bfc889a72d  tools/request_builder/core.py
b6eb4c86b61f82e989a0a308041270b749a41b4982a3347a7fc27268054035f7  tools/request_builder/entry.py
690cf31f41b8301419b55955a194375582e53acc86e3704b5461f42ed481f138  tests/test_reviewer_launch.py
f1b199710ab389e74f95cf2355e72b3fad2c36d219a1af9e16783309e8c6f9d5  tests/test_request_builder.py
247ffdcbead83f428b5b8cd083c2fb79502dd3d620b2c6caba01d709698bbeec  docs/development/prompts/request-builder-run.md
3acaed33ae9b916f4ca1d15b7c686ae9e089300f21bb8814b320b2f192a9ae8d  docs/development/prompts/reviewer-launch-run.md
```

## 2. 開始時の鮮度検査

起動promptが本recordのpathと期待SHA-256を渡す。読取り道具で本recordを開き、対象であることを確認する。digestの機械計算がこの実行環境で行えない場合は、freshnessへ`not_computable`と理由を記載する（内容が明らかに別物ならmismatchとして判定せず停止）。§1のdigest表は本record作成時点の固定値である。

## 3. Reviewer（あなた）への依頼：反証点

あなたは独立したReviewerです。次の反証点をそれぞれ反証的に検査し、各findingへ根拠（節番号・file・行）を付けてください。

1. **契約適合**：実装が契約016 v2 §7の固定形——正準抽出核（縦B側単一実装・**開始境界＝先頭見出し行の直後から**＝F-016-001是正後・fence状態追跡・fail-closed）、`launch --model`と起動前の記載照合（新設2語彙）、`assemble --backend/--model`（agy既定行byte不変・他backend新形）、checkのbackend別所属検査——と一致しているか。乖離があれば節番号と行で示す。
2. **先行E2E所見の是正の十分性**：terra E2E判定（`rejected`・F-016-001／002）への是正——(1) 開始境界の実装（敵対試験のRED先行→最小実装→全緑＝commit `0519daa`）、(2) 手順書の旧記載（terra選択は範囲外）の契約016整合への更新——が各指摘を実質的に解消しているか。あわせて、実装後の正規全試験で発覚した保護対象（運用集計）の`_render`旧引数呼び出しへの互換復元（`52e9f65`・保護対象は無変更・全試験2,668件合格のreceipt）が既定不変goldenと矛盾なく閉じているか。
3. **§9-7実E2Eの成立**：terra指定の組み立て（新経路の実運用初使用・check合格）→起動→完走・raw保存・転記・事後照合4点・**rollout観測＝gpt-5.6-terra**・領域外読取り0件（是正Evidence §3）が、選択機構と記載照合の一気通貫の機械証明として十分か。途中の手戻り2件（並行実行によるworktree_not_clean停止・digest表陳腐化→別名再組み立て）の整理（是正Evidence §4）が妥当か。
4. **証拠の追跡可能性と登録定型化**：RED再現（git履歴からの3 command機械再現）・GREEN（単独実行の終了コード）・既定不変golden・後方互換fixture・敵対fixture 5種が第三者再照合可能な形か。登録定型化（data-driven試験＋backendごとの承認pin＋手順書「モデル追加手続き」節）が承認record規律を弱めないか。§9受入条件・§10停止条件との対応に不足がないか。

## 4. 判定の形式

- headless起動時は、起動promptが指定するJSON schemaに完全に従う構造化出力だけで返す。`verdict`は5語彙（`verified`／`verified_with_findings`／`rejected`／`stale_target`／`unable`）、`blocking`は「採用・受入を止めるべき所見」の意味、実施できなかった検査は`unexamined`配列へ明示、`summary`は日本語で書く。
- 手動fallback時は同じ項目（判定・findings・未検査・要旨）を日本語の文章で返し、冒頭にmodel名を記載する。

## 5. 判断済み・範囲外（蒸し返し不要）

- 判断済み（蒸し返し不要）：契約016 v2の採用と実装開始（利用者2026-08-20）。停止語彙は新設2つ（利用者裁定）。抽出核＝縦B側単一実装。許可一覧の値は不変・選択は一覧の内側のみ・直書き原則の維持。旧型record（agy記載×他backend起動）の停止化と移行整理。terra E2Eの機械経路成立（是正Evidence §3の実測）。
- 範囲外（「無い」という指摘は不要）：許可一覧の値の変更・実行時のmodel登録機構・縦C合議・`record.py`／G30／session_logs／egress／RQ2装置の変更・過去recordの書き換え・codex再レビュー実施の要否（Human判断事項）。
- 事実の明示：本依頼recordは契約011の正式経路で組み立てられている（既定＝agy形・本recordの依頼先行自体が既定不変の実例）。あなた（agy・Tier 1）の判定が契約§9-8の完了レビューの正式判定である。先行するterra E2E判定（対象に含む）は`rejected`だったが、全所見への是正Evidenceも対象に含まれており、反証点2で是正の十分性を判定してほしい。§7.5残余risk 4点の最終受容は利用者の製品受入判断事項（妥当性への懸念はfindingsで示してよい）。

## 6. 手順（Human・Claude向け）

1. 利用者が起動を明示指示する（起動は契約010 §2の承認境界に従う）。
2. Claudeが単体入口を実行する：

```text
reviewcompass3-reviewer-launch launch \
  --repository /Users/Daily/Development/ReviewCompass3 \
  --request records/session-handoffs/2026-08-20-model-selection-correspondence-completion-request-v1.md \
  --expected-sha256 <本record commit後のSHA-256> \
  --private-root <repo外私有領域の絶対パス> \
  --run-id <実行識別子>
```

3. アダプタが判定recordを`records/session-handoffs/2026-08-20-model-selection-correspondence-completion-verdict-v1.md`へ機械転記して単独commitし、事後照合4点を実行する。
4. `verified`系（blocking 0件）なら次のHuman判断へ進み、blocking所見があれば停止して利用者へ諮る。
