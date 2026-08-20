# 契約015実装（codex-cli第3 backend）完了レビュー（codex E2E） 独立確認依頼record（headless起動対象・Claude→Reviewer）

- 作成日：2026-08-20
- 依頼元：Claude（操縦）
- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、許可model `gemini-3.1-pro-high`）
- 起動方式：`reviewcompass3-reviewer-launch launch`によるheadless機械起動（利用者の明示指示後）。fallbackは暫定手動体制
- レビュー種別：実装完了レビュー（読み取り専用・repositoryへの書込みなし）
- 実装基準commit：`ee41cddce4455cbe8654f8e19ebbe06d2c03a14c`

## 1. 対象と固定（SHA-256）

```text
e2c8b5b1aeadb3d7e295f78e4b92ea8a6edd5f878180ffbccfa471c237b8dccc  records/task-contract/2026-08-20-codex-cli-backend-candidate-v2.md
84204f4a7bb3952339f7f9448728db0ac80de626da75dc1b45d4e075824b129c  records/development/2026-08-20-codex-cli-backend-contract-adoption-decision-v1.md
d97b2839ba304cdf6fa1039cf448cac981d004c9028faa9e9d97e3e886f47372  records/development/2026-08-20-codex-model-observation-correction-decision-v1.md
f0f0536ccda07d942e06c1d96fa75c2781387763f63afd0439a5d9c9f7d67c99  records/development/2026-08-20-codex-allowed-models-approval-v1.md
ce6ccaf74b3a6e887b59d414cc2666cdd3f090d6d58acd8fcffa063c9893c164  records/development/2026-08-20-codex-cli-backend-red-probe-evidence-v1.md
68e3511de7377584fd203ae1ac87f0eb5d3500b303b49dfbc74c90dd734cb48e  records/development/2026-08-20-codex-cli-backend-implementation-evidence-v1.md
8d0352bf89ccbfce53bad5961801a88c5723e8afe9aef635357cd8d7610895ba  records/development/2026-08-20-contract-015-green-measurements-v1.md
88d3dab9bebafc87a7a3757c8216710f7517cffe4b6101fca6d4cb08b1ab2684  tools/reviewer_launch/core.py
946e5fc4291ee9cb8f6ae179a11017d87e7b95da5848f5e1a436b13b276f6f9d  tools/reviewer_launch/entry.py
0443c38e61880e6c330f7c38182390df900f53cea174a655132c6a3dee361866  tests/test_reviewer_launch.py
8cf52d9f7dc0d9f70d93b34035deeaad65a72ebe58372be037d906133ec65cd0  docs/development/prompts/reviewer-launch-run.md
```

## 2. 開始時の鮮度検査

起動promptが本recordのpathと期待SHA-256を渡す。読取り道具で本recordを開き、対象であることを確認する。digestの機械計算がこの実行環境で行えない場合は、freshnessへ`not_computable`と理由を記載する（内容が明らかに別物ならmismatchとして判定せず停止）。§1のdigest表は本record作成時点の固定値である。

## 3. Reviewer（あなた）への依頼：反証点

あなたは独立したReviewerです。次の反証点をそれぞれ反証的に検査し、各findingへ根拠（節番号・file・行）を付けてください。

1. **契約適合**：実装（`tools/reviewer_launch/core.py`・`entry.py`）が契約015 v2 §7と訂正record（2026-08-20）の固定形——backend登録簿の深化（読取り指示ブロック・引数組み立て関数・stream解析関数・許可model・環境一覧の登録化）、codex固定引数列（`exec`・`--json`・`--sandbox read-only`・`--skip-git-repo-check`・`--ignore-user-config`・`-m`・prompt末尾）、openai系4種の遮断、rollout（`turn_context.model`）によるmodel観測、stdin遮断——と一致しているか。乖離があれば節番号と行で示す。
2. **互換の機械証明の整合**：実装Evidence §3と測定ブロックが主張する互換証明（生成promptのbyte不変golden一致・agy／claude既存試験の無変更全緑・和集合4値の先頭＝agy値不変・契約011対象42件無変更全緑）が、試験コードの実体と整合しているか。和集合pin試験2本のliteral更新の整理（実装Evidence §5＝契約§5.1-5承認済み変更の帰結であり停止条件に該当しない）が妥当か。
3. **RED先行の完結性**：RED（21失敗・70合格）→最小実装→全緑の手続きが、実装Evidence §1〜3と測定ブロックの参照だけで第三者が追える形になっているか（数値の出所が機械生成fileに閉じているか）。
4. **読み取り専用性の抜け**：危険旗・書込み系値の不在（両向き試験）、認証遮断、stdin遮断、read-only sandbox、rollout読取り（repo外だがcodex自身の記録の読取りのみ）に、書込み・外部接続・権限昇格・API鍵混入の抜けが残っていないか。

## 4. 判定の形式

- headless起動時は、起動promptが指定するJSON schemaに完全に従う構造化出力だけで返す。`verdict`は5語彙（`verified`／`verified_with_findings`／`rejected`／`stale_target`／`unable`）、`blocking`は「採用・受入を止めるべき所見」の意味、実施できなかった検査は`unexamined`配列へ明示、`summary`は日本語で書く。
- 手動fallback時は同じ項目（判定・findings・未検査・要旨）を日本語の文章で返し、冒頭にmodel名を記載する。

## 5. 判断済み・範囲外（蒸し返し不要）

- 判断済み（蒸し返し不要）：契約015 v2の採用（利用者2026-08-20）。判定取得＝prompt指示＋JSON抽出のfallback確定（`--output-schema`はserver側strict検査で既存schema拒否＝RED実測Evidence）。model観測＝rollout方式への契約訂正（利用者承認「案1を承認する」）。許可model 2値と起動＝一覧先頭固定（承認record）。`IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`は(b)別作業単位。`gpt-5.6-terra`の起動選択機構は範囲外。
- 範囲外（「無い」という指摘は不要）：`tools/request_builder/`の変更・縦C合議・`tools/session_logs/`の変更・外部API後続・実E2E未了の指摘（本依頼への応答自体が§9-8の実E2Eである）。
- 事実の明示：本依頼recordは契約011の正式経路（assemble→記入→check合格）で組み立てられ、**codex-cli backendの実E2E対象**（契約015 §9-8）として別名slug（`-codex`）を持つ。完了レビューの正式判定は別途agy（Tier 1）で同一実装対象に対して行い、あなたの判定はそれと並ぶ判定役比較の材料にもなる。§7.5残余risk 6点の最終受容は利用者の製品受入判断事項（妥当性への懸念はfindingsで示してよい）。

## 6. 手順（Human・Claude向け）

1. 利用者が起動を明示指示する（起動は契約010 §2の承認境界に従う）。
2. Claudeが単体入口を実行する：

```text
reviewcompass3-reviewer-launch launch \
  --repository /Users/Daily/Development/ReviewCompass3 \
  --request records/session-handoffs/2026-08-20-codex-cli-backend-completion-codex-request-v1.md \
  --expected-sha256 <本record commit後のSHA-256> \
  --private-root <repo外私有領域の絶対パス> \
  --run-id <実行識別子>
```

3. アダプタが判定recordを`records/session-handoffs/2026-08-20-codex-cli-backend-completion-codex-verdict-v1.md`へ機械転記して単独commitし、事後照合4点を実行する。
4. `verified`系（blocking 0件）なら次のHuman判断へ進み、blocking所見があれば停止して利用者へ諮る。
