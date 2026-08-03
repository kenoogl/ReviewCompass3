# Work 3 Permanent Remediation GREEN Evidence V1

## Identity

- Evidence ID：`RC3-WORK3-PERMANENT-REMEDIATION-GREEN-2026-08-03-V1`
- recorded at：`2026-08-03T21:35:43+09:00`
- scope：Requirement格納形式の機械統一、policy準拠Test runner
- status：`verified / implementation_complete / authority_promotion_pending`

## RED Binding

- RED Evidence：`records/development/2026-08-03-work-3-permanent-remediation-red-evidence-v1.md`
- RED Evidence SHA-256：`700a26c69af875ad44e1df446ae79212fc4f3e6de0f552fa529624a70957ea2d`
- RED結果：`2 failed, 12 passed, 8 errors in 0.09s`

固定した3 Test fileを変更せず、共通reader、機械移行器、policy Test runnerを実装してgreenにした。
post-writeで追加発見したreceipt自己参照境界は別の回帰TestへREDを固定してから修正した。

## Implementation

### Unified Requirement migration

- mixed authority共通reader：`tools/requirements/artifact_layout.py`
  - SHA-256：`cbff52020530b7a8e6add78351e66cbf8af2061d087df77f5618c31cff0d72ec`
- 決定的移行器：`tools/requirements/unified_migration.py`
  - SHA-256：`4de6fa5cc9bbd022e36d7be84f4835d6bb76663a873c2931fb5c40495640affe`
- 移行definition：`records/requirements/definitions/`の旧37 Requirement対応37 file
  - 集合Digest：`63d5b41837969c3b3a606027abc12e789fd696f0c870cf37f60a0f39bd1cf50f`
- 統一50 candidate：
  `records/requirements/candidates/rc3-requirements-unified-50-2026-08-03-v1.json`
  - file SHA-256：`c82144375fecc22c088d06d510d9e041fe9c607a0d6e4eb353b034467654ca16`
  - candidate digest：`cc4ba8f872973f8035b798042f4a5335005394cca339ec6f0121cf16c8c533b4`
- current formal Evidence：
  `records/requirements/evidence/rc3-requirements-unified-50-evidence-2026-08-03-v2.json`
  - file SHA-256：`dce1994d194ef8f4c03d32a7fe66fe1764a2456b013270a79d93c261a074ba7f`
  - evidence digest：`5b42979ab79699b2da950bae4788f582b023211c5c919571209a7f43bb5492fe`

移行器は旧batchの9意味fieldを推測せずそのまま複製し、`acceptance_truth_changed: false`と旧definition
source、Human source、Approval、Completion Evidenceの4 refを付与した。生成初回は`written 38`、直後の
再実行は`written 0 / unchanged 38`、`--check`も`unchanged 38`だった。

### Policy Test runner

- runner：`tools/development/policy_test_runner.py`
  - SHA-256：`658282d425dcd507469b7fbf1e00af4ebcc8570ea00f0afc3f79ca2e673e583c`
- versioned config：`config/development-test-runner.json`
  - SHA-256：`8d43861e71eeb127bcce047a079c38cfdafb80b70dde1e8f0cf28a33a1330692`
  - config digest：`5a5ff957f6971ac2375214a8777bb1f654f9733ca5bad277f6e9f6122b0bd118`
- development dependency：`pyproject.toml`
  - SHA-256：`7c4a798164f999cdbd67d8327fbb0daed02f60390605d7f1a06f229e80a2cf56`
- official command案内：`README.md`
  - SHA-256：`299e5ca658c452ec2d0fa354585ca5519b90f66d8d885fd62b0ea9c410b9c094`
- current full Test receipt：
  `records/development/2026-08-03-work-3-permanent-remediation-full-test-receipt-v2.json`
  - SHA-256：`8405cdb8c9b7d74b4c5cb12d9c71c3f2baee8e900627c5fd023ae6f17f35cef4`

runnerは版付き設定から`python3 -m pytest -q`だけを選択し、Python／pytest versionをpreflightする。
設定環境がなければ`test_environment_unavailable`で停止し、別環境へfallbackしない。Test後はcommand、
実行器、version、config digest、source state digest、stdout／stderr、exit codeをreceiptへ原子的に保存する。

## Audit Results

- legacy source：37 Requirement
- migrated definition：37
- existing definition：13
- unified candidate：50 unique ID
- 意味field不一致：0
- definition／candidate／Evidence schema不一致：0
- mixed v1 authority machine reader：50 unique ID
- 連続再生成差分：0
- candidate subjectを含むformal Evidence subject：51
- 旧authority／legacy bindingの削除・上書き：0
- `git diff --check`：passed

独立結果：

```text
UNIFIED_MIGRATION_AUDIT_OK legacy=37 unified=50 semantic_mismatch=0 regenerated_diff=0
MIXED_READER_AUDIT_OK effective=50 duplicate=0
EVIDENCE_AUDIT_OK subjects=51 result=passed version=2
```

## Test Results

- 初回固定target green：`22 passed in 0.27s`
- formal Evidence target：`3 passed in 0.03s`
- receipt自己参照回帰を含む関連target：`26 passed in 0.33s`
- policy runnerによる全Test：`462 passed in 2.27s`
- Python：`3.9.6`
- pytest：`8.4.2`
- fallback：`false`
- source state digest：`71071c5af0e4dabed28807c26ec7e837dacf2f17bea252adbea692361db00e58`

## Problems and Treatment

1. 旧新混在authorityを監査ごとに手作業走査していた。共通readerと機械移行器へ置換し、通常の次期authority
   候補は50件すべてを`definition_refs`へ統一した。
2. `.venv/bin/python3`のような環境固有pathを人が選択していた。版付きconfig、preflight、fallback禁止、
   receipt必須の専用runnerへ置換した。
3. runner初版のpost-write確認で、既存receiptをsource stateへ自己参照させ得る境界を検出した。
   `tests/test_policy_test_runner_receipt_identity.py`でREDを確認し、指定receipt outputだけをsource state計算から
   除外した。旧receipt v1と、それを参照するformal Evidence v1はstaleな経過記録として保持し、判断対象から外す。

## Authority Boundary

現行effective authorityは引き続き
`records/requirements/authority/rc3-requirements-authority-2026-08-03--v1.json`である。新37 definition、
統一50 candidate、formal Evidence v2は`verified / human_decision_pending`であり、directoryまたは生成成功だけで
authorityにならない。Human promotion Decisionと、50 `definition_refs`だけを持ち旧v1を`supersedes`する
authority bundle v2は未作成である。

## Result

二つの恒久対策の実装と機械検証は完了した。格納形式のauthority切替だけは意味的裁定であるため、exact candidate
digestとEvidence digestへのHuman promotion判断を得るまで実施しない。
