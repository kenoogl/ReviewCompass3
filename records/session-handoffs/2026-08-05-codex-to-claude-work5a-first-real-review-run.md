# Codex → Claude：Work 5A 最初の実Review Run指示

## 実行者・Human承認・対象

**実行者はClaudeである。** Claudeは本ファイルを読み、Work 5Aの最初の実Review Runを実施する。
Humanは2026-08-05に次へ進むことを指示し、対象と範囲は次に固定する。

- target：`docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md`
- scenario：`new_development / fresh`
- review範囲：target一文書だけ
- base commit：`0ad628f`
- targetを含むhead commit：`2edb1b6`
- reviewer：deterministic stub reviewer

現在HEADと`2edb1b6`の間でtargetが変わっていないことをGitで確認する。変わっていた場合は、
このrunを開始せず`stale`として停止する。対象文書を書き換えない。

## 実施する範囲

実装済み`tools.task_contract`を使い、次を順に機械実行する。

```text
Requirement binding → Source Snapshot → Review Task Contract → compile / 6 typed view
→ Context Manifest → permit → deterministic stub review → Conformance → Final Challenge
```

RequirementはWork 4 proposal §7の16件を実repositoryのauthority definitionから束縛する。
Finding、Conformance、Final Challengeの結果を改竄せず記録する。想定ではerror 0件、warning 0件であるが、
実測値を優先する。

## 保存物

runにより得たHuman decision前のrecordを、次へnew-onlyで保存する。

1. `records/development/2026-08-05-work5a-first-real-review-run-records-v1.json`
   - Requirement bindingからFinal Challengeまでのrecord
   - source内容は重複保存せず、target path、Digest、base/head commitだけを保存する
   - `human_decision`、`provenance_verdict`、`accepted_artifact`を含めない
2. `records/development/2026-08-05-work5a-first-real-review-run-evidence-v1.md`
   - target、base/head、record ID/Digest、Finding件数、Conformance／Final Challenge結果、
     実行command、Human decisionが未実施であることを記す

Human decision無しではProvenance verdictとaccepted artifactを作らない。結果がerrorまたはwarningでも、
文書を自動修正しない。Humanへ提示して停止する。

## 検証・TODO・コミット

- targetが指定commitから変化していないことをGitで検証する。
- 保存後、全recordのDigest、相互reference、target Digestを読み戻して照合する。
- `TODO_NEXT_SESSION.md`を「最初の実Review Run完了、Human decision待ち」へ更新し、
  Evidenceとrecord bundleのDigestを実ファイルから再計算して記載する。
- TODO構造検査、TODO参照Digest検査、`git diff --check`、公式venv runnerの全testを実行する。
- record bundle、Evidence、TODOだけを一つのコミットにする。code、test、target文書を混ぜない。

## 禁止事項

- Human decision、Provenance verdict、accepted artifact、target文書の修正を作成しない。
- LLM、外部送信、外部DATA_ROOT、push、PR、CI、Work 4B、E2以降を開始しない。
- Requirement、Current Plan、checklist、Work 5A実装を変更しない。

## ClaudeからCodexへの完了報告

コミットに混ぜず、次へ新規保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-work5a-first-real-review-run.md`

報告にはcommit SHA、targetとbase/head、Finding件数、Conformance／Final Challenge結果、
record bundleとEvidenceのDigest、全test結果、Human decision等を行っていない事実だけを記す。
Codexが確認するまで次へ進まない。
