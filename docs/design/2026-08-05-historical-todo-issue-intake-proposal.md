# 過去TODOからのIssue Intake設計提案

状態：`approved_for_development_use`
対象：既存の一件限定Issue Pilotを、複数Issueの受付へ拡張する境界
改善候補：`IC-HISTORICAL-TODO-ISSUE-INTAKE-001`
承認記録：`DEC-HISTORICAL-TODO-ISSUE-INTAKE-001`

## 実施状態注記（2026-08-05）

この節だけが提案後に追記した現在の状態である。以降の本文は提案時点の事前計画をそのまま残しており、
過去形・将来形の書き換えはしていない。

- HumanはIssue Intake V4を**development-only provisional**（開発用・暫定）として承認した。
  `pilot_mode: development_only_provisional`は維持する。
- 実装、GREEN Evidence、過去TODO候補41件のHuman triageは完了している。有効decisionは41件で競合は無い。
- 現在のV4 Issueは3件（`ISSUE-HTC-BEB5E0BD`、`ISSUE-HTC-C9F6C917`、`ISSUE-HTC-66C3E6CA`）で、
  いずれも`registered`かつnonblockingである。active Issueは0件である。
- 正式製品schema、UI、automation、Work 8評価、および上記3 IssueのPlan化・実装は**承認範囲外**である。
- 承認record：`records/development/2026-08-05-historical-todo-issue-intake-v4-approval-decision-v1.md`
- 閉鎖Evidence：`records/development/2026-08-05-historical-todo-issue-intake-v4-closure-evidence-v1.md`

以下は提案時点の本文である。

**これはDecision recordではない。**承認までconfig、validator、code、test、既存Issue、Plan、TODOを
変更しない。圧縮前TODOの記述を自動でIssueへ昇格しない。

## 0. 先に報告すべき事実：現在testが1件失敗している

改善候補record `ic-historical-todo-issue-intake-001--v1.json`が
`.reviewcompass/workflow/improvement-candidates/`へ追加されたことで、
一件限定Pilotの受入testが現在**失敗している**。

```text
FAILED tests/test_issue_resolution_pilot.py::test_repository_contains_only_the_single_valid_pilot_subject
1 failed, 776 passed
```

原因は`tests/test_issue_resolution_pilot.py:182`の
`assert candidate_files == [CANDIDATE_PATH]`である。候補directoryに1 fileだけを許す検査であり、
現在は2 fileある。

これは本提案が扱う「一件限定の契約を破らずに複数件へ広げる」問題が、**候補記録の追加時点で
すでに顕在化している**ことを示す。本提案では、この失敗を局所修正で消さず、
§6の実施計画のなかで正しい形（新しいpilot versionの導入）で解消する。

本提案ではtestもconfigも変更しない。復旧の順序だけを設計として固定する。

## 1. 現在のPilotと新しい複数Issue Intakeの境界

### 1.1 既存記録の保持

早期Pilot（`pilot_version` 2および3）で作った次の記録は、履歴として保持し上書きしない。

| record | 状態 |
| --- | --- |
| `IC-PILOT-TODO-GROWTH-001` | 候補 |
| `DEC-PILOT-TODO-GROWTH-001` | triage decision |
| `ISSUE-PILOT-TODO-GROWTH-001` | Issue |
| `VERDICT-PILOT-TODO-GROWTH-001` | `outcome: resolved` |

これらは`pilot_version` 2／3のconfigで検証できる形のまま残す。
新しいversionのvalidatorは、旧versionの記録をversionごとの規則で読む。旧記録を新規則で再判定しない。

### 1.2 新しいversionと上限の置き方

`config/development-issue-resolution-pilot-v4.json`を新規に作る（v2、v3は変更しない）。
現行の`maximum_issue_subjects: 1`は、**「登録できる件数」と「同時に着手できる件数」を
区別していない**。V4では区別し、**登録済みIssue数に上限を置かない。**

| 設定 | 意味 | 値 |
| --- | --- | --- |
| 登録済みIssue数 | 発見して保存したIssueの総数 | **上限なし** |
| `maximum_active_issues` | 同時に`in_progress`にできるIssue数 | **1** |
| `maximum_active_leaves` | 同時に開始できるWork Item数 | **1**（既存の`single_active_leaf`と一致） |

上限を置くのは「同時に手を動かす数」だけである。問題を見つけたら件数を気にせず登録でき、
着手は常に一件に絞る。これによりWork 5Aの`single_active_leaf`および並行禁止と矛盾しない。

`registered`、`untriaged`、`deferred`、`suspended`のIssueは、**作業中Issue数に数えない。**
数えるのは`in_progress`だけである（§1.4）。

`pilot_version` 4のconfigは、旧`maximum_issue_subjects`も`maximum_registered_issues`も持たない。
validatorはversionごとに必須fieldを切り替える。旧versionでは`maximum_issue_subjects == 1`の
検査を維持する。

### 1.3 候補directoryの扱い

現在の受入testは候補file数を1に固定している。v4では、候補の総数ではなく
**「未triageの候補が滞留していないか」**を検査対象にする。
具体的には、各候補が`triage_decision_ref`を持つか、`untriaged`として明示されているかを見る。

### 1.4 Issueの状態と、作業中上限への算入

| 状態 | 意味 | 同時作業中上限への算入 |
| --- | --- | --- |
| `registered`／`untriaged` | 発見・保存されたが人の裁定前 | 算入しない |
| `deferred` | 人が後回しと決めた | 算入しない |
| `in_progress` | 現在、解決作業をしている | **算入する。常に最大1件** |
| `suspended` | 別の阻害問題のため中断した | 算入しない |
| `resolved`／`rejected` | 終了した | 算入しない |

#### 既存語彙との対応

既存recordは`issue_record`に`state`を持たず、進行はTODOと`resolution_verdict`の
`outcome`（`resolved`）で表していた。上表の状態語彙はV4で新設する。

| V4の状態 | 既存記録での表れ方 |
| --- | --- |
| `registered`／`untriaged` | `triage_decision_ref`が無い候補 |
| `deferred` | triage decisionの`disposition: defer` |
| `in_progress` | 明示的な表現なし（TODOのactive表示だけ） |
| `suspended` | 表現なし（V4で新設） |
| `resolved` | `resolution_verdict.outcome: resolved` |
| `rejected` | triage decisionの`disposition: reject` |

`state`は`issue_record`のschema版上げ（`schema_version` 2）を必要とする。
**名称だけを既存recordへ遡及適用しない。**既存の
`ISSUE-PILOT-TODO-GROWTH-001`は`schema_version` 1のまま保持し、V4のstateを後から書き込まない。
既存Issueの現在状態は、既存`resolution_verdict`の`outcome`から読む。

### 1.5 新しい問題が見つかった場合の中断規則

新しい問題の発見で作業が行き詰まらないようにする。

1. 新しい問題は、現在`in_progress`のIssueがあっても**登録できる**。登録に上限は無い。
2. 新しいIssueが現行作業を止める阻害要因**でない**限り、現行Issueを中断しない。
   新しいIssueは`registered`のまま置く。
3. 阻害要因である場合だけ、現行Issueを`suspended`へ移し、新しいIssueを唯一の
   `in_progress`にできる。
4. **新しいIssueの登録だけで、現行Issueを自動中断してはならない。**
   中断は`blocks`関係の登録とHumanの裁定を伴う。
5. 元のIssueの再開には、阻害Issueが`resolved`であること、または**Humanの明示的な再開裁定**を
   必須にする。機械が自動で再開しない。

### 1.6 阻害関係の循環を検出し、根本原因へエスカレーションする

`blocks`を有向関係として定義する。`A blocks B`は「Bを進めるにはAの解決が必要」を意味する。

#### 検出と保存の順序

1. 新しい`blocks`関係は、まず**提案関係**として検査する。
   **循環検出の前に、正本の`blocks`へ保存しない。**
2. 自己循環（`A blocks A`）、または既存経路と合わせて循環になる場合、
   正本の`blocks`へは保存せず、`root_cause_escalation_candidate`を作成する。
3. 循環に含まれるIssueをすべて`suspended`へ移し、**作業中Issueを0件にする。**
4. 循環にならない提案関係だけが、正本の`blocks`へ保存される。

#### `root_cause_escalation_candidate`の必須証跡

循環する矢印そのものは正本に残らない。代わりに、**何を提案し、どの経路で循環になり、
どのIssueを止めたか**を残す。次を必須fieldとし、一つでも欠ければ拒否する。

| field | 内容 |
| --- | --- |
| `proposed_blocker_issue_id` | 提案した関係の阻害側 |
| `proposed_blocked_issue_id` | 提案した関係の被阻害側 |
| `cycle_path_issue_ids` | 循環を構成する既存経路のIssue ID列（順序どおり） |
| `cycle_path_relation_ids` | 同じ経路を構成する既存`blocks`関係のID列 |
| `affected_issue_ids` | `suspended`へ移したIssueのID列 |
| `detection_reason` | `blocks_cycle_detected`固定 |
| `input_digest` | 検査に使った入力（既存`blocks`集合と提案関係）のcontent digest |
| `content_digest` | candidate自身のcontent digest |

#### 原子性

candidateの作成と、影響Issueを`suspended`へ移す状態変更は、**同じ検証済み入力から
一単位で成功するか、どちらも書き込まない。**

- candidateだけが残り、Issueが`in_progress`のままである状態を禁止する。
- Issueだけが`suspended`になり、理由のcandidateが無い状態を禁止する。
- 途中失敗を検出したら`cycle_detection_partial_write`で停止し、いずれも書き込まない。

#### candidateの権限

`root_cause_escalation_candidate`は**問題の存在を保存するだけ**である。次のいずれの権限も持たない。

- Issueを作る権限
- Planを作る権限
- Workを開始する権限
- `suspended`のIssueを再開する権限

根本原因Issueへの昇格、優先順位、既存Issueの統合、再開は**Humanの明示的な裁定だけ**が決める。
Humanが根本原因Issueを承認した場合だけ、それを唯一の`in_progress`にできる。

#### 平易に言うと

**循環する矢印を正本に残さず、循環を発見した事実と根拠だけを残す。**
これにより、同じ往復を繰り返さず、誰が何を根本から見直すべきかを判断できる。

「AのためにBが要る、BのためにAが要る」という状態は、一件ずつ直しても終わらない。
依存関係の切り方、設計、方針のいずれかを根本から見直す必要がある、という信号である。
だから機械は往復を止め、作業中を0件にして、Humanの判断へ渡す。

## 2. source universeと抽出規則

### 2.1 固定source

| 項目 | 値 |
| --- | --- |
| source | `records/session-handoffs/2026-08-04-todo-before-compaction-001.md` |
| SHA-256 | `16010a165c010fa8a25cea5ab0f11990734540f4d5c0f5fdb50fd7c21ee6c0f1` |
| 規模 | 900行、85,219 bytes |

このsnapshot一件だけをsource universeとする。他のTODO履歴を混ぜない。
Digestが一致しなければ`intake_source_digest_mismatch`で停止する。

### 2.2 候補にする見出し

| 見出し | 採否 | 理由 |
| --- | --- | --- |
| `### 未実施` | **採用** | 未着手項目そのもの |
| `### 残余risk` | **採用** | 受容したriskで、再確認の対象になり得る |
| `### 手戻り・機械化候補` | **条件付き採用** | §2.3の除外規則を通ったものだけ |
| `## blocker・Human判断待ち` | **採用** | 未解決の判断待ち |
| `### verified` | 除外 | 完了Claimである |
| `### reported_unverified／contradicted` | 除外 | 本文に修復済みと明記されている |
| `## 現在位置`、`## Git・Test`、`## 更新規則` | 除外 | 状態表示であり問題候補ではない |

### 2.3 決定的な除外規則

機械が適用する。規則IDを候補recordへ残す。

| 規則ID | 除外条件 |
| --- | --- |
| `X1` | 見出しが§2.2の除外側にある |
| `X2` | 行が`- Evidence：`、`- 観測した事後状態：`など、親項目の説明である（第2階層以下） |
| `X3` | 本文に「実装済み」「解消した」「訂正した」「完了した」を含み、かつcommit SHAまたはEvidence pathを伴う |
| `X4` | 本文が既存の解決済みIssue（`ISSUE-PILOT-TODO-GROWTH-001`）と同一主題である |
| `X5` | 引用が空、または見出しだけで本文が無い |

X3は「手戻り候補のうち、既に恒久対策commitが記載されているもの」を落とす。
snapshotには`commit f9adef4で実装済み`と明記された項目が複数あり、これらは履歴である。

### 2.4 候補ごとに保存するもの

```json
{
  "record_kind": "historical_todo_intake_candidate",
  "candidate_id": "HTC-0001",
  "source": {
    "relative_path": "records/session-handoffs/2026-08-04-todo-before-compaction-001.md",
    "sha256": "16010a16...",
    "heading_path": ["実施報告照合", "未実施"],
    "start_line": 802,
    "end_line": 802
  },
  "quotation": "<原文の該当行。改変しない>",
  "applied_rules": ["X1:pass", "X2:pass", "X3:pass"],
  "duplicate_suspect": {
    "suspected": false,
    "matched_record_ids": [],
    "basis": "quotation正規化一致およびEvidence path重複なし"
  },
  "human_fields": {
    "unresolved": null, "recurrence": null, "impact": null,
    "priority": null, "promote_to_issue": null
  },
  "content_digest": "..."
}
```

`human_fields`は機械が`null`のまま作る。**機械はここを埋めない。**

### 2.5 重複判定

機械は「疑い」までを出す。判定材料は二つだけとする。

1. 引用を正規化（空白・記号を畳む）した文字列が、既存Issue／候補の`problem`と一致する。
2. 参照するEvidence pathが既存Issue／候補と重なる。

いずれかに該当すれば`duplicate_suspect.suspected: true`とし、該当record IDを列挙する。
**重複と断定しない。**統合または却下はHumanが決める。

## 3. Human判断の境界

| 判断 | 主体 |
| --- | --- |
| 候補の抽出、位置、引用、除外規則の適用 | 機械 |
| 重複の疑いの提示 | 機械 |
| 未解決かどうか | **Human** |
| 再発性 | **Human** |
| 影響 | **Human** |
| priority | **Human** |
| Issueへの昇格 | **Human** |
| 重複の統合・却下 | **Human** |

### 3.1 一括判断してよい条件

次をすべて満たす候補群は、Humanが一括で同じ`disposition`を与えてよい。

- 同一の見出しに属する。
- `duplicate_suspect.suspected`が`false`である。
- 引用に完了Claim（X3の語）を含まない。
- 昇格ではない処置（`defer`、`reject`、`checkpoint`）である。

### 3.2 一件ずつ判断が必要な条件

- Issueへ昇格する（`issue_resolution`）。
- `duplicate_suspect.suspected`が`true`である。
- priorityを付ける。
- 既存Issueへ統合する。

昇格を一括で行わないのは、Issueが作業単位の入口であり、粒度と依存の判断が個別だからである。

## 4. lifecycleとPlanへの接続

### 4.1 経路

```text
historical_todo_intake_candidate（機械）
  → improvement_candidate（Humanが昇格を選んだものだけ）
  → human_triage_decision（Human）
  → issue_record（Human承認後）
  → issue_resolution_plan
  → work（active leafは常に1件）
  → resolution_verdict
```

機械が作るのは最初の`historical_todo_intake_candidate`までである。
そこから先はHumanの`disposition`が無ければ進まない。

### 4.2 TODOへ詳細を再累積させない規則

Issueが増えてもTODOの表示量を増やさない。既存の`todo_projection`設定を引き継ぐ。

| 規則 | 内容 |
| --- | --- |
| 表示単位 | active Issueだけを行として表示する。`maximum_entries` 5を超えない |
| 総量 | `maximum_section_bytes` 1024を超えない |
| 禁止marker | `### 手戻り・機械化候補`、`problem:`、`evidence_refs`、`期待executor`、`実executor`をTODOへ書かない |
| 登録済みIssue | 個別の説明を書かない。**件数の表示も必須にしない** |
| 詳細 | すべてrecord側に置き、TODOはIDと入口だけを示す |

登録が何件あっても、TODOに出るのは`in_progress`の入口だけである。
登録件数を書くかどうかは任意とし、書く場合も一行の数値に留める。
これが「Issueを何件登録してもTODOが再肥大しない」ことの機械的な担保である。

## 5. TDD受入条件

実装前にREDで固定する。

### 正常例

- I1：固定snapshotから複数候補を決定的に抽出できる。同じ入力から同じ候補IDと件数になる。
- I2：既存の解決済みIssue（`ISSUE-PILOT-TODO-GROWTH-001`）と新しい候補が共存できる。
  旧記録を書き換えない。
- I3：**登録済みIssueが何件あっても登録が成功する。**登録数に上限判定を行わない。
- I4：`registered`、`untriaged`、`deferred`、`suspended`のIssueが複数あっても、
  `in_progress`が一件なら有効である。
- I5：**非阻害の新規Issueを登録しても、現行の`in_progress`が中断されない。**
  新規Issueは`registered`のまま置かれる。
- I6：阻害Issueへ切り替えると、旧Issueが`suspended`、新Issueだけが`in_progress`になる。
- I7：阻害Issueが`resolved`になった後、またはHumanの再開裁定があった後だけ、
  `suspended`のIssueを再開できる。
- I8：TODO projectionが`maximum_entries`と`maximum_section_bytes`を超えない。
  登録件数の表示が無くても合格する。
- I9：`pilot_version` 2／3の既存記録が、旧versionの規則で引き続き検証を通る。
  既存IssueへV4の`state`を書き込まない。

### 負例

- J1：`### verified`の完了Claimを候補にすると拒否する（X1）。
- J2：`- Evidence：`行だけを候補にすると拒否する（X2）。
- J3：commit SHA付きで「実装済み」と書かれた行を候補にすると拒否する（X3）。
- J4：source Digestが一致しない → `intake_source_digest_mismatch`。
- J5：既存Issueと同一主題の候補を、`duplicate_suspect`を立てずに登録すると拒否する。
- J6：`human_fields.promote_to_issue`が`null`のままIssueを作ろうとすると拒否する
  （Human裁定なしの自動Issue化）。
- J7：**二件目の`in_progress`を開始しようとすると拒否する。**
- J8：`maximum_active_leaves`を超えてWork Itemを開始しようとすると拒否する。
- J9：**新規Issueの登録だけで現行Issueを`suspended`にしようとすると拒否する。**
  中断は`blocks`関係とHumanの裁定を伴う。
- J10：**自己循環（`A blocks A`）を拒否する。**提案関係を正本の`blocks`へ保存しない。
- J11：**二Issue以上の`blocks`循環（`A → B → A`）を拒否する。**循環する関係を正本へ保存せず、
  循環に含まれるIssueを`suspended`にして作業中Issueを0件にする。機械が相互に再開しない。
- J12：`root_cause_escalation_candidate`が`proposed_blocker_issue_id`、
  `proposed_blocked_issue_id`、`cycle_path_issue_ids`、`cycle_path_relation_ids`、
  `affected_issue_ids`、`detection_reason`、`input_digest`、`content_digest`の
  **いずれかを欠くと拒否する。**
- J13：**candidate作成と影響Issueの`suspended`化の一方だけが成功する状態を拒否する。**
  片方だけの書込みを検出したら`cycle_detection_partial_write`で停止し、いずれも書き込まない。
- J14：**candidateだけではIssue化、Plan化、Work開始、既存Issueの再開ができない。**
  Human裁定なしにこれらを行おうとすると拒否する。
- J15：**根本原因Issueの`resolved`またはHumanの裁定なしに、循環に含まれたIssueを再開しようと
  すると拒否する。**
- J16：TODOへ禁止markerを書き込もうとすると拒否する。

## 6. 段階的実施計画

| # | 単位 | 停止条件 | Human承認 |
| --- | --- | --- | --- |
| 1 | 本設計の承認、§8の判断 | — | **必要** |
| 2 | **I1〜I9、J1〜J16の全件**をREDで固定 | 既存testを弱める必要が生じたら停止 | 不要 |
| 3 | `pilot_version` 4のschema／config／validator実装（state、`blocks`、循環検出を含む） | 旧versionの検証が壊れたら停止 | 不要 |
| 4 | GREEN。**このとき§0の失敗も解消する** | 一件でも失敗したら停止 | 不要 |
| 5 | 固定snapshotから候補一覧を機械生成し、Humanへ提示 | 候補0件、またはDigest不一致なら停止 | 不要（提示で停止） |
| 6 | Human triage（一括／個別） | 一件でも`human_fields`が未記入なら停止 | **必要** |
| 7 | 昇格を選んだ候補だけをIssue化 | `promote_to_issue`が真でないものを含めたら停止 | **必要** |
| 8 | Plan化と着手 | `in_progress`が1件を超えたら停止。`blocks`循環を検出したら作業中0件で停止 | 不要 |
| 9 | 循環検出時の根本原因Issueの承認 | Human裁定が無ければ再開しない | **必要** |

単位2でREDにするのは全件である。中断規則（J9）、二件目の作業開始拒否（J7）、自己循環（J10）、
複数Issue循環（J11）、循環candidateの証跡欠落（J12）、原子性違反（J13）、Human裁定なしの昇格（J14）、循環中Issueの無断再開（J15）を、
**実装前のREDから検証する。**これらを後回しにすると、実装後に「動くから正しい」と誤認しやすい。

単位4で§0の失敗が解消する理由は、v4のvalidatorが候補file数ではなく
「未triage候補の滞留」を見る形へ変わるためである。testを緩めるのではなく、
**検査の対象を、契約に合った不変条件へ置き換える。**

単位3までは、既存の`ic-historical-todo-issue-intake-001--v1.json`をどう扱うかで
一時的に失敗が残る。これは§8の判断1に依存する。

## 7. 本設計に含めない範囲

- 過去TODO以外の履歴（session log、旧Evidence、commit message）からの抽出
- Issueの自動分類、priority自動判定、LLMによる要約
- 複数Work Itemの並行実行
- Issue Resolutionの正式schemaとpermit（Deferred Workのまま）
- 既存Issue、Plan、Verdictの再判定
- `blocks`循環の自動解決。機械は検出と停止までを行い、解き方はHumanが決める

## 8. Human判断が必要な点

1. **§0の失敗をどう解消するか。**
   単位4まで失敗を残したまま進めるか、それとも先に候補recordを一時退避して
   GREENへ戻してから進めるか。設計者の推奨は前者（v4導入で正しく解消する）である。
   ただし、その間は全testがGREENでないため、他作業のcommit境界に影響する。
2. **候補IDの体系。**`HTC-0001`形式でよいか。既存の`IC-`とは別体系にするか。
3. **`state`導入に伴う`issue_record`の`schema_version` 2化。**既存Issueを version 1のまま
   保持し、V4のstateを遡及適用しない方針でよいか。

登録済みIssue数の上限は、Humanの決定により**設けない**。判断事項から外した。

## 9. 本提案で行っていないこと

- config、validator、test、既存Issue、TODO、Plan、checklist、Requirementの変更
- 圧縮前TODOからのIssue自動昇格、候補recordの生成
- Decision record、code、testの作成
- LLM、外部送信、外部`DATA_ROOT`、push、PR、CI、Work 4B、Work 6A、後続評価E2以降
