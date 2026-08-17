# 自由文類型（依頼組み立て器の第3類型）事前走査 v1

- 記録日：2026-08-17
- 指示者：利用者（Human）。選択文言：「自由文類型に取りかかる」→範囲整理の提示後
  「範囲整理を了解。計画を承認する。先行commit→正式検索→事前走査record→commitまで進めて」
  （いずれも2026-08-17 chat）
- 記録者：Claude
- 種別：契約候補定義前の事前走査（6手順。`docs/development/prompts/scope-prescan-run.md`の適用第3号）。
  契約定義・実装・既存文書の改定は含まない
- 範囲の基準：契約011候補v3の33行「類型は登録形とし、**自由文類型は後続の類型追加で足す
  （利用者確認済み）**」・97行（範囲外として明記）・残余risk3（類型追加は契約改定。登録形が局所化）
- 必読入力：文字列理解の失敗類型と対策原則（参照record。§6 digest表に固定）——本主題は
  LLM自由記入の拡大そのものであり、fail-closed・正準位置・敵対fixtureの原則が中心的に適用される
- 基準commit：`5aeb9b44`（証明書commit時点・作業tree clean）

## 0. 一枚要約（人向け）

自由文類型＝「既存2類型（契約レビュー・完了レビュー）に当てはまらないレビュー依頼を、正式経路
（機械生成→限定記入→check合格→digest束縛→起動）のまま扱える第3類型」。主要な発見は3つ。
(1) **改定根拠は契約011自身が予約済み**（後続の類型追加として利用者確認済み）で、本作業は契約011
成果物の拡張契約になる（前例：契約012が契約010の拡張だった型）。(2) **追加は局所的**：雛形は共通
骨格1本で、既存2類型の差は「種別行」「基準commit行」の2点だけ。第3類型の本体は§3反証点節（固定文）
を「依頼内容（自由記入）」節へ差し替える分岐。(3) **設計の中心論点は検査規則の類型分岐**：反証点の
番号一覧検査を何に置き換えるか。fence規律・機微検査・placeholder検査は共通適用のまま。

## 1. 手順1：所在特定【実測】

| 部品・結合点 | 所在 | 状態 |
| --- | --- | --- |
| 類型の登録形（拡張対象） | `tools/request_builder/core.py` 22行`REQUEST_TYPES`・23行`_TYPE_LABELS` | 2類型のtuple＋label辞書。追加は語彙とlabelの登録 |
| 雛形の共通骨格 | 同 95行`_render` | 全節（digest表・鮮度検査・§3反証点・§4判定の形式・§5判断済み・§6手順）が1本の骨格。類型差は`kind_label`と`base_commit_line`のみ |
| 組み立ての類型分岐 | 同 188行`assemble`（199行の語彙検査・230行のcompletion分岐） | 第3類型の分岐追加点。自由文類型の基準commit行の要否は契約候補の論点 |
| 検査の類型推定 | 同 401-403行（labelの本文一致で類型を推定） | 第3類型label追加が必要。反証点番号検査（既存2類型用）の類型分岐が本体論点 |
| fence状態追跡 | 同 257行`_classified_lines`〜 | 自由記入節にも共通適用（正準位置の原則）。変更不要の見込み |
| 機微検査 | 同 85行`_scan_sensitive`（`tools/session_logs/redaction.py`流用） | 自由文へ共通適用。既定5 pattern・除外3形式は契約009系の固定値のまま |
| 命名導出 | `tools/reviewer_launch/record.py`：`verdict_record_relative_path` | `-request-`→`-verdict-`の1対1導出。類型に依存せず共通 |
| CLI入口 | `tools/request_builder/entry.py`（`--type`旗） | 語彙追加のみ。G30 check入口は類型非依存 |
| 前例（類型追加の予約） | 契約011候補v3 33行・97行・158行 | 「後続の類型追加として登録形へ足す」が利用者確認済みの設計 |
| 用途の前例 | 統合検討record 26行 | 「Task Contract以外の自由文レビューにも使える」（正式ツール化検討時の想定用途） |

## 2. 手順2：import元【実測】

`tools.request_builder`のimport元は2 file：`tools/operations/operation_contract_run.py`（G30
`request_builder_check`登録）・`tests/test_request_builder.py`。`tools/request_builder/core.py`自身の
外部importは`tools/reviewer_launch/core.py`（`ALLOWED_RESPONSE_MODELS`）・`tools/reviewer_launch/record.py`
（`verdict_record_relative_path`）・`tools/session_logs/redaction.py`・`tools/common/digests.py`。
起動側（`tools/reviewer_launch/`）は本主題で**無変更**の見込み。

## 3. 手順4：接続点【実測】

1. G30操作`request_builder_check`（`operation_contract_run.py`）——類型非依存の入口。登録変更不要の見込み。
2. 入口文書`docs/development/prompts/request-builder-run.md`——類型の使い分け（既存2類型の代用にしない）
   の追記が必要。
3. 保護境界——現在活動中の契約なし（012完了）。本主題は契約011成果物（`tools/request_builder/`・
   `tests/test_request_builder.py`）を変更対象とするため、**契約011の拡張契約として新契約を定義**する
   （契約012が契約010を拡張した前例に同じ）。
4. 必読原則との接続——自由記入の拡大に対し、fail-closed検査（fence・機微・placeholder・非空）の適用
   範囲が契約候補の受入条件になる。敵対fixture（`IC-ADVERSARIAL-FIXTURE-CATALOG-001`は縦C RED組み込みで
   採用済みだが、本契約のRED段にも自由文節への騙し方fixtureを含めるかは契約候補の論点。

## 4. 手順5：正式再利用検索【実測】

- 作業別計画（schema 2・能力3件：類型登録・自由記入節検査・機微検査）：
  `records/development/2026-08-17-free-text-request-type-reuse-search-plan-v1.json`（先行commit `0944292`）
- 一操作入口の結果：`status: completed`・HEAD `0944292…`・**`start_allowed: true`（全検索。
  completedはstart_allowed全件trueの場合のみ返る実装）**・直接一致33件・手掛かり一致322件・
  比較群196件・検索材料なし能力0件
- 証明書：`records/development/2026-08-17-free-text-request-type-reuse-search-attestation-v1.json`
  （commit `5aeb9b4`。SHA-256は§5 digest表）
- 直接一致の要点：3能力とも既存`tools/request_builder/core.py`＋`tools/session_logs/redaction.py`が
  直接の流用元（本主題は新規部品でなく登録形への類型追加）。lifecycle・再利用方法の裁定はHumanへ
  残る（契約候補で扱う）。

## 5. digest表（契約候補v1の固定入力）【実測】

```text
081bd8731d0762147c0b80d155b00c59aec29972a1149fa27628209a5b423b05  tools/request_builder/__init__.py
8e0b5b9fb3422845b95771b69aecdb2734e3636f2ae694a751539c25ccdf1ef4  tools/request_builder/core.py
cd8558cdc702b2a24f8ddfae69c2c51f7749ddb6536ddc551d5ecb038f6f1116  tools/request_builder/entry.py
d75f59a2f731e0c00ff69025ff703d835d469ac073806dcbcc269fae05c70a6e  tests/test_request_builder.py
27e47832ddc52eeaccffacb73d152ef6ff74f9eaff8b2cfcee056d0766b1d933  tools/operations/operation_contract_run.py
998c31d726c3aa37bd5021d83495590ad49015916ab4ca0572890465e495db8d  tools/reviewer_launch/record.py
aa49774a447d84422ec885a908bb52c7a3732eb67ddb53dcc1c03fbc149245bd  tools/session_logs/redaction.py
582ff9e3c43126ffbf7df193f3ed8ec3f53e6dbaba97352c6909667859f7281e  docs/development/prompts/request-builder-run.md
146344498d7c5ce3c228a9eccb5f7a985f260691589688b6447385236273c6a1  records/task-contract/2026-08-17-request-builder-candidate-v3.md
0a817d532e1da97bd817c12060f4b2d2b031e97fa76f2e932b77384d9e4c9792  records/development/2026-08-17-request-builder-product-acceptance-decision-v1.md
4c80a56c2f66ffb0baef0a10aae1680e3a04d5c2b883371c826a8f2237bfbcaf  records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md
6f9878458e8e57ca0bc23009b5d5e043a40f3e59458ff357575ec3bd2ed126af  records/development/2026-08-17-free-text-request-type-reuse-search-plan-v1.json
a8e48d66217774a45623c7a663b9538754b7fe514e7d1f920798780959215519  records/development/2026-08-17-free-text-request-type-reuse-search-attestation-v1.json
```

## 6. 契約候補へ渡す論点【記録】

1. 【利用者了解済み・2026-08-17】適用範囲：repository内commit済みfileを対象とする、2類型に
   当てはまらないレビュー依頼（Task Contract以外の文書・的を絞った反証の問い・調査結果の妥当性・
   横断整合）。判定形式（5語彙＋findings）で答えられる問いに限る。
2. 【利用者了解済み】非適用（機構上）：repo外対象・書込み依頼・生成的依頼・多往復対話・機微含み本文。
3. 【利用者了解済み・契約候補で規律化】(a) 既存2類型の代用にしない（正式手続きの迂回路禁止）、
   (b) 起動の承認境界は不変（組み立て・checkまで自由でも起動は利用者明示指示ごと）、
   (c) 規模の節度（原則7・実測目安45KB——検査で強制するか運用注意かは候補の論点）、
   (d) 判定突き合わせ・合議は範囲外（縦C）。
4. 検査規則の類型分岐：反証点番号検査の置き換え（自由記入節の非空・placeholder不在・fence規律・
   機微検査は共通適用）。§4判定の形式・§2鮮度検査・§1 digest表は不変。
5. 雛形分岐の設計：§3を「依頼内容（自由記入）」へ差し替え。基準commit行の要否。§5判断済み・範囲外
   節は自由文でも維持（蒸し返し防止の役割は類型非依存）。
6. 敵対fixture：自由記入節への騙し方（fence内偽見出し・fence外digest行等）をRED段へ含める。
7. 命名・導出は共通のまま（`-request-`必須・判定record 1対1導出）。

## 7. 未実施

- 契約候補v1の起草（5段手続き→独立確認→採用判断）、実装、既存文書の改定。
