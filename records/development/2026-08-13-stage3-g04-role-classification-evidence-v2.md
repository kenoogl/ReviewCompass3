# 第3段 G04六試験の役割分類 Evidence v2

- 記録日：2026-08-13
- 状態：`corrected_pending_one_time_review`
- 置換元：`records/development/2026-08-13-stage3-g04-role-classification-evidence-v1.md`
- 置換理由：四番目の現役正本参照と三つの報告不一致を独立レビューが検出した
- 作業票：`docs/development/2026-08-13-stage3-g04-role-classification-bootstrap-work-ticket-v1.md`
- 基準commit：`9351429b386a610ec521623563cf5394cf04102e`
- 独立レビュー：`records/development/2026-08-13-stage3-g04-role-classification-independent-completion-review-v1.md`
- 独立レビューSHA-256：`6264a3095c67f343308d5262659ea55a27d38540de2d7ba676172dcd00bd9cae`

## 1. 限定修正

【判断】v1の母集団六件、宣言対応表の五件対一件という訂正、一番目・二番目・三番目・五番目・六番目の
分類は維持する。次の四点だけを修正する。

1. 四番目を`役割終了候補`から`両方`へ変更する。
2. 現在の案内入口が範囲固定v3を正本として参照する事実を追加する。
3. 「先行独立レビューも六件すべてが対応表参照だと記録した」という誤った帰属を取り消す。
4. 三番目の保証を、実際に静的確認する四条件へ限定する。

## 2. 対応表参照の訂正

【実測】宣言対応表から参照されるG04試験は、二番目から六番目までの五件である。一番目
`test_process_inventory_baseline_matches_fixed_commit`は対応表にない。現在の同試験ファイル8関数のうち、
対応表参照は7件、未参照は同試験一件である。

【判断】誤った「G04六件すべて」という主張があるのは、意味群分類Evidence §5である。先行の独立完了レビューは
六件の参照先を説明したが、六件すべてが対応表参照だとは記録していない。v1 §2の帰属を本節で訂正する。

【判断】401件の欠落0、重複0、G04の六件という母集団、G03との境界は変わらない。対応表をG04六件共通の
選定根拠には使わず、五件の当時要求を読む材料としてだけ使う。

## 3. 六件の役割分類

| 試験 | 分類 | 根拠と境界 |
| --- | --- | --- |
| `test_process_inventory_baseline_matches_fixed_commit` | 役割終了候補 | 現在のコード利用者は同試験だけ。固定commitの処理目録と生成処理の一致を確認する。生成・比較処理と基準JSONを同じ結合単位で調べる |
| `test_existing_pilot_commands_and_six_egress_files_remain_unchanged` | 両方 | 現在のPilot命令集合・引数と、基準commitの外部送信六ファイル全bytes固定が一関数に混在する。分離または置換を比較する |
| `test_red_suite_uses_only_fake_process_and_never_launches_claude` | 現在の動作保証 | 現在の二つのClaude初期接続試験が使う共通補助処理を検査する。確認範囲は`.run`呼出し一件、Git引数の固定文字列、`FakeClaudeProcess`の存在、`claude --`文字列の不在という四条件に限る |
| `test_scope_review_human_red_approval_and_all_fixed_inputs_are_pinned` | 両方 | 過去の範囲レビューとRED開始判断を固定する一方、範囲固定v3は現在の`docs/development/prompts/claude-bootstrap-run.md`が正本として直接参照する。三資料を一括して役割終了にできない |
| `test_declaration_map_keys_equal_scope_requirement_ids` | 役割終了候補 | 2026-08-11時点のRED対応表の32要求IDだけを確認し、現在の製品要求集合を確認しない。対応表は固定commitから回復できる |
| `test_red_evidence_keeps_green_fields_explicitly_unimplemented` | 役割終了・削除判断済み | RED証跡の三文言だけを固定する。製品動作と証跡全体を保証せず、固定commitから回復できる。利用者の削除承認済みだが実施待ち |

## 4. 現在の利用者、重複、履歴回復

【実測】処理目録の生成・比較処理を使う現在コードは一番目の試験以外に見つからない。Pilot三命令の実際の
引数拒否と結果は`tests/test_pilot_collaboration_cli.py`、bootstrap命令の二入力は
`tests/test_claude_bootstrap_cli.py`、外部送信の動作はegress系42件が別に確認する。

【実測】三番目が読む共通補助処理は`test_claude_bootstrap.py`と`test_claude_bootstrap_adversarial.py`から
現在も使われる。ただし三番目は任意の外部処理起動手段を網羅しない。

【実測】現在の`docs/development/prompts/claude-bootstrap-run.md`は、四番目が固定する三資料のうち
`records/session-handoffs/2026-08-11-codex-pilot-approved-claude-send-path-scope-v3.md`を正本として直接参照する。
この現役参照を理由に四番目を`両方`とする。

【実測】処理目録、宣言対応表、RED証跡、範囲レビュー、RED開始判断、範囲固定v3の現在bytesは、commit
`8cdac45`のGit物体と全六件一致した。回復可能性はあるが、現在の正本参照を消す根拠にはしない。

## 5. 意味的な後続単位

【判断】六件を次の五単位へ分け、一括削除しない。

1. **維持候補**：三番目。実際の四条件へ保証範囲を限定する。
2. **命令と全bytes固定の混在整理候補**：二番目。
3. **現在正本と過去資料の混在整理候補**：四番目。三資料の固定を分ける必要性を比較する。
4. **履歴固定の整理候補**：五番目と六番目。六番目だけ削除承認済みである。
5. **未使用処理との結合整理候補**：一番目。生成・比較処理と基準JSONを含めて調べる。

【判断】次に削除へ進まず、G04で見つかった履歴固定と同型の候補を他群から軽量抽出し、複数群をまとめた
実施計画へ接続する。現在安全を守る三番目と、現役正本を含む四番目は履歴固定だけの削除候補から分離する。

## 6. 反証と手戻り

【実測】四番目が履歴専用という反証は、現在の案内入口から範囲固定v3への正本参照により成立したため、
`両方`へ修正した。三番目が履歴専用という反証は、現在の共通補助処理利用により不成立だった。一番目の
処理目録生成器に隠れた現役コード利用者は見つからなかった。

【実測】v1作成時、固定資料の履歴照合にshellの`path`変数を使って終了コード127となった結果は採用せず、
Pythonから引数配列でGitを実行し直して全六件一致、終了コード0を確認した。今後も同型照合ではshellの
`path`変数を使わない。

## 7. 未実施

【未実施】試験、製品コード、設定、証跡、対応表、宣言データの変更、削除、統合、試験実行、全試験、変異検査、
新しい台帳・検査器・試験の追加、他群の抽出、実施計画の確定、Claudeへの手動受け渡し、外部送信、push、
履歴書換え、第3段完了は行っていない。
