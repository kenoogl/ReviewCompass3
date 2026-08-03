---
lifecycle: provisional
normative_status: non-normative
promotion_required: true
related_policy: ../development/2026-08-02-development-policy.md
related_plan: ../current/reviewcompass3-plan-current.md
related_checklist: ../development/2026-08-03-initial-development-checklist.md
---

# 会話上の実施報告を実状態と照合する仕組みの検討メモ

## 1. 問題

sessionの会話では、提案、予定、生成要求、Toolの開始、実際の書込み、検証済み成果が同じように
「実施した」と報告されることがある。報告だけを完了根拠にすると、存在しないfile、未実行Test、
未作成commit、未反映の文書を完了済みとして扱い、TODO、checklist、Current Work Projection、
後続判断が誤った状態へ進む。

会話中の報告は「実施されたという主張」のEvidenceにはなるが、対象操作が実際に完了したことの
Evidenceにはならない。本メモは、報告Claimと観測可能な実状態を照合する最小規律を整理する。

## 2. 基本原則

1. 報告はClaimであり、完了Evidenceではない。
2. 「実施」「結果」「判断」「提案」「未実施」を分離する。
3. 実施・結果Claimは、対象identity、固定source、事後状態、検証結果へ接続する。
4. EvidenceがないClaimは失敗と断定せず`reported_unverified`とするが、完了には使わない。
5. 報告と事後状態が競合した場合は`report_execution_mismatch`とし、完了判断を停止する。
6. 不一致を報告文だけの訂正で隠さず、影響を受けたcheckbox、TODO、Verdict、projectionをstaleにする。
7. 予定または提案だけで終わった作業は、正当に「未実施」と報告できる。

この規律を実施報告照合（`execution_claim_verification`）と呼ぶ。

## 3. Claimの分解

最終報告を、少なくとも次の種類へ分ける。

| 種類 | 例 | 完了Evidenceの要否 |
|---|---|---|
| `action_claim` | fileを作成・変更・移動した | 必須 |
| `result_claim` | Testが412件通過した | 必須 |
| `decision_claim` | Humanが方針を承認した | Decision sourceが必須 |
| `proposal_claim` | 次にvalidatorを作るべき | 実施Evidenceは不要。実施済みと表示しない |
| `not_executed` | commitは行っていない | 未実施範囲の明示として保持 |

「文書を修正し、Testを実行し、commitした」のような複合報告は三つのClaimへ分ける。一部だけに
Evidenceがある場合、報告全体をverifiedにしない。

## 4. 最小照合record

初期はsession報告、TODOまたはSession Evidenceへ、次の情報を人が読める形で記録すればよい。

```yaml
claim_id: EC-...
claim_type: action_claim | result_claim | decision_claim | proposal_claim | not_executed
statement: ...
target_identity: ...
source_identity: ...
evidence:
  - type: file | diff | digest | command | test_run | commit | receipt | decision
    locator: ...
observed_post_state: ...
verification_status: reported | evidence_attached | verified | reported_unverified | contradicted
verified_by: ...
verified_at: ...
```

正式schema、全会話のClaim抽出、独立serviceは初期範囲にしない。

## 5. Claim別のEvidence

| Claim | 最小Evidence | 追加確認 |
|---|---|---|
| file作成 | path、存在、内容再読込、Digest | 参照元から解決できること |
| file変更 | diff、変更後再読込 | validator、参照整合、stale閉包 |
| file移動・削除 | 変更前後path、name-status | link検査、rollbackまたは復旧可能性 |
| Test実行 | command、exit code、件数 | Source Snapshot、tool、environmentの一致 |
| commit | commit SHA、対象tree | `git show`と事前Change Setの一致 |
| 文書反映 | path、該当内容、Digest | 関連文書との意味整合 |
| 外部操作 | provider receipt、外部ID、事後状態 | partial failure、再試行、side effect |
| Human判断 | instructionまたはDecision Record | 対象、scope、時点、authority |

低riskの文書変更はpath、diff、再読込、参照整合でよい。code変更は固定sourceとTestを追加する。
外部送信、不可逆操作、権限、release等のhigh risk Claimには、独立した事後確認またはHuman確認を要求する。

## 6. session終了時の照合

1. 最終報告から複合文を原子的なClaimへ分ける。
2. 各Claimを実施、結果、判断、提案、未実施へ分類する。
3. 実施・結果・判断ClaimへEvidence locatorを付ける。
4. 対象を再読込または再照合し、観測した事後状態を記録する。
5. `verified`だけを完了、checkbox、Current Work Projectionの入力に使う。
6. `reported_unverified`と`contradicted`を、未完了または停止として明示する。
7. 提案と未実施範囲を別欄に残す。

会話の長い説明をすべて構造化する必要はない。完了、変更、Test、commit、外部操作、Human判断など、
後続状態を変えるClaimを優先する。

## 7. 不一致時の扱い

`report_execution_mismatch`を検出した場合は、次を行う。

- 該当Claimを`verified`にしない
- 現行WorkまたはStage完了を停止する
- 誤ったTODO、checkbox、Verdict、projectionをstaleにする
- 未実施なら実行し直すか、報告を訂正して未実施として残す
- 原因、影響、修復Evidenceを記録する
- 反復、重大、広範囲の場合は改善候補としてprocess改善へrouteする

報告者の意図を推測して自動修復しない。外部または不可逆side effectの有無が不明な場合は、
重複実行を避けて先に事後状態を確認する。

## 8. 機械化の境界

初期は`git status`、`git diff`、Digest、file存在、Test結果、commit SHA、link検査を手作業で照合する。
Session Log Bootstrap後は、報告文からClaim候補を抽出し、既存Provenance、Git、Test Run、receiptとの
対応候補を提示できる。ただし、意味的に同じ作業か、Evidenceが十分か、high risk Claimを受容できるかは
Humanまたは有効なDecision Authorityが判断する。

機械化を行う場合も、報告者自身の「成功」出力だけを唯一のoracleにしない。対象systemの事後状態と、
可能な場合は独立経路で照合する。

## 9. 評価

Work 8では、少なくとも次を観測する。

- 完了報告Claim数とEvidence接続率
- `reported_unverified`と`report_execution_mismatch`の件数
- 不一致による誤ったStage進行、checkbox、TODO、Verdictの件数
- post-write照合で初めて見つかった不備
- Claim分解と照合の時間、記録量
- 同種不一致の再発率

Claim数や記録量の増加だけを品質としない。誤った完了判断を防ぎつつ、通常の小さな変更を過剰な
手続きで止めないことを確認する。
