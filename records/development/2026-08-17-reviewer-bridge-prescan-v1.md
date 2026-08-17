# reviewer接続（データ取得順序3）事前走査 v1

- 記録日：2026-08-17
- 指示者：利用者（Human）。選択文言：「続けて順序3（reviewer接続）に着手。範囲固定文書から
  進めて」（2026-08-17 chat。上位計画＝評価データ取得計画v1 §4順序3）
- 記録者：Claude
- 種別：作業単位定義前の事前走査（6手順。手順5は作業票の着手後手続きへ委譲）
- 基準commit：`8756968`（作業tree clean）

## 0. 一枚要約（人向け）

Task Contract実行経路のreviewerはdeterministic stub（LLMを呼ばない）であり、論文実験
（paired trial）にはLLM reviewerへの接続が要る。接続の両端は確定した：stub側の出力
（finding_set＝`finding_id`・`severity`・`target_ref`…のsealed集合）と、正式起動側の入出力
（依頼record→launch→判定record findings）。**適合性検査が要求するのはseverity語彙
（error／warning／info）だけ**なので、変換adapterは薄く作れる。設計の本質論点は方式選択——
**正式経路（依頼record→check→launch）を機械駆動する案Aを推奨**し、下層直結（案B）は
安全境界（認証遮断・読み取り専用・fail-closed）の迂回になるため不採用。もう一つのHuman裁定
＝**実験バッチの起動承認の形**（ケースごと承認は非現実的）。

## 1. 手順1：所在特定【実測】

| 部品・結合点 | 所在 | 状態 |
| --- | --- | --- |
| stub reviewer（置換対象の参照仕様） | `tools/task_contract/execution.py` 239行`run_stub_reviewer` | 入力＝contract・context_manifest・permit。出力＝finding_set（`finding_id`・`severity`・`target_ref{relative_path, sha256}`・`requirement_ref`・`rule_id`・`description`のsealed集合） |
| 適合性検査の要件 | 同 298行`evaluate_conformance` | **severity集計のみ**（error→failed）。変換後findingが満たすべき契約は小さい |
| 正式起動経路 | `tools/reviewer_launch/`（契約010/012・受入済み）＋依頼record組み立て`tools/request_builder/`（契約011/013） | `free_text`類型が「調査結果の妥当性」等の自由文レビューを受ける正式枠（契約013 §7.2） |
| 判定recordのfindings形式 | `record.py`転記（`identifier`・`claim`・`severity`・`blocking`・`evidence_path`・`evidence_location`） | finding_setへの変換対応：`evidence_path`→`target_ref.relative_path`・severity語彙は同一系（info実例確認済み） |
| 実行メタ | `launch.json`（順序1で時間・prompt bytes追記済み・トークンはrawから復元可） | 実験の費用・時間データは自動取得できる状態 |
| 装置の同居先 | `tools/evaluation/`（順序2で新設） | adapterの置き場候補 |

## 2. 手順2：import元・保護境界【実測】

- `execution.py`・`reviewer_launch`・`request_builder`はいずれも**無変更**（読み取り専用利用）。
  保護境界＝task_contract系試験（E2E 38本ほか）・reviewer_launch 68本・request_builder 40本・
  G30 75本の緑維持。
- 接続はadapter新設（`tools/evaluation/`内）で行い、製品本体へ手を入れない。

## 3. 手順4：接続点と方式の選択肢【実測・記録】

1. **方式（Human裁定・推奨あり）**：
   - **案A（推奨）：正式経路の機械駆動**——Task Contract chainの文脈から`free_text`依頼record
     本文を機械組み立て（assemble→記入相当を機械生成→check合格）→承認済みバッチ内でlaunch→
     判定recordのfindingsをfinding_setへ変換。安全境界・Provenance（依頼・判定recordが残る）を
     正式経路のまま通る。**実験の完全な追跡可能性が論文の主張材料（H5）にもなる**。
   - 案B：`reviewer_launch`下層（prompt構築・subprocess）の直接利用——認証遮断・読み取り専用・
     fail-closedの再構成が必要になり、契約010の安全設計の迂回。**不採用を推奨**。
2. **バッチ起動の承認形（Human裁定）**：契約010 §2の起動承認は「利用者のchat指示ごと」。実験
   （8〜15ケース×条件）で1起動ごとの承認は非現実的。**「実験計画（ケース一覧・条件・起動回数
   上限・費用見積り）の事前承認をもって、バッチ内の個別起動を委任する」**形の確立が必要。
3. 実験recordの置き場：正式経路のまま`records/session-handoffs/`へ、実験専用slug
   （例：`rq2-case-NNN-…`）で区別する案を推奨（経路を分岐させない——入口統一の既存原則）。
4. 対象の制約：checkはcommit済みrepo内fileを対象とする——実験ケース材料はrepoへcommitする
   構成（`tools/evaluation/fixtures/`系）で整合。

## 4. digest表【実測】

```text
32035909a96e6ce28f19792716b5d3e49b7132f6f8e316c1287679c9da291cd0  tools/task_contract/execution.py
814f890360312e70904fbb6b4654ed930cffa8a1db18351bf42dc54fe30318b7  tools/reviewer_launch/core.py
998c31d726c3aa37bd5021d83495590ad49015916ab4ca0572890465e495db8d  tools/reviewer_launch/record.py
e61215eddc0e7f50468c87a9b17c2cba6825fd2470a80d0bac3eca72c0e3907d  tools/request_builder/core.py
cd8558cdc702b2a24f8ddfae69c2c51f7749ddb6536ddc551d5ecb038f6f1116  tools/request_builder/entry.py
30c22465607cb2e37be775d742028c22fcc6ee044c2f4000bbcc494ab018740a  tools/evaluation/rq1_contract_completeness.py
c666bdd7d0b5c44a8fbb876238a19c1d05ee245e693a2b104ceee514cdad55cb  docs/development/2026-08-17-evaluation-data-acquisition-plan-v1.md
```

## 5. 作業票へ渡す論点【記録】

1. 方式＝案A（正式経路の機械駆動）の確認。
2. バッチ起動承認の形の確定（実験計画の事前承認→バッチ内委任）。
3. finding変換表の固定（severity対応・`blocking`の扱い＝errorへ写像するか）。
4. 本作業（順序3）の範囲は**adapterと変換・試験（起動はfake）まで**とし、実起動を伴う実験は
   順序4（paired evaluation・実験計画の承認）で行う——範囲の切れ目の確認。

## 6. 未実施

- 作業票v1の承認、正式再利用検索、RED/GREEN、実起動を伴う実験（順序4）。
