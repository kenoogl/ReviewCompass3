---
evidence_id: RC3-SESSION-TRANSCRIPT-EVENTUAL-PRESERVATION-IMPLEMENTATION-CHECKPOINT-2026-08-04-V1
recorded_at: 2026-08-04T00:12:10+09:00
status: verified_checkpoint
workflow_state: human_storage_decision_pending
confidentiality_class: project-internal
---

# Session Transcript Eventual Preservation Implementation Checkpoint Evidence V1

## 1. 結果

終了hookに依存しないmanual collector、durable cursor、source-root reconcile、byte-exact raw、private
verbatim transcript、任意のredacted transcript、private Provenance、safe reportをtest-firstで実装した。
Claude、Codex exec JSONL、Codex rolloutの3形式を同じ入口で扱う。

実private logはまだcopyしていない。次の関門は保存候補に対するHuman判断であり、承認後に現在のCodex
Desktop task 1件だけを手動保存して同一再実行を確認する。

## 2. AuthorityとTask Contract

| role | artifact | SHA-256 |
|---|---|---|
| implementation Decision | `records/development/2026-08-03-session-transcript-eventual-preservation-implementation-decision.json` | `1fe3c2a6cf8a3430ffb9a290a437dbc34777d2514beac910a26f52a419732262` |
| Task Contract | `records/task-contract/session-transcript-eventual-preservation-v1.json` | `981e7cb1e7344f576afe3dbaf9fee94462e353980e4944b7fd2bd33401e595cf` |
| initial RED Evidence | `records/development/2026-08-04-session-transcript-eventual-preservation-red-evidence-v1.md` | `f7e8649c2ebff2d9941716d67c531990664b53364c20d2c70f70166a3f6938a1` |

initial REDはmoduleとCLI入口の未実装だけを理由として`11 failed in 0.16s`だった。

## 3. 実装と固定Test

| role | artifact | SHA-256 |
|---|---|---|
| collector／cursor／reconciler | `tools/session_logs/eventual_preservation.py` | `a9503935489593d5c9007be7a1e1f52534a972d78539e5a4a460a15c9e66029b` |
| fixed manual entry | `tools/session_logs/entry.py` | `ddffc769cd683ffeed8b1474d9e599c9ce1283f1ed875d460b6b0953f019bc3e` |
| macOS standard path fallback | `tools/session_logs/deployment_paths.py` | `48f90aef8db88ab7b80e5a4a427365a1bc0efc9886b71205897eda0791a7b380` |
| collector Acceptance Test | `tests/test_session_log_eventual_preservation.py` | `a4f704c4ac267e983c0831b2f1a6a97a64c6db335b8eae9d3efa032e897b3999` |
| path resolver Test | `tests/test_session_log_deployment_paths.py` | `a1830ba2729c53d547e91b5d3c660a017cff75083f48000d9531d3429199f88f` |

固定した挙動は次のとおりである。

- rawを先にprefix保全し、派生物とProvenanceの後にcursorをcommitする。
- 同一再実行は`unchanged`、純粋追記は`updated`となり、eventを重複させない。
- JSONL部分行はrawへ保存するが、完全行になるまで解析offsetを進めない。
- cursor commit失敗後の再実行で重複なく復旧する。
- source短縮／途中置換ではarchiveとcursorを上書きせず`diverged`とする。
- private outputがrepository内なら書込み前に拒否する。
- private directoryを`0700`、fileを`0600`へ固定する。
- CLIは相対pathで1 sourceだけを選べ、reportへpathまたは本文を出さない。

## 4. 追加REDと処置

### private permission

初回GREEN後の安全監査でowner-only permission Testを追加し、lock directoryだけがOS既定`0755`となる
`1 failed`を確認した。artifact fileは`0600`、他directoryは`0700`だった。lock取得前にprivate directory
chainを`0700`で作成するよう修正し、collector Testは`12 passed`となった。

### OS標準path

実環境のpath候補解決で、公式Pythonにoptional dependency `platformdirs`がなく
`DeploymentPathError`となることを確認した。macOS標準pathを標準libraryだけで解決するTestを追加し、
実装前`1 failed`、fallback実装後に関連`14 passed`と実環境resolver合格を確認した。

### 限定1 source CLI

source root全体にはCodex 907、Claude 664 JSONLがあり、pilotで全件取得するのは過大だった。相対pathで
1件だけを指定するTestを追加し、実装前`1 failed`、実装後collector／path Testは`15 passed`となった。

## 5. GREEN

- collector固定Test：`12 passed in 0.12s`
- session-log全Test：`171 passed in 1.62s`
- collector／path関連：`15 passed in 0.12s`
- 公式全Test receipt：
  `records/development/2026-08-04-session-transcript-eventual-preservation-implementation-checkpoint-test-receipt-v1.json`
- receipt SHA-256：`7e496d33d955dfa10e1423176d72332a9c751a7efd0e01a5b671c52befe51c33`
- 公式全Test：`490 passed in 2.19s`、exit code 0、fallback `false`
- compile：`PYTHONPYCACHEPREFIX`をprivate temporary rootへ固定して3 module合格
- `git diff --check`：finding 0

## 6. 保存候補と判断待ち

- Candidate：`records/development/2026-08-04-session-transcript-eventual-preservation-storage-candidate-v1.json`
- Candidate SHA-256：`0c712308275cd321870fe2c203b0b53207bc817108a9fba3910da6ee730a5fdc`
- 推奨：`option_1_os_standard_limited_pilot`

推奨optionはOS標準application-data rootの論理bindingへ、現在のCodex Desktop task 1件だけを保存する。
raw、private verbatim、cursor、private Provenance、ledgerを対象とし、redacted transcript、過去履歴、Claude、
hook、watcher、scheduler、background serviceは対象外である。retentionは自動削除せず、2026-09-03に
Human reviewする。

## 7. 問題、手戻り、機械化候補

- 調査用並列tool callのJavaScript出力区切りをLLMが誤記し、構文エラーが1回発生した。期待executorは
  tool-call schemaを検査するmachine、実executorはLLM直接組立てだった。成果物影響はない。候補は
  `functions.exec` composition lint、routeは`manual_operation_candidate / checkpoint`とする。
- `py_compile`がworkspace外の標準cacheへ書こうとしてsandboxに拒否された。実／期待executorはともにmachineで
  手作業因果はない。task専用`PYTHONPYCACHEPREFIX`で再実行し合格した。候補はcompile runnerのcache固定、routeは
  `machine_environment_mismatch / checkpoint`とする。
- `platformdirs`欠落とpermission REDは既存／新実装の安全契約不足をmachine Testが検出して閉じたもので、
  手入力転記による手戻りではない。

## 8. 未実施

- storage CandidateのHuman判断
- current private Codex rolloutの読取り、copy、逐語録生成
- 実保存後の同一再実行、permission、Digest、Git非混入確認
- hook、watcher、scheduler、background service activation
- commit、push、Work 4開始

以上により実装checkpointを`verified_checkpoint / human_storage_decision_pending`とする。Task Contract完了は
限定実ログ保存と事後照合まで保留する。
