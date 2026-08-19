# WSSE 5頁版 英文骨子 v2（Related Work節の追加）

- 記録日：2026-08-19
- 記録者：Claude（執筆スレッド）
- 根拠：利用者文言「関連研究をコンサイスに入れる必要がある」（2026-08-19 chat）
- v1からの差分：**独立節「Related Work」（約0.4頁）を§5として新設**し、頁配分を再調整。
  v1の§0〜§4の要旨・数値束縛表（v1 §7）は不変（本書は差分のみを載せる）
- v1：`docs/paper/2026-08-19-wsse-skeleton-v1.md`
  （SHA-256 `4071a7e1fccdcbf01af610034d8134ab45844b2476304cfc24878b304b42a2bb`）

## 1. 改訂後の節構成と頁配分（合計5.0頁）

| 節 | v1配分 | **v2配分** | 調整 |
| --- | --- | --- | --- |
| 1 Introduction | 0.75 | 0.75 | 不変 |
| 2 Task Contracts | 1.0 | **0.9** | 図の説明文を圧縮 |
| 3 Evaluation I: RQ1 | 0.75 | **0.7** | 検出経路の内訳をTable 1脚注へ |
| 4 Evaluation II: RQ2 | 1.5 | **1.4** | ケース列挙を1文へ圧縮 |
| **5 Related Work（新設）** | — | **0.4** | 1段落構成 |
| 6 Discussion and Conclusion | 0.75 | **0.6** | 従軸1文と締め文を統合 |
| References | 0.25 | 0.25 | 10〜12件 |

位置は**評価の後・考察の前**（§5）。序論P2〜P3で問題と提案は動機づけ済みのため、先に挟んで
流れを重くしない。評価を見た読者に「個別要素は既存・新規性は統合的導出」の位置づけを短く
示してから考察へ入る（構想§9の整理と一致）。

## 2. §5 Related Work の英文要旨（1段落・約190語）

> **Related Work.** Each ingredient of our approach exists in prior work. LLM-based code
> review has been studied empirically, with attention to detection performance and false
> positives; these studies largely fix the review input — a diff, a file, or the full
> context — rather than deriving it from a task-specific responsibility. Retrieval-augmented
> generation and context engineering select inputs by relevance, but similarity-based
> selection drifts as the corpus grows, precisely the regime our RQ2 probes, whereas
> contracts select by declared obligation, deterministically. Design by Contract introduced
> machine-checkable responsibilities for program units; we lift the idea from program units
> to review tasks and compile contracts into execution, verification, and provenance plans.
> Requirements traceability links requirements to artifacts; our binding tables and sealed
> records mechanize this link and check it before execution. Agent harnesses orchestrate LLM
> tool use; here the harness configuration itself is derived from the contract. Our
> methodology borrows defect seeding from classic inspection experiments and preregistration
> from empirical software engineering. The novelty we claim is not any single ingredient but
> the integrated derivation: one machine-interpretable contract as the control plane
> connecting requirements, context assembly, execution, verification, and provenance.

日本語注記：6領域（LLMレビュー実証・RAG／文脈工学・Design by Contract・要求追跡・agent
harness・実験方法論）を各1〜2文で対比し、締めに「新規性は統合的導出」（構想§9の確定整理）。
各文が**本文のどこと対応するか**が明確：RAG文→RQ2、DbC文→§2、追跡文→§2封印record、
方法論文→§4設計。

## 3. 引用の当て込み（文献特定は起草時・計10〜12件）

| Related Workの文 | 引用予定 | 件数 |
| --- | --- | --- |
| LLMコードレビューの実証研究 | 代表的実証1〜2件（検出性能・誤検出を測る系） | 1〜2 |
| RAG／context engineering | RAGの代表1件＋文脈選択の survey か手法1件 | 1〜2 |
| Design by Contract | Meyer | 1 |
| Requirements traceability | 代表survey 1件 | 1 |
| Agent harness | LLM agent／tool useの代表1件 | 1 |
| 欠陥注入（inspection実験） | Basili系1件 | 1 |
| 事前登録（実証SE方法論） | registered reports系1件 | 1 |
| （§1・§2から）仕様駆動開発・vibe codingの言及 | 実務文献または位置づけ論文1〜2件 | 1〜2 |

## 4. 未実施・確認点（v1 §8を更新）

1. v1 §8-1のまま：「主張しないこと」5点→4点への圧縮の確認。
2. 本v2（Related Work追加・頁再配分）の確認。
3. 全文起草（共通部品＝Table 1・2・Figure 1から）。文献の特定と整形。LaTeX様式の確認。
