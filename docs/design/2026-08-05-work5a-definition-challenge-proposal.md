# Work 5A 最小Definition Challenge設計提案

状態：`awaiting_human_approval`
改訂：第四版（compile後の`plan_bundle`をcompile前のDefinition Challenge入力にする循環を訂正）
対象：既に受理済みの最初の文書Review Task Contract version 1を後継する
draft version 2（`TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V2`）
基準文書：`docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md`（§2、§7、§8）
Requirement：`records/requirements/definitions/req-contract-004--v1.json`（`REQ-CONTRACT-004`）ほか、
Work 5Aが直接束縛する16件
承認記録（予定）：`DEC-WORK5A-DEFINITION-CHALLENGE-001`

**これはDecision recordではない。**承認までContract version 2、実装、test、実Runを
作成・実行しない。汎用Challenge frameworkを作らない。対象は後継する一Contract versionだけである。

## 1. 三つの検査の違い

`REQ-CONTRACT-004`は「Contract Conformance Review、Definition Challenge、Final Contract Challengeを、
目的、材料、Finding、完了条件を混同せず実行できなければならない」と定める。
今回の最小sliceでは次のとおり固定する。

| 観点 | Definition Challenge | Conformance | Final Challenge |
| --- | --- | --- | --- |
| 何を見るか | **Contractの定義**が要件を取りこぼしていないか、境界が狭すぎないか、禁止操作と依存を忘れていないか | 成果がContractの義務を満たすか | 成果がContract適合でも上位の目的を損なわないか |
| 実施時点 | **Contract確定前**。compileより前 | 成果（Finding集合）の後 | Conformanceの後 |
| 入力 | Requirement definition、draft Contract、開発方針、Current Plan、固定material set | challengedかつapprovedなContract、Plan bundle、Finding集合 | Contract、Conformance verdict、Finding集合 |
| 対象の単位 | Contract version | 成果候補または成果version | 成果version |
| 出力 | `definition_challenge_verdict` | `conformance_verdict` | `final_challenge_verdict` |
| Findingの性質 | 定義の欠落・過小・禁止漏れ | 義務の未充足 | 上位目的との齟齬 |
| 完了条件 | blocking Findingが0件 | `error` Findingが0件 | Conformance通過かつ上位目的を損なわない |
| 失敗時 | Contractを新versionへ。compileへ進まない | 成果を直して再実行 | Contract versionの見直し |

Current Planは「常に別Runを要求しない。low riskでは一つのRunから別identityのVerdictを生成できる」と
定める。本Contractはlow risk（文書一件、外部side effectなし）であるため、独立した実行主体による
別Runは強制しない。ただしDefinition Challengeはcompile前の別lifecycle stepとし、verdictのidentityと
ownerをConformance、Final Challenge、Human decisionから分ける。

## 2. 固定材料と不足材料

### 2.1 使える材料

| 材料 | 役割 | Digest固定 |
| --- | --- | --- |
| Work 4設計提案§2、§7、§8 | Contractの定義、束縛16 Requirement、既存受入条件 | file SHA-256 |
| `records/requirements/definitions/`の16 file（`req-contract-004--v1.json`を含む） | 各Requirementの本文 | material setに各file SHA-256を保持 |
| draft `review_task_contract` version 2 | 検査対象そのもの | `content_digest` |
| `docs/development/2026-08-02-development-policy.md` | LLMと機械処理の責務分離、Human判断必須操作 | file SHA-256 |
| `docs/current/reviewcompass3-plan-current.md` | Work 5A／6A境界、Definition Challengeの検査観点 | file SHA-256 |

材料は`definition_challenge_material_set`としてまとめ、各fileのpathとDigestを固定する。
Contractのdigestは`record_ref`で持つ。

### 2.2 不足材料と、そのためにできない検査

Current Plan 551行はDefinition Challengeの固定材料として
「source Requirements、**Architecture Policy**、**risk catalog**、**隣接Contract**」を挙げる。
このうち後三者は、この最小sliceでは**実在しない**。推測で新設しない。

| 不足材料 | 実在状況 | できない検査 |
| --- | --- | --- |
| Architecture Policy | `docs/design/`に該当文書なし | 設計方針との齟齬、層・依存方向の違反の検査 |
| risk catalog | 該当record・policyなし | risk等級に応じた独立reviewer要否、Human gate要否の判定 |
| 隣接Contract | Task Contractは`records/task-contract/`に21件あるが、いずれもWork 5AのReview Contractと同じ運用面に無い。`.reviewcompass/contracts/`は`.gitkeep`のみでContract recordが無い | cross-contract責務の重複・隙間の検査 |
| Challenge Policy | 実在しない | 検査項目・閾値の外部固定。今回は本提案で直接固定する |

したがって本提案の検査規則は、**Requirement、draft Contract、開発方針、Current Planから
決定的に導ける範囲に限る。**上記4種の検査は行わず、Work 6Aまたは後続へ送る（§7）。

材料が一件でも欠ける、またはDigestが一致しない場合は`definition_material_missing`で停止し、
verdictを発行しない。

## 3. 最小の決定的検査規則

すべてLLMを使わず、固定入力から同じ結果を再生成できる形にする。

| # | 検査 | 判定 | 停止code |
| --- | --- | --- | --- |
| D1 | 束縛16 Requirementのすべてに、Contract側の受け先がある | `requirement_receivers`が16 IDと完全一致し、各値が10節の実在する非空fieldを指す | `definition_requirement_unreceived` |
| D2 | Contractの10節（identity、responsibility、boundary、preconditions、context obligations、allowed capabilities、expected output、acceptance、provenance obligations、escalation）が空でない | 10節すべて非空、かつAcceptanceとProvenanceがDefinition Challengeを必須stepとする | `definition_section_missing` |
| D3 | 対象が`docs/`配下の一文書だけである | `boundary.target_paths`が1件かつ`docs/`始まり | `definition_scope_violation` |
| D4 | 禁止能力が明示的に偽である。LLM呼出、外部送信、成果物書込み、Git write | 4項目すべて`false` | `definition_forbidden_capability` |
| D5 | 四つのreview判断のownerがContractでcompile前に固定されている | `review_owners`のDefinition Challenge、Conformance、Final Challenge、Human decisionが非空でpairwise distinct | `definition_owner_separation` |
| D6 | Deferred 34 Requirementを直接受理していない | Contractの`requirement_ids`が束縛16件と完全一致 | `definition_deferred_requirement_accepted` |
| D7 | 材料が揃い、各Digestが実fileと一致する | 全材料一致 | `definition_material_missing` |
| D8 | Definition Challengeがcompile後または成果側の入力を使っていない | material setにPlan bundle、compile verdict、Finding集合、Conformance／Final Challenge verdictが無い | `definition_stage_confusion` |

D1の`requirement_receivers`とD5の`review_owners`はversion 2のContractが新しく持つfieldである。
実装module内の定数やcompile後のPlan bundleをContract側の宣言の代わりに使わない。

D6は「34件のdeferred Requirementを、Contractが黙って受け入れていないか」を見る。
Contractの`requirement_ids`に16件以外が現れた場合、Requirement authorityの解釈が広がっている。
これは意味の変化であり、Definition Challengeで止める。

D8は`REQ-CONTRACT-004`の「混同せず実行」を機械的に担保する。Definition Challengeの入力に
compile後の計画または成果側のrecordが混ざっていれば停止する。

## 4. Findingとverdictの最小schema

### 4.1 Finding

```json
{
  "finding_id": "DF-001-D1",
  "check_id": "D1",
  "severity": "blocking",
  "target_ref": { "record_kind": "review_task_contract", "record_id": "...", "content_digest": "..." },
  "requirement_ref": "REQ-CONTRACT-001",
  "description": "束縛RequirementにContract側の受け先が無い。"
}
```

`severity`は`blocking`と`nonblocking`の二値とする。既存Findingの
`error`／`warning`／`info`とは別語彙にする。**段の混同を語彙のうえでも防ぐ**ためである。

分類根拠は次のとおり固定する。

| 分類 | 根拠 | 該当検査 |
| --- | --- | --- |
| `blocking` | Contractの定義が成立していない。compileへ進めば誤った成果が正当化される | D1〜D8 |
| `nonblocking` | 定義は成立するが、後続で確認したい観測 | 現時点では該当なし。将来の追加検査用に語彙だけ用意する |

現時点でD1〜D8はすべて`blocking`である。`nonblocking`の実例を無理に作らない。

### 4.2 verdict

```json
{
  "record_kind": "definition_challenge_verdict",
  "record_id": "DCV-<contract id>",
  "record_version": 1,
  "owner": "definition_challenge_owner",
  "status": "passed",
  "contract_ref": { "...": "record_ref" },
  "material_set_ref": { "...": "record_ref" },
  "checks": ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"],
  "findings": [],
  "blocking_count": 0,
  "content_digest": "..."
}
```

`status`は`passed`と`failed`だけとする。`blocking_count`が1以上なら必ず`failed`とする。

### 4.3 blocking Findingがある場合の経路

```text
definition_challenge_verdict: failed
  → compileへ進まない（Plan bundleを作らない）
  → Review Runを開始しない
  → accepted artifactを作らない
```

`compile_contract`は、`definition_challenge_verdict`が`passed`でなければ
`not_compilable`を返す。`accept_artifact`は`provenance_verdict`の`verified_nodes`に
`definition_challenge_verdict`が含まれることを要求する。
これにより、blocking Findingがあるとaccepted artifactへ到達できない。

### 4.4 来歴への追加

`provenance_verdict`のnode列へ`definition_challenge_verdict`を加える。
位置は`review_task_contract`の直後、`compile_verdict`の前とする。

```text
requirement_binding → review_task_contract → definition_challenge_verdict → compile_verdict
→ context_manifest → workflow_permit → finding_set → conformance_verdict
→ final_challenge_verdict → human_decision
```

node 10件、edge 9件になる。自己辺を作らない規則は変えない。
これは後継Contract version 2の新しいRunが作る来歴形式である。既存Contract version 1の
`provenance_verdict` version 2を上書きせず、新しいrecord identityとversionでnew-only作成する。

## 5. TDD受入条件

実装前にREDで固定する。

### 正常例

- G1：材料が揃った正しいdraft Contract version 2で`passed`、`blocking_count`が0、`findings`が空になる。
- G2：`definition_challenge_verdict`が`passed`のときだけ`compile_contract`が`compiled`を返す。
- G3：来歴のnodeが10件、edgeが9件になり、自己辺が無い。
- G4：Contract version 2の`review_owners`で四者がpairwise distinctである。

### 負例

- H1：束縛16 Requirementの一件に受け先が無い → `definition_requirement_unreceived`、`failed`。
- H2：Contractの10節のいずれかが空 → `definition_section_missing`。
- H3：`target_paths`が2件、または`docs/`外 → `definition_scope_violation`。
- H4：`call_llm`、`external_transmission`、`write_artifact`、`git_write`のいずれかが`true`
  → `definition_forbidden_capability`。
- H5：Contract version 2の`review_owners`で二者以上が同一owner → `definition_owner_separation`。
- H6：Contractの`requirement_ids`にdeferred Requirementが混入 → `definition_deferred_requirement_accepted`。
- H7：材料file欠落、またはDigest不一致 → `definition_material_missing`。
- H8：Definition Challengeのmaterial setへ`plan_bundle`、`compile_verdict`、`finding_set`、
  `conformance_verdict`または`final_challenge_verdict`を入れる → `definition_stage_confusion`。
- H9：`failed`のverdictで`compile_contract`を呼ぶ → `not_compilable`。
- H10：`definition_challenge_verdict`を欠いた来歴 → `provenance_node_missing`。
- H11：`failed`のverdictから`accepted_artifact`を作れない。

H8は「Definition ChallengeとFinal Challengeの混同」を直接扱う負例である。
`REQ-CONTRACT-004`の要求に対応する。

## 6. 既存recordとの接続と初回実Run

### 6.1 version 1とversion 2の関係

既存の`records/development/2026-08-05-work5a-first-real-review-acceptance-v2-records.json`は、
Contract version 1の当時の有効な9 node構成を保持している。これを上書き、無効化、後付け変更しない。

Definition Challengeを必須にするため、同じ責務、対象文書、束縛16 Requirementを持つdraft
Contract version 2をnew-onlyで作る。version 2は次だけをversion 1から変える。

- `requirement_receivers`で束縛16 RequirementとContract内の受け先を明示する。
- `review_owners`でDefinition Challenge、Conformance、Final Challenge、Human decisionのownerを明示する。
- Acceptance、Provenance obligations、EscalationへDefinition Challengeの通過、位置、失敗routeを追加する。
- version 1への`supersedes`参照を持つ。

version 2の作成はversion 1の既存accepted artifactをstaleまたは誤りにしない。version 2が完了した後の
運用上の関係は、version 1を履歴として有効に保持しつつ`superseded_by_v2`と記録する案を推奨し、
§8のHuman判断とする。

### 6.2 初回実Runの手順

1. 束縛16 Requirementと後継関係を保持するdraft Contract version 2をnew-onlyで作る。
2. 材料set（§2.1）を作り、各fileとrecordのDigestを固定する。
3. compileやPlan bundle生成を行わず、D1〜D8を実行する。
4. verdictを`records/development/`へnew-onlyで保存する。
5. 結果（`passed`／`failed`、Finding件数）をHumanへ提示する。
6. `passed`の場合だけHumanにContract version 2の承認を求め、承認後にcompileと新しいReview Runへ進む。

Definition Challenge実Run自体は実際の`docs/`配下の対象文書を再度reviewしない。
Definition ChallengeはContract定義の検査であり、成果の再評価ではない。ただしversion 2の承認後は、
そのContractに対するcompile、Review Run、Conformance、Final Challenge、Human decision、Provenanceを新しい
record identityで実行し、version 1の成果をversion 2の成果として流用しない。

### 6.3 循環のない正常経路

```text
Requirement definition / binding → draft Contract v2 → material set
→ Definition Challenge verdict → Human Contract approval → compile / Plan bundle
→ Context Manifest → Workflow permit → Finding set → Conformance
→ Final Challenge → Human review acceptance → Provenance → accepted artifact
```

## 7. Work 6Aへ送る範囲

今回の最小Definition Challengeに含めず、Work 6Aまたは後続で扱う。

| 項目 | 理由 |
| --- | --- |
| Architecture Policyとの齟齬検査 | 材料が実在しない（§2.2） |
| risk catalogによる独立reviewer・Human gate要否の判定 | 同上。Current Plan 557行の`low/medium/high`分岐は、riskの正本が無いと機械化できない |
| 隣接Contractとのcross-contract責務検査 | 同上 |
| 「Requirementを欠くContract fixtureを実行前に検出」の網羅版 | 今回はD1で束縛16件だけを見る。Requirement authority全体の被覆はWork 6Aの負例catalog |
| `nonblocking` Findingの実運用 | 現時点で実例が無い。語彙だけ用意する |
| 複数Contract、複数version間のDefinition Challenge比較 | 対象が一Contractのため |
| Definition Challengeの独立Run強制（high risk時） | risk catalogが無いため判定できない |

## 8. Human判断が必要な点

意味・authority・scopeに関わる二点だけである。

1. **Contract version 1とversion 2の関係。**
   version 1のaccepted artifactを履歴として有効に保持し、version 2完了後に
   `superseded_by_v2`をnew-onlyで記録するか、両方を現行として並存させるか。
   設計者の推奨は前者であり、version 1を無効化またはstaleにしない。
2. **Definition Challengeのownerを誰にするか。**
   `REQ-CONTRACT-004`は三段の分離を求めるが、Humanが四つ目のownerを兼ねてよいかは
   意味の判断である。設計者の推奨は、Conformance・Final Challenge・Human decisionのいずれとも
   異なる論理ownerとし、実行主体は機械（deterministic）とすることである。

## 9. 実施単位の分割

| # | 単位 | 停止条件 | Human承認 |
| --- | --- | --- | --- |
| 1 | 本設計の承認 | — | **必要**（§8の二点を含む） |
| 2 | Contract version 2とG1〜G4、H1〜H11のRED固定 | 既存38件を弱める必要が生じたら停止 | 不要 |
| 3 | `definition_challenge_verdict`の実装と`compile_contract`の事前gate接続 | 設計を満たせない矛盾が出たら停止 | 不要 |
| 4 | GREEN、既存38件、全test | 一件でも失敗したら停止 | 不要 |
| 5 | 初回Definition Challenge実Run、結果の提示 | `failed`ならContractを訂正。`passed`でもContract承認前に停止 | **必要（Contract version 2の承認）** |
| 6 | version 2のcompile、新Review Run、来歴・受理recordの作成 | §8-1が未確定なら停止 | 承認後の承認範囲内 |
| 7 | 独立検証 | — | 不要 |

既存Contract version 1の9 node形式は読めるまま保持する。H10は後継Contract version 2の
新しいRunにだけ適用し、version 1の既存recordを拒否fixtureに使わない。

## 10. 本提案で行っていないこと

- `tools/task_contract/`、`tests/`、`TODO_NEXT_SESSION.md`、Current Plan、checklist、Requirementの変更
- Challenge Policy、risk catalog、Requirement、Contractの新設
- 実装、test、実Run、Decision record
- LLM、外部送信、外部`DATA_ROOT`、push、PR、CI、Work 4B、Work 6A、後続評価E2以降
