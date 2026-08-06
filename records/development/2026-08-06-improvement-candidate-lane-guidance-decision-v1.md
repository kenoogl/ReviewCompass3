# 改善候補の登録経路をAGENTS.mdへ明記する 承認Decision v1

- Decision ID：`DEC-IMPROVEMENT-CANDIDATE-LANE-GUIDANCE-001`
- decision maker：Human
- decided at：`2026-08-06T10:26:43+09:00`
- decision：`approved`
- decision class：`operational_guidance_decision`

## 1. 経緯

2026-08-06、恒久検査器の要否をIssueのレーンへ載せるにあたり、新しく気づいた改善を1件登録する
素直な入口が既存形式に無いことが判明した。既存の`improvement_candidate`形式は
`source_identity.kind`が`observation`固定で`OBS-`始まりのIDを要求し、もう一方の形式は
過去TODO snapshotへ束縛されている。

Claudeは3案（既存形式に合わせる／過去TODO用形式に入れ物を足す／形式そのものを直す）を提示し、
Humanは既存形式に合わせる案を選んだ。理由は「どの方法を選んでも証跡を作る必要があるので、
観測recordを1件作る手間は無駄ではない」である。

その後Humanは、この運用方針はClaudeのmemoryではCodexから参照できないため、
repositoryへ書くべきだと指摘し、`AGENTS.md`への追記を承認した。

## 2. 追記内容

`AGENTS.md`の「開発方針」節へ次の1項目を追加した。既存項目の削除と書換えはしていない。

> 改善候補の登録は既存経路で行う。まず`OBS-`始まりの観測recordを作り、それを`source_identity`へ
> 束縛した`IC-`始まりの候補を`.reviewcompass/workflow/improvement-candidates/`へ置く。
> `python3 -m tools.development.issue_resolution_pilot --config config/development-issue-resolution-pilot-v3.json record <path>`
> で検証してからHumanの仕分け判断を仰ぐ。候補記録の形式そのものの作り直しを先に提案しない。

既存の改善候補規定（`improvement_candidate`として記録し分類・停止判定・routeを行う、
Issue昇格はHumanが判断する）は変更していない。本追記は、その経路の具体的な入口と
検証commandを明示するものである。

## 3. 範囲

- 追記は`AGENTS.md`1 fileのみ。Development Policy、Current Plan、checklist、Contract、
  Requirement、実装、Testは変更していない。
- 候補記録の形式そのもの、validator、config、schemaは変更していない。
- Issue昇格の権限境界は変更していない。引き続きHumanが判断する。

## 4. 残る不便さ

「今日新しく気づいた改善を1件登録する」ための直接の入口は無いままである。形式を満たすために
観測recordを先に1件作る必要がある。Humanは、どの方法でも証跡は要るためこの運用で差し支えないと
判断した。形式そのものの改定が必要になった場合は、別途RED先行とHuman承認を要する。

## 5. 検証

| 項目 | 結果 |
| --- | --- |
| `AGENTS.md`のSHA-256（追記後） | `330b6f9f21dfa618bbb9d06a10eb25078d69da9ba0e691dd4ad0c75c7458e933` |
| 入口Test `tests/test_todo_handoff_prompt_entrypoints.py` | `3 passed` |
| 公式全Test | `1017 passed`（failed 0、errors 0、Python 3.9.6、pytest 8.4.2、fallback `false`） |
| `git diff --check` | 合格 |

本追記の実例が`IC-AUTHORITY-REFERENCE-DIGEST-CHECK-001`
（`.reviewcompass/workflow/improvement-candidates/ic-authority-reference-digest-check-001--v1.json`）と
その観測record`records/development/2026-08-06-authority-reference-digest-drift-observation-v1.json`で
あり、commit `235a7d3`に含まれている。

## 6. 既存recordへの影響

new-onlyで作成した。既存recordの上書き、削除、無効化、stale化はしていない。
