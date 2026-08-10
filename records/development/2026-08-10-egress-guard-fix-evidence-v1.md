# Evidence：group E（外部送信・機微境界）blocking 7件の修正

- 範囲固定：`records/session-handoffs/2026-08-10-claude-pilot-egress-guard-fix-scope-v2.md`
  （SCOPE v2 `4b52776`、範囲レビューv2 `verified`：`4e9ce51`）＋
  `…-scope-v3.md`（RED定義の改定、`8d2f3a4`）
- Human承認（2026-08-10）：「承認」（risk `high`確定・資格情報3形式・64桁hex除外規則・
  RED-1開始）、「RED定義の改定を承認する」
- 作成日：2026-08-10
- executor：Claude（Pilot。mode `role_neutral_pilot_review`、Reviewer=codex、Closer=codex）

## 1. commit系列（slice 1）

| 種別 | SHA | 内容 |
| --- | --- | --- |
| SCOPE v2 | `4b52776` | 範囲固定のみ |
| 範囲レビューv2 | `4e9ce51` | Codex作成。`verified`・blocking 0 |
| SCOPE v3 | `8d2f3a4` | RED定義の改定のみ |
| RED-1 | `ea7ccbb` | test 5 fileのみ |

## 2. RED-1（実装前・単独実行）

- command：`.venv/bin/python3 -m pytest tests/test_egress_approval.py
  tests/test_egress_gate.py tests/test_egress_payload.py
  tests/test_egress_prefilter.py tests/test_egress_adversarial.py
  tests/test_egress_dry_run.py`
- 結果：**63 failed, 44 passed**、exit `1`
- 失敗理由の内訳（機械集計）：`AttributeError` 27（`APPROVED_REDACTION_HOOK`・
  `load_approval_file`の不在）、`TypeError` 18（新契約の引数不在／旧引数の残存）、
  `AssertionError` 10・`Failed: DID NOT RAISE` 8（検証の欠落そのもの）
- file別：approval 30 failed/9 passed、gate 18 failed/0 passed、payload 1 failed/13 passed、
  prefilter 6 failed/15 passed、adversarial 8 failed/3 passed
- **更新していない既存test**：`tests/test_egress_dry_run.py` は **4 passed**（変更なし）
- environment：Python 3.9.6、pytest 8.4.2

### 2.1 契約更新した既存test（scope v3 §2.2の列挙義務）

旧契約（承認を辞書で渡す／caller提供`now`／任意callback）を写していたため、
呼び出し形のみを新契約へ更新した。**検査している性質は削除・緩和していない。**

| file | 更新した既存test | 更新内容 |
| --- | --- | --- |
| `test_egress_approval.py` | `TestValidateApprovalRecord`（`test_valid_record_passes`、`test_each_violation_is_rejected` 10 params）、`TestConsumption::test_mark_consumed_is_permanent` | `_validate`から`now=`を除去。基準recordの`expires_at`を実時刻基準で有効な将来日時へ。期限切れ反証は過去日時へ |
| `test_egress_gate.py` | `TestGateAllows`1件、`TestGateBlocks`5件、`TestStageOneSender`2件 | 承認を`approval_record_path`＋`approval_record_sha256`へ、hookを`APPROVED_REDACTION_HOOK`へ、`now=`を除去 |
| `test_egress_gate.py` | `test_redaction_masking_anything_is_blocked` | 任意lambdaでの「内容が変わったら拒否」を、**許可実装の伏字化が内容を変えた場合**の同性質検査へ置換（AWS key形式を含むsourceで再現） |
| `test_egress_adversarial.py` | `TestForgedContent` 3件（`_run` helper経由） | 同上の契約更新 |

### 2.2 追加した反証test

- F-E1：`TestExpiryUsesRealTime` 2件、`TestConsumedFieldIsStrict` 4件、
  `TestApprovalFileBinding` 5件、`TestApprovalIsBoundToHumanRecordFile` 4件、
  `TestApprovalForgeryIsRejected` 2件
- F-E2：`TestFragmentContentIsBoundToSource` 2件、`TestPayloadJsonIsCrossChecked` 2件
- F-E3：`test_approved_credential_formats_are_detected` 5 params、
  `test_digest_hex_is_not_reported_as_personal_identifier` 3 params、
  `TestCredentialScanCoversApprovedFormats` 4件
- F-E4：`TestThresholdsAreValidated` 7件
- F-E5：`TestInjectedCallbackIsRejectedBeforeExecution` 2件（**痕跡fileの不在**を確認）

## 3. GREEN-1実装

| finding | 実装 |
| --- | --- |
| F-E1 | `approval.load_approval_file(path, sha256=…)`を新設し、Human作成record fileのbytes・Digest一致・JSON解釈・7項目検証を一体で行う。`validate_approval_record`から`now`引数を削除し、期限は`datetime.now(timezone.utc)`で判定。`consumed`は`isinstance(bool)`必須（欠落・非boolは拒否）。`gate`・`sender`は`approval_record_path`＋`approval_record_sha256`のみを受け取る |
| F-E2 | `verify_fragment_provenance`が再切出し本文・Digest・本文の自己整合の3点を照合。`payload.fragment_document`と`machine_feature_violations`を公開し、gateが送信JSONの`fragment_a`／`fragment_b`／`machine_features_*`をpayload fieldと**相互照合**、許可field名の値の型・列挙も検査 |
| F-E3 | `_SECRET_PATTERNS`へ`AKIA/ASIA`＋16桁、`gh[pousr]_`＋20桁以上、`-----BEGIN … PRIVATE KEY-----`を追加。電話番号判定の前に`_DIGEST_HEX_PATTERN`（64桁hex）を除去し、Digest由来の誤検出を止める |
| F-E4 | `prefilter._validate_thresholds`を新設し、`classify_pair`の先頭で数値型・有限性・0..1範囲・`diff_max < same_min`・重み合計1をfail-closedで検査 |
| F-E5 | `gate.APPROVED_REDACTION_HOOK`（`tools.session_logs.redaction`の既定規則を適用する唯一の許可実装）を定義。gateは同一性が一致しないhookを**呼び出さずに**拒否し、`sender`は関門へ渡す前段で拒否する |

- 上流設計v4・保全設計・config・schemaは未変更。外部依存の追加なし。
- `tools/egress/`に通信手段（socket・http・urllib・requests・httpx・subprocess）は
  引き続き存在しない（反証4で機械確認）。

## 4. Test実行の記録（slice 1）

| 区分 | command | 結果 | exit code |
| --- | --- | --- | --- |
| RED-1（実装前） | 上記6 file | 63 failed / 44 passed | `1` |
| targeted GREEN-1 | 同上 | **107 passed** | `0` |
| 公式全Test | `policy_test_runner --suite full --receipt records/development/2026-08-10-egress-guard-fix-slice1-test-receipt-v1.json` | **1423 passed**、status `passed`（failed 0・error 0・skipped 0を再読込みで確認） | `0` |
| `git diff --check` | 各commit前 | 指摘なし | `0` |

## 5. 受入条件の対応（scope v2 §5、v3 §3）

1. 危険側：group E判定recordの反証のうちslice 1該当分（A1〜A3・P1・G1〜G3・F1・S1）は、
   同じ入力に対しすべて拒否側になった（§2.2の各testで固定）。
2. 副作用の不在：S1系は痕跡file（marker）が**存在しない**ことをgate・sender双方で確認。
3. 正例：64桁hexを含む正常payloadは個人識別子として拒否されない（3 params）。
   既定閾値の分類、正常な承認file経路、段階1の`EgressSendingNotApproved`は維持。
4. 件数：§7の6 test file合計 **107 passed**（RED-1前は69 passed。追加・更新後の全件）。
   公式全Test 1423 passed。
5. 実際の外部送信：未実施。段階1は関門合格後も`EgressSendingNotApproved`で停止する。
6. 上流・config・schema：未変更。

## 6. SHA-256（slice 1完了時点）

| file | SHA-256 |
| --- | --- |
| `tools/egress/approval.py` | `cb8f97e1d2b05f0ec7e9bad9e045c80b8378a03167be2d623f13853c3236b243` |
| `tools/egress/gate.py` | `ec611dfa65c0ff8f8ccf586ed491e944430cf80952a797861ea3b06a7f1de0c1` |
| `tools/egress/payload.py` | `daeb48b1ef3c00f7ae14ba1debfaba7efe564387808e505d57e4c15a14d34a1f` |
| `tools/egress/prefilter.py` | `c0b6a2da30923802eb419817d55bf8c2eb1f2e6a9a580074b1f90cd77773bf43` |
| `tools/egress/sender.py` | `05286fe21ee5baf264c80fe8518eccef3602de1c7ada6041e121dd4a2b5bbef8` |
| `tests/test_egress_approval.py` | `1cb52dc85a979a553b70964934dfd7544e8a34d9798f19006bb2e511c639dffb` |
| `tests/test_egress_gate.py` | `bd463b8013fe8df46598120c4aa329e765046b6c326d5076faebeaf0b199dfe4` |
| `tests/test_egress_payload.py` | `3bcac6b0fac87e93f878218d635a6621b9ff1184c6825ed72c58cbbc03e37f58` |
| `tests/test_egress_prefilter.py` | `6e44b223bd3b5b444832e0c5ac4d32b13b11d32099575ef1a7aa9ab9c429da1f` |
| `tests/test_egress_adversarial.py` | `e865785bbe30536adae69897cd63144e436dc290b5e27c61b76afada0f254da6` |
| 公式receipt（slice 1） | `c4c1a9287483ddb925cae86634368d63e40c66f534794d0c8ae5a36fc55ef34a` |

## 7. slice 2（保全：F-E6・F-E7）

上流：`docs/design/2026-08-03-session-transcript-eventual-preservation-design.md` §5.3
Raw Archive（追記専用・prefix検査・atomic replace・lock・integrity ledger）。

### 7.1 commit系列

| 種別 | SHA | 内容 |
| --- | --- | --- |
| GREEN-1 | `e7c25fa` | slice 1（`tools/egress/`・Evidence・receipt） |
| RED-2 | `f78a57e` | `tests/test_session_log_preservation.py`のみ |

### 7.2 RED-2（実装前・単独実行）

- command：`.venv/bin/python3 -m pytest tests/test_session_log_preservation.py`
- 結果：**4 failed / 4 passed**、exit `1`。既存4件は更新せずそのまま合格した
  （slice 2では既存testの契約更新は不要だった）
- 追加した反証4件：
  1. `test_tampered_backup_is_not_legitimised_by_a_later_preservation`（F-E6。
     保全を1回挟んで改変値を台帳の正本にできること、その後の復元で改変値が
     復元されることを反証）
  2. `test_raw_log_symlink_pointing_outside_root_is_rejected`（F-E7・読取り側）
  3. `test_backup_directory_symlink_escaping_root_is_rejected`（F-E7・書込み側）
  4. `test_restore_target_symlink_escaping_raw_root_is_rejected`（F-E7・復元側）

### 7.3 GREEN-2実装

| finding | 実装 |
| --- | --- |
| F-E6 | `_verify_existing_backup`を新設し、既存backupを**台帳へ照合してから**台帳を更新する順序へ変更。台帳entryと不一致のbackupは`PreservationIntegrityError`で拒否し、台帳を書き換えない（改変の正当化を断つ） |
| F-E7 | `_bind_inside_root`を新設し、raw・backup・復元先の各pathを**解決後**にroot内束縛で照合。`relative_to`も解決後pathで計算するため、最終component・祖先componentのsymlinkでroot外を読み書きできない |

- schema・config・上流設計・他moduleは未変更。lock・atomic replace・追記専用の
  既存性質は維持。

### 7.4 Test実行の記録（slice 2）

| 区分 | command | 結果 | exit code |
| --- | --- | --- | --- |
| RED-2（実装前） | `pytest tests/test_session_log_preservation.py` | 4 failed / 4 passed | `1` |
| targeted GREEN-2 | 同上 | **8 passed** | `0` |
| 関連回帰 | `pytest tests/test_session_log_eventual_preservation.py tests/test_preservation_migration.py tests/test_redaction_registration_preservation_path.py tests/test_session_log_pipeline.py` | 36 passed | `0` |
| 公式全Test | `policy_test_runner --suite full --receipt records/development/2026-08-10-egress-guard-fix-slice2-test-receipt-v1.json` | **1427 passed**、status `passed`（failed 0・error 0・skipped 0） | `0` |

### 7.5 SHA-256（slice 2完了時点）

| file | SHA-256 |
| --- | --- |
| `tools/session_logs/preservation.py` | `645e2430c15fe8bd8c4cabc94a21349335902299abefc533e9b363b02725ea5e` |
| `tests/test_session_log_preservation.py` | `bacb8ed2cff642269c2c3bd8762a043c07e4f5cd6f841dd3143e5bbddeff35f1` |
| 公式receipt（slice 2） | `dfa98e0f5d01e877cc8654eeec957c9a1942b0aa2cb94bd858d7c7329e333b06` |

## 8. 未実施

- group A〜Dのblocking 19件（裁定record `4bb1c9b`の順序に従い、A→B→C→Dで別単位）。
- TODO・checklist反映（Closer）。実際の外部送信、push、履歴書換え：未実施。
