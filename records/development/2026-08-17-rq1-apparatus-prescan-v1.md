# RQ1装置（Contract completeness計測）事前走査 v1

- 記録日：2026-08-17
- 指示者：利用者（Human）。選択文言：「続けて順序2（RQ1装置）に着手。範囲固定文書から進めて」
  （2026-08-17 chat。上位計画＝評価データ取得計画v1 §3優先1a・§4順序2）
- 記録者：Claude
- 種別：作業単位定義前の事前走査（6手順。手順5＝正式再利用検索は作業票の着手後手続きへ委譲）
- 基準commit：`f3eca20`（作業tree clean）

## 0. 一枚要約（人向け）

RQ1の5指標のうち、**照合・検出の中核部品はすべて既存**である：Requirement被覆の照合器
（`check_requirement_coverage`・双方向試験a3つき）・6 Plan生成（`compile_contract`＋
`_plan_views`・試験a2つき）・欠落系の検出器（`definition_challenge`の`_check_*`群）。
よってRQ1装置の実態は、**既存部品を呼んで指標JSONを機械生成する集計器1本＋negative fixture群
＋再生成一致の比較器**に縮小できる。新しい検証ロジックは書かない（検証器の重複実装を避け、
装置は「呼ぶ・数える・来歴をつける」だけにする）。

## 1. 手順1：所在特定【実測】

| 部品 | 所在 | RQ1指標との対応 |
| --- | --- | --- |
| compile本体 | `tools/task_contract/contract.py` 444行`compile_contract`・356行`_plan_views`（6 view）・391行`_sealed_record` | 再生成一致率（同一入力での再実行比較）・obligation-to-plan coverage |
| Requirement被覆の照合器 | 同 332行`check_requirement_coverage`（`REQUIREMENT_OBLIGATIONS` 16要求） | Requirement-to-obligation coverage（**照合器は既存**・試験a3が双方向を固定済み） |
| 欠落・不備の検出器 | `tools/task_contract/definition_challenge.py`（`_check_requirement_receivers`・`_check_sections`等・severity＝blocking／nonblocking） | negative case検出率・誤停止率（検出器は既存。**注入fixtureが未整備**） |
| compileの門 | `contract.py` 402行`compile_gate_reason`（challenge verdict・approval門） | negative（門の停止系）の計測点 |
| 最小Contractの生成手段 | `tests/test_first_review_task_contract_e2e.py`のruntime fixture（a1〜a11・11本） | 正常系fixtureの流用元 |
| 指標の出力先 | 未存在 | 装置が新設する（指標JSON・数値の来歴つき——RC初代の流儀） |

## 2. 手順2：import元・保護境界【実測】

`tools.task_contract`のimport元は試験系（`test_first_review_task_contract_e2e.py`ほか
task_contract系試験）と`tools/development/`の一部。本装置は**読み取り専用の利用者**として
加わるだけで、`tools/task_contract/`本体・既存試験は無変更（保護境界＝task_contract系試験の
緑維持）。

## 3. 手順4：接続点【実測】

1. **装置の置き場（論点）**：評価系の既存パッケージは無い。新設`tools/evaluation/`が機能領域
   分割の既存流儀に合う（extraction/はセッション抽出系で別物）。
2. fixture置き場：装置と同居（`tools/evaluation/fixtures/`または試験側）。再現可能package化
   （REQ-EVAL-003）を意識し、装置・fixture・出力仕様を一箇所に。
3. 指標出力：`records/development/`へのrecord化はHuman指示時（record-run論点4の裁定と同型）。
   装置は標準出力へ正準JSON一行（既存CLIの流儀）。
4. G30登録：対象外（評価装置は運用契約でない）。
5. 権威：REQ-EVAL-001〜003は権限束v2に収録済み（着手権威あり・2026-08-17機械確認）。

## 4. digest表【実測】

```text
68d3a87dcbff34dd18237a9757d768b3d9a3f2a0387b30abeccd84d6f81ed8e9  tools/task_contract/contract.py
cee75835ea882080f2142a0c1d9eb126b2aa9d9e46924111620c379d0be64594  tools/task_contract/definition_challenge.py
32035909a96e6ce28f19792716b5d3e49b7132f6f8e316c1287679c9da291cd0  tools/task_contract/execution.py
cc99faaa4813aa629c9640431e31d4da635890bc5ec1e1f30c631d06c513661f  tests/test_first_review_task_contract_e2e.py
c666bdd7d0b5c44a8fbb876238a19c1d05ee245e693a2b104ceee514cdad55cb  docs/development/2026-08-17-evaluation-data-acquisition-plan-v1.md
d2668b6720b9578fd89382d943c1ec72225a6b781e20776455c8fd01f46f93d3  records/development/2026-08-17-evaluation-recoverability-map-v1.md
```

## 5. 作業票へ渡す論点【記録】

1. 装置の置き場＝`tools/evaluation/`新設の確認。
2. 指標の定義固定：coverage 2種（数え方の分母・分子）・再生成一致（byte一致か構造一致か——
   sealed recordの決定性を踏まえbyte一致を第一とする案）・negative検出率／誤停止率（fixture
   集合の設計：欠落・競合・stale・正常の4群）。
3. negative fixtureの規模（各群いくつ——初版は各3〜5件・後から追加可能な登録形）。
4. 出力形式（正準JSON一行・数値の来歴欄つき）。

## 6. 未実施

- 作業票v1の承認、正式再利用検索、RED/GREEN、fixture作成、指標の初回計測。
