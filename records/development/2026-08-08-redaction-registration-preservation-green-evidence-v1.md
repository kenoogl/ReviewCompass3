# GREEN Evidence：伏字化規則の設定登録と保全経路への接続

- 指示書：`records/session-handoffs/2026-08-08-codex-to-claude-redaction-registration-preservation-path.md`
- 作成日：2026-08-08
- executor：Claude（Codex指示書に基づく委譲作業）

## 1. commit系列

| 種別 | SHA | 内容 |
| --- | --- | --- |
| base | `32a8ac7af3817674f470a2d47adf1c6e891b34fd` | 指示書の固定base |
| 指示書配布 | `2ec86caf57ed5731b53253ec3004169e90075715` | 指示書fileのみ追加（Codex作成、205行、開始時に機械確認済み） |
| RED | `89affb753ce2f92e1bf2d9afdeb3026352cd9d20` | `tests/test_redaction_registration_preservation_path.py`のみ追加 |

開始時確認：branch `main`、worktree clean、固定入力12fileのSHA-256は指示書の表と全件一致。

## 2. RED（Commit 1）

- command：`.venv/bin/python3 -m pytest tests/test_redaction_registration_preservation_path.py`
- 結果：9件収集、9件失敗、exit code `1`
- 期待失敗の理由（全件が今回の未実装のみに起因）：
  - 通常の新規設定の`redaction_rules`が`[]`のままで8宣言が未登録（AssertionError）
  - loaderがenvironment reference宣言を読めない（`KeyError: 'pattern'`）
  - `Config.environment_redaction_rules`が未実装（AttributeError）
  - 不正宣言（両方持つ・どちらも持たない・未知role）が`ConfigError`にならない
- fixture不備、実在値の露出、既存実装でGREENになるTestは無い。

## 3. 設定登録の8宣言と実行経路

登録した宣言（宣言sourceは`tools/session_logs/redaction.py`の
`default_pattern_rules()`と`environment_reference_rules()`のみ。patternの重複記載なし）：

- pattern：`email`、`bearer_token`、`api_key_assignment`、`private_key_block`、
  `aws_access_key_id`（既存形式`{"label", "pattern"}`）
- environment reference：`home_directory`、`user_name`、`host_name`
  （承認済み形式`{"label", "environment_role"}`。実値・解決後patternは書かない）

実行経路（設定→loader→collector）：

1. `tools/session_logs/portable_config.py`の`default_redaction_rule_declarations()`が
   8宣言をJSON表現へ写し、`run()`（init-config）が通常の新規設定の既存top-level key
   `redaction_rules`へシリアライズする。`build_portable_config(..., redaction_rules=...)`の
   既存呼出し互換（既定値`()`）は維持。
2. `tools/session_logs/config.py`の`_parse_redaction_rules()`がpattern宣言を`Rule`、
   environment reference宣言を`EnvironmentRule`として区別して読み込む。
   `Config.redaction_rules`はpattern規則だけを保持（既存consumer互換）、
   environment referenceは新field `Config.environment_redaction_rules`へ保持。
   両方持つ項目・どちらも持たない項目・未知roleは`ConfigError`でfail-closed
   （例外文に入力値を含めない）。
3. `tools/session_logs/eventual_preservation.py`の`collect_source`と
   `reconcile_source_root`が`environment_redaction_rules`（keyword引数、既定`None`）を
   受け取り、規則が明示的に渡された経路は`redact_with_environment(..., strict=True)`で
   environment reference（長い値から）→pattern（登録順）→現行high-entropy検査の順に適用。
   Provenanceの`redaction_rules_sha256`はenvironment reference宣言＋pattern宣言から
   決定的に算出（役割名は入るが解決値は入らない）。
   `redaction_rules is None`の「伏字化派生物を作らない」契約と、environment宣言なしの
   既存呼出し（digest・伏字化結果とも従来と同一）は維持。

## 4. GREEN（Commit 2）のTest結果

| 区分 | command | 結果 | exit code |
| --- | --- | --- | --- |
| targeted | `.venv/bin/python3 -m pytest tests/test_redaction_registration_preservation_path.py` | 9 passed | `0` |
| 関連回帰 | `.venv/bin/python3 -m pytest tests/test_session_log_config_boundaries.py tests/test_session_log_portable_config.py tests/test_session_log_eventual_preservation.py tests/test_redaction_environment_rules.py` | 34 passed | `0` |
| 公式全Test | `.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt records/development/2026-08-08-redaction-registration-preservation-green-test-receipt-v1.json` | 1278 passed / status `passed` | `0` |

- `git diff --check`：指摘なし。
- RED commit後、Testは変更していない（実装側のみ修正）。

## 5. SHA-256

| file | SHA-256 |
| --- | --- |
| `tools/session_logs/config.py` | `af8651cc911b7d4afac2a4b02562b60cd408a21c98967a2c700d2392b1e4dc8c` |
| `tools/session_logs/portable_config.py` | `135faff2d565f36206ce8017f46fb0d016b1c883b66444537c7eec90ee93d34b` |
| `tools/session_logs/eventual_preservation.py` | `b66f6e9afb924ef99201ec2711441b2781923d4d7a8f7d9d5ad8a9519b76796c` |
| `tests/test_redaction_registration_preservation_path.py` | `157f0874032de2089153498d26c4e7f21138d2ac3307652ff051f9fe648ec57f` |
| 公式receipt（同上JSON） | `05fd70b9c9c31b0b57f6571e83a470fe1607c7811cd089471c70116ea15e0d56` |

## 6. 受入条件の確認結果（合成fixtureのみ）

- 解決値非漏洩：合成したhome directory・user name・host name・email・tokenが
  伏字化派生物に残らず、置換先は`[REDACTED:<label>]`である。設定file・Provenance本文にも
  合成解決値は出ない。規則digestは異なる合成環境の間で同一（宣言のみから算出）。
- fail-closed：patternで消えない高entropy合成値が残る場合は`CollectionError`となり、
  伏字化派生物・Provenance・cursorの成功状態を作らない。例外連鎖の文言に該当値は出ない。
- raw先行保全：fail-closed時もrawはprivate rootへ保全済み。通常経路ではrawと
  verbatimが従来どおりprivate rootへ保全され、対象の変造・削除はない。
- 冪等性：同じ固定入力の再実行は`action == "unchanged"`で、同一の伏字化結果と
  規則digestを生む。既存のpattern-only設定・明示的な空listの意味も維持。
- Testは実在の秘密・実在の保全データ・hostの実際のhome/user/hostnameを記録せず、
  `monkeypatch`と`tmp_path`による合成値だけを使用。

## 7. 未実施範囲とHuman境界

- 既存の保全済みデータ・`SENSITIVE_ROOT`・hostの実session logへの遡及適用は未実施
  （別のHuman判断）。
- `TODO_NEXT_SESSION.md`・initial checklist・Decision・Issue・Candidate・workflow台帳・
  既存Evidenceは未変更（完了反映はCodexの独立確認後）。
- push・外部送信・deployment・hook・watcher・schedulerの実行・変更は未実施。
- `tools/session_logs/redaction.py`（固定入力）は未変更。high-entropy検査の
  pattern・長さ・entropy閾値・allow pattern・位置づけも未変更。
