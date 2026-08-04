# Work 4A Routine Ledger Representative Review Scope Proposal v1

- Proposal ID：`PROP-WORK4A-ROUTINE-LEDGER-REVIEW-SCOPE-2026-08-04-V1`
- status：`proposed / Human decision required`
- fixed Snapshot：`4f01c7f2b0f6b8df03fa360e9aedb3639d972a890a80bbca5fd48b07b28213d7`
- fixed candidate list：`DATA_ROOT/routine-classification-candidates/4f01c7f2b0f6b8df03fa360e9aedb3639d972a890a80bbca5fd48b07b28213d7/routine-classification-candidates-v1.json`
- candidate list SHA-256：`19cb5030a61da25570432ebbf90d255f7a7d9dde7612692f02d6412aac0bb63a`

## 1. 現在の事実

機械出力は144件である。内訳はpublic 48、shared 23、high-risk 53、duplicate candidate 20であり、
dynamic attribute lookupは6件を未解決として明示した。retired candidateは0件である。

これは候補一覧であって、routineの責務、統合可否、公開契約、retirement、Ledger登録を確定しない。
とくに同一bodyの`main`や短い検証helperは、同じ実装であっても統合すべきとは限らない。

## 2. Human確認用の代表sample

| 観点 | symbol | 機械的事実 | Human確認すること | この時点の結論 |
| --- | --- | --- | --- | --- |
| public / shared | `tools.bootstrap.material_bundle.calculate_bundle_digest` | 3 moduleからstatic import | 安定した共通APIか、入力・出力とdigest規則をLedger化すべきか | candidateのまま |
| public / shared | `tools.bootstrap.review_contract.materialize_review_contract` | 2 moduleからstatic import | review contractをmaterializeする責務と互換性境界 | candidateのまま |
| high-risk | `tools.development.bootstrap_environment.bootstrap_environment` | filesystem write | write先、失敗時、独立verification、owner | candidateのまま |
| duplicate | `tools.bootstrap.closed_payload._material_document` と `tools.bootstrap.material_bundle._material_document` | normalized bodyとsignatureが同一 | 共通化する価値か、各moduleへ意図的に局所化するか | mergeしない |
| unresolved | 6件のdynamic attribute lookup | 静的参照へ解決不能 | external／dynamic consumerの有無を確認する必要 | retired根拠に使わない |

## 3. Reusable Routine Ledgerの最小record境界案

Ledger entryはcandidate一件ではなく、Humanが責務を確認した「一つの再利用可能なroutine責務」を単位にする。
最初のbaselineでは全666 symbolや144 candidateを一括登録せず、上表のpublic/shared/high-riskから承認された
routineだけを登録する。duplicateは個別entryを自動作成せず、Humanが`merge | intentional_separation`を裁定した後に
relationとして結線する。

各entryに最低限必要なfieldは次のとおりである。

- record identity：`ledger_entry_id`、version、Digest、status、Decision reference
- source binding：Snapshot ID、symbol ID、source path、source content Digest
- meaning：Human確認済みの責務、入力、出力、side effect、constraint
- reuse：consumer、alias、類似／duplicate relation、`reuse | extend | merge | split_with_rationale`のHuman disposition
- lifecycle：`active | retired`、successor、統廃合履歴

配置案は`records/inventories/reusable-routine-ledger/`とし、directory名だけで正本性を決めない。各recordの
ID・version・Digest・Decision referenceで正本性を定める。entryを一括更新する巨大な単一fileにはせず、entryと
relationを個別recordにする。index／coverage projectionは派生物として再生成可能にする。

## 4. 先に解消すべきcoverage gap

Work 4A checkboxはcross-contract候補の抽出も要求する。しかし現行extractorはそのrule、evidence、Test、出力を
持たない。これは0件ではなく未測定であるため、`IC-WORK4A-CROSS-CONTRACT-CLASSIFICATION-GAP-001`として記録した。

推奨は、Ledger schemaや登録を始める前に、cross-contractの最小境界をHumanが承認し、RED／GREENとfresh actual
captureを完了することである。Humanが明示的にdeferを選ぶ場合だけ、authorityとWork 4A完了条件を整合してから
Ledger登録範囲へ進む。

## 5. Human判断依頼

1. cross-contractをWork 4Aの最小ruleとして追加するか、authority改定のうえdeferするか。
2. 上表の4 routine／relationを最初のLedger representative review対象としてよいか。
3. Ledgerの個別record方式と`records/inventories/reusable-routine-ledger/`配置案を採用するか。

この提案だけではLedger schema、entry、routine disposition、Work 4A完了を確定しない。
