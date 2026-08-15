# 最小運用契約実行 blocking 3件の訂正Evidence v1

- 実施日：2026-08-16
- 契約：`TC-RC3-PRODUCT-MINIMAL-OPERATION-CONTRACT-EXECUTION-006 / v4`
- 訂正根拠：独立完了レビューv1（判定`correction_required`、blocking 3件）
  `records/development/2026-08-16-minimal-operation-contract-execution-independent-completion-review-v1.md`、
  SHA-256 `38460b84e469cc81950633b3026cb195d6c308e4aaa171a22d10458cd0e13281`、単独commit `06742d9c41798817d26e65ab415a9fcbea1c1b3a`
- 訂正担当：Claude
- 訂正範囲：契約§12の上限内（実行核・入口・対象試験）だけ。契約本文の変更なし

## 1. 訂正内容

| Finding | 訂正 |
| --- | --- |
| B-01 読取り中の同一inode・同一size変更を受理 | 実行核`read_contract_file`の読取り前後同一性比較へ`st_mtime_ns`・`st_ctime_ns`を追加。契約§7の「読取り中変更は停止する」を同一size書換えにも成立させた |
| B-02 NUL・単独サロゲートpathが`internal_failure` | 入口`_is_absolute_lexical_path`と実行核`_absolute_path_parts`で、NUL文字・単独サロゲートを含むpathを読取り前に拒否（`invalid_path / arguments`・終了コード2） |
| B-03 機微pattern 3類型の欠落を試験が検出しない | 対象試験へbearer token・API key代入・秘密鍵blockの停止試験3件を追加。規則が欠けると停止理由と終了コードが変わり試験が失敗する形で、変異を検出する |

追加試験はB-01の反証（初回読取り直後に同一sizeの別内容を書き戻す注入で`unreadable_input / contract`）、
B-02の2変種（NUL・単独サロゲート→`invalid_path / arguments`・終了コード2・固定停止形）を含む。対象試験は61件から67件になった。

## 2. 機械確認（各単独command・終了コード個別判定）

【実測】

- 対象試験：67件成功、終了コード0
- G08対象107件・G24対象111件・G02対象158件・G30基盤e2e 38件：各単独成功、終了コード0
- 正規全試験（既存の禁止認証隔離条件）：2,305件成功、終了コード0
- `git diff --check`：終了コード0

## 3. 未実施

- 独立完了再レビュー（受入条件20）
- 利用者の製品受入（受入条件22）
