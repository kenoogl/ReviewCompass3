---
source_id: SRC-RC2-ISSUE-PLAN-001
captured_at: 2026-08-02
source_kind: predecessor-project-operational-path-and-failure-evidence
normative_status: predecessor-evidence
confidentiality_class: project-internal
raw_snapshot_retained: false
---

# ReviewCompass2 Issue→Plan経路とPlan品質関門の継承記録

## 1. 位置付け

ReviewCompass2で有効だった、開発中の問題をIssueへ固定し、後からPlanとして立案して
実行する経路と、そのPlan品質不足によって生じた失敗を、ReviewCompass3の再計画へ反映する
ための参照記録である。参照元を現行正本として複製せず、固定commit、Git blob、SHA-256、
観測した教訓、採用判断を保持する。

## 2. 参照元identity

- repository：`/Users/Daily/Development/ReviewCompass2`
- fixed commit：`d6bbb01500002872c713412bfbd63b702a291c99`
- 観測日：`2026-08-02`

| artifact | Git blob | SHA-256 |
|---|---|---|
| `.reviewcompass/backlog/issues/issue-2026-07-25-issue-to-plan-granularity-gate.yaml` | `5b2f04a7546976ff4a2d69f4683762006f289e21` | `366f660a8c9897c395719da69c03c4f9e6f090bd7c37fa75f0faa1c0ecb80a63` |
| `.reviewcompass/backlog/issues/issue-2026-07-25-session-log-capture-tool.yaml` | `ce4e17fa6a0a09c5a923f3b24389a8b8e0c6dcaf` | `c0901946f909274bda7b68f72a0a6cb3c08dcefe63595bfab8ad4b09c13386d6` |
| `.reviewcompass/backlog/plans/plan-2026-07-25-session-log-capture-tool.yaml` | `ebbd88f3170ce6b9e94bfc93ef492790a4552cd7` | `eaf5dfad6199ad17828c2cb128fdfc6bef0cb37f192f2f2b096788a62a4497c9` |
| `.reviewcompass/evidence/reviews/2026-07-25-plan-session-log-capture-r1.yaml` | `08b42b23c899f1bcd99c9379841b24c2b4030f7d` | `365d41172325216d4820eec0c2a27e08332e3b46d0a0a0ea885105678682a50b` |
| `.reviewcompass/evidence/reviews/2026-07-25-plan-session-log-capture-r2.yaml` | `36e25d6104eaeca25b92ada2871dc30b508ed7b0` | `71528d826e36586163b1b2e408cd9af651db32c9307c25a9d1724481ea392d5a` |
| `.reviewcompass/specs/requirements-f4.md` | `10ffc019fcdbc1c69ef4d4ca8ddf228399eccd0e` | `14d75dcf5dbafce1feb035986de35059060f8ff7fd4b0506661ed466ce7f08cf` |
| `.reviewcompass/specs/design-f4.md` | `c875a937820c7178f3d3c664f60d271b07a8d160` | `d91ab0d1fee15b7d2df8a3e76b1018997c3e988bc1465064373aa67f33666e4a` |

## 3. 有効だった経路

- Issueを問題・必要作業の発生記録とし、動機、経緯、関連ファイル、意味単位、session、
  状態を保持した。
- PlanをIssueとは別の成果物とし、対象Issueと複数の作業項目を保持した。
- checklistを別ファイルにせずPlan内へ吸収し、Issue→Plan→作業項目の境界を一つ減らした。
- IssueとPlanを案件の安定した背番号として使用し、後日の実施と証拠へ結んだ。
- 作成・完了を機械コマンドと単一状態台帳へ結ぶ要件と設計を持っていた。
- 実案件のPlanに独立reviewを二回適用し、実装前に多数の事実誤認、欠落、矛盾、
  実現不能な検査を検出した。

## 4. 観測した失敗

Issue→Plan粒度関門Issueは、過去案件で次を観測している。

- red Testだけがあり、それをgreenにする実装作業がない。
- 一部実装がred Testなしに始められる。
- 作業項目単独で合否を判定できない。
- Issueの禁止事項、対象外、停止点がPlanへの移送で失われる。
- Plan監査が実装開始permitへ結線されず、監査前に着手できる。
- 関門を別Issueへ書いても、未完了の前提依存により実装されないまま残る。

session-log-capture Planは第1版と第2版の独立reviewで全観点`要修正`となり、実データと
合わない前提、曖昧な主鍵、欠落した書込み作業、配置・機微情報の不整合、実装自身と
衝突する検査などを検出した。第3版では作業項目を赤Test参照中心へ再編し、一項目の
calibrationをred→greenとmutationで確認してから全体を進めた。

## 5. ReviewCompass3へ維持して取り込むもの

- 開発中に直ちに解消しない問題を、後日計画化できるIssue Recordとして耐久保存する。
- Issueと実施計画を分離し、一つのIssueから複数案、不採用案、改定版をたどれるようにする。
- Plan内に作業項目とIssue obligation対応を置き、外部checklistとの追加移送境界を作らない。
- Issue→Planの粒度、単独判定可能性、禁止事項保持、TDD closureをPlan Challengeで検査する。
- 機械がschema、参照、Digest、独立性、未解決blocking件数を検査し、独立評価者が意味、
  実現可能性、過不足、oracleを検査する。
- Planと固定材料のDigestが変われば旧Challenge合格をstaleにする。
- blocking FindingがあるPlanからWork Itemを開始しない。
- 最初は手作業Pilotで実演し、必要なschemaと機械関門を実物から確定する。

## 6. 修正して取り込むもの

- `open | completed`の状態欄上書きを正本にせず、Issue、Plan、Work Item、Resolution Verdictの
  identityと状態を分離し、旧versionとeventを保持する。
- `sdd | maintenance | reopen`のlaneをそのまま戻さず、現行のwork origin、continuation
  mode、Issue dispositionへ写像する。
- PlanをTask Contract CompilerのPlan bundleと同一視せず、意味的な`Issue Resolution
  Plan`と決定的な`compiled Plan bundle`へ分離する。
- review強度は一律三者にせず、通常は独立評価者一名、high riskまたは所見競合時だけ
  複数評価へ上げる。
- 第3版の`acceptance_tests`だけを作業項目に置く形式は採用しない。Task ContractとPlanに
  expected outcome、boundary、non-scope、prohibition、oracleを残し、Testを一つの実行可能な
  Evidenceとして参照する。
- Plan承認、Work Item完了、commit作成をIssue解決とみなさず、Acceptance Evidenceを持つ
  Resolution Verdictで閉じる。

## 7. 初期適用範囲

最小Review Task E2Eのstable化を妨げない。E2E後に、実在するnon-blocking Issue一件を対象に
手作業でIssue Record、Triage、Resolution Plan、独立Plan Challenge、Task Contract route、
Resolution Verdictを通す。Pilot結果を得る前にIssue管理UI、外部tracker同期、汎用的な
project-management機能を実装しない。

## 8. Evidenceの限界

参照元raw snapshotは本repositoryへ複製していない。固定commitのGit objectを取得できる間は
blobから再構成できるが、外部repositoryとobjectの双方を失った場合は原文全体を
`non_reconstructable`として扱う。Plan reviewの所見数は特定の大規模案件に依存するため、
ReviewCompass3の通常案件へ同じreviewer数、所見数、token費用を一般化しない。
