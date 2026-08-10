# レビュー方法の整理案 レビュー結果 v1

- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：completion（Pilotの整理案に対する1周限定レビュー）
- risk：`medium`（Human指定相当）
- 対象commit：`a9e7859e995672f7646ee048b41b1d9d0a6f59cb`
- 対象：
  `records/development/2026-08-10-review-method-consolidation-v1.md`
  （SHA-256 `93d2dbb26d9c5742c2f7c1ae0dcec4d4448c1c4dddef41a40b5ee89960be6a15`）
- 共通レビュー基準：`docs/development/work-review-protocol.md`
  （SHA-256 `403491ca1c8f37abeee373ef06401610bc726361f7897611a020d7e3656c6772`）
- 役割中立mode：`docs/development/role-neutral-pilot-review-collaboration.md`
  （SHA-256 `762580c54ad830895f029d87eb1a7b1b062bf7de4ac780cfd30ae57ec508279e`）
- 関連有効性レビュー：
  `records/session-handoffs/2026-08-10-codex-review-result-rule-c-effectiveness-v1.md`
  （commit `061cb1c921a5a9bd504199744282d1d5fc31baf2`、SHA-256
  `b327d3891f93b6723db2cc3925e439048770fb9e5574f28abb4ecbcf616c781e`）
- 関連Human裁定：
  `records/development/2026-08-10-scope-prescan-rule-decision-v1.md`
  （SHA-256 `bb24ab9d046dd103462f192236b2ea057f5a77f32cd1f4e04be49518d5160174`）
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`

## 1. 総合判定

総合判定：**`reported_unverified`**。現行のレビュー方法としては確認済みにできない。

【判断】規約Cの既知限界を隠さず運用し、散文レビューの費用を1周へ制限する問題意識は妥当である。
一方、型1・型2の終了条件は現行authority（判断の正本）がrisk別に要求する確認を満たさず、型3・型4の
回数上限は既存のHuman停止・再レビュー規定と衝突する。さらに§5の生件数比較は、発生率が同じでも
対象単位数が半分なら改善と判定できる。このため、整理案をそのまま合格根拠にはできない。

Findingはblocking 3件、non-blocking 2件である。本レビューはHuman指示どおり1周で終了し、
blockingは「Pilotへ再提出を求める」という意味ではなく、Humanが採否または残余riskを判断すべき
重大事項という意味で用いる。

## 2. 観点1：§0・§2.1・§5の数値

### 2.1 §0

【実測】対象commitの親 `a9e7859^`を測定終点に固定すると、§0の分類を「`tools/`または`tests/`へ
触れるcommit」と「それ以外」に分けた場合、`106 / 23 / 83 / 8 / 0`は再現した。これは対象recordを
commitする直前の値である。

【実測】指定された対象commit `a9e7859`自身を測定終点にすると、正しい値は次のとおりだった。

| 指標 | §0記載 | `a9e7859`時点の独立再実行 |
| --- | ---: | ---: |
| 2026-08-10のcommit | 106 | **107** |
| `tools/`または`tests/`を含むcommit | 23 | **23** |
| `tools/`・`tests/`を含まないcommit | 83 | **84** |
| `431dd7b..a9e7859`のcommit | 8 | **9** |
| 上記9件のうち`tools/`・`tests/`を含むcommit | 0 | **0** |

【実測】「recordのみ」を文字どおり変更pathが`records/`配下だけのcommitと数えると、親時点は75件、
対象commit時点は76件だった。対象commit時点の残り8件は`TODO_NEXT_SESSION.md`だけのcommitである。

【判断】106・83・8は測定終点を親commitへ固定すれば再現するが、対象recordにはその終点と分類条件が
ない。「recordのみ」83件は文字どおりには再現しない。対象commit時点の値として示すべき数値は、
`107件、code/testを含む23件、records/だけ76件、TODOだけ8件`であり、RED後は9件中code/test 0件である。

### 2.2 §2.1

【実測】関連する原因分析record §2.1のscriptと§7.2の命令を独立再実行し、次を再現した。

- `tools/`配下の先頭40 moduleのうち、現在Digestが別fileにあるもの：**32件**。
- Digest計算を含むtest：**35 file**。
- その35 fileのうちpin期待値との比較条件を併せ持つもの：**12 file**。

【判断】数値自体は一致する。ただし32件と12件について、対象record §2.1には実行可能な命令がなく
コメントと値だけがあるため、対象record単体では§4の「再現commandを併記する」を満たさない。

### 2.3 §5の基準値

【実測】原因分析record §7.1の定義へ戻ると、`scope改訂commit 7`、
`範囲レビュー要修正 4`、`完了レビューblocking 3`、`実装中の停止2回・理由3件`は再現した。

【判断】基準値そのものは既存定義の下で正しい。一方、対象record §5だけからは同じ集合を一意に
再生成できない。測定可能性は観点4で判定する。

## 3. 観点2：型分けと現行authority

### 型1

【記録】`work-review-protocol.md` §3・§4.4・§5は、守り役codeを既定`high`とし、全Testに加えて
独立した判定基準、代表データ、異常注入または変異、新作反証を要求する。

【判断】整理案の「反証が拒否され、副作用が残らず、公式全Test合格」だけでは、これらを満たさない。
型1の終了条件は現行authorityより弱く、これだけで機械的に終了できない。

### 型2

【記録】現行authorityは通常codeでもriskを別軸にし、`medium`では全Test、`high`では独立した
判定基準と新作反証を加える。codeの最小確認にはRED根拠、対象Test、既存Test、必要な全Test、
静的検査がある。

【判断】「Test合格」だけでは、どのTestか、risk別確認、RED根拠、静的検査が決まらない。
型2も現行authorityの終了条件にはならない。

### 型3

【記録】`role-neutral-pilot-review-collaboration.md` §8は、`verified`以外の各結果についてHumanが
修正開始・後回し・本線復帰を判断し、承認された修正後は新しいreview requestを経て再レビューすると定める。
同§4は改訂回数の上限を置かず、`high`では合格した範囲レビューとHuman再開承認までREDを開始しない。

【判断】「改訂2回まで／3回目はHuman裁定」は、1回目・2回目の不合格にも存在するHuman判断境界を
省くように読めるうえ、3回目を回数だけで終了条件にする。既存のstop・verdict規定と衝突する。
Humanが別の方針変更として確定しない限り、現行運用へは使えない。

### 型4

【記録】今回の対象だけを1周で終えることはHumanの直接指示であり、本レビューもそれに従う。
一方、整理案は散文一般へ1周上限を広げている。現行authority §8は、不合格を直した成果を確認済みに
する場合には再レビューを求める。

【判断】今回限りの1周制と、散文一般の恒久的な終了条件は同じではない。型4一般で、未解消事項を
改善候補へ回した状態を`verified`相当に扱うなら現行authorityと衝突する。

## 4. 観点3：既知Findingとの一致

【実測】規約C項目8の行は、正例が既知の誤拒否境界へ接続されない限界を明記しており、
`RC-EFF-001`と一致する。項目10の行も、実物迂回が最低1件だけで同型変種・別型を残せる限界を
明記しており、`RC-EFF-002`と一致する。

【実測】`RC-EFF-002`が確認したW2は、現在のtool単体では「Humanが正当に指定した別repository」と
「本来の対象からのすり替え」を区別できない、という境界である。整理案は主語を外して
「原理的に判定不能」としている。

【判断】項目8・10の限界表明に過大主張はない。W2だけは、既知Evidenceが示す「現在のtool単体の限界」
より広い、あらゆる判断主体にとって不可能という主張へ拡大している。これは既知Findingの範囲を越える。

【記録】`risk low`について、意味上の定義をデータ収集まで保留するHuman裁定、実績3件、
完了レビュー済み2件中の初回要修正1件は一致する。`RC-EFF-003`が指摘したrisk別手順の既存差も、
整理案は「手順差がない」とは書いていないため、新たな不一致とはしない。

## 5. 観点4：§5指標の測定可能性

【判断】4指標は、原因分析record §7.1の定義を外部から補えば過去値を数えられる。しかし、整理案だけでは
次が一意でない。

| 指標 | 一意でない点 |
| --- | --- |
| scope改訂commit | 初版を含むか、v2以降だけか、件名以外の改訂を含むか |
| 範囲レビュー要修正 | 非`verified`のreview数か、blocking Finding数か、同じ版の再評価をどう数えるか |
| 完了レビューblocking | blockingを含むreview数か、blocking Findingの件数か |
| 実装中の停止 | scope外事由でHumanへ諮った停止だけか、レビュー停止や既知RED停止も含むか。回数と理由の同一性をどう固定するか |

【実測】基準はE/A/B/Cの4単位、比較先はC/Dの2単位で、対象単位数が異なるうえCが重複する。
単位当たり1件という同じ発生率を機械計算すると、4単位では4件、2単位では2件となり、
生件数は下がる。

【判断】したがって「同じ指標が下がれば規約が効いた」という判定は、規約に効果がなくても合格できる。
逆に、レビュー感度が上がってFindingを多く検出した場合も悪化と数え得る。4指標は作業量の観測値には
なるが、現在の定義と比較方法のままでは規約A・B・Cの有効性を一意に判定できない。

## 6. 観点5：型4を1周で打ち切る危険と便益

【判断】見逃しを恒常化させる危険はある。散文には事実、原因帰属、規範、適用範囲が混在し、1周目で
見つからなかった不一致や、1周目のFindingを反映した際に生じる新たな不一致を機械的に閉じにくい。
その散文が後続作業の前提や規約になれば、未確認の誤りが繰り返し使われる。特に「1周終了」を
「内容を確認済み」と同一視すると危険が大きい。

【判断】引き換えに得るものは、レビュー費用とHuman受け渡し回数の上限、同じ散文を巡る反復の停止、
未解消事項を明示してHumanの仕分けへ移す速さである。これは「真であることの確認」ではなく、
「ここで調査費用を打ち切り、残余の不確かさをHuman判断へ渡すこと」に価値がある。

【判断】独立意見として、1周制は費用制御としては合理性があるが、確認済みを作る終了条件としては
不十分である。Humanが次に判断すべき点は、この便益と引き換えに、型4を未確認の残余を持つまま
後続の前提へ使うriskを受容するかである。

## 7. Finding（§11区分）

### RMC-REVIEW-001 blocking／completion／§11.1類型1

【実測】型1・型2の終了条件は、現行authorityがrisk別に要求する全Test、独立した判定基準、
新作反証等を保持しない。

【判断】上流authorityより弱い条件でcodeレビューを終了できるため、類型1のblockingとする。
Humanが判断すべき事項は、この型別終了条件を現行authorityの要約として採用できるかである。
本レビューの結論は採用不可である。

### RMC-REVIEW-002 blocking／completion／§11.1類型1・2

【実測】型3はHuman裁定を3回目だけへ置くように読め、型4一般は再レビューを行わない。
現行authorityは各非`verified`結果でHuman判断を維持し、確認済みにする修正には再レビューを求める。

【判断】authorityとの矛盾とHuman境界の欠落に当たる類型1・2のblockingとする。今回の1周限定指示は
守られており、その個別指示を問題にはしない。Humanが判断すべき事項は、今回限りの打切りを散文一般の
恒久規則へ広げるか、および3回目上限を既存規則の変更として採るかである。

### RMC-REVIEW-003 blocking／completion／§11.1類型3

【実測】同じ単位当たり発生率でも、比較対象が4単位から2単位になれば生件数は4から2へ下がり、
§5の基準では効果ありと判定できる。

【判断】効果がなくても合格する反証が成立するため、検証条件の欠陥である類型3のblockingとする。
Humanが判断すべき事項は、§5の4指標を規約の有効性判定へ使えると認めるかである。本レビューの結論は、
現状では有効性の観測値としては使えても、判定根拠としては使えない、である。

### RMC-REVIEW-004 non-blocking／completion／§11.1の閉じた4類型の列挙外

【実測】§0の106・83・8は親commit時点の「code/test以外」なら再現するが、対象commit時点では
107・84・9である。「records/だけ」は76件である。

【判断】測定終点と分類名の不一致であり、類型1〜4には該当しないためnon-blockingとする。
Humanが判断すべき事項は、この数値を対象commitの実測として採用するかである。本レビューの結論は
採用不可で、正しい値は§2.1記載のとおりである。

### RMC-REVIEW-005 non-blocking／completion／§11.1の閉じた4類型の列挙外

【実測】W2の既知Evidenceは現在のtool単体の識別限界を示すが、整理案は判断主体を限定せず
「原理的に判定不能」とする。

【判断】既知Findingより広い過大主張だが、現時点で類型1〜4のblocking根拠にはならないため
non-blockingとする。Humanが判断すべき事項は、W2を現在のtoolの限界として扱うか、一般原理として
扱うかである。本レビューがEvidenceから支持できるのは前者だけである。

## 8. 独立再実行、変更範囲、未実施

【実測】対象commit `a9e7859`は対象record 1件だけを追加し、対象SHA-256は指定値と一致した。
対象commitの`git diff --check`は終了コード0だった。レビュー開始時のworktreeとindexはcleanだった。

【実測】medium相当の公式全Testは次の単独commandで実行した。

```text
.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt /private/tmp/2026-08-10-codex-review-method-consolidation-v1-full-receipt.json
```

終了コード1、status `failed`、`1470 passed / 12 failed / total 1482`、
`fallback_used=false`だった。receiptのSHA-256は
`32620a557eba3dae56f0d0780e964c22e128f06e9752a409301cf68dec9c6a4b`である。
12失敗はすべて先行RED commit `431dd7b`が追加したgroup Cの未実装testであり、対象commitは
codeとtestを変更していない。本整理案の判定はこの既知RED失敗に依存しない。

【判断】対象record、code、test、既存record、config、schema、TODO、checklistは変更していない。
外部送信、push、tag、amend、rebase、reset、不可逆操作も行っていない。本判定record 1件だけを
新規作成し、単独commitする。

未実施：対象recordの修正、規約のauthority文書への反映、実装方式または将来設計の提案、
group CのGREEN、Closer作業、TODO・checklist更新、外部操作、2周目レビュー。

次：Humanが、本recordのblocking 3件とnon-blocking 2件を改善候補として仕分け、整理案を
現行レビュー方法として採用するかを判断する。
