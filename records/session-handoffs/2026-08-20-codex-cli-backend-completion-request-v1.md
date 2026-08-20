# 契約015実装（codex-cli第3 backend）完了レビュー 独立確認依頼record（headless起動対象・Claude→Reviewer）

- 作成日：2026-08-20
- 依頼元：Claude（操縦）
- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、許可model `gemini-3.1-pro-high`）
- 起動方式：`reviewcompass3-reviewer-launch launch`によるheadless機械起動（利用者の明示指示後）。fallbackは暫定手動体制
- レビュー種別：実装完了レビュー（読み取り専用・repositoryへの書込みなし）
- 実装基準commit：`a5728676763e13424abba99a0e2e961626dad140`

## 1. 対象と固定（SHA-256）

```text
e2c8b5b1aeadb3d7e295f78e4b92ea8a6edd5f878180ffbccfa471c237b8dccc  records/task-contract/2026-08-20-codex-cli-backend-candidate-v2.md
84204f4a7bb3952339f7f9448728db0ac80de626da75dc1b45d4e075824b129c  records/development/2026-08-20-codex-cli-backend-contract-adoption-decision-v1.md
d97b2839ba304cdf6fa1039cf448cac981d004c9028faa9e9d97e3e886f47372  records/development/2026-08-20-codex-model-observation-correction-decision-v1.md
f0f0536ccda07d942e06c1d96fa75c2781387763f63afd0439a5d9c9f7d67c99  records/development/2026-08-20-codex-allowed-models-approval-v1.md
ce6ccaf74b3a6e887b59d414cc2666cdd3f090d6d58acd8fcffa063c9893c164  records/development/2026-08-20-codex-cli-backend-red-probe-evidence-v1.md
68e3511de7377584fd203ae1ac87f0eb5d3500b303b49dfbc74c90dd734cb48e  records/development/2026-08-20-codex-cli-backend-implementation-evidence-v1.md
f9baa23456de45030e76ceeaa7317ace78169a4561bc31afca1299bef752886c  records/development/2026-08-20-contract-015-green-measurements-v2.md
7171d84387ba763dc281fecf9de9798c114cbaffb35ae1b55a77dbbe35d167a1  records/development/2026-08-20-contract-015-red-replay-output.txt
65bca4012690d85beb84a260e91767ecc0cda4a8a171bfcb104a614d1d0e7446  records/development/2026-08-20-contract-015-full-test-receipt-v1.json
ce05e817aa0beddb1c542b1fcb640d1a065960360b0da5c677fa9c179a241351  records/development/2026-08-20-contract-015-e2e-findings-remediation-evidence-v1.md
2880a7541502ead6d581205eb67d95a656e4d1487323819e98c497e3e7ddc6c8  records/session-handoffs/2026-08-20-codex-cli-backend-completion-codex-verdict-v1.md
88d3dab9bebafc87a7a3757c8216710f7517cffe4b6101fca6d4cb08b1ab2684  tools/reviewer_launch/core.py
946e5fc4291ee9cb8f6ae179a11017d87e7b95da5848f5e1a436b13b276f6f9d  tools/reviewer_launch/entry.py
c7c5364ab72f5097557a00f086fdcc0cc5c555bb93bc1cfb5186645af8a04330  tests/test_reviewer_launch.py
8cf52d9f7dc0d9f70d93b34035deeaad65a72ebe58372be037d906133ec65cd0  docs/development/prompts/reviewer-launch-run.md
```

## 2. 開始時の鮮度検査

起動promptが本recordのpathと期待SHA-256を渡す。読取り道具で本recordを開き、対象であることを確認する。digestの機械計算がこの実行環境で行えない場合は、freshnessへ`not_computable`と理由を記載する（内容が明らかに別物ならmismatchとして判定せず停止）。§1のdigest表は本record作成時点の固定値である。

## 3. Reviewer（あなた）への依頼：反証点

あなたは独立したReviewerです。次の反証点をそれぞれ反証的に検査し、各findingへ根拠（節番号・file・行）を付けてください。

1. **契約適合**：実装（`tools/reviewer_launch/core.py`・`entry.py`）が契約015 v2 §7と訂正record——backend登録簿の深化、codex固定引数列（`exec`・`--json`・`--sandbox read-only`・`--skip-git-repo-check`・`--ignore-user-config`・`-m`・prompt末尾）、openai系4種の遮断、rollout（`turn_context.model`）によるmodel観測、stdin遮断（全backend共通）、prompt読取り指示ブロックの差し込み——と一致しているか。乖離があれば節番号と行で示す。
2. **互換の機械証明**：生成promptのbyte不変golden一致・agy／claude既存試験の無変更全緑・和集合4値（先頭＝agy値不変）・契約011対象42件無変更全緑（測定ブロックv2）が「現行値の不変移設」の証明として十分か。和集合pin試験2本のliteral更新の整理（実装Evidence §5）が停止条件（互換が保てない）に該当しないとする判断は妥当か。
3. **先行E2E所見の是正の十分性**：codex E2E判定（`rejected`・C15-REVIEW-001〜003）に対する是正——(1) 合否測定を`exec`置換の単独実行へ（測定v2。entry exitがpytest自身の終了コード）、(2) RED再現をgit履歴からの3 command機械再現＋生出力固定へ、(3) 遮断試験の4変数網羅化——が各指摘を実質的に解消しているか。残る穴があれば示す。
4. **受入条件の充足**：契約§9-1〜7・9の各条件（RED先行・互換・分岐消滅・危険旗不在・遮断・合成stream・和集合・正規全試験2,645件受領・保護対象差分0）と§9-8実E2E（完走・raw保存・転記・事後照合4点・領域外読取り0件の点検）がEvidence群から機械的に追えるか。§9-11（残余risk 6点の受容）へ進める状態か。

## 4. 判定の形式

- headless起動時は、起動promptが指定するJSON schemaに完全に従う構造化出力だけで返す。`verdict`は5語彙（`verified`／`verified_with_findings`／`rejected`／`stale_target`／`unable`）、`blocking`は「採用・受入を止めるべき所見」の意味、実施できなかった検査は`unexamined`配列へ明示、`summary`は日本語で書く。
- 手動fallback時は同じ項目（判定・findings・未検査・要旨）を日本語の文章で返し、冒頭にmodel名を記載する。

## 5. 判断済み・範囲外（蒸し返し不要）

- 判断済み（蒸し返し不要）：契約015 v2の採用と実装開始（利用者2026-08-20）。判定取得＝prompt指示＋JSON抽出のfallback確定（`--output-schema`はserver側strict検査で拒否＝RED実測）。model観測＝rollout方式への契約訂正（利用者承認済み）。許可model 2値・起動は一覧先頭固定（承認record）。`IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`は(b)別作業単位。`gpt-5.6-terra`の起動選択機構は範囲外。
- 範囲外（「無い」という指摘は不要）：`tools/request_builder/`の変更・縦C合議・`tools/session_logs/`の変更・外部API後続・codexの再レビュー実施の要否（Human判断事項）。
- 事実の明示：本依頼recordは契約011の正式経路（assemble→記入→check合格）で組み立てられている。あなた（agy・Tier 1）の判定が契約§9-10の完了レビューの正式判定である。先行するcodex E2E判定（対象に含む）は`rejected`だったが、その全所見への是正Evidenceも対象に含まれており、反証点3で是正の十分性を判定してほしい。§7.5残余risk 6点の最終受容は利用者の製品受入判断事項（妥当性への懸念はfindingsで示してよい）。digestの機械計算がこの実行環境で行えない場合の扱いは§2のとおり。

## 6. 手順（Human・Claude向け）

1. 利用者が起動を明示指示する（起動は契約010 §2の承認境界に従う）。
2. Claudeが単体入口を実行する：

```text
reviewcompass3-reviewer-launch launch \
  --repository /Users/Daily/Development/ReviewCompass3 \
  --request records/session-handoffs/2026-08-20-codex-cli-backend-completion-request-v1.md \
  --expected-sha256 <本record commit後のSHA-256> \
  --private-root <repo外私有領域の絶対パス> \
  --run-id <実行識別子>
```

3. アダプタが判定recordを`records/session-handoffs/2026-08-20-codex-cli-backend-completion-verdict-v1.md`へ機械転記して単独commitし、事後照合4点を実行する。
4. `verified`系（blocking 0件）なら次のHuman判断へ進み、blocking所見があれば停止して利用者へ諮る。
