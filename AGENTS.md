# AGENTS.md

## 作業進行

- 利用者から指示を受けたら、作業開始前に指示を自分の理解で復唱する。
- 作業開始前に、具体的な作業項目を適切な粒度で示す。
- 当面の開発作業は`docs/development/2026-08-03-initial-development-checklist.md`を開始入口とし、
  authority文書との一致を確認して、未完了の先頭工程から進める。
- checklistのcheckboxだけを完了根拠にせず、各節の固定Evidenceを確認する。
- `TODO_NEXT_SESSION.md`の読取、作成、更新、検証は、唯一の共通手順`docs/development/prompts/todo-handoff-update.md`に従う。
- 作業後に、実施内容と確認結果を報告する。
- 「実施した」という報告だけを完了根拠にしない。実施、結果、判断、提案、未実施を分け、
  実施・結果・判断にはpath、diff、Digest、command結果、commit SHA、receiptまたはDecisionを対応付ける。
- Evidenceがない報告は`reported_unverified`として未完了にし、報告と事後状態が違う場合は
  `report_execution_mismatch`として完了判断を停止し、影響を受ける表示と判断をstaleにする。
- Claude、Codexサブエージェント、人またはscriptへ委譲した作業のレビューは、
  `docs/development/work-review-protocol.md`を共通入口として実行者に依存しない順序で確認する。
- 問題がある場合は、起きている事象とその原因を平易に説明する。
- LLMは文章操作と意味分析に限定し、決定的な変換、抽出、集計、照合、file操作、Test、Git確認、
  command実行は機械処理を使用する。機械処理が未整備なら手作業で常態化させず改善候補へrouteする。
- 手戻りが発生した場合は、手作業箇所との因果を確認する。手作業が原因または原因候補なら、作業後報告に
  対象操作、期待executor、実executor、手作業理由、手戻り事象とEvidence、機械処理候補、routeを含める。

## 開発方針

- SDDと小さなE2E縦切りを基本単位とする。
- 振る舞いを変更する場合、実装前または同一変更内で関連テストを用意し、
  変更がなければ失敗することを確認する。
- 赤テストだけのコミットは必須にしない。統合対象のコミットは原則として緑にする。
- 要求の誤解または設計変更が判明した場合は、理由を記録してテストを修正できる。
- 変異検査、実データ検証、独立レビューは高リスク境界に適用する。
- validatorまたは入力前提を変更した場合は旧合格をstaleとし、risk別の正例・負例・境界例と
  必要な独立oracleを再実行する。
- 成果物を書き換えた場合は、再読込、関連validator、参照整合、stale閉包を確認する。
- 文書、試作、調査には形式的な赤緑サイクルを強制しない。
- Pythonは4スペースとし、その他の言語は標準フォーマッターに従う。
  既存ファイルは機能変更と無関係な一括整形をせず、変更時に段階的に合わせる。
- Human承認は、方針変更、外部送信、不可逆操作、意味的裁定、段完了に要求する。
- 自己適用にはstableと判定された機能だけを使用する。
- 自己適用中に問題、改善案、新機能案を見つけた場合、現行Plan、Task Contract、Testまたは
  受入基準を先に書き換えず、発生元Work、固定source、Evidenceを持つ改善候補
  （`improvement_candidate`）として記録し、分類、停止判定、routeを行う。
- safety、authority、Acceptanceの真偽、必須Provenance、source／Test／Verdict identity、不可逆または
  外部side effectへ影響する候補では現行Workを停止する。それ以外はcheckpointで扱う。
- AIまたは機械の分類とrouteは提案として扱い、上流改定、Issue昇格、risk受容、再開はHumanが判断する。
  採用候補はconsumerとOutcomeへ接続されるまでclosedにしない。
- 詳細は`docs/development/2026-08-02-development-policy.md`を正本とする。

## コミット方針

通常の開発作業のコミットは、次の最小条件をすべて満たす場合、コミットごとの利用者の明示指示なしに
行ってよい。正本は`records/development/2026-08-05-semantic-commit-minimal-guards-decision-v1.md`
（`DEC-SEMANTIC-COMMIT-MINIMAL-GUARDS-001`）とする。

- 一つの目的と確認結果を独立して説明できる、意味的に完結した作業単位である。
  ファイル数だけを基準に分割せず、途中状態が不整合またはテスト失敗になる分割はしない。
- stage対象は、明示したrepository-relative pathの列挙だけである。`git add -A`、`git add .`、
  範囲外ファイルの一括追加を使わない。
- `git diff --check`と、変更に応じたtest／validatorを実行して合格している。引き継ぎ文書を含める場合は、
  上記の共通手順が定める検査にも合格している。
- コミット後はread-onlyで状態を照合し、完了済み作業単位を未コミットのまま次の作業へ渡さない。
  自己SHAまたはremote状態の転記だけを目的とする追加コミットを作らない。

次は引き続き利用者の明示承認を必要とし、通常コミットの自律化に含めない。

- 方針変更、段完了、意味的裁定、不可逆操作、外部送信
- push、tag、amend、rebase、reset、force push、履歴書換え
- sandboxまたはhostの権限の迂回

その他の運用は従来どおりとする。

- 完了した作業単位を未コミットのまま次の作業単位へ進めない。作業単位の完了時と、利用者から
  「次へ」相当の指示を受けた時は、
  `python3 tools/development/work_unit_transition.py --work-status completed`を実行する。
- preflightが`completed_work_unit_uncommitted`を返した場合は、上の最小条件を満たす意味単位コミットを
  行い、transitionを再実行する。条件を満たせないときだけ停止して利用者へ報告する。
  作業中のdirty差分だけではこの状態に分類しない。
- 利用者が一括コミットまたは分割方法を指定した場合は、その指定を優先する。
- 最終コミット前のhandoff更新と検査も、上記の共通手順に従う。
- guarded commit、hook、コミットごとの恒久的な承認ファイル、巨大なcommit manifestは導入しない。
- `stage_completion`など、既存のHuman承認境界は緩めない。これらは通常のGit commitを意味しない。
