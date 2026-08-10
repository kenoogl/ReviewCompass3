# Human裁定：group Cを白紙に戻し、赤を解消して区切る

- 裁定日：2026-08-10
- 裁定者：Human（kenoogl）
- 裁定文言（原文）：「組Cを白紙に戻し、赤を消して区切る」

## 1. 実施内容

group CのRED commit `431dd7b`（test 2 fileへの191行追加）を`git revert`で取り消した。

- 取り消しcommit：`c24e3b4`
- 履歴は書き換えず、打ち消しcommitを積む形で実施した。
- 取り消し後の公式全Test（機械出力）：

```text
1469 passed in 12.72s
```

赤（12 failed）は解消した。

## 2. 白紙に戻した理由

Codexの独立点検（`records/session-handoffs/2026-08-10-codex-review-result-group-c-readiness-v1.md`、
commit `63ca50d`、判定：実装着手不可・blocking 4件）が、REDが機能していないことを機械実証した。

- **`GC-READY-001`**：H1〜H6は反証ではなく**未実装引数による`TypeError`**で失敗していた。
  H1・H2・H6は入力が上流反証と不一致。U1は偽runnerと有効な基準receiptを欠く。
  U2・U4は存在しない。**正例2件も失敗**していた。
- **`GC-READY-002`**：v3は実装2 fileのみ許可だが、Humanは第3 module追加とv4再レビューを指示済み。
- **`GC-READY-003`**：巻き添え対象はPilot申告の9 fileではなく**10 file**。
  `test_todo_handoff_projection_repository.py`を落としていた。H3の実運用接続2経路も未接続。
- **`GC-READY-004`**：訂正REDに必要なtest修正承認とGREEN再開承認が未固定。

**Pilotが12 commitにわたり「testは書き終わり、実装のみ残る」と報告していた前提が誤りであった。**
testは1件も反証として機能していなかったため、取り消しによる損失は無い。

## 3. 現在の状態

- 守り役の重大Finding26件のうち、**14件が独立検証済みで修正完了**
  （group E 7件・group A 2件・group B 5件。いずれもCodexが反証を独立再実行して`verified`）。
- **残り12件は未修正**（group C 5件・group D 7件）。
- 公式全Test：**1469 passed**、worktree clean。
- group Cは範囲固定v1〜v3と各範囲レビューがcommitとして残るが、**RED以降は白紙**。
  再着手時はv4作成から始める。

## 4. 再着手時に満たすべき前提（点検record §7より）

1. 範囲固定v4の作成と`high`範囲レビューの`verified`。
   `todo_record_generation.py`の追加、巻き添え10 file、H3の実運用接続2経路を含めること。
2. 訂正REDが**上流10反証そのものを理由に失敗**すること、正例が合格することの機械確認。
3. RED後のtest変更承認とGREEN再開承認のHuman固定。

## 5. 本裁定が決めていないこと

- group C・group Dの再着手時期。
- 本日作成した方針・分析recordの最終的な扱い（廃棄裁定`c53b69c`のとおり参照は断つ）。
