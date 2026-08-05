# Work 5A Human Contract approval gate 採用Decision v1

- Decision ID：`DEC-WORK5A-DEFINITION-CONTRACT-APPROVAL-GATE-001`
- decision maker：Human
- decided at：2026-08-05
- 対象候補：`IC-WORK5A-DEFINITION-CONTRACT-APPROVAL-GATE-001`

## 1. Human判断

Humanは、blocking改善候補の`upstream_revision`提案を「採用」と裁定した。

## 2. 採用内容

- Definition Challenge verdictとcompile verdictの間に、Humanが作る`contract_approval`recordを追加する。
- Contract version 2のcompileは、`passed` Challengeと`approved` Contract approvalの両方を必須にする。
- 欠落、拒否、content digest改竄、Contract ref不一致、Challenge ref不一致では
  `not_compilable`とし、Plan bundleを作らない。
- Contract version 2のProvenanceは`contract_approval`を含む11 node、10 edgeとする。
- Contract version 1の既存compileと9 node、8 edge履歴は変更しない。

## 3. 実装委譲

Humanは、実装作業をClaudeへ委譲するよう追加指示した。Codexは本Decision、Amendment、
固定source、TDD順序、停止境界を含む実装handoffを作成する。HumanがそのhandoffをClaudeへ渡し、
Claudeの作業終了後にCodexへ知らせる。CodexからClaudeへの直接送信は行わない。

Claudeへの委譲は次を変えない。

- 先にRED Testを作り、実装不在による期待理由の失敗を確認・commitする。
- 実装中は承認済みTestを弱めない。
- 初回Definition Challenge実Run後、Contract version 2のHuman承認前に停止する。
- push、PR、CI、外部送信の追加、既存Contract version 1の変更を行わない。

## 4. 固定入力

| 種別 | path | SHA-256 |
| --- | --- | --- |
| 承認済みAmendment | `docs/design/2026-08-05-work5a-definition-challenge-contract-approval-gate-amendment-v1.md` | `881a9192322e1e1176d3b453dfa121b6dea1a99a6e1c438ad637fc209ed5d0da` |
| blocking候補 | `records/development/2026-08-05-work5a-definition-challenge-contract-approval-gate-improvement-candidate-v1.md` | `96ee100a0633be4525e59f27d090e6460657e26352416e88d0261172845ff18d` |
| 元の承認Decision | `records/development/2026-08-05-work5a-definition-challenge-approval-decision-v1.md` | `9ca6a0f75c00f2979437fceca225ede10d28c84f1578a1624db0f04747d7214d` |
| 元の承認済み設計 | `docs/design/2026-08-05-work5a-definition-challenge-proposal.md` | `4d8f3fdf8d85b3513cc08575f12e92a80e617e51dff2329c02cf9d84399bfd4f` |
| Requirement | `records/requirements/definitions/req-contract-004--v1.json` | `5b0835fd9fb50eee64952575f3a98d9f1d2f43e4f9f82037c5a7abdc66985ebf` |

## 5. 非承認範囲

- 初回Definition Challenge実Run後のContract version 2承認
- Contract version 2承認前のcompile、Review Run、accepted artifact作成
- Work 5Aまたは段の完了判断
- Work 6A、汎用Challenge framework、Architecture Policy、Challenge Policy、risk catalog、隣接Contractの新設
- push、PR、CI、その他の外部送信

## 6. 次の停止境界

本DecisionとClaude実装handoffを含むcommitがcleanになった後に、HumanがClaudeへ実装を委譲する。
Claudeは初回Definition Challenge実Runの結果と固定Evidenceを返し、Contract version 2のHuman承認前に停止する。
