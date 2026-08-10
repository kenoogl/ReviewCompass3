# group A 共通guard修正 完了レビュー結果 v2

- レビュー日：2026-08-10
- collaboration mode：`role_neutral_pilot_review`
- Pilot：Claude／Reviewer：Codex／Closer：Codex
- レビュー段階：completion（完了レビュー、再レビュー）
- risk：`high`
- 対象：`records/session-handoffs/2026-08-10-claude-pilot-common-guard-fix-review-request-v2.md`
  （commit `46ad6717e6f0a3d9c95406f2d31ff55328263e79`）
- 先行レビュー：`records/session-handoffs/2026-08-10-codex-review-result-common-guard-fix-v1.md`
  （commit `fb0e2eaf74461e8e1f279c88d8ade2cc43ada192`、`reported_unverified`）
- 判定：**verified**
- Finding：blocking 0件、non-blocking 0件、defer 0件
- v1 Finding：`F-CG-COMP-001`は**解消**
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`

## 1. 固定入力と開始状態

【記録】Human裁定は2026-08-10「テスト修正を承認する」。許可された修正は、v1で指摘した
`test_validate_record_rejects_non_json_compatible_record`の入力訂正と、そのEvidence・receipt・
再レビュー依頼の固定である。Reviewerの許可範囲は読取り、独立検証、本判定record 1件の新規作成と
単独commitであり、code、test、既存record、config、schema、上流設計、TODOの恒久変更は禁止した。

【実測】レビュー開始時のbranchは`main`、HEADは`46ad671`、worktreeとindexはcleanだった。
対象commitの親は`bf2163c`で、修正列は次の直列3 commitだった。

| commit | 親 | 内容 |
| --- | --- | --- |
| `9461f34` | `fb0e2ea` | 対象test入力の修正 |
| `bf2163c` | `9461f34` | Evidence §7追記、公式receipt v2追加 |
| `46ad671` | `bf2163c` | 再レビュー依頼record追加 |

【実測】固定入力と依頼成果物のSHA-256を内容から再計算した。主要値は次のとおりで、scope、
先行判定、Evidence、依頼recordの記載値と一致した。

| 対象 | SHA-256 |
| --- | --- |
| group A判定record | `34a53581751a5b23864933b3ab23e08a875170ab5cdbe08e00e112c803da5139` |
| scope v1 | `b9a7f49ad5897525e2f572c6da86d2f09b083d8dc108ab798fd5c00fb631d163` |
| scope v2 | `b10f34c38b09d623bfbd37af6b19fce024a2f36b2ffbac9503d96c5d82d8d2d7` |
| 範囲レビューv2 | `68f1e4fa3b1f00437399a3cc5f7cef930715a01eac1f963cb1d0d91719858f91` |
| 完了レビューv1 | `4be0042f9ef22475921749013a1ec21d1912b2b51db5d14db3dcb783a74e99f5` |
| 修正後Evidence | `37d3618f4a2d252f6142c4111120a253ef5c1f54fd967272d0396d4517bf823a` |
| Pilotの公式全Test receipt v2 | `614866bfefdc830c521c46d99ab05421b1f26858a4775344be8186f3a22bb892` |
| 再レビュー依頼record | `6abf3cf02701e6ff4fccf4faf17d23997472da76096e1cb4d6798d833ec13f91` |

## 2. 修正範囲と検査性質

【実測】`9461f34`の変更は`tests/test_common_digests.py`の対象test 1件だけで、15行追加・
1行削除だった。不一致値`"0" * 64`を削除し、修正前のcanonical仕様
（`ensure_ascii=False`、区切り文字固定、key順固定、`allow_nan`既定）でNaN record自身から
Digestを計算する入力へ置き換えていた。追加分はこのDigest計算と、理由を説明するdocstringだけである。
testの追加・削除、期待する例外、他の入力、他のtest、実装は変更されていない。

【実測】`bf2163c`は既存Evidenceの§7追記と新規receipt v2だけ、`46ad671`は再レビュー依頼recordの
追加だけだった。`fb0e2ea..46ad671`の変更pathは、対象test、許可されたEvidence、receipt v2、
依頼recordの4件だけだった。`git diff --check fb0e2ea..46ad671`は終了コード0だった。

【実測】元base `17c2002`から対象commitまで、config、schema、`docs/current`、上流設計、
`TODO_NEXT_SESSION.md`の変更は0件だった。元baseに存在した`records/development`の変更も0件である。
修正列で変更された既存recordは、Human承認後の追記対象として明示されたEvidence 1件だけだった。

【判断】修正は当該test 1件の入力に閉じ、他のtestの検査性質を弱めていない。Human承認と変更範囲は
一致している。

## 3. F-CG-COMP-001の解消確認

【実測】主worktreeを汚さない一時worktreeをcommit `46ad671`から作り、次の実装3 fileだけを
`a84b8ca`へ切り替えた。

- `tools/common/digests.py`
- `tools/common/paths.py`
- `tools/task_contract/identity.py`

【実測】切替後、3 fileは`a84b8ca`と差分0、修正後の`tests/test_common_digests.py`は
`46ad671`と差分0であることを先に確認した。その状態で次を単独実行した。

```text
/Users/Daily/Development/ReviewCompass3/.venv/bin/python3 -m pytest -q \
  tests/test_common_digests.py::TestJsonCompatibilityIsEnforced::test_validate_record_rejects_non_json_compatible_record
```

結果は`1 failed in 0.03s`、終了コード1で、失敗理由は
`Failed: DID NOT RAISE <class 'tools.task_contract.identity.ContractError'>`だった。

【実測】一時worktreeの3 fileを`46ad671`へ復元して同じtestを再実行すると、
`1 passed in 0.02s`、終了コード0だった。復元後のindexとworktreeがcleanであることを確認し、
一時worktreeを削除した。主worktreeもcleanのままだった。

【判断】修正後testは、修正前仕様で自己整合するNaN recordを修正前実装が受け入れる欠陥を直接検出する。
Digest不一致という別理由で合格する経路は閉じた。v1の`F-CG-COMP-001`
（blocking／completion／§11.1類型3・類型4）は解消した。

## 4. v1で確認済みの事項の維持

### 4.1 F-A1とF-A2

【実測】F-A1について、非文字列key、tuple、NaNをそれぞれ
`canonical_content_digest`、`canonical_bytes`、`seal`、修正前仕様の正しい旧Digestを持つ
`validate_record`へ直接流した。全経路が所定の停止codeで拒否され、有限数・list・文字列keyの正例は
合格した。Pilotのfixtureにない反証として`Decimal("1.25")`も拒否された。終了コードは0だった。

【実測】F-A2について、`/private/tmp`の実在directoryでcase差とNFC/NFD差だけのpathが
`os.path.samefile == True`であり、`within == True`であることを確認した。case別名配下のchildも
`True`だった。root外、rootの親、root内からroot外へ向くsymlinkは`False`、存在しないroot内pathは
`True`、存在しないroot外pathは`False`だった。終了コードは0だった。

【判断】F-A1・F-A2の反証は現行実装に対して不成立のままで、拒否側と正例側の性質を維持している。

### 4.2 実台帳Digest

【実測】v1と同じ実台帳3件は`a84b8ca..46ad671`でbytes差分0だった。各recordについて、
Python標準JSON処理とSHA-256による独立計算、現在の共通関数、recordの宣言値を再照合し、
次の値で3者が一致した。

| record | 再計算・照合したDigest |
| --- | --- |
| `records/development/2026-08-04-issue-resolution-pilot-wi-001-snapshot-boundary-candidate-v1.json` | `f037398f905ed48973b6a059b5f59bf3b36b6f35097ea819716be7aeda107cc2` |
| `records/development/2026-08-05-task-contract-source-pin-todo-compaction-v2.json` | `ac6670d083e251d1a15e15588bdf17651e2d4e4e7b2686ea42ef61aa9167eb5e` |
| `records/development/2026-08-07-layer3-reuse-search-attestation-v1.json` | `d13344fa526baa2aff6f15d90a7bceec9785e135682633f605da4634f5b04f7b` |

【判断】実台帳のDigestは修正前から不変で、scope v1 §8-2・§8-3の停止条件に該当しない。

### 4.3 pinと共通正本への直結

【実測】`tests/test_common_module_pins.py`の`a84b8ca..46ad671`差分は、
`tools/common/digests.py`と`tools/common/paths.py`のpin値2件だけだった。key 5件、検査logic、
その他のbytesは不変で、現行pin値は各実装fileから再計算したSHA-256と一致した。

| file | 現行SHA-256 |
| --- | --- |
| `tools/common/digests.py` | `fc2d728c4c2cfd1b4e70b7eef6d0e6d4ce9a4a033712b93402bd2c7f984624f7` |
| `tools/common/paths.py` | `039512f579bf6e939d4086c1e75f848b0b4e5dba7f7170b63c21fd005b48e1ec` |
| `tools/task_contract/identity.py` | `fddffe6617c225e9fbedd33ea722316ea41f37c1f76c93cfbce3060ed55b5422` |

【実測】Pythonのobject同一性で、`tools.task_contract.identity.content_digest is
tools.common.digests.canonical_content_digest`が`True`だった。

【判断】pin更新は2値だけであり、`identity.content_digest`は共通正本へ直結したままである。

## 5. TestとDigestの独立再実行

【実測】関連5 test fileを単独commandで実行した。

```text
.venv/bin/python3 -m pytest \
  tests/test_common_digests.py tests/test_common_errors_paths_output.py \
  tests/test_common_module_pins.py tests/test_shared_function_sweep.py \
  tests/test_first_review_task_contract_e2e.py
```

結果は`125 passed in 0.51s`、終了コード0だった。

【実測】公式runnerを次の単独commandで実行した。

```text
.venv/bin/python3 -m tools.development.policy_test_runner \
  --suite full \
  --receipt /private/tmp/2026-08-10-codex-review-common-guard-fix-v2-full.json
```

結果は`1451 passed in 10.86s`、failed 0、error 0、skipped 0、status `passed`、終了コード0、
`fallback_used=false`だった。Reviewerの一時receiptのSHA-256は
`857e4548fc053c7e849c5b62e49ac58a4d324affaa958a472a265ff8547a41d9`である。

【実測】修正後成果物のSHA-256は再レビュー依頼の値と一致した。

| file | SHA-256 |
| --- | --- |
| `tests/test_common_digests.py` | `c5b23a77222693afece6f38848a6c111d5f7d9428fa806116952c15760972b2c` |
| Evidence | `37d3618f4a2d252f6142c4111120a253ef5c1f54fd967272d0396d4517bf823a` |
| Pilotの公式receipt v2 | `614866bfefdc830c521c46d99ab05421b1f26858a4775344be8186f3a22bb892` |

## 6. §11区分と判定

| §11区分 | 件数 | 根拠 |
| --- | ---: | --- |
| 類型1：上流authorityとの矛盾 | 0 | 観測なし |
| 類型2：Human境界・必要な承認の欠落 | 0 | test修正のHuman承認を確認 |
| 類型3：誤った合格を許す受入条件・検証の欠陥 | 0 | F-CG-COMP-001の赤・緑を独立再現して解消確認 |
| 類型4：禁止事項違反またはscope・schema境界の破り | 0 | 修正pathと内容は承認範囲内 |
| non-blocking | 0 | なし |
| defer | 0 | なし |

【判断】§11の比例原則に従い、blockingは閉じた4類型だけで判定した。v1で挙げなかった新規論点、
実装方式の好み、scope外の将来設計を後出ししていない。

判定：**verified**。

【判断】F-CG-COMP-001は解消し、元のF-A1・F-A2受入条件、正例Digest、pin、共通正本への直結、
関連Test、公式全Test、変更禁止範囲まで再確認できた。必須Evidenceが揃い、Pilotの報告と事後状態が
一致するため、完了レビューの受入条件を満たす。

## 7. Human境界、未実施、次

【実測】レビュー中にcode、test、既存record、config、schema、上流設計、TODO、checklistを
恒久変更していない。検証用の一時worktreeは現行内容へ復元してcleanを確認後に削除した。
外部送信、push、tag、amend、rebase、reset、不可逆操作も行っていない。本判定recordだけを
新規作成した。

未実施：Closerの完了projection、group B・C・Dの17件、TODO・checklist反映、外部操作。

次：Humanが本`verified`判定を確認し、Closerの完了projection開始可否を判断する。
