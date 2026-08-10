# 骨太方針3件と核の候補一覧 レビュー結果 v1

- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：completion（Pilot提案recordの事実、測定設計、authority整合の評価）
- risk：`medium`（Human指定相当）
- 対象：`records/development/2026-08-10-trusted-core-policy-proposal-v1.md`
  （commit `98e123a979e679ae3ceffd6e2be1333065c72a0f`、SHA-256
  `f48168652d22430d80c289420e9aac4362ffc3807c386b2274fd79f863cd7947`）
- 1周制：本recordでレビューを終了する。`blocking`は修正往復の要求ではなく、
  **Humanが採否またはauthorityの扱いを判断すべき重大事項**を表す。
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`

## 1. 総合判定

総合判定：**`report_execution_mismatch`**。この判定は、報告と実状態の不一致を意味する。
骨太方針の採否と核の選定を本recordでは行わない。

【実測】対象commitとSHA-256は指定値に一致し、対象commitの変更pathは対象record 1件だけだった。
開始時のbranchは`main`、HEADは`98e123a`、worktreeとindexはcleanだった。

【実測】対象record §3.2〜§3.4の推移逆依存26値を、対象commitの全133 moduleから独立に
再計算したところ、10値が一致しなかった。また、§3.2の`source_kind.py`は守り役「−」だが、
先行Human裁定は守り役該当と確定している。これらを、`work-review-protocol.md` §4.7・§11.1が
要求する競合Evidenceとする。

【判断】方針1の障害注入は、現状の定義では「核が周辺の誤りを検出した」ことを示さない失敗まで
検出数へ数えられる。方針1・2の一部は現行レビューauthorityと衝突し、方針3は残68件の
Human保留を自動解除する読みを排除していない。したがって、このrecordをそのまま方針採用または
核選定の根拠にはできない。1周制に従い、次の扱いは§6の一つのHuman仕分けへ渡す。

## 2. 5観点の逐一照合

### 2.1 観点1：§3の数値

#### 推移逆依存

【実測】独立計算は、`tools/`配下の`__init__.py`を除く全Python fileをmoduleとし、Pythonの
抽象構文木からmodule内の全`import`・`from ... import ...`を抽出した。既存の`tools` moduleへ
解決できる辺だけでgraphを作り、あるmoduleを直接または間接にimportするmoduleの集合を求め、
起点自身を除いた。終了コードは0、入力は133 moduleだった。

【実測】不一致だった10値と、同じ定義による正しい値は次のとおりである。ここにない16値は一致した。

| module | 対象record | 独立再計算 |
| --- | ---: | ---: |
| `tools/common/errors.py` | 24 | **27** |
| `tools/session_logs/redaction.py` | 18 | **19** |
| `tools/common/digests.py` | 18 | **23** |
| `tools/session_logs/parse_claude.py` | 14 | **15** |
| `tools/common/paths.py` | 11 | **12** |
| `tools/session_logs/preservation.py` | 6 | **7** |
| `tools/session_logs/eventual_preservation.py` | 0 | **1** |
| `tools/development/policy_test_runner.py` | 0 | **3** |
| `tools/development/pytest_summary.py` | 0 | **5** |
| `tools/development/todo_handoff.py` | 1 | **2** |

【実測】したがって§3.4の判定器群の範囲は「0〜3」ではなく**0〜5**である。
依存集中と影響の重大さが別軸だという定性的な説明は、この訂正後も成立する。

【実測】同じ順位付けでは、§3.2の最小表示値8以上であるのに同表へ出ていないmoduleが7件ある。
`parse_codex.py` 11、`parse_codex_rollout.py` 11、`common/output.py` 9、`session_logs/config.py` 9、
`session_logs/locking.py` 9、`bootstrap/closed_payload.py` 8、`session_logs/discovery.py` 8である。

【判断】§3.1には実際に使ったscript、版、Digest、command、import解決規則、表示行の選別規則がない。
そのため、Pilotが別のimport定義を使った可能性を排除できず、対象record自身の「再現可能」という
主張も満たさない。上の値は、曖昧さを除くために本レビューで固定した定義による値である。

#### 守り役件数

【実測】inventory v1 §4の表だけを機械抽出すると、該当91・非該当42・合計133は再現した。
ただし、同日10:23のHuman裁定
`records/development/2026-08-10-guard-backfill-priority-decision-v1.md`は、暫定非該当3件を
該当へ確定し、現行値を**該当94・非該当39・合計133**とした。同裁定はinventory v1を
snapshotとして保持し、自身を差分の正と明記している。

【実測】対象record §3.2の`tools/session_logs/source_kind.py`は「−」だが、Human裁定では
守り役該当・低・保留である。したがって、現在の判断材料としては「○」が正しい。

【判断】91・42・133は古いsnapshotの再現値としては正しいが、現行authorityを表す値ではない。
核以外の守り役数を考える場合も、現在の母数は91ではなく94である。

### 2.2 観点2：3方針の測定可能性

#### 方針1

【判断】「障害注入という方法を使える」こと自体は妥当だが、§2の実験設計では方針1の主張を
検証できない。次の三つの抜けにより、「検出できたこと」にできる。

1. 公式全Testのどれかが失敗しただけでも、核が誤りを検出したことにできる。注入先module自身の
   単体Test、構文error、import errorが失敗しても、核による検出ではない。公式runnerが核に含まれ、
   Test失敗を受け取って失敗する場合は、同じ信号を二度数えるだけである。
2. 失敗理由を照合しない。`review-method-consolidation-v1.md` §2.2が記録した
   `F-CG-COMP-001`では、狙った欠陥ではなくDigest不一致という別理由でTestが失敗し、
   一度は検出成功として扱われた。同じ誤判定を本設計でも排除できない。
3. 注入集合と分母の決め方がない。既にTestで捕まる欠陥だけを選ぶ、実行されない変異や同値変異を
   結果を見て分母から外す、同じ型だけを重ねる、といった選別でM/Nを高くできる。

【判断】主張を測るには、少なくとも、基準状態では全Testと核が合格すること、注入集合・乱数seed・
除外規則を結果を見る前に固定すること、独立oracleで各注入が禁止挙動を実際に生むことを確認すること、
核の検査を公式全Testと分離すること、狙った理由かつ必要なside effectより前に核が拒否した場合だけ
検出へ数えることが必要である。これは実装指示ではなく、Humanが方針1の安全性根拠を採用する際の
判断条件である。

#### 方針2

【実測】列挙された5 IDは、数値の単位または値の不一致を扱うFindingとして既存review recordに
存在する。件数そのものは数えられる。

【判断】しかし、「数値誤りFindingが0件」は、散文から数値を移した実施量を観測する指標であり、
方針の正しさを単独では検証しない。レビュー件数が減った、Finding分類が変わった、誤ったreceiptを
検証しなかった場合にも0になる。期間、対象record数、数値Claim数、receipt検証結果、
`report_execution_mismatch`件数を固定しなければ比較の分母も一意でない。

【判断】数値・Digest・件数を機械生成receiptへ置く部分は現行の責務分離と整合する。一方、
「散文のレビュー規則も不要になる」は、散文に残る方針、authority整合、Human境界、因果説明を
検査対象外にするため、現行authorityとは整合しない。

#### 方針3

【判断】「費用の方針であり、安全性の検証ではない」という限界表示は妥当である。ただし、
「触れないコードは壊れない」は一般には成立しない。依存先、実行環境、入力、呼出し側だけが変わっても、
触れていないmoduleの欠陥は顕在化する。

【判断】待ち行列68件を記録から消せば件数は0になるため、「68→0」だけでは改善を示さない。
Humanが68件を保留義務として維持するのか、既知riskとして受容して閉じるのかを先に決め、
触れた件数とは別に、未処理・顕在化欠陥・変更後の流出を観測する必要がある。

### 2.3 観点3：既存authorityとの整合

#### 方針1

【記録】`work-review-protocol.md` §3は、守り役codeを一律に既定`high`とする。
`role-neutral-pilot-review-collaboration.md` §3もこの規則を維持し、`high`に全Test、独立oracle、
Pilot fixtureにない反証を要求する。

【判断】方針1を「核以外の守り役はこの既定`high`から緩和する」と読む限り、現行authorityと矛盾する。
「周辺も通常のrisk分類に従い、守り役なら引き続き`high`」と読めば矛盾しないが、その場合は
対象recordが意図する緩和は成立しない。どちらにするかはHumanの方針変更判断が必要である。

#### 方針2

【記録】`work-review-protocol.md` §5は文書の最小oracleとして、diff、再読込み、参照解決、
authorityとの意味整合を要求する。

【判断】機械化できる値をreceiptへ移すことは整合するが、散文レビュー自体を不要にする部分は矛盾する。
Humanが採る場合は、削れるのは決定的な値の手照合だけで、意味整合とHuman境界のレビューは残る、
という適用範囲の判断が必要である。

#### 方針3

【記録】`guard-backfill-priority-decision-v1.md`は、高19件だけを実施し、中51・低17の計68件は
「別途Human裁定があるまで実施しない」と確定した。

【判断】高19件だけを一括実施した既往は、将来の一括後追いをやめる方針と両立できる。
しかし、残68件について「触れたら自動的に後追いレビューを開始する」と読むとHuman保留を解除し、
先行Decisionと矛盾する。現行Decisionを維持するなら、触れた変更自体への通常レビューは行っても、
後追いレビューの開始は別途Human裁定まで保留である。方針3でこのDecisionを置き換えるのか、
この解釈で併存させるのかをHumanが決める必要がある。

### 2.4 観点4：核以外の守り役を緩める新たな危険

【判断】独立した見解として、主な危険は次の四つである。これは核の選定ではなく、緩和判断の材料である。

1. **核へ届く前の誤った合格**：周辺の守り役が不正なartifactやreceiptを正しい形へ見せ、核がその出力を
   前提として信頼すると、核には検出材料が届かない。
2. **核を通らない経路**：import graphはcode依存を示すだけで、全実行経路が核を必ず通ることを示さない。
   単独CLI、移行用入口、外部送信、復旧経路から周辺の守り役が直接使われれば、核の検出を迂回できる。
3. **検出が遅すぎる経路**：外部送信、上書き、保全喪失などは、核が後段で異常を見つけてもside effectを
   取り消せない。検出率だけでなく、side effectより前に拒否したかが必要である。
4. **共通原因による同時故障**：周辺と核が同じDigest関数、identity解釈、設定または誤ったfixtureを共有すると、
   一つの誤りで両方が同じ誤判定をする。個別moduleへの単発注入ではこの同時故障を捉えにくい。

【判断】したがって、核以外を緩める安全性は「核の検出率」だけでは決まらない。核を必ず先に通ること、
核が周辺と独立した根拠を持つこと、不可逆なside effectの前で拒否すること、核を通らない経路を
別に扱うことが判断材料になる。

### 2.5 観点5：§0の棲み分け

【実測】Pilotは、どの行を核とするか、上位何件を核とするかを記していない。
明示的な核の選定はHuman境界に残されている。

【実測】一方、§3.1にはscriptやreceiptがなく、26値中10値が独立再計算と不一致だった。
また、同じ順位で表示対象となる値8以上の7 moduleが説明なく省かれ、現行Human裁定で守り役となった
`source_kind.py`も非該当表示のままである。§2のFinding 5件も、IDは列挙されるが機械生成receiptはない。

【判断】「Pilotが核を選定しない」は守られている。しかし、「機械処理が候補集合、数値、件数を
再現可能に決める」は守られたと確認できない。候補の意味的な三分類をLLMが説明することは許容範囲だが、
機械順位からどの行を表示するかという決定的な選別には、機械規則と出力が必要である。

## 3. Finding（§11区分）

### TC-POLICY-001 blocking／completion／§11.1類型3

【記録】方針1の実験は、公式全Testと核の検査が失敗した件数をMへ入れるが、失敗理由、核単独の信号、
変異の到達、分母の事前固定を要求しない。`review-method-consolidation-v1.md` §2.2には、
狙いと別のDigest不一致で失敗したTestを成功扱いした実例がある。

【判断】核が検出していない欠陥を検出済みにできるため、誤った合格を残す検証欠陥である。
Humanは、現設計を方針1の安全性根拠として**棄却する**か、§2.2に示した判断条件を持つ別実験を
後続作業として認めるかを判断する必要がある。

### TC-POLICY-002 blocking／completion／§11.1類型1

【記録】現行authorityは全守り役codeを既定`high`とし、safety・authority・Acceptanceへ影響する
risk受容と再開をHuman判断に残す。

【判断】核以外の守り役を緩和する方針1は、この既定を維持する限り矛盾する。Humanは、
現行`high`を維持して方針1の緩和を採らないか、残余riskを受容したauthority改定を別途行うかを
判断する必要がある。

### TC-POLICY-003 blocking／completion／§11.1類型1

【記録】現行authorityは文書についてもauthorityとの意味整合とHuman境界の確認を要求する。

【判断】方針2のうち「散文のレビュー規則も不要になる」はこの規則と矛盾する。Humanは、
方針2を決定的な値の機械化に限定し意味レビューを残すか、現行レビューauthorityを改定するかを
判断する必要がある。

### TC-POLICY-004 blocking／completion／§11.1類型1

【記録】先行Human裁定は残68件を別途Human裁定まで実施しないと固定した。

【判断】方針3を「触れたら自動開始」とする読みは、この保留とHuman境界に矛盾する。
Humanは、残68件の保留を維持するか、方針3により先行Decisionを置き換えるかを判断する必要がある。

### TC-POLICY-005 blocking／completion／§11.1類型1

【実測】対象recordは91・42を現在の守り役集計として用い、`source_kind.py`を非該当表示した。
先行Human裁定の正は94・39で、同moduleを該当とする。

【判断】核選定の判断材料が現行authorityと競合する。Humanは、選定時に対象recordの守り役列と
91件母数を使わず、先行Decisionを反映した94件母数を使う必要がある。

### TC-POLICY-006 non-blocking／completion／§11.1の閉じた4類型の列挙外

【実測】推移逆依存10値は独立再計算と一致せず、実script・版・Digest・command・選別規則もない。

【判断】これは`report_execution_mismatch`の競合Evidenceであり、候補一覧の再現性を損なう。
数値不一致だけでは§11.1のblocking 4類型に入らないためnon-blockingとする。ただしHumanは、
本recordの数値ではなく§2.1の訂正値と明示した計算定義を判断材料にする必要がある。

## 4. 独立再実行と事後状態

【実測】medium riskの公式全Testは次の単独commandで実行した。

```text
.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt /private/tmp/2026-08-10-codex-trusted-core-policy-review-full-receipt-v1.json
```

【実測】終了コード1、`1470 passed / 12 failed / total 1482`、status `failed`、
`fallback_used=false`だった。receiptのSHA-256は
`1099f934572e9ab09ef138fb4741acacedd80b5d2cd342fb3607a2e049915fb9`である。
12失敗はすべて既存RED commit `431dd7b`が追加したgroup Cの未実装Testであり、対象commit
`98e123a`はcode・testを変更していない。本レビューの数値不一致または方針判定の原因としては扱わない。

【実測】本レビューでは対象record、code、test、既存record、config、schema、TODO、checklistを
変更していない。外部送信、push、tag、amend、rebase、reset、履歴書換えも行っていない。

## 5. 未実施

- 【記録】核の選定はHuman担当のため実施していない。
- 【記録】3方針の採否、現行authorityの改定、残68件の保留解除は実施していない。
- 【記録】Pilotによる2周目の修正と再レビューは、Human指定の1周制により実施しない。
- 【記録】障害注入の実Runは、核が未選定であり実験契約も未確定のため実施していない。

## 6. 次のHuman判断

【判断】次の一判断は、TC-POLICY-001〜005と独立見解を一括して、3方針を
**現行authorityの範囲へ限定して採る／authority改定とrisk受容を伴って採る／採らない**の
いずれとして扱うかを仕分けることである。その際、核の候補を選ぶなら、91件母数と対象recordの
推移逆依存値ではなく、現行94件母数と§2.1の訂正値を判断材料にする。
