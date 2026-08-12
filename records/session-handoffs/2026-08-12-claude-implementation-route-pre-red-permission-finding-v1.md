# Claude実装委譲経路 RED前権限調査所見 v1

- 日付：2026-08-12
- 状態：`human_decision_required`
- 対象範囲SHA-256：`9881f7df526c3aef8c21e665f75927329608d1b0518e343db0ac5c89f954a024`
- 対象要求：`AC-CD-005`、`NG-CD-003`、`ST-CD-003`
- 確認したClaude Code：`2.1.220`
- 外部実行：なし

## 1. 事象

範囲固定v2は、Claudeへ`Bash`を見せ、固定した完全一致の試験commandだけを事前許可し、未列挙commandを
自動拒否する。同時にhookをすべて無効にする。

Claude Code 2.1.220の標準権限だけでは、この組合せを満たせない。読取専用と判定されたBash commandは
すべての権限方式で承認なしに実行される。`Bash`全体のdenyまたはask規則は、個別のallow規則より先に
評価されるため、固定試験commandだけを例外許可できない。

## 2. Evidence

- `claude --version`：終了0、`2.1.220 (Claude Code)`
- `claude --help`：終了0。`--tools`、`--allowedTools`、`--disallowedTools`、`--permission-mode dontAsk`、
  `--safe-mode`、`--settings`の存在を確認した。
- Claude Code公式権限仕様：読取専用Bash commandは全権限方式で承認なしに実行される。
  <https://code.claude.com/docs/en/permissions>
- 同仕様：権限規則はdeny、ask、allowの順で評価され、広いdenyへ狭いallowの例外を作れない。
- Claude Code公式隔離仕様：Bashのfile・network境界はOSで強制できるが、許可commandを完全一致1件へ
  狭める機能ではない。<https://code.claude.com/docs/en/sandboxing>

Claude process、認証確認、payload送信、repository内容の外部送信は行っていない。

## 3. 影響

範囲固定v2のまま試験を書くと、実装不能な受入条件か、実際には未列挙commandを通す偽の合格のどちらかに
なる。安全境界と受入条件へ影響するため、RED試験作成前に停止する。

## 4. 選択肢

1. 推奨：Claudeから`Bash`を外す。Claudeは`Read`、`Glob`、`Grep`、`Edit`、`Write`だけを使い、固定試験
   commandはClaudeの外にある機械処理が各ターン後に実行する。最も単純で、決定的処理を機械へ任せる
   開発方針にも合う。
2. Claudeへ`Bash`を残し、信頼済みの固定`PreToolUse` hookだけを例外的に許可して、完全一致command以外を
   実行前拒否する。境界は強いが、hook配布と検証が増える。
3. worktree内の読取専用Bash commandを許容し、変更・network・結果を事後検査する。単純だが、
   「未列挙commandを自動拒否する」という現行要求を弱める。

Humanが選択するまで範囲固定、RED指示、受入試験を変更しない。
