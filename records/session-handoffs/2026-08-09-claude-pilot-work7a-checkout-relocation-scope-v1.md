# 範囲固定：Work 7A第2項 別checkout・project移動後のBinding／Snapshot／Change Set復元

- 作成日：2026-08-09
- 作成者：Claude（Pilot）
- 状態：範囲レビュー待ち（risk `high`のため、実装はHuman再開承認まで開始しない）

## 1. mode宣言と役割

```text
collaboration_mode: role_neutral_pilot_review
pilot: claude
reviewer: codex
closer: codex
work_item: Work 7A第2項（別checkoutとproject移動後にProject Binding、Source Snapshot、
           Change Setを復元・照合できることをTDDで固定する）
```

Humanは2026-08-09にmode・役割・work itemを明示し、riskを`high`と確定した。

## 2. risk提案と確定

- 提案：`high`
- 根拠：本作業はProject Bindingの照合とSource Snapshot／Change Setの復元照合という
  「他の成果物の合否を決める守り役のcode」であり、失敗が誤った合格として黙って現れる。
  `work-review-protocol.md` §3の既定`high`（守り役のcode）に該当する。
- Human確定：`high`（mode宣言時に確定済み）
- 帰結：本文書のcommit後に停止し、Reviewer（Codex）の範囲レビューとHumanの再開承認を
  受けるまでREDを開始しない。

## 3. 開始状態

- branch：`main`
- base commit：`932d24697d4ee2f116b53a1bb4557527a2bf0023`
- 開始時worktree：clean（機械確認済み）

## 4. 固定入力

| role | path | SHA-256 |
| --- | --- | --- |
| 現在位置（次の一作業の定義元） | `TODO_NEXT_SESSION.md` | `19fd2246f87eeca4bbbcc8287d7a9400482240bee0d6455a1949a69aed842b15` |
| Work 7A checklist（第2項） | `docs/development/2026-08-03-initial-development-checklist.md` | `496a028e22c5f07ce54b670cdc6a6425d4e45252e5f5841cfc1cb620f46c3a1c` |
| Plan（Work 7A節） | `docs/current/reviewcompass3-plan-current.md` | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` |
| 用語集（Project Binding定義） | `docs/current/reviewcompass3-glossary-current.md` | `f1e7e9a9c57292fe911217d9b4f5d5b8ed99a881d6f113f9b60db1f0d01b19fa` |
| 第1項 独立レビューEvidence（開始条件） | `records/development/2026-08-09-work7a-four-root-separation-independent-review-evidence-v1.md` | `5418bc5839cd01cf8f6b99088c33108fb83fb366fa7a49ff773959e556fab1ec` |
| Layout v3固定record | `records/development/2026-08-04-layout-baseline-v3-project-first-candidate.json` | `4f469acd6c3122c2c7e5a83224f5cc610ffe309b561a369697ea669ccf7b7f38` |
| Layout v3承認Decision | `records/development/2026-08-04-layout-baseline-v3-project-first-approval-decision.json` | `793be4403d37806b41696031abf6576c98bc2047f28574e0792d3c6ab8ae6275` |
| deployment／Project Artifact境界Decision | `records/development/2026-08-04-deployment-project-artifact-boundary-decision.json` | `237dd1d0d40304240f0d8376713509c34364aaa6369d3161df3d3be2cc623c1b` |
| Binding既存実装（再利用のみ） | `tools/layout/baseline.py` | `6d00c3053da820cd694a0c4b47d5e5f1b632f00d83e81691f99060626bc94cb7` |
| Snapshot／Change Set既存実装（再利用のみ） | `tools/task_contract/execution.py` | `32035909a96e6ce28f19792716b5d3e49b7132f6f8e316c1287679c9da291cd0` |
| record identity共通規則（再利用のみ） | `tools/task_contract/identity.py` | `bbbce848e3beb50301c2ef4e242a75daf64968a0d5c1f2f733751ac2a75a5c42` |
| 第1項実装（再利用のみ） | `tools/deployment/local_integrated_roots.py` | `31e4e319c366cfbf51d58b691c11bdf6fb7c43636ac9ad3bfa7777c43cb5a149` |
| Layout既存Test（回帰対象） | `tests/test_layout_baseline.py` | `cdefaa57d8a41d59ac5275d55bd3498682f76bdd901eaf9efc31692883143ec0` |
| 第1項Test（回帰対象） | `tests/test_work7a_local_integrated_root_separation.py` | `7ec546a5aa6784cbce1c126f2950a80ee21d43459780aae8f267b7dbdd8b1d88` |
| 本mode手順書 | `docs/development/role-neutral-pilot-review-collaboration.md` | `856f5508787af653ecc2227a7f6376754963fdc42d61a1e98c577a01875af9ba` |
| 共通レビュー基準 | `docs/development/work-review-protocol.md` | `a3c6b608d243dd07ab5c9a1d9726c84e6ce71c498b3f134b6bfff2d5a7adbf37` |

## 5. 上流authorityとの関係

- TODO「次に行う一作業」＝本work item。開始条件（Humanの着手指示、第1項Evidenceと既存
  Binding・Snapshot・Change Set authorityの固定入力化、第2項への限定）を本文書で満たす。
- checklist §11第2項「別checkoutとproject移動後にBinding、Snapshot、Change Setを復元できる」。
- Plan Work 7A節「Repository Binding、Source Snapshot、Change Set、Verification Runを
  別checkoutでも復元・照合できること」のうち、**Verification RunはTODOの第2項定義に含まれて
  いないため本sliceの範囲外**とし、未実施範囲に明記する。
- 用語集：Project Bindingは「project IDと特定checkoutまたは配置を結ぶ記録。projectの移動や
  複数checkoutをProject Manifestの書換えで表さない」。本sliceはこの定義を不変条件とする。
- Layout v3：`binding_directory: deferred_until_concurrent_checkout_need`。本sliceは
  **Bindingの耐久保存（binding directory新設）を行わない**。記録は値（呼出し側が保持する
  record）として扱い、保存先の設計が必要になった場合は停止してHuman判断へ渡す。

## 6. 今回の最小E2E

新module `tools/deployment/checkout_relocation.py`（新規、namespace package配下、
`__init__.py`追加なし、4スペースindent）に、次の公開APIを最小構成で作る。

1. **捕捉（checkout Aで実行）**：既存APIだけを組み合わせ、合成project checkoutから
   Project Binding（`validate_project_layout`）とSource Snapshot＋Change Set
   （`read_source_snapshot`）を作る。新しいrecord schema・record kindは作らない。
2. **復元・照合（checkout Bで実行）**：project一式を別pathへ移動（または複製checkout）した
   後、次を照合・導出する公開APIを作る。
   - **identity保持の照合**：新checkoutのProject Manifestから読んだ`project_id`と
     manifest digestが、捕捉時のBinding記録と一致すること。
   - **Bindingの更新**：一致した場合だけ、新checkout向けの新Binding
     （新`checkout_id`・新`repository_root`、同一`project_id`、既存schema_version 1）を
     導出する。Project Manifestは書き換えない。旧Bindingが新checkoutで
     `validate_project_binding`により拒否されることは前提であり、変更しない。
   - **Snapshot／Change Setの復元照合**：Change Setの`changed_paths`を新checkout上で
     project相対pathとして再読取りし（`safe_relative_path`再利用）、Snapshotの各file
     SHA-256および`content_digest`（`seal`済record）との一致を照合する。
3. 全経路はread-only（Gitへ書かない、Manifest書換えなし、耐久保存なし、directory作成なし）。
   照合失敗・改変・欠落・path逸脱・schema不一致は、型付き例外と安定stop codeで
   fail-closedに拒否し、例外文へhost pathや未検査内容を出さない。

## 7. 受入条件

Acceptance Testは新規`tests/test_work7a_checkout_relocation.py`に書き、`tmp_path`の
合成fixtureだけを使う。公開APIの入出力とfilesystem事後状態をoracleにする。

正例：

1. 移動後checkoutで identity照合が成立し、新Bindingが導出される（同一`project_id`・
   同一manifest digest・新`repository_root`・新`checkout_id`）。導出結果は
   `validate_project_binding`で新checkoutに対し合格する。
2. 移動後checkoutでSnapshot／Change Setの復元照合が成立する（全file SHA-256一致、
   `content_digest`一致）。
3. 同じ入力での照合は決定的（2回実行で同結果）で、照合・導出は何も作成・変更しない
   （移動後checkoutのinventory不変）。

負例：

4. Manifest改変（`project_id`変更）後のrebindを拒否する。
5. Snapshot対象fileの改変・欠落で復元照合が失敗し、部分的成功を返さない。
6. 旧Bindingをそのまま新checkoutへ適用すると拒否される（既存挙動の固定）。
7. `changed_paths`の脱出path（絶対path・`..`）を拒否する。
8. Manifest欠落・不正なcheckoutでのrebindを拒否する。

境界例：

9. 移動なし（同一checkout）でも捕捉→照合が成立する。
10. record改竄（`content_digest`不一致）を拒否する。

## 8. 変更可能path

- `tests/test_work7a_checkout_relocation.py`（新規）
- `tools/deployment/checkout_relocation.py`（新規）
- `records/development/2026-08-09-work7a-checkout-relocation-green-evidence-v1.md`（新規）
- `records/development/2026-08-09-work7a-checkout-relocation-green-test-receipt-v1.json`（新規）
- `records/session-handoffs/2026-08-09-claude-pilot-work7a-checkout-relocation-review-request-v1.md`（新規、実装完了後）

本文書自体の改版が必要な場合は履歴を書き換えず`-scope-v2`を新規commitする。
上記以外の変更が必要になったら実装せず停止する。

## 9. 禁止事項

- `tools/layout/baseline.py`、`tools/task_contract/`配下、
  `tools/deployment/local_integrated_roots.py`を変更しない（再利用のみ）。
- Project Manifestの書換えでproject移動・複数checkoutを表現しない。
- Bindingの耐久保存・binding directory新設・新record kind・新schema version・
  Layout authority変更・外部依存追加を行わない。
- 実ホーム・既存利用者data・既存保全dataへaccessしない。Testは`tmp_path`のみ。
- 原子的filesystem競合防止、Verification Run復元、Work 7A第3項以降を実装しない。
- push、tag、PR、amend、rebase、reset、履歴書換え、`git add -A`／`git add .`を行わない。
- TODO・checklist・Plan・Decision・既存Evidenceを変更しない（完了反映はCloser＝Codexが
  `verified`後に別単位で行う）。

## 10. 停止条件

1. base、commit列、worktree、固定入力Digestが不一致。
2. §8以外のpath、特に固定入力実装の変更が必要。
3. 新record kind・新schema・binding directory・Layout authority変更が必要。
4. REDが今回の未実装以外の理由で失敗、または既存実装でGREEN。
5. targeted、関連回帰、公式全Test、`git diff --check`、receipt、Digest照合のいずれかが不合格。
6. 実データaccess、意味的裁定、Human境界の変更が必要。

停止時は理由・再現command・exit code・実施済みと未実施を固定し、Human判断へ渡す。

## 11. Test・validator・独立oracle

- targeted：`.venv/bin/python3 -m pytest tests/test_work7a_checkout_relocation.py`（単独）
- 関連回帰：`tests/test_layout_baseline.py`、
  `tests/test_work7a_local_integrated_root_separation.py`、
  `tests/test_first_review_task_contract_e2e.py`（`read_source_snapshot`の既存利用元）
- 公式全Test：`.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt records/development/2026-08-09-work7a-checkout-relocation-green-test-receipt-v1.json`
- Reviewer向け独立oracleの提案：受入条件をPilotのTestからでなく上流（Plan Work 7A節、
  checklist第2項、用語集のBinding定義、Layout v3のbinding defer）から独立導出し、`high`の
  ためPilotのfixtureに無い反証を最低1件機械実行する。

## 12. 予定するcommit境界

1. **SCOPE**（本commit）：本文書のみ。commit後に停止し、範囲レビューとHuman再開承認を待つ。
2. **RED**：`tests/test_work7a_checkout_relocation.py`のみ。単独実行で今回の未実装だけを
   理由とする失敗とexit code `1`を確認してからcommitする。RED実行結果（command、exit code、
   件数、environment、Test digest）はGREEN Evidenceへ記録する（従来方式踏襲）。
3. **GREEN**：`tools/deployment/checkout_relocation.py`、GREEN Evidence、公式receiptのみ。
   Testは変更しない（要求誤解等が判明した場合は停止しHuman承認後に理由を記録して訂正）。
4. **review request**：レビュー依頼書のみ。各handoff commitの前に
   `git check-ignore --no-index <path>`を単独実行し、exit `1`のみ続行する。

各commit前に`git diff --check`を実行し、明示pathだけをstageする。
