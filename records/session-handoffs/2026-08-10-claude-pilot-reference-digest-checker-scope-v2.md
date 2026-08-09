# 範囲固定 v2：authority参照Digest検査器（deferred #5＝ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001）

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 状態：再範囲レビュー待ち（risk `high`提案。Humanのrisk確定・allowlist承認・再開承認まで実装しない）
- 先行版：`scope-v1`（SHA-256 `00b02847dde7b602c87265863b52079f84f83abe36842aef4000c27eb06fce96`、変更せず保持）。
  範囲レビューv1はSR-P1-001（正式authorityとの対象不一致）でblocking判定。

## 1. Human裁定の固定

- 2026-08-10、HumanはSR-P1-001の二案から**「(a)で確定」**と裁定した：正式Issueどおり、
  Human承認済みkey許可一覧に限定した**front matter検査器**として#5を実施する。
- 本文参照表の検査（scope v1の方向）は#5に含めない。その需要（レビュー時の依頼書参照表の
  機械照合）は、観測として記録し**既存の改善候補経路**（観測記録→改善候補→Human仕分け）へ
  後日載せる。本sliceでは候補recordを作らない。

## 2. mode宣言と役割

```text
collaboration_mode: role_neutral_pilot_review
pilot: claude
reviewer: codex
closer: codex
work_item: deferred #5 ＝ ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001の解決slice
           （front matter authority参照のDigest検査器＋対象keyのallowlist宣言）
```

受け渡しは`docs/development/pilot-driven-record-handoff.md`による。

## 3. risk提案

- 提案：`high`（範囲レビューv1でも妥当と判定済み）
- 根拠：参照Digestの一致で他文書の現在有効性を判定する守り役のcode。誤りは
  「ずれの見逃し」または「正しい時点固定参照の誤拒否」として黙って現れる。

## 4. 開始状態

- branch：`main`
- base commit：`c7579ff`（試行計測訂正commit。`git log`で全SHA特定可能）
- 開始時worktree：clean

## 5. 固定入力

| role | path | SHA-256 |
| --- | --- | --- |
| **正式改善候補（scope・non_scope・対象key定義）** | `.reviewcompass/workflow/improvement-candidates/ic-authority-reference-digest-check-001--v1.json` | `d4e801aa35e4bd1ad2c17917d0cfd57b60e7e1aec93e7d1259bf8321285824c6` |
| **Human仕分けDecision（Issue昇格・allowlist先行承認の条件）** | `.reviewcompass/workflow/triage-decisions-v4/dec-ic-authority-reference-digest-check-001--v1.json` | `919f9c8803301297ed8a20e52333029020b17a4f8c7e24329fab1cf90f4a46bb` |
| **正式Issue** | `.reviewcompass/workflow/issues-v4/issue-authority-reference-digest-check-001--v1.json` | `d260ed570598f56ada2cd6b4e54f15543bba0e792db65c14403a038f8100afbe` |
| **参照種別Decision（現在有効／時点固定の区別）** | `records/development/2026-08-07-fixed-source-kind-decision-v1.md` | `07f891b5885fd13bfd9c736fccc29013034f665f9d2bbd85fa073b73b5614929` |
| deferred仕分け裁定（#5着手承認） | `records/development/2026-08-09-deferred-items-triage-decision-v1.md` | `0171453f6025451d955b1dc08083ed06d2ccc28e8f110a3bb951ff97c48e3c91` |
| 範囲レビューv1結果（SR-P1-001） | `records/session-handoffs/2026-08-10-codex-scope-review-reference-digest-checker-v1.md` | `397a367f66d4809620dc967d24cd4ec4438560ee431a6b8f4ee8921a8e07e721` |
| front matter実例1（検査対象の形） | `docs/development/2026-08-03-initial-development-checklist.md` | `4bf42b4bce858bdc2e299a08582e94411698db2e143a0af4b47840712756f38c` |
| front matter実例2 | `docs/current/reviewcompass3-plan-current.md` | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` |
| digest共通正本（再利用のみ） | `tools/common/digests.py` | `db6b830592f5d57ef7b42b5ec32fd398f4c36957a978604166525fc54da3396f` |
| Evidence節照合の先行例（参照のみ・変更しない） | `tools/development/todo_record_generation.py` | `4b09d48eb2ac3e545e1aa70b9f51e630ee07ff93d1b4a6d45112a3961c6789cd` |
| 共通レビュー基準 | `docs/development/work-review-protocol.md` | `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772` |
| mode手順書 | `docs/development/role-neutral-pilot-review-collaboration.md` | `762580c54ad830895f029d87eb1a7b1b062bf7de4ac780cfd30ae57ec508279e` |
| 受け渡し方式 | `docs/development/pilot-driven-record-handoff.md` | `93c84dd6ddd86af12175a4e844334ec9d62633f9be5ba9e97bcfbe3a435e92f0` |

## 6. allowlist宣言（Human承認の対象）

正式改善候補のscopeどおり、「現在有効な上位文書」を意味するfront matter keyを次の
**7 keyに限定**して機械可読宣言する。承認後の追加・削除はHuman承認事項とする。

```text
authority_order, operational_policy, policy_decision, related_design,
intent_ref, glossary_ref, reconciliation_ref
```

- 宣言の置き場所：`tools/development/authority_reference_keys.json`（新規。検査器が読む
  唯一の判別規則。key一覧と各keyの期待形〔単一mapping／mappingのlist〕を持つ）
- `generated_from`等の時点固定keyは宣言に含めず、検査対象にしない
  （`DEC-FIXED-SOURCE-KIND-001`の`pinned_at_start`区別に従う）。
- **この7 key宣言そのものが、Humanの承認文言を要する**（仕分けDecisionの
  `next_action`どおり）。承認はrisk確定・RED再開承認と同じmessageでよい。

## 7. 今回の最小E2E

新規`tools/development/authority_reference_checker.py`に読み取り専用CLI検査器を作る。

1. **入力**：検査対象のmarkdown file path（複数可）。
2. **解析**：file先頭の`---`〜`---`のfront matterから、allowlist宣言に載ったkeyだけを
   対象に`path`＋`sha256`の参照対を抽出する。汎用YAML解析器は使わず・作らず、
   宣言された期待形（`key:`直下の`path:`／`sha256:`、または`- path:`／`sha256:`のlist）
   だけを受け付ける専用解析とする。外部依存を追加しない。
3. **判定**：各参照対で、pathの安全性（相対・`..`なし・repository内）、実在、
   現行bytesのSHA-256一致を検査する。
4. **出力**：JSON（file別・key別のchecked／matched／mismatched／missingと行番号）。
   全一致かつ**検査対象参照が1件以上**の場合だけexit `0`、それ以外exit `5`。
5. **fail-closed**：allowlist key配下の解釈不能な形（`sha256`欠落、hex長不正、絶対path、
   `..`）は失敗として報告する。allowlistに無いkey（時点固定pin等）は**検査せず合否にも
   使わない**。参照Digestの自動書換え・fileの作成変更は行わない。
6. 実repository（docs配下の実文書）への適用と、そこで見つかる不一致の修復は
   **本sliceに含めない**（検査器の`verified`後、Humanの指示で別単位として実行する）。

## 8. 受入条件

新規`tests/test_authority_reference_checker.py`。`tmp_path`の合成file・合成allowlistのみ使用。

正例：

1. 7 key全種（単一mapping・list混在、複数file）で全一致→exit `0`、JSONの件数一致。
2. 参照対の抽出はallowlist宣言fileの内容に従う（宣言からkeyを外すと検査対象から消える）。

負例：

3. 1文字違いdigest→mismatched（path・key・行番号を報告）でexit `5`。
4. 参照先fileの欠落→missingでexit `5`。
5. allowlist key配下の`sha256`欠落・hex長不正・絶対path・`..`→fail-closedにexit `5`。
6. front matterが無い、または対象参照0件のfile→exit `5`（空合格の禁止）。
7. 読めない対象file・読めないallowlist宣言→exit `5`。

境界例：

8. **allowlist外のkey（例：`generated_from`）が古いDigestを持っていても合格に影響しない**
   （現在有効／時点固定の区別の核心）。
9. 同一pathを複数keyが参照する場合、各出現を独立に検査する。
10. front matter終端後の本文に64桁hexがあっても抽出しない（本文はnon_scope）。

## 9. 変更可能path

- `tools/development/authority_reference_checker.py`（新規）
- `tools/development/authority_reference_keys.json`（新規。Human承認済みallowlist）
- `tests/test_authority_reference_checker.py`（新規）
- `records/development/2026-08-10-authority-reference-checker-green-evidence-v1.md`（新規）
- `records/development/2026-08-10-authority-reference-checker-green-test-receipt-v1.json`（新規）
- `records/session-handoffs/2026-08-10-claude-pilot-reference-digest-checker-review-request-v1.md`（新規、実装完了後）

上記以外は変更しない。`todo_handoff.py`・`todo_record_generation.py`・`digests.py`・
既存record・docs実文書・TODO・checklistは変更しない。

## 10. 停止条件

1. base・worktree・固定入力Digestの不一致。
2. §9以外のpath変更が必要。
3. 7 keyの宣言で実front matterの現在有効参照を表せない、または汎用YAML解析・外部依存が
   必要と判明（対象keyの追加・形の拡張はHuman承認事項として停止）。
4. REDが今回の未実装以外の理由で失敗、または既存実装でGREEN。
5. targeted・関連回帰・公式全Test・diff check・receipt・Digest照合の不合格。
6. 実文書の不一致修復や参照書換えが必要になった場合（別単位としてHumanへ）。

## 11. Test・validator・独立oracle

- targeted：`.venv/bin/python3 -m pytest tests/test_authority_reference_checker.py`（単独）
- 関連回帰：`tests/test_todo_snapshot.py`、`tests/test_layout_baseline.py`
- 公式全Test：`policy_test_runner --suite full --receipt records/development/2026-08-10-authority-reference-checker-green-test-receipt-v1.json`
- Reviewer向け独立oracle：`high`のため、Pilot fixtureに無い反証を最低1件機械実行する
  （正しい時点固定参照を誤拒否する方向と、allowlist key内のずれを見逃す方向を優先）。
- 実装時確認事項（範囲レビューv1 §5、non-blocking）：resolve後pathのrepository外脱出の
  拒否、JSON集計と終了コードの一致。

## 12. 予定するcommit境界

1. **SCOPE v2**（本commit）：本文書のみ。再範囲レビュー起動→Human承認待ちで停止。
2. **RED**：Testのみ。単独実行で未実装だけを理由とする失敗とexit `1`確認後にcommit。
3. **GREEN**：実装2 file・Evidence・receiptのみ。Testは変更しない。
4. **review request**：依頼書のみ（ignore検査exit `1`確認のうえ）。
