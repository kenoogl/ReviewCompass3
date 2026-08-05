# 機械操作routing IssueのPlan提案

状態：`awaiting_human_approval`
対象Issue：`ISSUE-HTC-C9F6C917`
指示：`records/session-handoffs/2026-08-05-codex-to-claude-design-machine-operation-routing-plan.md`

**これは正式なIssue Resolution Plan、Decision、Task Contractではない。**Humanが承認するまで、
code、test、config、policy、runnerを変更しない。Issueのstateは`registered`のままである。
本書のどの記述も、実装着手の許可にはならない。

## 0. 固定入力

本提案は次を読んで書いた。pathと実際のSHA-256を固定する。

| 種別 | path | SHA-256 |
| --- | --- | --- |
| 対象Issue | `.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json` | `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed` |
| 主decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-c9f6c917--v1.json` | `5b698bd0e9069128710bef161e3d60475002c89c4a4b70cce015a39c31bbf444` |
| 関連decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-477ea1a4--v1.json` | `9e4d76f2e791deaa8c8bfd5fbb97e2ff01aff4449828a01d439e29cac3498d78` |
| 関連decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-186e9b83--v1.json` | `94c102c1313f21e799df8e4bca992663238b605c561c75869a55a3024d0aff62` |
| 関連decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-9dce8503--v1.json` | `8088e41b42a2e59b78bcb5717c9328c6e0a0eb0f50914efb518097c65844c606` |
| 関連decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-a5d1bcca--v1.json` | `5f8c771d6bf70b834e759b4c960debee7279906f2673090d16534e75f218628f` |
| 開発方針 | `docs/development/2026-08-02-development-policy.md` | `9078276d7ba1f540495a9679a75f12f9dac0c7717fcfd637e883f41b6bf739a0` |
| V4承認Decision | `records/development/2026-08-05-historical-todo-issue-intake-v4-approval-decision-v1.md` | `019879235577b39489e4383cd0fa092c562631d3c1b1e1ffa311056c8d1d9f7c` |
| V4閉鎖Evidence | `records/development/2026-08-05-historical-todo-issue-intake-v4-closure-evidence-v1.md` | `b942a9d17ea4c2818c6adb5f3ceabc0063f9b447c7ddb88ccc5baf3d1302d60e` |
| 隣接Issue | `.reviewcompass/workflow/issues-v4/issue-htc-66c3e6ca--v1.json` | `56e0911d6f565915ca0ad7737eae7befbb30d686d344eb5367ecc95598a8c732` |

対象Issueの`problem`は次である。

> LLMがGit書込み、shell実行、ツール呼出、Python cacheの決定的な実行手順を都度文字列として組み立てている。そのため権限選択、引用、shell特殊変数、構文、書込み先で手戻りが再発する。

## 1. 解きたいことと解かないこと

### 解きたいこと

LLMは「何を確認・変更したいか」という目的、対象範囲、意味的な説明を出す。そこまでは変えない。
変えたいのは、そこから先の**決定的に決まる実行手順**を、その場の文字列組立てで作っている点である。

機械側が扱う対象として想定するのは次である。

- command spec（どの種類の操作か）
- argv（コマンドと引数の配列。shellの文字列ではない）
- 作業directory（cwd）
- 書込み対象の分類（読むだけか、成果物を書くか、Git metadataを書くか）
- 必要な権限種別
- Python cacheなど一時生成物の書込み先
- 実行receipt（何をどう実行し、結果がどうだったか）

これは開発方針の「入力と規則から同じ結果を再生成できる決定的処理は、LLMが文章上で手計算・手転記・
手探索せず、版付きの機械処理へ渡す」に対応する。

### 解かないこと

- **sandboxの承認を迂回・無効化しない。** 権限を自動的に広げる仕組みは作らない。Git metadataへの
  書込みが必要な操作なら、最初の実行の前に「この操作にはGit書込み権限が要る」と宣言・要求して
  止まるだけである。承認するかどうかは人が決める。
- **host側の入力境界を、project内のrunnerが制御できるとは主張しない。** Codex host側の
  `functions.exec`に渡すJavaScriptの構文や、外部toolのAPI schemaは、このrepositoryの外にある
  入力の作法である。project内のrunnerを作ってもこれは直らない。混同しない。
- 既存の直接shell操作を、この提案の時点で一括置換しない。移行範囲は§5で分ける。
- 記録の定型欄の生成（`ISSUE-HTC-66C3E6CA`の担当範囲）は扱わない。境界は§5に書く。

## 2. 共通原因と5観測の対応

5つの観測はいずれも「決定的な実行手順をLLMが都度組み立てた」ことに由来するが、**足りない層が違う**。

| 観測 | 何が起きたか | 足りない層 | project内で解けるか |
| --- | --- | --- | --- |
| `HTC-C9F6C917` | `.git`が読み取り専用と分かっていたのに通常権限で`git add`し、一度止まった | 操作種別と必要権限の**事前判定**が無い | 解ける |
| `HTC-477EA1A4` | compile確認が作業領域外へPython cacheを書こうとしてsandboxに拒否された | machine environmentの**書込み先固定**が無い | 解ける |
| `HTC-186E9B83` | 検索語のバッククォートをshellが解釈し、検索が一度失敗した | argvを構造化せず**shell文字列へ埋め込んだ** | 解ける |
| `HTC-9DCE8503` | zshの特殊変数`path`をループ変数に使い、`shasum`が一度実行できなかった | **shell文法・予約名への依存**そのもの | 解ける |
| `HTC-A5D1BCCA` | 並列tool呼出のJavaScript構文を誤記し、構文エラーが一度発生した | host操作の文字列組立て | **解けない**（host側の入力境界） |

上4件はproject内のrunnerで扱える。5件目はhost側であり、project runnerの直接の対象外である。
「5件すべてをproject内で閉じる」と書かないこと自体が、この提案の重要な境界である。

## 3. 候補となる最小設計

### 3.0 project内で実現できるもの／できないもの

| 実現場所 | 内容 |
| --- | --- |
| project内 | 版付きoperation spec、shell非経由の構造化argv executor、Git metadata書込みのpreflight、task専用Python cache rootの決定、post-write／receipt検証 |
| host側のみ | tool呼出のJavaScript構文、外部toolのAPI schema、sandbox承認そのもの |

### 3.1 部品の候補（すべてを一度に作る前提にしない）

- **versioned operation spec**：operation kind、argv配列、cwd、書込み分類、cache policy、receipt要求を
  持つ版付きの構造。LLMはこのspecを埋めるだけで、実行文字列を書かない。
- **構造化argv executor**：shellを経由せずargvのまま実行する。引用もshell特殊変数も介在しない。
- **Git preflight**：Git操作を「読むだけ」と「metadataを書く」に分類し、後者は最初の実行前に
  必要権限を宣言・要求して停止する。試して失敗してから権限を切り替える運用をやめる。
- **task専用cache root**：Python cacheなど一時生成物の書込み先を決定的に固定する。
- **post-write／receipt検証**：specと実行receiptのidentityが一致することを確認する。

### 3.2 最小の縦切り 3案の比較

| 案 | 範囲 | 閉じる観測 | 大きさ | 主なrisk |
| --- | --- | --- | --- | --- |
| **案A** | 最小のoperation spec ＋ Git preflight ＋ receipt | `HTC-C9F6C917` | 小 | 引用・特殊変数・cacheは残る |
| **案B** | 最小のoperation spec ＋ 構造化argv executor ＋ cache root固定 ＋ receipt | `HTC-186E9B83`、`HTC-9DCE8503`、`HTC-477EA1A4` | 中 | 権限の事前判定が入らないまま実行経路が広がる |
| **案C** | spec ＋ executor ＋ preflight ＋ cache root ＋ post-write検証を一括 | 上記4件 | 大 | 一度に作るため受入条件が増え、高riskの権限部分の検証が薄まりやすい |

### 3.3 推奨案と理由（Humanが承認するまで確定しない）

**推奨は案Aである。** 理由は次の4点である。

1. 対象Issueの主候補`HTC-C9F6C917`が記録している恒久対策そのものが、読み取り専用のGit操作と
   Git metadata書込みを機械的に振り分け、失敗後の権限切替を廃止することである。主候補の記録と
   最初の縦切りが一致する。
2. 開発方針は権限を`high` riskに分類している。高riskの部分を最初に、狭い範囲で固定するほうが、
   受入条件を具体的に書ける。
3. 5観測のうち権限だけは、正しい振る舞いが「やり直す」ではなく「**実行する前に止めて要求する**」で
   ある。この境界を先に固定しないまま汎用のexecutorを作ると、「まず実行してみる」形が実行経路に
   埋め込まれる恐れがある。
4. 範囲が小さく、既存の直接操作をほとんど置換せずに縦切りを一本通せる。

案Bは次の縦切りとして扱う。案Cは、案Aと案Bを通した後に統合として検討する。
**この推奨は提案であり、Humanが承認するまで確定しない。**

## 4. 受入条件と検証方針

権限と外部作用に触れるため高riskとして扱う。各条件について、正常例・負例・境界例と、必要な検証手段を
提案する。**この提案では実際のTestを作らない。**

### 受入条件1：Git read-onlyとGit metadata書込みを誤分類しない

- 正常例：`git status`、`git log`、`git diff`は読み取り専用に分類される。
- 正常例：`git add`、`git commit`、`git tag`はmetadata書込みに分類される。
- 負例：未知のGit subcommandを、確認せずに読み取り専用へ倒さない（既定は書込み側または停止）。
- 境界例：`git diff --check`のような読み取りだけの検査、`git stash`のように読みと書きが混ざるもの。
- 検証手段：分類表に対する正例・負例・境界例のTest。誤分類時に停止codeが出ることを負例で固定する。
  分類表そのものは版付きで保存し、Digestで参照する。

### 受入条件2：権限が必要な操作は最初の実行前に停止・要求し、sandboxを迂回しない

- 正常例：metadata書込みと分類された操作は、実行前に必要権限を宣言して停止する。
- 負例：権限が無い状態で実行を試みない。失敗してから権限を切り替える経路を持たない。
- 負例：権限を自動的に広げる、承認を省略する、代替経路で同じ書込みを行う、のいずれもしない。
- 境界例：一連の操作の途中で初めてmetadata書込みが現れる場合も、その手前で止まる。
- 検証手段：fault injection（権限が無い状態を模した入力）で、実行が試みられないことを確認する。
  実行の有無は受け渡した実行関数の呼出し記録で独立に確認する。「停止した」という報告文だけを根拠に
  しない。

### 受入条件3：引用符、backtick、shell特殊変数を含む入力がshell解釈へ流れない

- 正常例：バッククォート、`$`、`*`、空白、改行を含む検索語がそのまま引数として届く。
- 負例：argvをshell文字列へ連結する経路が存在しない。`shell=True`相当の実行を持たない。
- 境界例：引数が空文字、非ASCII、極端に長い場合。
- 検証手段：特殊文字を含む入力の正例Testと、shell経由実行が存在しないことを示す負例Test。
  実際に渡ったargvを実行側から取り出して照合する。

### 受入条件4：cache rootがproject成果物や意図しない外部rootを汚さない

- 正常例：Python cacheがtask専用のcache rootの下だけに作られる。
- 負例：projectの成果物directory、`.reviewcompass/`、`records/`、作業領域の外に書かない。
- 境界例：cache rootが未設定、読み取り専用、既に存在する場合。
- 検証手段：実行前後のfile一覧の差分を機械比較し、cache root以外に増えたfileが無いことを確認する。
  この差分確認は報告文ではなく実測で行う。

### 受入条件5：構造化specと実行receiptのidentityが一致する

- 正常例：receiptがspecのidentityとDigestを持ち、両者が一致する。
- 負例：specを書き換えたのにreceiptが古いまま、またはreceiptが別のspecを指す状態を拒否する。
- 境界例：同じ内容のspecが複数回実行された場合の区別。
- 検証手段：一致・不一致の両方をTestで固定する。既存のpolicy runner receiptの扱いと整合させる。

### 受入条件6：host側のtool構文をproject runnerで解決したと誤報しない

- 正常例：`HTC-A5D1BCCA`はscope外として明示され、閉じたと書かれない。
- 負例：完了報告やEvidenceで「5観測すべてを解決した」と書かない。
- 検証手段：これはTestでは閉じられない。閉鎖Evidenceのscope記述に対する独立確認（作成者以外による
  読み合わせ）を提案する。

## 5. 依存・移行・停止条件

### 5.1 既存の直接操作からの移行範囲

一括置換はしない。段階を分ける。

1. 新しく書くGit metadata書込み操作から、案Aの経路を使う。
2. 既存のGit操作は、read-only／metadata書込みの分類だけを先に付ける。実行経路は変えない。
3. 案Bを承認した後に、新しく書くshell実行を構造化argvへ移す。
4. 既存の直接shell操作の置換順は、案Bの受入条件が満たされた後に別途Humanが決める。

### 5.2 既存の仕組みとの整合

- **Git sandbox承認**：現在の承認の仕組みを前提として使う。置き換えない。preflightは「要求して止まる」
  までであり、承認そのものは行わない。
- **`.venv`**：Pythonの実行環境は現在のまま使う。cache rootの固定は`.venv`の構成を変えない。
- **policy runner**：公式Testの起動とreceipt生成は現在どおりpolicy runnerが担う。今回の提案は
  policy runnerを置き換えない。operation specのreceiptは、policy runnerのreceiptと別の種類として扱う。
- **V4承認の範囲**：V4は開発用・暫定の限定機能として承認されている。本提案の実装はV4の承認範囲では
  なく、別途Humanの承認が要る。

### 5.3 停止条件

次に達したら、その場で止めて報告する。回避策を自分で選ばない。

- 必要な権限が無い操作に到達したとき。
- scope外のhost操作（tool呼出構文、外部toolのAPI schema、sandbox承認そのもの）に到達したとき。
- 分類表で判定できないGit subcommandに到達したとき。
- 既存の直接操作を置換しないと先へ進めないと分かったとき。

### 5.4 `ISSUE-HTC-66C3E6CA`との境界

`ISSUE-HTC-66C3E6CA`（記録生成の根本原因）は、Evidenceやtodoの**定型欄を正しい入力から生成する**ことを
扱う。本Issueは、**機械操作の実行手順を決定的に決めて実行する**ことを扱う。

| 事柄 | 担当 |
| --- | --- |
| 固定receiptからの数値転記、見出し位置の解決、時刻の確定、監査の内訳表示 | `ISSUE-HTC-66C3E6CA` |
| 操作種別と権限の事前判定、argvの構造化、cache先の固定、実行receiptの生成 | `ISSUE-HTC-C9F6C917`（本Issue） |

重なりうるのは「receipt」という語である。本Issueが作るのは**実行のreceipt**（何をどう実行したか）で
あり、`ISSUE-HTC-66C3E6CA`が扱うのは**記録の定型欄**（receiptの値を文書へ正しく写すこと）である。
両方でreceipt生成器を別々に作らないよう、実装着手時に片方へ寄せる。この切り分けもHuman判断が要る。

## 6. Human判断が必要な点

次はいずれも本提案では決めていない。Humanが決める。

1. **最初の縦切りをどれにするか。** 案A（Git preflight先行、推奨）、案B（argv executorとcache先行）、
   案C（一括）のいずれか。
2. **project内runnerの責任範囲。** operation specをどこまで持たせるか。既存のpolicy runnerと
   統合するか、別のtoolとして分けるか。
3. **host側操作の扱い。** `HTC-A5D1BCCA`をscope外のまま置くか、別の記録として残すか。
4. **既存の直接操作の移行順。** 新規分だけに適用するか、既存分も置換するか。置換するなら順序。
5. **`ISSUE-HTC-66C3E6CA`とのreceipt責務の寄せ先。**
6. **実装に着手してよいか。** 着手する場合、Test先行の作業単位をどこで切るか。

Humanの承認があるまで、本提案に基づく実装、RED test、runner・config・policyの変更、権限の昇格、
外部操作は行わない。
