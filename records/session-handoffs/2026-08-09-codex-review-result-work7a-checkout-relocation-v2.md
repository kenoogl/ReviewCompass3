# Work 7A第2項 checkout relocation 前駆slice 独立再レビュー結果 v2

- review date：2026-08-09
- Pilot：Claude
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- risk：`high`（妥当）
- verdict：`report_execution_mismatch`

## 1. 対象と固定入力

- 再レビュー依頼：
  `records/session-handoffs/2026-08-09-claude-pilot-work7a-checkout-relocation-review-request-v2.md`
- 依頼書SHA-256：`27e66a02fb4397c7ebe049fffc9ea96bce6c1399502f7f3cb84f8994715790ed`
- 依頼書commit：`d7bacd32cfc4446656567cceb95b1757b719f7b0`
- 有効scope：
  `records/session-handoffs/2026-08-09-claude-pilot-work7a-checkout-relocation-scope-v2.md`
- scope SHA-256：`f127351d05bc621af95a042506dc726790ca59ecc928cec4c34257ee23d473a8`
- 前回review result：
  `records/session-handoffs/2026-08-09-codex-review-result-work7a-checkout-relocation-v1.md`
- 前回result SHA-256：`ba5703edda25b73fb6251b73839367d2c9d7b12c5fd28a7109e9df06d7c8c0c6`
- 対象commit列：前回result `5633442247b351830b529e5b4c5ff37a45f6f893`、修正RED
  `2b27b4d4a00a7ee6989d29fc6a35e92ef01d8b56`、修正GREEN
  `af8e005f8844520042eec16252d48ef64ccee368`、再レビュー依頼
  `d7bacd32cfc4446656567cceb95b1757b719f7b0`

review開始時worktreeはclean。commit列は線形で、修正REDはTest 1 fileへ116行追加のみ、修正GREENは
実装・GREEN Evidence・公式receiptの3 fileのみ、依頼commitは依頼書1 fileのみを追加していた。
REDからGREENまでTest差分は0、scope固定入力22件は全件再計算Digestと一致し、禁止path変更は0だった。

修正後4成果物の再計算SHA-256も依頼書と一致した。

| file | SHA-256 |
| --- | --- |
| `tests/test_work7a_checkout_relocation.py` | `2a5c32ae22104217219e26a5c82b0de26b56de9dd3226a06e07765de0e273eda` |
| `tools/deployment/checkout_relocation.py` | `5c353c6f2815dbe434d5fab5374ac3af2d6996eddc417b9fa30930402778f589` |
| GREEN Evidence | `176f089dc9da544eab4116231f32856afe825472d00761e4d9589103b28b0932` |
| 公式receipt | `e653387a9f35eb04fe7951c670b9c21a6bdefbe699f70871e0a0d2e94e27684e` |

## 2. 上流から独立導出した受入条件

Work 3承認authorityは、Source Snapshotのstale triggerを「tracked content変更」、Change Setの
stale triggerを「actual file deltaとrecorded deltaの不一致」とする。またscope v2は
`tracked_changes`を機械取得し、対象fileのpathとSHA-256をmanifest化し、実Git deltaの
add／modify／delete／renameを区別するよう要求する。したがって次を受入条件とした。

1. 同じHEADでも、base／candidate間のtracked、staged、対象untrackedの実内容差を空Change Setにしない。
2. caller指定`head_commit`は実HEADと一致し、不一致を安定stop codeで拒否する。
3. command-scope Git configを含む呼出し環境でdirty状態をcleanへ偽装できない。
4. tracked symlinkでは参照先fileを読まず、Gitがtracked contentとして扱うlink payloadの差を識別するか、
   対応不能ならfail-closedに拒否する。異なるpayloadを同じ`content_identity`として受理しない。
5. 暫定lineage ID、耐久保存、Verification Run、checkbox、Human境界はscope v2のまま維持する。

このcodeはsource identityとChange Setの合否を決め、欠落が偽の合格として現れる守り役なので、risk
`high`は妥当である。

## 3. RED履歴と独立再実行

修正RED commitを`git archive`で独立directoryへ展開し、そのtreeでTestを単独実行した。新規3件だけが
空Change Set、旧HEADの無拒否、config注入によるclean偽装という反証どおり失敗し、先行19件は合格した。

| 区分 | command | 結果 | exit code |
| --- | --- | --- | --- |
| 修正RED再現 | `/Users/Daily/Development/ReviewCompass3/.venv/bin/python3 -m pytest tests/test_work7a_checkout_relocation.py`（commit `2b27b4d...` archive内） | 3 failed、19 passed | `1` |
| targeted | `.venv/bin/python3 -m pytest tests/test_work7a_checkout_relocation.py` | 22 passed | `0` |
| 関連回帰 | `.venv/bin/python3 -m pytest tests/test_layout_baseline.py tests/test_work7a_local_integrated_root_separation.py tests/test_first_review_task_contract_e2e.py` | 83 passed | `0` |
| 公式全Test | `.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt /private/tmp/2026-08-09-codex-work7a-checkout-relocation-rereview-receipt-v2.json` | 1337 passed、failed 0、fallback false | `0` |
| 前回独立反証3件 | `.venv/bin/python3 -m pytest /private/tmp/test_checkout_relocation_independent.py` | 2 passed、1 assertion mismatch | `1` |
| 追加独立反証 | `.venv/bin/python3 -m pytest /private/tmp/test_checkout_relocation_symlink_delta_v2.py` | 1 failed（空Change Set） | `1` |

Reviewer全Test receipt SHA-256は
`9b2cf0b55ab813ea4203673681a5bb51c42d0e7c0ebe9d7e03a441b23c5ee815`、status `passed`、
exit `0`、1337 passedである。前回独立反証fileのSHA-256は依頼書記載どおり
`ab45c847930ab85b9381463f52ad83b6108288a3977452ffa768e44870a66507`。追加反証fileのSHA-256は
`2da69bd7206e036b777d733e731ea08288c3144883bd8b6e3db740400223aa12`である。

前回独立反証の1 assertion mismatchは、旧fixtureが`checkout_state_mismatch`を固定していた一方、実装が
旧HEADを正しく拒否して新しい安定code `head_commit_mismatch`を返した差だけである。前回Findingはcode名を
指定せず「安定stop codeで拒否」を要求しており、旧HEADを受理する反証は再成立していない。この1件は
製品Findingに数えない。

## 4. 前回3 Findingsの再評価

| Finding | 再評価 | Evidence |
| --- | --- | --- |
| RR-P1-001 | 一般file・staged・対象untrackedの固定例は解消。ただしtracked symlinkで同種の偽陰性が残り、完全解消ではない | 前回反証1 passed、追加反証failed |
| RR-P1-002 | 解消 | 実HEAD不一致を`head_commit_mismatch`で拒否 |
| RR-P2-003 | 解消 | `GIT_CONFIG*`注入下でもmode dirtyを捕捉 |

## 5. Finding

### RR-P1-004：tracked symlinkのpayload差を空Change Setとして合格させる

`_tracked_changes`はworktree pathがsymlinkなら`content_identity=None`にする。そのため、同一HEADで
base Snapshot時のtracked symlink payloadを`target-b.txt`、candidate Snapshot時を`target-c.txt`にしても、
両状態は同じ`("M", None)`へ正規化される。追加独立反証ではGitが両方をdirty tracked changeとして観測する
状態で、`derive_change_set`が実file deltaを空配列として返した。

これは外部fileの内容を読む反証ではない。両参照先はfixture repository内にあり、差分対象はGitがsymlink blobの
contentとして追跡するlink payloadである。Work 3 authorityのtracked content stale trigger、actual file delta一致、
scope v2のtracked change／content manifest契約に反する。

影響：異なるtracked contentを同じSnapshot状態として扱い、空Change Setと既存Verification／Decisionを再利用できる。
source identityの守り役が実変更を黙って合格させるためblocking `P1`とする。

必要な修復：tracked symlinkを参照先へdereferenceせず、link payload自体の決定的identityとして捕捉・照合するか、
本sliceで安全に表現できない場合は安定stop codeでfail-closedに拒否する。同一HEADでbase／candidateのlink payloadが
異なる負例をREDで固定し、元22件、追加反証、関連、公式全Testを再実行する。既存in-memory値schemaで表せないと
判明した場合だけscope停止条件に従いHuman裁定を得る。

## 6. 一致したClaim、Human境界、判定

- 修正REDの3失敗／19合格、GREEN後のtargeted 22、関連83、公式全1337は再実行結果と一致した。
- RR-P1-002とRR-P2-003は解消し、RR-P1-001の通常file・staged・対象untracked例も解消した。
- `--no-optional-locks`位置、NUL区切り、rename threshold、Git config隔離は維持されている。
- `content_identity`はin-memoryのnested entry追加に留まり、top-level identity fields、新永続schema、
  `RECORD_KINDS`、禁止pathを変更していない。
- 耐久Binding、Verification Run、binding directory、TODO／checklist、Work 7A第2項checkboxは未実施である。
- push、tag、PR、履歴書換え、scope外実装変更は観測していない。

判定は`report_execution_mismatch`。covered Testの合格は有効だが、RR-P1-001を一般化したGREEN完了Claimと実状態が
RR-P1-004で競合する。GREEN Evidence §7とreview request v2の完了Claimはstaleとして扱い、`verified`、Closer
projection、後続slice開始の根拠にしない。Work 7A第2項checkboxとTODOは現状を維持する。

Humanが本Findingの修正を承認した場合、Pilotは修正RED、実装、GREEN Evidence／receipt更新、review request v3を
別commitで固定して停止する。Reviewerは元22件、前回独立3シナリオ、RR-P1-004反証、関連、公式全Testを再実行する。
