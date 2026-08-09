# 範囲固定：V4 Issue resolve tool（deferred #1＝IC-V4-ISSUE-RESOLUTION-PERSISTENCE-GAP-001）

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 状態：`medium`簡易範囲レビュー待ち→Humanのrisk確定・再開確認まで実装しない

## 1. mode宣言と役割

```text
collaboration_mode: role_neutral_pilot_review
pilot: claude
reviewer: codex
closer: codex
work_item: deferred #1 ＝ V4 Issue state遷移の正規永続化tool
           （裁定record：records/development/2026-08-09-deferred-items-triage-decision-v1.md）
```

受け渡しは`docs/development/pilot-driven-record-handoff.md`による。

## 2. risk提案

- 提案：`medium`
- 根拠：workflow台帳への書込みを行うが、**new-onlyの新version record追加のみ**で既存fileを
  書き換えず（復旧可能・不可逆でない）、他の成果物の合否を決める検査器でもない。
  一方でstate遷移の誤りは「誤った解決状態」として台帳に残るため`low`ではない。
  `work-review-protocol.md` §3の既定`high`（守り役・不可逆）には該当しないと判断する。
  過小分類の当否はReviewerの簡易範囲レビューと完了レビューで検査する。

## 3. 開始状態

- branch：`main`
- base commit：`8fee385`（#5 Closer projection。`git log`で全SHA特定可能）
- 開始時worktree：clean

## 4. 固定入力

| role | path | SHA-256 |
| --- | --- | --- |
| **正式改善候補（scope・non_scope）** | `.reviewcompass/workflow/improvement-candidates/ic-v4-issue-resolution-persistence-gap-001--v1.json` | `90fad5def3a731f27c4c320a3074808bb170323b8661fdea46140cbbdbf2c231` |
| **Human defer Decision（当時。着手は2026-08-09裁定で承認済み）** | `.reviewcompass/workflow/triage-decisions-v4/dec-ic-v4-issue-resolution-persistence-gap-001--v1.json` | `01c3e15ab98cca964dc3776127f2205219e915a2c26bdb61ea8327a4e91db355` |
| 動機Issue（最初のresolve対象候補） | `.reviewcompass/workflow/issues-v4/issue-todo-handoff-verification-gap-001--v1.json` | `475b0ea27b331b1d44e3883a30c575d21ebd14ab14b894725e8aa9121e51bba5` |
| V4 intake実装（変更せず再利用のみ） | `tools/development/issue_intake_v4.py` | `42b797ad9e1aef81620a94a08c279a99c8daa7924329b44a54da1024cc9f4fde` |
| V4 config（issue_states・active・terminal定義） | `config/development-issue-resolution-pilot-v4.json` | `ed274e487318d44baed701ffbc8a1130df3e9d81cadca96515848a2bea228a8e` |
| deferred仕分け裁定（#1着手承認） | `records/development/2026-08-09-deferred-items-triage-decision-v1.md` | `0171453f6025451d955b1dc08083ed06d2ccc28e8f110a3bb951ff97c48e3c91` |
| 共通レビュー基準 | `docs/development/work-review-protocol.md` | `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772` |
| mode手順書 | `docs/development/role-neutral-pilot-review-collaboration.md` | `762580c54ad830895f029d87eb1a7b1b062bf7de4ac780cfd30ae57ec508279e` |
| 受け渡し方式 | `docs/development/pilot-driven-record-handoff.md` | `93c84dd6ddd86af12175a4e844334ec9d62633f9be5ba9e97bcfbe3a435e92f0` |

## 5. 今回の最小E2E

新規`tools/development/issue_resolution_v4.py`に、Human裁定に基づくV4 Issueの
resolved／rejected遷移を**正規永続化する明示CLI**を作る。

1. **入力**：対象issue record path、遷移先state（`resolved`または`rejected`）、Human裁定の
   根拠（human id、裁定日時、裁定文言を固定したrecordのpath＋SHA-256）、解決Evidenceの
   参照（path＋SHA-256、1件以上）。
2. **永続化**：workflow台帳の命名規則どおり`<issue_id>--v<N+1>.json`の**新version record**
   として書く（new-only）。既存recordは読み取りのみで書き換え・削除しない。
   `content_digest`は共通正本（`canonical_digest`）で再計算する。
3. **fail-closed検証（書込み前）**：
   - 対象recordの`content_digest`再計算一致（改竄・破損の拒否）
   - 対象が当該issue_idの**最新version**であること（後続version存在時は拒否）
   - 二重解決の拒否（既にterminal state＝configの`terminal_issue_states`にある場合）
   - 遷移先stateがconfigの`issue_states`に存在すること
   - 非Human裁定の拒否（human根拠の欠落・裁定record不読・Digest不一致）
   - Evidence参照のpath安全性（相対・`..`なし）とDigest一致
   - 同時active Issueとの整合（既存`validate_issue_set`等の再利用による検査）
4. **再利用**：`issue_intake_v4.py`の公開関数（digest・record検証・path規則・config読込）を
   変更せず再利用する。V4 Issue schema（schema_version 2・record_fields）は**変更しない**。
5. 失敗は型付き例外と安定stop codeで報告し、部分書込みを残さない（検証完了までfileを
   作らない）。CLIは検証・書込みの結果をJSONで出力し、成功exit `0`／失敗exit `5`。

**実Issueへの適用は本sliceに含めない**：動機Issue
（`ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`）等の実際のresolveは、toolの`verified`後に
Human裁定を得て別単位で行う。

## 6. schema境界の注意（範囲レビューでの確認観点）

resolution根拠（human id・裁定record参照・Evidence参照）を新version recordの**どこへ
載せるか**は、V4 Issue schemaのrecord_fields定義に従う。既存fieldsで表現できる場合のみ
実装し、**新fieldの追加が必要と判明した場合はschema変更に当たるため停止してHuman判断を
得る**（その場合の代替案：resolution根拠を別recordとして残しissue側はstateと既存参照
fieldだけ更新する、等の裁定をHumanへ提示する）。

## 7. 受入条件

新規`tests/test_issue_resolution_v4.py`。`tmp_path`の合成台帳・合成config・合成裁定record
のみ使用。

正例：

1. registeredのissueを、Human裁定根拠つきでresolvedの新version record（v2）へ遷移できる。
   既存v1は不変、v2のcontent_digestが再計算一致、CLI exit `0`。
2. rejectedへの遷移も同様に成立する。
3. 遷移後の台帳が既存検証（`validate_issue_record`・`validate_issue_set`）に合格する。

負例：

4. 二重解決（terminal state対象・後続version存在）の拒否。
5. 非Human裁定（human根拠欠落・裁定record不読・裁定Digest不一致）の拒否。
6. stale入力（対象recordのcontent_digest不一致）の拒否。
7. 未知の遷移先state・Evidence参照のpath逸脱・Digest不一致の拒否。
8. 検証失敗時に新version fileが作られない（部分書込みなし）。

境界例：

9. 同一issue_idの複数versionが並ぶ台帳で、最新版だけが遷移対象になる。
10. 遷移は対象issueのみに作用し、台帳内の他recordのbytesに影響しない。

## 8. 変更可能path

- `tools/development/issue_resolution_v4.py`（新規）
- `tests/test_issue_resolution_v4.py`（新規）
- `records/development/2026-08-10-issue-resolution-v4-green-evidence-v1.md`（新規）
- `records/development/2026-08-10-issue-resolution-v4-green-test-receipt-v1.json`（新規）
- `records/session-handoffs/2026-08-10-claude-pilot-issue-resolution-tool-review-request-v1.md`（新規、実装完了後）

上記以外は変更しない。`issue_intake_v4.py`・`issue_resolution_pilot.py`・config・
実workflow台帳（`.reviewcompass/workflow/`配下）・TODO・checklistは変更しない。

## 9. 停止条件

1. base・worktree・固定入力Digestの不一致。
2. §8以外のpath変更、特に実台帳・既存toolの変更が必要。
3. §6のschema境界：既存record_fieldsでresolution根拠を表現できない。
4. REDが今回の未実装以外の理由で失敗、または既存実装でGREEN。
5. targeted・関連回帰・公式全Test・diff check・receipt・Digest照合の不合格。
6. 実Issueのresolve実行が必要になった場合（別単位としてHumanへ）。

## 10. Test・validator・独立oracle

- targeted：`.venv/bin/python3 -m pytest tests/test_issue_resolution_v4.py`（単独）
- 関連回帰：`tests/test_issue_intake_v4.py`、`tests/test_issue_intake_v4_single_candidate.py`、
  `tests/test_issue_resolution_state.py`
- 公式全Test：`policy_test_runner --suite full --receipt records/development/2026-08-10-issue-resolution-v4-green-test-receipt-v1.json`
- Reviewer向け独立oracle：`medium`のため全Testを含む独立レビュー。反証は任意だが、
  「非Human裁定での遷移」「部分書込み」の方向を推奨。

## 11. 予定するcommit境界

1. **SCOPE**（本commit）：本文書のみ。`medium`簡易範囲レビュー起動→Human確認待ちで停止。
2. **RED**：Testのみ。単独実行で未実装だけを理由とする失敗とexit `1`確認後にcommit。
3. **GREEN**：実装・Evidence・receiptのみ。Testは変更しない。
4. **review request**：依頼書のみ（ignore検査exit `1`確認のうえ）。
