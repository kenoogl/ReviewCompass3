# Work 7A第2項 checkout relocation 前駆slice 独立レビュー結果 v1

- review date：2026-08-09
- Pilot：Claude
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- risk：`high`（妥当）
- verdict：`report_execution_mismatch`

## 1. 対象

- review request：
  `records/session-handoffs/2026-08-09-claude-pilot-work7a-checkout-relocation-review-request-v1.md`
- review request SHA-256：`d759e59c5388b80ed6d009e6c84ca585dce63e79023be540b4e34848a87a1932`
- review request commit：`6167fb64fba9661bfd6200342a21b19e0fee8d28`
- 有効scope：
  `records/session-handoffs/2026-08-09-claude-pilot-work7a-checkout-relocation-scope-v2.md`
- scope SHA-256：`f127351d05bc621af95a042506dc726790ca59ecc928cec4c34257ee23d473a8`
- 条件付き承認：
  `records/session-handoffs/2026-08-09-codex-scope-reevaluation-work7a-checkout-relocation-v1.md`
- review対象commit列：RED `a7e58eb2f212c78e2c62e95947718fcf4da3ad9f`、
  GREEN `86f0f63cb24feda35de740f835a04b8c0782eb68`、review request `6167fb64...`

review開始時worktreeはclean。scope固定入力22件、成果物4件、scope、再評価recordのSHA-256は全件
再計算値と一致した。REDはTest 1件だけ、GREENは許可された実装・Evidence・receipt 3件だけ、
review requestは依頼書1件だけを追加している。RED後にTestが変更されていないことと、RED parentに
実装moduleが存在しないこともGitから確認した。

## 2. 上流から独立導出した受入条件

Work 3承認authorityとWork 7A authorityから、PilotのTestを使わず次を導出した。

1. Source Snapshotは、実際のbase、現在HEAD、index、tracked／staged／dirty、対象untracked、manifestを
   一つのidentityとして捕捉する。commit SHAだけでdirtyまたは部分選択worktreeを表したことにしない。
2. Change Setは固定したbase Snapshotとcandidate Snapshotの内容差から導出し、実際のfile deltaと一致する。
   Snapshotのcommitが同じでも、candidateのindex、tracked content、対象untrackedが変われば空Change Setを
   再利用しない。
3. source identityへ影響する利用者Git configを隔離し、同じfilesystem／Git状態を呼出し環境だけで
   cleanへ変えない。
4. 暫定lineage IDは本前駆sliceだけに限定し、耐久identity、耐久Binding、Verification Run、Work 7A第2項
   checkbox完了の根拠にしない。

このcodeはsource identityとChange Setの合否を決め、誤りが偽の合格になる守り役であるため、`high`は妥当。

## 3. 独立再実行

| 区分 | command | 結果 | exit code |
| --- | --- | --- | --- |
| targeted | `.venv/bin/python3 -m pytest tests/test_work7a_checkout_relocation.py` | 19 passed | `0` |
| 関連回帰 | `.venv/bin/python3 -m pytest tests/test_layout_baseline.py tests/test_work7a_local_integrated_root_separation.py tests/test_first_review_task_contract_e2e.py` | 83 passed | `0` |
| 公式全Test | `.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt /private/tmp/2026-08-09-codex-work7a-checkout-relocation-review-receipt-v1.json` | 1334 passed、fallback false | `0` |
| 独立反証 | `.venv/bin/python3 -m pytest -q /private/tmp/test_checkout_relocation_independent.py` | 3 failed | `1` |
| TODO validator | `python3 -m tools.development.todo_handoff TODO_NEXT_SESSION.md` | findings `[]` | `0` |

独立反証file SHA-256は`ab45c847930ab85b9381463f52ad83b6108288a3977452ffa768e44870a66507`。
Pilot fixtureをimportせず、別の`tmp_path` Git fixtureから次の3境界を機械実行した。

## 4. Findings

### RR-P1-001：dirty candidateを空Change Setとして合格させる

`derive_change_set`と`verify_change_set`は、base／candidate Snapshotの完全な内容差ではなく、両Snapshotの
`head_commit`だけを`git diff`へ渡す。独立反証では、base Snapshot捕捉後にtracked fileをdirty変更し、
同じHEADのcandidate Snapshotを捕捉した。candidateの`tracked_changes`とmanifestは変化しているが、導出された
`added_modified_deleted_renamed_items`は空だった。

影響：上流の「commit SHAだけではdirty worktreeを表せない」という中心規則に反し、実変更を含む
candidateへ空Change Setと旧検証結果を再利用できる。review requestのA/M/D/R一致、Snapshot束縛、GREEN完了Claimは
実状態と一致しない。

必要な修復：base／candidate Snapshotのindex、tracked content、対象untrackedを含む実内容差からChange Setを
導出・照合する。少なくとも同一HEADのdirty、staged、対象untrackedについて、空Change Setを拒否し、対応する
add／modify／deleteを固定するRED Testを追加する。既存schemaで表せない場合だけ停止してHuman判断を得る。

### RR-P1-002：実HEADと異なるcaller指定commitをSnapshotのHEADとして捕捉する

`capture_source_snapshot`はcaller指定`head_commit`がrepositoryに存在することだけを確認する一方、
`content_manifest_digest`のHEAD treeは実際の`HEAD`から取得する。独立反証ではcommit 2が現在HEADの状態で、
存在する旧commit 1を`head_commit`へ渡しても捕捉が成功した。結果は`head_commit=commit 1`と
`manifest=commit 2のHEAD tree`を同時に持つ。

影響：Source Snapshot内部のHEADとmanifestが競合し、そのSnapshotを`derive_change_set`が事前照合なしに消費できる。
実GitからHEADを捕捉したというClaimと事後状態が一致しない。

必要な修復：捕捉時に実HEADを機械取得してrecordへ設定するか、caller指定値を期待値として実HEADとの一致を
必須にする。旧HEADを指定した捕捉が安定stop codeで拒否されるRED Testを追加する。

### RR-P2-003：command-scope Git configが隔離されずdirty状態を隠せる

`_git_environment`は現在環境を複製して`GIT_CONFIG_GLOBAL`／`GIT_CONFIG_SYSTEM`を上書きするが、
`GIT_CONFIG_COUNT`、`GIT_CONFIG_KEY_*`、`GIT_CONFIG_VALUE_*`を保持する。独立反証ではこれらから
`core.fileMode=false`を注入すると、実file modeがHEADと異なる状態でもSnapshotの`index_state.clean`が
`true`になった。

影響：再評価recordの実装時確認事項3と、review requestの「config隔離」Claimを満たさない。
実装時確認事項1の`--no-optional-locks`位置、事項2のNUL区切り・rename thresholdは確認できた。

必要な修復：command-scope config注入用環境を除去し、identity判定へ影響するGit設定を明示的に固定する。
呼出し環境からの設定注入で同じ実状態がcleanへ変わらないRED Testを追加する。

## 5. 一致したClaimとHuman境界

- 暫定lineage ID限定はmodule／Test docstringへ明記され、耐久identityへ昇格していない。
- base／candidate Snapshot IDはそれぞれのcontent digestへ束縛され、別Snapshotへの差替えを拒否する。
- `--no-optional-locks`はglobal option位置、status／diffはNUL区切り、rename thresholdは50%で明示されている。
- targeted 19、関連83、公式全1334の合格、成果物Digest、commit境界は報告と一致する。
- 耐久Binding、Verification Run、binding directory、TODO／checklist projectionは未実施のまま保持されている。
- push、tag、PR、履歴書換え、scope外path変更は観測していない。

Humanの再開承認後にREDを開始し、review request commitで停止したWorkflow境界は維持されている。

## 6. 判定と次

`report_execution_mismatch`。既存Test／receiptの合格はそのTest集合について有効だが、RR-P1-001〜002の
中心受入条件とRR-P2-003の明示確認事項を覆わないため、GREEN完了、`verified`、Closer projectionの根拠にしない。
影響を受けるGREEN Evidenceとreview requestの完了Claimはstaleとして扱う。Work 7A第2項checkboxは開いたまま、
TODOも現状のまま維持する。

Humanが本resultをPilotへ渡して上記3 Findingの修正を承認した場合、Pilotは修正RED、実装、更新GREEN Evidence／
receipt、新review requestを別commitで固定して停止する。Reviewerは元の19 Test、独立反証3件、関連Test、
公式全Testを再実行する。
