---
lifecycle: proposed
normative_status: non-normative-design-proposal
implementation_status: human_hold
related_pilot_memo: 2026-08-04-reviewcompass2-issue-path-adoption-pilot-memo.md
related_approval: ../../records/development/2026-08-04-reviewcompass2-issue-path-early-pilot-decision.json
---

# TODO対策における手戻り候補の扱い修正メモ

## 1. 目的

`TODO_NEXT_SESSION.md`の巨大化対策について、手戻り・機械化候補の詳細をTODOへ累積する案を修正する。
作業後報告、耐久記録、Issue昇格、現在handoffを分離し、手戻り候補はReviewCompass2由来のIssue経路へ
routeする。TODOは候補の保存場所ではなく、現在作業に必要な状態projectionだけを表示する。

本メモは先に承認されたIssue Resolution早期Pilotの設計補足であり、実装開始permitではない。
既存policy、repository instruction、TODO template、validator、TODOの候補保存構造は、Humanの明示的な
再開指示まで変更しない。

## 2. 修正理由

現行のTODO templateには、`手戻り・機械化候補`として次の詳細を記載する欄がある。

- 対象操作
- 期待executorと実executor
- 手作業理由
- 手戻り事象とEvidence
- 機械処理候補
- route

これらは原因分析と改善判断には必要だが、sessionごとにTODOへ残すと、解決済み候補までhandoffへ累積する。
現行TODOが巨大化した主因の一つである。

開発policyが要求するのは、手戻りと手作業の因果を作業後報告へ含め、改善候補として記録・routeすることである。
TODOを候補の正本または恒久保存場所にすることは要求していない。作業後報告とTODO保存を同一視しない。

## 3. 固定参照

| role | artifact | SHA-256 |
|---|---|---|
| repository instruction | `AGENTS.md` | `31fb527bb5415249f25c7d73cb9c464cf6f532acfe6746ba4107284e2ab3c32b` |
| development policy | `docs/development/2026-08-02-development-policy.md` | `444898d51e1190458de000fbc3d6499a5bacee5dce2353a07e723e1b4546dc5e` |
| TODO template | `docs/development/templates/TODO_NEXT_SESSION.template.md` | `d2ec0b61441401887533bd2bce5b0d0040112765df7ad9932056fef267bd7f5a` |
| approved Pilot memo | `docs/design/2026-08-04-reviewcompass2-issue-path-adoption-pilot-memo.md` | `e0a1a140ad76a06c00e08244314a00d866e92efb0a377773358c00d5c0f4f4ef` |
| early Pilot Decision | `records/development/2026-08-04-reviewcompass2-issue-path-early-pilot-decision.json` | `5e19bca05aead7836595168f8e44edc3a5f146507ab33ffde3646de964814f9f` |

先行Pilotメモは承認DecisionがDigestへ束縛されているため書き換えない。本メモで、TODO対策における
手戻り候補の保存と表示を追加修正する。

## 4. 修正後の責務分離

### 4.1 作業後報告

作業終了時の会話では、発生した手戻りについて次を平易に報告する。

- 何が起きたか
- 手作業との因果
- 期待executorと実executor
- どう対処したか
- 機械処理候補
- どのrouteを提案するか

この報告は利用者がその場で状況を判断するための説明であり、TODOへの恒久転記を意味しない。

### 4.2 耐久記録

手戻りが`manual_rework_candidate`または`manual_operation_candidate`に該当する場合は、発生元Work、
固定source、Evidence、影響、提案を持つImprovement Candidateとして耐久記録する。候補の詳細をTODOへ
複製しない。

先行Pilotの暫定配置案にはImprovement Candidateの保存先が明示されていなかったため、実装再開後の候補rootを
次のように修正する。

```text
records/development/issue-resolution-pilot/
  improvement-candidates/
  triage-decisions/
  issue-records/
  resolution-plans/
  plan-challenges/
  resolution-verdicts/
  evidence/
```

この配置はdevelopment限定のPilot案であり、製品の正式schemaまたはauthorityではない。

### 4.3 Issue昇格

Improvement Candidateを自動的にIssueへ変換しない。Human Triage Decisionで、独立追跡が必要と判断された
候補だけをIssue Recordへ昇格する。

Issue昇格の主な判断材料は次とする。

- 現行作業内では解決していない
- 同種問題が再発している
- 複数Workまたは複数consumerへ影響する
- 独立したowner、Plan、Acceptanceまたは後続実行が必要である
- checkpointだけでは消費漏れのriskがある

同じ作業内で恒久対策とVerificationまで完了し、独立追跡が不要な候補はIssueへ昇格させない。その場合も
Candidate、Triage Decision、Completion EvidenceまたはResolution Evidenceの結線を残し、単なる会話記録で
閉じない。

### 4.4 TODO表示

TODOには候補やIssueの全文を置かず、現在作業に直接影響するものだけを次の形で表示する。

```markdown
## 現在作業に影響する改善候補／Issue

- `<candidate-or-issue-id>`：`<derived state>`、影響：`<current impact>`、次：`<one action>`
```

表示対象がなければ`なし`とする。解決済み、却下、duplicate、defer済み、現在作業へ影響しない候補はTODOから
除き、耐久recordとmachine projectionから参照する。

## 5. 修正後の経路

```text
Observed rework / manual operation
  → immediate Human-readable report
  → durable Improvement Candidate
  → Human Triage Decision
      ├─ current Work / upstream revision / dependency
      ├─ checkpoint / defer / reject / duplicate
      └─ Issue Record
           → Issue Resolution Plan
           → Plan Challenge
           → Task Contract／Work Item
           → Verification Evidence
           → Resolution Verdict

TODO_NEXT_SESSION.md
  ← active candidate／IssueのID、導出状態、現在影響、次の一操作だけをprojection
```

## 6. validatorとpromptの位置付け

TODO累積の再発防止は、短いpromptだけに依存させない。次の三層を組み合わせる。

1. policy／repository instructionで、TODOはprojectionであり候補の正本ではないと定める。
2. machine validatorで、詳細な手戻り履歴、解決済み候補、参照不能ID、上限超過を検出する。
3. Codex／Claude共通の短い更新promptで、現在情報への置換とmachine validator実行を促す。

promptはLLMの記載漏れを減らす補助手段とする。合否判定、ID参照、件数、byte数、状態導出はmachineが担う。

## 7. 実装再開後に変更する対象

HumanがPilot実装再開を明示した後、次を一つの整合した変更として進める。

1. Improvement Candidateの暫定identity、field、Digest、命名規則を固定する。
2. 正常例、負例、境界例をtest-firstで用意する。
3. Pilot用`improvement-candidates/`とTriage Decision経路を作る。
4. development policyと`AGENTS.md`で、作業後報告とTODO保存の違いを明示する。
5. TODO templateの`手戻り・機械化候補`詳細欄を、active ID projection欄へ置き換える。
6. 現行TODOの詳細履歴をmilestone snapshotと耐久Evidenceへ退避してから縮小する。
7. validatorへ詳細履歴、解決済み候補、参照、件数、byte上限の検査を追加する。
8. Codex／Claude共通promptを追加し、validatorを通してpost-write verificationする。

途中でTODO詳細を先に削除し、唯一のEvidenceまたは未処理義務を失わせない。

## 8. Acceptance

- 作業後報告には、手戻りと手作業の因果、Evidence、対処、機械処理候補、routeが含まれる。
- 手戻り候補の詳細はTODOではなく、Digestを持つ耐久recordへ到達できる。
- Issue昇格はHuman Decisionに限定され、自動昇格しない。
- TODOはactiveな候補／IssueのID、導出状態、現在影響、次の一操作だけを保持する。
- 解決済み候補をTODOから除いても、Candidate、Decision、Evidence、Verdictへ到達できる。
- validatorが詳細履歴の再累積、参照不能ID、上限超過を負例として検出する。
- CodexとClaudeの入口が同じpolicyとvalidatorを参照する。

## 9. 現在状態

- 手戻り候補の扱いを修正したTODO対策案：本メモへ記録済み。
- 先行Pilotメモと承認Decision：変更なし。
- policy、`AGENTS.md`、TODO template、validator、現行TODOの構造変更：未実施。
- Improvement Candidate、Issue Record、Plan、Challenge、VerdictのPilot artifact：未作成。
- 実装開始：保留。Humanの明示的な再開指示が必要。
- commit、push：未実施。
