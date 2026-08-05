# 定型記録生成 IssueのPlan提案

状態：`awaiting_human_approval`
対象Issue：`ISSUE-HTC-66C3E6CA`
指示：`records/session-handoffs/2026-08-05-codex-to-claude-design-record-generation-issue-plan.md`

**これは正式なIssue Resolution Plan、Decision、Task Contractではない。**Humanが承認するまで、
定型記録生成、TODO renderer、receipt parser、監査集計を実装しない。RED testも作らない。
既存recordの書換え、Git操作、外部送信も行わない。`ISSUE-HTC-66C3E6CA`のstateは`registered`のままである。

## 0. 固定入力（作成時の実値）

| 種別 | path | SHA-256 |
| --- | --- | --- |
| 対象Issue | `.reviewcompass/workflow/issues-v4/issue-htc-66c3e6ca--v1.json` | `56e0911d6f565915ca0ad7737eae7befbb30d686d344eb5367ecc95598a8c732` |
| Human triage decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-66c3e6ca--v1.json` | `bb2cfbb618f5b1ee918018a1ae4ae78d74a25eccb26a7cd46e07685571c31e5f` |
| 現行TODO手順 | `docs/development/prompts/todo-handoff-update.md` | `eff64878479ce82a48f8e5b4160dd7913364268c9e94d1a6f0a63087e7fb0f4d` |
| 現行TODO renderer | `tools/development/todo_handoff_projection.py` | `e43982c5c3f0e7930e21995c380d81b998515acd545214ae6efe5a5ec2d5cc89` |
| 現行TODO validator | `tools/development/todo_handoff.py` | `17077dde9953a93b316e600fe8762a2e4a42ef3f95b13f824a34b22a55a8d43d` |
| 現行公式Test receipt生成器 | `tools/development/policy_test_runner.py` | `21ad04f205855832c46d7b192c4fb3205c185c9fd3b7904eb42d8f064f4e3b69` |
| 現行TODO圧縮validator | `tools/development/todo_compaction.py` | `0e446f9aa100d8128c32a3ddbcaca601e66aead9548db349b11a9f5adde89a1f` |

対象Issueの`problem`は次である。

> LLMがEvidence・TODO等の定型欄を手入力または都度の位置推測で作成している。そのため固定receiptとの転記差、見出し位置の不一致、検証完了前の時刻確定、監査内訳の分かりにくさが発生する。

### 0.1 直近の実例

TODOの「直近の全Test」欄が`829 passed`のまま残り、実績の`852 passed`へ後から訂正された
（commit `815456e`、1行の訂正）。receiptには正しい値があったのに、TODOへ写す工程が手入力だったため
差が残った。これは本Issueが扱う型の代表例である。

### 0.2 いま在るものと、足りないもの

`tools/development/todo_handoff_projection.py`は、構造化projectionから**TODO本文を決定的に描画する**
関数を既に持つ。templateの固定見出しが1回ずつ存在することを確認し、参照fileのSHA-256を実bytesから
再計算して照合し、不一致なら停止する。

足りないのは次である。

- 現在のTODOはこのrendererを通しておらず、人が本文を直接編集している。
- rendererへ渡す**projectionの中身**（Test件数、version、fallback、参照digest、時刻、集計）を
  作る決定的な経路が無い。ここが手入力のままである。

したがって本Issueは、rendererを作り直す話ではなく、**rendererへ渡す値を正本から機械で集める**話である。

## 1. 解くことと解かないこと

### 解くこと

公式Test receipt、対象fileのbytes、構造化入力から、定型欄を決定的に**収集・検証・描画**する。
初期対象は次の5つである。

1. TODOの関連Test／全Test表示（件数、suite、Python版、pytest版、fallback）
2. 参照pathとそのSHA-256
3. 固定見出しの位置（templateの一意な見出しidentityから決める）
4. 完了後にだけ確定する記録時刻
5. cohort別の監査内訳

### 解かないこと

- LLMが書く説明、要約、判断理由。**禁止しない。** 機械値と混ぜず、非権威の入力として受け取る。
- Humanの承認そのもの。
- Issue、Decision、Task Contractの自動作成。
- 既存recordの一括修復。過去のEvidenceやreceiptを遡って書き換えない。
- Git操作、外部送信。

TODOは引き続き**人向けのprojection**である。Workflow stateまたは完了Evidenceの正本にしない。
この位置づけは変えない。

## 2. 正本と生成経路

「どの値を、どこから、いつ取得し、どこへ出すか」を分ける。

| 値 | 正本 | 取得の時点 | 出力先 | 取得方法 |
| --- | --- | --- | --- | --- |
| 全Test／関連Testの件数、suite、Python版、pytest版、fallback、実行時刻 | 公式Test receipt（`policy_test_runner`が生成するJSON） | 当該testの実行完了後 | TODOのGit・Test欄、Evidenceの結果欄 | receipt JSONの**構造化field**を読む |
| 参照fileのSHA-256 | 対象fileのbytes | 参照を書き出す直前 | TODOの最新Evidence欄、Evidenceの固定入力表 | bytesから再計算する |
| 固定見出しの挿入位置 | templateの見出しidentity | 描画時 | 生成文書の各節 | 見出しが**ちょうど1回**あることを確認して決める |
| 生成・完了時刻 | 検証の完了 | **すべての必須検証が終わった後** | 記録の`recorded_at`等 | 検証完了後に一度だけ確定する |
| cohort別監査内訳 | 構造化された監査結果 | 監査の完了後 | 監査表示、Evidenceの内訳 | 構造化結果から決定的に集計する |
| 説明文、判断理由 | LLM | 任意 | 自由文の節 | 非権威の入力として受け取り、機械値の欄へ混ぜない |

### 2.1 停止する条件（出力を更新しない）

- 入力の欠落（receiptが無い、参照pathが無い、必須fieldが無い）
- digest不一致（参照fileが変わっている）
- 同一見出しの重複、または欠落
- 未知field（受け取った構造に想定外のkeyがある）
- receiptが`failed`、または必須検証が未完了
- 書込み後の再読込が、生成した内容と一致しない

いずれも「推測して埋める」ことをせず、停止して人へ返す。

### 2.2 stdout解析を正本にしない

公式Test receiptには`stdout`文字列も入るが、そこから`852 passed`のような件数を正規表現で
拾う方式は**初期実装の正本に採用しない**。pytestの出力書式に依存し、`xfail`や`warning`が
混ざると壊れるためである。

代替案として比較はする。receiptの構造化fieldに件数が無い場合の選択肢は次の3つになる。

| 選択肢 | 利点 | 欠点 |
| --- | --- | --- |
| A. receiptに件数の構造化fieldを追加する | 脆さが無い。将来のEvidenceでも同じ値を使える | `policy_test_runner`の出力形式を変える必要がある（本Issueの承認範囲外） |
| B. stdoutを解析する | 既存receiptのまま使える | 出力書式に依存し、壊れ方が静かである |
| C. 件数はTODOへ出さず、receipt pathとstatusだけを示す | 最も安全 | 人が読む情報が減る |

推奨は**A**である。ただし`policy_test_runner`の変更は本提案の承認範囲を超えるため、
最小縦切りでは「receiptの既存構造化fieldだけで表現できる欄を先に機械化し、件数の扱いは
Human判断項目として残す」形にする（§6の判断点2）。

## 3. 最小縦切りの比較と推奨

### 案A：TODOだけを対象にする

既存の公式Test receiptと参照fileから**構造化projectionを組み立てる収集器**を作り、
既存の`render_todo_handoff()`へ渡してTODO本文を描画・検証する。

- 対象：TODOの1文書だけ。
- 新規に作るのは、projectionを**集める**部分と、描画後の検証をまとめる部分である。
- 既存rendererとvalidatorは活かす。作り直さない。

### 案B：TODOに加えてEvidence／Decisionの定型欄へ同時に一般化する

共通の入力modelとrecord種別ごとのrendererを先に設計し、TODO・Evidence・Decisionを同時に扱う。

### 比較

| 観点 | 案A | 案B |
| --- | --- | --- |
| 再発防止の直接性 | 実例（`829`→`852`）がTODOで起きており、直接効く | 効くが、TODOへ届くまで時間がかかる |
| 大きさ | 小。既存rendererを活かす | 大。共通modelとrecord種別ごとの差異を先に決める必要がある |
| 失敗したときの影響 | TODO 1文書に限定 | Evidence／Decisionの生成まで巻き込む |
| 受入条件の具体性 | 既存TODO validatorとbyte上限があり、書きやすい | record種別ごとに条件が分かれ、初期から広い |
| authorityへの影響 | TODOは非権威のprojectionなので低い | Evidence／Decisionは権威に近く、慎重さが要る |

### 推奨：案A（Humanが承認するまで確定しない）

理由は3点である。

1. 実際に起きた手戻りがTODOで起きている。最短で再発防止に効く。
2. 既存rendererとvalidatorが既にあり、新しく作る範囲が「値を集める部分」に絞れる。
3. TODOは非権威のprojectionであり、間違えたときの影響が権威recordより小さい。

### 案Bへ進むために先に決めておく境界

案Aを実装する時点で、次を**満たす形**にしておく。汎用frameworkを先に実装するという意味ではない。

- **共通入力model**：値の出どころ（receipt／file bytes／template／検証完了時刻／集計）を、
  record種別に依存しない形で分けておく。TODO固有の項目名をこの層へ持ち込まない。
- **version**：projectionと生成物の双方にschema versionを持たせ、形が変わったら版を上げる。
- **record種別ごとのrenderer**：描画はrecord種別ごとに分ける。共通化するのは入力の集め方だけにする。
- **authorityを勝手に変更しない規則**：生成器はEvidenceやDecisionの内容を書き換えない。
  権威recordへ広げるときも、生成は新規作成だけに限り、既存recordの更新は人の判断を要求する。

## 4. 受入条件と検証方針

**この提案では実際のtestを作らない。**将来どの検証が要るかだけを示す。

### 条件1：receiptの件数・version・fallbackが正しく反映され、手入力差が起きない

- 正常例：receiptの構造化fieldの値が、そのままTODOの表示へ現れる。
- 負例：人が値を上書きしても、再生成すると受理されない（生成結果と一致しない）。
- 境界例：fallbackが`true`のreceipt、suiteが`full`以外のreceipt。
- 検証：固定receiptを入力にした生成Testと、生成結果とreceipt fieldの照合Test。
  **独立照合**として、生成物の数値をreceipt JSONから読み直して突き合わせる。

### 条件2：参照対象を改竄したとき、digest不一致で停止しTODOを変えない

- 正常例：参照fileが一致していれば描画できる。
- 負例：参照fileを1 byte変えると停止し、TODOのbytesが変わらない。
- 境界例：参照fileが存在しない、path脱出（`..`や絶対path）。
- 検証：fault injectionでfileを改変し、停止codeと**TODOのbytes不変**の両方を確認する。

### 条件3：見出しが欠落または重複すると停止し、位置推測で書き込まない

- 正常例：templateの必須見出しがちょうど1回ずつある。
- 負例：見出しが0回、または2回あると停止する。
- 境界例：見出し文字列が本文中に引用として現れる場合。
- 検証：template variantを使った正例・負例Test。位置を近傍探索で推測する経路が無いことも確認する。

### 条件4：failed receiptまたは未完了verificationから完了表示・完了時刻を生成しない

- 正常例：`passed`のreceiptからだけ完了表示を作る。
- 負例：`failed`のreceiptを渡すと停止する。時刻も付けない。
- 境界例：必須検証の一部だけが終わっている状態。
- 検証：failed receiptのfault injectionと、時刻確定が**検証完了後に一度だけ**起きることの確認。

### 条件5：cohort集計は入力順に依存せず再現する

- 正常例：同じ集合を並び替えて入力しても同じ内訳になる。
- 負例：未知のcohort名があれば停止する（勝手に「その他」へ寄せない）。
- 境界例：件数0のcohort、全件が1つのcohortに集中する場合。
- 検証：順序を入れ替えた入力での同一出力Test（property的な確認）。

### 条件6：描画後に再読込、TODO validator、参照整合、byte上限を検証する

- 正常例：書込み後に読み直した内容が、生成した内容と完全に一致する。
- 負例：一致しなければ停止し、その旨を返す。
- 境界例：12,288 byteの上限ちょうど、上限超過。
- 検証：post-write verification、`todo_handoff.py`のcommit安定検査、`todo_compaction.py`の
  size・active ID・参照到達性検査を、生成経路の一部として通す。

### 条件7：同じ固定入力から同じ出力が得られる

- 正常例：同じprojectionとtemplateから、byte単位で同じTODOが出る。
- 負例：時刻など非決定な値を入力に含めず、必ず引数として渡す。
- 境界例：非ASCII、長い説明文、改行の混在。
- 検証：二回生成して`==`で比較する決定性Test。

## 5. 依存・移行・停止境界

### 5.1 既存toolとの役割分担

| tool | 現在の役割 | 本Issueでの扱い |
| --- | --- | --- |
| `todo_handoff_projection.py` | 構造化projectionからTODO本文を描画する | **活かす。** 描画はここに任せ、作り直さない |
| `todo_handoff.py` | TODOのGit節がcommit安定かを検査する | **活かす。** 生成経路の検証段階で通す |
| `todo_compaction.py` | size上限、active ID、禁止履歴、参照到達性を検査する | **活かす。** 同上 |
| `policy_test_runner.py` | 公式Testを起動しreceiptを生成する | **入力として読むだけ。** 本Issueでは変更しない |

新しく作るのは「projectionを集める部分」と「描画後の検証をまとめる部分」だけである。

### 5.2 移行の順番

1. 収集器を作り、現在のTODOと**同じ内容**を生成できることを確認する（既存TODOは書き換えない）。
2. 生成物と現在のTODOの差分を人が確認する。差があれば、どちらが正しいかを人が決める。
3. 合意後、TODOの更新経路を生成器経由へ切り替える。
4. 切り替え後も、人が説明文を書く欄は残す。

一度に全部を切り替えない。差分確認の段階を必ず挟む。

### 5.3 `ISSUE-HTC-C9F6C917`（機械操作routing）との境界

- 本Issueは**記録の内容を決める**。どの値をどこから取り、どう描くかを扱う。
- C9は**実行の経路を決める**。どの操作にどの権限が要り、どう実行して受領証を残すかを扱う。
- 重なる語は「receipt」である。C9のreceiptは**実行の受領証**、本Issueが読むのは**Testの受領証**であり、
  別物である。生成器を二重に作らないよう、実装着手時にどちらが受領証を作るかを一度確認する。

### 5.4 停止してHuman判断を仰ぐ条件

- 生成結果と現在のTODOに、意味の違う差分が出たとき。
- 生成のために、意味的な文章の書き換えが必要になったとき。
- authority（Decision、Evidence、承認対象Digest）の変更が必要になったとき。
- `policy_test_runner`のreceipt形式を変える必要が出たとき。

## 6. Human判断が必要な点

1. **最初の対象を案A（TODOだけ）に限定してよいか。**
2. **何を「公式Test receipt」として受け付けるか。** 件数を構造化fieldとして持つよう
   `policy_test_runner`を変えるのか（§2.2の選択肢A）、当面は件数をTODOへ出さないのか（選択肢C）。
3. **生成済みTODOの更新を、どのcommitへ含めるか。** 作業単位のcommitへ同梱するか、別commitにするか。
4. **将来Evidence／Decisionへ拡張する条件。** 何が満たされたら案Bへ進むか。
5. **実装に着手してよいか。** 着手する場合、Test先行の作業単位をどこで切るか。

Humanの承認があるまで、本提案に基づく実装、RED test、既存recordの書換え、外部操作は行わない。
