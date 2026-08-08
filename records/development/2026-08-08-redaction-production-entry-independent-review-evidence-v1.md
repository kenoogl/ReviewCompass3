# 伏字化設定・実保全入口接続 独立レビューEvidence v1

- 実施日：2026-08-08
- reviewer：Codex
- Human指示：Claude作業終了後の独立確認、続く「完了反映」
- 作業指示：`records/session-handoffs/2026-08-08-codex-to-claude-redaction-production-entry-correction.md`
- implementation base：`dc13ed153da3a77d381c3bcc9667071e4906940b`
- 修正RED commit：`698a5aa6076f559b027283726acff1a73f5a9733`
- 修正GREEN commit：`f9f92cf4bbb2843662e9377393df4afe4975c76a`
- risk：`high`（機密保護の実行経路）

## 1. 先行不一致と修復範囲

先行GREEN `dc13ed1`では、設定loaderとcollector APIは実装されたが、actual CLI
`tools.session_logs.entry collect-eventual`が設定を下流へ渡していなかった。Codexの合成反証では
CLI exit `0`／status `ok`のままredacted artifactが0件、Provenanceのredacted digestとrules digestが
ともにnullとなり、先行`completed_claim`を`report_execution_mismatch`と判定した。

修正は`eventual_preservation.run()`へのoptional `--config`と、load済みの
`redaction_rules`・`environment_redaction_rules`・`allow_patterns`を2分岐へ渡す配線だけである。
`--config` omitted時の既存契約、規則、entropy網、storage boundary、raw先行保全は変更していない。

## 2. commit・変更範囲・Digest照合

【実測】implementation baseからreview対象HEADまでのcommit列は、指示書 `73c9164`、RED `698a5aa`、
GREEN `f9f92cf`の順だった。REDはAcceptance Testだけ、GREENは
`tools/session_logs/eventual_preservation.py`、本修正のGREEN Evidence、公式receiptだけを変更した。
GREENでRED Testは変更されていない。指示外path、既存recordの書換え、履歴書換えは0件だった。

| artifact | SHA-256 |
| --- | --- |
| `tools/session_logs/config.py` | `af8651cc911b7d4afac2a4b02562b60cd408a21c98967a2c700d2392b1e4dc8c` |
| `tools/session_logs/portable_config.py` | `135faff2d565f36206ce8017f46fb0d016b1c883b66444537c7eec90ee93d34b` |
| `tools/session_logs/eventual_preservation.py` | `9a22242f64b3137849f3d39d25e2b450a7dce65938ed8e6f9f41379e329f3c18` |
| `tests/test_redaction_registration_preservation_path.py` | `ae370016e70d2baba00f9c259e3c59ef4046ae4a54c6b56c23e1af21797bd53b` |
| 修正GREEN Evidence | `d9ec9d812c3cd8a3eb2efdc293eb934fe02dafe157aae9c3b24c996f2cb08f21` |
| 修正GREEN receipt | `f2fb51467c13dbf4013698b63aa2b200bc8c5392b5348cce987c1375f55ca72c` |

## 3. 独立再実行

各Testはpipeや`;`連結を使わず、単独commandのexit codeで判定した。

| oracle | command | result |
| --- | --- | --- |
| targeted | `.venv/bin/python3 -m pytest tests/test_redaction_registration_preservation_path.py` | `13 passed`、exit `0` |
| related | `.venv/bin/python3 -m pytest tests/test_session_log_config_boundaries.py tests/test_session_log_portable_config.py tests/test_session_log_eventual_preservation.py tests/test_redaction_environment_rules.py` | `34 passed`、exit `0` |
| official full | `.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt records/development/2026-08-08-redaction-production-entry-independent-review-test-receipt-v1.json` | `1282 passed`、exit `0`、fallback `false` |

独立公式receiptのSHA-256は
`ce26543e61df279103dfa57150f939fe4935fd08c989524dad2d56f29e4d1627`。

## 4. reviewer独自oracle

Claudeのfixtureを唯一のoracleにせず、`tmp_path`相当の一時rootと合成値だけを使うone-off実行を
actual CLIへ行った。実在の秘密・既存保全データは読んでいない。

### 正常経路

【実測】`entry collect-eventual --config <synthetic-config>`の単一source分岐はexit `0`／status `ok`。
redacted artifact 1件、Provenance 1件を作成し、合成home・user・host・email・tokenはartifactと
CLI出力から消えた。redacted digestは実fileのSHA-256と一致し、rules digestはnon-nullだった。

### 新作した反証：actual CLIでのhigh-entropy残存

【実測】Claudeのactual CLI fixtureに無い反証として、承認済み8規則では消えない合成high-entropy値を
`--config` suppliedのactual CLIへ渡した。結果はexit `5`／status `error`、raw 1件、redacted 0件、
Provenance 0件、cursor 0件だった。診断への合成値漏れは0件で、raw先行保全とfail-closedが同時に成立した。

## 5. 判定と未実施

【判断】`verified`。設定への8規則登録、loader、actual CLIのsource-root全体・単一source分岐、
伏字化派生物、宣言由来rules digest、不正configの事前停止、high-entropy残存時のfail-closedが
Evidenceへ接続された。先行`report_execution_mismatch`は修復済みである。

【未実施】既存保全データへの遡及適用、C／Dの扱いの定義、deployment・hook・schedulerの起動、
外部送信、pushは行っていない。既存データへの遡及適用は別のHuman判断のままである。
