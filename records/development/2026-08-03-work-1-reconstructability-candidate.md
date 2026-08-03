---
candidate_id: IC-WORK1-DOC-RECONSTRUCTABILITY-001
observed_at: 2026-08-03
origin_stage: initial-development
origin_work: Work 1
candidate_kind: improvement_candidate
status: triage_required
suggested_route: pause_and_triage
confidentiality_class: project-internal
---

# Work 1 documentation reconstructability改善候補

## 1. 観測

`records/task-contract/task-contract-centered-documentation-v16.json`は、recordとmanifest対象を
同一commitへ固定し、後続revision前に全Digestを照合するforward ruleを持つ。ところが、同recordの
現行内容を含むcommit `e603804d4853f29c1ebeb97ef82774447211ff05`を再検証すると、manifest対象
18件のうち5件が記録Digestと一致しない。

再現command：

```sh
work1_snapshot=e603804d4853f29c1ebeb97ef82774447211ff05
while IFS=$'\t' read -r work1_path work1_expected; do
  work1_actual=$(git show "${work1_snapshot}:${work1_path}" | sha256sum | cut -d' ' -f1)
  if [ "$work1_actual" != "$work1_expected" ]; then
    echo "MISMATCH expected=$work1_expected actual=$work1_actual $work1_path"
  fi
done < <(jq -r '.artifacts[] | [.path, .sha256] | @tsv' \
  records/task-contract/task-contract-centered-documentation-v16.json)
```

観測結果：

| path | v16記録Digest | `e603804`の実Digest |
|---|---|---|
| `README.md` | `8bdcd33d1cc4091353e2bc7edf29544d495e2c8fef5c63f004c8e886136eaf8b` | `529a344aa61bb11c8bf48f452b2af5c9b8c31b7af88843d47a9fd1f729a4fc8f` |
| `docs/README.md` | `0c115beb2822fb635195be60c3a90c2d5c4ae20dd88bc8719c31dd7a435ab28d` | `639164d691fababd6238e7e5ba5c2d9824ab76e58478167a0f4280e20e4ea8c3` |
| `docs/current/reviewcompass3-intent-current.md` | `307bdbcc39d028064ea3ed715ccac38fb68760ac1e8a13b46d4caf3803c11c59` | `1950f5a37fb5d0d0554f56343b39bbca7fc635523409f10ee761d8cef68f9ec6` |
| `docs/current/reviewcompass3-plan-current.md` | `b5d11aa184d56cbb075f9fb7aea53cabfac14185dcd35442f954bba9e74705de` | `9c7d54aaa19c9146f751921e5cca962a1b6c151adc130afc5d009f9766f2603b` |
| `docs/design/2026-08-02-task-contract-design-amendment.md` | `42e46a6b390c842257496cc0fc329c7a90c060ee0b82f4f21612a37b52c0ab04` | `55115696a3a33612fa52d7fab59dddccb2045ef6baba982a4b5fe17437b25eda` |

`records/task-contract/2026-08-02-documentation-reconstructability-audit.json`はv1〜v15を監査対象とし、
v16以降のforward ruleを定めるが、このv16不一致自体は監査対象に含まれない。v16の現行recordも
`content-present-pending-git-commit`のままであり、post-commit照合済みとは記録されていない。

## 2. 分類と影響

```yaml
classification_candidates:
  - process_improvement
  - contract_defect
affected_authority:
  - documentation revision provenance
  - current Intent and Plan source reconstruction
acceptance_truth_changed: unknown
safety_or_security_impact: false
authority_impact: true
provenance_reconstructability_impact: true
source_test_verdict_identity_impact: true
current_work_can_continue: false
suggested_route: pause_and_triage
route_reason: 必須Provenanceと固定source identityへ影響し、現行Workの固定入力完了判断に使用できないため
```

現行Intent、用語集、計画の現在内容とchecklist記載Digestは一致しているため、現行文書の内容同一性が
直ちに失われたわけではない。一方、v16が主張したrevision snapshotは再構築できず、過去revisionから
現行候補へのProvenanceを完全と扱えない。このため、Work 1の通常完了とWork 1Aへの進行を停止する。

## 3. 提案する修復経路

1. v16を上書きせず、v16が`git-reconstructable`にならなかった事実をcorrective successor recordへ
   記録する。
2. 現行authority、source catalog、baseline、修復recordを一つの明示したChange Setとして固定する。
3. 固定commitからmanifest全件を再読込し、Digest一致をpost-commit Evidenceへ記録する。
4. Humanが、修復後のProvenanceでWork 1を再開するか、digest-onlyの残余riskを受容するか判断する。
5. 再開時はWork 1 Evidenceを新versionで作成し、旧blocked Evidenceを上書きしない。

本候補は修復案であり、現行Plan、Task Contract、Testまたは受入基準を変更しない。commit作成と
残余risk受容は本記録だけでは許可しない。

## 4. Human判断待ち

- 判断対象：corrective successor recordと同一commit固定による修復を開始するか。
- 既定提案：修復を開始し、固定commitのpost-commit照合後にWork 1を再開する。
- 代替：digest-onlyの残余riskを明示的に受容し、適用範囲と期限をDecisionへ固定する。
- 再開条件：上記いずれかのHuman判断がEvidenceとして固定されている。
