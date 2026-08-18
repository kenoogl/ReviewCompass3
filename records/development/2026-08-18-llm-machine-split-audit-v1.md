# LLMと機械の分担固定の徹底度 精査record v1（prompts手順書8件）

- 精査日：2026-08-18
- 指示者：利用者（Human）。文言「LLMと機械の分担の固定が徹底されているかを精査」→「精査結果を
  recordに固定し、対策1（既定値化の横展開）に着手してください」（2026-08-18 chat）
- 記録者：Claude
- 対象：`docs/development/prompts/`配下の全8手順書（機械計数8件・全文精読）
- 判定基準：AGENTS §3（LLMは文章操作と意味分析に限定）・数値の記録規律（scope-prescan-run.md）・
  機械化優先の原則（AGENTS §3・2026-08-18追記）

## 1. 結論

原則の明文化と「誤転記なら機械が止める」fail-closed束縛の一層目は広く徹底されている。残る手作業は
**「コマンド引数の手組み立て」類型**に集中しており（3手順書）、計画JSONのdigest埋め込みは道具が
無くLLMの手書きscript実行が発生している（2026-08-18に実例2回）。

## 2. file別所見

| 手順書 | 徹底されている点 | 残る手作業（穴） |
| --- | --- | --- |
| session-log-record-run | 模範。1コマンド固定・値はコード内固定・合否は単独終了コード・「件数を手書きしない」「LLMは分離判定をしない」明文 | 要約JSONのchat転記（人向け表示のみ・低risk） |
| review-plan-run | 模範。「LLMではなく入口で生成」明文・対象pathはGit差分から・追加指定入口なし・plan_sha256束縛 | `--base-commit`／`--target-commit`のSHA手書き転記 |
| pilot-collaboration-run | 「引数や承認票を手で組み立ててはならない」明文・一括入口が保存済み準備結果から全引数を読む | prepare等の初回引数に絶対パス手組み（一括入口で大半吸収済み） |
| scope-prescan-run | 測定ブロック原則・検索`--plan`のみ・時刻機械（2026-08-18改定） | 作業別計画JSONの`content_digest`埋め込みに専用道具が無い（heredoc手書き実行の実例2回） |
| request-builder-run | 機械欄生成・7項目機械検査・SHA束縛 | `--date`の日付手書き・`--repository`の絶対パス手組み・sha256の次コマンドへの手転記（誤りは停止する） |
| reviewer-launch-run | 事後照合4点機械・tier照合の機械停止 | 引数5つ全部が手組み立て。特に`--private-root`は検索CLIで解消済みの正準path手組みの同型が残存。run-id命名も手作業 |
| claude-bootstrap-run | 用途限定・承認束縛 | `--manifest-digest`のdigest手渡し（小） |
| todo-handoff-update | 検証は単一入口機械（上限・Digest一致・Git欄） | TODO本文の生成自体がLLM手組み（projection導出側未実装の既知の暫定。根治は運用実測後と裁定済み） |

## 3. 横断所見

1. **一層目（間違えても通らない）は完成**：SHA不一致停止・todo_handoff照合・tier照合が誤転記を
   止める。
2. **二層目（間違える行為自体を消す）が途上**：(a) 日付・commit SHA・run-idの手書き、(b) 正準path
   （private-root）の手組み＝検索CLIで解消済みの型の横展開未了、(c) 計画・分類JSONのdigest埋め込み
   writer不在。
3. `--expected-sha256`（reviewer-launch）の手渡しは**意図された束縛**（操作者が起動対象を明示確認
   する承認境界の一部）であり、手作業債務に数えない。

## 4. 対策候補（優先順・Human裁定済み＝1に着手）

1. **既定値化の横展開**（着手指示済み）：reviewer-launchの`--private-root`既定値・run-id自動採番、
   request-builderの`--date`機械記録・`--repository`既定値。
2. 計画JSON writer（digest埋め込みつき生成入口。heredoc手書きの排除）。
3. review-planのcommit引数のGit既定取得（要設計）。

## 5. 未実施

- 対策1の作業単位（事前走査から。本recordと同日）。対策2・3（登録のみ・着手はHuman指示ごと）。
