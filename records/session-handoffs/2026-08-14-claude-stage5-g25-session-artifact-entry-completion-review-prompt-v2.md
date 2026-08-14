# Claude向け 第5段 G25 Session記録読取り専用入口 修正後完了レビュー指示 v2

次の固定材料だけを入口に、読み取り専用で独立完了レビューを行ってください。利用者が手動で渡す他社モデル確認です。
リポジトリ内のfileは作成・変更しないでください。

## 1. この開発物は何か

利用者が許可したローカルSession記録一件を読み取り、ClaudeとCodexの三形式を識別し、伏字化した転写、要約、
来歴を、安全な項目だけのJSONとして画面へ返す製品入口です。過去の作業確認、引き継ぎ、レビュー、問題調査に
使います。保存、自動探索、複数file処理、外部送信、network、外部process、Git操作は行いません。

全ての機微情報を検出する機能ではありません。既定規則、高い乱雑性の検査、絶対pathの最終検査で確認できる
範囲だけを守り、結果には`external_send_approved: false`を付けます。

## 2. 固定材料

- 観測commit：`44cc5ea7b19e890218d67d23064af4bd5c5ea3fe`
- Task Contract：
  `records/task-contract/2026-08-14-g25-session-artifact-preparation-candidate-v1.md`
  - SHA-256：`20e4e0551c5b1357ba3e66d6ba849f19566da27c58c54ef98e8fa1db110fb72b`
- Human承認判断：
  `records/development/2026-08-14-stage5-g25-session-artifact-task-contract-approval-decision-v1.md`
  - SHA-256：`dde3ad7be1a31f1c7f77e253a90fe952496950e5b6a402fcdf473388d211ae39`
- 最初の実装Evidence：
  `records/development/2026-08-14-stage5-g25-session-artifact-read-only-entry-implementation-evidence-v1.md`
  - SHA-256：`d6b125a5b6a62f8a6eef0854c4394c3e87f5a400dc8b75c11814dcd1f03823af`
- 最初の独立完了レビュー：
  `records/development/2026-08-14-stage5-g25-session-artifact-read-only-entry-independent-completion-review-v1.md`
  - SHA-256：`798761ac4a77ff03c54327c0315f4687e8b149d287a0d6d78c6439f45609e5d7`
- 限定修正Evidence：
  `records/development/2026-08-14-stage5-g25-session-artifact-read-only-entry-correction-evidence-v1.md`
  - SHA-256：`2d297c90834d6c33c40cadcc4bcf3c53a29c57a939dea539f526913ba34126b5`
- 実装前commit：`8e339d8a2c09e9f8c5d87568be3b28e0107fa38a`
- 最初のRED：`85e4b9031ae79308dad36161eb1150a3a8666a94`
- RED入力訂正：`3e780c22f5222b5f2a1c6ce5600f63d6783a7f4b`
- 最初のGREEN：`1866d3863c7dab99bfae3649f189a50f2c8ec187`
- 限定RED：`208276c2bcaa784e85ca944e59339e2550f8b033`
- 限定GREEN：`8d7abafba03871dbe050b3c685592105589c0289`

最初にcommitの実在、fileのSHA-256、観測commitの変更範囲を機械照合してください。不一致があれば、影響する
判断を`reported_unverified`または`report_execution_mismatch`として止めてください。

## 3. 確認する中心判断

次を、Evidenceの結論をなぞる前に反証してください。

> 承認済みの三pathだけで、一件のSession記録を読み取る正規の製品入口が完成し、安全な項目だけを返し、
> 契約で禁止した書込み・送信等を行わず、独立レビューが見つけた二つの問題も限定修正されている。

確認するのは次の点です。

1. 実装の意味変更が、新入口、`pyproject.toml`の実行名、対象試験の三pathだけか。G25既存10 path、G26、G30、
   他142 path、既存試験、`config/`配下が不変か。
2. 二つのREDが未実装理由で失敗し、GREEN中に試験を弱めていないか。`token=`から`value=`への訂正は、既定規則に
   一致しない高乱雑性値を作るための正当な一行訂正か。
3. 三形式が処理でき、正常結果に未伏字`events`、raw bytes、規則pattern、入力由来の`detail`、例外本文、
   絶対pathが出ないか。
4. root外の通常pathとsymlink、高乱雑性値、種別不明、次の絶対path表記を、成功成果を返さず固定語彙で停止するか。
   - `work=/Users/example/project`
   - `absolute path:/Users/example/project`
   - `file:///Users/example/project`
5. 新入口からfile書込み、directory作成、network、外部process、Git、権限変更、環境値解決へ到達しないか。
   少なくとも一つ、リポジトリ外の合成入力と故障注入で反証してください。
6. `pyproject.toml`から作ったwheelに`reviewcompass3-session-artifact`が入り、リポジトリ外の新環境へ導入した
   実行名から合成例を処理できるか。
7. 対象試験12件、G25関連55件、正規全試験を独立再実行し、終了コードと状態識別値を観測commitへ結び付けられるか。
   件数は観測値であり恒久値ではありません。
8. 新入口の表示が、Human受入前の`provisional / non-normative / promotion_required: true`になっているか。
9. その他の低い乱雑性の機微情報をすべて検出する保証や外部送信許可を、成果が暗黙に主張していないか。

中心判断を否定する反証を少なくとも一つ試してください。実Session記録や秘密値をrepositoryへ置かないでください。

## 4. 深さと禁止事項

本質から外れた過剰な修正案を出さないでください。目的は上記一製品入口が契約どおり完成したかの判断です。
次は依頼していません。

- G25既存10 path、G26、G30、他142 path、上流候補の整理・修正。
- 全試験の一件ずつの必要性確認、試験数や実行時間の削減。
- 新しい台帳、検査器、関門、schema、生成器、状態機械、恒久script、追加の恒久試験。
- 保存、探索、複数file処理、外部送信、環境値解決の追加。
- Task Contract、立て直し計画、第4段、第5段の全面再レビュー。

止める指摘がある場合は、中心判断を崩す具体的な一原因へまとめ、不可欠な最小訂正だけを示してください。

## 5. 出力形式

1. 判定：`verified`、`correction_required`、`reported_unverified`、`report_execution_mismatch`のいずれか
2. 止める指摘（0件なら0件）
3. 報告不一致（0件なら0件）
4. 開発物の機能と用途を平易に説明
5. 変更範囲とREDからGREENへの移行
6. 安全な出力、入力境界、禁止副作用
7. 配布物と導入済み実行名
8. 対象・関連・正規全試験と状態の結び付き
9. 試した反証と結果
10. 利用者が完成判断前に判断する点
11. 未実施事項

Human受入、正式・安定表示への昇格、第5段完了を代行しないでください。fileの作成・変更、stage、commit、push、
履歴書換え、外部送信、コード・試験・設定・Issue・TODOの変更は行わないでください。一時材料はrepository外に
置いてください。
