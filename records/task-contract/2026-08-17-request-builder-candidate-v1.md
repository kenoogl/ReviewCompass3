# 依頼組み立て器（2類型・雛形生成＋機械検査） 作業契約候補 v1

- 契約ID：`TC-RC3-PRODUCT-REQUEST-BUILDER-011`
- 契約版：1
- 契約種別：レビュー実行体制の正式ツール化（統合検討の縦A）・第1縦切り
- 状態：`candidate_pending_independent_review`
- 作成日：2026-08-17
- 直前の製品契約：`TC-RC3-PRODUCT-REVIEWER-LAUNCH-ADAPTER-010 / v2`（受入済み）
- 入力：統合検討record（agy訂正済み）、設計方針メモ（利用者裁定2件）、縦A事前走査v1、正式再利用検索
  （計画・証明書）、利用者指示「縦A（依頼組み立て器）に取り組む」「方針了解。事前走査から進めて」
  「提案1，2，3を実行」「契約候補v1（契約011）を作成して」および裁定「コアを共有し薄いラッパーでの
  対応は、適切な対応。リファクタリングは不要と判断する」（いずれも2026-08-17 chat）
- 実装状態：未開始
- 危険度：中
- 危険の理由：外部送信・外部起動を伴わない完全local処理だが、機微検査という守りの部品の包みを新設する
  ため、検査の誤実装が後段（起動・送信）の安全前提を弱めるriskがある

## 1. 位置と縮小境界

【記録】依頼record（Reviewerへの指示書）は毎回LLMが手書きしており、契約010の運用でも2通を手書きした
（形式事故は機械で止まらない）。機械化目標の(1)自己レビュー材料・(2)文脈整理・(3)依頼組み立てが未機械化
の最後の定常手作業である。

【判断】本契約は縦Aの第1縦切りとして、**2類型（契約レビュー依頼・完了レビュー依頼）の雛形生成と
機械検査だけ**を機械化する。

- 類型は登録形とし、自由文類型は後続の類型追加で足す（利用者確認済み）。
- LLM／機械の分担線：機械＝雛形生成・digest表計算・機械検査（7項目＋`git check-ignore`＋機微検査）。
  LLMに残る＝反証点の文案・判断済み／範囲外の選定（雛形の記入欄）。
- 二段構え：`assemble`（雛形生成）と`check`（機械検査）の2入口。LLM記入は両者の間に挟まる。
- 依頼内容の質の承認手続き（5段手続きの自己レビュー・独立確認・Human判断）は変えない。本契約は
  形式の機械化だけを行う。

## 2. Human承認境界

- 本契約の処理は**外部送信・外部起動を一切行わない**（組み立てと検査のlocal処理のみ）。生成した
  依頼recordを使う起動・送信は、受入済みの既存境界（契約010 §2・契約008 v5 §2）のままである。
- 生成recordのcommitは通常の意味単位commit規律に従う。`assemble`・`check`はfileを
  `records/session-handoffs/`配下の新規pathへ書くだけで、既存fileの変更・削除を行わない。

## 3. 権威、証拠

| 役割 | path | SHA-256 |
| --- | --- | --- |
| 統合検討（利用者確定・agy訂正済み） | `records/development/2026-08-16-review-tooling-formalization-study-v1.md` | `00b294afefa90de8cc8dc5141e9d08c23d40971d4338b9ca5021fe857f2daae0` |
| 設計方針メモ（機微検査の縦A論点・利用者裁定） | `records/development/2026-08-17-review-path-design-principles-memo-v1.md` | `8e6a3668107b6bef114c2073c445092be1c54919decc65484e9a3def4b20648e` |
| 縦A事前走査v1（6手順・流用部品・論点） | `records/development/2026-08-17-vertical-a-request-builder-prescan-v1.md` | `8aa156c82653b6d873bbcf1195064f14a1a1aba3913b996225af7b2dad17a03c` |
| 正式再利用検索の作業別計画（schema 2） | `records/development/2026-08-17-vertical-a-request-builder-reuse-search-plan-v1.json` | `1a195b69803baf9355bb8648d3c6c4ab64be725454ebe8c87e6a726cb0173661` |
| **正式再利用検索の証明書（start_allowed: true）** | `records/development/2026-08-17-vertical-a-request-builder-reuse-search-attestation-v1.json` | `b081e9fa6243f46c653cd2870fc439c22f46cd903f7df21aa23f9f815e35c344` |
| 機械化目標（(1)(2)(3)の定義） | `records/development/2026-08-16-external-review-preparation-mechanization-goal-v1.md` | `46a415eb630266e23a87562e6083f873e2fe9790acd34a6699f59b30aee0b45e` |
| 実測済み雛形基準1（契約レビュー型） | `records/session-handoffs/2026-08-16-reviewer-launch-adapter-v2-review-gemini-request-v1.md` | `390bc32868a2ee99f11e68d6bb9489826681674786d64b93ea207592399ac995` |
| 実測済み雛形基準2（完了レビュー型・headless起動対象） | `records/session-handoffs/2026-08-16-reviewer-launch-adapter-implementation-completion-review-request-v1.md` | `29819b3fd33b934ed51ced3b4f4d3982939e9b5498ed3a5fd43c0c079fddb13c` |

## 4. 実装方法の3案

| 案 | 内容 | 判断 |
| --- | --- | --- |
| A 最小（既存機能のみ） | 手書きを続け、既存依頼recordを見本に複写運用する | 新規実装0だが形式事故（digest誤り・節欠落・機微混入）が機械で止まらず、機械化目標(3)に達しない。不採用 |
| B 雛形生成＋機械検査の2入口 | 類型登録形のcode内雛形から草稿を生成し、LLM記入後の完成recordを7項目＋check-ignore＋機微検査で機械検査する。核（redaction・digests・命名導出）は共有部品を流用し薄い包みだけ書く | 実測済み雛形2通を固定形にでき、利用者裁定（核共有＋薄い包み）と一致。推奨 |
| C 汎用文書生成基盤 | template engineの導入や全類型（自由文含む）対応を最初から作る | 外部依存追加・範囲肥大・自由文の対象固定が未定型のまま設計が膨らむ。不採用 |

## 5. 範囲

### 5.1 範囲内

1. **類型登録形と雛形生成**：2類型（`contract_review`・`completion_review`）の雛形をcode内定数として
   固定し、`assemble`が草稿を生成する。機械欄＝表題・依頼元／先・レビュー種別・対象と固定（digest表）・
   開始時鮮度検査・判定の形式・手順・命名。LLM記入欄＝反証点・判断済み／範囲外・事実の明示
   （`<<記入:...>>`形式のplaceholderで生成）。
2. **digest表の自動計算**：対象path一覧（引数）から`tools/common/digests.py`流用で機械計算する。
   手書きdigestを受け付けない。
3. **機械検査入口（`check`）**：完成した依頼recordへ次を決定的に検査し、不合格は停止理由つきで止める。
   1. 依頼recordの存在・UTF-8・commit済み（`git ls-files`）・`git check-ignore`不一致なし
   2. 必須節の存在（対象と固定／鮮度検査／反証点／判定の形式／判断済み・範囲外／手順）と
      反証点識別子の一意・placeholder残存なし
   3. digest表の参照fileの実在・commit済み・記載digestと実digestの全件一致
   4. 依頼元／先・レビュー種別・読み取り専用（書込みなし）の明記
   5. 類型と起動方式の整合（headless対象なら契約010の許可model一覧内のmodel名・`-request-`命名）
   6. 囲み記号（コードfence）の開閉対応
   7. **機微検査**：既定5 pattern＋高乱雑性検知を内容全体へ適用（§7.3の除外3形式つき）。検知は停止
4. **命名整合**：生成名が`-request-`を含み、契約010の導出関数で判定record名が導出可能である。
5. **導線配備**：単体入口（`pyproject` scripts `reviewcompass3-request-builder`）、G30操作登録
   （`_OPERATIONS`へ`request_builder_check`1 entry・check形式）、`docs/development/prompts/`のrun入口、
   `AGENTS.md` §1への入口1行。
6. **対象試験（RED先行）**と実運用E2E 1回（§9-8）。

### 5.2 範囲外

- 自由文類型（後続の類型追加として登録形へ足す）。
- 依頼内容（反証点の文案・判断済みの選定）の自動生成（LLMの意味作業のまま）。
- `review_plan`出力からの対象一覧の自動変換（本契約は対象path一覧を引数で受ける。変換は後続）。
- 5段手続きの残り（監査・判定の多周自動化＝縦C）、判定record側・起動側（契約010成果）の変更。
- 既存4製品の機微検査の包みの統合（利用者裁定：不要）。
- 歴史的record・既存依頼recordの書き換え。

## 6. 固定再利用部品と保護基準

保護基準commitは本候補の固定commitとする。次を変更しない：`tools/session_logs/redaction.py`・
`tools/common/digests.py`・`tools/reviewer_launch/`4 file・`tools/external_review/send.py`・
egress 7 module・受入済み製品群とその試験。`tools/operations/operation_contract_run.py`は
`_OPERATIONS`への1 entry追加だけを行う。

流用の型（利用者裁定の転記）：

> コアを共有し薄いラッパーでの対応は、適切な対応。リファクタリングは不要と判断する

（2026-08-17 chat）。本契約は核＝`redaction.default_pattern_rules`／`find_high_entropy`・
`digests.file_sha256`・`reviewer_launch.record.verdict_record_relative_path`（公開関数）を流用し、
自前の薄い包み（検査の対象選定・停止理由・除外定数）だけを新設する。既存4製品の包みは変更しない。

## 7. 中心的な取り決め

### 7.1 雛形の固定形

- 雛形は**code内定数**として契約固定する（設定file・環境変数・引数から変更できない。変更は契約改定）。
  template file案は、編集経路が契約管理外になるため不採用。
- 必須節の構成は実測済み雛形基準2通（§3）の節構造を正とする：対象と固定（digest表）／開始時鮮度検査／
  反証点（識別子つき）／判定の形式（verdict5語彙・未検査明示・model名記載）／判断済み・範囲外／手順。
- LLM記入欄は`<<記入:`で始まるplaceholderとして生成し、`check`はplaceholder残存を
  `placeholder_remaining`で停止する。

### 7.2 機械検査の写像

pilot-specific §5.1.1の7項目を依頼record構造へ写像した§5.1-3の検査を、**2類型共通の1入口**で行う
（種別ごとに検査処理を複製しない）。各不合格は固有の停止理由（`request_record_uncommitted`・
`required_section_missing`・`digest_mismatch`・`sensitive_data_remaining`等）で止め、自動修正・
自動切り詰めを行わない。

### 7.3 機微検査の固定

- 既定5 pattern（変更不可）と高乱雑性検知を、完成した依頼record内容の全体へ適用する。
- 高乱雑性検知の除外は**契約009 v2 §7と同値の3形式（X1a：40桁小文字hex・X1b：64桁小文字hex・
  X2：可読連結名）だけ**を、本契約の**自前の直書き定数**として宣言する（由来を契約009へ明記。
  `send.py`の私的定数はimportしない）。**同値性は試験で固定**し（§9-5）、乖離が検出された場合は
  停止してHumanへ諮る（勝手にどちらかへ合わせない）。
- 検知時は組み立てを合格にせず停止する。除外の追加・変更は契約改定とする。

### 7.4 残余risk（明示的に受容を諮る）

1. 機械検査は**形式の守り**であり、依頼内容の質（反証点の的確さ）は従来どおりLLMと独立確認の守りに
   残る（機械化目標の分担線どおり）。
2. 除外3形式の自前定数は、契約009側の将来改定で乖離しうる。緩和：同値性試験（§9-5）が乖離を検出し
   停止する。
3. 雛形は実測2通に基づくため、将来の類型追加・構造変更で契約改定が必要になる。緩和：類型登録形が
   追加を局所化する。

## 8. 変更上限

1. 新規：`tools/request_builder/`（類型定数・`assemble`・`check`・入口）。
2. 新規：`tests/`の対象試験（`test_request_builder*.py`）。
3. `pyproject.toml`の`[project.scripts]`へ1行追加。
4. `tools/operations/operation_contract_run.py`の`_OPERATIONS`へ1 entry追加。
5. 新規：`docs/development/prompts/request-builder-run.md`。`AGENTS.md` §1へ入口1行。
6. Evidence、独立確認、受入判断、TODO更新。

## 9. 受入条件

実装開始後は失敗試験を先に固定し、期待どおり失敗してから最小実装を行う。

1. RED：雛形生成（2類型・必須節・placeholder）・digest表計算・機械検査7項目の各停止理由・
   機微検査（検知停止と除外通過）・命名整合・placeholder残存停止の失敗試験を先に固定する。
2. 雛形生成：2類型の草稿が必須節と機械欄を完備して生成され、LLM記入欄が`<<記入:`placeholderで
   明示される。
3. digest表：対象一覧から機械計算され、手書き値を受け付けない。
4. 機械検査：§5.1-3の7検査それぞれについて、成立（合格）と不成立（固有の停止理由で停止）の両向き
   試験が緑になる。
5. 機微検査：既定5 pattern・乱雑列の検知が停止し、40／64桁hexと可読連結名が除外で通過する。
   **除外3形式の自前定数が契約009定数と同値であることを試験で固定する。**
6. 命名整合：生成名から契約010の導出関数で判定record名が導出でき、`-request-`を含む。
7. 導線：単体入口が別の現在位置から実行でき、G30操作として登録実行でき、prompts入口と`AGENTS.md` §1の
   1行が存在する。
8. 実運用E2E 1回：**本契約自身の完了レビュー依頼recordを本toolで組み立て**、`check`合格・commitの後、
   利用者の明示指示の下で契約010のアダプタから起動してレビュー一往復を完走する（縦Aの出力が縦Bの
   入力になる接続の実証。起動は契約010の承認境界に従う）。
9. 既存試験：対象試験、G30 e2e、正規全試験（禁止認証隔離条件）が各単独終了コード0。§6保護対象が
   基準commitから差分0。
10. 独立確認（正式経路：agy headless起動）：誤合格・未接続・禁止作用・上位目的への悪影響0件。
11. 利用者が§7.4残余riskを確認して製品処理を受け入れる。

## 10. 停止条件

- 7項目の写像が実測雛形基準2通の構造と両立せず、雛形基準側の変更が必要になる。
- 除外3形式の同値性が固定できない（契約009定数との乖離が解消できない）。
- §6保護対象の変更が必要になる。
- 対象・関連・正規全試験または独立確認が不合格になる。

## 11. 影響、未実施、次作業

【判断】受入後は、依頼record作成の手作業が「反証点の文案と判断済みの選定を記入するだけ」へ縮み、
形式事故（digest誤り・節欠落・機微混入・命名不整合）が起動前に機械で止まる。成果はheadless起動・
手動fallback・将来のAPI経路のすべてで同じに効く（設計方針メモの原則どおり、共通化は接点と規約の層）。
縦C（品質gate・合議）と自由文類型は本契約の登録形の上に載る。

【未実施】契約採用、実装、E2E、既存成果物の変更。

次は本候補の固定commit後、自己レビュー（5段手続き第1・2段）→依頼record作成→機械点検→独立確認
（正式経路：agy headless起動。起動は利用者の明示指示による）→採用判断の順で進める。
