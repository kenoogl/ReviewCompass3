# Codex → Claude：Work 4 最初のReview Task Contract設計提案

## 実行者・目的

**実行者はClaudeである。** Claudeは本ファイルを読み、Work 4の最初の設計提案を作成する。
Humanは2026-08-05にWork 4を進めるよう指示した。ただし、この指示は**設計提案の作成だけ**を
承認するものであり、製品実装、Decision Record、Requirement改訂、Task Contractの発行を承認しない。

目的は、Work 5Aで実装する最小Review Task Contractを、Humanが承認・不承認を判断できる粒度へ
具体化することである。対象はCurrent Plan §13で固定されている「ReviewCompass3自身の小さな文書変更を
対象とするReview Task Contract」とし、代表scenarioは`new_development / fresh`だけに限定する。

## 必ず読む正本

- `docs/current/reviewcompass3-plan-current.md` のWork 4、Work 4B、Work 5A、Work 6A、§13、§17
- `docs/development/2026-08-03-initial-development-checklist.md` のWork 4とWork 5A
- `records/requirements/authority/rc3-requirements-authority-2026-08-03--v2.json`と、そこから必要な
  Requirement definition
- `docs/design/2026-08-02-task-contract-design-amendment.md`
- `docs/development/2026-08-02-development-policy.md`
- `records/development/2026-08-05-work-4a-early-completion-and-4b-decision-v1.md`

既存のbootstrap実装、既存Test、commit履歴も読み、同じschema・validator・runtimeを重複設計しない。
Requirementsまたは既存正本の間に設計上の矛盾を見つけた場合だけ停止し、矛盾と根拠pathを完了報告へ
記録する。細かな記法や文書構成の判断では停止しない。

## 作成物

次の一ファイルを新規作成する。

`docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md`

状態は`awaiting_human_approval`とする。この文書はDecision Recordではない。少なくとも次を含める。

1. 対象scenario、利用者、入力、出力、非目標
2. 最小Review Task Contractのidentity、責務、境界、precondition、context obligation、allowed capability、
   expected output、acceptance、provenance、escalation
3. `Requirement → Contract → Plan bundle → Context Manifest → deterministic stub reviewer →
   Conformance → Final Challenge → Human decision → Provenance verdict → accepted artifact`の
   各record、owner、順序、許可／停止条件
4. `new_development / fresh`の正常経路と、欠落Requirement、Context不足、Conformance不合格、
   Challenge不合格、Human不承認、source変更によるstaleの負例・復旧経路
5. Work 5Aで初めて実装する最小componentと、Work 6A以降へdeferするcomponentの境界
6. Work 4AのReuse Discoveryを参照する境界、およびWork 4Bへ送る「routineを新設・変更する場合の
   再利用検索」の境界。今回のReview Contractは文書変更だけなので、Entry・Relation・Baselineを
   作らず、台帳を実装しない。
7. Requirement IDからContract obligation、受入testまでの対応表。根拠のない新Requirementを作らない。
8. Work 5A用の受入条件案。正常例、負例、境界例を分け、実装前にREDで固定できる形にする。
9. 未決のHuman判断を、実装上の細部ではなく意味・authority・scopeの判断だけに絞って列挙する。

大きな汎用framework、複数Contract type、LLMによる実レビュー、外部送信、CI起動、UI、
delegated AI、実装用Task Contract、Work 4Bの台帳・統合リファクタリングを提案のscopeへ入れない。

## TODO・コミット・検証

- `TODO_NEXT_SESSION.md`を「Work 4設計提案のHuman承認待ち」へ更新する。Current Planやchecklistは
  承認前に変更しない。
- TODO内の新規参照Digestを実ファイルから再計算する。
- `tools/development/todo_handoff.py TODO_NEXT_SESSION.md`、TODO reference Digest検査、
  `git diff --check`、公式venv runnerの全testを実行する。
- proposalとTODOだけを一つのGREENコミットにする。既存の未コミットファイルを混ぜない。

## 禁止事項と停止点

- 製品code、test、schema、policy、Requirement、Decision Record、Task Contract、外部DATA_ROOTを変更・作成しない。
- LLM呼出、レビュー実行、Human判断の代行をしない。
- Work 4Aの完了Evidence、Work 4Bの後続範囲、既存Requirementを弱めない。
- 設計正本同士の矛盾、authority境界、不可逆操作、外部side effectが問題になる場合だけ停止する。

## ClaudeからCodexへの完了報告

実装コミットへ混ぜず、次のファイルを新規作成する。

`records/session-handoffs/2026-08-05-claude-to-codex-work4-design-proposal.md`

報告には、commit SHA、作成文書のpathとDigest、全test結果、Human判断が必要な論点、
未実施（code/test/schema/policy/外部書込み）の確認だけを記す。Codexが確認するまで、
Decisionや実装へ進まない。
