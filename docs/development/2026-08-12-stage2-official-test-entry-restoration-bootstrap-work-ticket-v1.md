# 第2段 公式試験入口の正常化 軽量作業票 v1

- 作業票ID：`BTW-STAGE2-OFFICIAL-TEST-ENTRY-RESTORATION-001`
- 状態：`awaiting_independent_start_review`
- 上位計画：`docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md`
- 上位計画SHA-256：`c57336dd2df961e6fe65b8f7c46665db6bce8e0df66111fc90796398a48dd812`
- 基準コミット：`29190ad53685fef5bb699fd3f9d50216aa85b20d`
- 第2段採用表候補：`records/development/2026-08-12-stage2-minimum-trust-foundation-adoption-table-candidate-v1.md`
- 危険度案：`high`。他の成果物の合否を決める公式試験入口と既存試験を変更するためである。外部送信、
  不可逆操作、管理範囲外への書込みは行わない。
- 作業担当：操縦役が兼務できる。
- 開始前レビュー担当と完了レビュー担当：作業担当とは異なる実行単位と会話状態を使う。

## 1. 目的

第2段の採用表候補で確認した公式全試験15件の失敗を、原因を混ぜずに解消する。公式試験入口が、
利用者の端末に認証・接続用の環境変数が存在しても、それらを試験処理へ渡さず、版付き設定に従って
全試験を実行し、正常終了の結果記録を作れる状態へ戻す。

同時に、過去の一作業だけの変更範囲を現在の先端コミットへ適用し続けている3件の試験を、恒久的に
検査する部分と期限を終えた部分に分ける。単に過去の許可一覧へ現在のpathを追加する方法は採らない。

本作業は現行Python 3.9環境で原因を分離して正常終了を確認する。Python 3.13への移行は、正常な基準を
得た後の別作業とし、本作業へ混ぜない。本作業の完了だけで第2段を完了または採用済みにしない。

## 2. 入力と根拠

固定入力は次に限る。

| 入力 | SHA-256 | 用途 |
| --- | --- | --- |
| `records/development/2026-08-12-stage2-minimum-trust-foundation-adoption-table-candidate-v1.md` | `f8749c543da4753b4e357375241b40b144cbd26edf831437048b2589fa873121` | 15件の失敗、原因分類、Python移行との分離 |
| `records/development/2026-08-12-stage2-minimum-trust-foundation-post-fix-review-v1.md` | `763e09d72dc7f2595b1042e05e204a5242d1392b966302c20f730f88d2213cdd` | 第2段を止める残存不合格1件 |
| `config/development-test-runner.json` | `179382b8462b92d502399ede89f4fbc110095cc353e530584f1f580b2e067208` | 公式入口の版付き設定 |
| `tools/development/policy_test_runner.py` | `0f7072ab8a7c4ab9093f394858c7629e2f60c1d2b774d5fd3b640622998e5b24` | 試験処理へ渡す環境と結果記録の生成 |
| `tests/test_policy_test_runner.py` | `58e3b8d5014009a17b9553e8b57afce5c68a263df48240b03bca1271bb73163a` | 公式入口の受入試験 |
| `tests/test_claude_bootstrap_entrypoints.py` | `9b29ca6ad06fcd5a191bebf50a03dcec41e2c5611c5064a729988779d3f816fe` | 期限付きの変更範囲確認2件 |
| `tests/test_pilot_collaboration_entrypoints.py` | `a9bee42f163959c66a4407787e696334dcef8d74596d5c84303b50b3cd606948` | 期限付きの変更範囲確認1件と恒久的な使い捨てGit試験 |

公式全試験の失敗結果記録はリポジトリ外の
`/private/tmp/reviewcompass-stage2-official-test-receipt-v1.json`にあり、SHA-256は
`cd482d418928f3956f8d70340cc039b3f2c7e4ea8e79d3ee0243ff884600d686`である。終了コード1、
1,736件中1,721件成功、15件失敗だった。失敗nodeの整列済み列挙SHA-256は
`6396800628544698e8b681cdd427075c3a12a033efd2e5aaddba38e7c557b897`である。

【実測】認証・接続用の環境変数6個を当該試験処理だけから除くと、
`tests/test_claude_implementation_executor.py`は28件すべて成功した。3件の変更範囲試験は同じ隔離状態でも
失敗し、過去の基準コミット以後に正当に追加されたpathや変更を拒否した。

## 3. 作業範囲と対象外

### 3.1 変更可能path

変更可能pathは次の5件に限る。

| path | 許可する変更 |
| --- | --- |
| `tests/test_policy_test_runner.py` | 認証・接続用の環境変数を試験処理へ渡さない反例を先に追加し、版付き設定の期待を更新する |
| `config/development-test-runner.json` | 除外する6変数名を明示する欄を追加し、`runner_version`を2へ上げる |
| `tools/development/policy_test_runner.py` | 設定を検証し、全試験を起動する子処理の環境から指定名だけを除外する |
| `tests/test_claude_bootstrap_entrypoints.py` | 固定コミットから基準一覧を再生成する恒久検査を残し、現在の先端との差を一作業の1関数へ限定する検査を除く。過去コミット以後の全試験を不変とする検査を除く |
| `tests/test_pilot_collaboration_entrypoints.py` | 現在の先端を過去作業v6の許可pathだけへ限定する1件を除く。使い捨てGitで禁止pathを検出する恒久試験2件は残す |

結果Evidenceは次の一件だけを新規作成できる。

```text
records/development/2026-08-12-stage2-official-test-entry-restoration-evidence-v1.md
```

公式試験の結果記録と一時fileは`/private/tmp`へ置き、リポジトリへ追加しない。

### 3.2 固定する環境分離

版付き設定へ追加する除外名は次の6個だけとする。値は記録、表示、結果記録へ出さない。

```text
ANTHROPIC_API_KEY
ANTHROPIC_AUTH_TOKEN
ANTHROPIC_BASE_URL
ANTHROPIC_FOUNDRY_API_KEY
ANTHROPIC_VERTEX_PROJECT_ID
AWS_BEARER_TOKEN_BEDROCK
```

公式入口は親処理の環境を直接変更しない。Pythonとpytestの版確認処理は従来どおりとし、全試験を起動する
子処理の環境だけを複製し、上記6名を除外して、試験件数集計用の変数を加える。それ以外の環境変数は
本作業では変更しない。

### 3.3 対象外

- `tests/test_claude_implementation_executor.py`と`tools/development/claude_implementation_executor.py`の変更。
  認証用環境変数があると実送信前に停止する製品側の安全境界は緩めない。
- 過去の許可path集合、process一覧または全試験の内容識別値を、現在の先端へ合わせて拡張するだけの修正。
- 3件以外の既存試験の削除、期待値の弱体化、skip、xfail、選択除外。
- 結果記録の項目変更、集計方法変更、fallback許可、別の試験入口追加。
- Python、仮想環境、依存関係、`pyproject.toml`、Python 3.13移行。
- 未修正の重大な欠陥12件、外部送信、認証、応答解析、配置、第3段以降。
- push、tag、履歴書換え、管理範囲外への恒久書込み。

## 4. 期待する成果

成果は次の一つの意味単位とする。

1. 公式試験入口の環境分離を失敗させる試験が実装前に追加され、単独実行で失敗する。
2. 版付き設定と公式試験入口が、6変数名だけを全試験の子処理から除外する。
3. 期限付き3件が恒久検査と分離され、残した恒久試験が成功する。
4. 関連試験と公式全試験が現在のPython 3.9環境で正常終了する。
5. 実施、結果、判断、未実施、変更した試験の理由、実行コマンド、終了コード、件数、結果記録の
   内容識別値をEvidence一件へ記録する。

試験だけのRED（修正前なら失敗する状態）は、実装と分けた意味単位コミットへ固定する。GREEN
（修正後に成功する状態）は、設定、実装、Evidenceを別の意味単位コミットへ固定する。既存試験の変更理由は、
「要求を弱めるため」ではなく「一作業の範囲確認を恒久的な先端状態の合否から分離するため」とEvidenceへ残す。

## 5. 機械で確認する事実と正規入口

### 5.1 RED

最初に変更できるのは3試験fileだけとする。公式試験入口の環境分離試験を追加し、期限付き3件を§3.1どおり
整理する。実装前の`policy_test_runner.py`と設定に対して、次を単独実行する。

```text
.venv/bin/python3 -m pytest -q tests/test_policy_test_runner.py
```

新しい環境分離試験が失敗し、他の同file内試験が成功することを確認する。失敗理由が環境分離未実装以外なら
停止する。RED commit後、実装中は新しい試験を変更しない。

### 5.2 GREEN

実装後、次をそれぞれ単独実行し、終了コードを直接判定する。

```text
.venv/bin/python3 -m pytest -q tests/test_policy_test_runner.py
.venv/bin/python3 -m pytest -q tests/test_claude_bootstrap_entrypoints.py
.venv/bin/python3 -m pytest -q tests/test_pilot_collaboration_entrypoints.py
.venv/bin/python3 -m pytest -q tests/test_claude_implementation_executor.py
```

認証・接続用の6環境変数が親処理に存在する状態で、公式入口を単独実行する。値は出力しない。

```text
python3 -m tools.development.policy_test_runner \
  --suite full --receipt /private/tmp/reviewcompass-stage2-test-entry-restoration-receipt-v1.json
```

公式入口の終了コード0、結果記録の`status=passed`、failed 0、errors 0、fallbackなしを確認する。
`pytest --collect-only`による独立件数と結果記録のtotalが一致することも確認する。全試験の子処理へ6変数名が
渡っていないことは、新しい受入試験の差し替え処理で機械確認する。

各commit前に`git diff --check`、明示pathだけのstage、commit後の変更pathと内容再読込みを確認する。
成果物を書いた後は参照解決、SHA-256、結果記録の再読込み、作業ツリーの状態を確認する。

## 6. レビューで判断する事項

### 6.1 開始前レビュー

危険度`high`のため、実装開始前に異なる実行単位が一回だけ次を確認する。

- 6変数の除外が試験処理だけに限定され、製品側の認証禁止を緩めないか。
- 版付き設定の項目追加と版更新が必要最小限か。
- 3件が一作業限定の範囲確認であり、除去または縮小しても恒久的な安全検査が残るか。
- REDとGREENの境界、変更可能path、停止条件、利用者判断が明確か。
- Python 3.13移行や重大な欠陥12件の修復を混ぜていないか。

開始前レビューは`開始可`または`修正要`を返す。技術的に`開始可`でも、既存試験変更と設定項目追加の
意味判断は利用者が開始時に承認する。

### 6.2 完了レビュー

作業担当と異なる実行単位が一回だけ、REDが修正前後を区別すること、期限付き試験の分類、設定と実装の
接続、親環境の不変、製品側の安全試験、公式結果記録、変更path、対象外維持を確認する。判定と修正後確認は
上位計画v5 §6に従う。技術的な`verified`だけで第2段完了または採用済みにしない。

## 7. 停止条件と完了条件

### 7.1 停止条件

- 利用者の開始承認前、または独立開始前レビューが`開始可`でない状態で、試験、設定、実装を変更する必要がある。
- 除外名6個以外の環境変数を変更しないと正常終了できない。
- 3件以外の既存試験の変更、skip、xfail、試験選択除外が必要になる。
- 版付き設定とrunnerの変更だけでは環境分離を一意に再現できない。
- 公式全試験で、固定した15件以外の新しい失敗またはerrorが見つかる。
- Python、依存関係、仮想環境、結果記録項目、上流設計、別のschemaを変更する必要がある。
- 外部送信、認証値の読取りまたは表示、管理範囲外への恒久書込みが必要になる。

停止時は推測で修正を広げず、事象、原因、機械証拠、現行Plan上の位置と、`いま対処`、`候補として後回し`、
`本線へ戻る`の三択を利用者へ返す。

### 7.2 完了条件

- RED commitは試験3 fileだけを変更し、新しい環境分離試験が修正前実装で意図どおり失敗する。
- GREEN commitは設定、runner、Evidenceだけを追加変更し、RED commitの試験を変更しない。
- 設定版2が除外名6個を持ち、runnerが全試験の子処理だけからその6名を除く。
- 親処理の環境、版確認、結果集計、結果記録、fallback禁止、製品側の認証禁止は従来どおりである。
- 期限付き3件を除いた後も、固定基準の再生成、egress 6 file、使い捨てGitによる禁止path検出の恒久試験が残る。
- 関連4試験fileと公式全試験が終了コード0で、結果記録と独立収集件数が一致する。
- 許可path以外の変更、Python 3.13移行、外部送信、管理範囲外への副作用がない。
- Evidence一件が固定入力、REDとGREEN、実行結果、未実施へ結び付き、意味的に完結したcommitに固定される。
- 一回の独立完了レビューが`verified`である。

その後、利用者がテストコード管理候補の採用、第2段採用表の更新、第2段完了へ戻るかを別に判断する。
