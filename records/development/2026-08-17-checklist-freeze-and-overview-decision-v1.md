# 初期開発checklistの凍結と全体見取り図の新設 Human判断record v1

- 判断日：2026-08-17
- 判断者：利用者（Human）
- 記録者：Claude
- 対象：`docs/development/2026-08-03-initial-development-checklist.md`の扱い（現役維持か凍結か）と、
  人向け俯瞰資料の新設

## 1. 承認文言【記録】

> 案iiだが照合結果を見てから凍結を判断したい。照合までやって。現状の最新版のチェックリストは
> 不要か？

> 開発はそれでいいかもしれないが、人にはわからない。見通せる資料が必要

> セットで進める。添付メモ取り込み→見取り図v1起草→checklist凍結→Decision record→commitまで

（いずれも2026-08-17 chat。最後の一括指示により凍結と見取り図新設をセットで確定）

## 2. 照合結果【実測】

1. 凍結で失われる未正式化の方針・規則は**無い**。8/13〜15の方針コミット群（3案比較・lifecycle
   scope・TDD境界precheck・正式検索接続等）の実変更先は開発方針
   （`docs/development/2026-08-02-development-policy.md`）・AGENTS.md・個別Decision recordであり、
   checklist側は参照digestの1行追従だけだった（当初Claudeは「checklistが方針の追記先」と推測
   したが、差分照合で誤りと判明し訂正した）。
2. 更新実態：8/5〜8/15は活発（37回）、**8/16以降は更新ゼロ**。契約012〜014・record-run整備・
   デプロイ方針の全作業がchecklist非経由で進んだ（自然凍結の実測）。
3. checklistの残存価値は「Work体系での完了Evidence索引」と「未完了Work（7A残り・7B・8・8A・
   最終公開評価）の詳細」であり、読み取り専用で保存される。

## 3. 確定事項

1. **checklistを凍結**（`lifecycle: frozen`・冒頭に凍結宣言・以後更新しない読み取り専用の
   時点記録。参照digestは凍結時点の値で追従停止）。
2. **全体見取り図の新設**：`docs/current/reviewcompass3-overview-current.md`。人が全景と進捗を
   一目で見通すための資料（利用者指摘「開発はそれでいいかもしれないが、人にはわからない。
   見通せる資料が必要」への対処）。骨格は取り込み済みRC3全体計画メモのA〜F構造。状態語彙
   （完了／進行中／休止／未着手／凍結）と正本recordへの参照だけを持ち、詳細・履歴・件数を
   書かない。
3. **見取り図の更新規約**：作業単位の受入完了時（TODO更新と同時）にのみ状態欄を更新する。
   todo-handoff手順書の手順4へ組み込み済み（追従切れ＝第1世代checklistの失敗への対策）。
4. **「最新版checklist」は新設しない**：checklistの3役割は現行体制で分担済み——作業順・完了
   関門→契約・作業票の受入条件、現在位置→TODO（暫定。機械導出の方針はデプロイ方針record
   §4c）、完了記録→records。大きな1枚のchecklistへの回帰は追従切れの再現となるため行わない。
   全景の一覧性だけを見取り図が引き継ぐ。
5. 将来、現在位置の機械導出（計画正本§10.1.1）が実装されたら、見取り図はその人向け描画へ
   置き換える（見取り図の構造は導出出力の設計素案を兼ねる）。

## 4. 判断対象の束縛【実測】

```text
4654e952e9898b1b7cd15aa03e175afb6b75e7e7a851de8c307a62a3ef117520  docs/development/2026-08-03-initial-development-checklist.md
867f12748b008fc06e6b18ac36b3c9453caaeb2354ca7847b1b7fbb4053fd91c  docs/current/reviewcompass3-overview-current.md
601b2593940677ae06e4cace77628b000dbd8fcab746ea04a662889158f394ff  docs/design/2026-08-17-rc3-overall-plan-memo-import-v1.md
0fcf56fbaef1a09070f5e5390555545a2c6ef19206726b3be64ccbcab9180541  AGENTS.md
98cca5fcc0eccfb7661381dd654170720041c3b99eba6ffc6d6011f9047373a3  docs/development/prompts/todo-handoff-update.md
```

（値は凍結・新設commit後の機械計算。checklistの値は凍結宣言を含む凍結版のもの）

## 5. 付記：RC3全体計画メモ【判断】5点の現状対応（系譜整理の固定）

取り込み済みメモ（2026-08-10頃の停滞診断）の【判断】5点は次のとおり対応済みである。

| メモの【判断】 | 現状（2026-08-17） |
| --- | --- |
| 1. 計画と現在位置を一つの正本へ | 立て直し計画v5採用＋TODO handoff手順。残る機械導出はデプロイ方針record §4c（next最小形→本実装）で道筋固定 |
| 2. C群5件・D群7件の修正か明示延期 | v5 §10「過去資産の採用と不要物の整理」の枠組みへ吸収（一部は現役：`todo_handoff_projection.py`等） |
| 3. 一時的な範囲確認試験の分離 | `ISSUE-TEST-GROWTH-STATE-PINNING-001`として登録・条件付き再開待ち。全試験は安定（2026-08-16実測2,482件成功） |
| 4. Claude連携を限定範囲へ | pilot方式へ再編→レビュー基盤module（契約010〜013）として正式化・受入→2026-08-17休止 |
| 5. 安定部分の本線への取り込み | 手順書群・AGENTS.md入口・G30運用契約・正式経路として取り込み済み |

## 6. 未実施

- TODO handoffへの反映（本セットの受入完了の記載・見取り図は本recordで新設済みのため初回状態
  はcommit済み）。
