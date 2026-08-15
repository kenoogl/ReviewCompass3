# 必要な働きによるコード検索・比較候補生成との整合訂正 実装Evidence v1

- 日付：2026-08-15
- Work ID：`WORK-CAPABILITY-REUSE-SEARCH-WORK4A-ALIGNMENT-2026-08-15-V1`
- 判断：`DEC-CAPABILITY-REUSE-SEARCH-WORK4A-ALIGNMENT-2026-08-15-V1`
- 対象：開発支援用のコード再利用検索
- 判定：`implementation_verified / formal_safe_storage_search_pending`

## 1. 機能と用途

【実測】既存の比較候補生成を変更せず、後段の必要な働き検索へ記録schema 4を追加した。用途は、現在の
Git管理コードから得た検索材料を次の三種類に分け、人が再利用、修正利用、不採用、新規実装を判断できる形で
提示することである。

1. `direct_matches`：作業別計画が明示した既知の処理と、その直接の呼出し先・呼出し元。
2. `hint_matches`：参考file、処理名、必要作用に一致した検索上の手掛かり。再利用可能とは表示しない。
3. `comparison_groups`：Work 4Aが既に生成した比較集団の根拠、限界、件数、大きさ区分、代表最大三件、
   外部全件記録への参照。

比較集団の全構成員を直接対象へ複写しない。参考file内の全処理も直接対象にせず、手掛かりとして区別する。
必要作用だけの一致も手掛かりであり、既存実装があるという合格表示には使わない。

## 2. 既存設計の再利用

【実測】`tools/development/work4a_rebuild_v3.py`の`build_llm_initial_input`を使い、承認済みの比較集団要約を
そのまま取得する。要約は六種類の機械的根拠、根拠の限界、構成員数、`focused / broad / mass`の大きさ区分、
代表、全構成員を持つ既存記録への参照を含む。新しい類似度、点数、切捨て境界、中央一覧は追加していない。

- Work 4A実装SHA-256：`382e4edc608020dfcea1ab364d3ad1c2a27e94d074b7f234385e11ee12753055`
- Work 4A設計SHA-256：`b99edf3b9561da34bd4c0bd8a8e86418c36be18e202eef4f408d9b2e0392e538`
- 両fileの変更：0件

## 3. 版と過去記録

【実測】作業別計画schema 2は必要な働きの入力形として維持した。新しい正式実行は検索記録schema 4を作る。
旧検索記録schema 3は従来の検索処理で読込み・再現する分岐を残した。旧証明書と外部記録は書き換えていない。

新しい表示は次である。

- `direct_matches_found`：直接確認対象がある。
- `search_hints_found`：直接確認対象はなく、手掛かりまたは比較集団がある。
- `no_search_material`：この機械検索で確認材料を得られなかった。

機械処理は「必要な実装が既に存在する」と判断しない。`human_adjudication_required: true`を維持する。

## 4. 失敗確認から成功への移行

【実測】実装前に対象二fileの試験を単独実行し、16件中4件失敗、12件成功、終了コード1を確認した。

- 新しい区分済み検索が存在しない三件。
- 一操作入口が新結果を生成しない一件。

【実測】最小実装後、同じ対象試験は16件成功、終了コード0となった。確認内容は次である。

1. 直接対象、手掛かり、比較集団を混同しない。
2. 同じfileにあるだけの別処理を直接対象へ昇格しない。
3. 必要作用だけの一致を手掛かりと表示し、実装済みとは表示しない。
4. 比較集団の全構成員を後段結果へ複写せず、既存記録参照を保つ。
5. 検索材料がない働きを別表示する。
6. 旧schema 3記録を従来規則で再現できる。
7. 正式な一操作入口が計画schema 2から記録schema 4と証明書を作る。

## 5. 関連試験と正規全試験

【実測】Work 4A、Work 4B、鮮度、外部化、正式入口を含む関連14 fileは181件成功、終了コード0だった。

【実測】正規全試験は1,762件成功、失敗・error・skip 0、終了コード0だった。Python 3.13.14、
pytest 8.4.2、runner版2、代替実行なしである。

- リポジトリ外receipt：`/private/tmp/reviewcompass3-capability-grouped-search-full-receipt-v4.json`
- receipt SHA-256：`bc12e4bb894484db4806a7ba6850c4ff3663e196d68ba7f04892c3376f7cdebe`
- 結び付く状態識別値：`19e85f7ddcb27495eeb70a7fd39c3376622d403632675663d6506e43669ab710`

receiptは本Evidence追加前のコード・試験状態へ結び付く。本Evidenceの追加後、コード・試験・設定に変更がないことを
差分で確認し、文書一件の追加だけを理由に全試験を繰り返さない。

## 6. 変更物の内容識別値

- `tools/development/reuse_search_record.py`：`a0b8ad30f5daa9a4e021fef7e713b50954ac66633ff34f2c39566d86251270bb`
- `tools/development/formal_code_reuse_search.py`：`5f9e8054cbd70bb5be3e21e9359b8cbd9f86ea4ddfa38dc41f0c0089ee665b6d`
- `tests/test_capability_reuse_search.py`：`f8efb9031c08344f9c235daa8948841a8cd8238834d9e2e21b7b82cdb1394c0b`
- `tests/test_formal_code_reuse_search.py`：`f417c6d524b5ba579082271a0030e8cb8e57420d63719d882ce4597fade46edb`

## 7. 未実施

安全保存の八つの働きに対する新しい正式検索、検索結果の採否、製品TDD境界、製品コード、製品試験、製品設定、
安全保存Task Contract、比較候補生成、TODOは変更していない。自動commit、push、外部送信、履歴書換えは行っていない。
