# 範囲固定 v2：V4 Issue resolve tool（deferred #1）— 案B・in-place遷移

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 状態：`high`範囲レビュー待ち→合格後、HumanのRED再開承認まで実装しない
- 先行版：`scope-v1`（SHA-256 `81c3d8f1741052e46505b3101c8b58f58d11e4a0dcaf54a0680d4d59533c8f86`、
  変更せず保持）。範囲レビューv1はIR-SCOPE-001／002でblocking判定。

## 1. Human裁定の固定（2026-08-10）

「#1 risk highを確定。案Bでscope v2を承認する。遷移元はregisteredのみとする」

- **risk：`high`（Human確定済み）**——レビューv1の判定どおり、本toolはHumanの解決承認と
  台帳identityを判定する守り役（状態遷移・保存）に該当する。
- **案B**：V4 Issue schemaも既存tool・configも変更しない。永続化は**既存Issue record
  fileのstateとcontent_digestのin-place更新**（file名・issue_version不変）とし、これを
  正規手段とすることをHumanが明示承認した。解決の根拠（Human裁定・Evidence参照）は
  `records/development/`の**解決record（new-only）**として別に残す。
- **遷移元は`registered`のみ**：`in_progress`やterminal stateからの遷移は許さない。

## 2. mode宣言と役割

```text
collaboration_mode: role_neutral_pilot_review
pilot: claude
reviewer: codex
closer: codex
work_item: deferred #1 ＝ V4 Issue state遷移の正規永続化tool（案B）
```

受け渡しは`docs/development/pilot-driven-record-handoff.md`による。

## 3. 開始状態

- branch：`main`
- base commit：`9d8667f`（範囲レビューv1 record。`git log`で全SHA特定可能）
- 開始時worktree：clean

## 4. 固定入力

scope v1 §4の9件（SHA-256は同表のとおり全件不変）に次を追加する。

| role | path | SHA-256 |
| --- | --- | --- |
| 先行scope v1（変更せず保持） | `records/session-handoffs/2026-08-10-claude-pilot-issue-resolution-tool-scope-v1.md` | `81c3d8f1741052e46505b3101c8b58f58d11e4a0dcaf54a0680d4d59533c8f86` |
| 範囲レビューv1結果（IR-SCOPE-001／002） | `records/session-handoffs/2026-08-10-codex-scope-review-issue-resolution-tool-v1.md` | `f4ed18c15a38ef41e4ed56ec9c6a4d6b075fbe51983c38c49315f1f2aa81bfcd` |

## 5. 今回の最小E2E（案B）

新規`tools/development/issue_resolution_v4.py`に、読み取り検証→原子的書込みの明示CLIを作る。

1. **入力**：対象issue record path、遷移先state（`resolved`または`rejected`）、Human裁定の
   根拠（human id、裁定日時、裁定文言を固定したrecordのpath＋SHA-256）、解決Evidenceの
   参照（path＋SHA-256、1件以上）、解決recordの出力path（`records/development/`配下）。
2. **書込み前のfail-closed検証**（すべて合格した場合だけ書く）：
   - 対象recordの`content_digest`再計算一致（stale・改竄の拒否）
   - 対象の現stateが**`registered`であること**（それ以外は拒否＝二重解決も自動的に拒否）
   - 遷移先がconfigの`issue_states`にあるterminal state（`resolved`／`rejected`）であること
   - Human根拠の完全性（欠落・裁定record不読・SHA-256不一致の拒否）
   - Evidence参照のpath安全性（相対・`..`なし）とSHA-256一致
   - 解決record出力pathがnew-only（既存fileがあれば拒否）で`records/development/`配下
3. **永続化**：
   - 対象issue record fileを**in-placeで更新**する：変更は`state`の値と`content_digest`の
     再計算（共通正本`canonical_digest`）だけ。他fieldの内容・file名・`issue_version`は
     不変。台帳内の他recordのbytesへ影響しない。
   - 解決recordを`records/development/`へnew-onlyで書く：対象issueの参照
     （path・issue_id・更新前後のcontent_digest）、遷移、human id・裁定日時・裁定文言の
     所在、Evidence参照を持つ。workflow schema registryには登録しない開発record。
4. **事後検証**：更新後の台帳に対し、`issue_intake_v4.py`の**正規検証**
   （`validate_v4_issue_record`と`validate_v4_issue_repository`）を実行し、合格を確認して
   から成功を報告する。浅い検査（`validate_issue_record`／`validate_issue_set`）だけを
   合格根拠にしない（レビューv1の指摘3の反映）。
5. **無変更保証**：検証失敗時は、issue file・解決recordのどちらにも変更・新規fileを
   残さない。事後検証failの場合も元のbytesへ戻して失敗を報告する。
6. **再利用**：`issue_intake_v4.py`の公開関数（digest・検証・path規則・config読込）を
   変更せず再利用。schema・config・既存toolを変更しない。
7. **実Issueへの適用は本sliceに含めない**：実台帳のresolveはtoolの`verified`後に
   Human裁定を得て別単位で行う。

## 6. 受入条件

新規`tests/test_issue_resolution_v4.py`。`tmp_path`の合成台帳・合成config・合成裁定record
のみ使用。

正例：

1. `registered`のissueが`resolved`へin-place遷移する：file名・issue_version不変、
   変更はstateとcontent_digestのみ、解決recordが必須fieldつきで作成され、CLI exit `0`。
2. `rejected`への遷移も同様に成立する。
3. 遷移後の台帳が**正規検証**（`validate_v4_issue_record`＋`validate_v4_issue_repository`）に
   合格し、台帳内の他recordのbytesが不変である。

負例：

4. 遷移元が`registered`以外（`in_progress`・`resolved`・`rejected`）の拒否（二重解決を含む）。
5. 非Human裁定（human根拠欠落・裁定record不読・裁定SHA-256不一致）の拒否。
6. stale入力（対象recordのcontent_digest不一致）の拒否。
7. 未知の遷移先state・Evidence参照のpath逸脱・SHA-256不一致の拒否。
8. 解決record出力pathの既存衝突（new-only違反）の拒否。
9. 検証失敗時にissue file bytesと`records/development/`のどちらにも変更が残らない。

境界例：

10. 複数issueが並ぶ台帳で、対象issueだけが変わり他はbyte不変。
11. 更新後recordのcontent_digestが、更新前とは異なる正しい再計算値になる
    （digest未更新のstate書換えを合格させない）。

## 7. 変更可能path

- `tools/development/issue_resolution_v4.py`（新規）
- `tests/test_issue_resolution_v4.py`（新規）
- `records/development/2026-08-10-issue-resolution-v4-green-evidence-v1.md`（新規）
- `records/development/2026-08-10-issue-resolution-v4-green-test-receipt-v1.json`（新規）
- `records/session-handoffs/2026-08-10-claude-pilot-issue-resolution-tool-review-request-v1.md`（新規、実装完了後）

上記以外は変更しない。`issue_intake_v4.py`・config・schema・実workflow台帳・TODO・
checklistは変更しない（toolの実行はTest内の合成台帳に限る）。

## 8. 停止条件

1. base・worktree・固定入力Digestの不一致。
2. §7以外のpath変更、特に既存tool・config・schemaの変更が必要。
3. in-place更新後の台帳が正規検証（repository検証を含む）に合格できないと判明。
4. REDが今回の未実装以外の理由で失敗、または既存実装でGREEN。
5. targeted・関連回帰・公式全Test・diff check・receipt・Digest照合の不合格。
6. 実Issueのresolve実行が必要になった場合（別単位としてHumanへ）。

## 9. Test・validator・独立oracle

- targeted：`.venv/bin/python3 -m pytest tests/test_issue_resolution_v4.py`（単独）
- 関連回帰：`tests/test_issue_intake_v4.py`、`tests/test_issue_intake_v4_single_candidate.py`、
  `tests/test_issue_resolution_state.py`
- 公式全Test：`policy_test_runner --suite full --receipt records/development/2026-08-10-issue-resolution-v4-green-test-receipt-v1.json`
- Reviewer向け独立oracle（`high`）：Pilot fixtureに無い反証を最低1件機械実行
  （推奨方向：非Human裁定での遷移、部分書込みの残留、`registered`以外からの遷移、
  台帳内の他recordへの影響、digest未更新のstate書換え）。
- 実装時確認事項（レビューv1 §5、non-blocking）：Evidence pathのresolve後root外脱出の
  拒否、new-only非上書きと失敗時無変更の確認、deferred #4（原子的filesystem競合防止一般）
  へは拡張しない。

## 10. 予定するcommit境界

1. **SCOPE v2**（本commit）：本文書のみ。`high`範囲レビュー起動→HumanのRED再開承認待ちで停止。
2. **RED**：Testのみ。単独実行で未実装だけを理由とする失敗とexit `1`確認後にcommit。
3. **GREEN**：実装・Evidence・receiptのみ。Testは変更しない。
4. **review request**：依頼書のみ（ignore検査exit `1`確認のうえ）。
