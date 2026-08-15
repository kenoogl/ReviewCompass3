# Session記録安全保存 境界7 削除計画TDD Evidence v1

- 実施日：2026-08-15
- 開始基準commit：`f21c8ac`

【実測】確定済み・途中状態の決定的な読取り専用計画と、一覧外file拒否の3試験を先に追加した。単独実行は
終了コード1、3 failedで、主要理由は`plan_delete`不在だった。

【実測】二つの当該記録directoryだけを開き、許可固定名、有効operation、状態、実在fileを確認し、area・file名・
最終／一時の区分、件数、operationとmanifestの識別値、監査保持期限だけを返す処理を追加した。pathは返さず、
確認値は確認値自身を除く計画本文の正準JSONから計算する。file変更処理はない。

【実測】同じ単独試験は終了コード0、3 passed。専用試験47 passed、既存入口関連21 passed、
`git diff --check`は終了コード0だった。

- 実装SHA-256：`c2c8e1e978ef5a6bafaf6b13df7f1c24781a0d88adffea4407728de14fdd8d30`
- 試験SHA-256：`8355e0e49ee1f3daac6eef955d7b290fba5e42eb03384cfe1a579a95e8b61ee2`

【判断】境界7はREDを変えず最小GREENとなった。削除は未実施である。
