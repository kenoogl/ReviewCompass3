# 第3段 G07赤試験宣言契約の限定修正 Evidence v1

- 記録日：2026-08-13
- 状態：`implemented_pending_independent_completion_review`
- 対象Issue：`ISSUE-TEST-GROWTH-STATE-PINNING-001`
- 利用者承認：2026-08-13、案A
- 作業票：`docs/development/2026-08-13-stage3-g07-declaration-red-contract-correction-bootstrap-work-ticket-v1.md`
- 作業票SHA-256：`f08d004b8a782cf1da7583f9511bc52f21f516f1feece4fddfba38a9ffee0800`
- 基準commit：`8608df2`
- 作業票commit：`5ee4a79`

## 1. 実施

【実測】承認済み案Aに従い、次の二fileだけを変更した。

- `docs/development/work-review-protocol.md`
- `tests/test_declaration_red_map_check.py`

【実測】現行レビュー手順は、宣言から赤試験への対応表を作る場合に、対応表版2、各赤試験の予定失敗理由、
`verify_red=True`、`minimum_red_contract_version=2`を一体で必須にした。結果全体が`status: passed`であり、
`execution_errors`、`reason_mismatched`、`mismatched`、`unknown`がすべて0件でなければcommitしない。

【実測】既存の空条件試験一件は、同じ試験関数の中で次の二入力を別々に作り、それぞれ固有の所見を確認する形へ
変更した。

1. 試験file一覧を残し、宣言だけを空にする。
2. 宣言を残し、試験file一覧だけを空にする。

新しい試験関数、検査器、台帳、入口は追加していない。検査処理、設定、対応表、台帳、他試験、AGENTS、計画、
TODOは変更していない。

## 2. 試験結果

【実測】G07追加8件を単独実行し、8件成功、終了コード0だった。

【実測】専用四fileを実行し、22件成功、終了コード0だった。

【実測】混在二fileの関連7件を実行し、7件成功、終了コード0だった。関連29件は22件と7件の合計で、全件成功した。

【実測】現行レビュー手順への導線を確認する既存試験一件は成功、終了コード0だった。

【実測】変更した試験fileを収集すると9件、終了コード0だった。変更前と同じ9件で、試験数は増えていない。

## 3. 二つの空条件の変異確認

【実測】作業票commitのリポジトリ外複製二つへ、変更後の既存試験を置き、現在検査処理の拒否分岐を一つずつ
無効にした。

- 完全範囲で宣言が空の場合の拒否分岐だけを無効にすると、既存一試験は1件失敗、終了コード1だった。
- 完全範囲で試験file一覧が空の場合の拒否分岐だけを無効にすると、同じ既存一試験は1件失敗、終了コード1だった。

【判断】変更前は宣言側の一変異を関連22件が見逃したが、変更後は試験数を増やさず、二つの拒否分岐を個別に検出する。

## 4. 現行手順と既存版2の接続

【実測】現行レビュー手順を再読込みし、次の文字列が全て存在することを機械確認した。

- `red_verification_contract.version`
- `expected_failure_reason`
- `verify_red=True`
- `minimum_red_contract_version=2`
- `execution_errors`
- `reason_mismatched`
- `mismatched`
- `unknown`

【実測】別の一時対応表で、旧方式へ試験準備の`ModuleNotFoundError`を与えると、従来どおり`passed`、
`verified: 1`となった。同じ意味の入力を版2、予定失敗理由、最低版2で照合すると`failed`、
`execution_errors: 1`となった。

【判断】旧方式の互換動作は変更していない。現行手順が既存の安全な版2を必須にしたことで、通常の完成経路では
準備失敗を予定した機能不足として誤承認しない。

## 5. 変更範囲と三案の選択維持

【実測】検査処理の既定値、版1の対応表19件、版2の対応表2件、関連する29試験のうち対象一件以外は変更していない。

【判断】案Bの既定変更と試験追加、案Cの方式廃止は実施していない。案Aの簡潔さ、追加の常駐状態0、既存互換性、
二つの誤判定への直接性を維持した。

## 6. 未実施

【未実施】検査処理、設定、対応表、台帳、他試験、AGENTS、計画、TODOの変更、新しい試験・検査器・台帳・入口、
全試験、外部送信、Claude確認、別群、全401件、第3段完了判断は行っていない。全試験は、製品コードと検査処理を
変更せず、変更が手順書一件と既存試験一件に限られるため、作業票どおり対象・関連試験へ限定した。
