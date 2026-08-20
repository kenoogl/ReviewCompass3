# 契約015 codex E2E判定（rejected）の所見是正Evidence v1

- 実施日：2026-08-20
- 担当：Claude
- 出所：codex実E2Eの判定record
  `records/session-handoffs/2026-08-20-codex-cli-backend-completion-codex-verdict-v1.md`
  （`rejected`・blocking 2件＋非blocking 1件。E2Eの機械経路——完走・raw保存・転記・事後照合4点——
  自体は合格しており、所見はすべて**証拠品質**への指摘。設計・schema・契約の変更を要しない
  是正として本線内で処理した）
- 実測の正本：測定ブロック
  `records/development/2026-08-20-contract-015-green-measurements-v2.md`（宣言
  `records/development/2026-08-20-contract-015-green-commands-v2.json`。12項目・二重実行一致・
  非決定0件）

## 1. C15-REVIEW-001（blocking）→ 是正済み

指摘：GREEN合否の終了コード射影が`pytest ...; echo exit=$?`の`;`連結で、AGENTSの規律
「合否は単独で実行したcommandの終了コード」に反する。

是正：測定ブロックv2で、4 suiteを`sh -c 'exec .venv/bin/python3 -m pytest <suite> ...'`
（`exec`置換・連結なし・出力遮断）として実行し、**測定entry自身のexit＝pytest自身の終了コード**
として機械記録した。4 suiteともexit 0（v2の先頭4節）。v1測定
（`...-green-measurements-v1.md`）の終了コード射影4節はstaleとし、合否根拠に使わない
（収集件数・分岐固定点・golden・digest各節の値はv2で再取得済み）。

## 2. C15-REVIEW-002（blocking）→ 是正済み

指摘：REDの「21 failed, 70 passed」が例外転記のみで、第三者が機械再照合できない。

是正：**git履歴だけから再現可能なRED再現**を実行し、生出力を
`records/development/2026-08-20-contract-015-red-replay-output.txt`へ固定した（digestは
測定ブロックv2末尾節）。再現手順（第三者はこの3 commandで同一結果を機械再現できる）：

```text
git worktree add <一時dir> 7c46708
git -C <一時dir> checkout e64c0e5 -- tests/test_reviewer_launch.py
（<一時dir>で）.venv/bin/python3 -m pytest tests/test_reviewer_launch.py -q --tb=no -p no:cacheprovider
```

結果：**単独pytest終了コード1・`25 failed, 69 passed`**（現行試験94本を実装前commit
`7c46708`のcoreへ適用。25件の失敗＝契約015の新規挙動全件が実装前に失敗することの機械証明。
当初転記の21件との差は、その後の試験是正——遮断試験の4変数網羅化＋和集合pin——による）。

## 3. C15-REVIEW-003（非blocking）→ 是正済み

指摘：openai系4種の遮断試験がOPENAI_API_KEY 1変数のみ。

是正：`test_codex_forbidden_auth_environment_stops`を`@pytest.mark.parametrize`で
4変数（OPENAI_API_KEY・OPENAI_BASE_URL・OPENAI_ORGANIZATION・OPENAI_PROJECT）の網羅へ拡張
（commit `e64c0e5`）。収集件数は91→94（測定ブロックv2）。

## 4. あわせて固定した受入材料【実測＝測定ブロックv2参照】

- 正規全試験：公式runner単独実行で`status: passed`・exit 0。receipt＝
  `records/development/2026-08-20-contract-015-full-test-receipt-v1.json`（test_summary：
  total 2,645・failed 0。digestはv2末尾節）。
- 契約§6保護対象の基準commit（`91e0dcd`）からの差分file一覧：**空（0件）**。
- E2E rawの領域外読取り点検（§7.5-6・§9-8）：command_execution全21件を機械走査し、
  repo外への読取り0件（repo絶対path非含有3件はcwd＝対象repository内での読み取り専用git照会：
  `git status`・`rev-parse`・`cat-file`・`diff --stat`・`show --stat`）。再現：raw
  （`~/.reviewcompass3-private/reviewer-launch/contract-015-e2e-codex/reviewer.raw.json`の
  `raw_response`欄）の`item.started`かつ`item.type==command_execution`を全件列挙。
- 生成promptのgolden digest：是正後も基準値と一致（byte不変の維持）。

## 5. 未実施

- 完了レビュー（agy・Tier 1）の起動と判定。製品受入（Human）。codexによる再レビュー
  （実施の要否はHuman判断。E2Eの機械経路実証は初回で完了済み）。
