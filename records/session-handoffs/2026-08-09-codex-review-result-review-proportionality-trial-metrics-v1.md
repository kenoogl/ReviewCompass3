# レビュー比例原則・初回試行計測 独立レビュー結果 v1

- review date：2026-08-09
- Reviewer：Codex
- verdict：`要修正`
- Finding：P1×1、P2×2

## 1. 対象

- 比例原則追加：`2c3a998b550146067dc548a4e189df8f7df97335`
- 初回試行計測record追加：`011ca81f199256e62c4bd6d4447723b0853806cb`

## 2. 確認結果

- Human承認済みの歯止め5点は、`work-review-protocol.md` §11.1〜§11.5に網羅されている。
- 既存のレビュー順序と§5のoracle本文は変更されていない。ただしFinding P1-001のとおり、
  停止系判定の意味には既存条文との矛盾が生じている。
- §11.2・§11.5は範囲レビュー過剰判定の再評価と、§11.3はRR-P1-001から
  RR-P1-004へ反証が別周回になった実例と整合する。
- 計測recordのFinding 4件、修正commit 4件、全Test 1334→1337→1338、scope修正1回、
  同日完了はGit履歴・review resultと一致する。
- 両対象commitの`git diff --check`は終了コード0だった。

## 3. Findings

### P1-001：§11.1が既存の停止判定基準と矛盾する

`work-review-protocol.md` §4.7・§6は、Evidence不足を`reported_unverified`、報告と事後状態の
不一致を`report_execution_mismatch`とする。一方、§11.1は4類型のblocking Findingを1件以上
列挙できる場合だけ両判定を許すため、Evidence不足だけが判明した場合に適用可能な判定が競合する。
「§4の順序と§5のoracleを変えない」という宣言を満たすよう、両停止状態と4類型の関係を修正する必要がある。

### P2-001：範囲段階の停止判定回数が履歴と一致しない

計測recordは範囲段階を1回としているが、scope review v1とv2はいずれも
`reported_unverified`だった。v2は後の再評価で`verified`へ訂正されたが、周回コストの発生回数は
「範囲2回（うち1回は再評価で訂正）」である。

### P2-002：Human event回数を内訳から再現できない

承認・裁定5回に対し、備考はmode宣言、Closer確定、分割案1、RED再開、Finding修正承認2回の
6項目に読める。同一eventとして集約した項目を明記する必要がある。handoff約11回についても、
再評価を含めたevent単位の内訳または根拠recordへの参照が必要である。

## 4. 結論

5点の規約化と過去実例への接続は確認できたが、P1-001により既存判定基準が不変とは確認できず、
計測recordにも履歴との不一致と再現条件不足がある。3件を修正するまで`verified`にしない。
