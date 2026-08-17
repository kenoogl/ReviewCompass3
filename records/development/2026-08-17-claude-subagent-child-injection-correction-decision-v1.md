# 契約012 §7.2子環境の訂正（実行器の抑制注入変数の流用）Human判断record v1

- 判断日：2026-08-17
- 状態：`adopted`
- 対象：採用中の契約012候補v2 §7.2「claude-subagentの起動固定形」の子環境（注入変数）
  （`records/task-contract/2026-08-17-claude-subagent-backend-candidate-v2.md`。
  歴史的recordは書き換えず、本recordを訂正overlayとする。`--verbose`・通過変数の訂正record 2件と同列）
- 由来の改善候補：`IC-SUBAGENT-HARDENING-ENV-REUSE-001`
  （観測record `records/development/2026-08-17-subagent-hardening-env-omission-observation-v1.json`。
  本判断はそのHuman仕分け＝採用である）

## 1. 承認文言【記録】

> 実行器が子へ注入している抑制変数（CLAUDE.md読込み禁止など。レビューの独立性に有益）の流用に対応

（2026-08-17 chat。Claudeが改善候補として登録・報告した「実行器の抑制注入変数9種のsubagent流用」の
採用指示）

## 2. 根拠【実測・記録済み】

1. 実害：抑止なしの実起動中にclaude本体が自己更新（2.1.220→2.1.224）し、外部送信経路の本体同一性
   pinを破って試験24件を失敗させた（pin更新record・観測record）。実行器は`DISABLE_AUTOUPDATER=1`を
   注入しており、この経路では発生しない設計だった。
2. 独立性：抑止なしのprobe起動のinitはproject memoryのpath（CLAUDE.md等の読込み文脈）を含んでいた
   （model承認record §2.3のstream転記）。`CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`は操縦側指示のReviewer
   文脈への混入を防ぐ。
3. 動作実証：実行器と同一の子環境（通過9変数＋注入9種）での実起動は認証成立・応答model
   `claude-opus-5`・終了コード0を実測済み（通過変数訂正record §2-3の`executor9`条件）。

## 3. 訂正内容【判断】

1. claude-subagentの子環境へ、実行器`_child_environment`が注入する抑制変数9種と**同値の直書き定数**
   `CLAUDE_CHILD_ENVIRONMENT_INJECTIONS`を追加する（由来：実行器。同値性は試験で固定。変更は契約改定）：
   `CLAUDE_CODE_MAX_RETRIES=0`・`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`・
   `CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL=1`・`CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS=1`・
   `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1`・`CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`・
   `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1`・`ENABLE_CLAUDEAI_MCP_SERVERS=false`・`DISABLE_AUTOUPDATER=1`
2. 注入はclaude-subagentの起動だけに適用し、**agyの子環境は不変**（注入なし。既存試験の無変更緑と
   不変固定試験で機械証明）。
3. 契約v2本文は書き換えず、以後の契約参照はv2＋訂正record3件とする。

## 4. 安全性評価【判断】

- 9種はいずれも機能の**抑止**（自動更新・余分な通信・市場自動導入・組み込みagent・背景処理・
  CLAUDE.md読込み・Git指示・claude.ai MCP・自動再試行）であり、権限拡大・認証・書込みに一切
  作用しない。読み取り専用性・認証遮断・通過変数は不変。
- `CLAUDE_CODE_MAX_RETRIES=0`は契約の「自動再試行をしない」原則と整合する。
- 実行器で実運用済みの組であり、同一組での実起動成立を実測済み（§2-3）。

## 5. 試験追随【判断】

- RED先行：(1) 同値性試験（定数＝実行器`_child_environment`の注入。通過変数を全て消した状態で
  実行器関数を呼び、注入だけを取り出して比較）、(2) 挙動試験（subagent起動の子環境に注入9種が
  値どおり入る）。(3) agy不変の固定試験（agy起動の子環境に注入キーが無い）は不変性の押さえとして追加。
- 既存agy試験は無変更で全緑を維持。対象suiteと正規全試験（禁止認証隔離条件）の緑を確認する。

## 6. 未実施

- 実E2E（利用者の明示指示待ち）、§9-10完了レビュー、§9-11製品受入。
