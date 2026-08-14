# 立て直し計画v5 第4段 製品コード候補目録 限定訂正レビュー v1

- レビュー日：2026-08-14
- 状態：`completed`
- 対象Evidence：`records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-evidence-v1.md`
- 訂正後Evidence SHA-256：`c55367fc6b8f72f7041612cedc11d609b359909156f619fcb72e6d72bd33e72a`
- 訂正commit：`db99e057a65d0553b9876f51451f788ad4dfac1b`
- 先行レビュー：`records/development/2026-08-14-stage4-product-code-and-task-contract-input-inventory-independent-completion-review-v1.md`
- 先行レビューSHA-256：`7072027956c67534af613e7fa71aa661edb93d118cf1c01d052c742606ef03bd`
- 先行指摘：`ST4-INV-001`（依頼上の`CR-ST4-CODE-001`相当）
- 確認範囲：先行指摘の変更点だけ
- レビュー担当：先行独立完了レビューと同じサブエージェント

## 1. 判定

**`verified`**。

【実測】最初のTask Contract（作業契約）へ渡す最小入力表が追加され、必要な11項目をG25へ
対応付けた。第5段で確定する事項、未承認の上流候補、後回しにする実行機構も分けられている。

【実測】G25の環境参照は、G25自身が環境値を解決せず、呼出し側から渡された規則を使う説明へ
訂正され、実コードの呼出し関係と一致した。

【実測】訂正commitの変更は対象Evidence一件の28行追加、4行変更だけだった。コード、試験、設定、
計画、TODO、上流文書、Issueに変更はない。

【判断】先行指摘`ST4-INV-001`は解消した。先行レビューで確認済みの分類、G25の閉じた読取り範囲、
試験結果、G26反例、上流参照は変更の影響を受けていない。本確認は、それらを再実行または再レビューしない。

## 2. 最小Task Contract入力表

【実測】追加表の行を機械的に確認し、次の11項目が一度ずつ存在した。

1. Identity
2. Responsibility
3. Boundary
4. Preconditions
5. Context Obligations
6. Allowed Capabilities
7. Expected Outputs
8. Acceptance Criteria
9. Provenance Obligations
10. Escalation Policy
11. 版付きdependency

【判断】各行は「G25から固定できる入力」と「第5段で確定すること」を分けている。責務、10 pathの
境界、対応する三入力形式、必要材料、raw file読取りとメモリ上計算だけの能力、`PreparedArtifact`出力、
失敗時停止、来歴、Humanへ戻す条件、固定commitと内容識別値が対応付いた。

【判断】安定した契約ID、正式な上流要求、入力版、材料の必須・任意、出力形式、正式な合否判定、
保存期間、再試行条件等は、第5段の定義挑戦とHuman判断で確定するものとして残している。暫定候補を
正式要求へ昇格せず、第4段でTask Contractそのものを作っていない。

【実測】Boundary行はTask Contract実行基盤を範囲外とし、表の後の判断は、契約ID、schema、生成器、
状態機械、実行許可機構を作らず、G30を必須依存にしないと明記する。

【判断】この入力で、第5段においてG25の最初の契約案を定義し、未確定事項を定義挑戦へ渡せる。
未完成のG30、生成器、状態機械、許可機構は、その契約案を定義する前提になっていない。

## 3. 環境参照の訂正

【実測】`tools.session_logs.pipeline.prepare_artifact`が伏字化に使うのは、呼出し側から渡された`rules`、
`redact_text_strict`、`redaction_rules_digest`である。この呼出し経路は`resolve_environment_rules`、
`Path.home`、`socket.gethostname`へ到達しない。

【実測】環境値を解決する`resolve_environment_rules`は、別入口`redact_with_environment`から使われる。
`redaction_rules_digest_payload`は、型で環境依存規則を識別した場合に、解決値ではなく役割名を識別値の
入力へ入れる。

【判断】訂正文「G25自身は環境値を解決しない。呼出し側から渡されたpattern規則を使う」は実コードと
一致する。最小入力表も環境値解決をG25の許可能力へ含めず、呼出し側から規則を受けることを前提にした。
先行レビューで確認した報告不一致は解消した。

## 4. 変更範囲と先行確認の有効性

【実測】先行レビューcommit `69002dfd4dd04e0681c8f9eb02dadb79a033c2e5`から訂正commitまでの変更は、
対象Evidence一件だけだった。差分内容は次の二点と、節番号の繰下げだけである。

1. 環境参照一行の訂正。
2. 最小Task Contract入力表と、その表から第5段で契約案を作れるという判断の追加。

【実測】観測commit `66d608e5b5d605ddaf387bbd75a507ac934800c6`から訂正commitまで、`tools/`、
`tests/`、`setup.py`、`conftest.py`、`config/`、`pyproject.toml`に差分はない。先行レビュー記録の
SHA-256も変わっていない。

【判断】152件と192件の母集合、30群、二軸集計、G25関連55試験、G26反例、上流47参照の先行確認は
古くなっていない。本限定確認では、これらを再計算、再実行、全体再レビューしなかった。

## 5. 止める指摘と報告不一致

- 止める指摘：0件。
- 報告不一致：0件。

先行指摘と同じ原因に対する修正後確認は、本記録の一回で終了する。

## 6. 試した反証

1. 必須項目が表から漏れている：既存構想の最小核と追加項目に対応する11行がすべてあり、反証不成立。
2. G30または未完成機構が暗黙の必須依存になっている：Boundaryと表後の判断が明示的に除外し、
   版付きdependency行にもG30はなく、反証不成立。
3. G25から環境値解決へ依然到達する：対象入口の呼出し先に`resolve_environment_rules`、`Path.home`、
   `socket.gethostname`はなく、反証不成立。
4. 訂正へ分類や試験結果の変更が混入している：commit差分はEvidence一件の二点と節番号だけで、反証不成立。

## 7. 利用者判断境界

【判断】本レビューは、G25の正式製品コード採用、他142 pathの分類採用、上流候補の正式化、
最初のTask Contract、第4段完了、第5段移行を承認しない。

【判断】操縦役は、訂正後Evidence §11の五点を利用者へ提示できる。本レビューの`verified`は、
そのHuman判断を代行しない。

## 8. 未実施

【未実施】対象Evidence、先行レビュー、コード、試験、設定、計画、TODO、schema、上流文書、Issueの変更、
152件・192件・30群・上流参照の再計算、55試験・全試験の再実行、G26反例の再実行、Task Contractの
作成・承認・実装、G25の正式採用、第4段完了判断、外部送信、不可逆操作は行っていない。

本レビューでrepositoryへ追加するのは、本記録一件だけである。新しい台帳、検査器、試験、関門を
作成していない。

## 9. 次の一作業

操縦役が、訂正後Evidence §11の五つの判断点を利用者へ提示する。利用者の判断があるまで、正式採用、
Task Contract作成、第4段完了、第5段移行へ進まない。
