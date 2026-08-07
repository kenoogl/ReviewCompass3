# TODO_NEXT_SESSION

更新日：2026-08-07

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 5AのContract version 2 Review経路はaccepted artifactまで完了した。以降の開発はHumanの指示によりClaudeが継続する。
- 現在作業：評価②提案を**v2へ改稿し固定した**（Human指摘2件の反映：テスト修正の3分類＝挙動吸収は禁止・機械的参照替えはalias優先で条件付き・重複整理は範囲外、テスト重複は実測後に観測→改善候補→トリアージの既存経路でissue化）。定義（判断材料5点・決定者Human）、対象6系統（ほぼ全てが守り役codeに触れるため系統ごとの反証レビューhigh必須）、手順8段、挙動不変の原則。Human判断待ち（§7判断点4件）。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`：`registered / nonblocking`、影響：参照Digest driftの恒久検査器が無い。in_progressにはしていない、次：着手はHuman判断。判別規則の承認が実装の前提
- レビューbacklog課題（ID：`ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001`、`registered / nonblocking`）：守り役codeへの後追い独立レビュー未実施。in_progressにはしていない、次：着手はHuman判断（Work 4B台帳の後が合理的）。材料：[トリアージメモ](records/development/2026-08-07-unreviewed-work-review-triage-memo-v1.md)、[下流影響の参考情報](records/development/2026-08-07-unreviewed-work-review-downstream-impact-note-v1.md)。新設の`reuse_search_record.py`も守り役として対象に含める
- TODO検証の単一入口課題（ID：`ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`、`registered / nonblocking`）：TODO検証が二tool分離で片方だけ実行しても検出されない。terminal終了コードのpipe隠蔽も対象。次：着手はHuman判断

## 最新のauthority／Evidence

- [評価②提案v2（Human判断待ち）](docs/design/2026-08-08-consolidation-evaluation2-proposal-v2.md) — SHA-256 `967dd4cae74a0229a90a61df29ceff9c3f91aa6bd2a2be434da9f401196cbfe8`
- [経緯と結論Decision（A2中止・統合へ）](records/development/2026-08-08-egress-method-conclusion-decision-v1.md) — SHA-256 `d9228be3ec17db82fbed694e7a6bf05b8a5d6fae52ff2353aad39aeac27dc6fc`
- [「名前が契約」裁定・100%一致record](records/development/2026-08-08-egress-name-contract-adjudication-v1.md) — SHA-256 `bba8c1ac8840940d4e834242e8ebb7f1dc1292a77c70ebbc1d1f5fcfd262df70`
- [A1'再判定・方式比較record](records/development/2026-08-08-egress-a1prime-comparison-v1.md) — SHA-256 `18aff58ee76c1c299185d729cb3a022647e575edeca767ad2dd90f860da0f666`
- [B結果・基準Decision](records/development/2026-08-08-egress-b-check-decision-v1.md) — SHA-256 `40530e41f407a231d3e1cc96bf7c9fdeac49208e30fc25cde78846b1a61ba917`
- [A1判定record（59組）](records/development/2026-08-08-egress-a1-subagent-judgment-v1.md) — SHA-256 `2f8dda0d443666a2512bca5207bd0573f5667b190507224413420e8032ba8ef3`
- [反証レビュー結果（出口関門）](records/development/2026-08-07-egress-adversarial-review-v1.md) — SHA-256 `b0a3ad899bd2f3ef6d010a572e5cad7f3d48a9ea5a82638ba40f109efa87d09a`
- [段階1 GREEN Evidence](records/development/2026-08-07-egress-stage1-green-evidence-v1.md) — SHA-256 `ba75438bb22815783b6f5a52cae9f842b1672a5816fa8d52feb678664fb5f081`
- [出口の設計提案v4（確認済み）](docs/design/2026-08-07-external-egress-gate-proposal-v4.md) — SHA-256 `3a82b3973f8abc947782c4bbf8e2d54713043e8e8591a543089a5824c57bcacd`
- [判断点8件のHuman判断Decision](records/development/2026-08-07-egress-gate-v3-judgments-decision-v1.md) — SHA-256 `7f7741eeb840307af115a23d525abafd1ac3e509ff7d3191ab2c798f40abc08a`
- [ローカル事前分類 実験Evidence](records/development/2026-08-07-local-prefilter-experiment-evidence-v1.md) — SHA-256 `8376d0c53b32beb17bac39f98fabbafc51f629eeaf658f84d76115583942846b`
- [LLMGP外部レビュー資産の調査結果record](records/development/2026-08-07-llmgp-external-review-assets-investigation-v1.md) — SHA-256 `4acf974e09f6818241b17347aca1271a4bd54cf9d4436125178c44ce39d6e3a8`
- [LLMGP外部レビュー資産の観測](records/development/2026-08-07-llmgp-external-review-assets-observation-v1.json) — SHA-256 `872c4736b33f4c314e1fc3bd22ffb52ce8be5de6b0dcfaca3b9841921ae6bc07`
- [伏字化規則の不在 観測](records/development/2026-08-07-redaction-rules-absent-observation-v1.json) — SHA-256 `c77d4c385a7ac8b4cb52128acfd19e51da8655df2e8e9f70033aa36c27f88673`
- [機密関連の実施順序 Decision](records/development/2026-08-07-confidentiality-work-order-decision-v1.md) — SHA-256 `ca5c4a89adb6ab2807887bb7834c4778f4e8658a697deb9f64617893dd67de09`
- [伏字化規則 GREEN Evidence](records/development/2026-08-07-redaction-environment-rules-green-evidence-v1.md) — SHA-256 `9dae5c2df9d39be08a63e22f47936fb27336d42c9032d8b5442bca8d7df68f85`
- [出口の設計提案v2（要書き直し）](docs/design/2026-08-07-external-egress-gate-proposal-v2.md) — SHA-256 `aba30fb90ce95b044921979a0a8654c4113ebf88e2ff35b08a9a6a1477e5a295`
- [層3 GREEN Evidence](records/development/2026-08-07-verification-boundary-layer3-green-evidence-v1.md) — SHA-256 `4ed47b951ee9ccb8b28389a53ba91414cdf0d38f2eb9d4f3fb383118fc833722`
- [層2 GREEN Evidence](records/development/2026-08-07-verification-boundary-layer2-green-evidence-v1.md) — SHA-256 `dc8a83595c67077460793eb435e8aa65b38623a237ea2d905310a7ed364f18cf`
- [層1 GREEN Evidence](records/development/2026-08-07-verification-boundary-layer1-green-evidence-v1.md) — SHA-256 `baff96b87dd17f52da622f9d984b8836a3cb22922044c987a15ac9c56af71c65`
- [検証境界の設計提案（承認済み）](docs/design/2026-08-07-verification-boundary-proposal.md) — SHA-256 `f904e995003f30d9b7bf92555ac390649b4b084f232d9bc50fac341af6a4f4cb`
- [反証レビュー結果（新module 4件）](records/development/2026-08-07-adversarial-review-batch1-new-modules-v1.md) — SHA-256 `2558dd841712d24596ba79513b4e16da6edc0c236ca18d1537d660b72d6df94c`
- [反証レビュー結果（routing・Intake）](records/development/2026-08-07-adversarial-review-batch1-legacy-systems-v1.md) — SHA-256 `b6221cfbf2c1d8b220e0a0fe7087218551bbfed96303b777f3b461a9bcf0900d`
- [I-4処置 GREEN Evidence](records/development/2026-08-07-adversarial-remedy-i4-green-evidence-v1.md) — SHA-256 `fad332129fc7c2cbc84f7cacc1788ff1178ab9a3913e01fc3a461a4297fb7ec1`
- [構成C GREEN Evidence](records/development/2026-08-07-work4b-c-externalization-green-evidence-v1.md) — SHA-256 `a6ee5742a9bc9174db60304a9d6d7767a6ecc9d7159f276336896d33815543b4`
- [universe v2結果・診断訂正Evidence](records/development/2026-08-07-universe-v2-outcome-evidence-v1.md) — SHA-256 `0a06cb014652efedbd1c52139d9448c6a31506cad02eab8ad93a8b9f1100b7c8`
- [構成D 初回実運用Evidence](records/development/2026-08-07-work4b-d-ledger-first-operation-evidence-v1.md) — SHA-256 `f416a360bd9cd09f2646db4f5089fc0805624e26e44c6b8bffeb2b56297628a0`
- [構成A-2 GREEN Evidence](records/development/2026-08-07-work4b-a2-candidate-ranking-green-evidence-v1.md) — SHA-256 `7ce86a44e5ef270875135ce8d9c82017152db82302d76e29db750a5cb2bd96eb`
- [実順位表v1](records/development/2026-08-07-candidate-ranking-v1.json) — SHA-256 `7b02535390547f169b1643f2314979ca9bc5dfb7df8e59a9a99a942f3c09cfee`
- [構成B GREEN Evidence](records/development/2026-08-07-work4b-b-reuse-search-freshness-green-evidence-v1.md) — SHA-256 `cbf5a22317c8aa622a3bdd462ee521f93ba0ab5e662df57135c0287114de9877`
- [構成A-1 GREEN Evidence](records/development/2026-08-07-work4b-a1-integration-exclusions-green-evidence-v1.md) — SHA-256 `91910e837710140a43e0b060832b3726a1b11a5348a7ee4b59cc95b19467a153`
- [統合除外宣言record](.reviewcompass/workflow/integration-exclusions/integration-exclusions-001--v1.json) — SHA-256 `f482bf3d6200e1c2a4fc17233d4e87ed098f04d053dc1fa56e69e481a4b090fd`
- [設計束 承認Decision](records/development/2026-08-07-work4b-main-design-bundle-approval-decision-v1.md) — SHA-256 `6bbaea795f7280f006dce2834b0286bb7df0b1cdb05b12918d2ce7574c27bf5e`
- [設計束提案（承認済み）](docs/design/2026-08-07-work-4b-main-design-bundle-proposal.md) — SHA-256 `14c629d2f45a1dd36cbb3ed60b311ead2898c1e07fe71ffc8e5d2c6365234b5b`
- [設計議論の証跡Decision](records/development/2026-08-07-work5b-discussion-outcomes-decision-v1.md) — SHA-256 `8cfc4a1581ed53513d97f70fa78323f6dc574eb2555bbd35ed78c7a4e1214a9d`
- [Work 5B検査器 GREEN Evidence](records/development/2026-08-07-work5b-checker-green-evidence-v1.md) — SHA-256 `020db589b586e6db741e0d5d347d31c30c89a077c390ebd2232c42dfccbb7d2c`
- [作業レビュー手順書（高risk観点追記後）](docs/development/work-review-protocol.md) — SHA-256 `37c0391a322a6841421742125fff646600aff7d3acd905990c605f614d2e2967`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `a325a20814ad63131486570a94118b4d665dda88b952cd6fb8af476aec073942`

## 次に行う一作業

Humanによる評価②提案v2の承認判断（§7判断点4件：定義、手順8段、挙動不変の原則、着手順A→B→C…）。承認後は系統A（SHA-256計算、7file）の照合・実測・統合案提示から着手する。

開始条件：

- Humanの着手指示

完了条件：

- Human判断（§7の4件）が記録されること

後続作業：段階3（承認record形式の正式schema化。反証I-6の真正性担保を含む）→評価②（文脈依存の統合可否）の定義→実施順序の2番目以降（規則の登録、C・Dの定義、既存データの扱い）。送信の実装（段階4）と場面2は別提案。

## blocker・Human判断待ち

- blocker：なし。登録済み課題の着手、V1凍結レーンの解除、テストの一斉整理、Work 8前倒しは行わない。Codex側の指示書にある作業はHumanの指示により扱わない。
- Human判断待ち：評価②提案v2の承認（§7判断点4件）。
- 継続する留意点：背景調査の不足が累計5件、さらに本調査で6件目の未遂があった（配備先コピーを最新と誤認し、開発元の存在をHuman指摘で知った）。規律を三段で持つ：(1)提案前に既存機構の確認・前提の実測・用途の列挙 (2)確認の範囲は「記録が指す先」まで (3)**指された物が写しなら原本（開発元）まで遡り、鮮度（最終commit日）を確認してから状態を断定する**。

## stale・deferred

- stale：なし。
- deferred：Work 6AのCL-6A-04/05/06/07/11（行き先明記済み）、backlog以外の登録済み課題の着手、Current Work Projection正式写像、Work 7、Work 8、UI、automation。

## Git・Test

- branch：`main`
- commit境界：本handoffを含むcommit完了時点
- Git状態：HEAD、upstream、ahead／behind、push状態はGitから機械取得する
- worktree：本handoffを含むcommit完了時点でclean
- 直近の関連Test：egress計65 passed（dry-run 4件を含む）
- 直近の全Test：venv pytest 1205 passed、Python 3.9.6、pytest 8.4.2、fallback false
- 差分検査：`git diff --check`合格

## 更新規則

- 現在位置、active Issue、最新Evidence、次の一作業だけを置き換える。
- 詳細履歴と手戻り候補はdurable Candidate／Issue／Evidenceへ保存し、TODOへ累積しない。
- 完了済み作業単位が未コミットなら次作業へ進まない。
