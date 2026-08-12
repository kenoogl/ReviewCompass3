# 第2段 公式試験入口の正常化 独立完了レビュー v1

- レビュー記録ID：`REV-STAGE2-OFFICIAL-TEST-ENTRY-RESTORATION-COMPLETION-001`
- レビュー日：2026-08-12
- レビュー担当：作業担当とは異なる実行単位
- 危険度：`high`
- 上位入口：`docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md` §6
- 作業票v1：`docs/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-work-ticket-v1.md`
- 作業票v1 SHA-256：`5af82a43c618481e08abf398abdc50d289388eb1388da9aa58ae0ee9a4d1d00f`
- 最終作業票v4：`docs/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-work-ticket-v4.md`
- 作業票v4 SHA-256：`8f6632ec7754b48d88c661682c76d6c8de5ee56c5b9d2997341aa45f99131bc8`
- RED commit：`354c57e1d7dd28eaa6b2e271ea3dae60ce949720`
- 対応表補正commit：`48076c1b754ca09f061fa8a949600c1792cd563f`
- GREEN commit：`c4733cd161eff43f682defabfeaf6415ab72b7a2`
- Evidence：`records/development/2026-08-12-stage2-official-test-entry-restoration-evidence-v1.md`
- Evidence SHA-256：`ef5633cfb31b642487a8c7bf0137bc2c626664b651682de91a123c2a686ed4a1`
- 公式receipt：`/private/tmp/reviewcompass-stage2-test-entry-restoration-receipt-v2.json`
- 公式receipt SHA-256：`08b15d46c4a36ddd6abe894d9e11e21b8a2385852548c44adf6b3df852616f0f`
- 判定：`blocked`

## 1. 判定

【判断】REDによる修正前後の区別、期限付き試験の分離、設定版2と六名の環境分離、製品側の認証禁止、
対応表の未定義参照解消、関連試験と公式全試験、変更path、結果記録、作業単位移行は、固定材料と独立再実行で
一致した。実施結果と事後状態の報告不一致は0件である。

一方、v4が`OUT-PC-006`へ対応させたGit読取り専用検査には、`_run_git`の名前を実行時に組み立てて
`getattr`で取得するGit書込みを見逃す偽陰性がある。既存の二つの静的検査がともに違反0を返し、公式全試験も
この欠陥を検出しない。v4の完了条件と、次段の信頼基盤へ使える恒久検査という目的を満たさないため、
技術的完了を`verified`にしない。

【実測】止める指摘は1件、報告不一致は0件である。

## 2. 止める指摘

| ID | 区分 | 段階 | 根拠類型 | 影響 | 事象と反証 | 必要な修正 |
| --- | --- | --- | --- | --- | --- | --- |
| `CR-OTE-001` | blocking | completion | `work-review-protocol` §11.1 類型3 | `OUT-PC-006`、v4 §3〜§7、Evidence §3・§7の「読取り専用Git検査で解消」という判断 | 現行製品sourceへ、実行しない一時文字列として`getattr(sys.modules[__name__], "_run" + "_git")(Path("."), "push")`を追加した。`_git_process_policy_violations`と`_process_policy_violations`はともに空tupleを返した。直接4種と承認済み間接3変種の試験は成功する一方、同じ動的wrapper解決の別表現でGit書込みを追加しても合格する | 恒久保証を維持するなら、Human承認の下で製品側`_run_git`へruntimeの読取り専用allowlistを置き、静的表現に依存しない反例を追加する。製品codeを変更しないなら、自動試験が全Git書込み経路を防ぐという主張を狭め、固定commitと事後Evidenceだけで何を確認するかを作業票・対応表・Evidenceで再裁定する |

【判断】この所見は、v3で確認したalias、大域名前表、無名関数と同じ動的wrapper解決の変種である。新しい
機能要求ではなく、合格中の恒久試験へ書込み経路を残す機械反証なのでblocking類型3とする。表現改善や
範囲外の将来案として扱わない。

## 3. 報告と事後状態の一致

【実測】`report_execution_mismatch`に該当する競合Evidenceは0件である。次はEvidenceの報告と一致した。

- v1、開始前レビュー、開始判断、v2〜v4、範囲判断・修正レビューのpath、SHA-256、commit。
- RED、対応表補正、GREENの各commitと変更path。
- RED試験三fileのGREEN中不変、最終七fileのSHA-256。
- 設定版、六名、結果記録の設定digest、公式件数、独立collect件数、fallbackなし。
- 固定receipt取得後に追加されたEvidence一件を除く実行対象の`source_state_digest`。

【判断】`CR-OTE-001`は、報告したcommandや事後Git状態が実際と異なる問題ではなく、受入試験が誤った合格を
許す問題である。このため判定は`report_execution_mismatch`ではなく`blocked`とする。Evidenceの機械結果は
有効だが、「Git読取り専用検査で`OUT-PC-006`を解消した」という判断は本所見の影響を受け、完了根拠に使えない。

## 4. RED、期限付き試験、変更範囲

【実測】RED commitは次の試験三fileだけを変更した。

- `tests/test_policy_test_runner.py`
- `tests/test_claude_bootstrap_entrypoints.py`
- `tests/test_pilot_collaboration_entrypoints.py`

固定RED commitを`/private/tmp`へ一時展開し、同commitの
`tests/test_policy_test_runner.py`を実行すると、終了コード1、新規環境分離試験1件失敗、先行9件成功だった。
現在の同fileは10件成功、終了コード0である。REDが修正前後を区別することを独立再現した。

【実測】`git diff --exit-code 354c57e...c4733cd -- <RED三file>`は終了コード0、空差分だった。
対応表補正は`tests/test_pilot_collaboration.py`一件、GREENは設定、runner、Evidenceの三件だけであり、各commitの
差分検査も終了コード0だった。

【判断】期限付き三試験の分類と残る恒久検査は妥当である。

1. 処理一覧試験は、固定commitからbaselineを再生成する恒久部分を残し、過去作業後の差分を一関数だけへ
   固定する部分を除いた。
2. 過去commit時点の全試験byte不変検査を除き、既存pilot commandとegress六fileの恒久検査を残した。
3. 現在の先端を過去v6 allowlistだけへ限定する試験を除き、使い捨てGitで許可外pathとhandoff配下へ隠した
   codeを検出する二試験を残した。この二試験は2件成功、終了コード0だった。

## 5. 設定、環境分離、製品側安全境界

【実測】`config/development-test-runner.json`は`runner_version: 2`で、
`test_environment_excluded_names`は次の六名と順序まで完全一致し、重複0件である。

```text
ANTHROPIC_API_KEY
ANTHROPIC_AUTH_TOKEN
ANTHROPIC_BASE_URL
ANTHROPIC_FOUNDRY_API_KEY
ANTHROPIC_VERTEX_PROJECT_ID
AWS_BEARER_TOKEN_BEDROCK
```

【実測】runnerは版確認後、全試験の直前に`os.environ`を複製し、複製から設定六名だけを除き、件数集計用の
一名を加えて子processへ渡す。親環境を直接変更しない。設定読込みは版2、六名の完全一致、fallback禁止、
receipt必須を検証する。

【実測】公式入口の受入試験は10件成功、終了コード0だった。六名を親へmarker付きで置く試験は、子環境に
六名がなく、無関係な名前と集計用名が残り、親の六名の値が実行後も同じであることを確認する。

【実測】製品側実行器は六名を除いた状態で28件成功、終了コード0だった。`ANTHROPIC_API_KEY`だけへ試験markerを
置いた認証禁止試験は1件成功、終了コード0であり、製品process起動前停止を維持する。製品側実装fileは本作業で
変更されていない。

## 6. 対応表、Git検査、公式試験

【実測】四試験fileの構文木から独立抽出した対応表は26 key、参照出現52件、重複を除く参照32件、未定義0件で
ある。`OUT-PC-006`は`test_pilot_git_processes_are_read_only`一件を参照する。対応表試験と同Git試験はそれぞれ
1件成功、終了コード0、同file全体は65件成功、終了コード0だった。

【実測】新規Git試験は現行の`_run_git`定義一件、直接call三件
`ls-tree`、`show`、`cat-file`を正常例とし、直接書込み`push`、`commit`、`reset`、`tag`、間接のalias、
`globals()`、無名関数、wrapper外`subprocess.run`を反例に持つ。これら宣言済み反例は検出されるが、
`CR-OTE-001`の構築名による`getattr`変種は検出されなかった。

【実測】固定公式receiptは`status=passed`、終了コード0、1,736 passed、failed 0、errors 0、skipped 0、
fallbackなし、Python 3.9.6、pytest 8.4.2、runner版2である。独立collectは1,736件、終了コード0で一致した。

【実測】独立レビューでも六名すべてを親processへ値`stage2-completion-review-presence`として与え、公式入口を
別receiptへ実行した。終了コード0、1,736 passed、failed 0、errors 0、fallbackなしだった。別receiptの
SHA-256は`4bbb99d9134bfb9171897df09bc82cfe003540c0b4ee0803ad890bcf868fc91c`であり、marker値を保持しなかった。
固定receiptにも作業担当のmarker値`stage2-presence`と六名自体は含まれていない。

## 7. 内容識別値、事後状態、対象外

【実測】Evidence §6の実行対象七fileのSHA-256は現在値とすべて一致した。固定receipt取得後に追加された
Evidence一件だけを`source_state_digest`の入力から除外して独立再計算すると、
`7596dfd8dbdb9fffdecd8babc7a107e8308cc589f12f05c1714c768735a04dde`となり、固定receiptと一致した。
Evidence作成後に実行対象code、設定、試験が変わっていないことを確認した。

【実測】最終worktreeはcleanである。`work_unit_transition --work-status completed`は終了コード0、
`status=passed`、`next_work_allowed=true`だった。補正commit直後の保留中GREENを未コミットとした中間結果と、
GREEN commit後の最終結果は区別されている。

【実測】Python、仮想環境、依存関係、`pyproject.toml`、製品側認証処理、v6要求本文、結果記録schemaは
変更されていない。Evidenceはpush、tag、amend、rebase、reset、force push、履歴書換え、外部送信を未実施と
記録する。Gitで機械確認できた作業commitは通常commitであり、外部操作の実施記録はない。

【未実施】本レビューは成果物、既存file、試験、設定、実装、TODO、Python環境を変更していない。実Git書込み、
push、外部送信、履歴書換え、Python 3.13移行、重大な欠陥12件の修復、第2段の採用表更新、第2段完了、
第3段以降を実施または承認していない。

## 8. 利用者判断境界と次の一作業

【判断】技術判定が`blocked`なので、本成果を第2段完了、テストコード管理候補の採用、Python 3.13移行の
根拠にしない。これらは、技術的な`verified`が得られた後も利用者が別に判断する境界である。

【次】利用者は`CR-OTE-001`について、製品側runtime allowlistを別の限定修正として承認するか、自動試験の
保証範囲を狭めて固定commitと事後Evidenceへ責務を戻すか、現行成果を未完了のまま保留するかを判断する。
レビュー担当は成果を修正せず、同じ完了レビューを自動反復しない。

## 9. 主な独立実行

各commandの終了コードを単独で判定した。

| 目的 | command | 終了コード | 結果 |
| --- | --- | ---: | --- |
| RED再現 | 固定RED commitの一時展開で`pytest -q tests/test_policy_test_runner.py` | 1 | 1 failed、9 passed。期待したRED |
| 公式入口受入 | `.venv/bin/python3 -m pytest -q tests/test_policy_test_runner.py` | 0 | 10 passed |
| 固定基準・egress | `.venv/bin/python3 -m pytest -q tests/test_claude_bootstrap_entrypoints.py` | 0 | 8 passed |
| 変更範囲恒久検査 | `.venv/bin/python3 -m pytest -q tests/test_pilot_collaboration_entrypoints.py` | 0 | 6 passed |
| 対応表補正file | `.venv/bin/python3 -m pytest -q tests/test_pilot_collaboration.py` | 0 | 65 passed |
| 製品側実行器 | 六名を除いて`pytest -q tests/test_claude_implementation_executor.py` | 0 | 28 passed |
| 製品側認証禁止 | API key試験marker付きで認証禁止nodeを実行 | 0 | 1 passed |
| 開発環境整合 | `.venv/bin/python3 -m pytest -q tests/test_development_environment.py` | 0 | 9 passed |
| 独立collect | `.venv/bin/python3 -m pytest --collect-only -q` | 0 | 1,736 collected |
| 独立公式入口 | 六名を親へ与えて`policy_test_runner --suite full` | 0 | 1,736 passed |
| Git検査反証 | 一時sourceを二つのpolicy関数へ入力 | 0 | 両方が違反0。偽陰性を実証 |
| 実行対象digest | Evidenceだけを除外して`_source_state_digest`を再計算 | 0 | 固定receiptと一致 |
| 作業単位移行 | `.venv/bin/python3 -m tools.development.work_unit_transition --work-status completed` | 0 | passed、次作業可 |
| 差分形式 | `git diff --check` | 0 | 問題なし |
