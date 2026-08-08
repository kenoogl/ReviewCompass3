# Codex → Claude：伏字化設定を実保全入口へ接続する修正指示

## 1. 判定と修正対象

- Humanは、Codexの独立レビューで見つかった未接続について、選択肢1「いま修正する」を
  選択した。
- 先行実装commit `dc13ed153da3a77d381c3bcc9667071e4906940b`は書き換えない。
- 修正対象は1点だけである。

  `init-config`が登録し、`load_config`が読み込んだ8規則を、実際の
  `tools.session_logs.entry collect-eventual`入口から`eventual_preservation.run()`を経由して
  `reconcile_source_root`または`collect_source`へ渡す。

- Claudeは、actual CLIのRED Testを先にcommitし、そのTestを変更せず最小配線でGREENにする。
- 完了後はClaude→Codex報告を作り、Codexの再レビューまで停止する。

## 2. レビューで成立した反証

Codexは、Claudeのfixtureに無い合成sessionをactual CLIから機械実行した。

- 入口：`tools.session_logs.entry collect-eventual`
- 入力：pattern規則`email`の対象となる合成メール文字列
- 結果：CLI exit `0`、status `ok`
- `redacted_artifact_count = 0`
- Provenanceの`artifacts.redacted_sha256 = null`
- Provenanceの`redaction_rules_sha256 = null`

原因は`eventual_preservation.run()`の2分岐が、どちらも`redaction_rules`、
`environment_redaction_rules`、`allow_patterns`を渡さずに`reconcile_source_root`または
`collect_source`を呼んでいることである。新規Testの`_collect_with_config()`だけが手動で渡していた。

この不一致により先行の`completed_claim`は`report_execution_mismatch`であり、TODO・checklistの
完了反映は停止したままである。

## 3. 開始状態と固定入力

- implementation base：`dc13ed153da3a77d381c3bcc9667071e4906940b`
- branch：`main`
- 本指示書はimplementation baseの直後にCodexがcommitする。Claudeの開始HEADがbaseより1commit先で、
  そのdiffが本指示書1fileの追加だけであることは正常とする。それ以外の先行差分は停止条件である。

| role | path | SHA-256 |
| --- | --- | --- |
| 元指示書 | `records/session-handoffs/2026-08-08-codex-to-claude-redaction-registration-preservation-path.md` | `b1eb142a8d4e0883b8f92143a9e9acc6c4ab31a186fd0d8362eca8d3a9b1351d` |
| 先行GREEN Evidence | `records/development/2026-08-08-redaction-registration-preservation-green-evidence-v1.md` | `4b5fc501ffba652008cbfff47a2afa1769341fce35a5329ea0bea125b0f13956` |
| 先行公式receipt | `records/development/2026-08-08-redaction-registration-preservation-green-test-receipt-v1.json` | `05fd70b9c9c31b0b57f6571e83a470fe1607c7811cd089471c70116ea15e0d56` |
| 設定loader | `tools/session_logs/config.py` | `af8651cc911b7d4afac2a4b02562b60cd408a21c98967a2c700d2392b1e4dc8c` |
| 設定generator | `tools/session_logs/portable_config.py` | `135faff2d565f36206ce8017f46fb0d016b1c883b66444537c7eec90ee93d34b` |
| 未接続の実入口 | `tools/session_logs/eventual_preservation.py` | `b66f6e9afb924ef99201ec2711441b2781923d4d7a8f7d9d5ad8a9519b76796c` |
| 固定entry | `tools/session_logs/entry.py` | `ddffc769cd683ffeed8b1474d9e599c9ce1283f1ed875d460b6b0953f019bc3e` |
| 先行Acceptance Test | `tests/test_redaction_registration_preservation_path.py` | `157f0874032de2089153498d26c4e7f21138d2ac3307652ff051f9fe648ec57f` |
| 共同作業手順 | `docs/development/codex-claude-collaboration.md` | `beab9d2cf0db4f31a869ae2d597dff8265ace9a022d83bba2d03b810a984cc49` |
| レビュー手順 | `docs/development/work-review-protocol.md` | `37c0391a322a6841421742125fff646600aff7d3acd905990c605f614d2e2967` |
| 現在位置 | `TODO_NEXT_SESSION.md` | `77fc5867de82f52716dadcf6930ae7be06ef296fa68ca38b3125894b1782b3dd` |

作業開始時にcommit列、worktree、固定入力Digestを機械照合する。

## 4. 修正契約

### 4.1 actual CLIへのadditiveな設定引数

- `eventual_preservation.run()`に`--config` optional argumentを追加する。
- `--config` supplied時は、source discoveryやraw保全より前に`tools.session_logs.config.load_config`で
  1回だけ読み込む。
- loadした次の宣言を、source-root全体の分岐と`--source-relative-path`の単一source分岐の
  両方で下流へ渡す。
  - `config.redaction_rules`
  - `config.environment_redaction_rules`
  - `config.allow_patterns`
- `--config` supplied時にconfig loadが失敗したらexit `5`、`status: error`とし、source読取り、raw保全、
  派生物作成を開始しない。例外文や入力値を診断へ出さない。
- `--config` omitted時は既存CLI引数、exit、report、`redaction_rules is None`の
  「伏字化派生物を作らない」互換契約をそのまま保つ。
- `--tool-version`とpath群は従来どおりCLI引数を使う。今回configから読むのは伏字化規則と
  `allow_patterns`だけである。
- `tools/session_logs/entry.py`は引数をそのまま委譲できる現行実装を固定入力とし、
  変更しない。

### 4.2 actual CLI Acceptance

新規Testはdirect `collect_source()`やTest helperの手動配線をoracleにせず、次の公開入口を実行する。

`tools.session_logs.entry.run(("collect-eventual", ...))`

合成fixtureだけで次を固定する。

1. `init-config`が生成した8宣言入りconfigを`--config`へ渡す。
2. source-root全体分岐と単一source分岐の両方がexit `0`、status `ok`となる。
3. 両方でredacted artifactが存在し、合成home、user、host、email、tokenが残らない。
4. Provenanceの`artifacts.redacted_sha256`と`redaction_rules_sha256`がnon-nullで、実artifactと宣言から
   再計算した値に一致する。解決後の環境値はProvenanceに残らない。
5. 存在しないまたは不正なconfigを渡すとexit `5`となり、private rootにraw、redacted、
   Provenance、cursorを作らない。
6. `--config` omittedの既存actual CLI Testは引き続き合格する。

Testでは`tmp_path`と`monkeypatch`の合成値だけを使う。実在の秘密、host固有値、既存保全データを
読まない、表示しない。

## 5. TDDとcommit境界

### Commit 1：修正RED

- `tests/test_redaction_registration_preservation_path.py`にactual CLI Acceptanceを追加する。
- 実装前に対象Testを単独実行し、新規actual CLI Testだけが期待した未接続で失敗し、
  先行9 Testは通ることを確認する。
- `git diff --check`後、Test pathだけを明示stageし、RED Testだけの追加commitを作る。

### Commit 2：修正GREEN

- RED commit後は新規Testを変更せず、`tools/session_logs/eventual_preservation.py`だけを
  実装修正して通す。
- 対象Test、関連回帰、公式全Testを別々の単独commandで実行し、exit codeで判定する。
- 公式receipt：
  `records/development/2026-08-08-redaction-production-entry-correction-green-test-receipt-v1.json`
- 修正Evidence：
  `records/development/2026-08-08-redaction-production-entry-correction-green-evidence-v1.md`
- Evidenceにはbase、修正RED commit、先行mismatch、actual CLIの2分岐、不正configのfail-closed、
  targeted・関連・公式全Test、Digest、禁止境界、未実施範囲を記録する。
- `git diff --check`、receipt再読込み、Evidence参照、SHA-256を機械照合する。
- 実装、Evidence、receiptだけを明示stageして緑commitを作る。TestはRED commitのままとする。
- コミット後に`python3 -m tools.development.work_unit_transition --work-status completed`を実行する。

公式全Test command：

`.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt records/development/2026-08-08-redaction-production-entry-correction-green-test-receipt-v1.json`

## 6. 変更可能path

- `tests/test_redaction_registration_preservation_path.py`
- `tools/session_logs/eventual_preservation.py`
- `records/development/2026-08-08-redaction-production-entry-correction-green-evidence-v1.md`
- `records/development/2026-08-08-redaction-production-entry-correction-green-test-receipt-v1.json`

上記以外の変更は禁止する。`config.py`、`portable_config.py`、`entry.py`、`redaction.py`は
先行実装または固定入力であり、変更しない。

## 7. 禁止事項と停止条件

- 元のRED/GREEN commitをamend、rebase、reset、revert、履歴書換えしない。
- `TODO_NEXT_SESSION.md`、checklist、Decision、Issue、Candidate、workflow台帳、既存Evidenceを変更しない。
- 既存保全データ、`SENSITIVE_ROOT`、hostの実sessionを読まない、書かない、削除しない。
- pattern、environment role、entropy網、allow semantics、storage boundary、raw先行保全を変えない。
- deployment、hook、watcher、scheduler、background service、外部送信、push、tag、PRを行わない。
- `git add -A`、`git add .`を使わず、明示pathだけをstageする。

次では範囲を広げず停止する。

1. 開始commit列、worktree、固定入力Digestが不一致。
2. 変更可能path以外の変更が必要。
3. additiveな`--config`で両分岐を接続できず、CLI非互換または新schemaが必要。
4. REDが未接続以外の理由で失敗、または先行9 Testが不合格。
5. 不正configの場合にsource読取りまたはprivate artifact作成が先に発生する。
6. targeted、関連回帰、公式全Test、diff check、receipt、Digestのいずれかが不合格。
7. 実在値・既存保全データへのaccessが必要。

## 8. Claude→Codex報告

完了または停止後、次を作成し、commitに含めず停止する。

`records/session-handoffs/2026-08-08-claude-to-codex-redaction-production-entry-correction.md`

報告には次を含める。

- `completed_claim` または `blocked_claim`
- implementation base、指示書commit、修正RED、修正GREENのSHAと変更path
- RED、targeted GREEN、関連回帰、公式全Test、diff checkのcommand・結果・exit code
- actual CLIの2分岐でのartifact数、Provenance digest、不正configのfail-closed結果
- Evidence、receipt、実装、TestのSHA-256
- 禁止操作・実在データaccessの未実施と、停止条件・未実施範囲

Codexは報告後、commit列、diff、Digest、actual CLI、公式全Test、禁止境界を独立確認する。
本修正も機密保護の`high`であり、Claudeのfixtureに無い新しい反証を最低1件機械実行する。
