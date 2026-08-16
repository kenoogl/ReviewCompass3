# Claude → Codex：Work 5A Definition Challenge設計 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-work5a-definition-challenge-design.md`

## 1. commit SHA

`d8a13a617d83ba608e6590d64eb2cde50b6ae0f1`（Propose Work 5A definition challenge）

設計文書一件だけのcommitである。実装、test、TODO、Current Plan、checklist、Requirementを混ぜていない。

| file | SHA-256 |
| --- | --- |
| `docs/design/2026-08-05-work5a-definition-challenge-proposal.md` | `5b6f8aa4b9ffd3c85f9c95934de75e61f81bd3f39d113cbf81acb4e5e24d00c6` |

状態は`awaiting_human_approval`。Decision recordは作っていない。

## 2. 固定できた材料

いずれも実在を確認し、役割とDigest固定方法を提案§2.1へ記載した。

| 材料 | 役割 |
| --- | --- |
| `docs/design/2026-08-05-work-4-first-review-task-contract-design-proposal.md`（§2、§7、§8） | Contract定義、束縛16 Requirement、既存受入条件 |
| `records/requirements/definitions/`の16 file（`req-contract-004--v1.json`を含む） | 各Requirementの本文 |
| `review_task_contract` record | 検査対象そのもの |
| `plan_bundle`の6 typed view | Contractから導出した計画値 |
| `docs/development/2026-08-02-development-policy.md` | LLMと機械処理の責務分離、Human判断必須操作 |
| `docs/current/reviewcompass3-plan-current.md` | Work 5A／6A境界、Definition Challengeの検査観点（551行、557行） |

材料は`definition_challenge_material_set`としてまとめ、各fileのpathとDigestを固定する。
一件でも欠ける、またはDigestが一致しない場合は`definition_material_missing`で停止し、
verdictを発行しない。

## 3. 不足材料

Current Plan 551行が挙げる固定材料のうち、次はこの最小sliceに**実在しない**。
推測で新設せず、そのためにできない検査を提案§2.2と§7へ明記した。

| 不足材料 | 実在状況 | できない検査 |
| --- | --- | --- |
| Architecture Policy | `docs/design/`に該当文書なし | 設計方針との齟齬、層・依存方向の違反 |
| risk catalog | 該当record・policyなし | risk等級に応じた独立reviewer要否、Human gate要否の判定 |
| 隣接Contract | `records/task-contract/`に21件あるが同じ運用面に無い。`.reviewcompass/contracts/`は`.gitkeep`のみ | cross-contract責務の重複・隙間 |
| Challenge Policy | 実在しない | 検査項目・閾値の外部固定。今回は提案内で直接固定した |

Current Plan 557行の`low`／`medium`／`high`分岐は、riskの正本が無いと機械化できない。
本Contractはlow risk（文書一件、外部side effectなし）として扱い、別Runを強制しない設計とした。

## 4. 提案した最小検査範囲

すべてLLMを使わず、固定入力から同じ結果を再生成できる決定的検査である。

| # | 検査 | 停止code |
| --- | --- | --- |
| D1 | 束縛16 Requirementのすべてに受け先がある | `definition_requirement_unreceived` |
| D2 | Contractの10節が空でない | `definition_section_missing` |
| D3 | 対象が`docs/`配下の一文書だけ | `definition_scope_violation` |
| D4 | LLM呼出、外部送信、成果物書込み、Git writeが明示的に偽 | `definition_forbidden_capability` |
| D5 | Conformance、Final Challenge、Human decisionのownerが三者とも異なる | `definition_owner_separation` |
| D6 | deferred 34 Requirementを直接受理していない | `definition_deferred_requirement_accepted` |
| D7 | 材料が揃い、各Digestが実fileと一致する | `definition_material_missing` |
| D8 | Conformance／Final Challengeの入力を使っていない | `definition_stage_confusion` |

Findingの`severity`は`blocking`と`nonblocking`の二値とし、既存の`error`／`warning`／`info`とは
**別語彙**にした。段の混同を語彙のうえでも防ぐためである。現時点でD1〜D7はすべて`blocking`で、
`nonblocking`の実例は作らない。

`blocking`があると`compile_contract`が`not_compilable`を返し、Review Runを開始せず、
accepted artifactへ到達できない。来歴には`definition_challenge_verdict`をnodeとして加え、
node 10件・edge 9件の`provenance_verdict` version 3を新規に作る（version 2は上書きしない）。

受入条件は正常例G1〜G4と負例H1〜H11を提案§5へ固定した。
H8は「Definition ChallengeとFinal Challengeの混同」を直接扱う負例である。

## 5. Human判断が必要な点

意味・authority・scopeに関わる二点だけである。

1. **`provenance_verdict` version 2とversion 3の関係。**version 2はDefinition Challenge導入前の
   正しい9 node構成であり誤りではない。推奨は「`superseded_by_v3`として記録し、無効化はしない」。
2. **Definition Challengeのownerを誰にするか。**推奨は、Conformance・Final Challenge・
   Human decisionのいずれとも異なる論理ownerとし、実行主体は機械（deterministic）とすること。

## 6. 未実施事項

- `tools/task_contract/`、`tests/`、`TODO_NEXT_SESSION.md`、Current Plan、checklist、Requirement：
  **変更していない**。
- Challenge Policy、risk catalog、Requirement、Contract：**新設していない**。
- 実装、test、実Run、Decision record：**作っていない**。
- LLM、外部送信、外部`DATA_ROOT`、push、PR、CI、Work 4B、Work 6A、後続評価E2以降：
  **開始していない**。

検証は、参照先fileの実在、記載した事実（v2 recordのnodeが9件、既存testが38件、
Definition Challengeが未実装、`.reviewcompass/contracts/`にContract recordが無いこと）の機械照合、
および`git diff --check`を実施し、いずれも合格した。
照合で見つかった記述の粗さ二件（Requirement定義fileのpath明記、`.gitkeep`のみである旨）は、
commit前に訂正済みである。

Human承認まで実装へ進まない。
