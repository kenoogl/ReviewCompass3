# group E 外部送信・機微境界修正 範囲レビュー結果 v1

- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：scope（実装前の範囲レビュー）
- risk：`high`（Reviewer判断。Human確定前）
- 判定：**要修正**
- 実行状態：`correctly_stopped_before_RED`
- Finding：blocking 4件、non-blocking 0件
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`

## 1. 固定対象と開始状態

- 対象：
  `records/session-handoffs/2026-08-10-claude-pilot-egress-guard-fix-scope-v1.md`
- 対象SHA-256：`432ad92b523c0abd06cc99d5eabff19d2a01fcdb697b1044b01635db58718206`
- 対象commit：`2c970d91f631a641f191acdba3473dbd3c474e69`
- base：`4bb1c9bf41687734da0af075b0fe8dbbac03a58c`
- branch：`main`
- 許可範囲：本判定record 1件の新規作成と単独commit、読取り、一時領域での
  受入条件の反証確認
- 禁止範囲：対象scope、code、test、既存record、config、schema、TODO、checklistの変更、
  RED開始、実際の外部送信、push、履歴書換え

【実測】対象commitの親は申告baseと一致し、変更pathは対象scope 1件の追加だけだった。
レビュー開始時のworktreeとindexはcleanだった。対象scopeの固定入力5件はSHA-256を再計算し、
5／5で記載値と一致した。対象commitの`git diff --check`は終了コード0だった。

【実測】本recordの予定pathに対する`git check-ignore --no-index`は終了コード1、作成前の
`test ! -e`は終了コード0だった。

## 2. 上流authorityとの整合

【記録】出口設計v4は、送信payloadをcode断片、許可された数値・列挙値、承認済み定型文の
3種へ閉じ、Humanが目視した実物一覧への承認、承認recordの実在・有効期限・一回性、現在sourceからの
由来解決、秘密値走査、承認済み閾値、段階1の送信不能を要求する。

【判断】F-E1〜F-E5の修正方向はこの既存境界への適合に収まる。新しい送信段階、payload種別、
schema、方針値は導入していない。F-E3の3形式と除外規則は未承認の方針値としてHumanへ残しているため、
内容自体を本レビューで裁定しない。

【記録】出口設計v4 §2は実装対象を`runner`内の出口関門つき送信係とし、§9は生ログ保全を
設計対象としていない。F-E6・F-E7の上流根拠は、group E判定recordが参照するSession Logの
Requirementと保全契約である。

【判断】対象scope §4の「いずれも出口設計v4が既に要求している事項」という一括説明は、
F-E6・F-E7には成立しない。両Findingをgroup E修正へ含めること自体は修正順序Decisionと一致するが、
保全sliceの上流authorityとDigestを直接固定し、出口設計v4への適合と区別する必要がある。

## 3. Human境界

【判断】risk `high`の提案は妥当であり、対象scopeはHumanによるrisk確定と着手承認を未実施のまま
残している。RED後にtestを変える場合のHuman承認も§5に明記されている。この2境界に欠落はない。

【判断】一方、F-E3の形式一覧と除外規則は、期待挙動をRED testへ固定した時点で方針値を実質的に
確定する。対象scope §8.3は未承認時の停止をGREEN着手前にしか要求せず、RED-1開始前の停止を
明記していない。§9でHumanへの確認事項に列挙するだけでは、この順序の穴を閉じない。

## 4. 7 Findingと受入条件

【実測】対象scopeは、元の7 Findingと11件の成立反証を次のように全件取り込んでいる。

| Finding | 元の反証 | scope上の方向 |
| --- | --- | --- |
| F-E1 | A1、A2、A3 | 承認recordの実在束縛、必須field、有効期限 |
| F-E2 | P1、G1、G2 | 現在sourceとの一致、入れ子構造、値型 |
| F-E3 | G3 | 資格情報3形式とDigest由来数字列の除外 |
| F-E4 | F1 | 閾値・重みの有限性と承認済み関係 |
| F-E5 | S1 | 段階1での注入処理の事前拒否 |
| F-E6 | R1 | 改変backupを台帳で正当化しない順序 |
| F-E7 | R2 | raw・backup両側の解決後root束縛 |

【判断】7 Findingの実装対象moduleには取りこぼしも、別groupへの先取りもない。

【実測】元の反証scriptはgroup E判定record記載どおりSHA-256
`7906a65a20cb70ee56640ee01165927faa879d07bc8d96fbdac0309aa78c7c79`だった。
S1を再実行すると終了コード1で、出力は
`callback_side_effect_before_stop: true`と`stopped_as_not_approved: true`を同時に示した。

【判断】したがって、対象scope §6.1の「同じ入力で拒否される」だけではS1の修正を判定できない。
現行実装も最終的には拒否しているため、callbackが停止前に実行されないことを機械条件に含めなければ、
誤った合格が成立する。また、F-E3のDigest由来数字列の誤拒否は11件の名前付き反証に含まれず、
group E判定recordは既存正例もこの表現を踏んでいないと記録する。安全なDigest表現を誤拒否しない
正方向の機械条件も必要である。具体的なfixture構成は本レビューでは指定しない。

## 5. 変更可能path、slice、commit境界

【判断】egressとSession Log保全を2 sliceへ分け、各sliceをREDとGREENに分ける方向は妥当である。
実装完了後にreview requestを別commitにする境界も維持されている。

【実測】一方、§5のRED-1は`tests/test_egress_*.py`を変更対象とする。この表現には
`tests/test_egress_dry_run.py`が入るが、§7の変更可能pathには同fileが入っていない。
また、§7の「Evidence record（新規）・公式receipt（新規）・review request（新規）」は
repository-relative pathを固定していない。§5ではGREEN-1でEvidenceとreceiptを作り、GREEN-2で
それらを更新する記述になっており、slice別の新規成果物なのか同じ成果物の上書きなのかも確定しない。

【判断】この状態では、変更pathが許可範囲内か、各GREEN commitが独立したEvidenceと検査結果へ
結ばれているかを機械照合できない。実装手段ではなくscopeとcommitの境界そのものなので、RED前に
解消する必要がある。

## 6. Finding（§11）

### SR-EG-SCOPE-001 blocking／scope／§11.1類型1

【判断】F-E6・F-E7まで出口設計v4が要求するとしたauthority説明が、v4の対象境界と一致しない。
保全sliceの実際の上流authorityとDigestを固定し、F-E1〜F-E5の出口設計適合と分ける必要がある。

### SR-EG-SCOPE-002 blocking／scope／§11.1類型2

【判断】F-E3の形式一覧・除外規則に対するHuman承認がGREEN前にしか強制されず、未承認の方針を
RED testへ固定できる。F-E3を含むRED-1の開始前に承認境界を置く必要がある。

### SR-EG-SCOPE-003 blocking／scope／§11.1類型3

【判断】11件を一律に「拒否」で照合する受入条件は、拒否前の副作用が残るS1を誤って合格できる。
さらにF-E3のDigest由来数字列に対する偽陽性を検出する正方向条件がない。安全側と危険側の双方を
機械判定できる受入方向へ直す必要がある。

### SR-EG-SCOPE-004 blocking／scope／§11.1類型4

【判断】RED-1のワイルドカードと§7のtest一覧が不一致であり、新規Evidence、receipt、review requestの
pathと2つのGREEN間の扱いも未固定である。変更可能pathと意味単位commitの境界を一意にする必要がある。

### non-blocking／defer

【判断】0件。実装方式、command option、例外型、時刻取得方法、fixtureの細部には立ち入らない。

## 7. 判定と次

判定：**要修正**

【判断】scope commitは1 fileだけで、固定入力、開始base、停止地点は申告と一致する。しかし、
上記4件は上流authority、Human境界、誤った合格を許す受入条件、scope・commit境界に該当するため、
現scopeをRED開始の根拠にはできない。

Human境界：risk `high`の確定、F-E3の形式一覧・除外規則の承認、修正版scopeの範囲レビュー後の
RED再開承認は未実施のまま維持する。RED後のtest変更承認も維持する。

未実施：対象scope、code、test、既存record、config、schema、TODO、checklistの変更、RED、GREEN、
実際の外部送信、完了レビュー、Closer作業、push、履歴書換え。

次：Pilotが4件を反映したscope v2を新規commitして停止し、Codexが再範囲レビューする。
