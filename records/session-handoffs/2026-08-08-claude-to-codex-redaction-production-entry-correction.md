# Claude → Codex：伏字化設定の実保全入口への接続修正 完了報告

- 指示書：`records/session-handoffs/2026-08-08-codex-to-claude-redaction-production-entry-correction.md`
- 作成日：2026-08-08
- 本報告はClaimであり、Codexの再レビューを待つ。

## 1. 判定

`completed_claim`

## 2. commit系列と変更path

| 種別 | SHA | 変更path |
| --- | --- | --- |
| implementation base | `dc13ed153da3a77d381c3bcc9667071e4906940b` | （先行GREEN。書き換えていない） |
| 指示書commit | `73c9164a3ab94c6f8000bfba5ef25d8b562b45c8` | 修正指示書1fileのみ（172行。指示書§3の規定どおり正常） |
| 修正RED | `698a5aa6076f559b027283726acff1a73f5a9733` | `tests/test_redaction_registration_preservation_path.py`のみ（actual CLI受入Test 4件、160行追加） |
| 修正GREEN | `f9f92cf4bbb2843662e9377393df4afe4975c76a` | `tools/session_logs/eventual_preservation.py`、`records/development/2026-08-08-redaction-production-entry-correction-green-evidence-v1.md`（新規）、`records/development/2026-08-08-redaction-production-entry-correction-green-test-receipt-v1.json`（新規） |

開始状態の機械照合：branch `main`、worktree clean、固定入力11fileのSHA-256は指示書の表と
全件一致。GREEN commitではTestを変更していない（実装はRED commitのTestのまま合格）。

## 3. command・結果・exit code

| 区分 | command | 結果 | exit code |
| --- | --- | --- | --- |
| 修正RED（実装前・単独） | `.venv/bin/python3 -m pytest tests/test_redaction_registration_preservation_path.py` | 13件収集、新規actual CLI Test 4件のみ失敗（全件argparseの`unrecognized arguments: --config`＝未接続そのもの）、先行9件合格 | `1` |
| targeted GREEN | 同上command | 13 passed | `0` |
| 関連回帰 | `.venv/bin/python3 -m pytest tests/test_session_log_config_boundaries.py tests/test_session_log_portable_config.py tests/test_session_log_eventual_preservation.py tests/test_redaction_environment_rules.py` | 34 passed（`--config` omittedの既存actual CLI Testを含む） | `0` |
| 公式全Test | `.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt records/development/2026-08-08-redaction-production-entry-correction-green-test-receipt-v1.json` | 1282 passed、status `passed`（receipt再読込みでfailed 0を機械確認） | `0` |
| `git diff --check` | RED commit前・GREEN commit前 | 指摘なし | `0` |
| 事後transition | `python3 -m tools.development.work_unit_transition --work-status completed` | status `passed`、findings空 | `0` |

## 4. actual CLIの実測結果

受入Testは公開入口`tools.session_logs.entry.run(("collect-eventual", ...))`だけを実行し、
direct `collect_source()`や手動配線をoracleにしていない。入力は`init-config`が実際に
生成した8宣言入りconfigを`--config`へ渡したもの。合成fixture（`tmp_path`・`monkeypatch`）のみ使用。

- source-root全体分岐・単一source分岐とも：exit `0`、status `ok`、succeeded 1、
  **redacted artifact 1件**、Provenance 1件。
- Provenanceの`artifacts.redacted_sha256`はnon-nullで実artifactのSHA-256と一致。
  `redaction_rules_sha256`はnon-nullで、loaderが読んだ宣言（environment reference宣言＋
  pattern宣言、allow_patterns空）から再計算した
  `27987603a8d8ca672b1662c9fe7101baed73c824586553bc602e87507eb757ed`と一致。
  解決後の環境値（合成home・user・host）はProvenance本文・redacted artifact・CLI出力の
  いずれにも残らない。
- 不正configのfail-closed：存在しないconfigと不正宣言（`pattern`と`environment_role`の
  両持ち）のconfigは、いずれもexit `5`・`status: error`となり、**private root自体が
  作られない**（raw・redacted・Provenance・cursorなし＝source読取り・raw保全・派生物作成の
  いずれも開始しない）。出力にconfig path・宣言値・例外文は出ない（例外の型名のみ）。

実装は`run()`へのadditiveな`--config`のみで、supplied時はsource discoveryより前に
`load_config`で1回だけ読み込み、両分岐へ`redaction_rules`・`environment_redaction_rules`・
`allow_patterns`を渡す。omitted時は従来どおり`None`が渡り、既存CLI引数・exit・report・
「伏字化派生物を作らない」契約は不変。`--tool-version`とpath群は従来どおりCLI引数。

## 5. SHA-256

| file | SHA-256 |
| --- | --- |
| `records/development/2026-08-08-redaction-production-entry-correction-green-evidence-v1.md` | `d9ec9d812c3cd8a3eb2efdc293eb934fe02dafe157aae9c3b24c996f2cb08f21` |
| `records/development/2026-08-08-redaction-production-entry-correction-green-test-receipt-v1.json` | `f2fb51467c13dbf4013698b63aa2b200bc8c5392b5348cce987c1375f55ca72c` |
| `tools/session_logs/eventual_preservation.py` | `9a22242f64b3137849f3d39d25e2b450a7dce65938ed8e6f9f41379e329f3c18` |
| `tests/test_redaction_registration_preservation_path.py` | `ae370016e70d2baba00f9c259e3c59ef4046ae4a54c6b56c23e1af21797bd53b` |

## 6. 禁止操作・実在データaccessの未実施

- 元のRED/GREEN commitのamend・rebase・reset・revert・履歴書換え：未実施。
- 変更可能path以外の変更：なし（`config.py`・`portable_config.py`・`entry.py`・
  `redaction.py`は未変更。SHA-256はそれぞれ固定入力の表の値のまま）。
- pattern・environment role・entropy網・allow semantics・storage boundary・raw先行保全：未変更。
- `TODO_NEXT_SESSION.md`・checklist・Decision・Issue・Candidate・workflow台帳・既存Evidence：未変更。
- 既存保全データ・`SENSITIVE_ROOT`・hostの実sessionの読取り・書込み・削除・表示：未実施。
- deployment・hook・watcher・scheduler・background service・外部送信・push・tag・PR：未実施。
- stageは全て明示path指定（`git add -A`／`git add .`不使用）。

## 7. 停止条件の発生有無と未実施範囲

- 停止条件1〜7：いずれも発生せず。
- 未実施範囲：TODO・checklistへの完了反映（Codex再レビュー後）、実在データへの遡及適用
  （別のHuman判断）。
- 本報告fileはcommitに含めていない。Codexによる再レビューが終わるまで次の作業へ進まない。
