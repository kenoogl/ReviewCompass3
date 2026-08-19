# issue実態の突合 Human判断record v1

- 判断日：2026-08-19
- 判断者：利用者（Human）
- 記録者：Claude
- 判断の種別：issue台帳8件の実態突合（解決済みの終端遷移と維持の裁定）

## 1. 承認文言【記録】

> 推奨どおり裁定。1〜3をresolvedへ、4〜8は維持

（2026-08-19 chat。裁定材料の表は同日chatで提示——実態根拠・推奨・影響つき8行）

## 2. 遷移の機械record【実測】

`issue_state_transition`（2026-08-19新設・rollback付き）で3件を`registered`→`resolved`へ版遷移：

```text
ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001 → issues-v4/issue-todo-handoff-verification-gap-001--v2.json
ISSUE-HTC-66C3E6CA → issues-v4/issue-htc-66c3e6ca--v2.json
ISSUE-HTC-C9F6C917 → issues-v4/issue-htc-c9f6c917--v2.json
```

遷移後の一括検証`workflow_ledger_verify`＝**passed**（issue 8件＝registered 5・resolved 3・
findings空。候補勘定はvalidator 12・allowlist 1・決定束縛7——評価済み候補のevidence束縛の
版前進による分岐間移動は3分岐勘定の設計どおり）。旧v1 fileはgit履歴が保持する。

## 3. resolvedの根拠と残余

1. **TODO-HANDOFF-VERIFICATION-GAP**：単一入口`todo_handoff`が委譲先
   （`todo_update_path.default_verify`）で**compaction検証・参照digest照合・読み戻し照合を内包**
   することを実装で確認【実測】。運用中（本セッションで8回実行・全合格）。
2. **HTC-66C3E6CA（定型欄の手入力）**：測定ブロック（転記排除・二重実行guard）・計画writer・
   台帳writer往路復路の受入で対応済み【記録】。残余＝意味文の記述はLLMの役割（設計どおり・
   欠陥ではない）。
3. **HTC-C9F6C917（実行手順の都度組み立て）**：引数既定値化・writer群・測定ブロックで中核を
   機械化【記録】。**残余risk受容**＝Git・shell・Python cacheの定型化は行わない
   （2026-08-05仕分けrecordの裁定を維持。sandbox承認の迂回はしない）。

## 4. 維持5件の理由（要約）

TEST-GROWTH-STATE-PINNING＝既裁定「Issue状態を変更せず対象限定で再開」が有効／
TEST-SHA256-FIXTURE-DUPLICATION＝未着手／UNREVIEWED-WORK-REVIEW-BACKLOG＝部分進行
（旧C/D群残）／AUTHORITY-REFERENCE-DIGEST-CHECK＝着手前条件（allowlist宣言のHuman承認）未充足／
HTC-BEB5E0BD＝生ログ保持・削除・暗号化の方針未決（デプロイ前判断の種）。

## 5. 効果

- 台帳の`registered`が実態どおり5件になり、「実装済みなのに登録のまま」のずれが解消。
- checkpoint候補「issue実態の突合」は完了。復路道具（状態遷移・一括検証）の初回実運用を兼ねた。

## 6. 未実施

TODO反映とcommit。push（利用者の運用に従う）。維持5件の後続はそれぞれの合図・条件に従う。
