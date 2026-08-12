# Pilot Git実行時読取り専用ガード 軽量作業票 v1

- 作業票ID：`BTW-PILOT-GIT-RUNTIME-READ-ONLY-GUARD-001`
- 状態：`awaiting_independent_start_review`
- 上位計画：`docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md`
- 上位計画SHA-256：`c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- 基準コミット：`f85d70f5f9f8a7700ee742f0e892d6a4057b22dd`
- 元の完了レビュー：`records/development/2026-08-12-stage2-official-test-entry-restoration-completion-review-v1.md`
- 元の完了レビューSHA-256：`6518fbbb6662399590900e3069ce2d46a2bc9a69080a69d38b388c762a9bd02c`
- 採用する指摘：`CR-OTE-001`
- 危険度案：`high`。現役の共同作業入口が呼び出すGit処理の安全境界を製品codeで変更し、元の高危険度作業の
  完了可否を左右するためである。外部送信、不可逆操作、権限変更、管理範囲外への副作用は行わない。
- 作業担当：操縦役が兼務できる。
- 開始前レビュー担当と修正後確認担当：作業担当とは異なる実行単位と会話状態を使う。

## 1. 目的

静的な書き方の検査だけに依存せず、製品codeの`_run_git`自身がGitの読取り命令3種類だけを許す安全境界を持つ。
別名、動的な名前解決、無名関数など、どの呼出し方で`_run_git`へ到達しても、書込み命令を外部処理の起動前に
拒否する。

元の公式試験入口正常化作業で残った`CR-OTE-001`を一件の原因として解消し、同作業の完了条件と本作業の
完了条件を一回の修正後確認でまとめて確認する。本作業だけで第2段を完了または候補採用済みにしない。

【記録】利用者は2026-08-12、元の独立完了レビューが示した三択から、推奨案
「製品側のGit実行関数へ読取り専用命令の許可一覧を設ける」を選択肢`1`で承認した。

## 2. 入力と根拠

| 入力 | SHA-256 | 用途 |
| --- | --- | --- |
| 元の完了レビュー | `6518fbbb6662399590900e3069ce2d46a2bc9a69080a69d38b388c762a9bd02c` | `getattr`と分割文字列による偽陰性、修正方向 |
| `tools/development/pilot_collaboration.py` | `86d7c6b3604e8a61976b9e793255dee44d8578d006672271a2e901b2d81b3eb6` | `_run_git`実装と直接利用3件 |
| `tests/test_pilot_collaboration.py` | `678e35e434a52a11c87776395e52e775a918bd0d867d24fe709e5ad21144f646` | `OUT-PC-006`対応表と既存の読取り専用検査 |
| v6要求：`records/session-handoffs/2026-08-11-pilot-collaboration-entry-implementation-request-v6.md` | `5ab9474b425162df9c192124c7558754b4b371402d2e4d67adfab448cbbb3b5d` | `OUT-PC-006`、許可された変更範囲、停止コード集合 |
| 元の実施Evidence：`records/development/2026-08-12-stage2-official-test-entry-restoration-evidence-v1.md` | `ef5633cfb31b642487a8c7bf0137bc2c626664b651682de91a123c2a686ed4a1` | 元のRED、GREEN、公式全試験、対象外 |

【実測】現行`_run_git`は受け取った引数を確認せず、`subprocess.run`へ渡す。現在の直接利用は
`ls-tree`、`show`、`cat-file`の3種類だけで、いずれも読取り用途である。

【実測】元の完了レビューは、一時sourceの
`getattr(sys.modules[__name__], "_run" + "_git")(Path("."), "push")`に対し、二つの静的検査が
ともに違反0を返すことを確認した。これは外部処理を実行しない反証である。

## 3. 作業範囲と対象外

変更可能pathは次の3件だけとする。

| path | 許可する変更 |
| --- | --- |
| `tests/test_pilot_collaboration.py` | 既存`test_pilot_git_processes_are_read_only`へ、製品`_run_git`を直接呼ぶ実行時の正常例と拒否例を先に追加する |
| `tools/development/pilot_collaboration.py` | 読取り専用命令の固定集合を置き、`_run_git`が外部処理起動前に第一引数を完全一致で検査する |
| `records/development/2026-08-12-pilot-git-runtime-read-only-guard-evidence-v1.md` | RED、GREEN、元の指摘との接続、試験結果、未実施を記録する |

許可するGit副命令は次の3種類だけとする。

```text
ls-tree
show
cat-file
```

`_run_git`の可変引数が空、第一引数が文字列でない、または上記3種類以外の場合は、既存の`PilotStop`を
`internal_error`で送出し、`subprocess.run`を一度も呼ばない。引数全体や機密値を例外の説明へ含めない。
許可した命令の後続引数、戻り値、`binary`による文字列・bytes切替えは現行のままとする。

次は対象外とする。

- Git書込みの実行、Git全体を包む新しい共通基盤、外部依存、新しい設定schemaまたは停止コードの追加。
- `pilot_collaboration_cli.py`、v6要求本文、対応表のkeyや対応先、他の製品code、他の既存試験の変更。
- 元の公式試験入口正常化の設定、runner、RED 3 file、Evidence、完了レビューの書換え。
- Python 3.13移行、依存関係、仮想環境、重大な欠陥12件、第2段採用表、第2段完了、第3段以降。
- push、tag、amend、rebase、reset、force push、履歴書換え、外部送信。

## 4. 期待する成果

1. 先行試験は、現行実装では`push`が外部処理まで到達するため失敗し、実装の有無を区別する。
2. 実装後は、許可した3種類だけが従来どおり外部処理へ渡り、空、非文字列、書込み・変更命令は
   `internal_error`で外部処理起動前に停止する。
3. `getattr`と分割文字列を使って取得した同じ`_run_git`を呼んでも、`push`は実行されない。
4. 既存の静的検査、共同作業入口の全試験、関連する入口試験、公式全試験が成功する。
5. 試験だけのRED commitと、製品code・EvidenceだけのGREEN commitを分け、GREEN中にRED試験を変更しない。
6. 一回の修正後確認が、本作業と元の`CR-OTE-001`をまとめて確認する。

## 5. 機械で確認する事実と正規入口

### 5.1 RED

最初に変更できるのは`tests/test_pilot_collaboration.py`だけとする。既存の
`test_pilot_git_processes_are_read_only`へ、次を追加する。

- `monkeypatch`で製品moduleの`subprocess.run`を偽物へ差し替え、外部Gitを実行しない。
- `ls-tree`、`show`、`cat-file`がそれぞれ一回だけ偽物へ渡る正常例。
- `push`、`commit`、`reset`、`tag`、空引数、非文字列、先頭optionを拒否し、偽物の呼出し回数が増えない負例。
- `getattr(module, "_run" + "_git")`で得た関数へ`push`を渡しても同じく拒否する境界例。
- 拒否は`PilotStop.code == "internal_error"`で、詳細値を持たないこと。

次を単独実行し、現行実装では書込み命令が偽物へ到達するため当該試験が失敗することを確認する。

```text
.venv/bin/python3 -m pytest -q \
  tests/test_pilot_collaboration.py::test_pilot_git_processes_are_read_only
```

失敗理由が実行時ガード未実装以外なら停止する。試験一fileだけをRED commitへ固定し、GREEN中は変更しない。

### 5.2 GREEN

実装後、次をそれぞれ単独実行し、終了コードを直接判定する。

```text
.venv/bin/python3 -m pytest -q \
  tests/test_pilot_collaboration.py::test_pilot_git_processes_are_read_only
.venv/bin/python3 -m pytest -q tests/test_pilot_collaboration.py
.venv/bin/python3 -m pytest -q tests/test_pilot_collaboration_entrypoints.py
.venv/bin/python3 -m pytest -q tests/test_pilot_collaboration_cli.py
.venv/bin/python3 -m pytest -q tests/test_policy_test_runner.py
```

親処理へ認証・接続用6名を置いた状態で、公式入口の全試験を実行し、リポジトリ外へ新しい結果記録を作る。
終了コード0、失敗0、fallbackなし、独立収集件数との一致を確認する。試験用の値を結果記録へ残さない。

各commit前に`git diff --check`、明示pathだけのstage、commit後の変更pathと内容再読込みを確認する。
成果物作成後に参照解決、SHA-256、結果記録の再読込み、作業単位移行を確認する。

## 6. レビューで判断する事項

### 6.1 開始前レビュー

異なる実行単位が一回だけ次を確認する。

- 実行時の許可一覧が、静的な書き方に依存せず元の偽陰性を閉じるか。
- 読取り3種類の完全一致だけを許す範囲が、現在の全利用箇所と一致するか。
- `internal_error`が既存の結果形式を変えず、安全側に停止するか。
- 先行試験が外部Git書込みを実行せず、修正前後を区別できるか。
- 変更3 path、REDとGREEN、元の指摘との接続、対象外、利用者承認が明確か。

開始前レビューは`開始可`または`修正要`を返す。技術的に`開始可`であれば、利用者の選択肢`1`を本作業の
開始承認として実装へ進める。目的、許可命令、停止の意味を変える必要があれば停止し、利用者へ戻す。

### 6.2 修正後確認

作業担当と異なる実行単位が一回だけ、元の完了条件と`CR-OTE-001`、本作業の完了条件をまとめて確認する。
成果物は変更せず、静的検査を回避する別表現でも実行時ガードが書込みを止めること、RED不変、公式結果記録、
変更path、対象外維持を確認する。

## 7. 停止条件と完了条件

### 7.1 停止条件

- 許可するGit命令を3種類から増やす必要がある。
- 新しい停止コード、結果形式、設定schema、CLI、v6要求本文、対応表の変更が必要になる。
- `tests/test_pilot_collaboration.py`以外の既存試験を変更する必要がある。
- REDが外部Git書込みを実行する、または実行時ガード未実装以外の理由で失敗する。
- 公式全試験に、本変更と原因の異なる新しい失敗またはerrorが見つかる。
- 外部送信、認証値の表示、管理範囲外への恒久書込みが必要になる。

停止時は修正を広げず、事象、原因、機械証拠、現行Plan上の位置と、`いま対処`、
`候補として後回し`、`本線へ戻る`の三択を利用者へ返す。

### 7.2 完了条件

- RED commitは試験一fileだけで、実行時ガードがない現行実装を意図した理由で失敗する。
- GREEN commitは製品codeとEvidenceだけで、RED試験を変更しない。
- `_run_git`は許可3種類だけを完全一致で通し、他の値を外部処理起動前に`internal_error`で拒否する。
- 直接呼出し、元の`getattr`反証、別名や無名関数を経由した呼出しのすべてで同じ実行時境界が働く。
- 関連試験と公式全試験が終了コード0で、結果記録と独立収集件数が一致する。
- 許可path以外の変更、Git書込み、Python移行、外部送信、管理範囲外への副作用がない。
- Evidenceが元の指摘、RED、GREEN、実行結果、未実施へ接続される。
- 一回の修正後確認が`CR-OTE-001`の解消と本作業を`verified`とする。

その後も、第2段完了、テストコード管理候補の採用、Python 3.13移行は別の利用者判断とする。
