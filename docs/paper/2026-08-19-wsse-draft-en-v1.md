# WSSE 5頁版 英語初稿 v1（日本語草稿v4の英訳）

- 記録日：2026-08-19
- 記録者：Claude（執筆スレッド）
- 根拠：利用者指示「v4を確認した。v4を原本として英訳に進んでください」（2026-08-19 chat）
- 原本：`docs/paper/2026-08-19-wsse-draft-ja-v4.md`
  （SHA-256 `962f0aa5c1e2a3e8a383af9c9e1e48fc15fc621fb004377574b3fec0087be76b`）
- 用語対応：v4付記の規則を適用——「関係ありそうに見えるが判定には不要な文書（周辺文書）」は
  初出で task-adjacent but non-essential documents と定義し、以後 distractor documents。
  「irrelevant」は不使用。主要対訳は文末付記の表
- 数値：v4から転記（新規数値なし）。転記後にja↔enの数値トークン機械照合を実施
- 構成：v4と同一（要旨＋6節＋図1キャプション＋文献枠10件）。段落見出し（P1〜P4・方法・結果・
  観測1〜3等）もv4と対応

---

## Title

**Keeping LLM Code Reviews Small without Losing Evidence: Task-Contract-Guided Context Selection**

## Abstract

When we hand a review to an LLM, the question is what to let it read. As a project grows, its
documents multiply. What accumulates is not unrelated garbage but task-adjacent, non-essential
documents: documents that look relevant yet are unnecessary for the verdict at hand. Let the
reviewer read them and the input swells while the findings drift off target. We propose the Task
Contract: a machine-readable contract stating what a given review examines, over what scope, and
against what evidence. A compiler derives execution plans from the contract, and at run time the
reviewer receives only the materials the contract names. The same contract always yields the same
plans. We evaluated the approach on a software project under active development that uses it daily
for its own document reviews, asking two questions. First, do broken contracts stop before
execution? They do: all 9 contracts seeded with omissions, contradictions, or stale references
were caught before execution, and no intact contract was falsely stopped. Second, when such
distractor documents accumulate, does the review stay confined to the materials the verdict needs?
It does: in a controlled trial with answer keys sealed in advance (27 review executions), adding
114KB of distractor documents from the same project left the contract-based material selection
unchanged in all 10 cases, and input grew by no more than 5%. The same manipulation inflated the
baseline's input 4.0-fold and dropped the fraction of on-topic findings from 1.000 to 0.286.
Detection rates did not change in either setting. We release the scoring vocabulary, the sealed
answer keys, and machine-verifiable records.

---

## 1. Introduction

**(P1: What has changed)** Coding agents built around LLMs now carry out programming work of
considerable scale. With so-called vibe coding—issuing instructions as they come to mind and
taking whatever comes back—small programs can be made to work. At production scale this breaks
down. Specifications must be written down; development proceeds through phases—requirements,
design, decomposition, implementation—and each phase's artifacts are reviewed before the next
begins. Specification-driven development becomes necessary.

**(P2: The new problem it creates)** Specification-driven development has a cost. Every phase adds
plans, design documents, decision records, and work tickets. As documents accumulate, two burdens
grow together: the effort of managing the documents, and the human effort of deciding which review
findings to accept. Handing the reviews to an LLM adds a third burden: **unless what the reviewer
may read is stated explicitly, the review input grows with the repository**. And as the input
grows, the reviewer produces more findings that are "not wrong, but not what is being asked right
now." Moreover, what creeps in is not obviously unrelated garbage. It is documents from the same
project that look relevant but are unnecessary for the verdict at hand—task-adjacent but
non-essential documents, hereafter *distractor documents*. In our measurements, merely placing
such distractor documents in the directory under review inflated the input of a naive method by
about 4.0× and dropped the fraction of on-topic findings from 1.000 to 0.286.

**(P3: Proposal)** Our response is to sign a small contract for each review: the Task Contract.
The contract states, in machine-readable form, what the review's mandate is, which files are in
scope, what evidence to read, what must hold for acceptance, and what provenance—the record of
where each artifact came from—to leave behind. A compiler derives the execution plans from the
contract: the list of materials to read, the checks before and after execution, the provenance to
record, and the points where human approval is required. The review input is then determined by
the **size of the contract**, not the size of the repository. This machinery is not a research
prototype: the subject project uses it daily for its own document reviews.

**(P4: Questions and contributions)** This paper asks two questions. RQ1: Can broken
contracts—missing elements, contradictions, stale references—be caught by machine before
execution? RQ2: As distractor documents accumulate, do the materials the contract selects and the
quality of the findings remain stable? We contribute three things: (1) the Task Contract model
connecting requirements to LLM review execution, (2) a deterministic compiler that maps contract
obligations onto execution, verification, and provenance plans, and (3) a preregistered controlled
pilot showing input stability and evidence preservation under growing distractor documents. We do
not claim any of the following: a general-purpose runtime validated at scale, superiority over
human review, correctness of the requirements themselves, or statistical significance at pilot
scale.

## 2. Task Contract

**(What goes into a contract)** One contract is written per review. A contract contains the
mandate (what to judge), the scope (paths of the files under review), preconditions, obligations
on the materials to read, expected outcomes, acceptance criteria, and the provenance to leave.
Writing it down is not enough. Each contract is checked against the project's 16-item table of
required obligations, and an obligation that cannot be matched is a **typed error**, not a
warning. Contracts are examined twice. The first examination is of the contract itself (the
definition challenge), where human approval is captured as a formal record. The second is a
compile-time gate that checks, before execution, that no obligation has been dropped.

**(Compilation is deterministic)** The compiler derives 6 plans from one contract: how to gather
materials, how to execute the review, how to configure the execution harness, what to verify, what
provenance to record, and where to interact with a human. Compiling the same contract any number
of times yields byte-identical results (measured in §3). Every generated record is sealed with a
content digest (SHA-256), so tampering after the fact is machine-detectable.

**(What happens at run time)** At run time, the manifest—the list of materials—accepts only the
files the contract names. Anything not named is rejected. The review request document is assembled
mechanically from this manifest, and the reviewer is launched as a read-only process. Verdicts are
transcribed and committed in a structured form, and 4 final checks—freshness, standalone commit,
grounding, and format—run mechanically. Figure 1 shows the overall flow. Design details are
deferred to the extended version (arXiv).

**Figure 1**: From contract to execution. Contract → compiler → 6 plans → run time (manifest →
request assembly → read-only review → verdict transcription → 4 post-checks). Sealed records span
every stage.

## 3. Evaluation I: Do Broken Contracts Stop before Execution? (RQ1)

**(Method)** We exercised the compilation machinery on 12 contract fixtures: 3 intact contracts
and 9 broken ones—3 with elements removed, 3 with contradictory obligations, and 3 with bindings
or definitions rewritten after the fact (staleness). Table 1 reports 5 metrics.

**Table 1: The 5 RQ1 metrics (12 fixtures, first measurement)**

| Metric | Value |
| --- | --- |
| Requirement→obligation coverage (fraction of the 16 items matched to contract obligation fields) | 1.0 |
| Obligation→plan coverage (fraction of obligations mapped into one of the 6 plans) | 1.0 |
| Regeneration identity (same input compiled 3 times, byte-identical) | 1.0 |
| Negative detection rate (9 broken contracts caught before execution) | 1.0 (9/9) |
| False-stop rate (the 3 intact contracts stopped unjustly) | 0.0 (0/3) |

**(Results)** All 9 broken contracts were caught before execution: 5 stopped with binding-time or
compile-time errors, and 4 raised blocking warnings from coverage checks or digest verification.
None of the 3 intact contracts was stopped. This is a **demonstration of the machinery** on an
initial fixture set, not a claim about how defects arise in the wild. We state that plainly.

## 4. Evaluation II: Does the Review Stay Small as Distractor Documents Grow? (RQ2)

**(Design)** We built 10 cases from the subject project's own documents: 3 reproduce defects that
actually occurred (a contract table contradicting observed facts, a digest with a one-character
transcription error, a procedure document with a stale specification left in), 4 carry defects
seeded artificially in the classic way (omission, wrong fact, inconsistency, ambiguity), and 3 are
clean passing documents. The primary comparison is between condition B (the contract selects the
materials) and condition C (the same cases, with 10 distractor documents totaling 114KB placed in
the case directory). The distractors were drawn from real design documents of the same project. We
machine-checked, by full-text search for case-specific terms, that they contain none of the
answers; but they come from the same repository, in the same style and the same vocabulary, and on
reading they look plausibly related. As secondary comparisons we used a baseline that reads the
whole directory (A1 = without distractors, A2 = with distractors) and a condition D in which a
required material was deliberately removed. Answer keys were sealed with SHA-256 before launch and
verified unchanged afterward. We also extracted mechanically which files the reviewer actually
opened, and checked for out-of-scope reads. Reviewer model, prompt, and budget were fixed across
all conditions (one commercial LLM: Gemini 3.1 Pro). Of 30 launches, 27 executions succeeded
(1.53M tokens in total).

**(Result 1: The input did not swell)** The materials the contract selected were **identical in
all 10 cases** before and after the distractor documents were added. Mean input tokens went from
30,016 to 31,526, an increase of just +5.0%. The baseline went from 31,112 to 125,194, a 4.0×
increase. Per-case changes scatter in both directions; the contract side shows no systematic
growth due to distractors.

**(Result 2: Finding quality did not degrade—focus did)** Per-case detection rates were 0.889 for
both B and C, and 0.667 for the baseline. We adjudicated the 44 findings under a 7-way scoring
vocabulary—hit on a seeded defect, real defect present in the materials (non-seeded), false
positive, insufficient information in the request, off-topic but correct, out of mandate, and
minor—and **only 1 finding was a false positive** (a claim about a problem that does not exist in
the materials). The reviewer, in other words, is rarely wrong. What degraded as distractors were
added was not correctness but **focus**. The baseline began reporting inconsistencies that really
exist in the added distractor documents (but have nothing to do with the question at hand), and
its on-topic rate fell from 1.000 to 0.286. That 5 such off-topic findings appeared is itself
evidence that the distractors were "related enough to say something about"—that they had real
power to divert attention. The contract method held at 0.667 to 0.769. One further note: our
initial scoring used a coarse 4-way vocabulary, under which we counted 6 findings per condition as
false positives. Adjudication reclassified nearly all of them as correct findings of another kind.
**A coarse scoring vocabulary makes the reviewer look worse than it is.**

**Table 2: Key metrics by condition (final tally)**

| Condition | Runs | Defect cases | Detection | On-topic rate | False pos. | Mean input tokens | Mean materials |
| --- | --- | --- | --- | --- | --- | --- | --- |
| B (contract, no distractors) | 10 | 9 | 0.889 | 0.667 | 0 | 30,015.6 | 1.2 |
| C (contract, distractors) | 10 | 9 | 0.889 | 0.769 | 1 | 31,526.4 | 1.2 |
| A1 (baseline, no distractors) | 3 | 3 | 0.667 | 1.000 | 0 | 31,112.3 | 1.3 |
| A2 (baseline, distractors) | 3 | 3 | 0.667 | 0.286 | 0 | 125,194.3 | 11.3 |
| D (required material removed) | 1 | 1 | 0.000 | 0.000 | 0 | 27,277.0 | 1.0 |

**(Accompanying observations)** In condition D, with a required material removed, the reviewer did
not assert the seeded contradiction without evidence. It did not, however, report that materials
were missing either. The out-of-scope read check flagged 1 case; on inspection, the reviewer had
gone to look up a record cited by the material's own text and had not reached the answer key, so
the run was kept in the tally.

## 5. Related Work

Taken one at a time, every component of our approach already exists. LLM code review has been
studied empirically, but mostly with the review input held fixed (diff, files, or full context)
while detection performance is measured; deriving the input from the task's mandate is the missing
part. Retrieval-augmented generation (RAG) and context engineering select input by relevance; but
similarity-based selection is weak precisely against documents that look relevant yet are
unnecessary for the verdict—the very kind of document we placed in RQ2. A contract selects
deterministically from declared obligations, not from similarity. Design by Contract gave program
components machine-checkable obligations; we lift that idea from program components to review
tasks, and further compile the contract into execution, verification, and provenance plans.
Requirements traceability links requirements to artifacts; our binding tables and sealed records
mechanize that link and check it before execution. Research on agent harnesses orchestrates LLM
tool use; in our approach the harness configuration is itself derived from the contract.
Methodologically we borrow defect seeding from classic inspection experiments and preregistration
from empirical software engineering. What we claim as new is not any single component. It is the
integration: **one machine-readable contract acting as the control surface that connects
requirements, material selection, execution, verification, and provenance**.

## 6. Discussion and Conclusion

**(Observation 1: What needs fixing is input selection, not model intelligence)** The reviewer's
weakness was not being wrong. Of the 44 findings, exactly 1 was a false positive—a claim about a
problem that does not exist in the materials. Even the 5 off-topic findings the baseline produced
in reaction to the distractors were, in content, all correct: reports of inconsistencies that
really exist in the added documents. The reviewer, then, **speaks correctly about whatever it is
given to read**. What it could not do was tell which of the documents it was handed is "what is
being asked right now." On reflection this is no surprise: the scope of the question is written
nowhere in the input. Failing to discern what is not written down is not a lack of intelligence.
This distinction decides where the remedy belongs. If the degradation were caused by errors of
judgment—false positives—a smarter model would be the fix. But the measured cause was the growth
of findings that are correct yet not what is being asked, and that is something a smarter model
does not fix: the smarter the model, the more faithfully it will report every problem that really
exists in whatever it was given. What is being asked is information that exists only on the
requester's side, and the only place it can be conveyed to the machine is the **selection of the
input**. The contract writes that selection down as a declaration and gives the machine the means
to enforce it.

**(Observation 2: Absence is harder to spot than contradiction)** The defect that removed a single
acceptance criterion went undetected in every condition. Completeness—everything that should be
present is present—is a property to guarantee by machine, as RQ1's coverage checks do, not one to
expect from review.

**(Observation 3: Results as a field trial)** The experiment doubled as a field trial. The review
executions brought to light 4 real defects in the subject project's operational documents. For 1
of them (an inconsistency in an exit-code vocabulary), the reviewer's finding was the lead that
let us trace the implementation down to the root cause. In daily operation, 93.9% of review
requests are generated mechanically from contracts, 95.9% of digest bindings are
machine-traceable, and human approval is confined to 51 recorded decision points. The 51 is not an
impression. The subject project operates under a rule that every human approval must leave a
record quoting the **approval statement verbatim**; 51 is the machine count obtained by a metrics
tool that scans the full set of records and counts those bearing an approval statement. Because
approval always becomes a record, where humans intervened can be counted, and shown, after the
fact.

**(Limitations)** The limitations are equally clear. This is a 10-case pilot on a single project's
documents, with a single reviewer model, no comparison against human review, and no claim of
statistical significance. Moreover, the distractor documents were chosen from candidates far from
each case's topic. The harder setting—distractors very close to the topic, such as older versions
of the same contract or other documents covering the same subsystem—remains untested. Because the
contract names materials by path, selection should in principle remain unchanged there as well,
but the measurement is still to come, and we make it an explicit target of future testing. We also
plan to grow the fixture set, replicate across models, and extend the approach to code diffs.

**(Conclusion)** Our conclusion in one sentence is this. The Task Contract turns LLM review from
an open-ended conversation over an ever-growing corpus into a **small, bounded execution that is
evidence-backed and auditable**. The shift has three effects. First, review input and cost are
decoupled from repository growth and determined by the size of the contract (in this pilot, +5.0%
input against 114KB of distractors)—a direct answer to the third burden of §1, input that grows
with the repository. Second, findings stay on topic (an on-topic rate of 0.769 versus 0.286 under
distractors), which keeps the human burden of deciding which findings to accept from growing with
the documents; human involvement is compressed into a small number of recorded approval points—the
51 above—rather than blanket surveillance of every output. Third, the execution itself leaves
evidence. The same contract yields the same plans, and materials, verdicts, and provenance are
connected by sealed records, so a third party can later verify, from the records alone, why these
materials led to this verdict; and because broken contracts stop before execution, failure
detection moves from post-hoc reading to pre-execution machine checks. To trust a review not on
the impression of a conversation but on records that can be verified—that is where this method
arrives.

## References (identified — 12 entries; \cite wiring into the body happens at LaTeX typesetting)

[1] Z. Li, S. Lu, D. Guo, N. Duan, S. Jannu, G. Jenks, D. Majumder, J. Green, A. Svyatkovskiy,
S. Fu, and N. Sundaresan, "Automating Code Review Activities by Large-Scale Pre-training,"
ESEC/FSE 2022. — `li2022automating`
[2] R. Tufano, S. Masiero, A. Mastropaolo, L. Pascarella, D. Poshyvanyk, and G. Bavota, "Using
Pre-Trained Models to Boost Code Review Automation," ICSE 2022. — `tufano2022using`
[3] P. Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks,"
NeurIPS 2020. — `lewis2020rag`
[4] L. Mei et al., "A Survey of Context Engineering for Large Language Models,"
arXiv:2507.13334, 2025. — `mei2025context`
[5] B. Meyer, "Applying 'Design by Contract'," Computer 25(10), 1992. — `meyer1992contract`
[6] J. Cleland-Huang, O. C. Z. Gotel, J. Huffman Hayes, P. Mäder, and A. Zisman, "Software
Traceability: Trends and Future Directions," FOSE 2014. — `clelandhuang2014traceability`
[7] L. Wang et al., "A Survey on Large Language Model Based Autonomous Agents," Frontiers of
Computer Science 18(6), 2024. — `wang2024agents`
[8] V. R. Basili, S. Green, O. Laitenberger, F. Lanubile, F. Shull, S. Sørumgård, and
M. V. Zelkowitz, "The Empirical Investigation of Perspective-Based Reading," Empirical Software
Engineering 1(2), 1996. — `basili1996pbr`
[9] N. A. Ernst and M. T. Baldassarre, "Registered Reports in Software Engineering," Empirical
Software Engineering, 2023. — `ernst2023registered`
[10] R. Sapkota, K. I. Roumeliotis, and M. Karkee, "Vibe Coding vs. Agentic Coding: Fundamentals
and Practical Implications of Agentic AI," arXiv:2505.19443, 2025. — `sapkota2025vibe`
[11] S. Liu, "Spec-Driven Development: Unpacking One of 2025's Key New AI-Assisted Engineering
Practices," Thoughtworks Insights, Dec. 2025. — `liu2025specdriven`
[12] L. Moreau and P. Missier (eds.), "PROV-DM: The PROV Data Model," W3C Recommendation,
Apr. 2013. — `w3c2013provdm`

---

## 付記（草稿の管理情報・論文本文ではない）

- **数値**：すべてv4からの転記で、新規数値はない。ja↔enの数値トークン機械照合を転記後に実施
  （手順と結果はchat報告。単位表記の差＝「153万トークン」→「1.53M tokens」、語数表記
  （one／two／three等）への言い換えは照合時に説明対象として扱う）。
- **用語対応表（英訳で使用した主要対訳）**：周辺文書＝distractor documents（初出定義は
  task-adjacent but non-essential documents。要旨と§1 P2で定義）／責務＝mandate／境界＝scope／
  義務＝obligation／受入条件＝acceptance criteria／来歴＝provenance／封印＝sealed／
  材料＝materials・材料の一覧＝manifest／依頼＝review request／判定＝verdict／
  検出率＝detection rate／主題適中率＝on-topic rate／誤検出＝false positive／
  仕込んだ欠陥＝seeded defect／正解表＝answer key／採点語彙＝scoring vocabulary／裁定＝
  adjudication／被覆＝coverage／陳腐化＝staleness／誤停止率＝false-stop rate／範囲外読み取り＝
  out-of-scope read／承認文言＝approval statement (verbatim)／仕様駆動開発＝
  specification-driven development。「irrelevant」は本文で不使用（unrelated garbageのみ）。
- **double-blind配慮**：プロジェクト名・記録のpath・固有の道具名は本文に出さない
  （the subject projectで通す）。公開物（採点語彙・正解表・記録）は投稿時に匿名化して添付する
  前提（preprint方針はHuman判断待ち＝TODO記載のとおり）。
- **文献の特定（2026-08-19実施）**：骨子v2 §3の枠に対し12件を確定（利用者指示「文献の特定を
  先に済ませる。出典をbibtex形式で末尾に追記」）。全12件の書誌情報（著者・題名・出版元・年）は
  web検索で照合済み。BibTeXは本fileの末尾（付記の後）に追記。\citeの本文への当て込みは組版時
  ——目安：§1 P1のvibe coding→[10]・仕様駆動開発→[11]、§2の来歴→[12]（任意）、§4の欠陥注入→
  [8]・事前登録→[9]、§5の各文→[1,2]（LLMレビュー実証）・[3,4]（RAG／文脈工学）・[5]（DbC）・
  [6]（要求追跡）・[7]（agent）・[8]（inspection）・[9]（registered reports）。組版時の残確認
  ＝[9]の巻号・[2]のDOI・[7]の号数（DOIで機械解決可能）。文献節とBibTeXの年号・巻号は英語側
  のみの数値であり、ja↔en数値照合の対象外（照合は論文本文の統計値に限る）。
- **図1（2026-08-19作図済み）**：正本＝`docs/paper/figures/figure1-contract-flow.tex`
  （TikZ・standalone・単体コンパイル可の形）。構図はキャプションと一致——Compile time＝契約
  （definition challengeの人間承認注記つき）→16項目義務関門（型付きエラー）→コンパイラ（決定的）→
  6計画、Run time＝材料一覧→依頼組み立て→読み取り専用レビュー→判定転記→事後検査4点、最下段に
  封印record（SHA-256）の帯が全段へ破線で接続。本環境にLaTeX処理系が無いため**TikZは未コンパイル**
  （構文の最終検証は組版時。同構図のSVGプレビューでレイアウト確認済み・chat提示済み）。
- **残作業（TODOの後続）**：WSSE様式（LaTeX 5頁）での組版（\cite当て込みと図1のコンパイル確認を
  含む。LaTeX環境が必要＝BasicTeX等の導入またはOverleaf）→組版後に確定recordとの数値機械照合。
- v4（原本・日本語）：`docs/paper/2026-08-19-wsse-draft-ja-v4.md`（残す）

---

## 付記2：BibTeX（組版用・論文本文ではない・末尾追記）

```bibtex
@inproceedings{li2022automating,
  author    = {Li, Zhiyu and Lu, Shuai and Guo, Daya and Duan, Nan and Jannu, Shailesh and
               Jenks, Grant and Majumder, Deep and Green, Jared and Svyatkovskiy, Alexey and
               Fu, Shengyu and Sundaresan, Neel},
  title     = {Automating Code Review Activities by Large-Scale Pre-training},
  booktitle = {Proceedings of the 30th ACM Joint European Software Engineering Conference and
               Symposium on the Foundations of Software Engineering (ESEC/FSE)},
  year      = {2022},
  doi       = {10.1145/3540250.3549081}
}

@inproceedings{tufano2022using,
  author    = {Tufano, Rosalia and Masiero, Simone and Mastropaolo, Antonio and
               Pascarella, Luca and Poshyvanyk, Denys and Bavota, Gabriele},
  title     = {Using Pre-Trained Models to Boost Code Review Automation},
  booktitle = {Proceedings of the 44th International Conference on Software Engineering (ICSE)},
  year      = {2022}
}

@inproceedings{lewis2020rag,
  author    = {Lewis, Patrick and Perez, Ethan and Piktus, Aleksandra and Petroni, Fabio and
               Karpukhin, Vladimir and Goyal, Naman and K{\"u}ttler, Heinrich and Lewis, Mike and
               Yih, Wen-tau and Rockt{\"a}schel, Tim and Riedel, Sebastian and Kiela, Douwe},
  title     = {Retrieval-Augmented Generation for Knowledge-Intensive {NLP} Tasks},
  booktitle = {Advances in Neural Information Processing Systems 33 (NeurIPS)},
  year      = {2020}
}

@article{mei2025context,
  author  = {Mei, Lingrui and Yao, Jiayu and Ge, Yuyao and Wang, Yiwei and Bi, Baolong and
             Cai, Yujun and Liu, Jiazhi and others},
  title   = {A Survey of Context Engineering for Large Language Models},
  journal = {arXiv preprint arXiv:2507.13334},
  year    = {2025}
}

@article{meyer1992contract,
  author  = {Meyer, Bertrand},
  title   = {Applying ``Design by Contract''},
  journal = {Computer},
  volume  = {25},
  number  = {10},
  pages   = {40--51},
  year    = {1992},
  doi     = {10.1109/2.161279}
}

@inproceedings{clelandhuang2014traceability,
  author    = {Cleland-Huang, Jane and Gotel, Orlena C. Z. and Huffman Hayes, Jane and
               M{\"a}der, Patrick and Zisman, Andrea},
  title     = {Software Traceability: Trends and Future Directions},
  booktitle = {Future of Software Engineering (FOSE)},
  pages     = {55--69},
  year      = {2014},
  doi       = {10.1145/2593882.2593891}
}

@article{wang2024agents,
  author  = {Wang, Lei and Ma, Chen and Feng, Xueyang and Zhang, Zeyu and Yang, Hao and
             Zhang, Jingsen and others},
  title   = {A Survey on Large Language Model Based Autonomous Agents},
  journal = {Frontiers of Computer Science},
  volume  = {18},
  number  = {6},
  pages   = {186345},
  year    = {2024},
  doi     = {10.1007/s11704-024-40231-1}
}

@article{basili1996pbr,
  author  = {Basili, Victor R. and Green, Scott and Laitenberger, Oliver and Lanubile, Filippo and
             Shull, Forrest and S{\o}rumg{\aa}rd, Sivert and Zelkowitz, Marvin V.},
  title   = {The Empirical Investigation of Perspective-Based Reading},
  journal = {Empirical Software Engineering},
  volume  = {1},
  number  = {2},
  pages   = {133--164},
  year    = {1996},
  doi     = {10.1007/BF00368702}
}

@article{ernst2023registered,
  author  = {Ernst, Neil A. and Baldassarre, Maria Teresa},
  title   = {Registered Reports in Software Engineering},
  journal = {Empirical Software Engineering},
  year    = {2023},
  doi     = {10.1007/s10664-022-10277-5}
}

@article{sapkota2025vibe,
  author  = {Sapkota, Ranjan and Roumeliotis, Konstantinos I. and Karkee, Manoj},
  title   = {Vibe Coding vs. Agentic Coding: Fundamentals and Practical Implications of
             Agentic {AI}},
  journal = {arXiv preprint arXiv:2505.19443},
  year    = {2025}
}

@misc{liu2025specdriven,
  author       = {Liu, Shangqi},
  title        = {Spec-Driven Development: Unpacking One of 2025's Key New {AI}-Assisted
                  Engineering Practices},
  howpublished = {Thoughtworks Insights},
  month        = dec,
  year         = {2025},
  note         = {\url{https://www.thoughtworks.com/en-us/insights/blog/agile-engineering-practices/spec-driven-development-unpacking-2025-new-engineering-practices}}
}

@misc{w3c2013provdm,
  author       = {Moreau, Luc and Missier, Paolo},
  title        = {{PROV-DM}: The {PROV} Data Model},
  howpublished = {W3C Recommendation},
  month        = apr,
  year         = {2013},
  note         = {\url{https://www.w3.org/TR/2013/REC-prov-dm-20130430/}}
}
```
