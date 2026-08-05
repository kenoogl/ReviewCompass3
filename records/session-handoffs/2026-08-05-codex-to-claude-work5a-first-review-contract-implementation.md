# Codex → Claude：Work 5A 最小Review Task Contract実装指示

## 0. 実行者・Human承認

**実行者はClaudeである。** Claudeは本ファイルを読み、Work 5Aの最小Review Task Contractを実装する。
Humanは2026-08-05に
`docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md`を承認した。

この承認で固定する§9の五点は次のとおりである。

1. review対象は`docs/`配下の指定した一文書に限定する。
2. 直接束縛Requirementは§7の16件、残り34件はdeferredとする。
3. `warning`はConformance／Final Challengeを自動失格にしない。ただしHuman decisionは正常経路でも
   常に必須であり、warningを無視してaccepted artifactを自動確定してはならない。`error`は停止する。
4. `tools/bootstrap/`は参照だけとし、Work 5AのRuntime componentへ昇格しない。
5. ConformanceとFinal Challengeは、異なる論理ownerと異なるrecordで実行する。Humanは両verdictの後に
   独立してdecisionを行い、どちらのownerにもならない。

§11のE2〜E7は本実装のscope外である。E2、E4、E5の開始時には別途Human判断が必要である。

## 1. 固定scope

代表scenarioは`new_development / fresh`だけ、対象はReviewCompass3自身の`docs/`配下の小さな文書変更
一件だけとする。reviewerはdeterministic stubであり、LLM、外部送信、CI、push、PR、UI、
delegated AI、複数Contract type、複数Work Item、`maintenance`、`reopen`、`bounded_parallel`は実装しない。

Work 4A／4BのReuse Discovery、Entry、Relation、Baseline、統合リファクタリングはscope外である。
対象が文書変更のため、外部DATA_ROOTにも書き込まない。

## 2. 実装対象

新しい最小Runtime packageを`tools/task_contract/`の下に作る。`tools/bootstrap/`、`tools/development/`へ
実装を足してRuntime componentを混在させない。

実装するのは提案§2〜§8の最小経路だけである。

```text
Requirement binding
  → Review Task Contract
  → Compile verdict / Plan bundle / 6 typed view
  → Context Manifest
  → Workflow permit（single_active_leaf）
  → deterministic stub reviewer / Finding set
  → Conformance verdict
  → Final Challenge verdict
  → Human decision record
  → Provenance verdict
  → accepted artifact
```

- すべてのrecordはidentity、version、Digest、上流record referenceを持つ。
- Contract schemaは提案§2のidentity、responsibility、boundary、precondition、context obligation、
  allowed capability、expected output、acceptance、provenance、escalationを必須にする。
- Compilerは一Contract type、一versionから一Plan bundleと6 typed viewだけを決定的に作る。
- Contextは明示した材料だけを使い、Digest不一致、暗黙資料、範囲外pathを拒否する。
- permitは同時active leafを一件だけ許可する。
- stub reviewerは閉じたseverity（`error`、`warning`、`info`）のFindingを返す。LLMを呼ばない。
- ConformanceとFinal Challengeは別validator／別recordとして実装する。
- Human decisionは対象Digestと明示的な決定内容を束縛する。Human decision無し、Digest不一致、
  `error` Finding、いずれかのverdict不合格、Provenance断絶ではaccepted artifactを確定しない。
- source、Context、Contract、Policy相当の固定入力が変わった場合は、旧結果を再利用せず`stale`で停止する。

recordの具体的field・record kindは提案と束縛した16 Requirementを満たす最小の閉じたschemaとして
Claudeが決める。未定義の汎用schema、plugin、拡張ポイントは作らない。

## 3. TDDとコミット境界

### A. 設計確定コミット

- `records/development/`へWork 4設計承認Decisionをnew-onlyで作成する。承認文言、上記5決定、
  E2〜E7のdeferを引用する。
- Work 4 proposalの状態を`approved_for_implementation`へ更新する。
- Current Planとchecklistには「Work 4の最初のslice設計が承認され、Work 5Aへ進む」ことだけを
  記録する。Work 4全体、Work 5A、Work 4Bを完了扱いにしない。
- TODOをWork 5A実装中へ更新する。全参照Digestを再計算する。
- このコミットにcode、test、外部書込みを含めない。

### B. REDコミット

- `tests/test_first_review_task_contract_e2e.py`を新規作成し、提案§8のA1〜A11、B1〜B10、C1〜C4を
  受入testとして固定する。
- REDが未実装のRuntime packageまたはAPI不足という期待理由で失敗することを確認し、
  RED Evidenceを`records/development/`へnew-onlyで記録する。
- 既存testを弱めず、test期待をGREENに向けて書き換えない。

### C. GREEN実装コミット

- `tools/task_contract/`の最小Runtime packageと必要なfixtureだけを実装する。
- A1〜A11、B1〜B10、C1〜C4、既存全testをGREENにする。
- GREEN Evidenceを`records/development/`へnew-onlyで記録する。
- TODOを「Work 5A実装GREEN、実review run前」として更新し、全参照Digestを再計算する。

各コミットは独立して説明可能にし、完了済み作業単位を未コミットのまま次へ進まない。

## 4. 明確な禁止事項

- 実文書に対するreview run、Human decision、accepted artifactの作成を行わない。
- Requirement、Requirement authority、既存bootstrap、既存Work 4A Evidence、Work 4B scopeを変更しない。
- LLM、外部送信、外部DATA_ROOT、Git write／push／PR／CIを使わない。
- E2〜E7、Implementation Task Contract、台帳、リファクタリングを始めない。
- 設計と受入条件を満たせない矛盾、authority、安全性、不可逆操作の問題以外では止まらない。

## 5. ClaudeからCodexへの完了報告

実装コミットへ報告を混ぜない。次へ新規保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-work5a-first-review-contract-implementation.md`

報告にはA〜Cのcommit SHA、RED／GREEN／全test結果、作成したrecord kindとmodule path、
実review run・LLM・外部書込みを行っていない事実、設計停止があった場合だけその根拠を記す。
Codexが確認するまで、実review run、E2以降、Work 4Bへ進まない。
