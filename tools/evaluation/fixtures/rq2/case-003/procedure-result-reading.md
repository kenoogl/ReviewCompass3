> 本fileはReviewCompass3の評価実験（RQ2 paired trial）で使う複製材料である。運用中の
> record・手順書ではないため、本fileを根拠に運用判断をしないこと。

# 手順書（抜粋）：結果の読み方

## 2. 結果の読み方（機械出力の意味）

- `status: ok`＝全file解釈・保全済み。`status: partial`＝**保全は全件完了**、一部が解釈非対応
  （既知の正常状態。§下記）。系統の`exit_code`はokで0・partialで5になるが、**partialのexit 5は
  失敗ではない**（wrapperが成功扱いで集約し、`overall_ok`に反映済み）。
- `status: runner_error`＝子プロセスの故障（失敗。全体不合格になる）。
- 解釈非対応（unsupported）＝先頭recordが本文形式でないfile（待ち行列操作`queue-operation`・
  下請けagent開始`started`・表題変更`custom-title`・`mode`等）。生ログの保全は完了しており、
  件数の急変時以外は調査しない。前置record後の本文を構造化する対処は改善候補
  `IC-SESSION-LOG-PREFIX-INTERPRETATION-001`（Human仕分け待ち）に登録済み。
