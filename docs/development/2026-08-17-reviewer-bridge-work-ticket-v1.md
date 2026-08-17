# reviewer接続adapter 作業票 v1（範囲固定・データ取得順序3）

- 作成日：2026-08-17
- 指示者：利用者（Human）。選択文言「続けて順序3（reviewer接続）に着手。範囲固定文書から
  進めて」（2026-08-17 chat）
- 作成者：Claude
- 種別：範囲固定文書（軽量作業票）。**承認までは着手しない**
- 上位計画：評価データ取得計画v1 §4順序3。固定入力＝事前走査record
  `records/development/2026-08-17-reviewer-bridge-prescan-v1.md`

## 1. 目的

Task Contract実行経路のdeterministic stub reviewerに対し、**LLM reviewer（正式起動経路）への
接続adapter**を用意する。論文実験（順序4のpaired trial）でLLMレビューを実行するための前提部品
であり、本作業では**外部起動を伴わない範囲**（組み立て・変換・試験＝起動はfake）までを作る。

## 2. 正本範囲（成果物）

1. **adapter新設**：`tools/evaluation/reviewer_bridge.py`——
   - (a) Task Contract chainの文脈（contract・context_manifest）から`free_text`類型の依頼record
     本文を**機械組み立て**する部品（`request_builder`のassemble→機械記入→check合格まで。
     正式経路の部品を読み取り専用で呼ぶ）。
   - (b) 判定recordのfindingsを`finding_set`形式へ変換する部品（変換表§4）。
   - (c) launch呼び出しの包み（実行はinjectable——試験ではfake、実起動は順序4の承認後）。
2. **試験**：RED先行。組み立て（check合格まで）・変換・fake起動の一往復を検証。既存試験群
   （task_contract・reviewer_launch・request_builder・G30）は無変更維持。
3. **起動なしの保証**：本作業の試験・実装は外部プロセス起動（agy等）を一切行わない（fakeのみ）。

## 3. 方式の確定（Human確認点）

- **案A（正式経路の機械駆動）を採用**：依頼record→check→launch→判定recordの正式経路を
  adapterが機械駆動する。安全境界（認証遮断・読み取り専用・fail-closed）とProvenance
  （依頼・判定recordの残存）を迂回しない。**実験の完全な追跡可能性はH5の主張材料を兼ねる**。
- 案B（`reviewer_launch`下層の直接利用）は安全境界の再構成＝迂回となるため不採用。
- **バッチ起動承認の形（本票で確定を諮る）**：実起動を伴う実験（順序4）では、
  「実験計画record（ケース一覧・条件・起動回数上限・費用見積り）の**事前承認**をもって、
  バッチ内の個別起動をClaudeの実行へ委任する」。契約010 §2の起動承認境界の実験適用形であり、
  計画外の起動・上限超過は停止して再承認。**本作業（順序3）では実起動しない**ため、この形の
  適用は順序4の実験計画承認時。

## 4. finding変換表（固定）

| 判定record findings | finding_set（stub互換） |
| --- | --- |
| `identifier` | `finding_id`（`F-LLM-`接頭＋連番で一意化） |
| `severity`（error／warning／info） | `severity`（同語彙・無変換。**`blocking: true`はseverityがinfoでも`error`へ格上げ**——適合性検査の「errorで停止」に接続） |
| `evidence_path`・`evidence_location` | `target_ref.relative_path`＋`description`内へ位置を保存（`sha256`は対象materialのbundle値を引く。引けない場合は`target_ref`を省略せず`unresolved`を明示） |
| `claim` | `description` |
| （対応なし） | `requirement_ref`・`rule_id`＝`llm_review`固定（stubのrule系と区別） |

## 5. 受入条件

1. 正式再利用検索の証明書（`start_allowed: true`）。
2. RED：adapter試験が実装前に失敗（単独終了コード非0）。
3. GREEN：新設試験＋保護対象（task_contract系・reviewer_launch 68・request_builder 40・
   G30 75）の全通過（単独終了コード0）。
4. fake一往復の実証：組み立て→check合格→fake起動→変換→`evaluate_conformance`通過までを
   試験で固定（外部起動ゼロの機械確認を含む）。
5. `git diff --check`・意味単位commit・`work_unit_transition`合格。

## 6. 着手後の手続き（承認後の順序）

1. 作業別計画（schema 2・能力2件：依頼組み立て駆動・finding変換）→先行commit。
2. 正式再利用検索→証明書固定。
3. RED→失敗確認→commit。
4. GREEN→全緑→commit。
5. 完了報告（受入条件の対応付け）。

## 7. 範囲外

- 実起動を伴う実験・実験計画record・バッチ承認の行使（順序4）。
- `execution.py`・`reviewer_launch`・`request_builder`本体の変更。
- ケース材料の作成・正解Finding固定（順序4）。
