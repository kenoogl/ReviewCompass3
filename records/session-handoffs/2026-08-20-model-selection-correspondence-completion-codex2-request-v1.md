# 契約016実装（モデル選択・記載照合）完了レビュー（codex terra E2E・v2） 独立確認依頼record（headless起動対象・Claude→Reviewer）

- 作成日：2026-08-20
- 依頼元：Claude（操縦）
- 依頼先：Reviewer（backend `codex-cli`、許可model `gpt-5.6-terra`）
- 起動方式：`reviewcompass3-reviewer-launch launch`によるheadless機械起動（利用者の明示指示後）。fallbackは暫定手動体制
- レビュー種別：実装完了レビュー（読み取り専用・repositoryへの書込みなし）
- 実装基準commit：`2a4116781c35a46ad49e360474c648e98f1006e1`

## 1. 対象と固定（SHA-256）

```text
0a4a84032fc7470b88e923ec5508785f81abf6ad3f1bb87b30a3793f1943ddf2  records/task-contract/2026-08-20-model-selection-correspondence-candidate-v2.md
ef4cd3f8407de6154a19885c854752066c9d89eba4ad944c2f045b5b3b841dc2  records/development/2026-08-20-model-selection-correspondence-contract-adoption-decision-v1.md
c9a30587a84545832c1d333941dc0ca5f5b253760a0be11d8777845497b7e52f  records/development/2026-08-20-model-selection-correspondence-v1-self-review-v1.md
2a1fdee75254eabded8d6345330b11107e26018fa0698d9a35a03aa5216eab23  records/development/2026-08-20-contract-016-implementation-evidence-v1.md
73789230243c19a6fcf05f259049ab2d52c332c327bc43a607a757844d064624  records/development/2026-08-20-contract-016-green-measurements-v1.md
fec327341cc852eae30b533ec5b8e9c1db9792d0dcb84f84ff9e149dc02ddc6b  records/development/2026-08-20-contract-016-red-replay-output.txt
33d68be720f19c2f5c75187e787acdf64da77e37dc6d7a4b54f562fb744d9581  records/development/2026-08-20-contract-016-full-test-receipt-v1.json
62babeef27dd9f634a7f35851bc32ff1c9596b42836b78a19227a2faa61f7b3a  tools/reviewer_launch/core.py
ccaa9b96f1e27d30e014b67cfefb3a17978c6c5c5106def82b95d2a4c438f151  tools/reviewer_launch/entry.py
ef2d6efcea54aa2bdc2c9e5a3cf9d48e9410747252916afeddae97bfc889a72d  tools/request_builder/core.py
b6eb4c86b61f82e989a0a308041270b749a41b4982a3347a7fc27268054035f7  tools/request_builder/entry.py
4906692f2f754df02f59402d98345c6fade1b26a80fc17fced6eccf2e5134c9a  tests/test_reviewer_launch.py
f1b199710ab389e74f95cf2355e72b3fad2c36d219a1af9e16783309e8c6f9d5  tests/test_request_builder.py
247ffdcbead83f428b5b8cd083c2fb79502dd3d620b2c6caba01d709698bbeec  docs/development/prompts/request-builder-run.md
1c80a85ec584453dbaa522704b870b615ad72e8b15f5e672fa8caafbbe5643fd  docs/development/prompts/reviewer-launch-run.md
```

## 2. 開始時の鮮度検査

起動promptが本recordのpathと期待SHA-256を渡す。読取り道具で本recordを開き、対象であることを確認する。digestの機械計算がこの実行環境で行えない場合は、freshnessへ`not_computable`と理由を記載する（内容が明らかに別物ならmismatchとして判定せず停止）。§1のdigest表は本record作成時点の固定値である。

## 3. Reviewer（あなた）への依頼：反証点

あなたは独立したReviewerです。次の反証点をそれぞれ反証的に検査し、各findingへ根拠（節番号・file・行）を付けてください。

1. **契約適合**：実装（`tools/reviewer_launch/core.py`・`entry.py`・`tools/request_builder/core.py`・`entry.py`）が契約016 v2 §7の固定形——正準抽出核の縦B側単一実装（領域定義・最初のbacktick対＝backend名・`許可model`対＝model名・fence状態追跡）、`launch --model`（既定＝一覧先頭・非所属は`model_not_allowed`）、起動前の記載照合（新設2語彙`request_backend_mismatch`／`request_model_mismatch`・抽出不能はfail-closed）、`assemble --backend/--model`（agy既定行は現行文言byte不変・他backendは新形差し込み）、checkのbackend別所属検査（文書全体検索の廃止）——と一致しているか。乖離があれば節番号と行で示す。
2. **既定不変・後方互換の実証の整合**：実装Evidence §3と測定ブロックが主張する証明（改修前実装から機械取得した正規化SHAとの組み立てgolden一致・実record依頼先行の逐語fixtureの抽出互換・既存試験の無変更全緑・和集合記号の維持）が試験コードの実体と整合しているか。実装後の正規全試験で発覚した保護対象（運用集計）の`_render`旧引数呼び出しへの互換復元（`model`引数の受け直し・commit `52e9f65`・全試験2,668件合格のreceiptが対象に含まれる）が、既定不変goldenと矛盾なく閉じているか。
3. **RED→GREEN手続きの追跡可能性**：RED再現（git履歴からの3 command機械再現・生出力固定・単独終了コード1）とGREEN（`exec`置換の単独実行＝entry exitがpytest自身の終了コード・5 suite全て0）が、第三者がEvidenceと機械生成fileだけで再照合できる形になっているか。
4. **騙され耐性と登録定型化**：敵対fixture 4種（fence内偽依頼先行・本文中同形行・backtick欠落・正準行除去）の両向き試験が文字列理解の原則2を満たすか。登録定型化（data-driven試験＋backendごとの承認pin 1本＋手順書「モデル追加手続き」節）が承認record規律を弱めないか。§9受入条件・§10停止条件との対応に不足がないか。

## 4. 判定の形式

- headless起動時は、起動promptが指定するJSON schemaに完全に従う構造化出力だけで返す。`verdict`は5語彙（`verified`／`verified_with_findings`／`rejected`／`stale_target`／`unable`）、`blocking`は「採用・受入を止めるべき所見」の意味、実施できなかった検査は`unexamined`配列へ明示、`summary`は日本語で書く。
- 手動fallback時は同じ項目（判定・findings・未検査・要旨）を日本語の文章で返し、冒頭にmodel名を記載する。

## 5. 判断済み・範囲外（蒸し返し不要）

- 判断済み（蒸し返し不要）：契約016 v2の採用（利用者2026-08-20）。停止語彙は新設2つ（利用者裁定）。抽出核の配置＝縦B側単一実装（SR-C16-1）。許可一覧の値は不変・選択は一覧の内側のみ・直書き原則の維持。旧型record（agy記載×他backend起動）の停止化と移行整理。完了レビューの正式判定は別途agy（Tier 1）で実施。
- 範囲外（「無い」という指摘は不要）：許可一覧の値の変更・実行時のmodel登録機構・縦C合議・`record.py`／G30／session_logs／RQ2装置の変更・過去recordの書き換え・実E2E未了の指摘（本依頼への応答自体が§9-7の実E2Eである）。
- 事実の明示：**本依頼record自体が契約016の新経路（`assemble --backend codex-cli --model gpt-5.6-terra`）で組み立てられ、check（backend別所属検査）に合格している**——冒頭の依頼先行が新形・terra記載であることが実装の生きた実例である。あなた（codex・`gpt-5.6-terra`＝**この組み合わせの初起動**）の応答完走・model観測（rollout）・記載照合の通過が§9-7の実E2E証跡になる。先行の同内容依頼（slug末尾`-codex`）は、組み立て後の互換修正commitでdigest表が陳腐化したため起動を取りやめ、本record（現物digestで再固定）へ差し替えた。§7.5残余risk 4点の最終受容は利用者の製品受入判断事項（妥当性への懸念はfindingsで示してよい）。digestの機械計算が可能な環境であれば、§1のdigest表をshasumで実照合してよい。

## 6. 手順（Human・Claude向け）

1. 利用者が起動を明示指示する（起動は契約010 §2の承認境界に従う）。
2. Claudeが単体入口を実行する：

```text
reviewcompass3-reviewer-launch launch \
  --repository /Users/Daily/Development/ReviewCompass3 \
  --request records/session-handoffs/2026-08-20-model-selection-correspondence-completion-codex2-request-v1.md \
  --expected-sha256 <本record commit後のSHA-256> \
  --private-root <repo外私有領域の絶対パス> \
  --run-id <実行識別子>
```

3. アダプタが判定recordを`records/session-handoffs/2026-08-20-model-selection-correspondence-completion-codex2-verdict-v1.md`へ機械転記して単独commitし、事後照合4点を実行する。
4. `verified`系（blocking 0件）なら次のHuman判断へ進み、blocking所見があれば停止して利用者へ諮る。
