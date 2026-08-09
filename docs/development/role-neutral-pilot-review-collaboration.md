# 操縦者を差し替え可能にするPilot／Review連携方法

状態：運用メモ（試行）

共通レビュー基準：`docs/development/work-review-protocol.md`

既存の受け渡し例：

- `docs/development/codex-claude-collaboration.md`

本メモは、操縦者をClaudeまたはCodexのどちらにも固定せず、作業ごとに役割を割り当てるための
試行手順である。製品schema、Workflow state machine、既存authorityは変更しない。

## 1. 適用条件と優先関係

Humanが作業開始時に`role_neutral_pilot_review` modeを明示した場合だけ本メモを使う。
このmodeでは、`work-review-protocol.md` §9の実行者別受け渡しと既存連携文書の担当者固定だけを
本メモの役割割当に置き換える。レビュー順序、判定、Human境界、Git規律、TDD、Evidence規則は
置き換えない。

開始時に次を固定する。

```text
collaboration_mode: role_neutral_pilot_review
pilot: claude | codex
reviewer: codex | claude
closer: reviewer | humanが指定した担当
work_item: <一つの作業項目>
```

`pilot`と`reviewer`は同じ担当にしない。ClaudeとCodexは直接通信せず、Humanがpathと再開指示を
受け渡す。

本modeでは、独立Reviewerを確保するため、Pilotが操縦と実装を一体で担当する。操縦と実装を別担当に
する従来方式は`codex-claude-collaboration.md`のmodeとして分離し、本modeへ暗黙に混在させない。

## 2. 役割

| 役割 | 責務 | 禁止事項 |
| --- | --- | --- |
| Human | 作業項目の指定、意味的裁定、必要なrisk確定、再開・段完了承認、受け渡し | Evidenceのない完了Claimによる次段開始 |
| Pilot | authority確認、範囲固定案、risk提案、TDD、実装、Evidence、レビュー依頼 | 自分の完了Claimを`verified`として扱うこと |
| Reviewer | 上流からの独立導出、範囲レビュー、事後状態確認、反証、verdict | レビューと実装修正の混在 |
| Closer | `verified`後の完了Evidence、TODO、checklist、transitionの反映 | 未検証Claimまたは未承認の段完了反映 |

ReviewerとCloserを同じ担当にしてよい。ただし、レビューと完了projectionは別作業単位、別commitに
する。Reviewerはレビュー中に実装対象fileを変更しない。

## 3. Riskの提案と確定

Pilotは範囲固定文書へ`low`、`medium`、`high`の提案と根拠を書く。Humanがriskを確定するまで実装へ
進めない。不明、分類競合、上位risk該当の疑いが残る場合は`high`として停止する。

| risk | 実装前 | 完了後 |
| --- | --- | --- |
| `low` | Humanがriskと実装開始を確認すれば実装可能。Reviewerは完了レビューで過小分類も確認する | 対象Testと関連validatorを独立再実行 |
| `medium` | Reviewerが範囲とriskを簡易レビューし、Humanが再開を確認するまで停止 | 全Testを含む独立レビュー |
| `high` | Reviewerが上流から範囲を独立レビューし、Humanがriskと再開を明示承認するまで停止 | 全Test、独立oracle、Pilotのfixtureにない反証を最低1件実行 |

`medium`の簡易レビューでは、少なくとも上流authorityとの整合、受入条件・変更可能path・
禁止事項・停止条件の妥当性、risk分類の妥当性を確認する。

守り役のcodeと不可逆操作を行うcodeは`work-review-protocol.md`どおり既定で`high`とする。
safety、authority、Acceptance、必須Provenance、identity、外部side effectへ影響する自己適用作業では、
AIの分類とrouteは提案であり、Humanがrisk受容と再開を判断する。

Reviewerが過小分類を見つけた場合は実装済みでも`verified`にせず、適切なriskのoracleを追加して
再レビューする。Human判断が必要な境界を後付けで省略しない。

## 4. 範囲固定

Pilotは実装前に範囲固定文書を作り、単独commitする。pathは次を基本とする。

```text
records/session-handoffs/YYYY-MM-DD-<pilot>-pilot-<work>-scope-v<N>.md
```

`<work>`の命名規則とcommit前のignore検査（§6のhandoff path規則）は、本pathを含む
§4・§6・§7の全handoff確定pathへ適用する。

範囲固定文書には少なくとも次を書く。

- mode、Pilot、Reviewer、Closer、work item、risk提案と根拠
- base commit、branch、開始時worktree
- 固定入力のrepository-relative path、identity、version、SHA-256
- `TODO_NEXT_SESSION.md`、Initial Development Checklist、Plan、承認済みDecision、既存Evidenceとの関係
- 今回の最小E2E、受入条件、変更可能path、禁止path、未実施範囲
- Human承認境界、停止条件、必要なTest、validator、独立oracle
- 予定する意味単位のcommit境界

TODOの読取、更新、検証は`docs/development/prompts/todo-handoff-update.md`だけを入口にする。

`medium`または`high`の範囲レビューでは、ReviewerはPilotのTestや実装案をoracleにせず、先に上流
authorityから受入条件と反証候補を独立に導出する。結果は次へ固定する。

```text
records/session-handoffs/YYYY-MM-DD-<reviewer>-scope-review-<work>-v<N>.md
```

Reviewerは範囲レビュー結果を単独commitして停止する。未コミットhandoffを残さない原則は、
完了レビューだけでなく範囲レビューにも適用する。

範囲変更が必要なら元文書や履歴を書き換えず、Pilotが次versionを新規commitする。`high`では、合格した
範囲レビューとHumanの再開承認を受け取るまでREDを開始しない。

## 5. 実装とcommit境界

振る舞いを変更する場合、PilotはTDDで進める。

1. 期待入出力をTestへ固定する。
2. 実装がなければ失敗することを単独commandとexit codeで確認する。
3. RED Evidenceへcommand、exit code、件数、environment、Test digestを記録する。
4. Testを弱めず実装を修正し、対象Test、関連Test、riskに応じた全TestをGREENにする。
5. GREEN Evidenceと公式receiptを固定する。

`SCOPE`、`RED`、`GREEN`は意味的に完結する単位でcommitする。ただし、赤Testだけのcommitを必須と
するかは現行の開発方針とTask Contractに従う。文書、試作、調査へRED／GREENを強制しない。

要求の誤解、上流変更、Testの誤り、設計変更が判明した場合は停止する。Humanが変更を承認した後、
理由と影響範囲を固定し、必要なら新しい範囲versionまたは訂正RED commitから再開する。既存commitを
amend、rebase、resetして見えなくしない。

## 6. レビュー依頼

Pilotは実装後、次のレビュー依頼書を作り、単独commitして停止する。

```text
records/session-handoffs/YYYY-MM-DD-<pilot>-pilot-<work>-review-request-v<N>.md
```

handoff fileの命名には`<pilot>-to-<reviewer>`形式を使わない。`.gitignore`の
`records/session-handoffs/*-claude-to-codex-*.md`は非公開のchat型報告を管理外にする
既存規則であり、本modeのcommit対象handoffはこの規則に掛からない名前とし、ignore規則
自体は変更しない。

`<work>`には予約substring`claude-to-codex`を含めない。作業名が本来この語を含む場合は
`claude2codex`へ正規化して使う。§4・§6・§7の全handoff確定pathは、file作成・commitの
前に単独commandで`git check-ignore --no-index <path>`を実行し、exit codeで判定する。
`0`はignoredとして停止、`1`だけを続行可能、`2`以上は検査エラーとして停止する。

レビュー依頼書には次を書く。

- 範囲固定文書と、該当する範囲レビュー結果
- baseから最新の実装commit（GREEN等）までのcommit列と各役割。レビュー依頼commit自体の
  SHAは依頼書へ書かず、Reviewerがgitから特定する
- 実施、結果、判断、未実施、提案へ分けたClaim
- 成果物、Test、Evidence、receiptのpathとSHA-256
- Human承認と対象identity
- 禁止操作を行っていないこと、現在のworktree、停止地点

レビュー依頼書もcommitする。これによりレビュー入力を不変にし、完了時に未コミットhandoffを残さない。
レビュー依頼commitは完了Evidenceではなく、Claimを固定する境界である。

HumanがReviewerへ渡す文面：

```text
次のレビュー依頼書を全文読み、work-review-protocol.mdと参照された範囲固定文書に従って
独立レビューしてください。Pilotは<claude|codex>、Reviewerは<codex|claude>です。
上流authorityから受入条件を独立に導出し、risk分類の妥当性も確認してください。

<レビュー依頼書のrepository-relative path>
```

## 7. 独立レビュー

Reviewerは`work-review-protocol.md`の順序と判定を使う。特に次を確認する。

- base、commit列、変更path、範囲外変更、review時点worktree
- 固定入力と成果物の再読込、Digest再計算、参照解決
- 範囲固定後の受入条件、禁止事項、riskの無承認変更がないこと
- 対象Test、関連validator、riskに応じた全Testの独立再実行
- Workflow、Provenance、Human境界、外部side effect、未実施範囲
- Pilotの報告とrepositoryの事後状態の一致

`high`では、Pilotのfixtureにない反証を最低1件新作し、上流authorityから導出した独立oracleで確認する。
Reviewer自身が過去に範囲レビューを行っていても、PilotのTest再実行だけを独立oracleに数えない。

レビュー結果は次へ固定し、単独commitして停止する。実装修正と混在させない。

```text
records/session-handoffs/YYYY-MM-DD-<reviewer>-review-result-<work>-v<N>.md
```

判定は`verified`、`reported_unverified`、`report_execution_mismatch`、`blocked`、`not_executed`から選ぶ。
`verified`以外を完了、checkbox、次段開始の根拠にしない。

## 8. 不合格、修正、再レビュー

`verified`以外では次の順序を使う。

1. ReviewerがFinding、Evidence、影響範囲、staleになるClaim、未実施範囲をreview resultへ固定する。
2. HumanがresultのpathをPilotへ渡し、修正開始、後回し、本線復帰のいずれかを判断する。
3. Pilotは承認されたFindingだけを別作業単位で修正する。
4. 受入条件、Test、scope、schema、Human境界を変える必要があれば、変更前に停止してHuman判断を得る。
5. Pilotは訂正commitと新しいreview requestを固定し、Reviewerが元の受入条件を含めて再レビューする。

報告文だけを書き換えて不一致を閉じない。修正後は原因箇所だけでなく、元の受入条件、変更した検査器、
入力前提、影響する過去verdictを再確認する。

## 9. 完了projection

`verified`後、Closerはレビューとは別の作業単位として次を行う。

1. review result、独立Test receipt、成果物Digestを再読込する。
2. 必要な完了Evidenceを固定する。
3. Initial Development Checklistの該当項目だけをEvidence付きで更新する。
4. 共通TODO手順で`TODO_NEXT_SESSION.md`を次の一作業へprojectionする。
5. validator、`git diff --check`、該当Testを単独commandで確認する。
6. 明示pathだけをstageし、完了projectionを意味単位commitする。
7. commit後にread-only照合し、`work_unit_transition --work-status completed`を実行する。

段完了または意味的裁定を伴う場合は、Human承認を得てから反映する。自己SHAやGit状態の転記だけを目的と
する追加commitは作らない。

## 10. 試行で測るもの

方式の採否は印象で決めず、少なくとも次を試行Evidenceへ記録する。

- Humanの着手指示から範囲固定までの時間
- Humanによる受け渡しと再開承認の回数
- 実装前の範囲修正件数
- 完了レビューのFinding件数とseverity
- 修正commit数と全Test再実行回数
- `reported_unverified`または`report_execution_mismatch`の有無
- 完了までの総経過時間と、未実施範囲の保持

一件の結果だけで恒久方式へ昇格しない。`low`、`medium`、`high`の適用結果を分け、Humanが継続、改定、
廃止を判断する。

## 11. 最小チェック

- [ ] mode、Pilot、Reviewer、Closer、work itemを固定した。
- [ ] risk提案、authority、Digest、範囲、禁止事項、停止条件を固定した。
- [ ] riskに必要な範囲レビューとHuman再開承認を満たした。
- [ ] REDからGREENへの実行Evidenceを固定した。
- [ ] review requestをcommitし、Pilotが停止した。
- [ ] Reviewerが上流から受入条件を独立導出した。
- [ ] riskに応じたTest、validator、反証を独立実行した。
- [ ] 不合格時の修正を別作業単位にした。
- [ ] `verified`後の完了projectionをレビューと別commitにした。
- [ ] 次の一作業を始める前にtransitionを確認した。
