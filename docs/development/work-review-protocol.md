# 作業レビュープロトコル

状態：運用メモ

関連方針：`docs/development/2026-08-02-development-policy.md`

関連設計メモ：`docs/design/2026-08-03-execution-claim-verification-memo.md`

## 1. 目的と適用範囲

実行者がClaude、Codexのサブエージェント、人、scriptのいずれであっても、作業結果を同じ順序と判定基準で
確認する。実行者の完了報告だけで完了とせず、固定した作業指示とrepositoryの事後状態を照合する。

本プロトコルは開発作業、調査、文書変更、record生成、外部操作の事後確認に使う。作業固有の正しさは、
Task Contract、受入条件、Test、validator、Human判断などのoracleを差し替えて確認する。

本メモは新しい製品schemaや自動state machineを定義しない。既存方針を反復可能なレビュー手順へまとめた
運用入口である。

## 2. 基本原則

1. 完了報告はClaimであり、Evidenceではない。
2. レビュー対象は報告文ではなく、固定入力、変更物、commit、Test結果、record、事後状態である。
3. 実行者とreviewerを役割として分ける。reviewerは実行者の成功出力だけを唯一のoracleにしない。
4. Human承認、外部送信、不可逆操作、意味的裁定は、委譲してもHuman境界のまま維持する。
5. レビュー中に別の不具合を見つけても、承認なしに実装修正へ移らない。まず検証結果として分離する。
6. 同じ入力と同じ版の検証は再実行可能にする。検査器または入力前提が変われば、旧合格をstaleとする。

## 3. レビュー開始時に固定するもの

レビュー開始前に、少なくとも次を特定する。

| 項目 | 内容 |
| --- | --- |
| 作業指示 | Task Contract、handoff、受入条件または明示された依頼 |
| 開始状態 | base commit、branch、開始時のworktree、固定sourceの版とDigest |
| 許可範囲 | 変更可能path、許可した操作、作成可能なrecord |
| 禁止範囲 | 変更禁止path、外部操作、Human判断、次段の作業 |
| 期待成果 | file、record、commit、Test、receipt、完了報告 |
| 停止条件 | 固定source不一致、Test不合格、設計矛盾、承認待ちなど |
| risk | `low`、`medium`、`high`と必要なoracle |

次は既定で`high`とする。

- 守り役のcode。validator、Digest照合、承認関門の判定、改竄拒否など、他の成果物の合否を決めるcode。
  失敗が「誤った合格」として黙って現れるためである。
- 不可逆操作を行うcode。移行、削除、上書き、外部送信を含む。

開始状態を特定できない場合、差分の帰属を推測せず`reported_unverified`として停止する。

## 4. 標準レビュー順序

### 4.1 完了報告をClaimへ分ける

報告を次へ分解する。

- 実施：作成、変更、実行、送信など。
- 結果：Test件数、verdict、Finding、生成物など。
- 判断：Human承認、採否、risk受容など。
- 未実施：停止境界より後の操作、禁止操作を行っていないこと。
- 提案：次に行う候補。完了扱いにしない。

### 4.2 Gitと変更範囲を確認する

- base commitからreview対象commitまでのcommit列を確認する。
- `git show`とname-statusで変更pathを列挙する。
- 指示外の変更、既存利用者差分の混入、一括stage、履歴書換えがないことを確認する。
- RED、GREEN、実Runなど、指定された意味単位のcommit境界を確認する。
- review時点のworktree状態を確認する。

### 4.3 成果物を再読込みする

- fileの存在、内容、schema、参照先を確認する。
- Digestを報告値から転記せず、成果物から再計算する。
- record ID、version、content digest、上流ref、new-only規則を照合する。
- 削除、移動、外部操作では、変更前後と復旧可能性も確認する。

### 4.4 振る舞いを独立再実行する

- 対象Testと関連validatorをreviewer側で再実行する。
- `medium`以上では全Testを実行する。
- validator変更では正例、負例、境界例を確認する。
- `high`ではfault injectionまたはmutation、代表データ、独立oracleを追加する。
- `high`では、実行者のfixtureに存在しない反証を最低1件、reviewerが新たに作って機械で試す。
  守り役のcodeでは、誤って合格させる方向（改竄、偽装、迂回、境界値）を優先する。
  反証が成立した場合は検証結果として分離し、承認なしに実装修正へ移らない。
- 宣言→RED対応表を作る作業では、RED固定commitの前に`verify_red=True`で実行照合し、
  結果をRED Evidenceへ記録する。`mismatched`または`unknown`が残る間はcommitしない
  （`DEC-RED-VERIFICATION-ADOPTION-001`）。`red_now`はRED時点の主張であり、
  実装完了後には照合が成立しない。
- 実行command、exit code、件数、environment、receiptを記録する。

### 4.5 WorkflowとProvenanceを確認する

- 必須stepが順序どおりで、前段を飛ばしていないことを確認する。
- permit、approval、verdict、Human decisionの対象identityとDigestを照合する。
- 実行済みstepと未実行stepをrecord内容から確認する。
- 報告された停止地点より後の成果物が作られていないことを確認する。

### 4.6 禁止事項とside effectを確認する

- 禁止path、外部送信、push、PR、CI、不可逆操作の有無を確認する。
- 外部操作はprovider receiptと対象systemの事後状態を独立照合する。
- 実行有無が不明な外部操作を重複実行して確認しない。

### 4.7 報告と実状態を照合して判定する

各ClaimをEvidenceへ接続し、次の状態を一つ選ぶ。

| 状態 | 判定 |
| --- | --- |
| `verified` | 必須Evidenceが揃い、報告と事後状態が一致し、受入条件を満たす |
| `reported_unverified` | Claimはあるが、必要なEvidenceまたは再現条件が不足する |
| `report_execution_mismatch` | 報告と事後状態が競合する |
| `blocked` | 停止条件に正しく到達し、未実施範囲を保持している |
| `not_executed` | 作業または後続stepを実行していないことが確認できる |

`verified`だけを完了、checkbox、次段開始の根拠に使う。`blocked`は停止判断が正しいことの確認であり、
作業全体の完了ではない。

## 5. 作業種別ごとのoracle

| 作業種別 | 最小oracle |
| --- | --- |
| 文書 | diff、再読込み、参照解決、authorityとの意味整合 |
| code | RED根拠、対象Test、既存Test、必要な全Test、静的検査 |
| record／data | schema、件数、identity、version、Digest、上流ref、再生成一致 |
| Review Run | 固定入力、Finding、各verdict、step順序、Provenance、Human境界 |
| Git操作 | commit SHA、tree、name-status、stage対象、remote事後状態 |
| 外部操作 | Human承認、payload、送信先、permission、receipt、外部事後状態 |

`high`のcodeでは、期待挙動を実行者のTestからではなく上流（承認Decision、設計、Contract、
Requirement）から独立に導出して照合する。実行者が書いたTestの再実行だけを独立oracleに数えない。

**機械が検証していない箇所**は`tools/development/verification_boundary.py`の宣言
（`unverified_fields`）に列挙してある。Human裁定文、実行結果の説明、候補の提案文、host申告の
権限などがこれにあたる。これらの欄の合格表示は「検証した」ではなく「検証対象外」を意味する。
reviewerはこの一覧を、Humanが確認すべき対象として扱う。

LLMまたは別エージェントによる再読だけを、決定的Testや実状態照合の代わりにしない。同じモデル系の
サブエージェントによるレビューも、`high` risk作業の唯一の独立oracleにはしない。

## 6. 不一致と途中停止

### Evidence不足

`reported_unverified`として未完了にする。Evidenceを追加取得できる場合だけ再レビューする。

### 報告との不一致

`report_execution_mismatch`として進行を停止する。影響するTODO、checkbox、Verdict、projectionをstaleにし、
原因、影響範囲、修復Evidenceを記録する。報告文の書換えだけで完了にしない。

### 正しい途中停止

停止条件、再現結果、未実施範囲を確認する。停止に必要な作業だけを別指示として固定し、元の作業を暗黙に
拡張しない。修復後は、停止原因だけでなく元の受入条件まで再実行する。

## 7. 再レビューとconcurrency

- review対象commitの後に別作業が入った場合、対象commit列と現在HEADを分けて確認する。
- 共有workspaceで別executorが作業中なら、同じfileを変更しない。
- reviewerが修正を行う場合は、レビュー結果と修正作業を別単位にする。
- 修正後は、変更した検査器、入力前提、影響する過去verdictをstaleとして再確認する。
- 完了済み作業単位を未コミットのまま次へ進めない。

## 8. レビュー報告の最小形式

```text
判定：verified | reported_unverified | report_execution_mismatch | blocked

対象：<指示、commit、成果物>
変更範囲：<一致／不一致とpath>
独立再実行：<command、件数、結果>
Record照合：<identity、version、Digest、参照>
Human境界：<維持／違反>
未実施：<確認した未実行step>
次：<Human判断、修復、次段開始のいずれか>
```

通常の小さな変更では、この形式を短く埋めればよい。Evidence量や文書量を増やすこと自体を品質としない。

## 9. 実行者別の連携差

検証基準は実行者によって変えない。変わるのは結果の受け渡し経路だけである。

| 実行者 | 受け渡し |
| --- | --- |
| Claude | Codexが指示書を作り、Humanが渡し、Humanが完了をCodexへ知らせる |
| Codexサブエージェント | 親Codexが限定scopeを直接委譲し、結果を直接受け取る |
| Human | Humanの報告とrepository／外部systemの事後状態を照合する |
| script | exit codeとstdoutだけでなく、生成物、receipt、事後状態を照合する |

Claude固有の受け渡し方法は`docs/development/codex-claude-collaboration.md`を参照する。

Humanが`role_neutral_pilot_review` modeを明示した場合は、受け渡しと役割割当だけ
`docs/development/role-neutral-pilot-review-collaboration.md`の規則を使う。modeの明示が
ない場合は上表の従来方式を使う。いずれの場合も、レビュー順序と判定基準は本プロトコルの
まま変えない。

## 10. レビュー完了チェック

- [ ] 作業指示、base commit、許可範囲、停止条件を特定した。
- [ ] 完了報告を実施、結果、判断、未実施、提案へ分けた。
- [ ] commit列と変更pathを実状態から確認した。
- [ ] 成果物を再読込みし、Digestと参照を再計算した。
- [ ] 対象Testとriskに応じた全Test／oracleを独立再実行した。
- [ ] `high`では、実行者のfixtureに無い反証を新作して機械で試した。
- [ ] 宣言→RED対応表を作った場合、RED固定commit前に実行照合し、結果をEvidenceへ記録した。
- [ ] Workflow順序、Provenance、Human承認境界を確認した。
- [ ] 禁止操作とside effectの有無を確認した。
- [ ] `verified`以外を完了または次段開始の根拠にしていない。
- [ ] レビュー結果と修正作業を混在させていない。
- [ ] 次のHuman判断または作業を一つだけ示した。
