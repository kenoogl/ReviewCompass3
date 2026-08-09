# 範囲固定：参照Digest恒久検査器（deferred #5）

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 状態：範囲レビュー待ち（risk `high`提案のため、Humanのrisk確定と再開承認まで実装しない）

## 1. mode宣言と役割

```text
collaboration_mode: role_neutral_pilot_review
pilot: claude
reviewer: codex
closer: codex
work_item: deferred #5 参照Digest恒久検査器
           （裁定record：records/development/2026-08-09-deferred-items-triage-decision-v1.md）
```

受け渡しは`docs/development/pilot-driven-record-handoff.md`による。

## 2. risk提案

- 提案：`high`
- 根拠：本toolはrecordの参照（path＋SHA-256）の一致を判定する**守り役のcode**であり、
  誤りが「誤った合格」（改竄・欠落・古い参照の見逃し）として黙って現れる。
  `work-review-protocol.md` §3の既定`high`に該当する。
- 帰結：本文書のcommit後に範囲レビューを起動して停止し、Humanのrisk確定と
  再開承認を受けるまでREDを開始しない。

## 3. 目的と現状の穴

レビュー・範囲固定・依頼書の作成のたびに、path＋SHA-256の照合をその場のscriptで
書いて実行している（本session内だけで十数回）。TODOのEvidence欄は
`todo_handoff`が検証するが、**handoff record・Evidence・依頼書内の参照表を検証する
再利用可能な道具が無い**。都度scriptは書き誤り・検査漏れを機械的に防げない。

## 4. 開始状態

- branch：`main`
- base commit：`6eba2c4`（試行計測追記commit。`git log`で全SHA特定可能）
- 開始時worktree：clean

## 5. 固定入力

| role | path | SHA-256 |
| --- | --- | --- |
| 共通レビュー基準（§4.3 Digest再計算） | `docs/development/work-review-protocol.md` | `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772` |
| mode手順書 | `docs/development/role-neutral-pilot-review-collaboration.md` | `762580c54ad830895f029d87eb1a7b1b062bf7de4ac780cfd30ae57ec508279e` |
| 受け渡し方式 | `docs/development/pilot-driven-record-handoff.md` | `93c84dd6ddd86af12175a4e844334ec9d62633f9be5ba9e97bcfbe3a435e92f0` |
| 既存TODO検証入口（変更しない・役割重複させない） | `tools/development/todo_handoff.py` | `fbc6279b6471913f490b604940c14ef792b139e35819c951a0e4406ce5994d61` |
| digest共通正本（再利用のみ） | `tools/common/digests.py` | `db6b830592f5d57ef7b42b5ec32fd398f4c36957a978604166525fc54da3396f` |
| 参照表の形の実例1 | `TODO_NEXT_SESSION.md` | `edcf71de9ca8396882656a10e35563cb3b410dcf97b0e7bc1647f70bdf883ef5` |
| 参照表の形の実例2（裁定record） | `records/development/2026-08-09-deferred-items-triage-decision-v1.md` | `0171453f6025451d955b1dc08083ed06d2ccc28e8f110a3bb951ff97c48e3c91` |

## 6. 今回の最小E2E

新規`tools/development/reference_digest_checker.py`に、読み取り専用のCLI検査器を作る。

1. **入力**：検査対象のmarkdown record file（複数可、repository相対path）。
2. **抽出**：fileから「repository相対path＋64桁hex」の参照対を機械抽出する。対応する
   表記は次の2形だけとし、拡張しない。
   - 表形式：`` `path` `` のcellの後に `` `hex64` `` のcellが続く行
   - list形式：`[表示名](path) — SHA-256 \`hex64\``
3. **判定**：各参照対について、pathの実在（repository内・相対・脱出なし）と
   SHA-256再計算の一致を検査する。
4. **出力**：JSON（file別の checked／matched／mismatched／missing の件数と該当参照の
   path・行番号）。**全一致かつ抽出0件でない場合だけ**exit `0`、それ以外は exit `5`。
   file内容・期待値と実測値のhex以外の中身を出力しない。
5. **fail-closed**：参照対が1件も抽出できないfile、読めないfile、絶対path・`..`を含む
   参照、hex長不正は、合格にせず検査失敗として報告する（「参照0件で合格」を禁じる）。
6. 検査器自体はfileを作成・変更しない（読み取りのみ）。`todo_handoff`の役割
   （TODO本体の構造検証）は複製せず、変更もしない。

## 7. 受入条件

新規`tests/test_reference_digest_checker.py`。`tmp_path`の合成recordのみ使用。

正例：

1. 表形式・list形式の混在する合成recordで、全参照一致→exit `0`、件数がJSONで正しい。
2. 複数file入力で、file別の集計が正しい。
3. 実record形（固定入力の実例2形式に相当する合成）を抽出できる。

負例：

4. 1文字違いのdigest→mismatchedとして該当pathと行番号を報告しexit `5`。
5. 参照先fileの欠落→missingとして報告しexit `5`。
6. 絶対path・`..`を含む参照→fail-closedにexit `5`（検査対象外として黙って飛ばさない）。
7. 参照対が0件のfile→exit `5`（空合格の禁止）。
8. 読めないfile（不存在）→exit `5`。

境界例：

9. hexが63桁・65桁・大文字混じりは参照対として扱わず、そのfileの抽出0件判定に落ちる
   （偽の対を作らない）。
10. 同一pathが複数回参照される場合、各出現を独立に検査する。

## 8. 変更可能path

- `tools/development/reference_digest_checker.py`（新規）
- `tests/test_reference_digest_checker.py`（新規）
- `records/development/2026-08-10-reference-digest-checker-green-evidence-v1.md`（新規）
- `records/development/2026-08-10-reference-digest-checker-green-test-receipt-v1.json`（新規）
- `records/session-handoffs/2026-08-10-claude-pilot-reference-digest-checker-review-request-v1.md`（新規、実装完了後）

上記以外の変更が必要になったら停止する。`todo_handoff.py`・`digests.py`・既存record・
TODO・checklistは変更しない。

## 9. 停止条件

1. base・worktree・固定入力Digestの不一致。
2. §8以外のpath変更、特に既存検証toolの変更が必要。
3. 参照表記の2形で既存recordの主要な形を覆えず、表記の追加裁定が必要。
4. REDが今回の未実装以外の理由で失敗、または既存実装でGREEN。
5. targeted・関連回帰・公式全Test・diff check・receipt・Digest照合の不合格。

## 10. Test・validator・独立oracle

- targeted：`.venv/bin/python3 -m pytest tests/test_reference_digest_checker.py`（単独）
- 関連回帰：`tests/test_todo_snapshot.py`（TODO検証系の近接）、
  `tests/test_session_log_config_boundaries.py`（fail-closed系の近接）
- 公式全Test：`policy_test_runner --suite full --receipt records/development/2026-08-10-reference-digest-checker-green-test-receipt-v1.json`
- Reviewer向け独立oracle：`high`のため、Pilot fixtureに無い反証（改竄recordを誤って
  合格させる方向を優先）を最低1件機械実行する。

## 11. 予定するcommit境界

1. **SCOPE**（本commit）：本文書のみ。範囲レビュー起動→Human承認待ちで停止。
2. **RED**：Testのみ。単独実行で未実装だけを理由とする失敗とexit `1`確認後にcommit。
3. **GREEN**：実装・Evidence・receiptのみ。Testは変更しない。
4. **review request**：依頼書のみ（ignore検査exit `1`確認のうえ）。
