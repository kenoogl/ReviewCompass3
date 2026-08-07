# TODO_NEXT_SESSION

更新日：2026-08-07

> 人向けの現在位置入口。Workflow stateと完了Evidenceの正本ではない。

## 現在位置

- 全体：Work 1B、Work 2、Work 3、Issue Resolution早期Pilot、開発venv baseline、Project-first Runtime Layout v3、Work 4A再利用探索baselineが完了。Work 5AのContract version 2 Review経路はaccepted artifactまで完了した。以降の開発はHumanの指示によりClaudeが継続する。
- 現在作業：**digest系（A+C合流）の材料一式を固定し、手順4のHuman判断待ち**。11関数（9file）とも除外・凍結非該当、守り役8/11。A本体2行×7・C本体7行×4とも逐語同一。呼び出し47か所、テスト直接参照はCの公開2名のみ→**alias維持で既存テスト無修正**。効果：約−17行・digest定義11→2・canonical仕様の単一化（守り役中核仕様の保証改善）。**実施を推す所見**。追加観測：テスト側canonical自前定義12file（_sha256系14fileと同型。issue拡張はトリアージ判断）。
- Task Contract：`none`

## 現在作業に影響する改善候補／Issue

- `ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`：`registered / nonblocking`、影響：参照Digest driftの恒久検査器が無い。in_progressにはしていない、次：着手はHuman判断。判別規則の承認が実装の前提
- レビューbacklog課題（ID：`ISSUE-UNREVIEWED-WORK-REVIEW-BACKLOG-001`、`registered / nonblocking`）：守り役codeへの後追い独立レビュー未実施。in_progressにはしていない、次：着手はHuman判断（Work 4B台帳の後が合理的）。材料：[トリアージメモ](records/development/2026-08-07-unreviewed-work-review-triage-memo-v1.md)、[下流影響の参考情報](records/development/2026-08-07-unreviewed-work-review-downstream-impact-note-v1.md)。新設の`reuse_search_record.py`も守り役として対象に含める
- TODO検証の単一入口課題（ID：`ISSUE-TODO-HANDOFF-VERIFICATION-GAP-001`、`registered / nonblocking`）：TODO検証が二tool分離で片方だけ実行しても検出されない。terminal終了コードのpipe隠蔽も対象。次：着手はHuman判断
- テストfixture重複課題（ID：`ISSUE-TEST-SHA256-FIXTURE-DUPLICATION-001`、`registered / nonblocking`）：テスト14fileが同型の_sha256補助関数を自前定義。正規経路（OBS→IC→pilot v3検証→tool組立decision→issue）で登録済み。着手はHuman判断

## 最新のauthority／Evidence

- [digest系（A+C）統合判断の材料](records/development/2026-08-08-consolidation-digest-family-materials-v1.md) — SHA-256 `ea1ec1ab55a8c8073932497338cbfa6588c52a430d3d278f07905d887279592d`
- [系統A 統合判断の材料](records/development/2026-08-08-consolidation-family-a-materials-v1.md) — SHA-256 `502f8f643989664afb734752e18432e93dd8b91da7705dd4cc480480ec86df3a`
- [評価②提案v2 承認Decision](records/development/2026-08-08-consolidation-eval2-approval-decision-v1.md) — SHA-256 `2726c4f435f3fb31e22b7f5468a627a2b615ee4da7bb02c28bf9ce4b0854f173`
- [評価②提案v2（承認済み）](docs/design/2026-08-08-consolidation-evaluation2-proposal-v2.md) — SHA-256 `967dd4cae74a0229a90a61df29ceff9c3f91aa6bd2a2be434da9f401196cbfe8`
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
- [統合除外宣言record](.reviewcompass/workflow/integration-exclusions/integration-exclusions-001--v1.json) — SHA-256 `f482bf3d6200e1c2a4fc17233d4e87ed098f04d053dc1fa56e69e481a4b090fd`
- [設計束 承認Decision](records/development/2026-08-07-work4b-main-design-bundle-approval-decision-v1.md) — SHA-256 `6bbaea795f7280f006dce2834b0286bb7df0b1cdb05b12918d2ce7574c27bf5e`
- [設計束提案（承認済み）](docs/design/2026-08-07-work-4b-main-design-bundle-proposal.md) — SHA-256 `14c629d2f45a1dd36cbb3ed60b311ead2898c1e07fe71ffc8e5d2c6365234b5b`
- [設計議論の証跡Decision](records/development/2026-08-07-work5b-discussion-outcomes-decision-v1.md) — SHA-256 `8cfc4a1581ed53513d97f70fa78323f6dc574eb2555bbd35ed78c7a4e1214a9d`
- [Work 5B検査器 GREEN Evidence](records/development/2026-08-07-work5b-checker-green-evidence-v1.md) — SHA-256 `020db589b586e6db741e0d5d347d31c30c89a077c390ebd2232c42dfccbb7d2c`
- [作業レビュー手順書（高risk観点追記後）](docs/development/work-review-protocol.md) — SHA-256 `37c0391a322a6841421742125fff646600aff7d3acd905990c605f614d2e2967`
- [Initial Development Checklist](docs/development/2026-08-03-initial-development-checklist.md) — SHA-256 `99a84b333b8842c59c37230e58fd9f495e87dfdf1f19e22e5a5b4df1e329871d`

## 次に行う一作業

系統A+C合流の「digest系」材料を作る：C系統4関数（canonical digest計算。4file全て守り役）の実測（本体・呼び出し・テスト参照）を加え、共通module一括の統合案・削減行数・alias要否を提示して手順4の再判断に付す。issue登録のやり直し・AGENTS.md整理（139→78行）・checklist改定r1（Work 4B追随[x]2件、評価②の対応明記、Work 1B後続に機密レーン残3項を新設、Digest8件一致確認。Human承認済み）は完了。

開始条件：

- Humanの着手指示

完了条件：

- digest系材料が手順4のHuman判断に付されること

後続作業：段階3（承認record形式の正式schema化。反証I-6の真正性担保を含む）→評価②（文脈依存の統合可否）の定義→実施順序の2番目以降（規則の登録、C・Dの定義、既存データの扱い）。送信の実装（段階4）と場面2は別提案。

## blocker・Human判断待ち

- blocker：なし。登録済み課題の着手、V1凍結レーンの解除、テストの一斉整理、Work 8前倒しは行わない。Codex側の指示書にある作業はHumanの指示により扱わない。
- Human判断待ち：digest系の手順4判断（実施可否・moduleの置き場と命名）。
- 継続する留意点：(1)提案前に既存機構の確認・前提の実測・用途の列挙 (2)確認は「記録が指す先」まで、写しなら原本まで (3)**登録済み課題2件が実害として発現した**：pipe隠蔽で不合格コミットが2回通過（`;`連結が原因。コミット前の全test確認は独立コマンドで行う）、TODO byte上限超過をCLI検証が見逃しテストだけが検出（二tool分離）。workflow台帳へのrecord追加は必ず正規toolを通す（手作りJSONは台帳整合テストに落ちる）。

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
