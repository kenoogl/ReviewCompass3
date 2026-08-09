# GREEN Evidence：authority参照Digest検査器（deferred #5）

- 範囲固定：`records/session-handoffs/2026-08-10-claude-pilot-reference-digest-checker-scope-v2.md`
  （SHA-256 `c37b7742a05592f514fac85f5bed606c8e396410a9df7deeac22a7afe46f9172`、SCOPE v2 `34f44da`、
  再範囲レビューv2 `verified`・blocking 0：`40ccd3b`）
- Human承認（2026-08-10）：「#5 risk highを確定、7 key allowlist（…7 key列挙…）を承認、
  RED開始を承認する」および「RED訂正を承認する」
- 作成日：2026-08-10
- executor：Claude（Pilot。mode `role_neutral_pilot_review`、Reviewer=codex、Closer=codex、risk `high`）

## 1. commit系列

| 種別 | SHA | 内容 |
| --- | --- | --- |
| SCOPE v2 base | `c7579ff` | 試行計測訂正 |
| SCOPE v2 | `34f44da` | 範囲固定のみ |
| 再範囲レビューv2 record | `40ccd3b` | Codex作成。`verified`・blocking 0・non-blocking 2（実装時確認事項） |
| RED | `c3bcb0f` | `tests/test_authority_reference_checker.py`のみ（455行、15 Test） |
| 訂正RED | `6706cff` | 同Testの数値2箇所のみ（fixture参照数の数え違い10→11・9→10。Human承認済み。検査の緩和なし） |

## 2. RED（実装前・単独実行）

- command：`.venv/bin/python3 -m pytest tests/test_authority_reference_checker.py`
- 結果：15件収集、15件全てが新module未実装（`ModuleNotFoundError`該当メッセージ15件を
  機械確認）だけを理由に失敗、exit `1`
- 訂正RED後（実装後）：数値訂正はfixture算数の誤りのみで、失敗理由の性質は不変
- environment：Python 3.9.6、pytest 8.4.2

## 3. GREEN実装

1. **allowlist宣言** `tools/development/authority_reference_keys.json`（新規）：
   Human承認済み7 key（`authority_order`・`operational_policy`・`policy_decision`・
   `related_design`・`intent_ref`・`glossary_ref`・`reconciliation_ref`）と期待形
   （mapping／mapping_list）、承認者・承認日・承認文言の所在を機械可読で固定。
   検査器が読む唯一の判別規則。
2. **検査器** `tools/development/authority_reference_checker.py`（新規）：読み取り専用CLI。
   - front matter（先頭`---`〜`---`）だけを対象に、allowlist宣言のkeyだけから
     `path`＋`sha256`を専用解析で抽出（汎用YAML不使用・外部依存追加なし）
   - path安全性（相対・`..`なし・resolve後もroot内＝symlink脱出拒否）、実在、
     現行bytesのSHA-256一致（`tools.common.digests.file_sha256`再利用）を検査
   - JSON出力（file別のchecked／matched／mismatched／missing／invalidと行番号）。
     全一致かつ検査対象1件以上のときだけexit `0`、それ以外exit `5`
   - fail-closed：許可key配下の不正形（sha欠落・hex長不正・絶対path・`..`）は
     invalid、参照0件fileは不合格（空合格の禁止）、allowlist・対象fileが読めない場合は
     `status: error`（安定stop codeのみ、内容非出力）
   - allowlist外key（`generated_from`等の時点固定pin）と本文は抽出せず合否に使わない

## 4. Test実行の記録

| 区分 | command | 結果 | exit code |
| --- | --- | --- | --- |
| RED（実装前・単独） | `.venv/bin/python3 -m pytest tests/test_authority_reference_checker.py` | 15 failed（全件ModuleNotFoundError） | `1` |
| targeted GREEN | 同上command | 15 passed | `0` |
| 関連回帰 | `.venv/bin/python3 -m pytest tests/test_todo_snapshot.py tests/test_layout_baseline.py` | 21 passed | `0` |
| 公式全Test | `policy_test_runner --suite full --receipt records/development/2026-08-10-authority-reference-checker-green-test-receipt-v1.json` | 1353 passed、status `passed`（再読込みでfailed 0確認） | `0` |
| `git diff --check` | 各commit前 | 指摘なし | `0` |

## 5. 受入条件の対応（scope v2 §8 → Test）

- 正例1〜2：7 key全種・複数fileの一致（11参照）／宣言によるkey制御 — 2 Test
- 負例3〜7：mismatch報告（key・path・行番号）／missing／不正形4態様／参照0件2態様／
  読めない入力2態様 — 10 Test
- 境界8〜10：時点固定pin非影響／同一path独立検査／本文非抽出 — 3 Test
- 実装時確認事項（再範囲レビューv2）：resolve後pathのroot外脱出拒否は実装済み
  （`_classify_reference`）、JSON集計と終了コードの一致は正例・負例の件数assertで固定

合計15件（parametrize展開後）、全て合格。

## 6. SHA-256

| file | SHA-256 |
| --- | --- |
| `tools/development/authority_reference_checker.py` | `8641ceb7fb615c217ff9d67fd15229409d6a30dd1fb3a443ce556a1425cb707f` |
| `tools/development/authority_reference_keys.json` | `560a835103765149f7e02b52876b6d2cec2e4817e7ec94c8ab1cfea85cd744b2` |
| `tests/test_authority_reference_checker.py` | `b6edd8ce4f9c598a8240eb7562fccdeb267404ba961fcd341f8813c6241e398c` |
| 公式receipt | `5de14a42510d26721327db1b610b2b0c9c66cff4ea2ed5c67a09cbb497a0f518` |

## 7. 禁止境界と未実施範囲

- `todo_handoff.py`・`todo_record_generation.py`・`digests.py`・docs実文書・既存record・
  TODO・checklist：未変更。参照Digestの自動書換えなし。
- 外部依存の追加なし（PyYAML等は不使用）。
- **実repository（docs配下の実文書）への適用は未実施**（scope §7-6どおり。検査器の
  `verified`後、Humanの指示で別単位として実行し、不一致があれば修復も別単位とする）。
- Issue `ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`のstate更新（resolve）は未実施
  （正規resolve toolはdeferred #1の対象。#1完了後の扱いはHuman判断）。
- push・tag・PR・履歴書換え・一括stage：未実施。
