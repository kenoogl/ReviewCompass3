# Codex → Claude：Work 5A 最初の実Review結果の受理指示

## 誰が何をするか

- **Human**は、2026-08-05に最初の実Review結果を「承認」と判断した。
- **Claude**は、この承認を根拠に、ReviewCompass3の最小Review経路を完結させる三つのrecordを作成する。
- **Codex**は、Claudeの完了報告を独立に検証する。ClaudeはCodexの確認前に次作業へ進まない。

この承認は、review対象文書の内容を修正する指示ではない。今回のdeterministic stub reviewerの指摘0件を、
この最小実Review Runの結果として受理する判断である。設計内容の完全性を保証する判断ではない。

## 固定入力

- 上流record bundle：
  `records/development/2026-08-05-work5a-first-real-review-run-records-v1.json`
  - file SHA-256：`658e5ba98d6023085709733f91130a8b64acd674b3c9ca497b3f23784d588447`
- 上流Evidence：
  `records/development/2026-08-05-work5a-first-real-review-run-evidence-v1.md`
  - file SHA-256：`cdc4c4d8ad08a6f0d8373ea56d46018e070618ba2152ade7ac4dd09d72808b50`
- review対象：
  `docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md`
  - SHA-256：`14901323a958d686ba0ad0aed62b20b7b7d79908afcced08dc90f72fdb3d2054`
- Human decision：`approved`
- Human ID：`kenoogl`
- 決定時刻：Claudeがrecord作成時に、実際のJST時刻をISO 8601形式で記録する。

## 実施範囲

1. 上流bundleとEvidenceのfile SHA-256、上流9 recordの相互参照、targetのSHA-256を読み戻して照合する。
2. 現在のtarget SHA-256が固定入力と一致することを確認する。不一致なら`stale`として停止し、
   Human decision、Provenance verdict、accepted artifactを作らない。
3. `tools.task_contract`の既存APIだけを使い、上流9 recordに接続する次の三recordを作る。
   - `human_decision`（`approved`、Humanの実際の判断「承認」に束縛する）
   - `provenance_verdict`（上流9 recordとHuman decisionの来歴が連続していることを確認する）
   - `accepted_artifact`（上記二recordが成立した場合だけ作る）
4. 新規作成した三recordを、上流bundleへのfile digest参照とともに、次のnew-only fileへ保存する。
   - `records/development/2026-08-05-work5a-first-real-review-acceptance-records-v1.json`
5. 人向けの短い証跡を次へ作る。
   - `records/development/2026-08-05-work5a-first-real-review-acceptance-evidence-v1.md`
   - 「今回受理したのは最小レビュー経路の実行結果であり、対象文書の品質保証ではない」と明記する。
6. `TODO_NEXT_SESSION.md`を「Work 5Aの最初のhappy pathはaccepted artifactまで完了」に更新する。
   次作業は決めない。Current Planとchecklistは変更しない。

## 検証とコミット

- 保存後に新規三recordのDigest、上流record参照、target Digest、accepted artifactの参照を読み戻して照合する。
- TODO構造検査、TODO参照Digest検査、`git diff --check`、公式venv runnerの全testを実行する。
- 作成するrecord bundle、Evidence、TODOだけを一つのコミットにする。実装、テスト、target文書、Plan、checklistを混ぜない。

## 禁止事項と停止条件

- `tools/task_contract/`、`tests/`、review対象文書、Requirement、Current Plan、checklistを変更しない。
- LLM、外部送信、外部`DATA_ROOT`、push、PR、CI、Work 4B、Work 6A、E2以降を開始しない。
- target、上流bundle、上流EvidenceのDigest不一致、record参照不一致、またはProvenance検証不成立なら、
  accepted artifactを作らず、理由を完了報告へ記して停止する。

## ClaudeからCodexへの完了報告

コミットに混ぜず、次へ新規保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-work5a-review-acceptance.md`

報告には、commit SHA、照合した固定入力、三recordのIDとDigest、accepted artifactの有無、
全test結果、変更していない範囲だけを記す。
