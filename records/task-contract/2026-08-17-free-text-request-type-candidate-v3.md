# 自由文類型（依頼組み立て器の第3類型） 作業契約候補 v1

- 契約ID：`TC-RC3-PRODUCT-FREE-TEXT-REQUEST-TYPE-013`
- 契約版：3
- 契約種別：受入済み縦A製品（契約011）の拡張縦切り（前例：契約012による契約010の拡張）
- 状態：`candidate_pending_independent_review`
- 作成日：2026-08-17
- supersedes：`records/task-contract/2026-08-17-free-text-request-type-candidate-v2.md`、
  SHA-256 `a8d11bb9b25829449ade68fc754c1caa013f9432407b6332573a25fe4e036d06`
- 訂正根拠：独立確認cr-013-001（`verified_with_findings`・blocking 0件）の所見
  `prompt-injection-risk`（§7.4へ残余risk 5として明文化）。v1→v2は起草側自己レビュー
  `records/development/2026-08-17-free-text-request-type-v1-self-review-v1.md`の
  SR-C13-1（類型推定を正準位置＝「レビュー種別」行だけを正とする方式へ）、SR-C13-2（必須節の
  類型分岐の明記）、SR-C13-3（既存2類型のbyte不変はgolden固定試験で機械証明）
- 直前の製品契約：`TC-RC3-PRODUCT-CLAUDE-SUBAGENT-BACKEND-012 / v2＋§7.2訂正record3件`（受入済み）
- 入力：契約011候補v3（33行・97行・残余risk3＝類型追加の予約・利用者確認済み）、自由文類型事前走査v1、
  正式再利用検索（計画・証明書・start_allowed true）、文字列理解の失敗類型と対策原則（必読）、
  利用者指示「自由文類型に取りかかる」・範囲整理の了解「範囲整理を了解。計画を承認する」・
  「契約候補v1を起草して」（いずれも2026-08-17 chat）
- 実装状態：未開始
- 危険度：中
- 危険の理由：組み立て・検査は完全local（外部送信なし）だが、成果物はheadless起動（実質の外部送信）の
  入力になる。**LLM自由記入の範囲が広がる**ため、検査の緩みは騙され・機微漏えい・解釈失敗として
  外部送信の質へ波及する

## 1. 位置と縮小境界

【記録】契約011は2類型（契約レビュー・完了レビュー）に限定して受入され、「類型は登録形とし、
自由文類型は後続の類型追加で足す（利用者確認済み）」を明記した。既存2類型に当てはまらないレビュー
依頼（Task Contract以外の文書・的を絞った反証の問い・調査結果の妥当性・横断整合）は現状、正式経路に
乗らず手書きfallbackしかない。

【判断】本契約は縦Aの第2縦切りとして、次だけを行う。

- 類型登録形へ第3類型`free_text`（label「自由文レビュー」）を1件追加する。
- 雛形は共通骨格を維持し、§3「反証点」節（固定文＋番号一覧記入）を**「依頼内容（自由記入）」節**
  （placeholder付き）へ差し替える分岐だけを設ける。§1 digest表・§2鮮度検査・§4判定の形式・
  §5判断済み・範囲外・§6手順は不変。
- 機械検査`check`へ類型分岐を追加する：自由記入節は**非空・placeholder不在**を検査し、反証点番号
  検査は適用しない。fence規律（正準位置のみ）・機微検査・digest表検査・命名導出・commit状態検査は
  **類型非依存で共通適用のまま**。
- 起動側（`tools/reviewer_launch/`）・保存・転記・照合・G30登録は無変更で流用する。

## 2. Human承認境界

- 組み立て（`assemble`）と検査（`check`）は完全localで承認不要（契約011の踏襲）。
- **起動の承認境界は類型に依存せず不変**：headless起動（外部送信・課金）は利用者のchatによる
  実施指示ごと（契約010 §2）。自由文類型だからといって起動が自由になることはない。
- 本契約内の実運用E2E（§9-5）は、対象・依頼文を利用者と確認のうえ、利用者の明示指示で起動する。

## 3. 権威、証拠

| 役割 | path | SHA-256 |
| --- | --- | --- |
| 事前走査v1（6手順・接続点・利用者了解済み範囲整理） | `records/development/2026-08-17-free-text-request-type-prescan-v1.md` | `aad68904a58f8ac79a8d99b1075636e1691684fde911fc83e15edc30437d9b55` |
| 正式再利用検索の作業別計画（能力3件） | `records/development/2026-08-17-free-text-request-type-reuse-search-plan-v1.json` | `6f9878458e8e57ca0bc23009b5d5e043a40f3e59458ff357575ec3bd2ed126af` |
| **正式再利用検索の証明書（start_allowed: true）** | `records/development/2026-08-17-free-text-request-type-reuse-search-attestation-v1.json` | `a8e48d66217774a45623c7a663b9538754b7fe514e7d1f920798780959215519` |
| 拡張対象の契約011候補v3（受入済み・類型追加の予約） | `records/task-contract/2026-08-17-request-builder-candidate-v3.md` | `146344498d7c5ce3c228a9eccb5f7a985f260691589688b6447385236273c6a1` |
| 契約011の製品受入判断（正式経路化） | `records/development/2026-08-17-request-builder-product-acceptance-decision-v1.md` | `0a817d532e1da97bd817c12060f4b2d2b031e97fa76f2e932b77384d9e4c9792` |
| 文字列理解の失敗類型と対策原則（必読・設計基準） | `records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md` | `4c80a56c2f66ffb0baef0a10aae1680e3a04d5c2b883371c826a8f2237bfbcaf` |
| 用途の前例（Task Contract以外の自由文レビュー） | `records/development/2026-08-16-review-tooling-formalization-study-v1.md` | `00b294afefa90de8cc8dc5141e9d08c23d40971d4338b9ca5021fe857f2daae0` |

流用部品のcode・文書のdigestは事前走査v1 §5の表を正とする（固定commit時点の差分0を§9-6で確認する）。

## 4. 実装方法の3案

| 案 | 内容 | 判断 |
| --- | --- | --- |
| A 手書きfallback継続 | 2類型外の依頼は手書きで作り、checkを通さず起動もしない（または手動運搬） | 正式経路外が常態化し、fence規律・機微検査・digest束縛の守りが自由文にだけ働かない。不採用 |
| B 登録形への類型追加＋検査の類型分岐 | `REQUEST_TYPES`へ`free_text`を追加し、雛形の§3差し替えと検査の類型分岐だけを実装。他は全て共通骨格・共通検査の流用 | 変更が契約011成果物内の3箇所（語彙・雛形分岐・検査分岐）に局所化。事前走査の直接一致33件をそのまま流用。契約011の登録形設計（追加の局所化）の意図どおり。推奨 |
| C 汎用文書生成基盤 | template engine導入や任意節構成の汎用化 | 契約011の3案比較で不採用済みの肥大案の再来。不採用 |

## 5. 範囲

### 5.1 範囲内

1. **類型登録**：`REQUEST_TYPES`へ`free_text`、`_TYPE_LABELS`へ「自由文レビュー」を追加（直書き定数）。
2. **雛形分岐**：§3を「依頼内容（自由記入）」節へ差し替え（placeholder
   `<<記入:依頼内容（検査してほしい問い・観点・前提）をここへ書く>>`）。実装基準commit行は
   付さない（`contract_review`と同じ扱い。対象は実装とは限らないため）。他節は共通骨格のまま。
3. **検査の類型分岐**：(a) 類型推定は本文全文のlabel検索をやめ、**正準位置（冒頭の「レビュー種別」
   行）だけを正とする**3類型対応へ是正する（SR-C13-1。自由文本文に他類型のlabelが現れても誤判定
   しない。正当な既存2類型recordの推定結果は不変——試験で固定）。(b) **必須節の類型分岐**：
   `free_text`は「反証点」に代えて「依頼内容」を必須節とする（SR-C13-2）。(c) 自由記入節の非空・
   placeholder不在検査。反証点番号検査は`free_text`に適用しない。(d) fence規律・機微検査・digest表
   検査・命名・commit状態検査は共通適用。
4. **CLI**：`--type free_text`の語彙追加のみ（G30 check入口は類型非依存で無変更）。
5. **入口文書**：`docs/development/prompts/request-builder-run.md`へ類型の使い分け（§7.2の規律）を追記。
6. **対象試験（RED先行）**：雛形生成（必須節・placeholder・語彙外停止）・検査の両向き（依頼内容節の
   非空・placeholder・番号検査の非適用・必須節分岐の節欠落停止）・**敵対fixture（自由記入節への
   fence内偽見出し・fence外digest行・自由文本文への他類型label混入で推定が騙されない）**・
   既存2類型の無変更緑＋golden固定（生成結果SHA-256の固定試験）。
7. **実運用E2E 1回**（§9-5。利用者の明示指示で起動）。

### 5.2 範囲外

- 既存2類型の雛形・検査規則の変更。起動側（`tools/reviewer_launch/`）の変更。
- 生成的依頼・多往復対話・repo外対象・書込み依頼への対応（機構上の非適用。§7.2）。
- 縦C（合議・判定record比較）。自由文依頼の内容の自動生成・`review_plan`出力の自動変換。
- 外部API直接送信経路の後続（pendingのまま）。歴史的recordの書き換え。

## 6. 固定再利用部品と保護基準

保護基準commitは本候補の固定commitとする。次を変更しない：`tools/reviewer_launch/`（契約010・012
成果。命名導出`verdict_record_relative_path`のimport利用のみ）・`tools/session_logs/redaction.py`・
`tools/common/digests.py`・`tools/development/claude_implementation_*`・`tools/external_review/send.py`・
egress・`tools/operations/operation_contract_run.py`・`tools/bootstrap/`・受入済み製品試験のうち
`tests/test_reviewer_launch.py`。変更してよいのは§8の上限だけである。

## 7. 中心的な取り決め

### 7.1 類型の登録形固定

類型の語彙・labelは直書きの契約固定定数とし、設定file・環境変数・引数から追加・変更できない。
既存2類型の値・雛形出力は一切変えない（§9-4でbyte不変を機械証明する）。

### 7.2 自由文類型の適用範囲と規律（利用者了解済み・2026-08-17）

- **適用範囲**：このrepository内のcommit済みfileを対象（digest表で束縛）とし、判定形式（5語彙＋
  findings）で答えられるレビュー依頼。例：Task Contract以外の文書レビュー・的を絞った反証の問い・
  調査結果の妥当性確認・複数recordの横断整合。
- **非適用（機構上）**：repo外対象・書込みを伴う依頼・生成的依頼（文章作成・案出し等）・多往復対話・
  機微情報を含む本文（機微検査がfail-closedで停止）。
- **規律**：(a) 既存2類型の代用にしない（契約候補の独立確認・実装完了レビューは既存類型を必ず使う。
  正式手続きの迂回路禁止——入口文書へ明記）、(b) 起動の承認境界は不変（§2）、(c) 規模の節度は
  運用注意とする（原則7・実測目安45KB。対象はレビュー役が読取り道具で部分読みでき同梱爆発は構造的に
  無いため、機械上限は導入しない——残余risk3）、(d) 判定突き合わせ・合議は範囲外（縦C）。

### 7.3 検査の共通適用

fence状態追跡（正準位置の原則）・機微検査（既定5 pattern・高乱雑性・除外3形式＝契約009系の固定値）・
placeholder検査・digest表検査・命名導出・commit状態検査は、類型に依存せず共通の1入口で不変に適用する
（文字列理解の原則record §2の1・2・4・8の履行）。

### 7.4 残余risk（明示的に受容を諮る）

1. **自由文の内容の質は機械検査で担保できない**：形式（非空・placeholder・fence・機微）の守りに
   限られ、問いの明確さ・反証可能性はLLM起草と独立確認の守りに残る（契約011残余risk1と同型）。
2. **曖昧な依頼は`unable`判定を増やし得る**：反証点の型が無い分、レビュー役が答えられない依頼が
   通り得る。緩和：判定形式§4は不変であり、`unable`・`unexamined`は正直な縮退として機能する。
3. **規模の節度は運用注意に留まる**：巨大対象×網羅観点の依頼で解釈失敗が再発し得る。緩和：原則
   record（必読）の周知＋失敗時は分割して再依頼（機械強制は将来の改定候補）。
4. **類型の使い分け誤り**：正式レビューを自由文で代用する迂回が起き得る。緩和：入口文書の規律明記
   （§7.2 (a)）＋依頼recordのlabelで種別が機械判別できるため事後監査可能。
5. **自由文によるprompt注入**（cr-013-001所見の明文化）：依頼本文がレビュー役への出力形式破壊指示
   等を含み得る。緩和：起動promptの判定形式（JSON schema）は起動側が固定し、schema不適合・抽出
   不能は`verdict_schema_nonconforming`で安全停止（未加工出力は保存済み）。fence規律・機微検査は
   組み立て時にfail-closedで適用済み。実害は「レビュー不成立で停止」に留まる。

## 8. 変更上限

1. `tools/request_builder/core.py`（類型語彙・label・雛形分岐・検査分岐）。
2. `tools/request_builder/entry.py`（`--type`語彙のみ。実質は語彙検査がcore側なら変更なしの可能性）。
3. `tests/test_request_builder.py`（既存caseを維持したまま拡張）。
4. `docs/development/prompts/request-builder-run.md`への追記（類型の使い分け規律）。
5. Evidence、独立確認、受入判断、TODO更新。

## 9. 受入条件

実装開始後は失敗試験を先に固定し、期待どおり失敗してから最小実装を行う。

1. RED：`free_text`の雛形生成（必須節・依頼内容placeholder・語彙外停止）・検査の両向き（依頼内容節の
   非空・placeholder不在・番号検査の非適用・必須節分岐の節欠落停止）・類型推定の正準位置化（自由文
   本文への他類型label混入で誤判定しない・正当な既存2類型recordの推定不変）・敵対fixture（自由記入節の
   fence内偽見出しで節解析が騙されない・fence外digest行の拒否）の失敗試験を先に固定する。
2. 実装：最小実装で全試験緑。
3. 既存2類型の互換：既存2類型の`assemble`出力が**byte不変**（同一入力からの生成結果SHA-256を試験定数へ
   固定するgolden試験で機械証明——SR-C13-3）、既存の契約011対象試験が無変更で全緑、類型推定の
   正準位置化後も正当な既存2類型recordの推定結果が不変。
4. 検査の共通適用：機微検査・fence規律が`free_text`にも働くことの両向き試験。
5. 実運用E2E 1回：自由文依頼を1件、正式経路（assemble→LLM記入→check合格→commit）で組み立て、
   利用者の明示指示でheadless起動（agy既定）し、判定record取得まで完走する。対象・依頼文は起動前に
   利用者と確認する。不成立なら停止し、自動再試行をしない。
6. 既存試験：対象suite・G30 75件・layout・正規全試験が各単独終了コード0。§6保護対象が基準commitから
   差分0。
7. 完了レビュー：agy経路（Tier 1）で実施し、`verified`系（blocking 0件）を得る（依頼recordは
   契約011の正式経路`completion_review`類型で組み立てる）。
8. 利用者が§7.4残余risk 4点を確認して製品処理を受け入れる。

## 10. 停止条件

- 既存2類型のbyte不変が保てない（雛形共通骨格の変更が必要になる）。
- 契約011受入済み試験または§6保護対象の変更が必要になる。
- 対象・関連・正規全試験または独立確認が不合格になる。

## 11. 影響、未実施、次作業

【判断】受入後は、2類型に当てはまらないレビュー依頼も正式経路（機械生成→限定記入→fail-closed検査→
digest束縛→承認つき起動→機械転記）に乗り、手書きfallbackの常態化を防げる。2 backend体制（agy／
claude-subagent）とも組み合わせ可能。

【未実施】契約採用、実装、実起動、既存成果物の変更。

次は本候補の固定commit後、5段の念入り手続き（自己レビュー→文脈整理→依頼record組み立て〔契約011の
正式経路・`contract_review`類型〕→依頼レビュー→独立確認の起動〔利用者の明示指示〕）→採用判断の順で
進める。
