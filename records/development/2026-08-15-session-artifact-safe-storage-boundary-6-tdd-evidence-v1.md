# Session記録安全保存 境界6 検証付き再読込みTDD Evidence v1

- 実施日：2026-08-15
- 開始基準commit：`1295f04`

【実測】正常読込み、期限切れ無削除、raw・派生物・manifest・operation・commitの各一文字改変拒否の7試験を
先に追加した。単独実行は終了コード1、7 failed、主要理由は`load_derived`不在だった。

【実測】記録ID、二rootと作成物の安全属性、固定file集合、正準JSON、両operation、状態、全SHA-256、manifest、
commit、保持期限を読取り専用で照合する最小実装を追加した。期限内だけ許可済み派生物を返し、期限後は
`expired_pending_deletion`だけを返す。自動削除、探索、一覧、検索は追加していない。

【実測】同じ単独試験は終了コード0、7 passed。専用試験は44 passed、既存入口関連は21 passed、
`git diff --check`は終了コード0だった。

- 実装SHA-256：`5981bfc8bdcbf5c05bedebf1349090a4f1e3866dead0ad29e1ea5a5e59fd7fb6`
- 試験SHA-256：`94127e29da8e00cc07f91f2f043619ff0b1ad00f0f997d7741663ae4e9167b71`

【判断】境界6はREDを変えず最小GREENとなった。削除計画と削除は未実施である。
