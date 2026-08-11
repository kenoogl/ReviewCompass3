# 操縦者別連携 RED受入テスト 独立レビュー v1

- 日付：2026-08-11
- 実装指示：`records/session-handoffs/2026-08-11-pilot-collaboration-entry-implementation-request-v6.md`
- 実装指示SHA-256：`5ab9474b425162df9c192124c7558754b4b371402d2e4d67adfab448cbbb3b5d`
- base commit：`30925a54a0e8ee7c53e3503eccfda7a73fa11752`
- REDテストcommit：`df48bbafe29b62e2efe26e0e7b1ddebc75e47f2b`
- 実装担当モデル：`gpt-5.6-sol`
- レビュー担当モデル：`gpt-5.6-terra`
- 未加工結果保存：`specified_only`。最終応答は主担当の会話で受領したが、不変保存処理は未接続
- 判定：`reported_unverified`
- 現在状態：`Human判断待ち`

## 1. 変更範囲と独立再実行

変更は次の新規テスト4件だけで、既存file、実装code、文書、設定の変更はなかった。

- `tests/test_pilot_collaboration.py`
- `tests/test_pilot_collaboration_cli.py`
- `tests/test_bootstrap_immutable_result_store.py`
- `tests/test_pilot_collaboration_entrypoints.py`

主担当側で各fileを単独再実行した結果は、順に27 failed / 1 passed、7 failed、10 failed / 1 passed、
3 failed / 1 passedで、すべて終了コード1だった。4 fileの`--collect-only`は計50件、すべて終了コード0だった。
新規テスト4件を除く既存テストは1470 passed、終了コード0だった。

REDの代表原因は、未実装の`pilot_collaboration_cli`、`pilot_collaboration.py`、
`immutable_result_store`、共通prompt、共通entrypointの不存在であり、構文または収集失敗ではない。

## 2. 独立レビュー所見

| ID | 種別 | 段階 | 影響 | 事象 | 推奨修正 |
| --- | --- | --- | --- | --- | --- |
| `RT-PC-001` | blocking・類型3（誤った合格） | completion | `NG-PC-001`, `AC-PC-009`, `ST-PC-002` | 禁止起動検査は直接の`subprocess.run`と文字列リテラルだけを調べるため、`Popen`、別名、動的文字列を見逃す。既存保存処理の共通境界使用もimport文字列の存在だけで合格し、未使用importを見逃す | 禁止起動は許可されたGit操作以外のprocess起動経路をASTで一括拒否する。共通保存境界は未使用importで通らない振る舞いまたは呼出し確認へ変える |
| `RT-PC-002` | blocking・類型3（誤った合格） | completion | `AC-PC-004`, `AC-PC-006`, `AC-PC-008`, `OUT-PC-003` | launch記録のraw SHA-256不一致と、判定rawの`audit_parsed_sha256`不一致を故障注入していない。照合を省いた実装が通り得る | `raw_digest_mismatch`と`audit_digest_mismatch`をそれぞれ実際に発生させ、保存・停止code・非解析を確認する |
| `RT-PC-003` | blocking・類型3（誤った合格） | completion | `OUT-PC-003`, `OUT-PC-005` | `TRACEABILITY`は26 keyの件数と順序だけを検査し、参照先test名の実在を確認しない。`OUT-PC-003`は存在しない`test_fault_injection_matrix_covers_required_failures`を参照しても合格する | 対応表が参照するtest関数の実在を機械照合するか、実在する故障注入test群へ明示的に対応させる |
| `RT-PC-004` | blocking・類型3（誤った失敗） | completion | `ST-PC-001`, `NG-PC-007`, `OUT-PC-004` | 変更範囲testが固定対象commitでなく実行時の`BASE_COMMIT..HEAD`とworktree全体を調べる。後続のレビューrecordやTODO commitが入ると、実装変更でなくても恒常的に失敗する | 実装対象commitまたは機械的に渡す固定base/targetだけを検査し、後続recordと利用者差分を混ぜない |

レビュー担当は同じ類型の変種を同一周回で掃討し、上記4件以外のblocking所見を追加しなかった。

RT-PC-004は本記録と`TODO_NEXT_SESSION.md`の未コミット差分だけがある状態で、対象testを単独再実行して
終了コード1を確認した。余分なpathとしてこの2件が列挙され、実装変更がなくても誤って失敗することを実証した。

## 3. Human判断境界

`RT-PC-001`から`RT-PC-004`までの採用、不採用または保留をHumanが判断するまで、REDテストを変更せず、
production実装へ進まない。採用する場合は新規テスト4件だけを修正し、各単独RED、50件収集、既存1470件、
差分検査を再実行して、別の新しい会話状態で再レビューする。
