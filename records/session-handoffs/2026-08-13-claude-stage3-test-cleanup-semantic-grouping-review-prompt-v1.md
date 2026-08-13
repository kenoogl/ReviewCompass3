# Claude向け 第3段 試験整理候補の意味群分類 完了レビュー指示 v1

次の固定材料だけを入口に、読み取り専用の独立完了レビューを行ってください。

## 固定材料

- 観測commit：`9594d7baa7b33b4bd7aa8dafb188012226faad1f`
- 作業票：`docs/development/2026-08-13-stage3-test-cleanup-semantic-grouping-bootstrap-work-ticket-v1.md`
  - SHA-256：`f39e4450d627cb193f156e6f6cfa1d7e225c07ce0de8f36fbb7aeb4b7fff37c3`
- 実施順序Decision：`records/development/2026-08-13-stage3-test-cleanup-execution-sequencing-decision-v1.md`
  - SHA-256：`8d05c2e57dbd03442ad4b2c8f910e4ba63d679631ebc0e98ee7d7d13556946e8`
- 個別401件一覧：`records/development/2026-08-13-test-growth-nodeid-candidates-v1.txt`
  - SHA-256：`11d383f82196e6d964340f83e085d4fd6c7f4e9b1fd3570de8830bafbffbecad`
- 分類Evidence：`records/development/2026-08-13-stage3-test-cleanup-semantic-grouping-evidence-v1.md`
  - SHA-256：`cc77c218bc4baefc5e734ad7310824235900f32c122bd5f3c5ecdb786cb9399e`
- 現行開発方針：`docs/development/2026-08-02-development-policy.md`
  - SHA-256：`20c4c00a69677af9b4dc51b59b5718889c27fe6cfbbe2adc57cfcc2f601a7a42`

## 確認すること

1. 401件が16群に重複なく一度ずつ含まれ、群合計が401件かを成果物の集計値に頼らず確認する。
2. 群の境界がファイル名や件数だけではなく、現在の利用者、要求、製品機能、履歴資料、共有境界に基づくかを確認する。
3. `test_claude_bootstrap_entrypoints.py`を現在境界2件と作業時点固定6件に分けた判断を、各試験本文と参照先から反証する。
4. G04六件を最初に詳しく調べる提案が、六件の一括削除を意味せず、現在保証を先に整理対象から外す誤りを含まないかを確認する。
5. 暫定役割と個々の削除可否を混同していないか、承認済み一件が`削除判断済み・実施待ち`のままかを確認する。
6. 新しい台帳、検査器、試験、恒久機構を増やさず、読み取りと分類Evidenceだけに収まったかを確認する。

中心判断を否定する反証を少なくとも一つ試してください。特に、未分類または重複した候補、現在の安全境界を
履歴固定へ誤分類した候補、同じ製品境界を不自然に別群へ分けた候補がないかを優先してください。

## 深さと禁止事項

これは分類作業の完了レビューであり、401件すべての必要性判断、削除案、統合案、全試験、変異検査、
製品設計の再検討を依頼するものではありません。本質から外れた過剰な修正案、新しい仕組み、台帳、検査器、
試験群を提案しないでください。止める指摘がある場合は、分類作業の目的を満たすために不可欠な一原因へまとめ、
最小の修正方向だけを示してください。分類結果を変更したり、削除を実施したりしないでください。

## 出力形式

1. 判定：`verified`、`reported_unverified`、`report_execution_mismatch`、`blocked`のいずれか
2. 止める指摘と根拠
3. 報告不一致
4. 401件の完全性と16群の境界の確認結果
5. G03/G04分割とG04選定への反証結果
6. 試した反証
7. 利用者が次に判断する点
8. 未実施事項

fileの作成・変更、stage、commit、push、履歴書換え、外部送信を行わないでください。
