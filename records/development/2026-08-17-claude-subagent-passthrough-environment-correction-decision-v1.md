# 契約012 §7.2子環境の訂正（通過変数のUSER欠落）Human判断record v1

- 判断日：2026-08-17
- 状態：`adopted`
- 対象：採用中の契約012候補v2 §7.2「claude-subagentの起動固定形」の子環境（通過変数一覧）
  （`records/task-contract/2026-08-17-claude-subagent-backend-candidate-v2.md`。
  歴史的recordは書き換えず、本recordを訂正overlayとする。`--verbose`訂正record
  `records/development/2026-08-17-claude-subagent-verbose-argument-correction-decision-v1.md`と同列）
- 先行記録：契約012 subagent許可model承認record §4-2「操縦環境の認証」
  （`records/development/2026-08-17-subagent-allowed-models-approval-v1.md`）

## 1. 承認文言【記録】

> 訂正案1を承認する。訂正record→RED→実装→試験追随まで進めて

（2026-08-17 chat。Claudeが提示した訂正2案のうち、訂正案1「claude-subagentの通過一覧を実行器の
9変数と同値にし、同値性を試験で固定。agyの7変数は不変」の全文承認）

## 2. 事象と原因【実測】

1. 契約の子環境（通過7変数：`PATH, HOME, LANG, LC_ALL, LC_CTYPE, TERM, NO_COLOR`）では、
   claude CLIが保存済みログインを読めず「Not logged in」となる（model承認record §2.2。
   利用者端末の`env -i PATH HOME`実行でも同一再現、2026-08-17 chat貼り付け）。
2. 設計流用元の実行器`tools/development/claude_implementation_executor.py`の子環境一覧
   `ALLOWED_CHILD_ENVIRONMENT`は9変数（`HOME, USER, PATH, TMPDIR, LANG, LC_ALL, LC_CTYPE,
   TERM, NO_COLOR`）であり、Reviewer起動器の通過一覧（契約010のagy用7変数）には**`USER`と
   `TMPDIR`が欠けていた**。原因は流用時の一覧の取り違え（agy用一覧の共用）である。
3. 第4回実測（操縦環境から3条件。計測専用script・製品コード無変更。引数は
   `build_claude_arguments`＋`--verbose`訂正、親環境は`ANTHROPIC_BASE_URL`を外して環境検査を
   正規に通過）。scriptの出力の機械転記：

```json
[
  {
    "case": "executor9",
    "environment_keys": [
      "CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS",
      "CLAUDE_CODE_DISABLE_BACKGROUND_TASKS",
      "CLAUDE_CODE_DISABLE_CLAUDE_MDS",
      "CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS",
      "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC",
      "CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL",
      "CLAUDE_CODE_MAX_RETRIES",
      "DISABLE_AUTOUPDATER",
      "ENABLE_CLAUDEAI_MCP_SERVERS",
      "HOME",
      "LC_CTYPE",
      "PATH",
      "TMPDIR",
      "USER"
    ],
    "exit_code": 0,
    "models_observed": [
      "claude-opus-5"
    ],
    "first_text": "OK"
  },
  {
    "case": "launcher7+USER",
    "environment_keys": [
      "HOME",
      "LC_CTYPE",
      "PATH",
      "USER"
    ],
    "exit_code": 0,
    "models_observed": [
      "claude-opus-5"
    ],
    "first_text": "OK"
  },
  {
    "case": "launcher7+TMPDIR",
    "environment_keys": [
      "HOME",
      "LC_CTYPE",
      "PATH",
      "TMPDIR"
    ],
    "exit_code": 1,
    "models_observed": [
      "<synthetic>",
      "claude-opus-5"
    ],
    "first_text": "Not logged in · Please run /login"
  }
]
```

4. 結論：`USER`が保存済みログイン（keychain）読み出しの必要条件である。認証情報は操縦機に
   既存であり、これまでの「Not logged in」は全て`USER`欠落が原因（ログイン不在ではない）。
   `TMPDIR`単独は認証に寄与しないが、実行器の実証済み一覧の構成要素である。

## 3. 訂正内容【判断】

1. claude-subagent専用の通過一覧を、実行器`ALLOWED_CHILD_ENVIRONMENT`と**同値の直書き定数**
   `CLAUDE_PASSTHROUGH_ENVIRONMENT`（9変数・同順）として`tools/reviewer_launch/core.py`へ宣言する
   （由来：実行器。同値性は試験で固定。禁止6変数`CLAUDE_FORBIDDEN_AUTH_ENVIRONMENT`と同型）。
2. 子環境の組み立てをbackend別とする：agy＝従来の`PASSTHROUGH_ENVIRONMENT`（7変数・**不変**）、
   claude-subagent＝`CLAUDE_PASSTHROUGH_ENVIRONMENT`（9変数）。
3. 実行器が子へ注入する抑制変数（`CLAUDE_CODE_DISABLE_CLAUDE_MDS`等）は本訂正へ**含めない**
   （別途の改善候補として扱う）。
4. 契約v2本文は書き換えず、以後の契約参照はv2＋`--verbose`訂正record＋本recordとする。

## 4. 安全性評価【判断】

- `USER`は利用者名、`TMPDIR`は一時領域の場所を示す変数であり、認証秘密ではない。禁止6変数の
  遮断・「利用者のsubscriptionログインだけを使う」認証方針・読み取り専用性は全て不変。
- agy経路の子環境・値は一切変えない（既存試験の無変更緑で機械証明する）。
- 訂正後の子環境での認証成立・応答model `claude-opus-5`は§2-3実測（`launcher7+USER`・
  `executor9`）で確認済み。

## 5. 試験追随【判断】

- RED先行：(1) 同値性試験（`CLAUDE_PASSTHROUGH_ENVIRONMENT` ＝ 実行器
  `ALLOWED_CHILD_ENVIRONMENT`）、(2) 挙動試験（subagent起動の子環境へ`USER`・`TMPDIR`が通る）。
  (3) agy不変の固定試験（agy起動の子環境へ`USER`が通らない）は不変性の押さえとして追加する。
- 既存のagy経路試験は無変更で全緑を維持。対象suite（契約012・011・G30・layout）と正規全試験
  （禁止認証隔離条件）の緑を確認する。

## 6. 未実施

- 実E2E（起動場所は操縦環境＝案B。利用者の明示指示待ち）、§9-10完了レビュー、§9-11製品受入。
