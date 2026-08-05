# Codex → Claude：Work 5A Definition Challenge設計指示

## 誰が何をするか

- **Human**は、Work 5Aの未完了項目「Definition Challengeを通し、Contractの粒度と依存を確認した」を実施すると指示した。
- **Claude**は、最小Definition Challengeの設計提案だけを作る。
- **Codex**は、Claudeの完了報告を独立確認する。Humanが設計を承認するまで実装へ進まない。

## 平易な目的

Final Challengeは「実行した結果が上位の目的を損なわないか」を見る。
Definition Challengeはその前に、**「このReview Contractの定義が必要な要件を取りこぼしていないか、
範囲が狭すぎないか、禁止した操作や依存を忘れていないか」**を確認する。

今回の対象は、既に実装済みの最初の文書Review Contractだけである。汎用Challenge frameworkを作らない。

## 固定材料

設計案は、少なくとも次を読んで根拠を示す。

- `docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md`
  - §2（Contract定義）、§7（直接束縛する16 Requirement）、§8（既存受入条件）
- `records/requirements/definitions/req-contract-004--v1.json`
- Work 5Aが直接束縛する16 Requirement definition
- `docs/development/2026-08-02-development-policy.md`
- `docs/current/reviewcompass3-plan-current.md`のWork 5A・Work 6A境界
- `tools/task_contract/`と`tests/test_first_review_task_contract_e2e.py`

Architecture Policy、Challenge Policy、risk catalog、隣接Contractのうち、実在しないか、
この最小sliceで固定されていないものがあれば、推測で作らない。不足材料と、そのためにできない検査を
設計案へ明記する。

## Claudeが作るもの

次の新規文書一件だけを作る。

`docs/design/2026-08-05-work5a-definition-challenge-proposal.md`

状態は`awaiting_human_approval`とする。Decision recordは作らない。

設計案には、少なくとも次を含める。

1. Definition Challenge、Conformance、Final Challengeの違いを、目的・入力・出力・実施時点で表にして固定する。
2. 今回使う固定材料、材料ごとの役割、Digest固定方法、材料が不足した場合の停止条件。
3. 最小の決定的な検査規則。少なくとも、16 Requirementの受け先、Contractの10節、
   対象が一文書だけである境界、LLM／外部送信／Git書込み禁止、owner分離、
   Deferred 34 Requirementを誤って直接受理しないことを扱う。
4. Findingとverdictの最小schema、blocking／nonblockingの分類根拠、
   blocking Findingがあるとaccepted artifactを作れない経路。
5. TDD受入条件。正常例と、Requirement欠落、Contract節欠落、scope逸脱、禁止能力、
   材料不足、Definition／Finalの混同を含む負例を、実装前にREDで固定できる形にする。
6. Work 5Aの既存recordとの接続と、実際のContractを使った初回Definition Challenge Runの方法。
7. Work 6Aへ送る範囲。今回の最小Definition Challengeに含めず、負例の拡張で扱う項目を明確にする。
8. 実施単位の分割。設計承認、RED、実装、GREEN、実Run、Human判断が必要な箇所を示す。

## 禁止事項

- `tools/task_contract/`、`tests/`、`TODO_NEXT_SESSION.md`、Current Plan、checklist、Requirementを変更しない。
- Challenge Policy、risk catalog、Requirement、Contractを推測で新設しない。
- LLM、外部送信、外部`DATA_ROOT`、push、PR、CI、Work 4B、Work 6A、E2以降を開始しない。

## 検証・コミット・完了報告

- 設計文書の参照先、記載したDigest、`git diff --check`を確認する。
- 設計文書一件だけを一つのコミットにする。
- 完了報告はコミットに混ぜず、次へ新規保存する。

`records/session-handoffs/2026-08-05-claude-to-codex-work5a-definition-challenge-design.md`

報告には、commit SHA、固定できた材料、不足材料、提案した最小検査範囲、Human判断が必要な点、
未実施事項を記す。
