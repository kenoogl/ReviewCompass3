# 機械操作routing IssueのPlan提案 v2

状態：`approved_for_development_implementation`
対象Issue：`ISSUE-HTC-C9F6C917`
指示：`records/session-handoffs/2026-08-05-codex-to-claude-revise-machine-operation-routing-plan-v2.md`

## 実施状態注記（2026-08-05）

この節だけが提案後に追記した現在の状態である。以降の本文は提案時点のまま残しており、
全面的な時制の書き換えはしていない。

- Humanは**§3の最小縦切りだけ**を承認した。承認recordは
  `records/development/2026-08-05-machine-operation-routing-v2-approval-decision-v1.md`
  （`DEC-MACHINE-OPERATION-ROUTING-001`）である。
- 承認範囲は、versioned operation inventory、permission preflight、execution receiptの3部だけである。
  §4に挙げた後続項目（構造化argv executor、shell特殊文字対策の全面移行、cache root固定、
  既存直接shell操作の一括置換、host側tool構文、外部送信、`ISSUE-HTC-66C3E6CA`の定型record生成）は
  承認していない。
- 実装は`tools/development/operation_routing.py`として完了した。その後、execution receiptの
  改竄を拒否できない欠陥が見つかり、receipt validatorを訂正した。現在の実装は、receiptが
  **完全な検証済みpreflight recordを保存し、validatorがinventoryから必要権限を再計算して
  照合する**形であり、自己Digestを合わせ直した改竄も拒否する。execution receiptのschema versionは
  **2**である（operation inventoryとpermission preflightは1のまま）。
- 有効な完了根拠は、訂正Decision`DEC-MACHINE-OPERATION-ROUTING-RECEIPT-INTEGRITY-001`
  （`records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-correction-decision-v1.md`）と
  訂正GREEN Evidence
  `records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-green-evidence-v1.md`である。
  初回のGREEN Evidence
  `records/development/2026-08-05-machine-operation-routing-v2-green-evidence-v1.md`は、
  validatorの欠陥が判明した時点でstaleであり、履歴として残す。
- 本書は**正式なIssue Resolution PlanまたはTask Contractへ昇格していない**。
- `ISSUE-HTC-C9F6C917`のIssue recordの状態は`registered`のまま変更しない。

以下は提案時点の本文である。

**これは正式なIssue Resolution Plan、Decision、Task Contractではない。**承認していない範囲について、
argv executor、cache routing、config、policy evaluatorを変更しない。Issueは`registered`のままである。

## 0. 改訂の理由と、旧提案の扱い

旧提案`docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal.md`は次の2点で
現在のHuman承認済み方針と合わない。

1. 開発方針文書を**旧Digestで固定入力にしている**。方針文書はその後更新された。
2. Git metadataへの書込みが現れるたびに「止めてHumanへ要求する」前提で書かれている。
   Humanが承認した方針は、通常commitに個別承認を求めず、必要な権限は作業単位の開始前に
   一度だけ判定する、というものである。

旧提案は履歴として残す。上書き・削除・状態変更をしない。本書がv2として置き換わる。

### 0.1 固定入力（機械再取得したpathと現在のSHA-256）

| 種別 | path | SHA-256 |
| --- | --- | --- |
| 対象Issue | `.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json` | `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed` |
| 主triage decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-c9f6c917--v1.json` | `5b698bd0e9069128710bef161e3d60475002c89c4a4b70cce015a39c31bbf444` |
| 関連triage decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-477ea1a4--v1.json` | `9e4d76f2e791deaa8c8bfd5fbb97e2ff01aff4449828a01d439e29cac3498d78` |
| 関連triage decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-186e9b83--v1.json` | `94c102c1313f21e799df8e4bca992663238b605c561c75869a55a3024d0aff62` |
| 関連triage decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-9dce8503--v1.json` | `8088e41b42a2e59b78bcb5717c9328c6e0a0eb0f50914efb518097c65844c606` |
| 関連triage decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-a5d1bcca--v1.json` | `5f8c771d6bf70b834e759b4c960debee7279906f2673090d16534e75f218628f` |
| 開発方針 | `docs/development/2026-08-02-development-policy.md` | `0d34880353f06f50c7623282c765717348c8776938dc3113e28fdad4e9f8ac18` |
| 意味単位commit Decision | `records/development/2026-08-05-semantic-commit-minimal-guards-decision-v1.md` | `07eb9cbcd1e4e1b33aff787f597a45db1be6913a0685d76f8db1169adf965d23` |
| V4承認Decision | `records/development/2026-08-05-historical-todo-issue-intake-v4-approval-decision-v1.md` | `019879235577b39489e4383cd0fa092c562631d3c1b1e1ffa311056c8d1d9f7c` |
| V4閉鎖Evidence | `records/development/2026-08-05-historical-todo-issue-intake-v4-closure-evidence-v1.md` | `b942a9d17ea4c2818c6adb5f3ceabc0063f9b447c7ddb88ccc5baf3d1302d60e` |
| 隣接Issue | `.reviewcompass/workflow/issues-v4/issue-htc-66c3e6ca--v1.json` | `56e0911d6f565915ca0ad7737eae7befbb30d686d344eb5367ecc95598a8c732` |
| superseded proposal（旧提案） | `docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal.md` | `722e9448971bcf3e97423ab1b9b137ca202f1f1c0ed7afdd92a619738e608bfa` |

対象Issueの`problem`は次である。

> LLMがGit書込み、shell実行、ツール呼出、Python cacheの決定的な実行手順を都度文字列として組み立てている。そのため権限選択、引用、shell特殊変数、構文、書込み先で手戻りが再発する。

## 1. 解きたいことと解かないこと

### 1.1 役割の境界

LLMは、何をしたいのかという目的、対象範囲、意味の説明を担う。ここは変えない。

機械が担うのは、**決定的に決まる部分**である。

- operation inventory（その作業単位で行う操作の一覧と分類）
- argv（コマンドと引数の配列。shellの文字列ではない）
- 作業directory（cwd）
- 書込み対象の分類
- 必要な権限種別
- 一時生成物の書込み先（cache先）
- 実行receipt

これは開発方針の「入力と規則から同じ結果を再生成できる決定的処理は、LLMが文章上で手計算・手転記・
手探索せず、版付きの機械処理へ渡す」に対応する。

### 1.2 project内では解けないこと

次はこのrepositoryの外にある入力境界である。project内のrunnerを作っても解決しない。
**解決済みと書かない。**

- Codex host側の`functions.exec`に渡すJavaScriptの構文
- 外部toolのAPI schema
- sandboxまたはhostの承認そのものの決定

project内でできるのは、「どの権限種別が必要か」を機械的に出すところまでである。
その要求を承認するかどうかはhost側とHumanが決める。

### 1.3 権限に対する立場（v1からの変更点）

**sandbox／hostの承認そのものは迂回・無効化しない。** ここはv1と同じである。

変えたのは止め方である。v1は「書込みのたびに止めて要求する」形だった。v2は次にする。

- 作業単位を始める前に、機械がinventory全体を一度走査して必要な権限種別を出す。
- 必要な承認が未取得なら、**最初の書込みを一度も試さず**停止し、hostへ一回だけ要求を渡す。
- 取得済みなら、その作業単位はそのまま続行する。操作ごとに止めない。

通常のGit commitは、`DEC-SEMANTIC-COMMIT-MINIMAL-GUARDS-001`の4条件（意味的完結、明示pathのstage、
`git diff --check`と該当test／validatorの合格、post-commit read-only照合）を満たす場合、
Humanの個別承認を要求しない。**これはsandboxの権限承認を自動化・迂回する意味ではない。**
「誰がcommitの是非を決めるか」と「書込み権限が付与されているか」は別の問題であり、後者は変えない。

## 2. 共通原因と5観測の対応

5つの観測はいずれも「決定的な実行手順をLLMが都度組み立てた」ことに由来するが、足りない層が違う。

| 観測 | 何が起きたか | 足りない層 | v2の最小縦切りで扱うか |
| --- | --- | --- | --- |
| `HTC-C9F6C917` | `.git`が読み取り専用と分かっていたのに通常権限で`git add`し、一度止まった | 操作種別と必要権限の**事前判定**が無い | **扱う** |
| `HTC-477EA1A4` | compile確認が作業領域外へPython cacheを書こうとして拒否された | cache先の固定が無い | 後続 |
| `HTC-186E9B83` | 検索語のバッククォートをshellが解釈し、検索が一度失敗した | argvを構造化せずshell文字列へ埋め込んだ | 後続 |
| `HTC-9DCE8503` | zshの特殊変数`path`を使い、`shasum`が一度実行できなかった | shell文法・予約名への依存 | 後続 |
| `HTC-A5D1BCCA` | 並列tool呼出のJavaScript構文を誤記し、構文エラーが発生した | host操作の文字列組立て | **project内では解けない** |

## 3. v2の最小縦切り（推奨案）

次の**3部だけ**とする。

### 3.1 versioned operation inventory

作業単位で行う操作を、版付きの構造として先に並べる。各操作は次の分類のいずれかに割り当てる。

| 分類 | 意味 | 例 |
| --- | --- | --- |
| `read_only` | 読むだけ。何も書かない | `git status`、`git log`、file読取 |
| `project_artifact_write` | projectの成果物fileを書く | 記録fileの作成・更新 |
| `git_metadata_write` | `.git`配下のmetadataを書く | `git add`、`git commit` |
| `external` | project外へ出る | 外部送信、push |
| `unknown` | 上記のいずれとも判定できない | 未知のsubcommand |

`unknown`はfail-closedで停止する。既定で安全側へ倒し、勝手に`read_only`へ寄せない。

inventoryは版を持ち、identityとDigestで参照できる。LLMはこのinventoryを埋めるだけで、
実行文字列を書かない。

### 3.2 permission preflight

実行を始める前に、inventory全体を一度だけ走査する。

- 各操作の分類から必要な権限種別を導く。
- 必要な権限種別を**一回でまとめて**出す（操作ごとに小出しにしない）。
- 未取得の権限が一つでもあれば、書込みを**一度も試さず**停止し、hostへ一回の承認要求を渡す。
- すべて取得済みなら、preflight verdictを`granted`として作業単位を続行する。

失敗してから権限を切り替える経路は持たない。preflightは承認を与えるものではなく、
「何が要るか」を機械的に出すだけである。

### 3.3 execution receipt

inventory、preflight verdict、実行結果を一つのreceiptで結ぶ。

- inventoryのidentityとDigest
- preflightが出した必要権限種別と判定
- 実際に実行した操作と結果

inventoryとreceiptのidentityが一致しない場合は停止する。

### 3.4 なぜこの3部か

- 対象Issueの主候補`HTC-C9F6C917`が記録している恒久対策そのもの（権限の事前判定と、
  失敗後の権限切替の廃止）に一致する。
- 開発方針は権限を`high` riskに分類している。高riskの部分を最初に、狭い範囲で固定できる。
- 分類・preflight・receiptだけなので、既存の直接操作をほとんど置換せずに縦切りを一本通せる。
- 承認済みの通常commit方針と矛盾しない。commitの是非は最小4条件で決まり、権限の有無は
  preflightが別に扱う。

## 4. 最初に含めないもの（後続に残す）

- 構造化argv executor
- shell特殊文字対策の全面移行
- cache rootの固定
- 既存の直接shell操作の一括置換
- host側tool構文の解決
- 外部送信
- `ISSUE-HTC-66C3E6CA`が扱う定型recordの生成

`ISSUE-HTC-66C3E6CA`との境界は次のとおりである。重なりうるのは「receipt」という語だが、
本Issueが作るのは**実行のreceipt**（何をどう実行したか）であり、`ISSUE-HTC-66C3E6CA`が扱うのは
**記録の定型欄**（receiptの値を文書へ正しく写すこと）である。両方でreceipt生成器を別々に作らない。

## 5. 受入条件と検証方針

高riskとして扱う。**この提案では実際のTestを作らない。**必要な検証手段だけを示す。

### 条件1：操作分類を誤らない。`unknown`はfail-closed

- 正常例：`git status`／`git log`／`git diff`は`read_only`、`git add`／`git commit`は
  `git_metadata_write`、記録fileの書込みは`project_artifact_write`、pushは`external`に分類される。
- 負例：未知のGit subcommandを確認せずに`read_only`へ倒さない。`unknown`として停止する。
- 境界例：`git diff --check`のような読むだけの検査、`git stash`のように読みと書きが混ざるもの、
  同名だがoptionで意味が変わるもの。
- 検証手段：分類表に対する正例・負例・境界例のTest。分類表は版付きで保存しDigestで参照する。

### 条件2：write権限が要る操作が一件でもあれば、最初のwrite前に全必要権限を一回で列挙する

- 正常例：`git_metadata_write`が1件でもあれば、preflightがGit書込み権限を含む必要権限を
  一度にまとめて出す。
- 負例：操作ごとに小出しに要求しない。2回目以降の要求が発生しない。
- 境界例：inventoryが`read_only`だけの場合は権限要求を出さない。分類が混在する場合も一回で出す。
- 検証手段：inventoryを入力にした正例・負例Testと、要求回数を数えるTest。

### 条件3：権限が未取得ならexecutorが一度も呼ばれない

- 正常例：未取得のとき、preflightが停止し、実行関数は呼び出されない。
- 負例：試してから切り替える経路が存在しない。部分的に書いてから止まる状態を作らない。
- 境界例：作業単位の途中で初めて`git_metadata_write`が現れる場合も、開始前の走査で拾う。
- 検証手段：fault injection（権限未取得を模した入力）で、実行関数の呼出し記録が空であることを
  独立に確認する。「停止した」という報告文だけを根拠にしない。

### 条件4：最小4条件を満たす通常commitは、Human個別承認を待たない

- 正常例：意味的完結・明示pathのstage・検証合格・post-commit read-only照合を満たすcommitが、
  個別承認の待機なしに進む。
- 負例：`git add -A`や範囲外fileの一括追加、検証未実施では進めない。
- 負例：push、tag、amend、rebase、reset、force push、履歴書換え、外部送信は自律化に含めない。
- 境界例：`TODO_NEXT_SESSION.md`を含む場合は共通手順の検査も必要になる。
- 検証手段：`DEC-SEMANTIC-COMMIT-MINIMAL-GUARDS-001`の4条件を入力にした判定Test。
  権限承認の自動化と混同していないことは、条件3のTestが別に担保する。

### 条件5：inventoryとreceiptのidentityが一致しない場合は停止する

- 正常例：receiptがinventoryのidentityとDigestを持ち、両者が一致する。
- 負例：inventoryを変えたのにreceiptが古い、receiptが別のinventoryを指す場合は停止する。
- 境界例：同じ内容のinventoryが複数回実行された場合の区別。
- 検証手段：一致・不一致の両方をTestで固定する。既存のpolicy runner receiptの扱いと整合させる。

### 条件6：host側の問題を解決済みと誤報しない

- 正常例：`HTC-A5D1BCCA`はscope外として明示され、閉じたと書かれない。
- 負例：完了報告やEvidenceで「5観測すべてを解決した」と書かない。
- 検証手段：Testでは閉じられない。Evidenceのscope記述に対する独立確認（作成者以外による読み合わせ）を
  提案する。

## 6. 依存・移行・停止条件

### 6.1 既存の仕組みとの整合

- **sandbox／host承認**：現在の承認の仕組みをそのまま前提にする。置き換えない。
  preflightは要求種別を出すところまでである。
- **`.venv`**：実行環境は現在のまま使う。
- **policy runner**：公式Testの起動とreceipt生成は現在どおりpolicy runnerが担う。
  operation receiptはpolicy runnerのreceiptとは別種として扱う。
- **意味単位commit方針**：`DEC-SEMANTIC-COMMIT-MINIMAL-GUARDS-001`をそのまま前提にする。
  緩めも強めもしない。
- **V4承認範囲**：本提案の実装はV4の承認範囲に含まれない。別途Humanの承認が要る。

### 6.2 停止条件

次に達したら、その場で止めて報告する。回避策を自分で選ばない。

- 必要な権限が未取得のとき（書込みを試さず、開始前に一度だけ要求する）。
- 分類が`unknown`のとき。
- scope外のhost操作（tool構文、外部toolのAPI schema、sandbox承認そのもの）に達したとき。
- inventoryとreceiptのidentityが一致しないとき。

## 7. Human判断が必要な点（3点だけ）

1. **v2の最小縦切り（inventory＋preflight＋receiptの3部）を承認するか。**
2. **project内runnerを、既存のpolicy runnerと分けるか、統合するか。**
3. **取得済み権限の確認を、host側へどう渡すか。** project内は必要な権限種別を出すだけとし、
   取得済みかどうかの判定と承認はhost側に置く、という前提でよいか。

既存の直接操作の移行順、構造化argv executor、cache rootは後続の個別Planで決めるため、
今回の判断項目に入れない。

Humanの承認があるまで、本提案に基づく実装、RED test、runner・config・policyの変更、権限の昇格、
外部操作は行わない。
