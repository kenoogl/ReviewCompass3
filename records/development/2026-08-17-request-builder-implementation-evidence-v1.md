# 契約011 依頼組み立て器 実装Evidence v1

- 記録日：2026-08-17
- 記録者：Claude
- 契約：`TC-RC3-PRODUCT-REQUEST-BUILDER-011 / v3`（採用済み。採用record
  `records/development/2026-08-17-request-builder-contract-adoption-decision-v1.md`）
- 範囲：契約§9-1〜7（RED・実装・導線配備）。**§9-8実運用E2E・§9-10完了レビュー・§9-11製品受入は未実施**

## 1. 実施（RED→実装→緑）【実測】

1. RED：`tests/test_request_builder.py`（30試験）を先に固定し、module不在の状態で実行。
   結果：`30 failed`（期待どおりの失敗）。cr-011-001所見の敵対試験3件（破損placeholder・空digest表・
   既知すり抜け形の通過明示）を含む。
2. 最小実装：`tools/request_builder/`（`__init__.py`・`core.py`・`entry.py`）と`_OPERATIONS`への
   `request_builder_check`登録（`tools/operations/operation_contract_run.py`へimport 1行＋entry 9行）。
3. 緑：各単独実行の終了コード0で確認。
   - 対象試験：`tests/test_request_builder.py` → `30 passed`（一発合格）
   - G30：`75 passed`、縦B＋layout：`48 passed`
   - 正規全試験（禁止認証隔離条件）：`2,440 passed`
4. 試験の訂正：0件（RED後の試験変更なし）。

## 2. 実装した中心仕様（契約§5.1・§7の写像）

- **2類型のcode内雛形**（`contract_review`＝契約定義反証・`completion_review`＝実装完了レビュー。
  完了型は実装基準commitをGitから機械取得して埋める）。機械欄＝表題・依頼元／先（許可modelは縦Bの
  公開定数から転記）・digest表（`tools/common/digests.py`で機械計算）・鮮度検査・判定形式・手順
  （起動command・判定record導出名）。LLM記入欄＝`<<記入:`placeholder 2箇所（反証点・判断済み／範囲外）。
- **new-only書込み**：出力先が既存なら`output_already_exists`で停止（SR-C11-1）。
- **機械検査`check`**：内容検査（必須節6・placeholder完全形＋破損断片・反証点識別子の一意・記入欄の
  空内容・digest表の空拒否／実在／全件一致・明記事項・許可model照合・囲み記号・機微検査）→Git状態検査
  （参照のcommit済み・check-ignore・record自身のcommit済みと作業樹一致）の順。**commit前の実行は
  `request_record_uncommitted`だけが不合格となる途中経過**として成立（SR-C11-2どおり、両状態を試験で固定）。
- **機微検査**：既定5 pattern＋高乱雑性検知（除外3形式は契約009 v2 §7と同値の自前直書き定数。
  **同値性を試験で固定**——`send.py`実定数との一致を検査）。既知すり抜け形（64桁hexのダミー鍵）の通過を
  明示する固定試験を含む（§7.4-4の許容の可視化）。
- **命名整合**：`-request-`必須・縦Bの導出関数で判定record名を導出し、合格出力へ含める。合格出力の
  `request.sha256`はそのまま起動の`--expected-sha256`になる。

## 3. 導線配備（§5.1-5）【実測】

- `pyproject.toml`へ`reviewcompass3-request-builder`を登録し`pip install -e`で有効化。
- 別の現在位置からの実行確認：可読pathのdemo repositoryで**assemble→LLM記入相当→commit→check合格**の
  一巡を実演（合格出力にsha256と判定record導出名。demoは実演後に削除）。
- 付随の実測2件：(1) 手書きの旧依頼record（新雛形と節名が異なる）へ`check`を掛けると
  `required_section_missing`で正しく停止する（検査器は雛形準拠recordのための関門であることの確認）。
  (2) session一時領域のUUID path（hex断片のhyphen連結）を含むdemoでは機微検査が
  `sensitive_data_remaining`で正しく停止する（契約009の敵対設計「hexだけの断片連結は除外しない」の
  実演。実repositoryのpathは可読語のため影響なし）。
- G30操作`request_builder_check`を登録。run入口文書`docs/development/prompts/request-builder-run.md`と
  `AGENTS.md` §1の入口1行を追加。

## 4. 保護基準の確認【実測】

基準commit `a08844a`（契約011 v3の固定commit）からの差分：

- 保護対象（redaction・digests・縦B4 file・send.py・egress・bootstrap・reviews・design・requirements・
  受入済み製品試験）：**差分0**。
- 許可された変更：`tools/operations/operation_contract_run.py`のみ（+9行。import 1行と登録entry）。

## 5. 成果物一覧

| 種別 | path | commit |
| --- | --- | --- |
| 採用判断record | `records/development/2026-08-17-request-builder-contract-adoption-decision-v1.md` | `9d1d680` |
| 実装 | `tools/request_builder/`（3 file） | `9dab9c3` |
| 対象試験 | `tests/test_request_builder.py`（30件） | `9dab9c3` |
| G30登録 | `tools/operations/operation_contract_run.py`（+9行） | `9dab9c3` |
| 導線 | `pyproject.toml`・`docs/development/prompts/request-builder-run.md`・`AGENTS.md` §1 | `1b40578` |

## 6. 未実施（契約の残り）

- §9-8：実運用E2E 1回（本契約自身の完了レビュー依頼を本toolで組み立て→check合格→利用者の明示指示で
  縦B起動）。
- §9-10：完了レビュー（§9-8の起動が兼ねる設計）。
- §9-11：製品受入（§7.4残余risk 4点の最終受容）。
- TODO更新（本Evidence直後に共通手順で実施）。
