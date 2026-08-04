# Work 4A Reusable Routine Ledger Structure Proposal v2

- Proposal ID：`PROP-WORK4A-REUSABLE-ROUTINE-LEDGER-STRUCTURE-2026-08-04-V2`
- status：`proposed / Human schema approval required`
- supersedes：`PROP-WORK4A-ROUTINE-LEDGER-REVIEW-SCOPE-2026-08-04-V1`の配置案だけ
- authority：`.reviewcompass/project-manifest.json`の`artifact_roots.reuse`
- fixed source Snapshot：`1815b653533d0bde34093f30be0e0cb7894ae2518d1568e1acb7343568d44e24`

## 1. 配置と正本性

Ledgerの候補rootは`.reviewcompass/reuse/reusable-routine-ledger/`とする。これはProject Manifestが
`reuse` artifact rootとして`.reviewcompass/reuse`を指定しているためである。`records/inventories/...`は
候補rootにしない。

ただしdirectoryだけでは正本性を定めない。baseline manifest、entry、relationの各recordにID、version、
canonical content Digest、参照するDecisionを持たせ、baseline manifestが採用entryとrelationをDigest付きで
列挙する。したがって未参照のfileや古いversionは、存在だけでcurrent Ledgerにならない。

## 2. 個別record方式

```text
.reviewcompass/reuse/reusable-routine-ledger/
  ledger-baseline--v1.json
  entries/
    rrl-<stable-id>--v1.json
  relations/
    rrl-rel-<stable-id>--v1.json
```

- `ledger-baseline--v1.json`：固定Snapshot、entry／relation ref、coverage、Human Decision refを束縛する。
- `entries/`：一つのHuman確認済み再利用責務を一recordにする。candidate一件やsymbol全件を自動登録しない。
- `relations/`：duplicate、alias、successor、intentional separationなど、複数entry／symbolの関係を一recordにする。
- derived index／coverage projection：baseline manifestとentryから機械再生成する。正本として手編集しない。

## 3. 最小schema案

すべてのrecordは`record_kind`、stable ID、version、`content_digest`を持つ。baseline manifestにはさらに
`source_snapshot_id`、candidate list Digest、entry／relation ref、coverage、Decision refを必須とする。

entryには、symbol ID、source content Digest、Human確認済みの責務、入力、出力、side effect、constraint、
consumer、lifecycle（`active | retired`）、reuse disposition、Decision refを持たせる。`retired`にはsuccessor
またはHumanの明示理由を必須とする。relationにはrelation kind、participant、rationale、Decision refを持たせる。

candidate status、動的参照未解決、静的解析だけのduplicateはentryを作る十分条件にしない。

## 4. 実装時のAcceptance境界

1. Manifestの`reuse` root外へLedger recordを書こうとすると拒否する。
2. entry／relation／baselineのID、version、Digest、参照Digestの不整合を拒否する。
3. baseline manifestが列挙しないentryをcurrent Ledgerとして扱わない。
4. `retired`、`merge`、`split_with_rationale`、source Snapshot不一致を負例で拒否する。
5. Ledger artifact追加に伴い、reuse rootのProject Artifact Snapshot expectationと関連Testを同じ作業単位で更新する。

実装はRED Acceptance Testから始める。Ledger entryの実データ作成、routine disposition、Work 4A完了判定は
schema GREENとHuman確認の後である。

## 5. Human判断依頼

1. `.reviewcompass/reuse/reusable-routine-ledger/`をLedger rootとして採用するか。
2. baseline manifest・entry・relationの個別record方式を採用するか。
3. 上記の必須fieldとAcceptance境界をLedger schemaのRED入力として採用するか。
