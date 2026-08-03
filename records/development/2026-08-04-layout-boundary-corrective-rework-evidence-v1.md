---
record_id: RC3-LAYOUT-BOUNDARY-CORRECTIVE-REWORK-EVIDENCE-2026-08-04-V1
recorded_at: 2026-08-04T06:30:00+09:00
status: recorded
---

# Layout境界correctiveの手戻りEvidence V1

## 1. Test実行入口

- 事象：最初の対象Test実行で`.venv/bin/python3`を指定し、fileが存在しないためTest開始前に停止した。
- 原因：利用可能なrunnerを機械照合する前に、LLMが別workspaceで使われたpathを選んだ。
- 期待executor：版付きTest policyからPythonとcommandを解決するmachine。
- 実executor：LLMによるpath選択。
- 対処：`command -v python3`、version、pytest importを確認し、最終検証は既存の
  `tools.development.policy_test_runner`から実行した。
- 影響：成果物なし。RED取得前のTest実行が1回増えた。
- route：`manual_rework_candidate / resolved_by_existing_policy_test_runner`。今後は最初からpolicy runnerを使う。

## 2. compile cache

- 事象：`python3 -m py_compile`がworkspace外のmacOS Python cache作成を拒否され停止した。
- 原因：Python既定cacheとsandbox write境界の不一致。
- 期待executor／実executor：ともにmachine。手作業による原因ではない。
- 対処：task専用`PYTHONPYCACHEPREFIX`を`/private/tmp`配下へ指定し、同じcompileを合格させた。
- 影響：成果物なし。compile確認が1回増えた。
- route：`machine_environment_mismatch / resolved_by_task_scoped_cache`。共通compile runnerでcacheを固定する候補を維持する。

## 3. TODO patch anchor

- 事象：TODOの複数節を一括更新するpatchで、既存Decision Digestを一文字誤記し、適用前検査が停止した。
- 原因：LLMが長いexact anchorとDigestを手入力した。
- 期待executor：見出しidentityと実file内容から更新対象を解決し、Digestをartifactから取得するmachine。
- 実executor：LLMによるpatch文字列の直接組立て。
- 対処：失敗したpatchではfileが変更されていないことを確認し、該当節を再読込して見出し単位のpatchへ分けた。
- 影響：TODOの誤変更なし。一括patch試行が1回増えた。
- 再発性：現行TODOにも同種のexact anchor失敗が既知候補として記録されており、再発に該当する。
- route：`manual_rework_candidate / improvement_candidate_pending_workflow_root_approval`。Layout v2承認後、構造化TODO updaterまたは見出しlocatorの独立候補として耐久routeする。現在の一件限定Issue Pilotへ自動昇格しない。

## 4. commit分割用部分stage

- 事象：commit handoff対策とLayout／Pilot対策を分割するため、TODOの一部だけをstageするpatchをLLMが
  組み立てたが、`git apply --cached --check`がhunk count不整合を検出して拒否した。
- 原因：複数の意味変更とDigest更新が同じTODO／checklistへ入った状態で、LLMがunified diffの行数を手入力した。
- 期待executor：意味単位と参照閉包からstaged treeを生成・検証するmachine。
- 実executor：LLMによるpartial-stage patchの直接組立て。
- 対処：失敗patchがindexを変更していないことを確認した。TODOとchecklistの参照閉包を分離すると中間commitが
  不整合になるため、分割を中止し、TestとEvidenceが一致する現在stateを一つのcommit境界とした。
- 影響：managed fileの内容変更なし。部分stage検討が一回増えた。
- route：`manual_operation_candidate / resolved_by_atomic_consistent_commit`。今後、同一fileを跨ぐ分割が必要な場合は
  staged treeのTestと参照閉包を機械生成できる場合だけ実施する。

## 5. 結果

- 3件ともmanaged成果物の誤内容、Test failureまたはauthority変更を残していない。
- 手作業因果がある1件と3件は機械処理候補、2件はmachine環境不一致として区別した。
- Issue昇格は行っていない。Human Triage DecisionなしにIssue Recordへ変換しない。
