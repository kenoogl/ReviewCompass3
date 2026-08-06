# レビュー未対応作業の全量とトリアージ v1

- 状態：triage材料（不変。以後の訂正は後継versionで行い、本fileを書き換えない）
- 作成日：2026-08-07
- 判定基準：`docs/development/work-review-protocol.md`（`DEC-WORK-REVIEW-PROTOCOL-HIGH-RISK-001`による
  追記後、SHA-256 `22856c9836de2fd1a5d3a8a79d9437ea82150c8e167fb9ddc40ac6b82bb0a923`）
- 関連Decision：`DEC-WORK-REVIEW-PROTOCOL-HIGH-RISK-001`
  （`records/development/2026-08-07-work-review-protocol-high-risk-additions-decision-v1.md`）

## 1. 目的と方法

これまでの開発で「作業後の独立レビュー」（独立監査、Challenge、独立検証。作った本人の流れとは別に、
成果物を疑う側から検査して結果を記録に残す活動）が実施されていない作業を全量書き出し、
work-review-protocol.mdの基準でトリアージする。レビューは文書とcodeの両面から考える。

方法【実測】：(1) `records/development/`のRED／GREEN Evidence・receiptの作業単位名を正規化して列挙、
(2) チェックリスト本文とのfile名照合、(3) git全履歴736 commit（2026-07-27〜2026-08-07）の日付・件名走査、
(4) `tools/`配下の現存module数の集計。作業単位の同定は命名規約に依存するheuristicであり、
網羅の完全性は保証しない。

「独立レビュー実施済み」と数えるのは、独立監査（Work 3の各候補）、Plan Challenge v1〜v4、
Definition／Final Challenge（Work 5A）、Codex独立再確認（Work 5A）、被覆主張の独立検証（Work 6A
CL-6A-09）である【記録】。テスト（RED→GREEN）、書込み後の自己Digest照合、Human承認は
レビューに数えない（work-review-protocol §2-1「完了報告はClaimでありEvidenceではない」）。

## 2. 判定基準（work-review-protocol §3の写し）

- **既定`high`**：守り役のcode（validator、Digest照合、承認関門の判定、改竄拒否など、他の成果物の
  合否を決めるcode。失敗が「誤った合格」として黙って現れる）、および不可逆操作を行うcode（移行、
  削除、上書き、外部送信）。
- `high`のレビューには§4.4「実行者のfixtureに無い反証を最低1件新作して機械で試す」、
  §5「期待挙動を上流から独立導出する」を適用する。
- 先例【記録】：機械操作routing v2は全テスト合格後に「execution receiptの改竄を拒否できない」欠陥が
  発見され訂正を要した（`DEC-MACHINE-OPERATION-ROUTING-RECEIPT-INTEGRITY-001`）。守り役のcodeの
  盲点はテストでは検出できないことの実例である。

## 3. A群：チェックリスト以前（2026-07-27〜28、416 commit、stage 0〜5）

git履歴【実測】：全736 commitのうち416件（56%）がこの2日に集中し、ほぼ全件が
「Add red tests → 実装」のTDD対で構成される。現行チェックリストはこれらをWork 1の前身Evidenceとして
一括参照するのみで、個別作業単位は載っていない。

- **文書面**：commit列に設計・要件のreview記録が存在する（例：`dd237e0` "Record independent
  requirement review"、`17690cd` "Record stage five design review findings"）【実測】。さらに現行の
  Intent・用語集・RequirementsはWork 2〜3で再固定と監査を経ている【記録】。旧文書の未レビュー残riskは
  **低**（現行authorityが代替済み）。
- **code面**：stage期のcodeは現存し、現在も`tools/`配下にある【実測】：
  `tools/session_logs/` 39 module、`tools/extraction/` 23、`tools/bootstrap/` 17、
  `tools/requirements/` 7、`tools/task_contract/` 5、`tools/design/` 2、`tools/layout/` 1。
  独立レビュー記録はない。うち`tools/session_logs/`は秘匿情報の伏字化・高entropy検出
  （fail-closed、守り役）と、原本保存・lock・schedule登録（外部副作用）の両方を含む → **high**。
  `tools/task_contract/execution.py`は意図毀損検出（守り役）を含む → **high**。
  その他は用途を個別確認のうえ判定する（本メモでは未判定）。

## 4. B群：チェックリスト期（2026-08-03〜08-07）の未レビュー作業

「文書面」は当該作業の候補・Evidence文書への独立レビュー有無、「code面」は実装moduleへの
独立レビュー有無。riskはcode面の判定。

| # | 作業 | 主なcode | 文書面 | code面risk | 根拠 |
| --- | --- | --- | --- | --- | --- |
| 1 | Work 1（固定入力） | なし（記録のみ） | 自己再照合のみ | — | 文書はHuman承認・後続stale検査済み |
| 2 | Work 1A（Layout v1/v2/v3） | `tools/layout/` | Human承認のみ | 中 | fixture検証中心、生成物はGit管理下で復元可能 |
| 3 | Work 1B（Session Log Bootstrap） | `tools/development/session_log_bootstrap.py` | Human承認のみ | **高** | 非authority入力の拒否・第二正本検出（守り役）を含む |
| 4 | Work 2（Intent・用語集） | なし（記録のみ） | 自己点検のみ（誤り1件検出実績） | — | 現行authorityはWork 3で監査済み |
| 5 | Session transcript保全 | `tools/session_logs/`の一部 | Human承認のみ | **高** | 伏字化・秘匿検出（守り役）＋raw保存（副作用） |
| 6 | Project Manifest v2／Deployment境界 | manifest検証系 | Human承認のみ | 中 | 検証は読み取り、境界はTestで固定 |
| 7 | Issue解決Pilot実装（WI-001〜007） | `issue_resolution_pilot.py`、`todo_compaction.py`、`issue_resolution_state.py`、`todo_snapshot.py` | Plan文書はChallenge済み | **高** | 候補〜Challenge検証器（守り役）、restore上書き（不可逆） |
| 8 | Issue Intake V4実装 | `issue_intake_v4.py` | Human承認のみ | **高** | Issue登録・重複判定・昇格の検証器（守り役） |
| 9 | 機械操作routing v2 | `operation_routing.py` | Human承認のみ | **高** | 権限preflight・receipt改竄拒否（守り役）。欠陥実績1件 |
| 10 | Commit／handoff安定化 | `todo_handoff.py`、`work_unit_transition.py` | Human承認のみ | **高** | handoff検査・移行関門（守り役） |
| 11 | Development venv baseline | `bootstrap_environment.py`、`policy_test_runner.py` | Human承認のみ | **高**（runner）／中 | 公式Test receiptの生成（守り役に準ずる） |
| 12 | Work 4A実装 | `work4a_rebuild_v3.py` | 設計はHuman承認 | 中 | new-only生成・再生成可能・読み取り観測 |
| 13 | 意図毀損検出（CL-6A-10） | `tools/task_contract/execution.py` | 設計提案はHuman承認 | **高** | Contract適合成果の拒否判定（守り役） |
| 14 | 書庫Layout v3移行 | 移行tool | 承認Decisionあり | **高**→緩和 | 不可逆（移行）。byte一致12検査・旧書庫保持で残riskは低い |

## 5. C群：チェックリスト外の差し込みTDD（B群と重複しないもの）

| # | 作業単位 | 主なcode | code面risk | 根拠 |
| --- | --- | --- | --- | --- |
| 1 | read-only argv executor | `structured_argv_executor.py` | **高** | 機械操作の実行経路（権限判定の下流） |
| 2 | task Python cache＋AST境界 | `task_python_cache.py`、`python_ast_boundary_check.py` | 中 | cacheはevictable、AST検査は読み取り |
| 3 | 定型record生成＋境界修復 | `todo_record_generation.py`、`pytest_summary.py` | **高** | handoffのTest件数正本を生成（誤記＝誤った完了根拠） |
| 4 | Task Contract source固定 | source pin検証系 | **高** | 固定source一致の判定（守り役） |
| 5 | TODOテスト投影CLI | `todo_handoff_projection.py` | 低 | 表示のみ |
| 6 | TODO更新の書き込み境界 | `todo_update_path.py` | 中 | 書込み先の限定（守り役に準ずるが範囲小） |
| 7 | V4永続化2件（Issue／仕分け） | `issue_intake_v4.py`内 | **高** | B群8と同一moduleで扱う |
| 8 | Intake V4単体候補＋宣言→RED対応表 | 同上 | **高** | 同上 |
| 9 | チェックリスト参照Digest修復 | 一回限りの修復 | 低 | 機械検証済みの単発修復。恒久検査は`ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`の範囲 |
| 10 | Codexセッション再取得 | `tools/session_logs/`利用 | 中 | A群のsession_logs判定に従属 |
| 11 | Work 4A v1撤去・v2巻き戻し | revert map（履歴） | 低 | 完了済みの履歴操作、現行codeに残存なし |

## 6. トリアージ集計と対処候補

**`high`（守り役code。§4.4の反証新作レビューの後追い適用候補）**、優先度順の案：

1. `operation_routing.py`＋`structured_argv_executor.py` — 欠陥実績が既にある系統
2. `issue_intake_v4.py`、`issue_resolution_pilot.py` — Issue・候補・Decisionの合否を決める検証器
3. `todo_handoff.py`、`todo_record_generation.py`＋`pytest_summary.py`、`work_unit_transition.py`、
   `policy_test_runner.py` — handoff・移行・公式Test receiptの関門
4. `tools/development/session_log_bootstrap.py`、`tools/task_contract/execution.py` — 非authority拒否と
   意図毀損拒否の判定
5. `tools/session_logs/`の伏字化・秘匿検出系 — A群で唯一の即`high`。module数が多く、対象の絞り込み
   （守り役部分の特定）自体を最初の作業単位とする
6. `todo_compaction.py`のrestore経路、Task Contract source pin検証 — 上書き復元と固定source判定

**`high`だが緩和済み**：書庫Layout v3移行（byte一致12検査・旧書庫保持・冪等確認済み【記録】）。
後追いレビューの優先度は下げてよい。

**中以下**：一斉レビューは行わない。通常の変更時に、work-review-protocol.mdの該当riskで確認する。

**文書面**：独立監査・Challengeの経路はWork 3以降機能しており、新設は不要。未レビューはWork 1〜2期の
文書に限られ、現行authorityへの再固定で代替済みのため後追い不要。チェックリスト本文の陳腐化は
`IC-CHECKLIST-APPROVAL-SCOPE-STATEMENT-DRIFT-001`で別途登録済み。

**行わないこと**（`DEC-WORK-REVIEW-PROTOCOL-HIGH-RISK-001`の非承認事項と整合）：全codeの一斉再レビュー、
過去の完了済み作業単位の完了取り消し、変異検査の前倒し（Work 8割当てを維持）、テストの一斉整理。

## 7. 本メモの限界

- 作業単位の抽出は命名規約に依存するheuristicであり、規約外の作業は漏れうる。
- A群のstage期module（session_logs以外）の守り役該当の有無は未判定であり、着手時に個別確認を要する。
- 「主なcode」欄のmodule対応は代表であり、網羅ではない。
- 本メモは対処の実施を承認しない。優先度案を含めてHuman裁定の材料である。
