# GREEN Evidence：伏字化設定の実保全入口（actual CLI）への接続修正

- 指示書：`records/session-handoffs/2026-08-08-codex-to-claude-redaction-production-entry-correction.md`
- 作成日：2026-08-08
- executor：Claude（Codex修正指示書に基づく委譲作業）

## 1. 先行mismatchと修正対象

Codexの独立レビューで、`tools.session_logs.entry collect-eventual`のactual CLIが
`--config`を持たず、`eventual_preservation.run()`の2分岐がいずれも`redaction_rules`・
`environment_redaction_rules`・`allow_patterns`を渡していないため、8宣言入りconfigが
あっても伏字化派生物が作られない（`redacted_artifact_count = 0`、Provenanceの
`redacted_sha256`・`redaction_rules_sha256`がnull）ことが反証された。
先行の`completed_claim`は`report_execution_mismatch`。本修正はこの1点だけを、
`tools/session_logs/eventual_preservation.py`の`run()`へのadditiveな`--config`配線で解消する。

## 2. commit系列

| 種別 | SHA | 内容 |
| --- | --- | --- |
| implementation base | `dc13ed153da3a77d381c3bcc9667071e4906940b` | 先行GREEN（書き換えていない） |
| 指示書配布 | `73c9164a3ab94c6f8000bfba5ef25d8b562b45c8` | 修正指示書1fileのみ追加（172行、指示書§3で正常と規定） |
| 修正RED | `698a5aa6076f559b027283726acff1a73f5a9733` | `tests/test_redaction_registration_preservation_path.py`のみ（actual CLI受入Test 4件追加、160行） |

開始時確認：branch `main`、worktree clean、固定入力11fileのSHA-256は指示書の表と全件一致。

## 3. 修正RED（Commit 1）

- command：`.venv/bin/python3 -m pytest tests/test_redaction_registration_preservation_path.py`
- 結果：13件収集、新規actual CLI Test 4件のみ失敗、先行9件は合格、exit code `1`
- 失敗理由は全件が`--config`未接続そのもの（argparseの`unrecognized arguments: --config`）。
  fixture不備・実在値露出・別原因の失敗は無い。
- 新規Testはdirect `collect_source()`やTest helperの手動配線をoracleにせず、公開入口
  `tools.session_logs.entry.run(("collect-eventual", ...))`だけを実行する。

## 4. 修正GREEN（Commit 2）の内容

`tools/session_logs/eventual_preservation.py`の`run()`のみを変更（RED commit後、Testは未変更）。

- `--config` optional argumentを追加。supplied時はsource discoveryやraw保全より前に
  `tools.session_logs.config.load_config`で1回だけ読み込む。
- loadした`config.redaction_rules`・`config.environment_redaction_rules`・
  `config.allow_patterns`を、source-root全体分岐（`reconcile_source_root`）と
  `--source-relative-path`の単一source分岐（`collect_source`）の両方へ渡す。
- config load失敗時は既存のexcept経路でexit `5`・`status: error`とし、source読取り・
  raw保全・派生物作成を開始しない（private rootを作らない）。診断は例外の型名のみで、
  例外文・入力値・pathを出さない。
- `--config` omitted時は`redaction_rules=None`のまま渡し、既存CLI引数・exit・report・
  「伏字化派生物を作らない」互換契約を維持。`--tool-version`とpath群は従来どおりCLI引数。
- `tools/session_logs/entry.py`は無変更（引数をそのまま委譲する現行実装のまま）。

## 5. actual CLIの実測結果（受入Test、合成fixtureのみ）

- source-root全体分岐・単一source分岐とも：exit `0`、status `ok`、succeeded 1、
  redacted artifact 1件、Provenance 1件。
- 合成home・user・host・email・tokenはredacted artifactにもCLI出力にも残らず、
  置換先は`[REDACTED:<label>]`。
- Provenanceの`artifacts.redacted_sha256`はnon-nullで実artifactのSHA-256と一致。
  `redaction_rules_sha256`はnon-nullで、loaderが読んだ宣言（environment reference宣言＋
  pattern宣言、allow_patterns空）から再計算した値
  `27987603a8d8ca672b1662c9fe7101baed73c824586553bc602e87507eb757ed`と一致。
  解決後の環境値はProvenance本文に出ない。
- 存在しないconfig・不正宣言（patternとenvironment_role両持ち）のconfigは、いずれも
  exit `5`・`status: error`となり、private root自体が作られない（raw・redacted・
  Provenance・cursorなし）。出力にconfig pathや宣言値は出ない。
- `--config` omittedの既存actual CLI Test
  （`test_manual_entry_reports_counts_without_paths_or_content`）は引き続き合格。

## 6. Test実行の記録

| 区分 | command | 結果 | exit code |
| --- | --- | --- | --- |
| 修正RED（実装前・単独） | `.venv/bin/python3 -m pytest tests/test_redaction_registration_preservation_path.py` | 4 failed（新規のみ）／9 passed | `1` |
| targeted GREEN | 同上command | 13 passed | `0` |
| 関連回帰 | `.venv/bin/python3 -m pytest tests/test_session_log_config_boundaries.py tests/test_session_log_portable_config.py tests/test_session_log_eventual_preservation.py tests/test_redaction_environment_rules.py` | 34 passed | `0` |
| 公式全Test | `.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt records/development/2026-08-08-redaction-production-entry-correction-green-test-receipt-v1.json` | 1282 passed、status `passed` | `0` |
| `git diff --check` | RED commit前・GREEN commit前に実行 | 指摘なし | `0` |

公式receiptは再読込みし、status `passed`・exit `0`・1282件全合格・failed 0を機械確認済み。

## 7. SHA-256

| file | SHA-256 |
| --- | --- |
| `tools/session_logs/eventual_preservation.py` | `9a22242f64b3137849f3d39d25e2b450a7dce65938ed8e6f9f41379e329f3c18` |
| `tests/test_redaction_registration_preservation_path.py` | `ae370016e70d2baba00f9c259e3c59ef4046ae4a54c6b56c23e1af21797bd53b` |
| 公式receipt（同上JSON） | `f2fb51467c13dbf4013698b63aa2b200bc8c5392b5348cce987c1375f55ca72c` |

## 8. 禁止境界と未実施範囲

- 元のRED/GREEN commitのamend・rebase・reset・revert・履歴書換え：未実施。
- `config.py`・`portable_config.py`・`entry.py`・`redaction.py`：未変更。
- pattern・environment role・entropy網・allow semantics・storage boundary・raw先行保全：未変更。
- `TODO_NEXT_SESSION.md`・checklist・Decision・Issue・Candidate・workflow台帳・既存Evidence：未変更。
- 既存保全データ・`SENSITIVE_ROOT`・hostの実sessionの読取り・書込み・削除：未実施
  （Testは`tmp_path`と`monkeypatch`の合成値のみ）。
- deployment・hook・watcher・scheduler・background service・外部送信・push・tag・PR：未実施。
- stageは全て明示path指定（`git add -A`／`git add .`不使用）。
- 未実施範囲：TODO・checklistの完了反映（Codex再レビュー後）、実在データへの遡及適用
  （別のHuman判断）。
