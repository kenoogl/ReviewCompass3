# 第3段 G04六試験の役割分類 Evidence v1

- 記録日：2026-08-13
- 状態：`classified_pending_independent_review`
- 対象Issue：`ISSUE-TEST-GROWTH-STATE-PINNING-001`
- 作業票：`docs/development/2026-08-13-stage3-g04-role-classification-bootstrap-work-ticket-v1.md`
- 作業票SHA-256：`51104e11ee44b18d74b89b3ff4cb709fae6a9c1c4ea43bccb29132e883a3046f`
- 基準commit：`ec1ebbc`

## 1. 開始確認

【判断】開始可。作業票の六件は意味群分類EvidenceのG04と一致した。入力の内容識別値は固定値と一致し、
作業は読み取りと本記録一件に限定される。試験、製品コード、設定、証跡、対応表、外部状態を変更しないため、
危険度は`low`のままとした。

## 2. 先行記録の報告不一致

【実測】意味群分類Evidence §5と、その独立完了レビュー§5は「G04六件すべての試験名が当時の宣言対応表から
参照される」と記録した。宣言対応表のJSONを試験本文の関数名と機械照合すると、参照されるのは次の五件だった。

- `test_existing_pilot_commands_and_six_egress_files_remain_unchanged`：`AC-CB-013`
- `test_red_suite_uses_only_fake_process_and_never_launches_claude`：`NG-CB-002`
- `test_scope_review_human_red_approval_and_all_fixed_inputs_are_pinned`：`ST-CB-001`
- `test_declaration_map_keys_equal_scope_requirement_ids`：`OUT-CB-001`
- `test_red_evidence_keeps_green_fields_explicitly_unimplemented`：`OUT-CB-002`

`test_process_inventory_baseline_matches_fixed_commit`は対応表に無い。現在の同試験ファイル8関数のうち、対応表参照は
7件、未参照は同試験一件だった。

【判断】これは`report_execution_mismatch`である。先行記録の「六件すべてが対応表参照」という主張と、
独立レビューの同確認を古いものとして扱う。401件の欠落0、重複0、G04の六件という母集団、G03との境界は
変わらないため、影響は対応表を根拠にしたG04選定理由と本役割分類に限る。本記録では正しい五件対一件を使う。

【判断】旧記録をその場で書き換えず、本節を追加の訂正証跡とする。本記録の独立レビューでは、この訂正と
分類結果をまとめて一回確認する。

## 3. 六件の役割分類

| 試験 | 分類 | 現在の利用者・検出する欠陥 | 履歴・回復 | 重複・固有性 |
| --- | --- | --- | --- | --- |
| `test_process_inventory_baseline_matches_fixed_commit` | 役割終了候補 | 現在の利用者は同試験自身だけ。固定commitから生成した処理目録が保存JSONと同じことだけを確認する | baselineと試験は`8cdac45`、生成処理は`d58ac5f`から回復できる | 生成処理と比較処理は製品コード、設定、正規入口から呼ばれない。試験単独削除では未使用の生成処理が残るため、別の結合単位で扱う |
| `test_existing_pilot_commands_and_six_egress_files_remain_unchanged` | 両方 | 現在のPilot三命令の引数を確認する一方、外部送信六ファイルを基準commitのbytesへ固定する | 基準bytesはGitから回復できる | Pilot命令はCLI試験、外部送信の動作は42件の現役試験が別に確認する。ただし命令集合と六ファイル全bytes固定が一関数に混在するため、一括削除せず分離または置換要否を実施計画で判断する |
| `test_red_suite_uses_only_fake_process_and_never_launches_claude` | 現在の動作保証 | 現在のClaude初期接続試験が使う共通補助処理を構文木で読み、直接の外部Claude実行を混入させない | 補助処理の当時状態は`8cdac45`から回復可能 | 現役試験は実際に補助処理の偽processを使うが、この試験はその試験基盤自体の安全を静的に確認する固有境界である。履歴固定群と同時に削除しない |
| `test_scope_review_human_red_approval_and_all_fixed_inputs_are_pinned` | 役割終了候補 | 現在の製品処理は三つの開始資料の内容識別値や文言を入力にしない。過去の開始条件だけを固定する | 三資料は`8cdac45`で現在fileとbytes一致し、完全回復できる | 現在の承認と送信境界は別の現役試験が製品処理へ直接確認する。履歴資料の固定だけなので、現在全試験へ残す必要性は見つからない |
| `test_declaration_map_keys_equal_scope_requirement_ids` | 役割終了候補 | 2026-08-11のRED対応表が32要求IDを持つことだけを確認し、現在の製品要求集合を確認しない | 対応表と試験は`8cdac45`で現在fileとbytes一致し、完全回復できる | 対応表は現在の合否正本ではない。宣言検査器は別試験で現在の形式・欠落・重複を確認する。本試験の現在利用者は見つからない |
| `test_red_evidence_keeps_green_fields_explicitly_unimplemented` | 役割終了・削除判断済み | RED証跡の三文言だけを固定し、製品動作や証跡全体を保証しない | 証跡と試験は`8cdac45`で現在fileとbytes一致し、完全回復できる | 再評価v3と二者確認を経て利用者が削除を承認済み。実施は複数群をまとめた計画まで待つ |

## 4. 機械確認した事実

【実測】六件の関数本文をPython構文木で読み、行範囲、条件文、呼出し先を抽出した。六件はG04の抽出条件と
完全一致した。試験名の参照、製品処理、設定、正規入口を検索した結果、処理目録生成器を参照するコードは
対象試験と生成器自身だけで、履歴資料三種を現在の入力として使う製品コード、設定、案内入口はなかった。

【実測】`test_claude_bootstrap.py`と`test_claude_bootstrap_adversarial.py`は、共通補助処理の
`install_fake_process`を実際に使い、payload process、認証、送信前停止、host拒否を偽processで確認する。
したがって、三番目を履歴専用とは扱えない。

【実測】Pilotの三命令は`test_pilot_collaboration_cli.py`が実際のCLIを使って引数拒否と結果を確認し、外部送信境界は
egress系42件が承認、内容束縛、機密情報、送信関門を確認する。一方、二番目の一関数には、現在の命令集合と
基準commitからの六ファイル全bytes固定が同居している。

【実測】固定資料六ファイルについて、現在bytesとcommit `8cdac45`のGit物体を比較し、全六ファイルが一致した。
対象は処理目録、宣言対応表、RED証跡、範囲レビュー、Human RED開始判断、範囲固定v3である。

## 5. 意味的な後続単位

【判断】六件を一括削除しない。次の四単位へ分ける。

1. **維持候補**：三番目。現在の試験基盤が実外部処理を作らない安全境界として分離する。
2. **混在の整理候補**：二番目。現在のPilot命令確認と履歴的な全bytes固定を一関数から分ける必要性を、
   既存現役試験との重複を含めて実施計画で比較する。
3. **履歴固定の整理候補**：四番目、五番目、六番目。同じ2026-08-11の開始資料、対応表、RED証跡を
   現在全試験から固定する三件である。六番目だけ削除承認済みで、他二件はまだ未承認である。
4. **未使用処理との結合整理候補**：一番目。試験だけでなく、現在利用者の無い
   `tools/development/process_call_inventory.py`と処理目録資料の扱いを同じ意味単位で調べる。

【判断】次に削除へ進まず、G04で見つかった「履歴固定」と同型の候補をG06、G07、G11から軽量抽出し、
複数群をまとめた実施計画へ接続する。現在の安全境界は群ごとに分離し、一律の削除候補にしない。

## 6. 反証

【実測】中心判断「G04六件は履歴固定だけではなく現在安全を含むため、一括削除できない」への反証として、
全六件に現在の製品利用者が無い可能性を検索した。三番目は現在のClaude初期接続試験基盤を直接検査し、二番目は
現在のPilot命令集合も検査するため、反証は不成立だった。

【実測】逆方向に「履歴固定四件も現在製品に必要ではないか」を検索した。処理目録生成器、開始資料三件、
宣言対応表、RED証跡を現在入力にする製品コード、設定、正規入口は見つからず、固定commitから完全回復できた。
ただし一番目は未使用の生成処理と結合するため、試験だけの削除単位にはしていない。

## 7. 手戻り

【実測】固定資料六ファイルの履歴照合を最初にshellの`path`変数を使うloopで実行したため、zshの実行探索先を
上書きし、六回とも`git: command not found`、終了コード127となった。結果は判断に使わず、Pythonから引数配列で
Gitを六回実行する機械処理へ置き換え、全件bytes一致、終了コード0を確認した。

【判断】期待executorと実executorはいずれも機械処理で、手作業への切替はない。原因はシェル変数名の選択である。
今後の同型照合は、変数展開を含むshell loopではなく、引数配列を使う既存Python実行または個別Git commandを使う。

## 8. 未実施

【未実施】試験、製品コード、設定、証跡、対応表、宣言データの変更、削除、統合、試験実行、全試験、変異検査、
新しい台帳・検査器・試験の追加、実施計画の確定、Claudeへの手動受け渡し、外部送信、push、履歴書換え、
第3段完了は行っていない。
