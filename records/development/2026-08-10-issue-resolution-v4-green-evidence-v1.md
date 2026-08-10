# GREEN Evidence：V4 Issue resolve tool（deferred #1・案B）

- 範囲固定：`records/session-handoffs/2026-08-10-claude-pilot-issue-resolution-tool-scope-v2.md`
  （SHA-256 `ddc4b312ca529f58c38f2ad90127e0ec5ef065b03ffb1af17c1b10076eff2ee7`、SCOPE v2 `21daf5e`、
  `high`範囲レビューv2 `verified`・blocking 0：`f7c2255`）
- Human承認（2026-08-10）：「#1 risk highを確定。案Bでscope v2を承認する。遷移元は
  registeredのみとする」および「RED開始を承認する」
- 作成日：2026-08-10
- executor：Claude（Pilot。mode `role_neutral_pilot_review`、Reviewer=codex、Closer=codex、risk `high`）

## 1. commit系列

| 種別 | SHA | 内容 |
| --- | --- | --- |
| SCOPE v2 base | `9d8667f` | 範囲レビューv1 record |
| SCOPE v2 | `21daf5e` | 範囲固定のみ |
| `high`範囲レビューv2 record | `f7c2255` | Codex作成。`verified`・blocking 0・non-blocking 3（実装時確認事項） |
| RED | `48bb6ad` | `tests/test_issue_resolution_v4.py`のみ（486行、16 Test） |

## 2. RED（実装前・単独実行）

- command：`.venv/bin/python3 -m pytest tests/test_issue_resolution_v4.py`
- 結果：16件収集、16件全てが新module未実装（`ModuleNotFoundError`該当メッセージ16件を
  機械確認）だけを理由に失敗、exit `1`
- environment：Python 3.9.6、pytest 8.4.2
- fixtureは既存intake testの正規生成経路を再利用（実configの読み取り専用利用・
  候補bundleのtmp複製・`build_human_triage_decision`→`build_v4_issue_record`）。
  実workflow台帳へは一切触れない。

## 3. GREEN実装

新規`tools/development/issue_resolution_v4.py`のみ。

- **in-place遷移（案B）**：`registered`のissueだけを対象に、`state`と`content_digest`
  （共通正本`canonical_digest`で再計算）のみ更新。file名・`issue_version`・他fieldは不変。
- **書込み前検証**：対象recordの正規検証（`validate_v4_issue_record`＝digest・path・
  裁定連鎖まで）、遷移元`registered`限定（二重解決を自動拒否）、遷移先はconfigの
  `issue_states`かつ`terminal_issue_states`、Human根拠（human id・裁定日時・裁定record
  path＋SHA-256の実在一致）、Evidence参照（1件以上、相対path・root内・SHA-256一致）、
  解決record出力pathのnew-onlyと`records/development/`限定。
- **事後検証**：更新後に`validate_v4_issue_record`＋`validate_v4_issue_repository`を実行し、
  失敗時は元bytesへ完全復元して`post_validation_failed`（解決recordも残さない）。
- **解決record**：対象issueの参照（issue_id・path・更新前後digest）、遷移、Human根拠、
  Evidence参照を持つJSONを`records/development/`へnew-onlyで作成。
- schema・config・`issue_intake_v4.py`は不変（公開関数の再利用のみ）。例外は安定
  stop codeのみ。

## 4. Test実行の記録

| 区分 | command | 結果 | exit code |
| --- | --- | --- | --- |
| RED（実装前・単独） | `.venv/bin/python3 -m pytest tests/test_issue_resolution_v4.py` | 16 failed（全件ModuleNotFoundError） | `1` |
| targeted GREEN | 同上command | 16 passed | `0` |
| 関連回帰 | `.venv/bin/python3 -m pytest tests/test_issue_intake_v4.py tests/test_issue_intake_v4_single_candidate.py tests/test_issue_resolution_state.py` | 67 passed | `0` |
| 公式全Test | `policy_test_runner --suite full --receipt records/development/2026-08-10-issue-resolution-v4-green-test-receipt-v1.json` | 1373 passed、status `passed`（再読込みでfailed 0確認） | `0` |
| `git diff --check` | 各commit前 | 指摘なし | `0` |

## 5. 受入条件の対応（scope v2 §6 → Test）

- 正例1〜3：resolved遷移（in-place・digest再計算・解決record必須field）／rejected遷移／
  正規検証合格と他record bytes不変 — 3 Test
- 負例4〜9：遷移元3態様（×3）／非Human裁定2態様（×2）／stale／遷移先・Evidence 4態様
  （×4）／record path 2態様（×2）／事後検証失敗の完全復元 — 12 Test
- 境界10〜11：複数issue台帳の局所性（正例3に統合）／digest再計算の正しさ（正例1に統合）
- 実装時確認事項（範囲レビューv2）：①事後検証の意図的失敗→完全復元・record非残留は
  負例9で固定、②Evidence pathのresolve後root外脱出拒否は実装済み（`_resolve_inside`）、
  ③`registered`以外の全宣言state・非Human根拠・stale・他Issue bytes不変はTestで固定

合計16件（parametrize展開後）、全て合格。

## 6. SHA-256

| file | SHA-256 |
| --- | --- |
| `tools/development/issue_resolution_v4.py` | `c4b5c57dcfe69b8ce87c370361171f8eaba664f38186f1fd3db54d43c6405216` |
| `tests/test_issue_resolution_v4.py` | `29be67ce761ad0449f1adc2ba5d58e8a9a1d27ebaade4b2d7a7c8c8586e2e4a6` |
| 公式receipt | `a4887275f7074302b464020b171effdd1691d14011589cfea348588326341fe5` |

## 7. IR-COMP-001〜003修正（完了レビューv1反映）

完了レビューv1（`records/session-handoffs/2026-08-10-codex-review-result-issue-resolution-v4-v1.md`、
判定`report_execution_mismatch`、blocking 3件）へのHuman裁定（2026-08-10
「IR-COMP-001と002の修正を承認する。IR-COMP-003は(a)scope改定とする」）を、
scope v3（`a873544`）に基づき修正した。**本節が§3のClaimと§6のDigestを再置換する。**

- 修正RED commit：`4f39479`（Test変更のみ：裁定fixtureをscope v3 §2の厳密形JSONへ更新
  ＋束縛違反6態様＋部分書込み障害注入2系統を追加。実装前は新規8件のみが反証どおり
  失敗、先行16件合格、exit `1`）
- **IR-COMP-001修正**：`_verify_ruling`を構造化束縛へ変更——厳密形field、
  `decision_maker == "human"`限定、human_id・decided_at（timestamp形式検査）のCLI一致、
  対象issue_id・遷移先の一致、wording非空。file同一性だけでは合格しない。
- **IR-COMP-002修正**：issue更新・復元・解決record作成のすべてを`_atomic_write`
  （一時file＋原子的置換、失敗時は対象不変・一時file残骸なし）へ変更。
- **IR-COMP-003**：scope v3 §1のHuman裁定により、実configの読み取り専用fixture利用が
  scope上正規化された（Test側の変更は不要）。
- Test結果（全て単独command）：targeted 24 passed（exit `0`）、関連回帰67 passed
  （exit `0`）、公式全Test 1381 passed・status `passed`（receipt更新・再読込みで
  failed 0確認）、`git diff --check`指摘なし。

| file | SHA-256（本節で有効） |
| --- | --- |
| `tools/development/issue_resolution_v4.py` | `770585427e6185730506ec6aa5da8004a79d77e2cee00e9b4210290d03a2bae8` |
| `tests/test_issue_resolution_v4.py` | `d1d09ab998ebed10a85a9f93613463ba756593052a214853d02b52aab749a4fb` |
| 公式receipt（更新済み） | `1f351b652e45722c4c64932841baa6957caae3d421fb2c1b7a53e1ea7544d006` |

## 8. 禁止境界と未実施範囲

- `issue_intake_v4.py`・config・schema・実workflow台帳・TODO・checklist：未変更。
- **実Issueのresolve実行は未実施**（動機Issue `ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`等の
  実適用は、toolの`verified`後にHuman裁定を得て別単位で行う）。
- 外部依存の追加なし。push・tag・PR・履歴書換え・一括stage：未実施。
