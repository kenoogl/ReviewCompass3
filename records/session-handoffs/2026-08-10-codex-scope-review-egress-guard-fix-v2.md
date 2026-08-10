# group E 外部送信・機微境界修正 範囲レビュー結果 v2

- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：scope（実装前の範囲レビュー再実施）
- risk：`high`（Reviewer判断。Human確定前）
- 判定：`verified`
- 実行状態：`correctly_stopped_before_RED`
- Finding：blocking 0件、non-blocking 0件、defer 0件
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`

## 1. 固定対象と開始状態

- 対象：
  `records/session-handoffs/2026-08-10-claude-pilot-egress-guard-fix-scope-v2.md`
- 対象SHA-256：`74602a90b8d0f6009d1d742237deff13ff895d763568e06799eac9bbb2e5125b`
- 対象commit：`4b527763c55dd321b27fb9842401c8c2864034a3`
- base：`928997fbcf1a2ccd315feca00962dd4c26a38d68`
- branch：`main`
- 先行レビュー：
  `records/session-handoffs/2026-08-10-codex-scope-review-egress-guard-fix-v1.md`
  （commit `928997f`、要修正・blocking 4件）
- 許可範囲：本判定record 1件の新規作成と単独commit、読取り、決定的な照合
- 禁止範囲：対象scope、code、test、既存record、config、schema、TODO、checklistの変更、
  RED開始、実際の外部送信、push、履歴書換え

【実測】対象commitの親は申告baseと一致し、変更pathは対象scope v2 1件の追加だけだった。
レビュー開始時のworktreeとindexはcleanだった。対象commitの`git diff --check`は終了コード0だった。

【実測】本recordの予定pathに対する`git check-ignore --no-index`は終了コード1、作成前の
`test ! -e`は終了コード0だった。

【実測】scope v2に固定された7入力のSHA-256を内容から再計算し、7／7で記載値と一致した。

| 固定入力 | 再計算したSHA-256 |
| --- | --- |
| 修正順序の裁定 | `f69f8a969e732072514a44f684c7b216687e9d63cf2d4af9d280d2ea16f15997` |
| group E判定record | `a4bc656cdfe73188b1def7bc107a98a1027daf289dc3b6ab254b9808d3c86a33` |
| 範囲レビューv1 | `bbb45c0222f14d98eafaf73514dd4ccf1fbff6d931bb8c08d39e8206c9b1e928` |
| slice 1上流：出口設計v4 | `3a82b3973f8abc947782c4bbf8e2d54713043e8e8591a543089a5824c57bcacd` |
| slice 2上流：Session Log保全設計 | `b387b9cf913b11a0d39e13cbd5aa6222527fdb4f801e478f1110683c3dd8d1fe` |
| 共通レビュー基準 | `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772` |
| 現在位置 | `ce66c9f374319105f3c86558d910054151b79d1671a6352b80a9b661c827b137` |

## 2. v1 Findingの逐一照合

### SR-EG-SCOPE-001：解消

【実測】scope v2 §3は、F-E1〜F-E5のslice 1を出口設計v4へ、F-E6・F-E7のslice 2を
Session Log保全設計へ分け、両上流のrepository-relative pathとSHA-256を固定した。§4も
「各sliceの上流への適合」と記し、出口設計v4をslice 2へ及ぼしていない。

【記録】出口設計v4 §2〜§8は、送信payload、Human承認record、送信前関門、秘密値走査、
承認済み閾値、段階1の送信不能を定める。Session Log保全設計 §3、§5.3、§8、§10は、
追記専用raw、integrity ledger（完全性台帳）の不一致時停止、許可root境界を定める。

【判断】sliceごとの実際の上流authorityとDigestが固定され、v1で指摘した一括authorityの矛盾は
解消した。分類は§11.1類型1の解消確認である。

### SR-EG-SCOPE-002：解消

【実測】scope v2 §8-3は、§9の承認を得ないままRED-1へ着手することを停止条件にした。
§9はrisk `high`の確定と着手承認に加え、資格情報3形式と64桁hexの誤検出除外規則を
RED-1開始前のHuman確認事項として列挙し、未承認の間はRED-1へ着手しないと明記した。

【判断】F-E3の方針値をtestへ固定する前にHuman承認を要求しており、GREEN前だけに存在した
順序の穴は閉じた。分類は§11.1類型2の解消確認である。

### SR-EG-SCOPE-003：解消

【実測】scope v2 §5は、危険側11件の拒否に加えて、拒否時の副作用不在を独立した受入条件にした。
S1系ではcallbackが作る痕跡fileの不在をtestで固定し、停止前実行を合格させない。また、
64桁hexのDigest由来数字列を含む正常payloadと既存の正常経路を正例に置き、誤拒否も検出する。

【判断】拒否結果だけでなく拒否前の副作用と、秘密値走査の偽陽性を機械判定できる。
安全側と危険側の両方向が受入条件に入り、v1で実証した誤った合格を許す欠陥は解消した。
分類は§11.1類型3の解消確認である。

### SR-EG-SCOPE-004：解消

【実測】scope v2 §6はSCOPE、RED-1、GREEN-1、RED-2、GREEN-2、review requestの6 commitを
分け、REDの変更fileをワイルドカードなしで列挙した。§7は実装6 file、test 6 file、
Evidence 1件、slice別receipt 2件、review request 1件をrepository-relative pathで一意に列挙した。

【実測】GREEN-1はEvidenceを新規作成し、GREEN-2は同一Evidenceへslice 2節を追記する。
receiptはsliceごとに別pathであり、review requestも別の新規pathである。`test_egress_dry_run.py`は
変更対象でなく回帰実行だけの対象であることも§6に明記された。

【判断】§6のcommit表と§7の完全path一覧を合わせれば、各commitの変更可能pathと、2つのGREEN間で
Evidence・receiptをどう扱うかを一意に解決できる。v1のワイルドカード不一致と未固定pathは解消した。
分類は§11.1類型4の解消確認である。

## 3. 新たな境界欠陥の確認

【判断】上流authorityとの新たな矛盾はない。F-E1〜F-E5は出口設計v4の送信関門へ、F-E6・F-E7は
Session Log保全設計のRaw Archive・完全性台帳・許可root境界へ収まり、新しい送信段階、payload種別、
保存schema、方針値をscope内で確定していない。

【判断】Human境界の新たな欠落はない。risk `high`、F-E3の2つの意味的裁定、RED-1再開はHumanへ残り、
RED後のtest変更もHuman承認を要する。上流矛盾、許可path外変更、設計変更の必要が判明した場合も停止する。

【判断】誤った合格を許す新たな受入条件はない。危険側11件の拒否、副作用不在、Digest由来数字列と
既存正常経路の正例、対象testと公式全Test、段階1の送信不能を組み合わせて判定する方向は妥当である。
具体的なfixture、例外型、callbackの実現方法は完了レビューで確認する実装詳細であり、本レビューでは
裁定しない。

【判断】scope境界の新たな破れはない。変更可能pathはgroup Eの6 module、対応test、slice別Evidence、
receipt、review requestに閉じ、他group、config、schema、上流設計、TODO、checklistを除外している。

## 4. Finding（§11）

### blocking

【判断】0件。§11.1類型1〜4に該当する未解消事項はない。

### non-blocking／defer

【判断】0件。§11.2の範囲段階を越える実装方式や細部設計には立ち入らず、v1で挙げなかった論点を
後出ししていない。

## 5. 判定と次

判定：`verified`

【判断】scope v2は、v1のblocking 4件をすべて解消した。対象commitはscope文書1件だけで、
申告base、固定入力、Digest、変更範囲、停止地点と一致する。risk `high`の実装前scopeとして、
上流整合、Human境界、受入条件の方向、変更可能path、commit境界は妥当である。

Human境界：維持。risk `high`の確定、F-E3の資格情報3形式と64桁hex除外規則の承認、
RED-1開始の明示的な再開承認は未実施であり、Humanに残る。本`verified`判定だけではREDを開始できない。

未実施：対象scope、code、test、既存record、config、schema、TODO、checklistの変更、RED、GREEN、
実際の外部送信、完了レビュー、Closer作業、push、履歴書換え。

次：Humanがrisk `high`、F-E3の2項目、RED-1開始の再開を明示承認するか判断する。
