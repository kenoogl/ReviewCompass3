# 論文執筆計画 v1（章立て案＋データ台帳）

- 起草日：2026-08-18
- 指示者：利用者（Human）。選択文言「論文執筆に着手。章立て案と、書ける範囲・足りないデータの
  一覧から」（2026-08-18 chat）
- 起草者：Claude
- 位置づけ：論文執筆系列の最初の文書。**章立てとデータの対応を固定する計画**であり、原稿では
  ない。`docs/paper/`はこの系列の置き場として本文書で新設した
- 目標：**2026-08-30**までの最小論文（評価データ取得計画v1 §1）

## 0. 固定入力（確定済み事項の出所）

| 確定事項 | 出所 | SHA-256 |
| --- | --- | --- |
| 主題「Task Contracts for Evidence-Bounded LLM Code Review: A Requirements-to-Runtime Approach」・RQ1／RQ2・貢献3点・主張しない5点 | 利用者確定（2026-08-17 chat）→`docs/development/2026-08-17-evaluation-data-acquisition-plan-v1.md` §1 | `c666bdd7d0b5c44a8fbb876238a19c1d05ee245e693a2b104ceee514cdad55cb` |
| 構想の正本（九つ組・統合導出・H1〜H7・指標8領域・Positioning） | `docs/design/2026-08-17-task-contract-architecture-import-v1.md` | `d49062602b7965eb64416d22b26bdcd81e0f685775a3c728a5aed52d81e44577` |
| 構想の検討経緯 | `docs/design/2026-08-17-task-contract-discussion-import-v1.md` | `6e3c8395d71b7cec7a59b4834b3d6d04312e7d28e65e5cdd9f168f3193e13de2` |
| RQ1初回計測（5指標） | `records/development/2026-08-17-rq1-apparatus-first-measurement-evidence-v1.md` | `647fdb9c44fceb3dc70fa97e8ef89510461dae2a6611218a13ce5fac30c194f9` |
| RQ2実行Evidence（§11確定集計を含む） | `records/development/2026-08-17-rq2-paired-trial-evidence-v1.md` | `c6dbfa836866524b41edcd156e24b7cd39cec615110a0a9c1c793713a8b5522f` |
| RQ2裁定・議論・副産物（7語彙・主題適中率・判別基準） | `records/development/2026-08-18-rq2-adjudication-and-byproducts-v2.md` | `f4191636ea1ee701b3fbc29f42a24e0860afd3c81633a5bb543215777134a152` |
| RQ2生データ（31実行） | `records/development/2026-08-18-rq2-paired-trial-dataset-v1.json` | `d34ecd24a8d87c49e5b50f4ae204295841622ea12c34886e29dba5a32c85b893` |
| RQ2最終指標JSON | `records/development/2026-08-18-rq2-final-metrics-v1.json` | `5476c4c1b5db7a2c802aee69f44c5c821a5b5c4d448f5c15de2ee6b1ded27bda` |
| 復元可能性表（従軸の復元可否） | `records/development/2026-08-17-evaluation-recoverability-map-v1.md` | `d2668b6720b9578fd89382d943c1ec72225a6b781e20776455c8fd01f46f93d3` |

## 1. 章立て案（8章構成・フルペーパー想定）

分量の想定は10〜12頁（2段組）。ワークショップ（4〜6頁）へ縮める場合の短縮方針を各章に併記する。

### §1 Introduction

- 問題：LLMコードレビューは、repositoryが成長するほど「何を読ませるか」が制御不能になる。
  入力が膨らみ、**正しいが的外れな指摘**が主題を埋める（実測の導入：ベースラインは無関係資料で
  入力約4.0倍・主題適中率1.000→0.286）。
- 中心命題：機械解釈可能な責務契約（Task Contract）を要求と実行の間に置き、何を根拠に・どの
  範囲で・どの条件まで実行し・何を証拠に残すかを一貫制御する。
- 貢献3点（確定済み文言のまま）：(1) RequirementsとLLMレビュー実行を接続するTask Contract
  モデル、(2) obligationを実行・検証・Provenance計画へ写像する決定的compiler、(3) 無関係な
  repository成長に対する入力安定性とEvidence保持のpaired pilot。
- 主張しない5点を早期に明示（大規模実証済み汎用Runtime／人間レビュー超え／Requirements自体の
  正しさ保証／RC3全体の完成／少数ケースでの統計的優位）。
- 短縮時：そのまま（削らない）。

### §2 Motivating Example

- RC3の実運用から1ケース（case-001＝契約の表と観測の実物形の矛盾）を導入例に、
  「同じ依頼で、周囲の資料が10 file・113KB増えたとき何が起きるか」をB／C／A1／A2の4通りで見せる。
- 短縮時：§1へ吸収（図1枚に圧縮）。

### §3 Task Contract Model

- 九つ組（responsibility・boundary・preconditions・context_obligations・expected_output・
  acceptance・provenance_obligations等）と、16要求への義務束縛表（`REQUIREMENT_OBLIGATIONS`）。
- 二層検証（definition_challenge＝Contract自体の検査＋Human approval）。
- 実装の実在：`tools/task_contract/`（RC3で実運用）。
- 短縮時：九つ組の表と束縛の考え方だけ残す。

### §4 Deterministic Compilation

- Contract→6 Plan views（context_acquisition・review_execution・harness_and_capability・
  verification・provenance_capture・human_interaction）。
- compile gate（実行前検査）とsealed record（content_digest封）。決定性は再生成一致率で実証
  （RQ1指標）。
- 短縮時：図1枚＋RQ1の表へ委ねる。

### §5 Evidence-Bounded Review Runtime

- context manifest（明示材料のみ・暗黙資料拒否）→依頼recordの機械組み立て（assemble→check）→
  読み取り専用headless起動（安全境界・認証遮断・単独commit・事後照合4点）→finding変換。
- 実運用の来歴：E2E 7試行の訂正連鎖（実測記録がある）。
- 短縮時：安全境界の詳細を落とし、経路図1枚へ。

### §6 Evaluation

- **RQ1（Contract completeness）**：fixture 12件（正常3・欠落3・競合3・stale 3）で5指標——
  requirement被覆1.0・plan被覆1.0・再生成一致率1.0（byte一致×3回）・negative検出率1.0（9件
  全件が実行前検査で停止またはblocking）・誤停止率0.0。
- **RQ2（Context scalability）**：paired trial 27成功実行（起動30回・1.53Mトークン）。
  - 主結果：材料選択10ケース全件不変・入力+5.0%対約4.0倍・検出率0.889対0.667・
    主題適中率0.667→0.769対1.000→0.286。
  - 方法論：**事前登録**（正解表SHA-256封緘→実験後照合一致）・範囲外読取りの機械検査・
    採点7語彙と主題適中率・第一次採点と確定採点の差（採点者裁量幅の開示）。
- 脅威と限界（§7と分担）：単一model・10ケースpilot・材料は自プロジェクト文書・採点はClaude
  起草＋Human裁定。
- 短縮時：RQ2の表2枚（条件別指標・B→Cのケース別）とRQ1の表1枚まで圧縮。

### §7 Discussion

- 発見1：**誤検出はほぼゼロ（44指摘中1件）**。LLMレビューの弱点は「間違うこと」ではなく
  「何について語るかを制御できないこと」——文脈選択の設計が効く理由。
- 発見2：**脱落（omission）は矛盾より見つかりにくい**（case-004は4条件全て未検出）。受入条件の
  欠落は機械側の被覆検査（RQ1装置の型）で担保すべき類型。
- 発見3：採点語彙が粗いと性能を過小評価する（誤検出6→0〜1）。判別基準「依頼が渡したものだけを
  読んだとき、その指摘を避けられたか」。
- 発見4：実験が対象system自身の欠陥を4件検出（副産物）。指摘を起点に実装を追うと設計の根に届く
  ——人と機械の分担の実例。
- 短縮時：発見1・2だけ残す。

### §8 Related Work・§9 Conclusion

- 関連領域：Design by Contract・Requirements Traceability・RAG／context engineering・
  LLMコードレビュー・agent harness・provenance（W3C PROV系）・pre-registration。
  個別概念は既存であり、新規性は統合的導出関係にあると明確化（構想§9の整理どおり）。
- 短縮時：Related Workを1〜1.5段へ。

## 2. 書ける範囲の台帳（データ→章の対応）

| データ | 章 | 状態 |
| --- | --- | --- |
| RQ1の5指標＋fixture 12件の検出経路表 | §6 | **確定record化済み**。ただし§4.1参照（fixture初版に対する健全性確認という位置づけ） |
| RQ2の主結果（不変性・トークン・検出率・主題適中率） | §1・§2・§6 | **確定record化済み**（機械集計・生データから再計算可能） |
| 事前登録の封緘と照合一致 | §6方法論 | 済（SHA-256一致の機械照合record） |
| 範囲外読取りの機械検査（1件検出・検査して残置） | §6方法論 | 済 |
| 採点7語彙・主題適中率・判別基準・採点者裁量幅 | §6・§7 | 済（第一次と確定の両方が残っている） |
| 九つ組・16要求束縛・6 Plan views・二層検証・sealed record | §3・§4 | 実装実在（`tools/task_contract/`・試験群） |
| 正式経路（assemble→check→launch→事後照合）とE2E 7試行の訂正連鎖 | §5 | record化済み |
| 副産物4件の検出→改善候補→仕分け→対処の一周 | §7 | record化済み（2026-08-18） |
| 実験コスト（30起動・input 1,209,837／output 318,596・1レビュー約80秒の実測例） | §6 | 済（rawから機械抽出） |

## 3. 足りないデータの台帳

| # | 欠落 | 効く章 | 入手方法 | 無くても書けるか |
| --- | --- | --- | --- | --- |
| 1 | H4（依頼組み立ての所要時間分布・手動記入箇所数・自動導出率） | §5の実用性補強 | 順序5（運用集計コマンド）。launch.jsonの時間メタは順序1以降の起動分に存在 | **書ける**（§5は経路の記述と安全境界で成立） |
| 2 | H5（digest束縛の追跡可能率・受入判断の束縛表被覆） | §7の監査性補強 | 順序5。既存recordの機械集計 | **書ける**（定性記述＋束縛表の実例1枚で代替可） |
| 3 | H7（承認点の分布・問い合わせ数） | §7のHuman協調 | 順序5。chat承認文言→Decision record系列から復元 | **書ける**（承認境界の設計記述で代替可） |
| 4 | 全体コスト（セッションログからの道具呼び出し数・時間） | §6コスト欄 | 順序5。保全済みログ（契約014で構造化可能） | **書ける**（実験コストは既にある） |
| 5 | RQ1のfixture拡充後の本計測（初回12件は健全性確認の位置づけ） | §6 RQ1 | fixture類型の追加＋再計測（小規模） | **条件付きで書ける**（「装置の実証＋初回計測」として正直に位置づければ可。査読耐性を上げるなら拡充が望ましい） |
| 6 | H1／H3の直接対照（Contract無しの「通常のタスク記述」比較） | §6 | 追加実験（A条件が部分代替。完全な対照は依頼文の統制設計が要る） | **書ける**（主張しない5点と整合。RQ2のA条件を「粗いベースライン」と明示） |
| 7 | H6（状態変化後のContext Manifest再構築） | 主張外 | 追加実験 | **書ける**（本論文のRQ外。future workへ） |
| 8 | 関連研究の文献調査（引用リスト） | §8 | **執筆作業の一部**。RC2のsurvey資産（`docs/paper/survey`はRC2側）を参照可能か要確認 | 書けない（§8には必須。ただし執筆と並行で可） |
| 9 | 英文の外部校閲 | 全体 | 利用者判断 | 書ける（品質判断は利用者） |

**要点**：§1〜§7は**今あるデータだけで書ける**。足りないのは§8の文献調査（執筆作業そのもの）
と、あれば厚くなる従軸の数字（#1〜4＝順序5）である。8/30目標に対しては「§1〜§7を先に書き、
順序5は執筆中の待ち時間に回すか、v2へ送る」が成り立つ。

## 4. Human判断待ち（執筆前に決めたい4点・推奨つき）

| # | 判断 | 選択肢 | 推奨 |
| --- | --- | --- | --- |
| 1 | 投稿先・形式 | (a) arXiv先行公開→会議投稿 (b) ワークショップ（4〜6頁） (c) フルペーパー（10〜12頁）直行 | **(a)**。8/30目標と整合し、形式制約なしで全データを収められる。会議選定は後から |
| 2 | 執筆言語 | 英語／日本語 | **英語**（主題が英語で確定済み。文献も英語圏） |
| 3 | RQ1の扱い | 現状（初回12件）のまま正直に書く／fixture拡充して再計測（#5） | **まず現状で書く**。§6に「装置の実証」と明記し、拡充はv2 |
| 4 | 順序5の要否 | 執筆前に実施／執筆と並行／v2へ送る | **執筆と並行**（§3の台帳どおり本文は書ける。数字が出れば§5・§7を厚くする） |

## 5. 執筆の進め方案（8/30まで）

1. 本計画の確認（判断4点）→ §6 Evaluationから書く（データが最も固い章から）。
2. §3〜§5（実装記述——コードとrecordから起こす）→ §1・§2・§7。
3. §8関連研究（文献調査と並行）→ §9・要旨。
4. 原稿は`docs/paper/`配下で版管理（数値はすべてrecordのpath＋digestを脚注または付録で束縛）。

## 6. 未実施

- 判断4点の確定（§4）。原稿の起草。文献調査。順序5の実施判断。
