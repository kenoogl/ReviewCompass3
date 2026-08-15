# 一件の設計・受入条件照合 実装作業票 v2

- 作成日：2026-08-15
- 採用契約：`records/task-contract/2026-08-15-one-design-acceptance-conformance-candidate-v3.md`
- 契約SHA-256：`8d8b4a608372162c68665155ecde9c1dce8122402ab1ebea0dc40e2c621bac80`
- 採用判断：`records/development/2026-08-15-one-design-acceptance-contract-adoption-and-implementation-start-decision-v1.md`
- 採用判断SHA-256：`0287184fd38a3b47bc8630ef447c6c491b4cfad2c614692b4cdab99af8abad0d`
- supersedes：`docs/development/2026-08-15-one-design-acceptance-implementation-work-ticket-v1.md`
- v1 SHA-256：`e67bf0f286c4bbfe79edd16fcab2b2f2b30f7d196f2ea54c0c65458061b7154a`
- 訂正根拠：`records/development/2026-08-15-one-design-acceptance-implementation-start-review-v1.md`
- 訂正根拠SHA-256：`886f599af67d2b80389b95d3b06b504ab5ae7f77f27723892c3a02b177269db1`
- 実装案：案C
- 状態：`candidate_corrected_pending_limited_independent_start_review`
- 危険度：高

## 1. v2の読み方

本v2は、固定したv1の全内容を採用し、次の2箇所だけを置き換える限定訂正版である。
実装と確認では、上記SHA-256のv1と本v2を一組の作業票として使う。下記以外の目的、4境界、失敗試験、
最小実装、不変条件、条件対応、変更上限、禁止作用、停止条件、戻せる地点を変更しない。

## 2. 境界3・先行失敗試験への追加

v1 §5.2へ、次の2件を追加する。

1. 設計fileのopenだけを試験用差替えで失敗させる。終了コード2、`reason: unreadable_input`、
   `source: design`、`external_send_approved: false`だけを返し、標準エラーは空とする。
2. 受入条件fileのopenだけを試験用差替えで失敗させる。終了コード2、`reason: unreadable_input`、
   `source: acceptance`、`external_send_approved: false`だけを返し、標準エラーは空とする。

二例は実際の所有者・mode・ACLへ依存させず、境界2のfile open関数を対象fileごとに試験用差替えして決定的に起こす。
入力fileを特定できない読取失敗を`source: none`とする既存例は維持する。

`unreadable_input`を常に`source: none`へ変える欠陥処理は、上記二例の両方で失敗しなければならない。

## 3. 契約条件対応表の置換

v1 §7の条件12の行だけを次へ置き換える。

| 契約条件 | 主境界 | 失敗試験・確認 |
| ---: | --- | --- |
| 12 | 2・3 | 設計・受入条件・特定不能の読取失敗を3つのsourceへ分離し、他の停止も閉じたsource4値で示す |

条件1〜11、13〜20の行はv1から変更しない。

## 4. 限定再確認

同じ独立担当が成果物を変更せず、次だけを確認する。

1. 上記二例が、常に`source: none`へ変える欠陥を検出する。
2. 条件12が境界2と境界3へ接続される。
3. v1の他条件、4境界、変更上限、禁止作用に意味変更がない。

判定が`開始可`なら境界1へ進む。`修正要`なら製品コードへ進まない。
