# 第3段 全試験からの現行正本矛盾候補抽出 Evidence v1

- 実施日：2026-08-14
- 状態：`candidate_extraction_completed_meaning_judgment_pending`
- 観測commit：`1483bdf2f3e52efc383912e14a4ebb17859c7b69`
- 対象Issue：`ISSUE-TEST-GROWTH-STATE-PINNING-001`
- 作業票：`docs/development/2026-08-14-stage3-test-authority-contradiction-candidate-extraction-bootstrap-work-ticket-v2.md`
- 作業票SHA-256：`79167fa82d194b9a85e5ae8762d8ef0fc394b271e52f95de2dc38f39ff8075b0`
- 作業票確認：`records/development/2026-08-14-stage3-test-authority-contradiction-candidate-extraction-scope-one-time-review-v1.md`
- 作業票確認SHA-256：`cdc8e46733eac0b9cd584bcaea46490f7a48a4566e5aab6552ada5d34958ba69`

## 1. 結果

【実測】観測commitの現役全試験1,728件を機械走査し、現行正本との矛盾候補を三つの意味群へ絞った。
候補は6試験file、試験識別子17件である。

【判断】この17件を修正または削除すると決めたものではない。候補Aは現在方針と試験期待の食い違いを
一時複製で直接再現できた。候補Bは非authority文書の参照整合を全試験の合否に使う必要性、候補Cは
暫定要件文書から正式な要件判断への接続範囲を、後続の意味確認で裁定する必要がある。

【実測】試験数、実行時間、作成時期、似て見えることだけを理由に候補へ入れたものは0件である。
コード、試験、設定、Issue、既存Decision・Evidenceは変更していない。

## 2. 全試験集合と機械抽出

観測commitをリポジトリ外へ`git archive`で展開し、次の単独commandを実行した。

```text
/Users/Daily/Development/ReviewCompass3/.venv/bin/python3 -B -m pytest --collect-only -q -p no:cacheprovider
```

【実測】終了コード0、試験識別子1,728件、重複0件だった。試験識別子を出力順に改行で結び、末尾にも
改行を一つ置いた内容のSHA-256は
`5a22372d02cf4708809a029603945a5b9ff4d5c7c06aea66468da198b60b62e1`で、作業票と一致した。

【実測】収集された試験fileは188件だった。これに`conftest.py`と試験専用helperを加えた189 sourceを
Python構文木と文字列検索で走査した。構文解析失敗は0件だった。

| 抽出した直接参照 | 異なる値の件数 |
| --- | ---: |
| 要求・Decision・Issue等のID | 194 |
| 文書・設定・コード等のpath | 362 |
| 64桁のSHA-256 | 21 |
| 合計 | 577 |

【実測】`records/development/`直下でfile名に`decision`を含む利用者判断記録97件を検索対象にし、577の
直接参照を完全一致で逆引きした。該当1件以上は64参照、該当0件は513参照だった。該当0件の内訳は、
path 339、ID 156、SHA-256 18である。

該当0件を一律に候補へはしなかった。存在しない異常入力、`tmp_path`配下の合成入力、コード・設定path、
計算結果のSHA-256は、採用または置換される正本ではない。既存のrepository文書で試験の期待結果を決める
参照だけを、正本候補として次段へ送った。存在するrepository pathで判断記録との完全一致が0件だったものは
82件であり、現在の入口・形式定義、正式な要件台帳、履歴互換性用の固定入力に機械分類した後、
正本外宣言または未解決の採用関係を持つものだけを候補に残した。

リポジトリ外の一時抽出結果は次の内容識別値だった。

| 一時物 | SHA-256 |
| --- | --- |
| 直接参照・逆引き結果JSON | `aecbb09fa2f4fe51ce7fb6a2af8bb685ce4868ce4f28fefd55aa93efb1143d47` |
| 抽出script | `8fc7a4e1819c7f21dd0097b24002476d0c6105d364fcbcc4e443d5bf40036ab3` |
| 置換語探索script | `3c5ff50ca90f23d0841eb1505ae05f5ae66c3e2d2273d5160dc7d115ca9e84ea` |

一時scriptは恒久toolではなく、全試験一覧と一緒にリポジトリ外へ置いた。

## 3. 候補A：暫定の旧計画を現在位置のauthorityとして受け入れる試験群

### 3.1 直接参照と現在方針

【実測】`docs/current/reviewcompass3-plan-current.md`は
`lifecycle: provisional`を宣言している。直接参照の逆引きは利用者判断記録5件に一致した。
2026-08-06の`DEC-WORK6A-PROJECTION-NON-AUTHORITY-SCOPE-001`は、当時、この文書を正当な固定入力として
拒否対象から外した。一方、現在の作業票v2 §3.3は、`provisional`文書を現行正本に含めず、配置や
file名の`current`だけでは正本とみなさないと固定している。

【判断】古い利用者判断を履歴から消す問題ではない。現在位置の判定に、暫定の旧計画を引き続き
authorityとして使う試験期待が残っていることが候補理由である。

### 3.2 候補の試験識別子

1. `tests/test_session_log_bootstrap.py::test_projection_reduces_major_state_events_deterministically`
2. `tests/test_session_log_bootstrap.py::test_projection_reports_conflicting_active_work_as_inconsistent`
3. `tests/test_session_bootstrap_e2e.py::test_captures_session_lifecycle_and_renders_current_work_e2e`
4. `tests/test_session_bootstrap_e2e.py::test_display_failure_does_not_discard_valid_capture_or_authority`
5. `tests/test_session_log_completed_next.py::test_work_completed_replaces_started_next_with_completion_next`
6. `tests/test_session_log_completed_next.py::test_work_completed_without_next_is_incomplete`
7. `tests/test_work6a_current_work_projection_negative.py::test_plan_authority_markdown_is_still_accepted`

### 3.3 試した反証

【実測】観測commitの無変更状態で関連4 fileを実行すると23件成功、終了コード0だった。

リポジトリ外の別複製で、既存の非authority固定入力一覧へ
`docs/current/reviewcompass3-plan-current.md`を一行だけ加えた。これは新機構ではなく、作業票v2 §3.3の
現在方針を既存の判定方法へ当てた反証である。同じ23件を実行すると、16件成功、上記7件失敗、終了コード1に
なった。失敗内容は、暫定文書を拒否した結果の`incomplete`または不足一覧を、試験が`complete`、`valid`、
不足0件としていた不一致だった。

【判断】正しい現在方針を実装するとこの7件が変更を妨げる可能性は、機械反証で成立した。修正方法と
G01完了判断への影響は、本抽出では裁定しない。

## 4. 候補B：非authority文書の参照整合を全試験の合否に使う一件

### 4.1 候補の試験識別子

- `tests/test_authority_reference_checker.py::test_approved_current_documents_match_all_allowlisted_references`

【実測】この試験は、初期開発チェックリストと暫定の旧計画を「承認済み2文書」として既存の全試験入口から
検査し、7 key・11参照の現在bytes一致を要求する。初期開発チェックリストは自身を進行確認用の入力とし、
完了authorityではないと宣言する。旧計画は`provisional`である。

【実測】観測commitではこの一件は成功、終了コード0だった。リポジトリ外の複製で、現行開発方針へ一行だけ
加え、初期開発チェックリスト側の参照SHA-256を更新しない状態を作ると、この試験だけが終了コード5を受けて
失敗した。

【判断】参照ずれ検出能力は実在し、G01実装完了判断も利用者判断で維持されている。未解決点は、現在の
設計判断そのものではない二文書について、参照更新を全試験の必須合否にすることが、正当な方針変更の
安全確認か、非authority文書による変更妨害かである。能力が動くことと維持の必要性を分け、候補として残す。

## 5. 候補C：暫定要件文書の採用範囲を限定逆引きできない九件

### 5.1 直接参照

【実測】`tests/test_requirements_artifact_layout.py`の補助関数`_fixture_records`は、
`docs/requirements/2026-08-02-task-contract-requirements-delta.md`の現在bytesからSHA-256を計算し、定義、Evidence、
候補、Decision、authority bundleの試験入力を組み立てる。この文書は`lifecycle: provisional`、
`normative_status: review-candidate`、`promotion_required: true`を宣言する。

【実測】このpathを`records/development/`のDecision記録へ完全一致で逆引きした結果は0件だった。一方、
`records/requirements/decisions/dec-requirements-added-13-2026-08-03-v1.json`はHumanによる13要件の承認を記録し、
`records/requirements/authority/rc3-requirements-authority-2026-08-03--v1.json`は対応する13定義を正式なbundleへ
含める。原文pathは定義・候補・Evidenceに残るが、Human Decisionは原文pathを直接参照せず候補の内容識別値を
参照する。

### 5.2 候補の試験識別子

1. `tests/test_requirements_artifact_layout.py::test_validates_minimum_artifacts_and_resolves_authority`
2. `tests/test_requirements_artifact_layout.py::test_rejects_invalid_definition_shape_identity_or_locator[missing_statement]`
3. `tests/test_requirements_artifact_layout.py::test_rejects_invalid_definition_shape_identity_or_locator[record_id_mismatch]`
4. `tests/test_requirements_artifact_layout.py::test_rejects_invalid_definition_shape_identity_or_locator[digest_mismatch]`
5. `tests/test_requirements_artifact_layout.py::test_rejects_invalid_definition_shape_identity_or_locator[unknown_field]`
6. `tests/test_requirements_artifact_layout.py::test_rejects_invalid_definition_shape_identity_or_locator[wrong_path]`
7. `tests/test_requirements_artifact_layout.py::test_directory_or_definition_alone_does_not_confer_authority`
8. `tests/test_requirements_artifact_layout.py::test_rejects_stale_candidate_or_evidence_binding`
9. `tests/test_requirements_artifact_layout.py::test_rejects_same_requirement_version_with_different_digest`

【実測】対象file全14件は観測commitで成功、終了コード0だった。

【判断】正式な要件bundleがあるため、直ちに矛盾とは判定しない。ただし、暫定原文の現在bytesを変えるだけで
試験入力全体の内容識別値が変わる一方、利用者の採用範囲は原文pathからの完全一致逆引きで確定できない。
作業票v2の0件時境界に従い、採用範囲を確認する未解決候補として残す。

## 6. 候補にしなかった主な集合

一件ごとの非候補台帳は作らず、機械条件ごとの集計だけを残す。

### 6.1 暫定宣言を持つ試験source

【実測】試験file 90件はmodule先頭に`lifecycle: provisional`を持っていた。試験file自身の成熟度だけでは、
期待結果が現行設計と反対とはいえない。暫定機能を試験することと、その試験を設計authorityにすることは
別であるため、この宣言だけでは候補にしなかった。

### 6.2 SHA-256とrepository状態の固定

【実測】64桁SHA-256の直接参照は21種類だった。共通module 5件の指紋固定は
`DEC-SHARED-FUNCTION-POLICY-001`の「変更はHuman承認」と一致した。ほかは、履歴Task ContractのGit blob、
不変の履歴bundle、承認済み外部送信試行材料、または合成入力の期待値だった。現行方針と反対の変更妨害は
この条件から追加で見つからなかった。

### 6.3 件数・file集合の固定

【実測】数値を含むassertionは949件だった。件数だけでは候補にせず、repositoryの`glob`、要求ID集合、
追跡対応表、履歴bundle等を固定する式を機械抽出した。正式要件集合、利用者承認済み範囲、凍結した旧lane、
一つの共通入口という現在規則に結び付くものは候補にしなかった。試験数や処理時間の削減理由には使っていない。

### 6.4 既知の処理呼出し目録問題

【記録】`compare_process_call_inventories`は、禁止関数を許可関数名として返す既知の欠陥を持ち、現在呼出し0件で
ある。現在の試験`test_process_inventory_baseline_matches_fixed_commit`は固定commitの目録再生成だけを検査し、
欠陥のある比較関数を安全と判定しない。したがって本作業の「誤った試験期待」候補には入れず、開発支援コードの
別問題として既存の後回し判断を維持した。

## 7. 停止条件の確認

【実測】全試験集合は固定値と一致し、構文解析失敗は0件だった。直接参照の逆引きが複数Decisionへ一致した
もののうち、候補Aの旧判断と現在方針の関係は時点と明文から区別できた。候補BはG01維持判断を併記し、
候補Cは一意に決めず未解決候補へ送った。全Decisionまたは全試験の人手総点検には戻っていない。

【判断】作業票§6の停止条件は発生していない。候補Cの意味判断は抽出後の利用者判断であり、抽出処理自体を
新機構へ拡張する理由にはしない。

## 8. 次の判断点

1. 候補Aについて、暫定の旧計画を現在位置authorityから外す方針を試験と開発支援コードへ反映するか。
2. 候補Bについて、G01の参照整合能力を維持しつつ対象文書の呼び方と合否境界を変えるか、現状維持にするか。
3. 候補Cについて、正式な要件Decisionが暫定原文のどの版・範囲を採用したかを確認し、現状維持または
   参照方法の修正へ送るか。

この三点は本Evidenceでは裁定しない。独立完了レビュー後、候補だけを利用者へ渡す。

## 9. 未実施

【未実施】試験の修正・削除・使用停止、開発支援コード・製品コード・設定・Issue・既存Decision・Evidenceの
変更、候補外試験の個別台帳、全Decisionの人手確認、新しい恒久tool・検査器・試験・関門、通常の全試験実行、
変異検査、第3段完了判断、Work 8評価、外部送信、push、tag、履歴書換えは行っていない。
