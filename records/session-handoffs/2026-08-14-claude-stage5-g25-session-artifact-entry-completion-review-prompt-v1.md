# Claude向け 第5段 G25 Session記録読取り専用入口 完了レビュー指示 v1

次の固定材料だけを入口に、読み取り専用で独立完了レビューを行ってください。これは利用者が手動で渡す
他社モデル確認です。リポジトリ内のfileは変更しないでください。

## 1. 固定材料

- 観測commit：`2f62c664ec15b66b1438b92d5f997a4e459735b0`
- Task Contract候補：
  `records/task-contract/2026-08-14-g25-session-artifact-preparation-candidate-v1.md`
  - SHA-256：`20e4e0551c5b1357ba3e66d6ba849f19566da27c58c54ef98e8fa1db110fb72b`
- 定義挑戦：
  `records/development/2026-08-14-stage5-g25-session-artifact-task-contract-definition-challenge-v1.md`
  - SHA-256：`0d7277f98c09cfbf2c107e94a8179aa76b4f55c189c3ba024792a087ee671f52`
- 限定訂正レビュー：
  `records/development/2026-08-14-stage5-g25-session-artifact-task-contract-definition-correction-review-v1.md`
  - SHA-256：`8f07d74cb03e4ab6134a1774af8b775e1d01c57d836f32720ad6296dd1099e91`
- Human承認判断：
  `records/development/2026-08-14-stage5-g25-session-artifact-task-contract-approval-decision-v1.md`
  - SHA-256：`dde3ad7be1a31f1c7f77e253a90fe952496950e5b6a402fcdf473388d211ae39`
- 実装Evidence：
  `records/development/2026-08-14-stage5-g25-session-artifact-read-only-entry-implementation-evidence-v1.md`
  - SHA-256：`d6b125a5b6a62f8a6eef0854c4394c3e87f5a400dc8b75c11814dcd1f03823af`
- 実装前commit：`8e339d8a2c09e9f8c5d87568be3b28e0107fa38a`
- RED commit：`85e4b9031ae79308dad36161eb1150a3a8666a94`
- RED入力訂正commit：`3e780c22f5222b5f2a1c6ce5600f63d6783a7f4b`
- GREEN commit：`1866d3863c7dab99bfae3649f189a50f2c8ec187`

最初に、上記commitの実在、fileのSHA-256、観測commitの変更範囲を機械照合してください。不一致があれば、
影響する判断を`reported_unverified`または`report_execution_mismatch`として止めてください。

## 2. この開発物は何か

利用者が処理を許可したローカルSession記録一件を読み取り、三形式を識別し、伏字化した転写、要約、来歴を
安全な項目だけのJSONとして画面へ返す製品入口です。過去の作業内容の確認、引き継ぎ、レビュー、問題調査に
使います。保存、自動探索、複数file処理、外部送信、network、外部process、Git操作は行いません。

全ての機微情報を検出する機能ではありません。既定規則、高い乱雑性の検査、絶対pathの最終検査で確認できる
範囲だけを守り、結果には`external_send_approved: false`を付けます。

## 3. 確認する中心判断

次の主張を、Evidenceの結論をなぞる前に反証してください。

> 承認済みの三pathだけで、一件のSession記録を読み取る正規の製品入口が完成し、安全な項目だけを返し、
> 契約で禁止した書込み・送信等を行わず、既存G25の振る舞いも壊していない。

具体的には次だけを確認してください。

1. 実装前からGREENまでの意味変更が、新しい入口、`pyproject.toml`の実行名、対象試験の三pathだけか。
   G25既存10 path、G26、G30、他142 path、既存試験、`config/`配下が不変か。
2. REDが入口未実装9件と実行名未登録1件で失敗し、`token=`から`value=`への一行訂正が、既定規則に
   一致しない高乱雑性値を作るための正当な入力訂正か。GREEN中に試験を弱めていないか。
3. Claude、Codex公開JSON、Codex rolloutの三形式が処理できるか。成功結果に未伏字`events`、raw bytes、
   規則pattern、入力由来の`detail`、例外本文、絶対pathが出ないか。
4. root外の通常pathとsymlinkを読取り前に拒否するか。高乱雑性値、低乱雑性の絶対path、種別不明では、
   転写・要約を返さず固定した停止結果だけを返すか。元fileのbytesが不変か。
5. 新入口からfile書込み、directory作成、network、外部process、Git、権限変更、環境値解決、外部送信へ
   到達しないか。禁止副作用を少なくとも一つ、リポジトリ外の故障注入で反証してください。
6. `pyproject.toml`を正本として作ったwheelに`reviewcompass3-session-artifact`が入り、リポジトリ外の新しい
   環境へ導入した実行名から合成例を処理できるか。
7. 対象試験、G25関連55件、正規全試験を独立再実行し、件数、終了コード、状態識別値を観測commitへ
   結び付けられるか。件数を恒久値として扱わないでください。
8. 新入口の`lifecycle: stable`、`normative_status: normative`、`promotion_required: false`が、Human承認済みの
   契約と現在の受入段階に対して過大表示でないか。過大なら、この表示だけを最小訂正候補として示してください。
9. その他の低乱雑性の機微情報をすべて検出する保証や外部送信許可を、成果が暗黙に主張していないか。

中心判断を否定する反証を少なくとも一つ試してください。合成した値だけを使い、実Session記録や秘密値を
repositoryへ置かないでください。

## 4. 深さと禁止事項

本質から外れた過剰な修正案を出さないでください。このレビューの目的は、上記一製品入口が契約どおり完成したかを
判断することです。次は依頼していません。

- G25既存10 path、G26、G30、他142 path、上流候補の整理または修正。
- 全試験の一件ずつの必要性確認、試験数や実行時間の削減。
- 新しい台帳、検査器、関門、schema、生成器、状態機械、恒久script、追加の恒久試験。
- 保存、探索、複数file処理、外部送信、環境値解決の追加。
- Task Contract全体、立て直し計画、第4段、第5段の全面再レビュー。

止める指摘がある場合は、中心判断を崩す一原因へまとめ、不可欠な最小訂正だけを示してください。好み、一般論、
将来改善を混ぜないでください。

## 5. 出力形式

1. 判定：`verified`、`correction_required`、`reported_unverified`、`report_execution_mismatch`のいずれか
2. 止める指摘（0件なら0件）
3. 報告不一致（0件なら0件）
4. 開発物の機能と用途を平易に説明
5. 変更範囲とREDからGREENへの移行
6. 安全な出力、入力境界、禁止副作用の確認
7. 配布物と導入済み実行名の確認
8. 対象・関連・正規全試験と状態の結び付き
9. 試した反証と結果
10. 利用者が完成判断前に判断する点
11. 未実施事項

第5段完了または利用者の製品受入を代行しないでください。fileの作成・変更、stage、commit、push、履歴書換え、
外部送信、コード・試験・設定・Issue・TODOの変更は行わないでください。一時材料と受領記録はrepository外に置いて
ください。
