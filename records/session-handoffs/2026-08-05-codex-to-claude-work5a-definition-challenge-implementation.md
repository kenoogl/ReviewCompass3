# Codex → Claude：Work 5A Definition Challenge実装指示

## 0. 担当と受け渡し

- **Human**は、Human Contract approval gateのupstream revisionを「採用」し、実装をClaudeへ委譲した。
- **Codex**は、承認済み設計、固定source、TDD順序、停止境界を本指示へ固定した。実装は行わない。
- **Human**が本ファイルをClaudeへ渡す。CodexからClaudeへの直接送信は行わない。
- **Claude**は本ファイルと固定資料をrepositoryから読み、下記の範囲だけをTDDで実施する。
- Claudeの作業終了後、HumanがCodexへ知らせる。CodexはClaudeのcommitと報告を独立検証する。

開始基準commitは`6b6c989cd676be81b81a376a2f6b6253c869c406`である。開始時に、Humanが本指示を
含む後続commitまで取得済みで、worktreeに他者の未コミット変更が無いことを確認する。差分がある場合は
上書きせず停止してHumanへ報告する。

## 1. 目的

後継Review Task Contract version 2に、compile前のDefinition ChallengeとHuman Contract approval gateを
実装する。正常経路は次の順序だけである。

```text
Requirement definition / binding → draft Contract v2 → material set
→ Definition Challenge verdict → Human Contract approval → compile / Plan bundle
→ Context Manifest → Workflow permit → Finding set → Conformance
→ Final Challenge → Human review acceptance → Provenance → accepted artifact
```

今回Claudeが実行してよいのは、実装、GREEN確認、初回Definition Challenge Runまでである。
初回Runが`passed`でも、HumanがContract version 2を承認して`contract_approval`を作る前に停止する。
version 2のcompile、Review Run、Human review acceptance、accepted artifactは作らない。

## 2. 必ず読む固定資料

作業開始前に次を全文読み、SHA-256を機械照合する。一件でも欠落またはDigest不一致なら実装せず停止する。

| 役割 | path | SHA-256 |
| --- | --- | --- |
| 採用Decision | `records/development/2026-08-05-work5a-definition-challenge-contract-approval-gate-adoption-decision-v1.md` | `90f4f8a82041955c0fc4125b88fdd9ab80658a13a22f6eb1027fcbc4f35e2ac3` |
| approval gate Amendment | `docs/design/2026-08-05-work5a-definition-challenge-contract-approval-gate-amendment-v1.md` | `881a9192322e1e1176d3b453dfa121b6dea1a99a6e1c438ad637fc209ed5d0da` |
| 元の承認済み設計 | `docs/design/2026-08-05-work5a-definition-challenge-proposal.md` | `4d8f3fdf8d85b3513cc08575f12e92a80e617e51dff2329c02cf9d84399bfd4f` |
| 元の承認Decision | `records/development/2026-08-05-work5a-definition-challenge-approval-decision-v1.md` | `9ca6a0f75c00f2979437fceca225ede10d28c84f1578a1624db0f04747d7214d` |
| blocking候補 | `records/development/2026-08-05-work5a-definition-challenge-contract-approval-gate-improvement-candidate-v1.md` | `96ee100a0633be4525e59f27d090e6460657e26352416e88d0261172845ff18d` |
| Requirement | `records/requirements/definitions/req-contract-004--v1.json` | `5b0835fd9fb50eee64952575f3a98d9f1d2f43e4f9f82037c5a7abdc66985ebf` |
| Current Plan | `docs/current/reviewcompass3-plan-current.md` | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` |
| Development Policy | `docs/development/2026-08-02-development-policy.md` | `0d34880353f06f50c7623282c765717348c8776938dc3113e28fdad4e9f8ac18` |
| 現行Contract実装 | `tools/task_contract/contract.py` | `be7ec9d314492c529ae0fa962458e35777d400586f8ca461dd5ccbe2c88c74cd` |
| 現行実行・Provenance実装 | `tools/task_contract/execution.py` | `2c9952b7477de32ee81cf9877e29e3f114d25a5fa488b3a8e1707973d1f730e5` |
| identity共通実装 | `tools/task_contract/identity.py` | `d44a8a51aed3bb6c10f6e0289b1bd8b6991bf2092494df052340d24d6e0f6e1a` |
| 公開API | `tools/task_contract/__init__.py` | `649514d501f3dcf72855cc79725e575ed5e680a41e79f93b2595b5f74f768651` |
| 既存Work 5A Test | `tests/test_first_review_task_contract_e2e.py` | `cc99faaa4813aa629c9640431e31d4da635890bc5ec1e1f30c631d06c513661f` |

Work 5Aが直接束縛する16 Requirement definitionも元設計§2.1の材料として全文を読む。Digestは初回Runの
`definition_challenge_material_set`へ各file単位で固定する。Architecture Policy、risk catalog、同じ運用面の
隣接Contract、Challenge Policyは実在しないため、推測で新設しない。

## 3. 作業単位1：RED Testだけを固定する

新規Test fileを次へ作成する。

`tests/test_work5a_definition_challenge.py`

元設計§5のG1〜G4、H1〜H11とAmendment§5のG5〜G8、H12〜H17を、正例・負例・境界例として固定する。
少なくとも次を個別に機械確認する。

- D1〜D8の決定的検査、closedなFinding／verdict schema、同一入力の同一Digest。
- Contract version 2が`requirement_receivers`とpairwise distinctな`review_owners`を持つ。
- Definition Challengeへcompile後のrecordを入力できない。
- `failed` ChallengeではPlan bundleを作らない。
- `passed` Challengeだけでもversion 2をcompileできず、`contract_approval_missing`になる。
- `approved` approvalだけが、同一Contract v2と同一passed verdictへidentity、version、Digestで束縛される。
- approvalの欠落、拒否、改竄、別Contract／別Challengeへの差し替えをAmendmentの閉じたreasonで拒否する。
- version 2 Provenanceは11 node、10 edgeで、`contract_approval`がChallengeとcompileの間にある。
- rejectedまたは改竄approval、failed Challenge、不正Provenanceからaccepted artifactを作れない。
- Contract version 1の既存compileと9 node、8 edge Provenanceが変更なく通る。

この単位では`tools/task_contract/`を変更しない。追加Testを実行し、新APIまたはversion 2 gateが未実装という
期待理由でREDになることを確認する。既存38件はGREENのままであることを確認する。

RED結果を次へnew-onlyで記録する。

`records/development/2026-08-05-work5a-definition-challenge-red-evidence-v1.md`

TestとRED Evidenceだけを一つの意味的commitにする。Test期待をGREENへ向けて後から弱めない。

## 4. 作業単位2：最小実装をGREENにする

`tools/task_contract/`だけへ、承認済み設計を満たす最小実装を行う。責務を分ける必要がある場合は
`tools/task_contract/definition_challenge.py`を新設してよい。未定義の汎用framework、plugin、policy、
拡張pointは作らない。

実装要件は次のとおりである。

1. `definition_challenge_material_set`、`definition_challenge_verdict`、`contract_approval`を版付き、
   Digest付き、上流`record_ref`付きの閉じたrecord kindとして扱う。
2. draft Contract version 2は元設計§6.1で列挙した差分だけをversion 1へ追加する。version 1を上書きしない。
3. D1〜D8を決定的に検査し、Findingは`blocking | nonblocking`、verdictは`passed | failed`だけを使う。
4. Contract approvalはAmendment§2の必須fieldを検証する。会話文、TODO、単なるbooleanで代用しない。
5. `compile_contract`のversion 1呼出し互換性を保持する。version 2ではChallengeとapprovalを必須にし、
   Plan bundle生成前にAmendment§3のreasonでfail-closedにする。
6. Provenanceの期待node／edgeをContract versionに応じて検証する。version 1は9／8、version 2は11／10とし、
   辺数だけで通さず各nodeのkind、identity、version、Digestとedge順序を照合する。
7. Definition Challenge、Contract approval、Conformance、Final Challenge、Human review acceptanceの
   論理owner境界を混同しない。同じHuman個人が別decision classを担うこと自体は禁止しない。
8. public APIは`tools/task_contract/__init__.py`から明示exportする。

追加Test、既存`tests/test_first_review_task_contract_e2e.py`、公式全TestをGREENにする。
実装中に設計矛盾が判明した場合は、Testや設計を局所修正せず停止して報告する。

GREEN Evidenceと公式receiptを次へnew-onlyで作る。

- `records/development/2026-08-05-work5a-definition-challenge-green-evidence-v1.md`
- `records/development/2026-08-05-work5a-definition-challenge-green-test-receipt-v1.json`

公式全Testは次の経路で実行する。

```text
.venv/bin/python3 -m tools.development.policy_test_runner \
  --project-root . \
  --suite full \
  --receipt records/development/2026-08-05-work5a-definition-challenge-green-test-receipt-v1.json
```

実装、Test、GREEN Evidence、receiptを一つのGREEN commitにする。

## 5. 作業単位3：初回Definition Challenge Runだけを行う

GREEN commitとclean transitionの後、実際の固定材料を使って次だけをnew-onlyで作る。

- draft Review Task Contract version 2
- `definition_challenge_material_set`
- `definition_challenge_verdict`
- Runの入力、出力、Digest照合を束ねるrecord bundle
- 実行command、結果、Finding、未実施範囲を記すEvidence

保存先は次とする。

- `records/development/2026-08-05-work5a-definition-challenge-first-run-records-v1.json`
- `records/development/2026-08-05-work5a-definition-challenge-first-run-evidence-v1.md`

Definition ChallengeはContract定義だけを検査する。対象文書の再Review、compile、Plan bundle、Context Manifest、
Workflow permit、Finding set、Conformance、Final Challenge、Human review acceptance、Provenance、
accepted artifactを作らない。

- verdictが`failed`なら、そのまま停止し、Findingと固定Evidenceを報告する。推測でContractや設計を直さない。
- verdictが`passed`でも、`contract_approval`を作らず停止する。HumanのContract version 2承認を代行しない。

TODOを更新する場合は`docs/development/prompts/todo-handoff-update.md`の共通手順だけを使い、構造化projection、
validator、参照Digest検査を通す。Run records、Evidence、機械生成済みTODOだけを一つのcommitにする。

## 6. 各作業単位の共通検証

- stage対象は明示したrepository-relative pathだけにする。`git add -A`と`git add .`を使わない。
- 各commit前に`git diff --check`と該当Test／validatorを実行する。
- 完了済み作業単位を未コミットのまま次へ渡さない。
- commit後にread-onlyで差分、commit内容、worktreeを照合し、
  `python3 tools/development/work_unit_transition.py --work-status completed`を実行する。
- Pythonは4スペース、その他は既存formatterに従う。無関係な一括整形をしない。
- 既存の利用者差分があれば変更、stage、commitしない。

## 7. 禁止事項と停止条件

- 承認済み設計、Amendment、Decision、Requirement、Current Plan、checklist、Development Policyを変更しない。
- Contract version 1、既存accepted artifact、既存Provenance recordを上書き、無効化、stale化しない。
- Humanの`contract_approval`またはHuman review acceptanceを作成、推測、代行しない。
- Work 4B、Work 6A、Architecture Policy、Challenge Policy、risk catalog、隣接Contract、汎用Challenge
  framework、LLM reviewer、UI、CI、外部`DATA_ROOT`を開始しない。
- push、PR、tag、amend、rebase、reset、force push、履歴書換え、外部送信を行わない。
- 固定source不一致、設計矛盾、REDが期待理由で失敗しない、既存Testの回帰、全Test不合格、
  実Runの`failed`では停止し、範囲を広げず報告する。

## 8. ClaudeからCodexへの完了報告

完了報告は実装commitへ混ぜず、Git管理外の次へ新規保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-work5a-definition-challenge-implementation.md`

報告には次を記す。

- RED、GREEN、初回Runの各commit SHA。
- 追加したpublic API、record kind、stop reason、変更module。
- REDの期待失敗、追加Test、既存38件、公式全Testの実測結果とreceipt path。
- 初回RunのContract v2、material set、verdictのID、version、content digest、Finding件数。
- `contract_approval`、compile、Review Run、accepted artifactを作っていない確認。
- 変更していない範囲、停止または設計上の判断が生じた場合の根拠。

報告作成後は次へ進まない。HumanがCodexへ作業終了を知らせ、Codexの独立検証を待つ。
