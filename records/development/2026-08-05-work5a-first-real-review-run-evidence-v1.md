# Work 5A First Real Review Run Evidence v1

## 対象と範囲

- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-work5a-first-real-review-run.md`
- 承認：`DEC-WORK4-FIRST-REVIEW-CONTRACT-DESIGN-001`
- 実装：`tools/task_contract/`（Work 5A GREEN、commit `cee88d7`）

| 項目 | 値 |
| --- | --- |
| target | `docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md` |
| target SHA-256 | `14901323a958d686ba0ad0aed62b20b7b7d79908afcced08dc90f72fdb3d2054` |
| base commit | `0ad628f` |
| head commit | `2edb1b6` |
| scenario | `new_development` / `fresh` |
| review範囲 | target一文書だけ |
| reviewer | deterministic stub reviewer（LLM非使用） |

## 事前検証：targetが指定commitから変化していないこと

Gitで次を確認した。`stale`停止の条件には該当しなかった。

- `2edb1b6:<target>`のblob objectと`HEAD:<target>`のblob objectが同一（`694411dd…`）。
- `2edb1b6`のblob内容のSHA-256と、作業treeのfile SHA-256が一致
  （いずれも`14901323…`）。
- `git diff --stat 2edb1b6 HEAD -- <target>`は空。

targetは`0ad628f`には存在せず、`2edb1b6`で新規追加された。したがってChange Setは追加一件であり、
`new_development / fresh`と整合する。

## 実行command

```text
.venv/bin/python（`tools.task_contract`を用いた機械実行）
  bind_requirements → read_source_snapshot → build_review_task_contract
  → compile_contract → build_context_manifest → acquire_permit
  → run_stub_reviewer → evaluate_conformance → evaluate_final_challenge
  → release_permit
```

Requirementは実repositoryの`records/requirements/definitions/`から、Work 4 proposal §7の16件を
束縛した。`compile_verdict`は`compiled`であった。

## record ID とDigest

| record kind | record ID | content digest |
| --- | --- | --- |
| `requirement_binding` | `RB-FIRST-REVIEW-CONTRACT` | `831217a7c3850fb7…` |
| `source_snapshot` | `SS-FIRST-REVIEW-CONTRACT` | `170e9f9ffec1fdce…` |
| `review_task_contract` | `TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | `e67dc0d175510d22…` |
| `compile_verdict` | `CV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | `ad68259896fe188f…` |
| `context_manifest` | `CM-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | `b955bfc01a82117a…` |
| `workflow_permit` | `WP-CM-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | `9631097c88c6d975…` |
| `finding_set` | `FS-CM-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | `151bc3e4e56f03ae…` |
| `conformance_verdict` | `CFV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | `8b7d44954e336157…` |
| `final_challenge_verdict` | `FCV-TC-RC3-REVIEW-DOC-CHANGE-2026-08-05-V1` | `b059894e80e325c6…` |

全文は`records/development/2026-08-05-work5a-first-real-review-run-records-v1.json`にある。

## 結果

| 項目 | 実測 |
| --- | --- |
| Finding件数 | 0（`error` 0、`warning` 0、`info` 0） |
| Conformance | `passed` |
| Final Challenge | `passed` |
| `human_decision_required` | `true` |

想定（error 0件、warning 0件）と実測が一致した。改竄していない。
Finding 0件は設計§8.3のC1（Finding 0件でも正常経路が完結する）に相当する実データである。

## source内容の非重複保存

record bundleにsource本文を重複保存していない。次の二recordを保存時にredactした。

| record | 除去したfield | 保持した情報 |
| --- | --- | --- |
| `source_snapshot` | `files[].text` | 相対path、SHA-256、base/head commit、元の`content_digest` |
| `context_manifest` | `material_contents` | 材料束（role、相対path、出所、SHA-256）、Scope contract、元の`content_digest` |

redactは`redaction`fieldで明示し、`unredacted_content_digest`に元のDigestを残した。
このためこの二recordは保存物からDigestを再計算できない。下流recordの参照Digestと
target Digestで整合を確認する形とした。この限界は本Evidenceの記載事項とする。

## 読み戻し照合

保存後にfileを読み戻し、29項目を機械照合して全一致を確認した。

- redactしていない7 recordのDigest再計算が一致した。
- redactした2 recordが元Digestとredaction理由を保持していた。
- 相互reference10件が一致した（compile→contract、context→plan_bundle、permit→context、
  finding→context、finding→permit、conformance→finding、challenge→conformance、contract→binding ほか）。
- target Digestが、作業tree、`2edb1b6`のblob、context材料束、snapshotの四箇所で一致した。
- `human_decision`、`provenance_verdict`、`accepted_artifact`が未収録であった。
- 束縛Requirementが16件であった。

## Human decisionの状態

**未実施である。**Human decisionが無いため、`provenance_verdict`と`accepted_artifact`を作っていない。
target文書も修正していない。次の判断はHumanが行う。

## 未実施の確認

LLM、外部送信、外部`DATA_ROOT`、push、PR、CIを使っていない。
Requirement、Current Plan、checklist、Work 5A実装、targetを変更していない。
Work 4B、後続評価E2以降も開始していない。
