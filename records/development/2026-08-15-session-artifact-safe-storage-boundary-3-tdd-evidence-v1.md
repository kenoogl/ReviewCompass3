# Session記録安全保存 境界3 新規確定保存TDD Evidence v1

- 実施日：2026-08-15
- 対象境界：累積実装作業票v2＋v3の境界3「新規一記録の確定保存」
- 開始基準commit：`81d7f4d`
- 実施担当：主担当Codex

## 1. 目的

【判断】事前検査に合格した合成一件を二領域の固定fileへ保存し、作成物の安全属性と全内容を再確認した後、
`commit.json`を最後に置いて初めて`stored / committed: true`を返す。既存ID、途中復旧、同時更新、通常再読込み、
削除は扱わない。

## 2. RED

【実測】境界3の試験5例を追加した。正常例は次を再読込みして確認する。

- sensitive側は`operation.json`と`raw.bin`、data側は`operation.json`、`derived.json`、`manifest.json`、`commit.json`だけ
- 記録directoryは実効利用者所有・0700、通常fileは同所有者・0600、追加ACLなし、`.tmp`残存0
- rawは入力bytesと完全一致し、派生物は契約§3.1の許可項目だけで`provenance.source_path`がない
- raw、派生物、manifest、commit、operationの識別値が一致し、両rootのoperationが同一で`committed`
- `commit.json`が最後に公開され、結果・非raw保存物・固定名にraw秘密値、入力path、root、合成home・user・host値がない

残る4例は、作成直後の所有者、mode、追加ACL、file種類の検査が不合格なら`commit.json`を作らず停止することを要求する。

【実測】最初のREDでは、製品操作の前に観測hookを参照したため、`_publish_file`と`_validate_created_fd`不在という
二理由に分かれた。一つの主要理由へ揃えるため、未定義でもhookを差し替え可能にし、製品操作を先に呼ぶよう試験だけを訂正した。
期待する保存結果、反例、件数は変更していない。

【実測】訂正後に次を単独実行した。

```text
.venv/bin/python3 -m pytest -q tests/test_session_artifact_safe_storage.py -k store_new
```

- 終了コード：1
- 結果：5 failed、21 deselected
- 全例の主要な失敗理由：`AttributeError: module 'tools.session_logs.safe_storage' has no attribute 'store_new'`

【判断】新規一件の確定保存処理不在という一つの理由で全例が失敗し、境界3のREDとして正しい。

## 3. 最小GREEN

【実測】`safe_storage.py`へ次だけを追加した。

- 正式入口の正常結果から契約§3.1のtop-level項目とprovenance項目だけを新しい値へ複製する
- raw、派生物、規則、tool版、保持期限の識別値から決定的な64桁`record_id`を作る
- 明示した保存時刻より後のtimezone付き保持期限だけを受け付ける
- 二rootに記録directoryを排他的に0700で作り、open後に所有者、種類、mode、追加ACLなしを確認する
- 固定`.tmp`をnew-only・0600・symlink非追跡で作成し、file同期、再読込み、同一directory rename、directory同期、最終file再確認を行う
- 両rootへ同じ`incomplete` operation、raw、派生物、manifestを置き、operationを`committed`へ置換してから`commit.json`を最後に置く
- 成功結果は契約の最小8項目だけを返す

【実測】既存IDの再保存、途中状態の再開、競合、通常再読込み、期限切れ、削除計画、削除、製品入口は実装していない。

## 4. GREENと回帰確認

【実測】境界3試験を単独実行した。

```text
.venv/bin/python3 -m pytest -q tests/test_session_artifact_safe_storage.py -k store_new
```

- 終了コード：0
- 結果：5 passed、21 deselected

【実測】安全保存専用試験を単独実行した。

```text
.venv/bin/python3 -m pytest -q tests/test_session_artifact_safe_storage.py
```

- 終了コード：0
- 結果：26 passed

【実測】正式入口、pipeline、provenanceを含む関連試験を単独実行した。

```text
.venv/bin/python3 -m pytest -q tests/test_session_artifact_safe_storage.py tests/test_session_log_read_only_entry.py tests/test_session_log_pipeline.py tests/test_session_log_provenance.py
```

- 終了コード：0
- 結果：47 passed

【実測】`git diff --check`は終了コード0だった。変更後SHA-256は次のとおり。

- `tools/session_logs/safe_storage.py`：`8e03c35fc8167125d0f620391dbafc7015cb9f766a40dd80300c996111ca47d4`
- `tests/test_session_artifact_safe_storage.py`：`f7acae1a0bc3a9c8612f6f0c608f06d70720480d6f7f7755794bf7d4ad12c956`

## 5. 手戻り記録

【実測】対象操作はRED観測hookの準備、期待executorと実executorはともにpytestである。初回は製品操作より先に
内部hook属性を読む試験構造により二種類の`AttributeError`へ分かれた。手作業で試験の評価順を直し、同じ期待を
製品操作不在の一理由へ戻した。Evidenceは§2の前後command結果である。

【判断】原因は一回限りの新規hook配置であり、機械処理を追加するより既存の開始前方針と本Evidenceへrouteする方が
小さい。後続境界では、観測hookを製品操作呼出し前に必須参照しない。

## 6. 判断

【判断】境界3は訂正後のRED試験を変更せず最小GREENになった。保存物、属性、順序、Digest、安全出力を実fileから
確認し、専用26件、関連47件が成功した。境界4へ進む前に本単位をcommitする。

## 7. 未実施

【未実施】同一入力の`unchanged`、異なる内容の上書き拒否、同時更新、途中復旧、通常再読込み、保持期限後拒否、
削除計画、削除、製品入口、正規全試験、故障注入、独立完了レビュー、製品受入判断は実施していない。
外部送信、push、履歴書換えも行っていない。
