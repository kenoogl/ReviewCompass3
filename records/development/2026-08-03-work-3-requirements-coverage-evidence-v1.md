---
evidence_id: RC3-WORK3-REQUIREMENTS-COVERAGE-EVIDENCE-2026-08-03-V1
recorded_at: 2026-08-03T17:19:38+09:00
stage: initial-development
work: Work 3
status: verified_candidate
workflow_state: human_decision_pending
completion_authority: human
confidentiality_class: project-internal
---

# Work 3 Requirements Coverage Candidate Evidence V1

## 1. 結果

既存37 Requirementを`preserve | adapt | replace | defer`へ1行ずつ分類し、owner、successor、追加13要件との
関係、旧Acceptance Test、後継test、停止・復旧・受入義務の継承内容を一つの構造化候補へ固定した。
37 IDの欠落・重複は0、既存継承表との分類不一致は0、追加13要件からの逆引き未被覆は0である。

本成果はHuman判断候補であり、Requirements本文または現行Plan本文を変更せず、Work 3先頭checkboxも
Human承認前は未完了のままとする。

## 2. 候補

| artifact | SHA-256／state |
|---|---|
| `records/development/2026-08-03-work-3-requirements-coverage-candidate-v1.json` | `c529e1495a8ea5a84ac15ae651299a410f6aba627ee115b395a5940aa209cb7e`／`human_decision_candidate` |
| `records/development/2026-08-03-work-3-requirements-baseline-evidence-v1.md` | `7fdc24c8063292871761af3c888824f3e3c715689df3a3924c28c7856f9c5a20`／`verified_baseline` |

候補は固定source 5件のpathとDigestへ束縛した。再計算時のDigest不一致は0だった。

## 3. 分類結果

| disposition | 件数 | 意味 |
|---|---:|---|
| `preserve` | 15 | 既存ID、owner、停止、復旧、受入、対象外を維持する |
| `adapt` | 20 | 既存IDと安全義務を維持し、追加13要件のidentityまたはcontrol関係を後継versionへ加える |
| `replace` | 2 | 旧Requirementを履歴として保持し、旧negative behaviorを後継Requirement／testへ移す |
| `defer` | 0 | 既存37 Requirement自体は初期scopeから外さない |

`replace`は`REQ-CONTEXT-001`と`REQ-IMPROVE-002`である。前者は7項目Task authorityを
`REQ-CONTRACT-001`へ移し、後者は直接的なWorkflow設定変更を版付きImprovement Proposalと通常ownerの
revision pathへ置換する。どちらも旧停止条件とnegative acceptanceを削除しない。

## 4. 順逆被覆

### 4.1 既存37 Requirementからの順方向

- 37行、unique Requirement ID 37件。
- 既存構造化recordの37 IDに対する欠落0、余剰0。
- owner不一致0。
- 全行にsuccessor、追加Requirement relation、旧test、後継test、coverage noteがある。
- 既存Acceptance Test継承表の37行とdisposition、旧test、後継testが全件一致する。

### 4.2 追加13 Requirementからの逆方向

次の13 IDはすべて1件以上の既存Requirement行から逆引きできる。

```text
REQ-CONTRACT-001 .. REQ-CONTRACT-008: 8 / 8
REQ-WORKFLOW-005 .. REQ-WORKFLOW-009: 5 / 5
reverse missing: 0
reverse extra: 0
```

`REQ-WORKFLOW-010`と`011`は手作業Pilot後の候補であり、現行13件へ混入していない。

## 5. 独立監査と訂正

初回の構造監査は、`REQ-TRACE-004`の`legacy_acceptance_test`が
`AT-TC-TRACE-004`となっている参照転記ミスを1件検出した。正しい旧ID`AT-TRACE-004`へ訂正し、同じ
監査を再実行した。

```text
rows 37 unique 37
dispositions {'adapt': 20, 'preserve': 15, 'replace': 2}
inheritance_rows 37
reverse_covered 13 of 13
errors []
matrix_audit: passed
```

この訂正はRequirementの意味分類、owner、successorまたは追加13要件との関係を変更していない。

## 6. Authorityと判断対象

- 候補は`proposed_only`であり、Human DecisionなしにRequirements authorityを変更しない。
- 現行Planと追加13要件の`provisional / review-candidate`状態を維持する。
- 承認対象は候補Digestに固定した37行のdisposition、successor、関連追加要件、義務継承である。
- 承認はRequirements本文改定、Work 3後続項目完了、Design着手、commitまたはpushを含まない。

Human判断候補は次の二択とする。

1. 現行候補を承認し、Work 3先頭項目を`verified / completed`とする。
2. 変更が必要なRequirement IDと修正内容を指定する。

