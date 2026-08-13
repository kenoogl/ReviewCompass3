# 第3段 処理呼出し目録の役割再評価 独立完了レビュー v1

- 確認日：2026-08-13
- 判定：`verified`
- 作業票：`docs/development/2026-08-13-stage3-process-call-inventory-lifecycle-reassessment-bootstrap-work-ticket-v1.md`
- 作業票SHA-256：`34da7143927e8813251926eb38a3263f04c952dad31cdf69dc4bd1d02bb9b039`
- 成果：`records/development/2026-08-13-stage3-process-call-inventory-lifecycle-reassessment-evidence-v1.md`
- 成果SHA-256：`887b6f71390c899461838e8e9f9eaf6387103efc6bb383a5c6dd20a379c62f50`
- 基準commit：`2e48db71f1d52dc2acfc395f3d4f04462447091b`
- 結果commit：`ded5541e3e7cfbf8d7df766328a75c6aaabff051`

## 1. 判定

**`verified`**。

【実測】固定された二文書のSHA-256、二commitの実在、成果が示す現在の三対象のSHA-256はすべて一致した。
現在参照、過去の変更、目録件数、比較処理の誤判定、役割分類を別に照合し、成果の中心判断を覆す事実は
見つからなかった。

## 2. 止める指摘と報告不一致

- 止める指摘：0件
- 報告不一致：0件

## 3. 現在参照と正本

【実測】全Python fileの構文木から関数呼出しを独立に数えた。
`generate_process_call_inventory`の呼出しは
`tests/test_claude_bootstrap_entrypoints.py::test_process_inventory_baseline_matches_fixed_commit`の一件だけで、
`compare_process_call_inventories`の呼出しは0件だった。定義そのものは呼出しに数えていない。

【実測】`docs/development/prompts/claude-bootstrap-run.md`は
`records/session-handoffs/2026-08-11-codex-pilot-approved-claude-send-path-scope-v3.md`を正本と明記している。
同正本の§10は固定commitからの処理目録と実装後目録の比較、§11の`AC-CB-012`はその比較の合格、§13は
`tools/development/process_call_inventory.py`を変更可能pathとして明記する。v4以降の正本や、同案内から
範囲固定v3を外す現役文書は見つからなかった。

【判断】通常の製品入口から呼ばれないことだけを根拠に、処理目録全体を現在の正本と無関係とは分類できない。

## 4. 履歴と2026年8月12日の判断

【実測】commit `8cdac45`は基準JSONと、基準再生成と現在比較を一つにした試験を追加した。commit `d58ac5f`は
処理目録の生成・比較moduleを追加した。commit `354c57e`は現在比較の14行を試験から除き、試験名を現在名へ
変更した一方、moduleと基準JSONを変更していない。この三段階は成果の説明と一致する。

【記録】`records/development/2026-08-12-stage2-official-test-entry-restoration-start-decision-v1.md`は、利用者が
期限付きの先端差分制限を外し、固定基準再生成を恒久検査として残す意味単位を承認したことを記録する。
同日の実施Evidenceと独立完了レビューも、その分離を同じ内容で記録する。

【判断】この承認は実在する。ただし、第3段で維持の必要性を再評価することまで禁止する判断ではない。成果が、
当時の承認を無断で覆さず、今回の現状維持と後続の利用者裁定を分けた扱いは妥当である。

## 5. 件数と対象試験

【実測】製品の集計結果を写さず、別に実装したPython構文木の走査で再計算した結果は次のとおりだった。

- 固定基準：79項目
- 現在：110項目
- 追加：37項目
- `tools/development/claude_bootstrap.py`以外で後から増えたprocess呼出し：3件

三件は次の現在の正常な後続処理だった。

- `tools/development/claude_implementation_confirmation.py`の`subprocess.run`
- `tools/development/claude_implementation_executor.py`の`subprocess.run`
- `tools/development/claude_implementation_route.py`の`subprocess.run`

【実測】製品の生成関数でも固定commitからの再生成結果は基準JSONと完全一致し、現在比較の結果は空の一覧だった。

【実測】許可された対象試験二件を一件ずつ単独実行し、どちらも一件成功、終了コード0だった。

1. `test_process_inventory_baseline_matches_fixed_commit`
2. `test_shell_tools_agents_fallback_retry_and_generic_runner_are_unreachable`

## 6. 試した反証

中心判断「比較関数を現在の一関数境界の安全保証として扱えない」を否定するため、repositoryを書き換えず、
`tools/development/claude_bootstrap.py`内の`forbidden_process_entry`が`subprocess.run`を呼ぶ最小の構文木入力を
作った。

【実測】構文木目録にある実際の関数名は`forbidden_process_entry`だったが、
`compare_process_call_inventories`は次を返した。

```text
function: run_approved_no_tool_bootstrap
```

比較関数は関数名や所属する関数の境界を入力から調べず、対象file内にprocess追加があり、別pathに追加呼出しが
なければ固定した許可関数名を返す。この反例は成立し、中心判断を支持した。

別の反証として、固定基準との差が現在も許可結果を返す可能性を試したが、対象外pathの後続呼出し三件により
空の一覧を返した。正常な後続開発にも追従できないという成果の説明と一致した。

## 7. 役割分類と今回の扱い

【判断】次の分類は妥当である。

| 構成物 | 分類 | 独立確認の理由 |
| --- | --- | --- |
| 基準JSON | 履歴・監査資料 | 2026年8月11日の固定commitにある79項目を保存し、現在110項目の状態を表さない |
| 生成関数 | 両方 | 過去の基準を再現し、現在の正式な試験集合から一件が呼ぶ |
| 基準再生成試験 | 両方 | 過去資料の再現性を現在も検査するが、現在の外部process安全全体は検査しない |
| 比較関数 | 役割終了かつ現状保証不能 | 現在呼出し0件で、禁止関数を許可関数と誤表示し、正常な後続追加にも追従できない |
| 全体 | 混在 | 履歴資料、現在の監査再現性、役割を終えた比較処理が同じ単位にある |

【判断】今回の現状維持は過剰でも不足でもない。試験だけを先に削除すると生成関数と基準JSONの所有関係を
弱める。一括削除は現行正本と2026年8月12日の利用者判断を無断で覆す。反対に、比較関数が正しい保証を持つと
認定する根拠もない。したがって、今回は変更せず、現行の受入条件を維持するかを利用者が裁定した後に、正本改定、
削除または正しい検査への接続を別作業にする順序が適切である。

## 8. 利用者が判断する点

【判断】成果が示す三択のうち、「候補として後回し」を推奨できる。今回の作業でも外部送信入口を使っておらず、
直ちにコードを変更する必要はない。一方、現行`AC-CB-012`の記述と比較関数の実力は一致しないため、当該入口を
安全保証済みとして再利用する前には、必ず正本と現在保証を利用者が裁定する必要がある。

この選択は、外部送信入口の安全を承認する判断、正本変更、比較関数の修正・削除、第3段完了を含まない。

## 9. 未実施

コード、試験、設定、基準JSON、正本、案内、TODO、成果の変更、削除、統合、新しい検査器・試験・台帳・入口、
全試験、Claude確認、外部送信、第3段完了判断は行っていない。正式な改善候補登録と、食い違いへの対処開始も
行っていない。
