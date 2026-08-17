# RQ2 paired trial ケース正解表 v1（草案・利用者確定待ち）

- 起草日：2026-08-17
- 起草者：Claude（作業票`docs/development/2026-08-17-rq2-case-fixture-work-ticket-v1.md`）
- 上位：`records/development/2026-08-17-rq2-paired-trial-plan-v1.md`（承認済み）§1・§4
- 状態：**草案（未確定）**。計画§4-2により**利用者が確定**する。確定後に本表を版として固定し、
  実起動後の正解の事後変更は行わない（変更が必要になったら理由をrecordして別版を立てる）
- 材料：`tools/evaluation/fixtures/rq2/case-001/`〜`case-010/`（本作業でcommit）

## 1. 材料のdigest表【機械出力の転記】

`find tools/evaluation/fixtures/rq2 -name "*.md" | sort | xargs shasum -a 256` の出力そのまま。

```text
f818d2c47a7899f8c5b2788d0cee06f67b5dba6951a8885172c1d0d0724c59e2  tools/evaluation/fixtures/rq2/case-001/contract-canonical-sequence.md
2de3b0e9914ef8eb04f769384ab4f815e66c8930e90f18f6e667a1df5d7f79a4  tools/evaluation/fixtures/rq2/case-001/observation-prefix-record-shapes.md
50437d998848421bb7ae85eafc0f4c11b8ae519ea0190dbfae6488e1a58ec483  tools/evaluation/fixtures/rq2/case-002/prescan-digest-record.md
850dfcbe6aff70f1f9f54deb75bd4377001284e697e8bd0cd06bf6230e95ca95  tools/evaluation/fixtures/rq2/case-003/contract-interpretation-scope.md
b600cb2ffe48186c01b650fa41187f206f19c817f1171fad1a565dc89dd4f2ad  tools/evaluation/fixtures/rq2/case-003/procedure-result-reading.md
246f62652a5ab1390579a0f91d198a775e507048f2a8d58ebe58a97fe789e8d9  tools/evaluation/fixtures/rq2/case-004/rq1-apparatus-work-ticket.md
57145f3824b64632f536c30414be0b359f275007b964bf2b603a1f3ce61bd693  tools/evaluation/fixtures/rq2/case-005/reviewer-launch-e2e-evidence.md
e675f3aeb1a1e753f535fb9de7465de94e81c8933359acab0eeabd6f64d092eb  tools/evaluation/fixtures/rq2/case-006/reviewer-bridge-work-ticket.md
0b1c065cf94514b3d9e0da56829d84353f78066d5905458276d450c09726c579  tools/evaluation/fixtures/rq2/case-007/contract-approval-boundary.md
c0c66a692bc14fada8e6643d34984c75c1fa38b3ebd24fc640e4177770ab0404  tools/evaluation/fixtures/rq2/case-008/session-log-record-run.md
4a0ac0ce0835a811cc0657c2f2ce850b3808afd6a4c9e0b3fa252a970caae961  tools/evaluation/fixtures/rq2/case-009/product-acceptance-decision.md
a422e4e01a3ed7d17d107078bdd6755f25fd2071b36a759c59de79ddf5dfd223  tools/evaluation/fixtures/rq2/case-010/launch-metrics-work-ticket.md
```

材料の合計は12 file・35,800 byte。ケース別のbyte数：001＝2,443／002＝1,447／003＝2,684／
004＝4,577／005＝5,024／006＝5,179／007＝1,147／008＝4,220／009＝4,808／010＝4,271。

## 2. 全ケース共通の作り

- 各材料の冒頭2行は**全10ケースでbyte一致**の表示である（機械確認済み。欠陥の有無・正解の
  所在を示唆しない）。行番号は**この2行と続く空行を含めた材料file内の番号**である。
- 材料本文に複製元pathを書いていない（repository内の原本へ誘導しないため）。来歴は本表が持つ。
- 合格系（008〜010）は共通表示3行を除き複製元と**1文字も違わない**（`diff`で機械確認済み）。

## 3. ケース別の正解

### case-001（実欠陥の再構成・定義と実物の矛盾）

| 欄 | 内容 |
| --- | --- |
| 群 | 実欠陥（契約014の遡及実測1回目不合格の再構成） |
| 複製元 | `records/task-contract/2026-08-17-session-log-prefix-interpretation-candidate-v2.md`（`4dd6796d179f76fa58930108146ab1a9a007838577365d8a1a118e455c34a3b1`）の §7冒頭〜§7.2直前を抜粋。観測記録側は調査結果を材料用に1表へ整理したもの |
| 注入操作 | なし（v2の記述をそのまま使う。v2の定義自体が実物と食い違っていたのが実欠陥） |
| 期待Finding | 正準列の必須欄が`queue-operation`全体に`content`存在を課しているが、観測記録では`operation`＝`dequeue`のrecord（76件）に`content`欄が存在しない。この定義では実物の大多数が打ち切りになる |
| severity | error |
| 根拠 | `case-001/contract-canonical-sequence.md:15`（必須欄の表）と`case-001/observation-prefix-record-shapes.md:15`（dequeueの実キー） |
| 検出に必要な材料 | 2 file両方。片方だけでは検出不能 |

### case-002（実欠陥の再構成・機械出力と転記表の食い違い）

| 欄 | 内容 |
| --- | --- |
| 群 | 実欠陥（2026-08-17に実際に起きたdigest手転記ミスの再構成） |
| 複製元 | 事前走査recordのdigest固定節の形式を材料用に3件へ縮約して構成（digest値は実在fileの実値） |
| 注入操作 | §2表の3行目の値の末尾1文字を`…cdad55cb`→`…cdad55ce`へ変更（§1の機械出力は変更なし） |
| 期待Finding | 同一file`docs/development/2026-08-17-evaluation-data-acquisition-plan-v1.md`のSHA-256が、§1の機械出力と§2の表で末尾1文字違う。表の値が誤りである |
| severity | error |
| 根拠 | `case-002/prescan-digest-record.md:13`（機械出力）と同`:24`（転記表） |
| 検出に必要な材料 | 1 file内で完結（SHA-256の再計算は不要） |
| 設計の断り | 計画§1の原案は「実fileと1文字違うdigestを混入」だったが、**LLMはSHA-256を計算できない**ため、file実体との照合による検出は原理的に不可能である。実欠陥の検出可能な本質は「機械出力と転記の食い違い」であり、その形へ改めた（事前走査v1 §4） |

### case-003（実欠陥の再構成・旧仕様の残置）

| 欄 | 内容 |
| --- | --- |
| 群 | 実欠陥（契約014の実装後・手順書改定前に実在した状態の再構成） |
| 複製元 | 手順書側＝commit `0d3c992`時点の`docs/development/prompts/session-log-record-run.md`（当時のfile digest `e1a25223df1b3bc58749940150b6c4a79cda20e83b04cc20f20700d723b57893`）の§2。契約側＝候補v2の§7.3〜§7.4直後まで |
| 注入操作 | なし（当時の版をそのまま使う） |
| 期待Finding | 手順書が「解釈非対応＝先頭recordが本文形式でないfile」と定義しているが、契約は前置recordを無issueでスキップし本文へ到達できるfileを処理対象とする。手順書の定義は契約の定めと矛盾する（旧仕様の残置） |
| severity | error |
| 根拠 | `case-003/procedure-result-reading.md:12`（非対応の定義）と`case-003/contract-interpretation-scope.md:8`（無issueスキップ）・同`:17`（本文へ到達できるfileは補助でない） |
| 検出に必要な材料 | 2 file両方 |
| 副次の可検出点 | 手順書が改善候補を「Human仕分け待ち」と書いているのに契約が既に存在する点（severity＝warning。検出されなくても不合格としない） |

### case-004（人工欠陥・受入条件の脱落）

| 欄 | 内容 |
| --- | --- |
| 群 | 人工（Basili分類の omission＝脱落） |
| 複製元 | `docs/development/2026-08-17-rq1-apparatus-work-ticket-v1.md`（`cce799197ae88c48f3591a0dfafd00f9924c9076772633f90b58d7717e039873`） |
| 注入操作 | §5受入条件の第4項「初回計測の実施」（2行）を削除し、旧第5項を第4項へ繰り上げ |
| 期待Finding | §6手続きの第5段「初回計測→Evidence転記」と§2の主成果物（指標JSON）に対応する受入条件が存在しない。成果物の検証段が受入条件から欠落している |
| severity | error |
| 根拠 | `case-004/rq1-apparatus-work-ticket.md:52-55`（受入条件の全4項）と同`:64`（手続き第5段） |
| 検出に必要な材料 | 1 file内で完結 |

### case-005（人工欠陥・誤事実）

| 欄 | 内容 |
| --- | --- |
| 群 | 人工（Basili分類の incorrect fact＝誤事実） |
| 複製元 | `records/development/2026-08-17-reviewer-launch-e2e-attempt7-success-evidence-v1.md`（`eca7ae8f534a467e4e16bf094416bc742aeebd85231558c2fca98033e6b15711`） |
| 注入操作 | 2点。(a) §1の「単独commit（`e87d9f60`。」を`e87d9f68`へ変更。(b) §2の「読取り7件」を「読取り9件」へ変更 |
| 期待Finding | 2件。(a) §1本文のcommit `e87d9f68`が、同じ§1に貼られた機械出力JSONの`record_commit` `e87d9f60c357…`と食い違う。(b) 「読取り9件」と書きながら続く列挙は7件（依頼record・試験1・module 3・operations 1・実装Evidence 1）である |
| severity | (a) error／(b) error |
| 根拠 | `case-005/reviewer-launch-e2e-evidence.md:17`（機械出力JSON）・同`:20`（本文のcommit）・同`:31`（件数と列挙） |
| 検出に必要な材料 | 1 file内で完結 |
| 採点 | 2件のうち**いずれか1件の検出で「検出」と数える**。両方の検出は加点しない（recallの分母はケース単位） |

### case-006（人工欠陥・範囲の不整合）

| 欄 | 内容 |
| --- | --- |
| 群 | 人工（inconsistency＝節間の矛盾） |
| 複製元 | `docs/development/2026-08-17-reviewer-bridge-work-ticket-v1.md`（`c3ac8e5a09fba51cb230dc7246181661929d05753b2aeca1f96fe26490d3ddec`） |
| 注入操作 | §7範囲外へ1行追加：「判定recordのfindingsを`finding_set`形式へ変換する部品（順序4の実験装置で扱う）。」 |
| 期待Finding | 同一の成果物（判定findingsのfinding_set変換）が§2正本範囲の(b)と§7範囲外の双方に置かれており、範囲の定義が自己矛盾している |
| severity | error |
| 根拠 | `case-006/reviewer-bridge-work-ticket.md:26`（正本範囲(b)）と同`:76`（範囲外の追加行） |
| 検出に必要な材料 | 1 file内で完結 |

### case-007（人工欠陥・承認境界の曖昧化）

| 欄 | 内容 |
| --- | --- |
| 群 | 人工（ambiguity＝曖昧） |
| 複製元 | 候補v2の§1〜§2（`4dd6796d…5c34a3b1`）を抜粋 |
| 注入操作 | §2の4項目を、承認の**主体と時点を特定しない**表現へ全面的に書き換え（「関係者間で適宜合意」「必要に応じて承認を得る」「状況に応じて適切な時点で」「担当者が判断する」） |
| 期待Finding | 「Human承認境界」と題しながら、誰が・いつ承認するのかが1項目も特定できない。承認の有無を後から判定できず、境界として機能しない |
| severity | warning |
| 根拠 | `case-007/contract-approval-boundary.md:16-19`（§2の4項目） |
| 検出に必要な材料 | 1 file内で完結 |

### case-008〜case-010（合格系・期待Finding 0件）

| ケース | 複製元 | 複製元digest |
| --- | --- | --- |
| case-008 | `docs/development/prompts/session-log-record-run.md` | `9c1808fdbb8c730d4d3f843a76dfce8f202260e2870e385f37eae557f48b834d` |
| case-009 | `records/development/2026-08-17-session-log-prefix-interpretation-product-acceptance-decision-v1.md` | `759154984591f0479c505e4a2d01d6a86e2d9fd3a2c584b1187eb22f067e3a35` |
| case-010 | `docs/development/2026-08-17-launch-metrics-recoverability-work-ticket-v1.md` | `3db49c0b74a581507d4076d06c7b1730308434b65893871695583de6bd40c2c7` |

いずれも受入済み・commit済みの現行文書の無改変複製である。**期待Findingは0件**であり、
severity `error`または`warning`のFindingが出た場合は誤検出として数える（§4の判定基準による）。

## 4. Findingの採点基準

| 区分 | 定義 |
| --- | --- |
| **検出（true positive）** | 期待Findingと同じ欠陥を指しているFinding。表現の一致は問わず、**欠陥の所在（材料file）と内容の要旨が一致**すれば検出とする |
| **誤検出（false positive）** | severityが`error`または`warning`で、期待Findingのいずれとも対応しないFinding |
| **責務外（out of scope）** | 材料の内容の妥当性ではなく、材料の外側（複製元の存在・repository構成・実験そのもの）を論じるFinding。誤検出とは別に数える |
| **非加算** | severity `info`で、内容が表現の好みや軽微な体裁に留まるFinding |

- 採点は**ケース単位**（1ケースにつき検出0または1）。case-005のように期待Findingが複数ある
  ケースは、いずれか1件の検出で検出とする。
- 採点はまずClaudeが機械変換後のfinding_setに対して行い、**判定の境界例は利用者が裁定**する。

### 抜粋に由来する指摘の扱い（全ケース共通）

case-001・case-003・case-007の材料は元文書からの抜粋であり、次の性質を**構造上必ず持つ**。
これらを指す指摘は**責務外**として数え、誤検出には数えない。

- 材料の中に存在しない節への参照が残る（例：「§7.1と同一の共有定義」「事前走査record §1」
  「§5.1-3の6 file一覧」）。
- 見出しの階層が抜粋の切り口で飛ぶ（`#`の直下に`###`が来る等）。
- 冒頭の題名（「# 契約候補（抜粋）：…」）は元文書には無く、材料の組み立て時に付けたものである。

合格系（008〜010）は抜粋ではなく全文の複製であり、この扱いは適用しない。

## 5. 既知の限界と交絡（正直な記載）

1. **材料が実験用複製であることを明かしている**：共通表示に「評価実験で使う複製材料」と書いて
   ある（実recordとの取り違えを防ぐための計画§1の要求）。reviewerは自分が試験されていることを
   知りうる。全ケースで同一文言のため**ケース間の識別には使えない**が、レビューの慎重さ全体に
   影響する可能性は排除できない。
2. **ケース間の内容の重なり**：材料はいずれも同一projectの文書群から採っているため、あるケースの
   材料が別ケースの背景を含みうる。確認した重なりは次のとおり。
   - case-009（合格系・契約014受入判断）は「手順書§2改定」に言及する。case-003の**答そのものでは
     ないが背景の示唆**になる。
   - case-004（RQ1作業票）とcase-005（契約010 E2E Evidence）は同じ`records/development/`圏の
     文書だが、互いの期待Findingには触れていない。
   - 起草の途中で、契約014実装Evidenceを使うとcase-001の答（dequeueに`content`が無いこと）を
     平文で含むことが判明したため、**case-005の出典を契約010のE2E Evidenceへ差し替えた**。
   - **帰結**：条件C（無関係資料の追加）で「他ケース材料」を混ぜると、この重なりが検出率へ
     交絡する。§6の論点3を参照。
3. **reviewerはrepository配下を読める**：起動promptは対象repository内の読取りを許している
   （事前走査v1 §1-2）。本表がrepository作業treeにある状態で実起動すると、正解が読まれうる。
   §6の論点2を参照。
4. **規模**：10ケースはpilot study規模であり、統計的優位性は主張しない（計画§6のとおり）。

## 6. 実験計画v1への是正提案（利用者の裁定が要る3点）

| # | 対象 | 現状（計画v1） | 推奨 |
| --- | --- | --- | --- |
| 1 | 測定量 | §2「依頼recordの材料選択・prompt bytesが不変」 | **prompt bytesを取り下げ**、`material_bundle`の件数・内訳の不変性＋**reviewerの実入力トークン**（raw応答から機械抽出）へ差し替える。起動promptは固定形式で材料本文を含まないため、prompt bytesは条件B／Cを区別できない（事前走査v1 §1-1） |
| 2 | 正解表の配置 | §4「確定recordをcommitしてから実起動」 | **事前登録（pre-registration）形**：正解の本体はrepo外私有領域へ置き、repoには本表のSHA-256を封じたrecordだけを実起動前にcommitする。実験後に本体をcommitしてdigest照合する。汚染の遮断と事後変更の否定を同時に満たす |
| 3 | 条件Cの資料 | §2「他ケース材料＋汎用文書」 | **他ケース材料を外し、どのケースの期待Findingにも触れない文書だけの独立プール**にする（§5-2の交絡を断つ）。上位案として、実験専用の作業treeを作り材料と依頼recordだけを置けば、§5-3の汚染も同時に解消できる |

論点1・3は装置実装（後続2）の前に、論点2は実起動（後続3）の前に確定が要る。**本表の確定
（計画§4-2）とは別の判断**である。

## 7. 未実施

- 本表の**利用者確定**（計画§4-2。見積り1時間弱）。
- paired evaluation装置の実装・実起動バッチ・RQ2集計（後続2〜4）。
