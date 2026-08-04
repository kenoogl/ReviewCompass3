# Work 4A Rebuild Design Proposal

状態：`approved_for_rebuild`
対象：Work 4A Reusable Routine Ledger
この文書は、既存のWork 4A patch群を正本にせず、revert後に最初から実装するための設計である。
Human承認は`DEC-WORK4A-REBUILD-DESIGN-001`に記録する。

## 1. 目的と今回止めること

目的は、既存routineを再利用・拡張・統合・分割する判断を、後から同じ根拠で追跡できる最小の台帳にすることである。

今回止めることは次の二つである。

- 新しい関数を一件登録するたび、既存entryを全件コピーして新versionを作ること。
- GitのHEADが変わっただけで、source内容が同じ台帳までstaleと誤判定すること。

したがって、台帳の「現在」はbaseline manifestだけで選び、個別entryとrelationは変更が必要なものだけをnew-onlyで増やす。

## 2. 配置とauthority境界

Project Manifestの`artifact_roots`は既にdeployment packageに含まれるproject artifactのrootを固定している。
この設計はrootを追加しない。台帳は既存の`artifact_roots.reuse`配下に置く。

| 種別 | 配置 | authority | Git・deployment | 手編集 |
| --- | --- | --- | --- | --- |
| Source Observation、Source Symbol Index、Candidate Run | `DATA_ROOT/projects/<project_id>/reuse/` | source codeから機械生成した観測結果 | Git外。deployment package外 | 禁止 |
| Human Decision | `<PROJECT_ROOT>/<artifact_roots.design_decisions>/` | 人が採用した意味的判断 | Git管理のproject artifact。deployment buildには含めない | 人が作成・承認 |
| Ledger Entry、Relation、Baseline Manifest | `<PROJECT_ROOT>/.reviewcompass/reuse/reusable-routine-ledger/` | Human Decisionと機械検証を結んだproject artifact | Git管理のproject artifact。deployment buildには含めない | 禁止。専用writerだけ |
| Historical Contract Status | `records/task-contract-status/` | 既存`records/task-contract/`を歴史的記録として扱う裁定 | Git管理の開発record。deployment buildには含めない | Human Decisionを伴うwriterだけ |

`DATA_ROOT`は環境ごとに異なるため、そこにある観測結果をdeployment packageへ含めない。deployment先では、そのprojectのsourceから再採取する。
台帳とDecisionはdeployment packageの一部ではなく、target projectに属するproject artifactとしてpackageの外で保持する。
従ってpackage更新は台帳を移動・書換えず、deployment版はそのproject artifactをread-onlyで参照する。
これは既存の「project固有recordをpackageに含めない」方針と一致する。

## 3. recordの最小モデル

| record | stable ID | versionを上げる条件 | 必須の結線 | currentの決め方 |
| --- | --- | --- | --- | --- |
| Source Content | `source_content_id` | source universe、対象path、対象file Digestが変わる | fileset Digest | 同じ内容なら同一。recordを保存する対象ではなく算出identity |
| Source Observation | `snapshot_id` | 採取時のHEAD、tool version、採取時刻またはsource内容が変わる | `source_content_id`、HEAD、index Digest | Candidate RunとBaselineが参照したもの |
| Candidate Run | `candidate_run_id` | search input、tool version、candidate結果が変わる | `source_content_id`、snapshot Digest、candidate Digest | Human Decisionが参照したもの |
| Ledger Entry | `entry_id` | 責務、symbol binding、side effect、Human dispositionが変わる | Decision ID/Digest、source symbol、source_content_id | BaselineがID/version/Digestで参照したもの |
| Ledger Relation | `relation_id` | 参加entry、relation kind、rationaleが変わる | 両entry ref、Decision ID/Digest | BaselineがID/version/Digestで参照したもの |
| Baseline Manifest | `baseline_id` | entry/relation集合またはそれらのrefが変わる | `source_content_id`、Observation、Candidate Run、全entry/relation ref | 唯一のcurrent pointer |
| Historical Contract Status | `contract_status_id` | 契約の運用上の状態またはその根拠が変わる | 対象Contractのpath/Digest、creation commit、Human Decision | 対象Contractごとの最新の承認済みstatus |

ここでいう`Digest ref`は、少なくとも`record_id`、`version`、`path`、`sha256`を同時に持つ参照である。pathだけ、IDだけ、またはversionだけの参照は認めない。

## 4. identityとfreshness

`source_content_id`は、対象source universe、正規化した相対pathの列、各fileのcontent Digestから決める。
Git HEAD、採取時刻、実行環境の絶対pathは含めない。

`snapshot_id`は、上記の`source_content_id`に加えて、HEAD、tool version、採取時刻を持つ監査用の観測IDである。
従って、documentationだけのcommitなどでHEADが変わっても、対象sourceの内容が同じならbaselineはfreshのままでよい。ただし、新しいObservationは残るので、どのHEADで再確認したかは追跡できる。

Baselineがfreshである条件はすべて満たすことである。

1. 再採取した`source_content_id`がBaselineの値と一致する。
2. Baselineが参照するEntry、Relation、Decision、Candidate RunのDigestが一致する。
3. 現行Policyにより`revalidation_required`となる変更がない。
4. Project Manifestから解決したreuse rootがproject外へ脱出していない。

一つでも満たさなければ`stale`または`invalid`であり、再利用判断の根拠に使わない。

## 5. new-only version規則

```text
新しい関数を発見
  └─ Candidate Runを生成
       └─ Humanが判断
            ├─ 既存entryの意味が不変
            │    └─ 新Entry（必要なら新Relation）だけを書く
            └─ 既存entryの意味が変化
                 └─ そのEntryだけ新versionを書く
                      └─ 新Baselineが全current refを束ねる
```

- entryのversionを上げるのは、責務、symbol binding、side effect、またはHuman dispositionが変わる時だけである。
- relationのversionを上げるのは、参加entry、relation kind、またはrationaleが変わる時だけである。
- 新entryの追加時は、新Entry一件、新Relation（必要な件数）、新Baseline一件だけを書く。既存EntryとRelationを複製してはならない。
- Baselineのversionは集合の変更ごとに上げる。Baselineだけが「現在使うentry/relationの集合」を決める。旧Baselineはhistoryとして残す。
- writerは既存recordを上書きしない。存在するID/version/pathへの書込み、Digest不一致、current baselineの複数化を失敗として停止する。

この規則により、関数一件の追加で処理するのは「候補抽出、必要なHuman判断、新record、Baseline参照の更新」であり、既存台帳全件の書換えではない。

## 6. Task Contractの現在と履歴の分離

旧Task Contractは内容を改竄せず残す。`active`、`fixed_pending_containing_commit`等の状態を、経過時間やGitの位置だけから自動で`historical`へ変更してはならない。

歴史的扱いへ移すには、次を満たす新しいHistorical Contract Status recordとHuman Decisionが必要である。
これは既存Contractを移動・書換えない、別identityのrecordである。

1. 対象Contractのpath、Digest、作成commitを固定する。
2. そのContractが指した作成時Policy Digestと、当時のGit provenanceを検証する。
3. Humanが`completed_historical`を承認する。
4. 現行の開始許可や安全判定に流用しないことを明記する。

現行の作業に使う`active`、再開対象、high-risk Contractは常に現行Policy Digestで検証する。security、authority、必須provenance、不可逆操作に関わるPolicy変更は、過去にHumanが承認していても`revalidation_required`とする。

これにより、古いContractを「policyを満たす現行許可」と取り違えず、同時に履歴としての検証可能性を失わない。

## 7. 一つのE2Eとして先に証明する範囲

実装を小片に分けて先へ進まない。以下を一つの受入単位にする。

1. clean sourceからSource Observation、Index、Candidate Runを`DATA_ROOT`へ機械生成する。
2. Candidate Runを根拠に、Human Decisionを作る。
3. 最初のEntryとBaselineをnew-only保存し、Digest連鎖を検証する。
4. source内容を変えずに新関数一件を対象にし、既存Entryのpath/Digestを再利用した新Baselineだけを作る。
5. artifact commit後にsourceを再採取し、同じ`source_content_id`ならfresh、HEADだけの差ではstaleにならないことを確認する。
6. 対象source内容の変更、Entry/Relationの改竄、unsafe reuse root、Candidate RunのDigest差、high-risk Policy変更をそれぞれ拒否する。
7. 実際の旧Task Contractを一件選び、Human承認なしではhistorical扱いにできず、承認済みstatusがあれば作成時根拠を検証できることを確認する。

この七項目を一つの受入test群で先にREDにし、実装中にtestの期待を緩めない。途中のIndexだけ、Ledgerだけ、履歴Contractだけを「完了」とは報告しない。

## 8. 実装とcommitの順序

1. この設計をHuman承認し、設計文書だけをcommitする。
2. Humanが承認した範囲で、旧Work 4A patch群をrevertする。historyを書き換えず、revert commitで戻す。外部`DATA_ROOT`は削除しない。
3. 上記七項目のE2E acceptance testを先に作り、REDを確認してcommitする。
4. Source Observation、Candidate Run、Ledger、Historical Contract Statusを、同じidentity chainを通す最小実装として作る。
5. unit、負例、境界、E2EをGREENにし、実装単位でcommitする。
6. 実データ一件でHuman Decisionを得て、actual artifactを生成する。
7. source再採取とDigest再照合を行い、freshness receiptを固定する。HumanがWork 4A完了を承認する。

source codeを変更するcommitとartifactを書き込むcommitは区別する。artifact commitの前後でsource再採取を行い、source content IDが同じことを機械確認する。これが「commitしたのでbaselineが古い」という誤判定を防ぐ。

## 9. revert境界と非対象

設計承認後のrevert候補は、Work 4A source index開始commit `2a23117`から、historical policy validation commit `90bc6fe`までのWork 4A patch群、および未コミットの局所Ledger変更である。実行時は対象commitを再確認し、一括resetは使わない。

次はrevert対象外である。

- Work 4A開始前のvenv、Layout Baseline、Project Manifestの確定済み基盤。
- `DATA_ROOT`にある過去の観測データ。これはGit管理外の履歴であり、今回削除しない。ただしrebuildの正本・freshness根拠には使わない。
- Work 4Aと無関係なrecords、session log、deployment機能。

## 10. 完了の判定

Work 4Aは、次のすべてがEvidenceで確認できた時だけ完了とする。

- BaselineからDecisionまで、ID/version/path/Digestの連鎖が閉じている。
- 一件の追加で既存Entry/Relationが書換え・複製されない。
- source内容IDに基づくfreshnessが、HEADだけの差と内容変更を区別する。
- Historical Contractの移行にHuman Decisionが必須で、現行許可に再利用できない。
- 正例、負例、境界例、実データ一件のE2E receiptがある。
- HumanがWork 4A完了を承認する。
