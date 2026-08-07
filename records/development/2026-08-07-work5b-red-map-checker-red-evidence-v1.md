# Work 5B 宣言→RED対応表検査器 RED Evidence v1

- 作成日：2026-08-07
- 承認：`DEC-WORK5B-START-001`（`records/development/2026-08-07-work5b-start-decision-v1.md`）
- 実装前検索record（gate通過済み）：
  `records/development/2026-08-07-declaration-red-map-checker-reuse-search-v1.json`、
  content digest `93343aaba1d318aa79d706e6cb4b6a38468d17816b1cfbbc96761be8e6efc0d1`、
  `gate_check`結果`start_allowed: true`

## 1. 宣言→RED対応表の関門

対応表は`records/development/2026-08-07-work5b-red-map-checker-declaration-red-map-v1.json`
（`RC3-WORK5B-RED-MAP-CHECKER-DECLARATION-RED-MAP-001`）。機械照合（その場AST照合の最終回）の結果：

- 宣言：4件（C1〜C4）
- **testの無い宣言：0件**
- 列挙したのにfileへ実在しないtest：0件
- どの宣言にも結ばれないtest：0件

GREEN後は本検査器自身が後続の対応表の照合器になる（恒久tool化、`DEC-WORK5B-START-001` §1-3）。

## 2. 固定したTest

- 検査器の宣言C1〜C4：`tests/test_declaration_red_map_check.py`、6 test
- Contract結線：`tests/test_work5b_contract.py`、5 test（Contract実体・固定source・reuse search
  gate束縛・Work Item順・Human境界と禁止事項）

## 3. RED結果（機械実行、終了コード直接判定）

- 検査器test：exit `2`（`ModuleNotFoundError`相当。module
  `tools/development/declaration_red_map_check.py`未実装による期待どおりのRED）
- Contract結線test：exit `1`（Contract実体
  `records/development/2026-08-07-work5b-implementation-task-contract-v1.json`不在による
  期待どおりのRED）
- 既存全Test（上記2 fileを除外）：`1055 passed`、exit `0`。既存Testは弱めていない。

## 4. 既知の限界（記録）

再利用検索の固定sourceであるRoutine Profile v3は2026-08-05の観測snapshotであり、それ以降に
新設されたroutine（例：`tools/development/python_ast_boundary_check.py`のroutineはProfileに
存在しない）は検索に映らない。検索の網羅性はsource観測時点に束縛される。Profile再観測の
運用周期はWork 4B本体の後続判断とする。

## 5. 状態と次

- 本RED作業単位のcommit後、Contract実体を作成してContract結線testをGREENにする。
- **Contract commit後、Humanの`implementation_ready`判断を記録するまで検査器の実装
  （検査器testのGREEN化）を開始しない**（checklist §10）。
