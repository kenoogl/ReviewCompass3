# WSSE 5頁版 英文骨子 v1（全節の要旨）

- 記録日：2026-08-19
- 記録者：Claude（執筆スレッド）
- 根拠：利用者文言「用語の読みはそれでよい。この構成で5頁版の英文骨子（全節の要旨）を先に
  見せて」（2026-08-19 chat）
- 入力：動機record v1（`2026-08-19-wsse-introduction-motivation-v1.md`）・執筆計画v2 §2.1・
  確定データ（RQ2＝dataset v1／final metrics v1、RQ1＝初回計測Evidence、従軸＝dataset v7）
- 性格：**骨子**（各節の中核主張を論文調の英文で固定）。全文起草の前段。数値は確定recordから
  転記済み（起草時に再照合する）
- 匿名化：repository名・利用者名は書かない。対象は "an in-development software project" と表現

## 0. Title and Abstract (draft)

**Title**: Task Contracts for Evidence-Bounded LLM Code Review: A Requirements-to-Runtime Approach

**Abstract (draft, ~170 words)**:

> LLM-based coding agents have made specification-driven development practical, but each
> phase adds documents, and the growing corpus inflates review inputs and the human burden of
> adjudicating review findings. We propose Task Contracts: machine-interpretable responsibility
> contracts placed between structured requirements and review execution. A deterministic
> compiler maps each contract's obligations to six executable plan views (context acquisition,
> review execution, harness configuration, verification, provenance capture, and human
> interaction), and the runtime assembles review inputs only from materials the contract names.
> We evaluate two research questions on an in-development software project that applies the
> approach to its own reviews. RQ1 (contract completeness): pre-execution checks detected all
> nine seeded omission, conflict, and staleness defects in contract fixtures with no false
> stops, and compilation was byte-identical across repeated runs. RQ2 (context scalability):
> in a preregistered paired trial with 27 review executions, adding 114 KB of irrelevant
> documents left contract-guided material selection unchanged in all ten cases and input
> tokens within 5%, while a baseline grew 4.0x and its on-subject rate fell from 1.000 to
> 0.286. We release the scoring vocabulary, sealed answer keys, and machine-checkable records.

日本語注記：主題は確定済みの文言。要旨は「動機1文→提案2文→RQ1の結果1文→RQ2の結果2文→
公開物1文」。数値は確定値のみ（114 KB＝113,976 byteの丸め。起草時に表記を統一）。

## 1. Introduction（0.75頁・動機record §4の4段落）

**P1 (capability shift)**:
> LLM-based coding agents now complete substantial programming tasks. "Vibe coding" —
> instructing an agent informally and accepting what it produces — works for small programs,
> but breaks down at practical scale, where teams instead adopt specification-driven
> development: requirements, design, decomposition, and implementation, each phase reviewed
> before the next.

**P2 (the new problem)**:
> Specification-driven development has a side effect. As phases progress, project documents
> multiply, and two costs grow with them: the effort of managing the documents, and the human
> burden of adjudicating review results. LLM-based review inherits a third cost: without an
> explicit boundary, the input to each review grows with the repository, and the reviewer
> increasingly reports findings that are correct but irrelevant to the task at hand. In our
> measurements, adding unrelated documents to a review directory quadrupled baseline input
> tokens and dropped the share of on-subject findings from 1.000 to 0.286.

**P3 (proposal)**:
> To mitigate this, we introduce Task Contracts: machine-interpretable responsibility
> contracts placed between structured requirements and review execution. A deterministic
> compiler derives executable plans — which materials to read, what to verify before and
> after execution, what provenance to record, and where human approval is required — so that
> review inputs are bounded by the contract rather than by the repository. The approach is
> implemented and used in production by the project under study for its own document reviews.

**P4 (RQs, contributions, non-claims)**:
> We ask two questions. RQ1, contract completeness: can compilation detect missing, conflicting,
> or stale contract elements before execution? RQ2, context scalability: does contract-guided
> context selection keep review inputs and finding quality stable as irrelevant repository
> material grows? Our contributions are (1) a Task Contract model connecting requirements to
> LLM review execution, (2) a deterministic compiler mapping obligations to execution,
> verification, and provenance plans, and (3) a preregistered paired pilot demonstrating input
> stability and evidence retention under repository growth. We do not claim a large-scale
> validated general runtime, superiority over human review, correctness of the requirements
> themselves, or statistical significance at pilot scale.

日本語注記：P2の第3のコスト（入力の無限定な成長）で動機とRQ2を接続。P4末尾の
「主張しないこと」は確定5点の圧縮（RC3全体の完成は対象systemの匿名化に伴い削り、4点に）。
→**確定5点のうち「RC3全体の完成を主張しない」の扱いだけ利用者確認**。

## 2. Task Contracts（1.0頁・図1枚）

**要旨**:
> A Task Contract declares, in machine-checkable form, a review task's responsibility, its
> boundary (target paths), preconditions, context obligations, expected output, acceptance
> criteria, and provenance obligations. Each contract binds to a fixed table of sixteen
> requirement obligations; binding failures are typed errors, not warnings. Contracts are
> validated twice: a definition challenge checks the contract itself (with human approval
> recorded as a first-class artifact), and a compile gate checks obligation coverage before
> any execution. The compiler is deterministic: from one contract it derives six plan views —
> context acquisition, review execution, harness configuration, verification, provenance
> capture, and human interaction — and sealed records carry content digests so that any
> post-hoc modification is machine-detectable. At runtime, the context manifest admits only
> materials named by the contract (implicit materials are rejected), the review request is
> assembled mechanically from the manifest, and the reviewer runs as a read-only headless
> process whose verdict is transcribed and committed with four post-checks (freshness, single
> record commit, evidence, schema form).

**Figure 1**: Contract → compiler → six plan views → runtime (manifest → request → read-only
review → verdict) の一枚図。

日本語注記：九つ組の全欄挙列は避け、契約→決定的コンパイル→実行時の入力束縛、の3点に圧縮。
詳細設計はarXiv版参照の1文を末尾に置く。

## 3. Evaluation I: Contract Completeness (RQ1)（0.75頁・表1枚）

**要旨**:
> We validate the compilation apparatus on twelve contract fixtures in four groups: three
> well-formed, three with missing elements, three with conflicting obligations, and three
> stale (tampered bindings or rewritten definitions). Table 1 reports five metrics.
> Requirement-to-obligation coverage and obligation-to-plan coverage are both 1.0; compiling
> the same input three times yields byte-identical sealed records (regeneration match 1.0);
> all nine negative fixtures are caught before execution (detection 1.0) — five stopped by
> typed errors at binding or compile time, four flagged as blocking by coverage or digest
> checks; and none of the three well-formed fixtures is falsely stopped (false-stop rate 0.0).
> We position this as validation of the apparatus on an initial fixture set rather than a
> claim about defect distributions in the wild.

**Table 1**: 5指標（coverage 2種・regeneration match・negative detection・false stop）×値。

日本語注記：「装置の実証」という位置づけを本文に明記（裁定どおり）。検出経路の内訳
（bind段停止・compile段blocking・seal照合・再束縛比較）は1文で圧縮。

## 4. Evaluation II: Context Scalability (RQ2)（1.5頁・表1〜2枚＋小図1）

**要旨（設計）**:
> We ran a preregistered paired trial on ten review cases drawn from the host project's own
> documents: three reconstructed real defects (a contract table contradicting observed record
> shapes; a digest transcribed with a one-character error; a procedure retaining superseded
> behavior), four seeded defects following classic defect-injection practice (an omission, a
> factual error, an inconsistency, an ambiguity), and three clean documents. The primary
> comparison is B (contract-guided selection) versus C (identical cases with ten irrelevant
> documents, 114 KB, placed in the same directories); a baseline that reads whole directories
> (A1 without, A2 with the irrelevant pool) and a missing-material condition (D) serve as
> secondary probes. The answer key was sealed by SHA-256 before any launch and verified
> unchanged afterwards; a mechanical check extracts every file the reviewer actually opened,
> flagging out-of-scope reads. The reviewer model, prompts, and budgets were fixed across
> conditions; 30 launches yielded 27 successful executions (1.53M tokens).

**要旨（結果）**:
> Contract-guided selection was invariant: in all ten cases, condition C selected exactly the
> materials of condition B, and mean input tokens moved from 30,016 to 31,526 (+5.0%). The
> baseline grew from 31,112 to 125,194 tokens (4.0x). Per-case detection was 0.889 under both
> B and C, against 0.667 for the baseline. Findings were adjudicated under a seven-way
> vocabulary (detected; latent defect in materials; false positive; request gap; off-subject;
> out of scope; non-counted): of 44 findings, only one was a false positive. What degraded
> under document growth was not correctness but focus — the baseline's on-subject rate fell
> from 1.000 to 0.286 as it began reporting genuine but off-subject inconsistencies inside
> the added pool, while the contract path held (0.667 to 0.769). First-pass scoring with a
> coarse four-way vocabulary had counted six false positives per condition; adjudication
> reclassified nearly all as genuine findings of other kinds, indicating that coarse scoring
> vocabularies understate reviewer performance.

**Table 2**: 条件別（B・C・A1・A2・D）×（cases, detection, on-subject rate, false positives,
input tokens, materials selected）。
**小図または表3**: B→C と A1→A2 の入力トークン対比（ケース別または平均）。

日本語注記：事前登録・汚染検査・単一model固定を設計段落で明示（査読耐性）。採点の
「第一次→確定」の差は方法論の知見として結果段落の最後に置く。

## 5. Discussion and Conclusion（0.75頁）

**要旨**:
> Three observations stand out. First, the reviewer's weakness was not being wrong — false
> positives were nearly zero — but talking about the wrong things when given unbounded input;
> context selection is therefore the right control point. Second, omissions are harder than
> contradictions: the one seeded deletion of an acceptance criterion went undetected under
> every condition, suggesting that completeness must be guaranteed mechanically (as RQ1's
> coverage checks do) rather than delegated to review. Third, the experiment doubled as a
> field test: review runs surfaced four real defects in the host project's own operational
> documents, including an exit-code vocabulary inconsistency whose root cause was found by
> tracing a reviewer finding into the implementation. In production use, 93.9% of each review
> request is derived mechanically from the contract, human approval is confined to 51 recorded
> decision points, and 95.9% of digest bindings remain machine-traceable. Limitations: a
> ten-case pilot on one project's documents with a single reviewer model; no comparison with
> human review; no claim of statistical significance. We plan fixture expansion, multi-model
> replication, and code-diff review targets. Task Contracts turn LLM review from an
> open-ended conversation over a growing corpus into a bounded, auditable execution.

日本語注記：発見3件＋従軸1文＋限界＋今後＋締めの1文。従軸の数字（93.9%・51・95.9%）は
dataset v7から。締め文は中心命題の言い換え。

## 6. References（0.25頁・最小構成の当て込み）

最小8〜12件の想定：Design by Contract（Meyer）・Requirements Traceability・LLM code review
（実証研究1〜2）・RAG/context engineering（1〜2）・agent/harness（1）・provenance（W3C PROV）・
preregistration（実証SEの方法論1）・defect seeding（Basili系1）。**文献の特定と整形は次段の
執筆作業**（計画v1台帳#8）。

## 7. 数値の出所（起草時に再照合する束縛表）

| 数値 | 出所record |
| --- | --- |
| RQ2主結果（30,016／31,526／31,112／125,194／0.889／0.667／1.000→0.286／0.667→0.769／44指摘中誤検出1） | `records/development/2026-08-18-rq2-final-metrics-v1.json`・裁定record v2 §2 |
| 実行規模（30起動・27成功・1,528,433トークン・113,976 byte） | RQ2実行Evidence v1 §1・事前登録record §4 |
| 封緘照合一致 | RQ2実行Evidence v1 §0・事前登録record §2 |
| RQ1 5指標・fixture 12件・検出経路 | RQ1初回計測Evidence §2 |
| 従軸（93.9%・51 record・95.9%・真の不一致13） | dataset v7（追補v2 §2） |

## 8. 未実施・確認点

1. **P4の「主張しないこと」**：確定5点のうち「RC3全体の完成を主張しない」は匿名化に伴い
   4点へ圧縮した。この扱いの確認。
2. 全文起草（共通部品＝Table 1・2・Figure 1から）。文献の特定（§6）。
3. LaTeX様式（WSSE指定template）の確認と設定。
