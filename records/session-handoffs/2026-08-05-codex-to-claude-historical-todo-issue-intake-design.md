# Codex → Claude：過去TODOからのIssue Intake設計指示

## 誰が何をするか

- **Human**は、過去TODOに埋もれた個別の問題候補を忘却させず、Issue化を早急に進めると指示した。
- **Codex**は、忘却防止の候補`IC-HISTORICAL-TODO-ISSUE-INTAKE-001`を記録した。
- **Claude**は、既存の一件限定Issue Pilotを複数Issueの受付へ拡張する設計提案だけを作る。
- **Human**が設計を承認するまで、config、validator、既存Issue、Plan、TODO、個別Issueを変更しない。

## 現在の制約

`config/development-issue-resolution-pilot-v2.json`は`maximum_issue_subjects: 1`である。
そのため、既存の`ISSUE-PILOT-TODO-GROWTH-001`以外を今の形式で追加すると、早期Pilotの契約を破る。

この制約を無視して個別Issueを増やさない。設計で複数件の受入条件と、履歴をIssueへ複製しない境界を
先に固定する。

## 固定材料

- `records/session-handoffs/2026-08-04-todo-before-compaction-001.md`
  - SHA-256：`16010a165c010fa8a25cea5ab0f11990734540f4d5c0f5fdb50fd7c21ee6c0f1`
- `.reviewcompass/workflow/improvement-candidates/ic-historical-todo-issue-intake-001--v1.json`
  - candidate ID：`IC-HISTORICAL-TODO-ISSUE-INTAKE-001`
- `.reviewcompass/workflow/issues/issue-pilot-todo-growth-001--v1.json`
- `.reviewcompass/workflow/resolution-verdicts/verdict-pilot-todo-growth-001--v1.json`
- `config/development-issue-resolution-pilot-v2.json`
- `tools/development/issue_resolution_pilot.py`と関連test
- `docs/development/2026-08-02-development-policy.md`

## Claudeが作るもの

次の新規設計提案一件だけを作る。

`docs/design/2026-08-05-historical-todo-issue-intake-proposal.md`

状態は`awaiting_human_approval`とする。Decision record、config、code、test、Issue recordは作らない。

設計案には、少なくとも次を含める。

1. **現在のPilotと新しい複数Issue Intakeの境界**
   - 早期Pilotの一件限定recordを履歴として保持し、上書きしない方法。
   - 新しい複数Issue用のversion、最大件数、active Issue数、並行禁止との関係。
2. **source universeと抽出規則**
   - 圧縮前TODO snapshotのどの見出し・記述を候補にするか。
   - 完了Claim、解決済み手戻り、Evidence説明、単なる履歴を除外する決定的規則。
   - 候補ごとに保存するsource位置、引用、Digest、既存Evidence／Issueとの重複判定。
3. **Human判断の境界**
   - 機械は候補一覧だけを作り、未解決、再発性、影響、priority、Issue昇格はHumanが決めること。
   - Humanが一括判断できる条件と、一件ずつ判断が必要な条件。
4. **IssueのlifecycleとPlanへの接続**
   - candidate → triage decision → issue → plan → work → resolution verdictの関係。
   - Issueを増やしてもTODOに詳細を再累積させないprojection規則。
5. **TDD受入条件**
   - 正常例：複数候補、既存解決済みIssueとの共存、Humanが選んだ複数Issueの登録。
   - 負例：解決済み履歴の誤登録、Evidenceだけの誤登録、source Digest不一致、重複Issue、
     Human裁定無しの自動Issue化、active leafを越える実行開始。
6. **段階的実施計画**
   - 設計承認 → RED → schema／validator → historical候補一覧作成 → Human triage → 個別Issue作成 → Plan化。
   - 各段階の停止条件とHuman承認が必要な箇所。

## 禁止事項

- config、validator、test、既存Issue、TODO、Plan、checklist、Requirementを変更しない。
- 圧縮前TODOの記述を自動でIssueへ昇格しない。
- LLM、外部送信、外部`DATA_ROOT`、push、PR、CI、Work 4B、Work 6A、E2以降を開始しない。

## 検証・コミット・完了報告

- 設計文書内の参照と`git diff --check`を確認する。
- 設計文書一件だけを一つのコミットにする。
- 完了報告はコミットに混ぜず、次へ新規保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-historical-todo-issue-intake-design.md`

報告には、commit SHA、提案した複数Issue境界、機械抽出できる候補とHuman判断が必要な点、
未実施事項を記す。
