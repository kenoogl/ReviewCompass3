# 縦B事前走査 追補（Gemini CLI提供終了とAntigravity CLI実測） v1

- 記録日：2026-08-16
- 指示者：利用者（Human）。承認文言：「追補recordを作成し、統合検討recordもagyへ訂正して。契約候補v1は
  第1 backend＝agyで作成に進んで」（2026-08-16 chat）
- 記録者：Claude
- 種別：事前走査v1への追補。v1 §1の外部CLI実測の更新と、§7論点1・3の差し替え
- 追補対象：`records/development/2026-08-16-vertical-b-reviewer-launch-adapter-prescan-v1.md`
  （SHA-256 `736b9d58227cdb8b66f41abe9b6b0ab1b54515f415e5ccb69170c97bab7cb33a`、commit `272f6cc`）

## 1. 利用者提供の事実【記録】

利用者は2026-08-16のchatで次の事実を提供した。

> 以前提供されていた Gemini CLI は2026年6月18日をもって提供を終了し、現在は後継となる
> Antigravity CLI (agy) へ移行しています。

Claudeの知識は2026年1月時点までであり、この提供終了は利用者提供の事実として扱う。

## 2. Antigravity CLI（agy）の実測【実測】

確認は版数と説明文の表示だけで行い、promptの送信（外部送信・課金を伴う操作）は行っていない。

- 所在：`command -v agy` → `/Users/keno/.local/bin/agy`（present。`antigravity`名はMISSING）
- 版数：`agy --version` → `1.1.13`
- headless（非対話起動）関連の旗（`agy --help`の出力から該当行を転記）：

```text
--print / -p / --prompt          Run a single prompt non-interactively and print the response
--output-format                  Output format for print mode (text, json, stream-json) (default text)
--json-schema                    Optional JSON schema string or path to a schema file to enforce structured output (for stream-json, only applicable to the final result)
--model                          Model for the current CLI session
--effort                         Reasoning effort for the current CLI session (low|medium|high)
--mode                           Set the agent execution mode for this session (accept-edits, plan)
--sandbox                        Run in a sandbox with terminal restrictions enabled
--add-dir                        Add a directory to the workspace (repeatable)
--print-timeout                  Timeout for print mode wait (default 5m0s)
--disable-slash-commands         Disable slash command and skill expansion in print mode
--dangerously-skip-permissions   Auto-approve all tool permission requests without prompting
```

- 含意：print方式・stream-json・model指定・slash無効化という構成は、実行器
  （`tools/development/claude_implementation_executor.py`）のclaude CLI起動設計と同型であり、
  起動引数の組み立て・出力解析の設計をほぼそのまま写せる。`--json-schema`により判定の構造化出力を
  CLI側で強制できる（claude CLIの起動設計に無い追加能力）。

## 3. 事前走査v1への影響

| v1の記載 | 追補後 |
| --- | --- |
| §1 外部CLI表「gemini: MISSING」 | 当時の走査として事実どおり維持。後継`agy`はpresent（本record §2） |
| §7 論点1「gemini-cli backendは導入＋headless仕様実測が前提」 | **解消**。後継CLIは導入済みで、headless旗一覧も実測済み。残るのは§4の未確認事項だけ |
| §7 論点3「第1 backend＝claude-subagent推奨」 | **差し替え**。第1 backend＝`antigravity-cli`（agy）。理由：(1) 別プロバイダによるTier 1独立性で現行の手動Gemini体制を運搬0回へ機械化できる、(2) 暫定体制のReviewer（Gemini）と判定の連続性を保てる、(3) headless仕様が実行器設計と同型で実装が容易 |
| §7 論点2・4・5・6 | 不変 |

統合検討record（`records/development/2026-08-16-review-tooling-formalization-study-v1.md`）の
backend名`gemini-cli`は、利用者承認（冒頭の承認文言）により`antigravity-cli`（agy）へ本commitで訂正する。

## 4. 未確認事項（契約内の承認付き実測へ送る）【記録】

- 認証状態（利用者アカウントでのheadless実行可否）と課金・利用枠。
- 実headless挙動：読み取り専用相当でのrepository読取り可否、`--json-schema`の実挙動、
  終了コード仕様、`--sandbox`・`--mode`の実効果。
- 利用可能なmodel名の一覧（`agy models`は認証を伴う可能性があるため本走査では実行していない）。

これらは外部起動（実質の外部送信）を要するため、契約010の受入条件内で利用者承認の下に実測する。

## 5. 利用者決定の固定【記録】

冒頭の承認文言により次が確定した。

1. 第1 backend＝`antigravity-cli`（agy）。
2. claude-subagent backendは第2縦切りへ送る（Tier 2／3の宣言・Human受容の型はそこで作る）。
3. 契約候補v1（`TC-RC3-PRODUCT-REVIEWER-LAUNCH-ADAPTER-010`）の作成へ進む。
