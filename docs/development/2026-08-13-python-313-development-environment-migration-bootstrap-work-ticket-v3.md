# Python 3.13開発環境移行 軽量作業票 v3

- 作業票ID：`BTW-PYTHON-313-DEVELOPMENT-ENVIRONMENT-MIGRATION-001`
- 作成日：2026-08-13
- 状態：`awaiting_delta_review`
- 基準コミット：`f969dbd6cfe8d2516d9ce7982b81efe318586a59`
- 先行版：`docs/development/2026-08-13-python-313-development-environment-migration-bootstrap-work-ticket-v2.md`
- 先行版SHA-256：`1d5836efed25fd049ce35772c6de60aaf4e40a952bfe8c580e7004a5ab5c5d16`
- 危険度：`high`（正式`.venv`切替えを含む先行判断を継承）
- 完了レビュー担当：作業担当とは異なる新規実行単位

## 1. この版の役割

本版はv2を置き換えて全文を再設計するものではない。v2の実施中、Homebrew版Python 3.13で公式全試験を
実行したときに表面化したbytecode cache（Pythonが作る実行用の一時ファイル）の出力先だけを補正する。
以下に明記しないv2の目的、許可範囲、依存固定、復旧方法、対象外、Human承認境界は維持する。

## 2. 判明した事実

1. 【実測】正式`.venv`はPython 3.13.14、pytest 8.4.2である。v2の対象34試験は34件成功し、
   独立収集は1,736件、いずれも終了コード0だった。
2. 【実測】`PYTHONDONTWRITEBYTECODE=1`を手作業で付けた公式全試験は1件失敗、1,735件成功だった。
   失敗はbytecode cache作成を期待する試験であり、この手作業条件を外すと当該1件は成功した。
3. 【実測】手作業条件を外した正規commandでは6件失敗、1,730件成功だった。6件はすべて、合成Git
   worktree内に生じた`tests/__pycache__`を許可外変更として検出したものだった。
4. 【実測】退避済みApple付属Python 3.9.6の`sys.pycache_prefix`は
   `/Users/keno/Library/Caches/com.apple.python`、Homebrew Python 3.13.14は`None`だった。
   3.9で代表試験は成功し、3.13で失敗した。
5. 【実測】3.13へproject外の一時`PYTHONPYCACHEPREFIX`を明示すると、合成Git worktreeの代表試験と
   bytecode cache作成試験は同時に2件成功した。

失敗結果記録は次のとおりであり、消さずにEvidenceへ残す。

| 結果記録 | SHA-256 | 結果 |
| --- | --- | --- |
| `/private/tmp/reviewcompass-stage2-python313-migration-green-v1.json` | `f537dae22206f325967324388fda62a72dba4c4cc249ae080763f04b91d7ef36` | 手作業条件あり、1 failed / 1,735 passed、終了コード1 |
| `/private/tmp/reviewcompass-stage2-python313-migration-green-v2.json` | `eeb4ed725095b7c569b9fc222c14ef5f23ae2579193ee3a8a11e9a1cc0c4fd42` | 正規command、6 failed / 1,730 passed、終了コード1 |

## 3. v2から変える範囲

今回新たに変更できるのは次の2 pathだけである。

| path | 許可する変更 |
| --- | --- |
| `tests/test_policy_test_runner.py` | 公式試験の子processへproject外の一時cache pathを渡し、親環境を変えず、実行後に片付けることを要求するRED |
| `tools/development/policy_test_runner.py` | 公式試験本体の実行中だけ一時directoryを作り、子processの`PYTHONPYCACHEPREFIX`をその絶対pathで上書きし、終了後に片付ける最小実装 |

v2で変更済みの試験3件、設定2件、`constraints/development-py313.txt`は変更しない。最終Evidenceはv2が許可した
`records/development/2026-08-13-python-313-development-environment-migration-evidence-v1.md`一件へ、今回の失敗、
原因、補正、再確認を追記する形で新規作成する。

## 4. 変えないもの

- `config/development-test-runner.json`の形式、`runner_version: 2`、認証用環境変数6名の除外。
- 結果記録の項目、公式command、試験集合、skip・xfail・選択除外。
- `PYTHONDONTWRITEBYTECODE`を除去する一般的な環境正規化。最初の1件失敗は作業担当がv2にない条件を
  手で加えたことが原因であり、今回の製品修正へ広げない。
- 合成Git worktree側、Git差分検査、task cache機構、`.gitignore`、製品code、公開Python対応範囲。
- 外部実装経路、Claude送信、第2段完了、第3段、既知のGit検査問題。
- 一時cache pathや実行環境全般を設定項目にする新しい仕組み。

## 5. 試験先行と実装順

1. `tests/test_policy_test_runner.py`だけを変更する。
2. 既存の偽processを使い、次を機械確認するREDを追加する。
   - 子processの`PYTHONPYCACHEPREFIX`は絶対pathで、project root外にある。
   - 呼出し前に親processへ同名変数があっても子processでは上書きされる。
   - 試験本体を実行している間は一時directoryが存在する。
   - `execute()`終了後は一時directoryが存在しない。
   - 親processの環境値は変わらない。
3. 次を単独実行し、新しい要求だけが失敗することを確認する。

```text
.venv/bin/python3 -m pytest -q tests/test_policy_test_runner.py
```

4. REDを意味的commitへ固定した後、`tools/development/policy_test_runner.py`だけを変更する。
5. 標準ライブラリの一時directoryを公式試験本体の実行中だけ保持し、そのpathで子process環境を上書きする。
   project内になった場合は試験を実行せず停止する。親processの`os.environ`は変更しない。
6. 結果記録の作成、構造化集計の読込み・削除、失敗結果の記録という既存順序を変えない。

## 6. 確認

次をそれぞれ単独実行し、終了コードを直接確認する。

```text
.venv/bin/python3 -m pytest -q tests/test_policy_test_runner.py
.venv/bin/python3 -m pytest -q \
  tests/test_development_environment.py \
  tests/test_policy_test_runner.py \
  tests/test_policy_test_runner_summary.py \
  tests/test_claude_implementation_route.py \
  tests/test_claude_implementation_executor.py \
  tests/test_task_python_cache.py
.venv/bin/python3 -m pytest --collect-only -q
.venv/bin/python3 -m tools.development.policy_test_runner \
  --suite full \
  --receipt /private/tmp/reviewcompass-stage2-python313-migration-green-v3.json
git diff --check
```

公式結果記録はPython 3.13、pytest 8.4.2、fallbackなし、失敗・error・skip 0を示し、成功件数が独立収集件数と
一致しなければならない。実行後にproject内へ未追跡`__pycache__`が残らず、一時cache directoryが片付いている
ことも確認する。GREEN commit後にEvidence一件を別commitへ固定する。

## 7. 差分限定レビュー

開始前レビューはv2から本版で変えた§2から§6だけを見る。v2で確認済みのHomebrew取得、依存固定、正式`.venv`
退避・復旧、設定変更を再レビューしない。次の問いだけに答える。

1. 2 pathの変更だけで、3.13で表面化した6件の原因を直接除けるか。
2. 既存のcache作成試験を壊さず、合成Git worktreeへcacheを残さないか。
3. 一時pathの範囲、寿命、親環境不変をREDで確認できるか。
4. 結果記録形式や設定形式の変更など、本質から外れた拡張が混じっていないか。

修正案は、上の目的を達成できない止める欠陥がある場合だけ最小限に示す。「念のため」の一般化、新しい
環境管理機構、他の試験改善、文書表現の改善は提案しない。

## 8. 停止条件と完了条件

次の場合は停止する。

- 2 path以外のcode・試験・設定変更が必要になる。
- 既存試験の意味を弱める、skipする、または試験集合を減らす必要がある。
- 一時cacheがproject内に入る、実行後に残る、親環境を変更する。
- 関連試験または公式全試験に今回の原因以外の失敗が残る。
- 結果記録形式、設定形式、外部実装経路、第2段完了へ範囲を広げる必要がある。

完了には、REDが新しい要求だけを検出し、2 pathだけのGREENで関連試験と公式1,736試験が終了コード0になり、
結果記録と独立照合が一致し、新規実行単位の独立完了レビューが`verified`になることを要求する。第2段完了は
その後の別の利用者判断とする。
