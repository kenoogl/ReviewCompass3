# claude本体2.1.224のpin更新 Human判断record v1

- 判断日：2026-08-17
- 状態：`adopted`
- 対象：外部送信経路部品`tools/development/claude_bootstrap.py`の本体同一性固定値
  （`_VERSION`・`_EXECUTABLE_SHA256`）と、その試験用合成fixture
- 関連：契約012 subagent許可model承認record・同§7.2訂正record2件（`--verbose`・通過変数）

## 1. 承認文言【記録】

> claude本体2.1.224のpin更新を承認する。更新record→定数更新→全試験→3 commit（訂正→pin→TODO）
> まで進めて。あわせて抑制変数流用を改善候補として登録して

（2026-08-17 chat。Claudeの推奨提示の全文承認。改善候補登録は別record
`2026-08-17-subagent-hardening-env-omission-observation-v1.json`で履行）

## 2. 事象【実測】

1. 契約012の通過変数訂正の試験追随中、正規全試験で`tests/test_claude_bootstrap.py`21件・
   `tests/test_claude_bootstrap_adversarial.py`3件の計24件が`claude_binary_mismatch`で失敗した。
2. 原因はclaude本体の自動更新である。本日早朝の実測streamは
   `"claude_code_version":"2.1.220"`（model承認record §2.3）だったが、現在は次のとおり
   （commandの出力の機械転記）：

```text
% which claude
/Users/keno/.local/bin/claude
% readlink -f "$(which claude)"
/Users/keno/.local/share/claude/versions/2.1.224
% shasum -a 256 "$(readlink -f "$(which claude)")"
391df9d2ab04e4cf32199335720ac7715a582e91eaecfd4d2198a16f57ea59b3  /Users/keno/.local/share/claude/versions/2.1.224
% claude --version
2.1.224 (Claude Code)
```

3. 独立性の機械証明：契約012訂正の変更2 file（`tools/reviewer_launch/core.py`・
   `tests/test_reviewer_launch.py`）を`git stash`で一時退避して同一試験を実行しても同一失敗が
   再現した（退避後に復元済み）。失敗原因は本体更新のみである。
4. 更新の契機：本日の実測・確認でclaude CLIを実起動した条件の一部に自動更新の抑止変数
   （`DISABLE_AUTOUPDATER=1`。実行器は子環境へ注入する）が無く、その間に本体が自己更新された
   と見られる。再発防止は改善候補`IC-SUBAGENT-HARDENING-ENV-REUSE-001`として登録する（別record）。

## 3. 更新内容【判断】

1. `tools/development/claude_bootstrap.py`：`_VERSION = "2.1.224"`、
   `_EXECUTABLE_SHA256 = "391df9d2ab04e4cf32199335720ac7715a582e91eaecfd4d2198a16f57ea59b3"`
   （§2-2の実測値の機械転記）。
2. 試験用合成fixtureの連動（値のみ。歴史的recordではない）：
   `tests/fixtures/claude_bootstrap/helpers.py`（偽装`--version`出力）・
   `tests/fixtures/claude_bootstrap/contract-v1.json`・
   `tests/fixtures/claude_bootstrap/result-schema-provenance-v1.json`（各版・digest値）。
3. **触らないもの**：`tools/development/claude_implementation_confirmation.py`の
   `CLAUDE_VERSION`（実装経路自身のpin。契約012 §6保護対象の実行器4 fileの一つで、当該試験は
   本件で無傷。次回その経路を使う際に、その経路自身の手続きで更新する）。

## 4. 安全性評価【判断】

- 本pinは「信頼するclaude本体」の受入を意味する供給元同一性のanchorである。受入根拠：
  従前信頼していた2.1.220と同一の導入経路（公式自動更新channel）・同一設置場所での更新版であり、
  digestは設置実体から機械計測した（§2-2）。
- 残余：2.1.224でのCLI挙動差（`--verbose`要件・stream内model表記）は未再測。実E2Eは
  `launch_failed`・`response_model_not_allowed`・`verdict_schema_nonconforming`等の停止条件で
  保護されるため、挙動差があれば安全側で停止し実表記を持ち帰る。

## 5. 試験【実測】

- bootstrap 2 suite：41件全緑。
- 正規全試験（禁止認証隔離条件）：2,461件成功・終了コード0（契約012の通過変数訂正を含む状態）。
- `git diff --check`合格。

## 6. 未実施

- 実E2E（利用者の明示指示待ち）、§9-10完了レビュー、§9-11製品受入、改善候補のHuman仕分け。
