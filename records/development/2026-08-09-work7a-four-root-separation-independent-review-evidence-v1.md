# Work 7A 4種root分離 独立レビューEvidence v1

- 実施日：2026-08-09
- reviewer：Codex
- Human指示：Claude作業終了後の独立確認、続く「次へ」による完了反映
- risk：`high`（filesystem write境界の守り役）
- 元指示書：`records/session-handoffs/2026-08-08-codex-to-claude-work7a-four-root-separation.md`

## 1. 対象commitと修復系列

| role | commit |
| --- | --- |
| 元実装base | `ebc0bffdc42b7595727701788094fc74d201da04` |
| 元RED | `b006e603e3e32c0baec47ec0c2fc87a3161b6abe` |
| 元GREEN | `663ec503ce92307332a532af7b3eb7259b0b0fe3` |
| symlink差替え修正RED | `2239a02bb0d19d1d3f339cf74d654b0ee0c7cf15` |
| symlink差替え修正GREEN | `6f1c41708c606099139ba71d3ad0d529b25c536c` |
| 例外連鎖path修正RED | `b77e044d9a51343e94adebe6e71fcb49380c3acd` |
| 例外連鎖path修正GREEN | `58e2533ee83706554f92949a90c72cc5437baf8c` |

【実測】各REDは指定Testだけ、各GREENは実装、対応GREEN Evidence、公式receiptだけを変更した。
GREENで直前のRED Testは変更されず、指示外pathと先行commitの履歴書換えは0件だった。

## 2. 先行不一致と修復

### 2.1 runtime root差替え

元GREEN後、未作成runtimeを解決してからruntime pathをinstall rootへのsymlinkへ差し替える
独立反証を実行した。元実装はsymlinkを辿って
`<install_root>/projects/<project_id>/runtime/sensitive`を作成し、install rootのmodeも変更し得た。
元`completed_claim`を`report_execution_mismatch`として完了反映を停止した。

修正は初期化前のread-only root identity再検査である。runtime本体、`projects` component、
未作成runtime祖先の3種の差替えは、全て`runtime_initialization_target_invalid`で
Layout初期化を呼ぶ前に停止する。installとprojectのinventory、SHA-256、mode、mtimeは不変で、
symlink先へのartifact作成は0件だった。

### 2.2 原因例外からのhost path漏洩

最初の修正後、runtimeを自己参照symlink loopへ差し替える独立反証を実行した。
filesystem writeは停止したが、path入り`RuntimeError`が`RootSeparationError.__cause__`へ残り、
「例外連鎖にpathを含めない」というClaimと不一致だったため、再度完了反映を停止した。

修正は`OSError`／`RuntimeError`のhandler外でstop errorをraiseし、原因例外objectを
cause／contextへ連結しないことに限定した。実symlink loopと強制`RuntimeError`で
`__cause__ is None`、`__context__ is None`、表示tracebackへの入力path・marker漏洩なしを確認した。

## 3. 最終成果物Digest

| artifact | SHA-256 |
| --- | --- |
| `tools/deployment/local_integrated_roots.py` | `31e4e319c366cfbf51d58b691c11bdf6fb7c43636ac9ad3bfa7777c43cb5a149` |
| `tests/test_work7a_local_integrated_root_separation.py` | `7ec546a5aa6784cbce1c126f2950a80ee21d43459780aae8f267b7dbdd8b1d88` |
| 元GREEN Evidence | `bcbeac855d73528f8c5c002797b63429853d59eb15286a1de35e1344bdfcd864` |
| symlink差替え修正GREEN Evidence | `49d557782f59f7435c8359a3b3e42e393bd24e752283bebfbd18aee2ad737159` |
| 例外連鎖path修正GREEN Evidence | `f3896c8a2d4ec74003ce7633621bef65e41f18906b2e105c0e3d55eb77867239` |
| 独立レビュー公式receipt | `a88ee495c3d473cea2c6de60439e6a17c13d5070fa67f1c1d1984601dbc16f7f` |

## 4. 独立再実行

各commandはpipeや`;`連結を使わず、単独commandのexit codeで判定した。

| oracle | command | result |
| --- | --- | --- |
| targeted | `.venv/bin/python3 -m pytest tests/test_work7a_local_integrated_root_separation.py` | `33 passed`、exit `0` |
| related | `.venv/bin/python3 -m pytest tests/test_project_runtime_layout.py tests/test_layout_baseline.py tests/test_task_python_cache.py` | `46 passed`、exit `0` |
| official full | `.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt records/development/2026-08-09-work7a-four-root-separation-independent-review-test-receipt-v1.json` | `1315 passed`、exit `0`、fallback `false` |

公式receiptのSHA-256は
`a88ee495c3d473cea2c6de60439e6a17c13d5070fa67f1c1d1984601dbc16f7f`。

## 5. reviewer独自oracle

最終GREEN後、Claudeのfixtureに無い`OSError`経路を一時directoryの合成fixtureだけで実行した。
解決済みrootの初期化前再検査で、入力path markerを含む`OSError`を`Path.resolve()`から発生させた。

【実測】public initializerは`runtime_initialization_target_invalid`で停止し、
`__cause__`と`__context__`はともに`None`、表示tracebackへのmarkerと入力path漏洩は0件、
runtime artifact作成は0件だった。commandはexit `0`、出力は
`INDEPENDENT_COUNTEREXAMPLE_PASSED`だった。

## 6. 受入条件の照合

- 4 root identity：install＝承認済み`code_root`相当、project＝Project Manifestのcheckout、
  runtime＝Layout v3外部root、sensitive＝runtime profile内専用rootとして解決される。
- 物理分離：install、project、runtimeはcanonical identityで非overlap。sensitiveは承認済みLayout v3
  どおりruntime配下にあり、他のruntime kindと別identityである。
- write境界：4 root kindは宣言root配下だけを許可し、runtime一般writeからsensitiveを除外する。
  cross-root、prefix sibling、symlink escape、未知kindをfail-closedに拒否する。
- 初期化境界：通常時はruntime祖先とsensitiveだけを作成し、解決後の完了済みfilesystem差替えは
  副作用前に拒否する。
- 正例・負例・境界例：targeted 33件と独立oracleで合格した。

## 7. 判定と未実施

【判断】`verified / completed`。Work 7A第1項「install、project、runtime、sensitiveの各rootを
分離した」の完了根拠として使用できる。先行2件の`report_execution_mismatch`は修復Evidenceと
独立反証で置換済みである。

【未実施】初期化syscallと同時の別process競合を防ぐ原子的filesystem protocol、Project Bindingの
耐久保存、別checkout／project移動後のSnapshot／Change Set復元、Work 7A第3項以降、実deployment、
実ホーム・既存dataへのaccess、外部送信、pushは行っていない。原子的競合防止は本縦切りの
完了Claimに含めず、後続候補として保持する。
