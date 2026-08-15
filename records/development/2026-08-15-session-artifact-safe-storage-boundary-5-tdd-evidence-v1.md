# Session記録安全保存 境界5 中断保存再開TDD Evidence v1

- 実施日：2026-08-15
- 開始基準commit：`d9c08dd`
- 対象：累積作業票v2＋v3の境界5

## 結果

【実測】raw公開後、派生物公開後、manifest公開後、確定印直前、`raw.bin.tmp`書込み後の5停止点と、一覧外file、
改変operation、有効operationなしの3反例を先に追加した。単独実行は終了コード1、8 failed、29 deselectedで、
主要理由は途中状態を一律`record_busy`とする現行処理だった。

【実測】許可された固定名の部分集合、operation、既存本文・一時fileのbytesを変更前に全照合し、正しい一時fileの
公開、欠けたfileの補完、operation確定、確定印作成だけを行う最小再開処理を追加した。不明名・改変・operation不在は
それぞれ`record_conflict`または`record_unrecoverable`で変更せず停止する。

【実測】同じ単独試験は終了コード0、8 passed。専用試験は終了コード0、37 passed。既存入口関連は終了コード0、
21 passed。`git diff --check`も終了コード0だった。

- 実装SHA-256：`75ee21a542ca1695755e6b5e05aa36a934fedcf5abf30893ab5e0cb0b8bfd76b`
- 試験SHA-256：`644b270b17e977ed6ed4bb626e86494f7b8798b92ab0f2dad67c8dca57105b3b`

【判断】境界5はREDを変えず最小GREENとなった。通常再読込みと削除は未実施である。
