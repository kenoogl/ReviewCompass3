# 評価データ取得計画（論文優先・広め） v1

- 作成日：2026-08-17
- 作成者：Claude
- 承認文言【記録】：「データ取得計画としては、広めに考え、プライオリティとしては、論文向け
  データを最初にとる。この2層整理で確定。論文構想2文書もrepoへ取り込み、research sliceの
  事前走査から着手し、データ取得計画を策定、メモ化。」（2026-08-17 chat）
- 位置づけ：Work 8前倒しの計測基盤（評価仕掛け）の**計画メモ**。research slice事前走査の
  結果を含む。実装の範囲固定文書・正式再利用検索は着手時に別途行う（本メモは計画であり
  実装権威ではない）

## 1. 主題と2層整理（確定済み）

論文主題（利用者提示・2026-08-17 chat）：

> **Task Contracts for Evidence-Bounded LLM Code Review: A Requirements-to-Runtime Approach**
> 中心命題：Task Contractを、要求とLLMレビュー実行の間に置く機械解釈可能な中間表現とし、
> 必要Evidence、許可能力、受入条件、Provenance、Human escalationを決定的に実行計画へ変換する。
> これにより、リポジトリが大きくなってもレビュー入力を変更影響に比例させながら、必要根拠の
> 欠落を防げる。

| 層 | 中身 | 仕掛け |
| --- | --- | --- |
| **主軸（優先1）** | RQ1（Contract completeness）・RQ2（Context scalability）の対照実験 | 実験装置（paired evaluation・正解付きケース）＋実験データ |
| 従軸（優先2） | 運用計測（H4ハーネス導出・H5 Provenance・H7 Human介入・コスト） | 既存recordの集計＋欠落計測点の追記 |

- RQ1：Task Contractからの決定的なPlan compilationが、実行前にEvidence・権限・受入条件・
  Provenanceの欠落や競合を検出できるか。
- RQ2：Contract誘導のContext選択が、無関係なrepository材料の増加に対して入力サイズを安定させ、
  必要EvidenceとFinding品質を維持できるか。
- 貢献3点（予定）：(1) RequirementsとLLMレビュー実行を接続するTask Contractモデル、
  (2) obligationを実行・検証・Provenance計画へ写像する決定的compiler、(3) 無関係な
  repository成長に対する入力安定性とEvidence保持のpaired pilot。
- 主張しないこと：大規模実証済み汎用Runtime／人間レビュー超え／Requirements自体の正しさ保証／
  RC3全体の完成／少数ケースでの統計的優位。
- 根拠の系譜：概念文書§13検証仮説（`docs/concepts/2026-08-02-task-contract-centered-engineering.md`
  677行〜）が本RQと一対一対応。研究構想の正本は取り込み済み2文書（§5 digest表）。

## 2. research slice事前走査の結果【実測・2026-08-17】

| 構想が要る部品 | 既存実装 | 充足 |
| --- | --- | --- |
| Review Task Contract schema（九つ組） | `tools/task_contract/contract.py`（responsibility・boundary・preconditions・context_obligations・expected_output・acceptance・provenance_obligations等の欄＋16 Requirementへの義務束縛表） | **あり** |
| Contract validator | 同上＋`definition_challenge.py`（compile前検査） | **あり** |
| **6種Plan導出の決定的compiler** | `contract.py`の`PLAN_VIEWS`＝context_acquisition・review_execution・harness_and_capability・verification・provenance_capture・human_interaction | **あり（6種完備）** |
| 二層検証（Contract-challenge） | `definition_challenge.py`（Contract自体の検査＋Human approval record） | **あり** |
| 実行経路 | `execution.py`（Source Snapshot→accepted artifact。変更集合の扱いを含む） | あり（**reviewerはdeterministic stub**） |
| LLM reviewer接続 | stubのまま。ただし契約010〜013の`reviewer-launch`（agy headless・Tier 1）が正式資産として存在し接続可能 | **一部**（接続作業が必要） |
| 影響閉包に基づくContext選択 | `execution.py`に変更集合の扱いあり（paired trialが要求する「無関係資料を追加しても入力不変」の検証装置としての完成度は要精査） | 一部 |
| paired evaluation装置（4条件比較） | なし | **新設要** |
| 正解付きケース8〜15件 | 素材あり：RC3判定record 12件（cr-系）・LLMGP実運用履歴（`WindTurbineWake/LLMGP/.reviewcompass/`）・初代RCレビューrun。**人手の正解固定作業が必要** | 素材あり |
| 計測メタ | 判定recordに所要時間・prompt規模・トークンが**ない**（2026-08-17機械確認） | **欠落（追記要）** |

**8/30実現性の評価**：構想文書は「製品実装code未着手」という古い現状認識で書かれているが、
実際はschema・validator・6種compiler・二層検証・実行経路まで既存（Work 5A/6A成果）。残作業は
(a) stub reviewerのreviewer-launch接続、(b) paired evaluation装置の新設、(c) ケースの人手固定、
(d) 計測メタの追記——であり、pilot study（8〜15件）の成立見込みは構想の想定より高い。

## 3. データ取得計画（広め・論文優先）

### 優先1a：RQ1（Contract completeness）のデータ

| 指標 | 取得方法 |
| --- | --- |
| obligation-to-plan coverage | compile出力（6 Plan）とContract義務の対応を機械照合 |
| Requirement-to-obligation coverage | `REQUIREMENT_OBLIGATIONS`表（16要求）の被覆を機械集計 |
| 同一入力からの再生成一致率 | 同一Contractのcompile再実行のbyte/構造比較（決定性の実証） |
| negative case検出率 | 欠落・競合・staleを注入したfixture（既存の敵対fixture流儀）でcompile/検査の停止を測る |
| 誤停止率 | 正常ケースでの不当停止の率 |

### 優先1b：RQ2（Context scalability）のデータ——paired trial

- 4条件×ケース8〜15件：(A)ベースライン（固定prompt/広域Context）・(B)Task Contract方式・
  (C)B＋大量の無関係資料・(D)必要資料の意図的欠落（negative）。同一の変更・model・Tool・budget。
- 指標：review input tokens・source universe bytes・impact closure size・Evidence Coverage・
  Finding recall/precision・責務外Finding率・Human escalationの正否・実行時間と費用。
- **核心の図**：無関係資料追加（C）で入力が不変、関連資料追加時だけ増える——入力安定性と
  Evidence保持の同時提示（トークン削減だけを成果にしない）。

### 優先2：運用計測（従軸・既存recordから）

- H4（ハーネス導出）：assemble→check→launchの所要時間・手動記入箇所数・自動導出率。
- H5（Provenance）：digest束縛の追跡可能率・受入判断の束縛表被覆。
- H7（Human介入）：承認点の分布・問い合わせ数（chat承認文言→Decision recordの系列から復元）。
- コスト：セッションログ（全量保全済み・契約014で構造化可能）から道具呼び出し数・時間を復元。

### 横断：計測メタの追記と復元可能性表

- `reviewer-launch`実行メタ（所要時間・prompt bytes・model・backend）の判定record／raw保存への
  追記（小改修）。
- **復元可能性表**（初代`recoverability.md`の型）：現recordから復元できる指標・できない指標を
  正直に固定し、以後の計測欠落を防ぐ。

### ケース供給源

- RC3のcr-系判定record 12件（正式経路の実運用）＋LLMGPの実レビュー履歴＋初代RCのレビューrun。
- 今後の運用（縦C・デプロイ版以降）は本計画の計測メタつきで自動蓄積。

## 4. 取得の順序（実装の作業単位案）

1. **計測メタの追記＋復元可能性表**（小・すぐ効く——以後の全運用がデータになる）
2. **RQ1装置**（compile決定性・coverage・negative fixture——既存部品の試験拡張が主）
3. **reviewer-launch接続**（stub置換——契約010資産の再利用）
4. **paired evaluation装置＋ケース固定**（RQ2本実験）
5. 運用計測の集計コマンド（従軸）

各作業単位は着手時に範囲固定文書＋正式再利用検索（コード変更を含むため）を経る。

## 5. 固定入力（digest表）【実測】

```text
68d3a87dcbff34dd18237a9757d768b3d9a3f2a0387b30abeccd84d6f81ed8e9  tools/task_contract/contract.py
32035909a96e6ce28f19792716b5d3e49b7132f6f8e316c1287679c9da291cd0  tools/task_contract/execution.py
cee75835ea882080f2142a0c1d9eb126b2aa9d9e46924111620c379d0be64594  tools/task_contract/definition_challenge.py
6e3c8395d71b7cec7a59b4834b3d6d04312e7d28e65e5cdd9f168f3193e13de2  docs/design/2026-08-17-task-contract-discussion-import-v1.md
d49062602b7965eb64416d22b26bdcd81e0f685775a3c728a5aed52d81e44577  docs/design/2026-08-17-task-contract-architecture-import-v1.md
80f388b9308450f1758f623346e25fa6623c8d5d59cb32979436ee3831af1d91  docs/concepts/2026-08-02-task-contract-centered-engineering.md
cc99faaa4813aa629c9640431e31d4da635890bc5ec1e1f30c631d06c513661f  tests/test_first_review_task_contract_e2e.py
```

## 6. 未実施

- §4の全作業単位（各々、範囲固定文書→正式再利用検索→RED/GREENで着手）。
- 正式な事前走査record（scope-prescan 6手順）は最初の実装作業単位の着手時に作成（本メモの
  §2はその先行調査を兼ねる）。
- TODO・見取り図への反映。
