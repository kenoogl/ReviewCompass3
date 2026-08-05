# 機械操作routing 後続範囲のPlan提案

状態：`awaiting_human_approval`
対象Issue：`ISSUE-HTC-C9F6C917`
指示：`records/session-handoffs/2026-08-05-codex-to-claude-plan-machine-operation-routing-follow-on.md`

**これは実装許可ではない。**正式なIssue Resolution Plan、Decision、Task Contractでもない。
Humanが承認するまで、argv executor、cache root、移行inventory、Git／shell操作の置換を実装しない。
RED testも作らない。`ISSUE-HTC-C9F6C917`のstateは`registered`のままである。

## 0. 固定入力（作成時の実値）

| 種別 | path | SHA-256 |
| --- | --- | --- |
| 対象Issue | `.reviewcompass/workflow/issues-v4/issue-htc-c9f6c917--v1.json` | `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed` |
| 主triage decision | `.reviewcompass/workflow/triage-decisions-v4/dec-htc-c9f6c917--v1.json` | `5b698bd0e9069128710bef161e3d60475002c89c4a4b70cce015a39c31bbf444` |
| 既存の正本設計 | `docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal-v2.md` | `e01c3aaf8039377da2b43dab7f735d28a2f86bf10aa83f5bb22e5dd1eefa8572` |
| 最小縦切りの承認 | `records/development/2026-08-05-machine-operation-routing-v2-approval-decision-v1.md` | `c73cdc69b3ca3251b9de9480867c9677e0de4312f7bedff138a407af297cd969` |
| receipt整合性の訂正Decision | `records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-correction-decision-v1.md` | `f73f06e12f464a27ded059522e37015acbd2f9487d7d65d55ed96823a6f8033b` |
| 現在の実装 | `tools/development/operation_routing.py` | `0fb5636feac3e12c42104830cd710bdb2a6f9398b784edf211c57128e1cd9178` |

## 1. 現状と目的

### 1.1 最小縦切りで解決済みのこと

承認済み（`DEC-MACHINE-OPERATION-ROUTING-001`）で実装済みなのは3部だけである。

1. **operation inventory**：作業単位の操作を`read_only`／`project_artifact_write`／
   `git_metadata_write`／`external`／`unknown`に分類し、必要権限とcontent digestを持つ。
2. **permission preflight**：実行前にinventory全体を一度走査し、必要権限を一回の集合で出す。
   未取得なら書込みを一度も試さず停止する。
3. **execution receipt**：inventory、完全な検証済みpreflight、実行結果を結ぶ。改竄は再計算で拒否する。

このmoduleは**自分ではprocessを起動しない**。実行はcallerのcallbackが行う。

### 1.2 未解決として残っていること

| 後続項目 | 状態 |
| --- | --- |
| shellを経由しない構造化argv executor | 未承認・未実装 |
| task専用Python cache rootの決定的な固定 | 未承認・未実装 |
| 既存の直接shell／Git操作を安全に移す順序 | 未承認・未実装 |
| host側tool構文と外部送信の境界 | project内では解決できない。誤報しない扱いだけを維持する |

### 1.3 5観測との対応（再確認）

| 観測 | 足りない層 | 最小縦切りで閉じたか | 後続で扱うか |
| --- | --- | --- | --- |
| `HTC-C9F6C917` Git metadata書込みの権限事前判定 | 操作種別と権限の事前判定 | **閉じた** | — |
| `HTC-477EA1A4` Python cacheの書込み先 | cache先の固定 | 閉じていない | 後続2 |
| `HTC-186E9B83` shellの引用解釈 | argvの構造化 | 閉じていない | 後続1 |
| `HTC-9DCE8503` shell特殊変数への依存 | shellを経由しないこと | 閉じていない | 後続1 |
| `HTC-A5D1BCCA` host側tool構文 | host側の入力境界 | **project内では解けない** | 扱わない（§6で境界だけ維持） |

### 1.4 現状調査（read-onlyの機械検索。件数は推測していない）

`.venv`とegg-infoを除く`.py` **246 file**を走査した。

| 事実 | 件数 | 根拠 |
| --- | --- | --- |
| `tools/`配下でGit commandを起動する箇所 | **6** | 下表 |
| そのうちGit metadata書込み（`add`／`commit`／`tag`／`push`） | **0** | argv先頭語の機械照合 |
| repository全体の`shell=True` | **1** | `tests/test_operation_routing_v2.py:337`。これは実際の使用ではなく、moduleのsource textに現れないことを確かめる**禁止語の照合**である |
| repository全体の`os.system` | **0** | — |
| repository全体の`PYTHONPYCACHEPREFIX`設定 | **0** | — |
| repository全体の`sys.dont_write_bytecode`設定 | **0** | — |

`tools/`配下のGit起動箇所は次である。すべてargvの配列またはtupleで渡しており、shell文字列の
組立ては無い。

| path:line | 起動するGit操作 | 分類 |
| --- | --- | --- |
| `tools/bootstrap/migration_candidates.py:101` | `git ls-tree` | read_only |
| `tools/bootstrap/source_universe.py:18` | `git ls-files` | read_only |
| `tools/design/bootstrap_conformance.py:670` | `git show <commit>:<path>` | read_only |
| `tools/development/issue_resolution_pilot.py:308` | `git cat-file blob` | read_only |
| `tools/development/work_unit_transition.py:53` | `git status --porcelain` | read_only |
| `tools/session_logs/repository_context.py:27` | `git log`／`git diff`（引数は呼出し側） | read_only |

`tools/development/policy_test_runner.py`はPythonとpytestを起動するが、Git操作ではない。

**この調査から導かれる重要な事実**：repositoryのcodeには**Git metadataを書く経路が無い**。
Git metadataの書込みは、agentが自分の操作として行っている。したがって後続3（既存直接操作の移行）は、
「codeの中の危険な書込みを直す」作業ではなく、「agentが都度組み立てている操作を、inventoryと
executorの経路へ寄せる」作業である。この違いは、移行の優先順と受入条件に直接効く。

### 1.5 目的

後続範囲の目的は、**決定的に決まる実行手順を、その場の文字列組立てから機械側へ移すこと**である。
LLMは目的・対象範囲・意味の説明を担い続ける。

## 2. 後続3部の責任境界

### 2.1 構造化argv executor

`operation_routing.py`は**権限種別を計算するだけ**であり、processを起動しない。この責任分担を変えない。
executorは別moduleとし、次を担う。

- `argv`をshell文字列へ**再結合しない**。OSのexec相当へ配列のまま渡す。
- 検証（実行前にすべて確認し、一つでも欠ければ起動しない）
  - 各要素が文字列であること。`None`、数値、入れ子listを受理しない。
  - 先頭要素（実行file）が空でないこと。空文字列の要素を拒否するか許すかは、
    引数として意味を持つ場合があるため**Human判断点**とする（§6）。
  - `cwd`がproject root内の実在するdirectoryであること。絶対path、`..`、symlinkを拒否する。
  - 許可対象：inventoryに載っている操作だけを起動する。inventoryに無いargvは起動しない。
- 起動の可否は、必ずpreflightの`granted`を前提にする。executorは権限を判定も付与もしない。

**混同しない境界**：`operation_routing.py`＝分類と権限計算とreceipt、executor＝起動と結果返却。
executorはinventoryとpreflightを入力として受け取り、判定をやり直さない（二重判定は不整合の元になる）。

### 2.2 task専用Python cache root

観測`HTC-477EA1A4`は、compile確認が作業領域外へcacheを書こうとして拒否された事例である。
配置候補を比較する。

| 候補 | 汚さないか | 利点 | 欠点 |
| --- | --- | --- | --- |
| A. project内の除外directory（例：`.reviewcompass/cache/`） | project成果物は汚さないが**project内**である | 権限が確実。cleanupが簡単 | source state digestやlayout検査の除外規則を足す必要がある |
| B. OSの一時領域（`TMPDIR`配下のtask専用dir） | project外。利用者の常用cacheも汚さない | 隔離が明確 | sandboxが書込みを拒む場合がある（実際に拒否された事例がある） |
| C. 利用者の標準cache（`XDG_CACHE_HOME`等） | 利用者の常用cacheを**汚す** | 追加設定が不要 | 他作業と混ざる。推奨しない |

- **作成権限**：どの候補でも、実行前に「書けること」を確認し、書けなければcacheを使う操作を
  起動しない（起動してから失敗させない）。
- **cleanup／保持**：作業単位ごとに作って終了時に消すか、task IDで保持して再利用するかを比較する。
  保持する場合、古いcacheの削除条件を決める。
- **platform境界**：`TMPDIR`（macOS／Linux）と`TEMP`／`LOCALAPPDATA`（Windows）、path区切り、
  長さ上限、大文字小文字の扱いが異なる。共通仕様は「task専用rootを決定的に決め、そこ以外へ書かない」
  ことだけとし、rootの決め方をplatform adapterに寄せる案を推奨する。

現状`PYTHONPYCACHEPREFIX`の設定は**0件**であり、既存の挙動を壊さずに追加できる余地がある。

### 2.3 既存直接操作の移行

**全面置換を一括で行わない。** 次の順で進める。

1. 機械抽出した**移行inventory**を作る（§4の方法）。
2. 操作種別ごとに一種類ずつ移す。1種類ごとに、移行前後で分類・preflight・receiptを比較する。
3. §1.4のとおりcode内のGit書込みは0件なので、最初に移すのは**agentが行う操作**である。

## 3. 安全な段階と停止条件

### 3.1 段階順の比較

| 案 | 順序 | 利点 | 欠点 |
| --- | --- | --- | --- |
| **案1（推奨）** | 設計固定 → RED test → argv executor最小slice → cache root最小slice → 移行inventory → 操作種別ごとの段階移行 | 起動経路を先に安全にしてから対象を広げる。各段が小さい | 移行の全体像が見えるのが後になる |
| 案2 | 設計固定 → 移行inventory → RED test → executor → cache root → 段階移行 | 全体像が早く見える | inventoryだけ先に作っても実行経路が無く、使い道が無い期間が生まれる |
| 案3 | executorとcache rootを同時に1 sliceで作る | commit数が減る | 受入条件が混ざり、失敗時に原因の切り分けが難しい |

**推奨は案1**である。理由は3点。

1. 5観測のうち後続で閉じられるのは引用・特殊変数・cacheであり、前2つはexecutorが閉じる。
   最も件数の多い層から着手できる。
2. §1.4のとおりcode内にGit書込みが無いため、移行inventoryを先に作っても直す対象がcode内に無い。
   executorという受け皿を先に用意するほうが順序として自然である。
3. 段階が小さく、失敗しても影響範囲が1 sliceに閉じる。

### 3.2 各段階で実装しないこと・Human承認が要る条件

| 段階 | 実装しないこと | Human承認が要る条件 |
| --- | --- | --- |
| 設計固定 | code一切 | 設計そのものの承認 |
| RED test | 実装 | — |
| argv executor最小slice | shell経由の実行、既存呼出しの置換、cache設定 | 許容する操作種別、実行責任の境界（§6-1） |
| cache root最小slice | 既存呼出しの置換、cacheの自動削除 | 配置と保持方針（§6-2） |
| 移行inventory | 置換そのもの | 移行対象の優先順（§6-3） |
| 段階移行 | 一括置換 | 種別ごとの着手可否 |

**既存の動作を変更しない確認**：各段階で、移行前後の公式全testが同じ集計になることと、
既存の呼出し経路を触っていないことをdiffで示す。

### 3.3 維持する停止原則

最小縦切りで固定した次の原則は、後続でも変えない。

- `unknown`分類はfail-closedで停止する。
- 未取得権限では、書込みを一度も試さず停止し、必要権限を一回の集合で出す。
- scope外のhost操作に達したら停止する。
- `external`操作はこのrunnerで実行しない。
- inventory／preflight／receiptのidentityが一致しなければ停止する。

## 4. 移行対象の調査方法（今回は実施しない）

次段階で作る成果物と、その作り方だけを提案する。**今回は移行inventoryもcodeもtestも作らない。**

### 4.1 機械検索の方法

`.venv`とegg-infoを除く`.py`を走査し、次を列挙する（今回の§1.4はこの方法で得た）。

| 目的 | 検索対象 |
| --- | --- |
| 直接shell実行 | `subprocess.run`、`subprocess.Popen`、`shell=True`、`os.system` |
| Git操作 | argvの先頭語が`git`である呼出し |
| Git metadata書込み | 上記のうち第2語が`add`／`commit`／`tag`／`push`等 |
| Python cache設定 | `PYTHONPYCACHEPREFIX`、`dont_write_bytecode` |

検索は行単位ではなく、呼出し式の範囲で見る（引数が複数行に分かれるため）。件数は必ず機械で数え、
文章へ手入力しない。

### 4.2 次段階で作る成果物（提案）

- **移行inventory record**：path、行、起動するcommand、分類、移行の可否、移行順、根拠を持つ版付きrecord。
- **選定規則**：read-onlyのGit操作は後回し、書込みを伴う操作を先に扱う。injectable な`run`引数を
  すでに持つ箇所（`work_unit_transition`、`policy_test_runner`、`session_logs`）は差し替えやすいため
  優先度を上げる、など。
- **除外規則**：test内の呼出しはfixtureの一部であり、製品経路ではないため移行対象から外す。

## 5. 受入条件と検証方針（Testは作らない）

### 条件1：shell解釈へ渡らない

- 正常例：空白、`"`、`'`、backtick、`$`、`*`、改行、非ASCIIを含む引数がそのまま届く。
- 負例：argvをshell文字列へ連結する経路が存在しない。`shell=True`相当を持たない。
- 境界例：引数が空文字列、極端に長い、pathに見える文字列。
- 独立確認：起動側に渡ったargvを実行層から取り出して比較する。報告文を根拠にしない。

### 条件2：不正argv・unsafe cwd・未取得権限でprocessが一度も起動しない

- 正常例：検証を通った場合だけ起動する。
- 負例：型不正、空の実行file、inventory外のargv、絶対path／`..`／symlinkのcwd、未取得権限のいずれでも
  起動回数が0である。
- 境界例：作業単位の途中で初めて書込み操作が現れる場合も、開始前の走査で拾う。
- 独立確認：起動関数の呼出し記録を数える（最小縦切りのfault injectionと同じ方式）。

### 条件3：cache rootがproject内や意図しないrootへ書かれない

- 正常例：cacheがtask専用root配下だけに作られる。
- 負例：project成果物directory、`.reviewcompass/`、`records/`、利用者の常用cacheへ書かない。
- 境界例：rootが未設定、読み取り専用、既存、path長上限。
- 独立確認：実行前後のfile一覧の差分を機械比較し、task専用root以外に増えたfileが無いことを確かめる。

### 条件4：移行前後で挙動が後退しない

- 移行対象ごとに、**分類**・**権限preflightの結果**・**receipt identity**を移行前後で比較する。
- 差が出たら移行を止める。差が無いことを、移行1件ごとの記録に残す。
- 独立確認：公式全testの構造化集計が移行前後で一致すること。

### 条件5：platform差の扱い

| 事項 | 共通仕様 | platform adapter |
| --- | --- | --- |
| argvの渡し方 | 配列のまま渡す。shellを経由しない | — |
| cache rootの決め方 | 「task専用rootを決定的に決め、そこ以外へ書かない」 | rootの基準（`TMPDIR`／`TEMP`／`LOCALAPPDATA`）、path区切り、長さ上限 |
| path検証 | 絶対path・`..`・symlinkを拒否する | 大文字小文字の扱い、予約名（Windows） |
| 実行fileの解決 | inventoryに載った名前だけ | 拡張子の扱い（Windows） |

Windows環境は現在このrepositoryで検証していない。**共通仕様だけを先に固定し、adapterは
実際に対象環境が必要になった時点で作る**ことを推奨する。今回、Windows向けcodeは書かない。

## 6. Human判断が必要な点

1. **argv executorの許容操作種別と実行責任の境界。**
   起動を許すのは`read_only`と`project_artifact_write`までか、`git_metadata_write`も含めるか。
   空文字列の引数を受理するか。executorはinventoryとpreflightを再判定しない、でよいか。
2. **cache rootの配置・削除／保持方針。** 候補A（project内の除外directory）、B（OSの一時領域）、
   C（利用者の標準cache）のどれか。作業単位ごとに消すか、task IDで保持するか。
3. **移行対象の優先順と、最初の実装sliceの承認可否。**
   §1.4のとおりcode内のGit書込みは0件である。最初に移すのはagentの操作でよいか。
   injectableな`run`を持つ3箇所を先に扱うか。
4. **host側tool構文と外部送信を本Issueで扱わないことの確認。**
   `HTC-A5D1BCCA`はproject内では解けない。解決済みと書かない境界を維持する、でよいか。

Humanの承認があるまで、本提案に基づく実装、RED test、移行inventoryの作成、既存呼出しの置換、
Git／shell／Python cacheの実行自動化は行わない。
