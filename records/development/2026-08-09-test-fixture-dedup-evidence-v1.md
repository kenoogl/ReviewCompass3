# Evidence：テストfixture重複の共通化（deferred #7）

- 範囲固定：`records/session-handoffs/2026-08-09-claude-pilot-test-fixture-dedup-scope-v1.md`
  （SHA-256 `4c9595d15195c5d3504bebcdb1f4b82fac282530a7e5e20d66b64c71beb86a36`、SCOPE commit `91be5a9`）
- Human承認：risk `low`確定・実装開始承認（2026-08-09
  「#7 risk lowを確定、実装開始を承認する」）
- 作成日：2026-08-09
- executor：Claude（Pilot。mode `role_neutral_pilot_review`、Reviewer=codex、Closer=codex）

## 1. 実施内容

新helper `tests/shared_fixtures.py`へ次の3系統を集約し、対象7 fileの重複定義を
薄い委譲へ置き換えた。REDは作らない（振る舞い変更なし。scope §5どおり）。

- Project Manifest v2（7 artifact roots）：`project_manifest_v2`／`write_project_manifest_v2`
  ← `test_work7a_local_integrated_root_separation.py`・`test_work7a_checkout_relocation.py`
- Work 4A形manifest（4 artifact roots）：`work4a_manifest`
  ← `test_work4a_rebuild_v3_e2e.py`・`v3_1`・`v3_2`（各fileの`_manifest`は委譲のみ残す）
- 合成Claude会話record：`claude_conversation_records`／`write_jsonl`
  ← `test_session_log_eventual_preservation.py`・`test_preservation_migration.py`
  （file固有の本文・secret・markerは呼出し引数で維持）

assert文・テスト関数名・parametrize・受入条件の意味は変更していない（fixture抽出のみ）。

## 2. 受入条件の機械照合

| scope §6条件 | 方法 | 結果 |
| --- | --- | --- |
| 1. fixture内容の同一性 | 置換前後で同一probe（各fileのfixture生成関数を固定引数で実行しSHA-256化。probe scriptと出力はscratchpad、hash値は下表） | **9項目すべて一致** |
| 2. 対象suiteの収集数・合格数不変 | 置換前後で同一command（対象7 file一括pytest） | 前：129 passed／後：129 passed、exit `0` |
| 3. 公式全Test合格 | `policy_test_runner --suite full --receipt records/development/2026-08-09-test-fixture-dedup-receipt-v1.json` | 1338 passed（置換前と同数＝helperの誤収集なし）、status `passed`、receipt再読込みでfailed 0確認 |
| 4. 差分がfixture抽出のみ | `git diff`目視＋assert・関数名の不変（Reviewer再確認対象） | 7 file合計 +28／−126行 |
| 5. `git diff --check`・worktree | 実行 | 指摘なし・commit後clean |

fixture同一性probeのhash（置換前＝置換後）：

| probe | SHA-256 |
| --- | --- |
| separation_manifest ＝ relocation_manifest | `c38144d35713bd7e70eba766ef3548c4c4a6f42059bbdc590ad5e77e1e7a98db` |
| separation_readme | `1750a907a3031a3ae59255e406e22e7a6b753793805289d4a1ae7d71d76f222d` |
| work4a_v3 ＝ work4a_v3_1 | `745ab39cec5b50972237be065e815f23d436f377a153d0da1a2fc56482c88bca` |
| work4a_v3_2 | `7bc28ab1adf8bcb4f295ec7b2fe5ee96b4cba9a8d541886ee56b1b412f67ba01` |
| eventual_records_default | `881eb29cc5342841df60647969b34bbd9a9b654018502c483a7028a2e602ee7f` |
| eventual_records_secret | `af5d49065d84db31c7ea282a02346c0dbdec224b66bf6cfe8573371f6b5c776c` |
| migration_records | `5bdf77f049d36081b4f1e74d24b3108065d13be08b5a948be6b16956f5291c49` |

（separation＝relocation、v3＝v3_1のhash一致は、共通化前から内容が重複していたことの実証でもある）

## 3. 禁止境界

- product code・`tools/`配下・対象外test file・TODO・checklist・Decision・既存Evidence：未変更。
- push・tag・PR・履歴書換え・一括stage：未実施（明示path stageのみ）。
