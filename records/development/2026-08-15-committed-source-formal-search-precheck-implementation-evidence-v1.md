# 正式コード検索の確定コミット事前確認 実装Evidence v1

- 実施日：2026-08-15
- 対象Decision：`DEC-COMMITTED-SOURCE-FORMAL-SEARCH-PRECHECK-2026-08-15-V1`
- 対象：`tools/development/work4a_rebuild_v3.py`
- 判定：`implemented_and_related_tests_passed`

## 1. TDDの失敗から成功

【実測】製品実装より前に`tests/test_work4a_committed_source_observation.py`を追加し、対象6件を単独実行した。
実装前は6件すべてが`capture_committed_observation`未実装を理由に失敗し、終了コード1だった。

【実測】試験を変更せず、`tools/development/work4a_rebuild_v3.py`だけへ正式観測入口を実装した。同じ6件は
6件成功、終了コード0へ移行した。

## 2. 実装内容

【実測】正式入口`capture_committed_observation`は、既存の`preflight_next_work`を再利用し、次を行う。

- repository root、未commit変更、追加登録、未登録file、表示を隠した差分を確認する。
- `git rev-parse --verify HEAD^{commit}`でローカルcommit識別値を取得する。
- `git ls-tree -r --name-only HEAD -- <include_root>`でcommit内の候補pathを取得する。
- source universe規則で対象pathを絞り、作業場所の観測集合と完全一致させる。
- 一致後にだけ既存`capture_observation`へ、Gitから導出したcommit識別値を渡す。

【実測】実装が呼ぶGit操作は`rev-parse`、`status`、`diff`、`ls-files`、`hash-object`、`ls-tree`の読取りだけである。
commit、add、push、fetch、network、外部repository参照は実装にない。

## 3. 確認例

| 例 | 結果 |
| --- | --- |
| 変更なし・外部repositoryなしのローカルcommit | Gitから導出したcommit識別値で成功 |
| 追跡fileの未commit変更 | `uncommitted_repository_state`で停止 |
| 追加登録済み・未commitの新規file | 同じ理由で停止 |
| 未登録の新規file | 同じ理由で停止 |
| Gitの無視指定に入れた未登録Python file | `committed_source_set_mismatch`で停止 |
| Git repositoryでない作業場所 | `committed_source_unavailable`で停止 |

## 4. 関連確認

【実測】新規6件、Work 4A v3からv3.3の既存試験、作業単位遷移、権威参照をまとめた関連107件は
107件成功、終了コード0だった。

【実測】初回の正規全試験は1,743件成功・3件失敗だった。3件はすべて、開発方針のSHA-256を更新した後も
`TODO_NEXT_SESSION.md`が旧値を参照していたことを検出した。共通のTODO更新手順で参照を訂正し、正規入口を
一回だけ再実行した結果、1,746件成功、失敗・error・skip 0、終了コード0、Python 3.13.14、pytest 8.4.2、
runner版2、fallbackなしだった。リポジトリ外の受領記録SHA-256は
`4934159d21f43538cfceb5eb5e9c7e1682cfa1dd4a549145bdd19173fd6cd9d1`である。

【実測】変更後の内容識別値は次のとおりである。

- 実装file SHA-256：`382e4edc608020dfcea1ab364d3ad1c2a27e94d074b7f234385e11ee12753055`
- 試験file SHA-256：`89cfe329c47e1d9722052cac0470944c4eafa5f1dab06c95f27b00356546e018`
- 開発方針SHA-256：`9d550502038bf8d2ff230b98f4bed9c0378d925a00bbbdd54026b1b3cb7fae7a`
- source universe v5 file SHA-256：`1d2089268237a6cdddc50a93e3fb77d6f748c26f8eeaeb4981deca7d57584ffb`
- freshness policy v8 file SHA-256：`d6948eda4c1990f6675113f8dc40486654df80d23b95ec216e882b4aad14b372`

## 5. 境界

【判断】この入口が保証するのは、正式検索の観測元が一つの確定ローカルcommitと一致することだけである。
検索候補の再利用判断、コードの正式・暫定・使用停止区分、TDD実装境界、製品実装の開始可否は別判断である。

【記録】正規全試験の受領後に更新するのは、本Evidenceと現在位置TODOだけである。実装、試験、設定、
Task Contract、製品コードは変更せず、全試験結果は同じコード状態の結果として使う。

【未実施】現在の安全保存検索の再実行、製品コード、製品試験、製品設定、Task Contract、TDD境界の変更、
自動commit、push、外部送信、networkは行っていない。
