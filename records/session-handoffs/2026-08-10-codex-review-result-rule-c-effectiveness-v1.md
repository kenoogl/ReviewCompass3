# 規約C（項目8〜10）有効性レビュー結果 v1

- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：completion（Human裁定recordの有効性判定）
- risk：`medium`（Human指定）
- 対象commit：`7711999930dacf409586d0df4151f559cd26566a`
- 対象：
  `records/development/2026-08-10-scope-prescan-rule-decision-v1.md`
  （SHA-256 `bb24ab9d046dd103462f192236b2ea057f5a77f32cd1f4e04be49518d5160174`）
- 関連：
  `records/session-handoffs/2026-08-10-claude-pilot-scope-omission-cause-analysis-v1.md`
  （SHA-256 `460d08768a7820bd0e27eed6eea7f6a7347105a2dbe8d552a3ff9f2808aae06e`）
- 先行レビュー：
  `records/session-handoffs/2026-08-10-codex-review-result-scope-omission-cause-analysis-v2.md`
  （commit `90b7e2b0b626e05e407ea7407bd76b9a0af08750`、SHA-256
  `22b991f0f79fd07169f71e9abf06c411ba34b20165d68a0fda2cbb9bb08e0a93`）
- 判定基準：`docs/development/work-review-protocol.md`（SHA-256
  `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772`、
  特に§4.7・§11）
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`

## 1. 総合判定

総合判定：**条件付き**。規約C全体について、CA-V2-REVIEW-001の残余3種を
すべて防げるとは判定しない。

| 項目 | 有効性判定 | 結論 |
| --- | --- | --- |
| 項目8 | **条件付き** | 危険側・副作用不在・正例の三方向はgroup E scope v2 §5と対応する。ただし正例が既知の偽陽性境界を踏む条件がなく、形式を満たしても`SR-EG-SCOPE-003`の一部を残せる |
| 項目9 | **防げる** | scope v1/v2の宣言集合とGREEN `f8c01b5`の実変更集合を比較すると、範囲外の契約record 1件を検出できた。これはcommit作成自体ではなく、範囲適合としての誤った完了合格を防ぐ判定である |
| 項目10 | **条件付き** | 適切な実物迂回を選べばW1型を検出でき、W2型を限界として明記する方針も妥当。ただし最低1件では、実際に使った3反証すべては要求されない |

【判断】項目9は既知事象への有効性を実例で確認できた。項目8と10は見出しの存在だけを
機械確認しても内容の対応を保証せず、誤った合格が残るためblocking Finding 2件とする。
実装方式または将来設計の提案は行わない。

## 2. 項目8：SR-EG-SCOPE-003

### 2.1 実recordとの対応

【実測】group Eの範囲レビューv1 `SR-EG-SCOPE-003`は、危険入力11件の最終的な拒否だけでは、
callbackが拒否前に実行されるS1を合格させると指摘した。また、Digest由来数字列を含む安全な
入力が誤拒否されない正方向条件を要求した。

【実測】group E scope v2 §5は、次を別々の受入条件にした。

1. 危険側11件の拒否。
2. S1でcallbackが作る痕跡fileが存在しないこと。
3. 64桁hexのDigest由来数字列を含む正常payloadと、既存の正常送信経路が通ること。

完了レビュー
`records/session-handoffs/2026-08-10-codex-review-result-egress-guard-fix-v1.md`
（SHA-256 `82e95646ab23dae68f488ed04fe0c96204d97321803c7ff6dd4671b86b3d090b`）は、
痕跡fileが0件であることと、64桁hexを含む正例が通ることを一時環境で独立確認している。

【判断】項目8の三点セットは、この三方向そのものには過不足なく対応する。しかし項目8は、
正例を「具体入力を最低1件」とだけ定める。group Eで既に通る別の正常経路だけを正例に選んでも
形式確認を通り、Digest由来数字列の偽陽性は未検査のまま残せる。したがって、既知の誤拒否境界へ
正例が接続され、かつ人が列挙した観測可能な副作用が十分な場合に限って防げる。

有効性判定：**条件付き**。

### 2.2 残る限界

【記録】項目8自身が、観測できる痕跡の列挙は人が行い、列挙外の副作用は検出できないと
限界を明記している。

【判断】この限界表示は正確である。一方、機械確認は3見出しの存在だけなので、正例が既知の
偽陽性境界を踏むか、痕跡の列挙が対象処理の副作用を覆うかは機械確認されない。

## 3. 項目9：SR-EG-SCOPE-004とF-C2

【実測】group B scope v1 §6・§7とscope v2 §3・§4を合わせたGREENの宣言集合は、
実装4件、`conftest.py`、新規Evidence、receiptの計7 pathである。既存の
`records/development/2026-08-07-work5b-implementation-task-contract-v2.json`は含まれない。

【実測】`git show --stat f8c01b5`は8 pathを表示した。さらに、
`git diff-tree --no-commit-id --name-only -r f8c01b5`の集合から上記宣言集合を引く
機械照合は、次の1件だけを返し、終了コード0だった。

```text
records/development/2026-08-07-work5b-implementation-task-contract-v2.json
```

【判断】項目9の「各commitの実変更集合が宣言集合の部分集合」という確認をscope v1/v2へ
適用すれば、GREEN `f8c01b5`は不合格になり、F-C2を実際に検出できる。新規recordの確定pathと、
同じfileをslice間で再度扱う方法の明記も、group E scope v2 §6・§7が
`SR-EG-SCOPE-004`を解消した内容と一致する。

有効性判定：**防げる**。ここで防ぐ対象は、範囲外fileを含むcommitを履歴上作ること自体ではなく、
そのcommitを宣言した境界内として誤って合格させることである。宣言集合そのものが誤っている場合を
防げないという項目9の限界表示も妥当である。

## 4. 項目10：F-C1

【実測】group B完了レビューv1は、使い捨てGit repositoryで次の3反証を実行した。

- `skip-worktree`で索引表示から作業bytes差を隠す。
- 同類型の追加反証として`assume-unchanged`で隠す。
- dirtyな対象の代わりに別のclean repositoryを要求rootとして渡す。

前2件では状態表示とHEAD差分表示が空のまま完了関門が合格し、別repositoryもそのroot自身を
Git rootとして返すため合格した。既存Test 48件は全件合格しており、作り物の入力だけでは
このF-C1を検出できなかった。

【判断】項目10は、作り物だけでなく実際の仕組みを使い、一時環境で反証することを要求するため、
方向はF-C1に合う。しかし要求数は最低1件であり、型(a)〜(c)の各1件でも、既知反証の全件でもない。
したがって、項目10単独では`skip-worktree`、`assume-unchanged`、別clean repositoryの
3件すべてが要求されることにはならない。適切な索引隠蔽を1件選べばW1型は検出できるが、
別の型または同型変種を残したまま形式確認を通せる。

【実測】修正後の完了レビューv2では、索引隠蔽2種は不成立になった一方、別の正当なclean repository
そのものを要求rootとして指定した場合は合格した。tool単体では「利用者が正当に選んだ対象」と
「本来の対象からのすり替え」を区別できないというscope v3の限界と実挙動が一致した。

【判断】W2型を検出可能と過大主張せず、限界として明記する方針は妥当である。これはW2を防ぐことではなく、
保証範囲を正確に限定して誤った完了Claimを防ぐ扱いである。

有効性判定：**条件付き**。

## 5. §1の留保と§3の適用記載

【実測】§1の残余表は項目8〜10の各行に「有効性はレビュー未了」と記す。§3は
「設計しただけ」「対応済みとは書かない」と再度留保し、§5も有効性を未決事項に残している。

【判断】残余3種を解消済みとする過大主張はない。項目8と10の機械確認は見出しの存在に限られるため、
§C冒頭の「記載が欠けていれば機械的に止められる」は、欠落検出についてだけ読めば整合する。
内容の十分性まで機械判定できるとは書いていない。

【記録】§3の即時適用と全risk levelへの適用はHuman原文と一致する。文書への恒久反映を
別単位として未実施に保っており、本record内の裁定と運用文書への反映を混同していない。

## 6. §2.1 risk lowの独立照合

【実測】scope文書を機械検索すると、Humanが`low`を確定した作業単位は次の3件だった。

1. deferred #7 テストfixture共通化。
2. deferred #6 第1単位、守り役後追いレビュー対象一覧の作成。
3. deferred #6 第2単位、優先度「高」19 moduleの独立レビュー。

【実測】完了レビュー結果は、#7が`verified`、#6第1単位の初回が
`report_execution_mismatch`でblocking 1件だった。後者は9 moduleを守り役でないとした分類漏れで、
修正後のv2は`verified`である。#6第2単位にはgroup A〜Eの5判定commitがあるが、本実測時点で
この単位全体の完了レビュー結果はない。よって「実施3件、完了レビュー済み2件、うち初回要修正1件」は
再現する。

【実測】要修正となった第1単位の成果commit `4bed486`は一覧record 1件の追加だけで、codeとtestを
変更していない。Findingは非該当51件のうち9 moduleの分類漏れであり、後続の高優先度一覧の前提に
なる記録だった。したがって「失敗はcode非変更の調査記録」「誤った結論を後続前提へ残す危険」は
再現する。

【判断】ただし「`low`が何を省いてよいかの規定は存在せず、手順上の差は範囲レビューの省略だけ」
という説明は完全には再現しない。`work-review-protocol.md` §3に`low`の分類基準がない点は正しいが、
本modeで適用される`role-neutral-pilot-review-collaboration.md` §3は、`low`では実装前の範囲レビューを
要求せず、完了後は対象Testと関連validator、`medium`では実装前の簡易範囲レビューと完了後の全Test、
`high`ではさらに独立oracleと新作反証を要求すると定める。つまり意味上の分類基準は不足しているが、
省ける手順と完了oracleの差は既に一部定義されている。

【判断】母数3件から信頼性の比率を決められないこと、Human裁定どおりデータ収集後まで意味上の
`low`定義を保留することは妥当である。

## 7. 全risk levelへ課すことによる害

【実測】本レビューで、項目8〜10の全risk適用が既存成果物を壊した事象は確認していない。

【推測】一方、次の新たな負担はあり得る。

- 項目8を振る舞い変更のない調査recordにも同じ形で課すと、実質のない危険側・副作用・正例の記述が増え、
  重要な境界と形式的な記載の区別が弱くなる。
- 項目10は本文上「対象が合否を決める関門のとき」の条件付きである一方、適用範囲は全単位とするため、
  関門でない単位では適用結果の読み方が一意でない。
- 項目9の事前path固定は範囲外混入を見つけるが、調査で成果pathが後から判明する単位では
  scope改訂と確認の記述コストが増える。

【判断】これらは現時点で実害を機械実証したFindingではなく、Humanが全risk適用を選んだ裁定を
覆す根拠にはしない。ただし、追加記述がそのまま有効性になるわけではなく、項目8・10の条件付き判定を
維持する理由にはなる。

## 8. Finding（§11区分）

### RC-EFF-001 blocking／completion／§11.1類型3

【実測】項目8の機械確認は三見出しの存在で、正例は具体入力を最低1件とする。group Eで必要だった
Digest由来数字列の正例との接続は必須でない。

【判断】既知の偽陽性境界を踏まない正例でも形式上合格でき、`SR-EG-SCOPE-003`の誤った合格を残す。
受入条件・検証の欠陥である類型3のblockingとする。

### RC-EFF-002 blocking／completion／§11.1類型3

【実測】項目10は実物迂回を最低1件だけ要求し、実際に使った索引隠蔽2種と別repositoryの
全件実行を要求しない。

【判断】一つの迂回反証だけが不成立でも、同型変種または別型の誤った合格を残せる。
F-C1全体への無条件な予防策としては類型3のblockingとする。W2の限界明記自体は妥当である。

### RC-EFF-003 non-blocking／completion／§11.1類型1に関係

【実測】§2.1の「省ける手順の規定がない」「手順差は範囲レビューだけ」という記載は、適用される
role-neutral連携文書§3のrisk別手順と完全には一致しない。

【判断】関連authorityとの部分的不一致である。ただし、`low`の意味上の分類基準がないこと、
実績3件と初回要修正1件、Humanの直接裁定は維持され、項目8〜10の個別有効性を新たに止める
独立根拠ではない。§11比例原則によりnon-blockingとする。

## 9. 独立再実行、変更範囲、未実施

【実測】対象commit `7711999`は対象Decision record 1件だけを変更し、親は`6c47d35`だった。
対象・関連recordの指定SHA-256は再計算一致し、対象commitの`git diff --check`は終了コード0だった。
レビュー開始時のworktreeとindexはcleanだった。

【実測】medium riskの公式全Testは次の単独commandで実行した。

```text
.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt /private/tmp/2026-08-10-codex-rule-c-effectiveness-v1-full-receipt.json
```

終了コード1、status `failed`、`1470 passed / 12 failed / total 1482`、
`fallback_used=false`だった。receiptのSHA-256は
`18b137cca20c777af13b17a12b375074f86f3d5471909e107648b9476cf48c38`。
12失敗はすべて先行RED commit `431dd7b`が追加したgroup Cの未実装testであり、対象commitは
codeとtestを変更していない。本有効性判定の反証結果はこの既知RED失敗へ依存しない。

【判断】対象record、code、test、既存record、config、schema、TODO、checklistは変更していない。
外部送信、push、tag、amend、rebase、reset、不可逆操作も行っていない。本判定record 1件だけを
新規作成し、単独commitする。

未実施：対象Decision recordの訂正、規約の運用文書への反映、実装方式または将来設計の提案、
group CのGREEN、Closer作業、TODO・checklist更新、外部操作。

次：Humanが、項目8と10の条件付き有効性およびblocking 2件を受けて、規約Cを残余3種への
十分な予防策として扱うかを判断する。
