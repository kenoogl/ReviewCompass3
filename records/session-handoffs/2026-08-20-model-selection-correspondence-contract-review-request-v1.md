# 契約016候補v2 独立確認 独立確認依頼record（headless起動対象・Claude→Reviewer）

- 作成日：2026-08-20
- 依頼元：Claude（操縦）
- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、許可model `gemini-3.1-pro-high`）
- 起動方式：`reviewcompass3-reviewer-launch launch`によるheadless機械起動（利用者の明示指示後）。fallbackは暫定手動体制
- レビュー種別：実装開始前の契約定義反証（読み取り専用・repositoryへの書込みなし）

## 1. 対象と固定（SHA-256）

```text
0a4a84032fc7470b88e923ec5508785f81abf6ad3f1bb87b30a3793f1943ddf2  records/task-contract/2026-08-20-model-selection-correspondence-candidate-v2.md
c9a30587a84545832c1d333941dc0ca5f5b253760a0be11d8777845497b7e52f  records/development/2026-08-20-model-selection-correspondence-v1-self-review-v1.md
e89adcd8085ce5bd46f62ed432aa15c3ec15b87de71edb289b77f81dc9294ad3  records/development/2026-08-20-model-selection-correspondence-prescan-v1.md
52a8c157a3b3698b62b7dd7fe72438238793dce00e1024e7c28d4ab6e4870c1a  records/development/2026-08-20-model-selection-correspondence-reuse-search-attestation-v1.json
```

## 2. 開始時の鮮度検査

起動promptが本recordのpathと期待SHA-256を渡す。読取り道具で本recordを開き、対象であることを確認する。digestの機械計算がこの実行環境で行えない場合は、freshnessへ`not_computable`と理由を記載する（内容が明らかに別物ならmismatchとして判定せず停止）。§1のdigest表は本record作成時点の固定値である。

## 3. Reviewer（あなた）への依頼：反証点

あなたは独立したReviewerです。次の反証点をそれぞれ反証的に検査し、各findingへ根拠（節番号・file・行）を付けてください。

1. **正準抽出の一意性と騙され耐性**：契約§7.2の抽出仕様——正準位置の領域定義（先頭見出し直後から最初の`## `節見出しまでのfence外`- `行群の最初の「- 依頼先：」行）、抽出規則（最初のbacktick対＝backend名・`許可model`直後のbacktick対＝model名）、抽出核の配置（`tools/reviewer_launch/core.py`単一実装・request_builderが既存依存方向で共用＝SR-C16-1）——が一意に実装でき、fence内偽行・本文中同形行・backtick欠落等の騙されに対してfail-closedで閉じているか。
2. **既定不変・後方互換の証明の十分性**：§9-2（固定入力での組み立て出力SHA-256を改修前実装からpinするgolden）と§9-3（実record依頼先行の逐語fixtureでの抽出互換＋既定組み立ての新check合格）が「現行運用を壊さない」証明として十分か。agy既定行の文言byte不変維持（§7.2）と、契約011互換記号（和集合の名称・tuple意味・先頭要素）の維持に穴がないか。
3. **新設2語彙の発火条件**：`request_backend_mismatch`（記載backend≠起動backend・抽出不能を含む）・`request_model_mismatch`（記載model≠requested model）が§7.3の条件だけで発火し、正常経路（agy既定record×agy起動・`--backend`指定record×同backend起動）で誤発火しないか。既存停止語彙との重複・意味変更がないか。移行整理（旧型record＝agy記載×他backend起動の停止化）の帰結が契約に正しく明示されているか。
4. **範囲・受入条件の完備性**：受入条件§9-1〜9とRED一覧・§10停止条件に不足がないか。登録定型化（§7.4＝データ駆動試験＋backendごとの承認pin 1本＋手順書）が承認record規律（一覧変更＝契約改定）を弱めないか。実E2E（§9-7＝terra指定初起動）の設計が一意に実装できるか。

## 4. 判定の形式

- headless起動時は、起動promptが指定するJSON schemaに完全に従う構造化出力だけで返す。`verdict`は5語彙（`verified`／`verified_with_findings`／`rejected`／`stale_target`／`unable`）、`blocking`は「採用・受入を止めるべき所見」の意味、実施できなかった検査は`unexamined`配列へ明示、`summary`は日本語で書く。
- 手動fallback時は同じ項目（判定・findings・未検査・要旨）を日本語の文章で返し、冒頭にmodel名を記載する。

## 5. 判断済み・範囲外（蒸し返し不要）

- 判断済み（蒸し返し不要）：統合1本（利用者裁定2026-08-20）。停止語彙は新設2つ（利用者裁定「停止語彙は新設2つの案で」）。許可model一覧の値は本契約で変更しない・選択は一覧の内側のみ。直書き原則の維持（実行時登録機構は作らない）。既定＝そのbackendの一覧先頭（現行互換）。抽出核は`tools/reviewer_launch/core.py`単一実装（SR-C16-1＝循環import回避・複製禁止）。実E2Eはterra指定のcodex起動（起動は別途の明示指示）。完了レビューはagy（Tier 1）。
- 範囲外（「無い」という指摘は不要）：許可一覧の値の変更・実行時のmodel登録機構・縦C合議・`record.py`／G30／session_logs／egress／RQ2装置（`rq2_paired_trial.py`・`reviewer_bridge.py`）の変更・過去recordの書き換え。
- 事実の明示：本依頼recordは契約011の正式経路（assemble→記入→check合格）で組み立てられている。候補v2は起草側自己レビュー（SR-C16-1〜3：抽出核の配置・golden／後方互換の機械化形・正準位置の領域定義）を反映済み。§7.5残余risk 4点の最終受容は利用者の製品受入判断事項（妥当性への懸念はfindingsで示してよい）。本依頼record自身は改修前の現行雛形で組み立てられており、依頼先行はagy既定形である（後方互換の実例そのもの）。

## 6. 手順（Human・Claude向け）

1. 利用者が起動を明示指示する（起動は契約010 §2の承認境界に従う）。
2. Claudeが単体入口を実行する：

```text
reviewcompass3-reviewer-launch launch \
  --repository /Users/Daily/Development/ReviewCompass3 \
  --request records/session-handoffs/2026-08-20-model-selection-correspondence-contract-review-request-v1.md \
  --expected-sha256 <本record commit後のSHA-256> \
  --private-root <repo外私有領域の絶対パス> \
  --run-id <実行識別子>
```

3. アダプタが判定recordを`records/session-handoffs/2026-08-20-model-selection-correspondence-contract-review-verdict-v1.md`へ機械転記して単独commitし、事後照合4点を実行する。
4. `verified`系（blocking 0件）なら次のHuman判断へ進み、blocking所見があれば停止して利用者へ諮る。
