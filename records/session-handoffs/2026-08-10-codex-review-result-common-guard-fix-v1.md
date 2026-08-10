# group A 共通guard修正 完了レビュー結果 v1

- レビュー日：2026-08-10
- collaboration mode：`role_neutral_pilot_review`
- Pilot：Claude／Reviewer：Codex／Closer：Codex
- レビュー段階：completion（完了レビュー）
- risk：`high`
- 対象：`records/session-handoffs/2026-08-10-claude-pilot-common-guard-fix-review-request-v1.md`
  （commit `e63649c6c6e34ead38cc4d6f68dad3311906ac3e`）
- 判定：**要修正（`reported_unverified`）**
- Finding：blocking 1件、non-blocking 0件、defer 0件
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`

## 1. 固定入力と開始状態

【記録】固定scopeはv1（commit `3594172`）と、commit境界・変更可能path・受入条件5だけを
差し替えたv2（commit `35d2fe6`）である。範囲レビューv2（commit `9fd43ba`）の判定は
`verified`である。

【実測】固定入力と依頼成果物を内容から再計算した。主要なSHA-256は次のとおりで、scope、
先行判定record、Evidence、依頼recordの記載値と一致した。

| 対象 | SHA-256 |
| --- | --- |
| group A判定record | `34a53581751a5b23864933b3ab23e08a875170ab5cdbe08e00e112c803da5139` |
| scope v1 | `b9a7f49ad5897525e2f572c6da86d2f09b083d8dc108ab798fd5c00fb631d163` |
| scope v2 | `b10f34c38b09d623bfbd37af6b19fce024a2f36b2ffbac9503d96c5d82d8d2d7` |
| 範囲レビューv2 | `68f1e4fa3b1f00437399a3cc5f7cef930715a01eac1f963cb1d0d91719858f91` |
| GREEN Evidence | `653106b0e9eabc48cfb716b0efa55eb08d6de18e0f8da7c586192b6a07a131a4` |
| Pilotの公式全Test receipt | `429ca5d4ae990893837df90509837fc5f2e6f73ff83438e6fb87bda38cdb3fd5` |
| レビュー依頼record | `b146d541a32e1a7fd6ab0e2c00362f4b81a6cf88d41a04677525c26d1219f898` |

【実測】レビュー開始時のbranchは`main`、HEADは`e63649c`、worktreeとindexはcleanだった。
scope v1に固定されたFinding、裁定、上流設計、レビュー基準、TODOのSHA-256は5件とも一致した。
初期開発チェックリストが固定するIntent、用語集、Plan、開発方針、方針DecisionのSHA-256も
5件とも一致した。

## 2. commit列と変更範囲

【実測】`17c2002..e63649c`は、scope v1、範囲レビューv1、scope v2、範囲レビューv2、RED、
GREEN、レビュー依頼の直列7 commitであり、親子関係に分岐や履歴書換えはなかった。

【実測】RED commit `a84b8ca`の変更は次のtest 2件への追加だけだった。

- `tests/test_common_digests.py`：119行追加
- `tests/test_common_errors_paths_output.py`：56行追加

【実測】GREEN commit `b20d76b`の変更は、scope v2 §2で許可した実装3件、pin 1件、
新規Evidence 1件、新規receipt 1件だけだった。REDのtest 2件、
`tests/test_shared_function_sweep.py`、`tests/test_first_review_task_contract_e2e.py`は
GREENで変更されていない。依頼commit `e63649c`は依頼record 1件だけの追加だった。

【実測】`17c2002..e63649c`でconfig、schema、`docs/current`、上流設計、
`TODO_NEXT_SESSION.md`の変更は0件だった。`records/development`は許可されたEvidenceとreceiptの
新規2件だけで、既存recordの変更は0件だった。

## 3. 元Findingの反証照合

### 3.1 F-A1：非JSON互換入力

【実測】group A判定record §4のD1・I2と同じ欠陥入力を直接流した。非文字列key、tuple、NaNは、
`canonical_content_digest`では`digest_input_not_json_compatible`、`canonical_bytes`、`seal`、
`validate_record`では`schema_violation`として全件拒否された。`validate_record`には修正前の
canonical仕様で計算した正しい旧Digestを与え、Digest不一致による別理由の拒否ではないことを
切り分けた。対応する文字列key、list、有限数の正例はDigest計算に合格した。commandの終了コードは0。

【実測】Pilotのfixtureにない追加反証として`Decimal("1.25")`を含む入力を試した。
`canonical_content_digest`、`canonical_bytes`、`seal`はすべて所定の停止codeで拒否した。
commandの終了コードは0。

【判断】現行実装上では、D1・I2の非文字列key、tuple/list衝突、非有限数による反証は不成立である。

### 3.2 F-A2：case差・NFC/NFD差

【実測】`/private/tmp`の実在directoryで、case差とNFC/NFD差だけのpathがそれぞれ
`os.path.samefile == True`であることを独立oracleとし、`within == True`を確認した。
case別名配下の実在childも`True`だった。独立commandの終了コードは0。

【実測】同じcommandで、root外のsibling、rootの親、root内からroot外へ向くsymlinkは
すべて`False`だった。存在しないroot内pathは`True`、存在しないroot外pathは`False`で、
従来の解決後path判定を維持した。

【判断】現行実装上では、P1・P3のcase差・NFC/NFD差による反証は不成立であり、root外を
誤って内側とする回帰も観測しなかった。

## 4. 正例のDigest回帰照合

【実測】次の実台帳3件をReviewerが明示選択し、RED commit `a84b8ca`時点のbytes、現在bytes、
Python標準JSON処理とSHA-256による独立計算、現在の共通関数、recordの宣言値を照合した。
3件とも修正前後のbytesが同一で、4つのDigest値が一致した。commandの終了コードは0。

| record | 再計算・照合したDigest |
| --- | --- |
| `records/development/2026-08-04-issue-resolution-pilot-wi-001-snapshot-boundary-candidate-v1.json` | `f037398f905ed48973b6a059b5f59bf3b36b6f35097ea819716be7aeda107cc2` |
| `records/development/2026-08-05-task-contract-source-pin-todo-compaction-v2.json` | `ac6670d083e251d1a15e15588bdf17651e2d4e4e7b2686ea42ef61aa9167eb5e` |
| `records/development/2026-08-07-layer3-reuse-search-attestation-v1.json` | `d13344fa526baa2aff6f15d90a7bceec9785e135682633f605da4634f5b04f7b` |

【判断】代表する既存台帳recordのDigest値に回帰はなく、scope v1 §8-3の停止条件には該当しない。

## 5. pinと共通正本への結線

【実測】`tests/test_common_module_pins.py`を`a84b8ca`とGREEN後で機械比較した。`_PINS`のkeyは
5件で同一、検査logicとその他のbytesは同一で、変更は次の2値だけだった。2値は現在の実装bytesから
再計算したSHA-256とも一致した。commandの終了コードは0。

- `tools/common/digests.py`：`db6b8305...`から`fc2d728c...`へ更新
- `tools/common/paths.py`：`daa32579...`から`039512f5...`へ更新

【判断】pin更新はscope v2 §2が許可した唯一のGREEN test変更の範囲内である。

【実測】Pythonのobject同一性で、`tools.task_contract.identity.content_digest is
tools.common.digests.canonical_content_digest`が`True`だった。
`tests/test_shared_function_sweep.py`を含む対象Testも合格した。

【判断】`identity.content_digest`は共通正本へ直結したままで、写しの禁止要求を維持している。

## 6. TestとREDの独立再実行

【実測】RED commit `a84b8ca`をrepository外の一時directoryへ展開し、次を単独実行した。

```text
/Users/Daily/Development/ReviewCompass3/.venv/bin/python3 -m pytest \
  tests/test_common_digests.py tests/test_common_errors_paths_output.py \
  tests/test_common_module_pins.py tests/test_shared_function_sweep.py \
  tests/test_first_review_task_contract_e2e.py
```

結果は`15 failed, 110 passed in 0.63s`、終了コード1だった。失敗15件は、非文字列key・tuple・
非有限数の非拒否8件、Digest衝突2件、`seal`と`canonical_bytes`の非拒否2件、case別名・
NFC/NFD別名・case別名配下childの誤判定3件であり、F-A1・F-A2の反証そのものだった。
既存のpin、共通結線、Task Contract E2EはRED時点でも合格した。

【実測】現行HEADで同じ5 test fileを単独実行し、`125 passed in 0.51s`、終了コード0だった。

【実測】公式runnerを次で独立実行した。

```text
.venv/bin/python3 -m tools.development.policy_test_runner \
  --suite full \
  --receipt /private/tmp/2026-08-10-codex-review-common-guard-fix-full.json
```

結果は`1451 passed in 10.92s`、failed 0、error 0、skipped 0、status `passed`、終了コード0、
`fallback_used=false`だった。一時receiptのSHA-256は
`03647aa4f108f618befd8cefa5879c5e11d742ee7cd7ba164f39a506000cc29d`である。

## 7. Finding

### F-CG-COMP-001 blocking／completion／§11.1類型3・類型4

対象：`tests/test_common_digests.py`の
`test_validate_record_rejects_non_json_compatible_record`

【実測】RED commit `a84b8ca`でこのtestだけを単独実行すると、`1 passed in 0.02s`、終了コード0だった。
testはNaNを含むrecordへ`"0" * 64`という不一致Digestを置くため、非JSON互換検査がなくても
Digest不一致だけで`ContractError`になり合格する。

【実測】同じRED commitの実装へ、group A判定record I2と同じ条件、すなわち修正前のcanonical仕様で
計算した正しいDigestを持つNaN recordを渡すと、`validate_record`はrecordを合格させた。
出力は`accepted: true`、終了コード0だった。したがって、対象欠陥が存在する状態でも新設testが
合格することを機械で再現した。

【判断】これは「誤った合格」を検出できない検証の偽陰性であり、§11.1類型3のblockingである。
また、scope v1 §6が固定した「実装前に新規testが反証どおり失敗する」というRED境界を、
`validate_record`の受入条件について満たしていないため類型4にも該当する。現在の実装挙動が正しいこと、
全Testが合格すること、既存testを弱めていないことはこの偽陰性を閉じない。

【判断】実装方式の好み、将来設計、scope外fixtureをFindingにはしていない。

## 8. §11区分と判定

| §11区分 | 件数 | 根拠 |
| --- | ---: | --- |
| 類型1：上流authorityとの矛盾 | 0 | 観測なし |
| 類型2：Human境界・必要な承認の欠落 | 0 | risk確定、着手承認、RED開始承認、範囲レビューを確認 |
| 類型3：誤った合格を許す受入条件・検証の欠陥 | 1 | F-CG-COMP-001 |
| 類型4：禁止事項違反またはscope・schema境界の破り | 1 | F-CG-COMP-001と同一Finding |
| non-blocking | 0 | なし |
| defer | 0 | なし |

判定：**要修正（`reported_unverified`）**。

【判断】F-A1・F-A2の現行実装挙動、正例、変更範囲、pin、共通正本への結線、対象Test、
公式全Testは確認できた。しかしF-CG-COMP-001が、修正前に失敗する回帰Testという必須の
RED Evidenceと恒久検査を欠かせるため、`verified`にはできない。完了報告と事後状態の競合ではないため
`report_execution_mismatch`ではなく、正しい途中停止でもないため`blocked`ではない。

## 9. Human境界、未実施、次

【実測】レビュー中にcode、test、既存record、config、schema、上流設計、TODO、checklistを変更していない。
外部送信、push、tag、amend、rebase、reset、不可逆操作も行っていない。本判定recordだけを新規作成した。

未実施：F-CG-COMP-001の修正、Closer作業、group B・C・Dの17件、TODO・checklist反映、外部操作。

次：Humanが本判定recordをPilotへ渡し、F-CG-COMP-001の修正を別作業単位として開始するかを判断する。
修正する場合は、元Findingと同じ正しい旧Digestを持つ非JSON互換recordでREDを確認した後、元の受入条件、
対象Test、公式全Testを再レビューする。
