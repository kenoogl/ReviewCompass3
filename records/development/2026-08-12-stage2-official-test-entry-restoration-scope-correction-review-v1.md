# 第2段 公式試験入口の正常化 範囲修正後確認 v1

- レビュー記録ID：`REV-STAGE2-OFFICIAL-TEST-ENTRY-RESTORATION-SCOPE-CORRECTION-001`
- レビュー日：2026-08-12
- レビュー担当：作業担当とは異なる実行単位
- 対象作業票：`docs/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-work-ticket-v3.md`
- 作業票ID：`BTW-STAGE2-OFFICIAL-TEST-ENTRY-RESTORATION-003`
- 作業票SHA-256：`7dc25beaf1af7bb22cbb9a0f1a4401babcda53cce66d6e5c7c19793b9ec4d6b1`
- 作業票コミット：`df7966b3d72f2e65d7e63a73532fe8697d818a5e`
- 前回レビュー：`records/development/2026-08-12-stage2-official-test-entry-restoration-scope-extension-start-review-v1.md`
- 前回レビューSHA-256：`76fe16bda12de34727840cffde88b706e6ad56591e3fc2ce7641c2c6e375f133`
- 前回レビューコミット：`aa8ed0ededac8acec2b431747ee7d91b98e546bb`
- REDコミット：`354c57e1d7dd28eaa6b2e271ea3dae60ce949720`
- 危険度：`high`
- 判定：`修正要`

## 1. 判定

【判断】v3は、`OUT-PC-006`を変更範囲二試験へ対応させる誤りを除き、Git書込み禁止を一件の恒久試験、
意味的に完結したcommit・停止・Gitと外部操作の事後状態を完了Evidenceへ分けた。この責務分担は、自動試験だけで
要求全体を証明済みとしないため妥当である。

しかし、提案された「直接の`_run_git`呼出しを列挙し、第二引数を検査する」方式は、`_run_git`を別名または
動的参照で呼ぶGit書込みを列挙しない。現行process検査もこの迂回を違反にしないため、v3の期待する
「将来のGit書込み追加を失敗させる」を満たさず、対応済みとして誤って合格できる。

【実測】前回指摘`SR-SE-001`は、要求と変更範囲試験の虚偽対応、および試験とEvidenceの責務混同については
解消したが、静かな迂回による誤った合格が残るため、全体として未解消である。残る止める指摘は1件である。

## 2. 前回指摘の確認

| 前回指摘の要素 | v3の修正 | 確認結果 |
| --- | --- | --- |
| `OUT-PC-006`を変更範囲二試験へ誤対応 | 新設`test_pilot_git_processes_are_read_only`一件へ変更 | 【判断】解消 |
| commit、停止、push・履歴書換え・外部送信まで自動試験で証明したように見える | 静的なGit書込み禁止と、Git履歴・作業単位移行・外部操作なしの完了Evidenceを分離 | 【判断】解消。完了レビューでは試験結果と事後Evidenceを別々に確認する必要がある |
| 現行process検査が直接literal配列の`git push`を受理 | `push`、`commit`、`reset`、`tag`を直接`subprocess.run`と直接`_run_git`の反例に追加 | 【判断】方向は妥当だが、間接`_run_git`呼出しを見逃すため未解消 |

## 3. 残る止める指摘

| ID | 区分 | 段階 | 根拠類型 | 事象 | 必要な修正 |
| --- | --- | --- | --- | --- | --- |
| `SR-SC-001` | blocking | scope | `work-review-protocol` §11.1 類型3 | v3が定める直接`_run_git` callsite列挙の模擬では、直接`push`は違反1になる一方、`git_writer = _run_git`、`globals()["_run_git"]`、lambdaへ渡した`_run_git`から`push`する三変種は違反0となった。現行`_process_policy_violations`も三変種すべて空の違反一覧を返す。新試験が成功してもGit書込みを追加できる偽陰性である | 一件の新試験と一時source反例の範囲内で、`_run_git`の別名化、動的解決、call targetとして直接使わない参照を拒否する受入条件を作業票へ明記する。少なくとも確認した三変種が失敗し、現行の直接三callだけが成功することを固定する。これを同一file内で検査できない場合だけ、製品側runtime allowlistを別案として利用者へ返す |

【判断】alias、`globals`動的解決、lambda渡しは、同じ「直接callsiteだけを数える」原因の変種なので一件へ
まとめた。直接`subprocess`のalias・dynamic経路は既存反例17件が成功しており、今回の残存原因は`_run_git` wrapperの
間接呼出しに限定される。

## 4. 範囲、allowlist、Evidence境界

【実測】現行`tools/development/pilot_collaboration.py`の直接`_run_git` callsiteは3件で、第二引数は
`ls-tree`、`show`、`cat-file`である。すべて読取り操作で、v3のallowlistと一致する。直接`push`へ変える一時sourceは
callsite違反1となった。

【判断】追加path一件、新しい恒久試験一件、`TRACEABILITY`三key、process反例だけという範囲は最小である。
`SR-SC-001`の修正も、同じ新試験へ間接呼出しの反例を足すだけならこのpath・試験数・製品code不変を維持できる。

【判断】新試験は製品codeにGit書込みcallsiteがないことだけを確認し、意味的に完結したcommit、作業担当の停止、
push・履歴書換え・外部送信なしは、結果commit、Git事後状態、作業単位移行と操作記録を完了Evidenceで別確認する
v3の分離が妥当である。保持中GREENがあるため、作業単位移行の最終確認は、補正commit後ただちにcleanを要求せず、
GREENとEvidenceを意味的に完結したcommitへ固定した作業末尾で行う必要がある。

【実測】v3は追加文書一件だけのcommitである。v1のRED三file、保持中GREEN二file、Python、製品code、v6要求本文を
変更していない。現在の未コミット差分は、従前から保持される`config/development-test-runner.json`と
`tools/development/policy_test_runner.py`だけである。

## 5. 機械確認結果

合否は各commandの終了コードを単独で確認した。

| 目的 | 実行内容 | 終了コード | 結果 |
| --- | --- | ---: | --- |
| 固定材料 | `shasum -a 256`、`git rev-parse`、`git show --stat` | 0 | v3と前回レビューのSHA、commit、v3の一file差分が固定値と一致 |
| 現行callsite抽出 | Python構文木で`_run_git`直接callの第二引数を抽出 | 0 | `ls-tree`、`show`、`cat-file`の3件、allowlist違反0 |
| 直接書込み反証 | 一時sourceへ直接`_run_git(repository, "push")`を追加 | 0 | callsite違反1 |
| 間接呼出し反証 | 一時sourceへalias、`globals`、lambda経由の`push`をそれぞれ追加 | 0 | 全三変種でcallsite違反0、process違反0 |
| 既存process反例 | `test_process_policy_rejects_alias_popen_check_and_dynamic_routes` | 0 | 17件成功。直接process側の既存迂回検査は維持 |
| RED・既存差分 | `git diff --name-only` | 0 | RED三fileにRED commit後の追加変更なし。作業treeの対象外差分は保持中GREEN二fileだけ |
| 差分検査 | `git diff --check`、`git diff --cached --check` | 0 | 問題なし |

## 6. 利用者判断境界、未実施、次の一作業

【記録】技術的な修正後確認は、新しい恒久試験と対応表の意味変更を承認しない。利用者が新たに判断する対象は、
`tests/test_pilot_collaboration.py`一件で、対応表三key、新しいGit読取り限定試験一件、直接Git書込み四種の反例に加え、
`SR-SC-001`の間接`_run_git`反例を扱う修正版の範囲である。製品code、要求本文、RED三file、保持中GREEN、
Python 3.13、第2段完了、外部送信の承認は含まない。

【未実施】作業票、対応表、試験、設定、実装、Evidence、TODO、保持中GREENは変更していない。公式全試験、
新しい恒久試験、実Git書込み、push、外部送信、履歴書換え、第2段の採用・完了判断は実施していない。

【次】本確認は一回限りなので自動的に再レビューしない。操縦役は、`SR-SC-001`の三反例を同一file・同一新試験の
範囲へ明記した修正版と、現行範囲のままでは開始しない選択を利用者へ返す。
