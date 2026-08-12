# Python 3.13開発環境移行 軽量作業票 v1

- 作業票ID：`BTW-PYTHON-313-DEVELOPMENT-ENVIRONMENT-MIGRATION-001`
- 作成日：2026-08-13
- 状態：`awaiting_independent_start_review`
- 基準コミット：`80dba8ee1f82e904a34a9e9a5fb8446a78bdcd52`
- 危険度：`high`
- 作業担当：開始承認後の主担当
- 完了レビュー担当：作業担当とは異なる新規実行単位

## 1. 目的

第2段で採用候補とした公式試験入口の実行環境を、保守終了済みのPython 3.9系列からPython 3.13系列へ移す。
現行3.9環境を先に壊さず、3.13の隔離確認、版付き設定と依存固定の変更、正式`.venv`の切替え、公式全試験の
順で確認する。移行完了だけで第2段を完了にしない。

## 2. 入力と根拠

| 入力 | SHA-256または値 | 用途 |
| --- | --- | --- |
| 第2段再判定・利用者判断 | `6ecd6ae710edefdefe5d7d6ca18aa9ddb98895f2122cef3eee6e167b4e3dabfb` | Python 3.13を第2段完了前の次作業とする根拠 |
| `config/development-environment.json` | `d310298bfb35c24c1ec5b8b2c2c4f73d8d19d68e2874e88814100da35166792d` | 現行3.9環境、`.venv`、依存固定、構築command |
| `config/development-test-runner.json` | `9bdf7bcc3c9f84e471b0caf80b0d56111012d569e3e34dd79375b8c4df88f64d` | 公式試験入口のPython範囲 |
| `constraints/development-py39.txt` | `1307ed9075ddcc312697d18114b8f5b594796f047ab5df586e7a7b448058c8f2` | 3.13隔離確認の最初の依存候補。変更しない |
| `tools/development/bootstrap_environment.py` | `c0eb8db44c5646e4a231736a671032abe6d6be8b9e617a2e08f7c4de38eeda36` | 環境構築と検証の正規入口 |
| `tools/development/policy_test_runner.py` | `d749685737f09c301cfb9f118a8fe4688ad1d864d47f7c7e1ff9ef44bd7df076` | 公式全試験と結果記録の正規入口 |
| 移行前公式結果記録 | `6c9690f8ab87004ea50f6a857a272862165631ae4d60959f89bdbcea605f683e` | 3.9.6、pytest 8.4.2、1,736件成功の比較基準 |

移行前公式結果記録は
`/private/tmp/reviewcompass-stage2-python313-migration-baseline-v1.json`にある。単独実行の終了コードは0、
`status=passed`、1,736件成功、失敗・error・skipは0、fallbackなしである。

【実測】観測環境はApple Silicon、macOS 26.5.1で、`python3.13`、`uv`、`pyenv`、`mise`はPATH上にない。
Homebrewは`/opt/homebrew/bin/brew`にあるが、Python 3.13は未導入である。

【記録】2026-08-13に公開元を確認した。Homebrew公式は`python@3.13`の安定版とApple Silicon向け配布物、
`/opt/homebrew/bin/python3.13`への導入を案内する。PyPIは現行固定のpytest 8.4.2、platformdirs 4.4.0、
PyYAML 6.0.3をPython 3.13対応としている。実際の全依存導入可否は公開表示だけで合格にせず、隔離環境で確認する。

- `https://formulae.brew.sh/formula/python@3.13`
- `https://pypi.org/project/pytest/8.4.2/`
- `https://pypi.org/project/platformdirs/4.4.0/`
- `https://pypi.org/project/PyYAML/6.0.3/`

## 3. 作業範囲と対象外

変更可能pathは次の7件だけとする。

| path | 許可する変更 |
| --- | --- |
| `tests/test_development_environment.py` | 公式開発環境が3.13以上3.14未満、`python3.13`、3.13用依存固定を要求するRED |
| `tests/test_policy_test_runner.py` | 公式runnerが3.13を受理し3.9を拒否するREDと、現在環境を表す試験値の更新 |
| `tests/test_policy_test_runner_summary.py` | 現在の公式runner設定を使う試験値だけを3.13へ更新 |
| `config/development-environment.json` | `base_python`、Python範囲、依存固定path・SHA-256、二つの導入commandの依存固定path |
| `config/development-test-runner.json` | Python範囲だけを3.13以上3.14未満へ変更 |
| `constraints/development-py313.txt` | 3.13隔離環境で実際に解決・導入した依存を正規化した完全固定 |
| `records/development/2026-08-13-python-313-development-environment-migration-evidence-v1.md` | RED、隔離確認、切替え、試験結果、復旧可能性、未実施の記録 |

`environment_version: 1`と`runner_version: 2`は項目形式を変えないため維持する。`.venv`という正規path、
pytest 8.4.2、fallback禁止、結果記録必須、認証用環境変数6名の子process除外も維持する。

次は対象外とする。

- `pyproject.toml`と`setup.py`の公開Python対応範囲、製品code、試験以外の既存code。
- 既存`constraints/development-py39.txt`の変更または削除。
- pytestその他の依存の版更新、試験のskip・xfail・選択除外、期待の弱体化。
- Git検査、`OUT-PC-006`、外部実装経路の再開、Claude送信、重大な欠陥12件、第3段、第2段完了。
- Homebrew公式の`python@3.13`と同formulaが必須とする依存以外の導入・更新、既存Homebrew packageの削除。
- push、tag、amend、rebase、reset、force push、履歴書換え。

## 4. 期待する成果

1. 3.13を使う試験先行の変更が、現行3.9設定との差を意図した理由で検出する。
2. 現行3.9 `.venv`を保持したまま、`/private/tmp`の隔離環境でPython 3.13と現在の固定依存候補を導入し、
   project importと対象試験を確認する。
3. 隔離環境の実導入結果から`constraints/development-py313.txt`を機械抽出し、名前順、完全固定、重複0件にする。
4. 二つの版付き設定が3.13以上3.14未満と新しい依存固定へ一致する。
5. 現行`.venv`を`/private/tmp`の明示backupへ移した後、正規bootstrap入口で3.13の新しい`.venv`を作る。
6. 環境検証、関連試験、試験収集、公式全試験が3.13で成功し、結果記録と収集件数が一致する。
7. 失敗時は新しい不完全な`.venv`を別の一時pathへ退避し、3.9 backupを元へ戻せる。
8. GREEN実装、公式結果記録、Evidenceの順を保ち、Evidence追加後の確認ではGREEN commitの対象状態を
   再構成して結果記録の`source_state_digest`を照合する。

## 5. 機械確認と実施順

### 5.1 RED

最初に変更できるのは試験3件だけとする。現行3.9設定を使って次を単独実行し、3.13移行が未実施のため
失敗することを確認する。

```text
.venv/bin/python3 -m pytest -q \
  tests/test_development_environment.py \
  tests/test_policy_test_runner.py \
  tests/test_policy_test_runner_summary.py
```

失敗が3.13の版範囲、`python3.13`、3.13用依存固定以外なら停止する。試験3件だけをRED commitへ固定し、
GREEN中は要求の誤りが判明しない限り変更しない。

### 5.2 3.13の取得と隔離確認

利用者が、外部取得と`/opt/homebrew`への書込みを明示承認した後だけ、次を行う。

```text
/opt/homebrew/bin/brew install python@3.13
```

実行直前にHomebrewが示す導入対象を確認し、`python@3.13`と同formulaの必須依存以外の既存package更新が
含まれる場合は停止する。Homebrew公式が現在示す必須依存は`mpdecimal`、`openssl@3`、`sqlite`、`xz`である。

`/opt/homebrew/bin/python3.13 --version`が3.13以上3.14未満であることを確認する。続いて`mktemp -d`で作った
`/private/tmp`配下だけに隔離環境を作り、現在の依存固定を制約としてtoolchainと`.[development]`を導入する。
現在の固定版を変えないと導入できない場合は停止し、勝手に依存を更新しない。

隔離環境から`python -m pip list --format=freeze --exclude reviewcompass3`を取得し、名前の大文字小文字を無視した
順序で機械整列して3.13用依存固定候補を作る。重複、未固定行、local path、editable指定を許さない。

### 5.3 設定変更と正式切替え

独立開始前レビューが`開始可`となり、利用者が正式`.venv`の退避・置換まで含めて明示承認した後だけ行う。

試験3件を変えず、設定2件と3.13用依存固定を変更する。依存固定のSHA-256を機械計算し、
`config/development-environment.json`へ反映する。

正式`.venv`の切替え直前に、現在の`.venv`を一意な`/private/tmp`配下へ移し、backupのPython 3.9.6が起動する
ことを確認する。その後、次の正規入口を使う。

```text
/usr/bin/python3 -m tools.development.bootstrap_environment \
  --config config/development-environment.json \
  --project-root .
```

失敗時は不完全な新`.venv`を別の一時pathへ移し、3.9 backupを`.venv`へ戻す。backupを先に削除しない。

設定2件と3.13用依存固定をGREEN実装commitへ固定する。REDの試験3件はGREEN中に変更しない。

### 5.4 GREENと公式確認

次をそれぞれ単独実行し、終了コードを直接確認する。

```text
.venv/bin/python3 -m pytest -q \
  tests/test_development_environment.py \
  tests/test_policy_test_runner.py \
  tests/test_policy_test_runner_summary.py
.venv/bin/python3 -m pytest --collect-only -q
.venv/bin/python3 -m tools.development.policy_test_runner \
  --suite full \
  --receipt /private/tmp/reviewcompass-stage2-python313-migration-green-v1.json
git diff --check
```

結果記録はPython 3.13、pytest 8.4.2、fallbackなし、失敗・error・skip 0を示し、成功件数は独立収集件数と
一致しなければならない。この結果をEvidenceへ記録して別commitへ固定する。完了レビューはGREEN commitへ
Evidence一件だけを加えた状態からEvidenceを除外して対象状態を再構成し、`source_state_digest`を結果記録と照合する。

## 6. レビューで判断する事項

危険度を`high`とする理由は、外部package取得、`/opt/homebrew`への書込み、正式`.venv`の置換を含むためである。
開始前レビューは、次だけを確認する。

- 3.13移行に必要なpathと操作へ限定され、公開package対応範囲や製品codeへ広げていないか。
- 3.9 `.venv`を先に壊さず、隔離確認と復旧手段があるか。
- 依存版を無断更新せず、実導入結果から新しい依存固定を作るか。
- Human承認の対象が、Homebrew取得と正式`.venv`切替えまで具体的に固定されているか。
- 外部実装経路の使用停止を維持し、Git検査問題を混ぜていないか。

開始前レビューは`開始可`または`修正要`を返す。実装方法の一般化、Python導入管理の新機構、複数版対応、
継続的試験環境の設計を追加しない。

完了レビューは、RED、隔離確認、許可path、依存固定、backupと復旧可能性、3.13環境、関連試験、公式全試験、
結果記録、対象外、外部実装経路の使用停止を一回で確認する。レビュー担当は成果物を変更しない。

## 7. 停止条件と完了条件

次の場合は停止する。

- Python 3.13を取得できない、または3.13以上3.14未満でない。
- 現在の固定依存版が3.13隔離環境へ導入できず、依存版更新が必要になる。
- 許可path外のcode、公開package対応範囲、既存試験の意味変更が必要になる。
- 現行3.9 `.venv`のbackupを確認できないまま正式切替えが必要になる。
- 関連試験または公式全試験に、版表示の期待変更以外の失敗が見つかる。
- Git検査、外部実装経路、重大な欠陥12件、第3段、第2段完了へ範囲を広げる必要がある。
- 管理範囲外への未承認書込み、外部送信、履歴書換えが必要になる。

完了条件は次のとおりである。

- 試験3件だけのRED commitが、現行3.9状態を意図した理由で失敗させる。
- HomebrewのPython 3.13と隔離環境が確認され、新しい依存固定が実導入結果と一致する。
- 設定2件と3.13用依存固定だけのGREEN実装commitが意味的に完結し、試験3件はRED commitから不変である。
- GREEN実装commitの公式結果を記録したEvidence一件が、その後の別commitへ固定される。
- 正式`.venv`がPython 3.13で、環境検証、関連試験、独立収集、公式全試験が終了コード0となる。
- 公式結果記録の件数、版、fallback、`source_state_digest`が独立照合と一致する。
- 外部実装経路は`使用停止`のまま、既知の静的Git検査を保証根拠に使っていない。
- 一回の独立完了レビューが`verified`となる。

その後も、第2段完了は別の利用者判断とする。
