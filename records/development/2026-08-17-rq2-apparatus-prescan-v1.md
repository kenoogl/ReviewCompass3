# RQ2 paired evaluation装置（後続作業単位2）事前走査 v1

- 記録日：2026-08-17
- 指示者：利用者（Human）。選択文言「正解表v1を確定。論点2も事前登録形で確定。後続(2)から
  実起動まで一気に進めて」（2026-08-17 chat）
- 記録者：Claude
- 種別：作業単位定義前の事前走査（6手順）。**コード新設を含むため正式再利用検索を適用する**
- 上位：実験計画v1（承認済み）§7-(2)、測定・プール裁定record
  `records/development/2026-08-17-rq2-measurement-and-pool-decision-v1.md`
- 基準commit：`d449e2f`（作業tree clean）

## 0. 一枚要約（人向け）

実装前に**2つの硬い制約**を実測で確定した。どちらも設計を変える必要がある。

1. **契約が受け付ける対象pathは`docs/`配下だけ**である（`build_review_task_contract`の実装。
   これ以外は`path_out_of_scope`で停止）。現在の材料は`tools/evaluation/fixtures/rq2/`にあり、
   **そのままではTask Contract chainを組めない**。→ 材料を`docs/evaluation/rq2-cases/`へ移す。
   file内容は変えないのでdigestは不変であり、正解表の答も変わらない（pathの表記だけ差し替え）。
2. **reviewerの読取り許可は本repositoryのフォルダに束縛されている**（`resolve_project_binding`
   が設定から機械解決する。許可を与えられるのは利用者の対話sessionだけ）。したがって
   **実験専用の別作業treeを作る案は成立しない**（`project_binding_missing`で起動前に停止する）。
   実験は本repositoryで実行するほかなく、**正解表の事前登録（repo外退避）が必須**になる——
   利用者の論点2裁定（事前登録形）と一致する。

条件A／B／C／Dは、いずれも**契約へ渡す対象pathの違い**として同じ起動経路で実装できる（§3）。

## 1. 手順1：所在特定と実測【実測】

| 確認項目 | 実測結果 |
| --- | --- |
| 契約chainの成立 | `bind_requirements`（16要求すべて解決）→`read_source_snapshot`→`build_review_task_contract`→`compile_contract`→`build_context_manifest`が本repositoryに対して成立（材料1件で試行・成功） |
| 対象pathの制約 | `tools/task_contract/contract.py:196-198`——`docs/`で始まらないpathは`path_out_of_scope` |
| 材料の現在地 | `tools/evaluation/fixtures/rq2/case-001`〜`case-010`（12 file・35,800 byte） |
| agyのproject束縛 | 本repositoryに対し解決成功（id先頭`c6fb567d`）。読取り恒久許可あり |
| 許可model | `gemini-3.1-pro-high`の1件（契約の許可一覧。実験中は固定） |
| 起動promptのbyte上限 | 16,384。起動promptは固定形式のため材料量に依存せず、上限に触れない |
| 私有領域 | `/Users/keno/.reviewcompass3-private/reviewer-launch`（既存。`e2e-013-001`まで実績あり） |
| 依頼組み立ての制約 | `request_builder.assemble`は対象pathに`docs/`制約を課さない（読めれば可） |

## 2. 手順2：import元と保護境界【実測】

- 本作業で新設する装置が呼ぶ既存部品：`tools.task_contract`（読み取り専用）・
  `tools.evaluation.reviewer_bridge`（順序3で新設・読み取り専用）・
  `tools.request_builder.core`（bridge経由）・`tools.reviewer_launch.core`（実起動）。
- **既存部品は一切変更しない**。装置は新file 1本（`tools/evaluation/rq2_paired_trial.py`）＋
  その試験に限る。
- 保護対象：`tests/test_rq1_contract_completeness.py`・`tests/test_reviewer_bridge.py`（各
  現状全通過）、task_contract系・reviewer_launch系・request_builder系の既存試験。

## 3. 手順4：接続点——条件A／B／C／Dの実装形【設計判断】

CLI方式では起動経路は1本（依頼record→固定prompt→reviewerが自分で読む）であり、条件差は
**契約へ渡す対象pathの集合**と**ケースディレクトリの物理内容**で表す。

| 条件 | 対象path（契約へ渡す） | ケースディレクトリの物理内容 |
| --- | --- | --- |
| B（主） | ケース材料のみ | 材料のみ |
| C（主） | ケース材料のみ（Bと同一） | 材料＋独立プール |
| A（副・資料少） | ディレクトリ内の全file | 材料のみ |
| A（副・資料多） | ディレクトリ内の全file | 材料＋独立プール |
| D（副） | ケース材料から必須1件を除いたもの | 材料のみ |

- **A（資料少）はBと対象pathが一致する**（プールが無いときディレクトリ全file＝材料）。同一入力
  の2回目の起動になるため、**実行間のばらつき（再現性）の観測**として扱う。この位置づけを
  正解表・集計で明示する。
- 実行順序は物理配置の切り替え回数を最小にする：**B全件＋A（少）＋D → プール配置（1 commit）
  → C全件＋A（多） → プール撤去（1 commit）**。
- 起動ごとの前提：依頼recordを先にcommitし作業treeを清浄にする（launcherが判定recordを
  **単独commit**するため）。

## 4. 手順3：digest表【実測】

```text
abcc1b57a2ba61a246a680539b8484ccd46152d65c204625fc1c89707f0b7be9  tools/evaluation/reviewer_bridge.py
30c22465607cb2e37be775d742028c22fcc6ee044c2f4000bbcc494ab018740a  tools/evaluation/rq1_contract_completeness.py
68d3a87dcbff34dd18237a9757d768b3d9a3f2a0387b30abeccd84d6f81ed8e9  tools/task_contract/contract.py
32035909a96e6ce28f19792716b5d3e49b7132f6f8e316c1287679c9da291cd0  tools/task_contract/execution.py
e61215eddc0e7f50468c87a9b17c2cba6825fd2470a80d0bac3eca72c0e3907d  tools/request_builder/core.py
814f890360312e70904fbb6b4654ed930cffa8a1db18351bf42dc54fe30318b7  tools/reviewer_launch/core.py
790f80c9c185805107bc56edc3adc38c64248559094310225fc41a8796095f6a  records/development/2026-08-17-rq2-case-answer-key-v1.md
3fd9e1d5bd733354db7207727d0a26dbef5c6babdd09568f1a3ddc532bff99c3  records/development/2026-08-17-rq2-measurement-and-pool-decision-v1.md
```

## 5. 作業票へ渡す論点【記録】

1. **材料の移設**（`tools/evaluation/fixtures/rq2/`→`docs/evaluation/rq2-cases/`）。内容不変・
   digest不変。正解表はpath表記だけを差し替えたv2を作り、v2を事前登録の対象にする。
2. **正解表の事前登録**（論点2裁定の実施）：本体をrepo外私有領域へ退避し、repoにはSHA-256を
   封じたrecordだけを実起動前にcommitする。実験後に本体をcommitしてdigest照合する。
3. 起動ごとのrecord数：依頼29＋判定29＝**58 record**がrepositoryへ増える。命名は計画§5-2どおり
   `rq2-case-NNN-<条件>-request-v1.md`。
4. 中断条件（計画§5-4の4種）を装置へ機械実装し、超過時は停止して報告する。

## 6. 未実施

- 手順5（正式再利用検索）——作業別計画の先行commit後に実行する。
- 作業票の固定、RED、GREEN、プール選定、事前登録、実起動、集計。
