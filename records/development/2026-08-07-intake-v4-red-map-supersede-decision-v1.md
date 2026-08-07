# Intake V4宣言→RED対応表の所見処置（A案：後継版supersede）Decision v1

- decision ID：`DEC-INTAKE-V4-RED-MAP-SUPERSEDE-001`
- decision maker：Human
- decided at：2026-08-07
- 指示：本sessionのHuman文言「両方とも推奨案で。」（2026-08-07。所見処置についてA案を承認）

## 1. 対象の所見

検査器の第一実運用（`records/development/2026-08-07-work5b-checker-first-run-v1.json`、SHA-256
`e2c4fb658c289340f2d0ac3c27a7cb3bce8168b3dcccd6926de30c5e21aca20c`）が、Intake V4の
宣言→RED対応表v1に対して検出した実在所見2件。

1. `listed_test_missing`：N9のtest名が、N7-N9修正（`DEC`記録：
   `records/development/2026-08-06-intake-v4-n7-n9-amendment-decision-v1.md`）に伴う改名へ
   追随していない。
2. `test_file_listing_invalid`：`tests/test_issue_intake_v4.py`の`test_files`欄が他の対応表と
   異なるdict形式である。

## 2. Humanの決定（A案）

後継版v2を新規作成して差し替える。v1は歴史record（RED固定時点の宣言と結線の記録）として
不変のまま保持し、以後の検査はv2に対して行う。検査器は厳格なまま保ち、別形式は教えない。

- v2：`records/development/2026-08-07-intake-v4-declaration-red-map-v2.json`、SHA-256
  `0c4974452e440d06b857d3483a4c5804d57a28984075a7c1a10630b648338ff3`。
  恒久検査器`tools/development/declaration_red_map_check.py`による検査は`passed`
  （宣言12、testの無い宣言0、実在しない列挙0、結ばれないtest 0）。
- v1：`records/development/2026-08-06-intake-v4-declaration-red-map-v1.json`、SHA-256
  `c24ebaf58eee3ce2d318084697051d41c9669e30aa756086706f9f110117ce40`。superseded。
  歴史としての検査結果（failed）は第一実運用recordに固定済みであり、以後の運用検査の対象から外す。

## 3. あわせて採用する運用規則

Human承認済みの修正でtestの改名・削除が発生した場合、その修正の作業単位は、影響を受ける
宣言→RED対応表を後継版でsupersedeする。対応表は「RED固定時点の歴史record」と「現役の
宣言→test対応」の二役を持ち、前者は不変、後者は後継版で追随する。

## 4. この決定が承認していないこと

- v1の書き換え・削除（不変のまま保持する）
- 検査器へのdict形式対応の追加
- 他の対応表の変更
