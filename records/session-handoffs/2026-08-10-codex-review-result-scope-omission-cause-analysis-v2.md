# Pilot範囲漏れ原因分析 再レビュー結果 v2

- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：completion（Pilot自己申告の原因分析と規約の訂正再レビュー）
- risk：`medium`（Human指定）
- 対象commit：`416c9360af3a2105b6e9f67b564b8667161137c3`（親commit
  `ca747c11a01264fd4accf47f46f51c1d4c370935`）
- 対象：
  - `records/session-handoffs/2026-08-10-claude-pilot-scope-omission-cause-analysis-v1.md`
    （SHA-256 `6ffeb208147d1c17859cd87f23d03e1f4c9c575627b89b1f6f8745722a8fcd51`）
  - `records/development/2026-08-10-scope-prescan-rule-decision-v1.md`
    （SHA-256 `1c47244ce12cfba8c2208d143ea6b3f6daec11bd2b3e785e8c38e141b49e7e87`）
- 先行レビュー：
  `records/session-handoffs/2026-08-10-codex-review-result-scope-omission-cause-analysis-v1.md`
  （commit `ca747c1`、SHA-256
  `34733ff54840f1d050904f74f863659a09c6e059cce0adf2dc384d150a4ddeec`）
- 関連Human裁定：2026-08-10「分析と規約を指摘どおり修正せよ。
  5手順は『巻き添え防止』に限定し、検査の正しさは別項目として立てよ」
- 判定基準：`docs/development/work-review-protocol.md`（SHA-256
  `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772`、
  特に§4.7・§11）
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`

## 1. 判定

判定：**要修正（`report_execution_mismatch`）**。`verified`ではない。

`report_execution_mismatch`は、報告内容とリポジトリの実状態が競合する
判定である。本再レビューでは、次の競合を機械照合で確認した。

1. 規約AとBの分離、および「Aを実行してもBの事象は検出できない」
   という明記は確認できた。しかし、Bの2項目は、Bが防ぐとした
   `SR-EG-SCOPE-003`・`004`とgroup Bの`F-C1`を実際に検査する内容に
   なっていない。
2. 原因分析§7.1の4指標は、scope改訂commit 7、範囲レビュー要修正4、
   完了レビューblocking 3までは再現した。一方、「Human停止3回」は、
   group Bの1回の停止に2理由を数えており、回数としては2回、理由数として3件である。
3. 原因分析§7.2の35 fileは再現したが、その35 fileを記載された第2条件で
   絞ると12 fileであり、23 fileではない。23は第2条件だけを`tests/`
   全体へ掛けた件数である。
4. §7冒頭は§4を置換対象に含めていないのに、§7.3は§4も共同寄与へ
   改めるとしている。そのため、旧§4の「Pilotの手順不足が主因」と§7.3の
   「どちらか一方を主因とは判定しない」が同時に残る。

【判断】上の1と4は、先行blockingの解消とHuman裁定への適合を止める。
2と3は訂正後の実測Claimと独立再実行の結果が競合する。
したがって§4.7の`report_execution_mismatch`とする。

## 2. Finding（§11区分）

### CA-V2-REVIEW-001 blocking／completion／§11.1類型3・4

【実測】規約Bの第6項は、REDが狙った理由で失敗したかを確認するため、
group Aの`F-CG-COMP-001`を扱う。第7項は上流authority（判断の正本）と
Human承認順序を検査するため、`SR-EG-SCOPE-001`・`002`を扱う。

【記録】`SR-EG-SCOPE-003`は、最後に拒否するだけではなく、拒否前の副作用が
無いことと、安全な入力を誤拒否しないことを機械条件に求めた。
`SR-EG-SCOPE-004`は変更可能pathだけでなく、新規Evidence・receipt・依頼記録の
確定pathと2つのGREEN間のcommit境界を求めた。group Bの`F-C1`は、
Gitの非表示指定と別repositoryによる完了関門の偽陰性だった。

【判断】第6項と第7項のいずれも、拒否前の副作用・安全側の正例、
意味単位commitの境界、または完了関門の実入力による迂回を検査対象に
していない。それにもかかわらず、裁定recordはBが上記3種を防ぐとしている。
既知の「誤った合格」とscope・commit境界の残余であり、§11.1類型3・4の
blockingとする。実装方式や将来設計は指定しない。

### CA-V2-REVIEW-002 blocking／completion／§11.1類型1

【実測】原因分析§7冒頭は「本節が§1・§2.1・§3・§5を再置換する」とし、
§4を含めない。一方、§7.3は見出しと本文で§4の原因帰属も共同寄与へ
改めるとしている。

【判断】§7.3の実質的な文章は、先行レビューの「どちらか一方を主因と
判定できない」と一致し、Pilotの過度な自己批判にも自己弁護にもなっていない。
しかし、置換範囲の明記上は旧§4が残り、Humanの「分析を指摘どおり修正」と
矛盾する。上流authorityとの矛盾である§11.1類型1のblockingとする。

### CA-V2-REVIEW-003 non-blocking／completion／§11.1の閉じた4類型の列挙外

【実測】§7.1の指標aはE:2・A:1・B:2・C:2の計7commitで再現した。
指標bはegress v1、common v1、position v1、position v2の4レビューで再現した。
指標cは`F-CG-COMP-001`の1件と`F-C1`・`F-C2`の2件、計3件で再現した。

【記録】group Bのscope v2は「停止した理由」として1回の停止に
`conftest.py`結線と既存test契約更新の2理由を並べる。group CはRED
`431dd7b`の後に範囲外のCRLF実処理が判明し、GREEN commitを作らず停止している。

【判断】停止の回数はgroup Bとgroup Cの2回、停止理由は3件である。
さらに「GREEN着手後」を厳密な定義にすると、group CはGitでRED後までしか
固定されておらず、GREEN着手自体の独立Evidenceはない。したがって指標dの
「Human停止3回」はどちらの読みでも再現しない。この数値不一致自体は
§11.1の4類型には該当しないためnon-blockingとする。

### CA-V2-REVIEW-004 non-blocking／completion／§11.1の閉じた4類型の列挙外

【実測】§7.2の第1命令は終了コード0、35 fileを列挙した。その35 fileの各々に
第2条件 `assert.*==.*expected\|_PINS\|immutable_record\|fixed_sources`を掛けると
12 fileだった。第2条件だけを`tests/`全体へ掛けると23 fileになった。

【判断】「そのうち」と23 fileとする記載は、記載された二段階条件では
再現しない。旧16は選別条件がないため、撤回自体は妥当である。
しかし、裁定record§2にはなお「16 file存在する」が残り、同record§6と
原因分析§7.2の撤回と競合する。数値の再現性の問題であり、§11.1の
4類型には該当しないためnon-blockingとする。

### CA-V2-REVIEW-005 non-blocking／completion／§11.1の閉じた4類型の列挙外

【実測】原因分析§7.4は、group Aのpin、group Bの`conftest.py`と契約pin、
group CのCRLF所在を「指標bのうち巻き添え型」とする。しかし、指標bは
範囲レビュー要修正回数であり、group Bの2件とgroup Cの1件は指標dの
停止理由である。
また、裁定record§2には旧「8回・4回」も残っている。

【判断】§7が§1・§2.1・§3・§5を置き換える構成の中で、新指標の参照先と
裁定recordの根拠数値が整合していない。判定を新たに止める独立の類型1〜4の
証拠ではないためnon-blockingとするが、訂正版の内部不一致である。

## 3. v1 Finding 4件の解消可否

| v1 Finding | 判定 | 根拠 |
| --- | --- | --- |
| `CA-REVIEW-001` | **未解消** | A・Bの分離と限界明記は成立したが、Bが防ぐとした`SR-EG-SCOPE-003`・`004`、group B `F-C1`が2項目の検査対象に入っていない |
| `CA-REVIEW-002` | **一部解消** | 7・4・3は再現した。停止3回は再現せず、正しい区別は停止2回・理由3件 |
| `CA-REVIEW-003` | **未解消** | 35は再現し、16の撤回は妥当。しかし記載条件の交差は23でなく12。裁定record§2に16も残る |
| `CA-REVIEW-004` | **一部解消** | §7.3の共同寄与の内容は先行v1と一致し中立。ただし§7の置換宣言が§4を含まず、旧§4のPilot単独主因説が残る |

## 4. 独立再実行と変更範囲

【実測】対象2 fileのSHA-256はHuman指定値と2／2で一致した。
`416c936` の変更pathはその2 fileだけである。レビュー開始時の
worktreeとindexはcleanだった。

【実測】Digest密度は原因分析記載のscriptを単独実行し、終了コード0、
32／40を再現した。test fileは第1条件35、第1と第2の交差12、
第2条件だけで23だった。

【実測】medium riskの全Testは次の単独commandで実行した。

```text
.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt /private/tmp/2026-08-10-codex-scope-omission-cause-analysis-v2-full-receipt.json
```

終了コード1、`1470 passed / 12 failed / total 1482`、status `failed`、
`fallback_used=false`だった。receiptのSHA-256は
`f3abab24fdd14bb12b82f0ad18159575d775b965fb13a91e843ce4ea476a4de2`である。
12失敗はすべてgroup CのRED commit `431dd7b`が追加した未実装testであり、
訂正commit `416c936`がcodeまたはtestを壊した結果ではない。

【判断】本レビューでは対象record、code、test、既存record、config、schema、
TODO、checklistを変更しない。外部送信、push、tag、amend、rebase、reset、
不可逆操作も行わない。本判定record 1件だけを新規作成し、単独commitする。

## 5. Human境界、未実施、次

Human境界：恒久規約化の裁定自体は変更しない。本レビューは、
訂正文の再現性と既知事象の被覆だけを判定する。

未実施：対象recordの再訂正、規約の文書反映、group CのGREEN、Closer作業、
TODO・checklist更新、外部操作。

次：Humanが本判定を受け、上記blocking 2件と数値・置換の不一致をPilotへ
再訂正させるかを判断する。
