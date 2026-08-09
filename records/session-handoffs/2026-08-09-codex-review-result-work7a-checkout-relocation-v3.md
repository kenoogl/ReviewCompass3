# Work 7A第2項 checkout relocation 前駆slice 独立再レビュー結果 v3

- review date：2026-08-09
- Pilot：Claude
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- risk：`high`（妥当）
- verdict：`verified`

## 1. 対象と変更範囲

- 再レビュー依頼：
  `records/session-handoffs/2026-08-09-claude-pilot-work7a-checkout-relocation-review-request-v3.md`
- 依頼書SHA-256：`194af1365343d46ad7a101f352f30c46265be5f7bb44e7e43263d27927581278`
- 依頼書commit：`121f33c3854431188eab782df7c75c85e5e63863`
- 有効scope：
  `records/session-handoffs/2026-08-09-claude-pilot-work7a-checkout-relocation-scope-v2.md`
- scope SHA-256：`f127351d05bc621af95a042506dc726790ca59ecc928cec4c34257ee23d473a8`
- 前回review result：
  `records/session-handoffs/2026-08-09-codex-review-result-work7a-checkout-relocation-v2.md`
- 前回result SHA-256：`9d307e0c8cf9d0a1a1fc74f4bb27e69f52d86e91dc2ee1f5309e5eb5ec6e10ad`
- 対象commit列：前回result `0861875e1fb9e49233c8ab8aa2c5cd12981cdee8`、修正RED
  `0e1952195d0c40c5b3285fc151a55ac0ebf085cf`、修正GREEN
  `2c834b4e686c8c0c95779e5784853b508663ecc3`、再レビュー依頼
  `121f33c3854431188eab782df7c75c85e5e63863`

review開始時worktreeはcleanで、commit列は線形だった。修正REDはTest 1 fileへ62行追加のみ、
修正GREENは実装・GREEN Evidence・公式receiptの3 fileのみ、依頼commitは依頼書1 fileのみを
追加していた。REDからGREENまでTest差分は0、scope固定入力22件は全件再計算Digestと一致し、
禁止path変更は0だった。

修正後成果物の再計算SHA-256は依頼書と一致した。

| file | SHA-256 |
| --- | --- |
| `tests/test_work7a_checkout_relocation.py` | `ab8f311dd6099085acec942c8e956523209756e4bcdc585be5e5b89e84b19258` |
| `tools/deployment/checkout_relocation.py` | `2a81b11d1355f5bcde1381ff40dd9cd9337781e2719cbb696befc5d60d44eed1` |
| GREEN Evidence | `c20a8d4056cbe55870defd61f7a3f3de61942f945a1fe9cb7bfb696d34105c10` |
| 公式receipt | `b4384813ff82ca0e7aa9a133996dc618710658a7f5a7ca1c405c63805f9d9a9e` |

## 2. 上流から独立導出した受入条件

Work 3承認authorityのtracked content stale trigger、actual file delta一致、およびscope v2の
tracked change／content manifest契約から、次を固定した。

1. 同一HEADでもbase／candidate間のtracked symlinkのlink payload差を空Change Setにしない。
2. link payloadを識別するとき参照先fileをdereferenceせず、外部内容を取り込まない。
3. 通常fileとsymlinkの種別変化を同じ内容identityとして扱わない。
4. 前回までに固定したdirty／staged／対象untracked、実HEAD束縛、Git config隔離の受入条件を
   staleとして再確認する。
5. 暫定lineage ID、耐久保存、Verification Run、checkbox、Human境界はscope v2のまま維持する。

source identityとChange Setの偽陽性を防ぐ守り役のcodeであるため、risk `high`は妥当である。

## 3. RED履歴と独立再実行

修正RED commitを`git archive`で独立directoryへ展開し、Testを単独実行した。RR-P1-004の新規1件だけが
空Change Setで失敗し、先行22件は合格した。

| 区分 | 結果 | exit code |
| --- | --- | --- |
| 修正RED再現（commit `0e195219...` archive内） | 1 failed、22 passed | `1` |
| targeted | 23 passed | `0` |
| 関連回帰 | 83 passed | `0` |
| 公式全Test | 1338 passed、failed 0、fallback false | `0` |
| 前回独立3シナリオの固定file再実行 | 2 passed、1旧stop code assertion mismatch | `1` |
| RR-P1-004追加反証 | 1 passed | `0` |
| Reviewer新規反証 | dangling symlink／file→symlink種別変化の2 passed | `0` |

Reviewer公式全Test command：

```text
.venv/bin/python3 -m tools.development.policy_test_runner --project-root . --suite full --receipt /private/tmp/2026-08-09-codex-work7a-checkout-relocation-rereview-receipt-v3.json
```

receipt SHA-256は`3334b48620f88d7872c5fa36ad25b27f6c272ad7aca3505cdeb63e02d9bf3b8b`、
status `passed`、exit `0`、1338 passedである。

RR-P1-004反証file SHA-256は依頼書どおり
`2da69bd7206e036b777d733e731ea08288c3144883bd8b6e3db740400223aa12`で、同一HEADの
tracked symlink payload差から`modify`が導出され、照合も成立した。Reviewer新規反証file SHA-256は
`09bbd0e1a435348c068db9a83d87d073edfadb9964f8f99e92f50d55a7c2a6a9`。存在しない参照先を持つ
tracked symlinkでもpayload identityが変わり、通常fileは`file:`、symlinkは`symlink:`として区別された。

前回独立3シナリオの固定file SHA-256は
`ab45c847930ab85b9381463f52ad83b6108288a3977452ffa768e44870a66507`。1 assertion mismatchは
前回result v2で分類済みの、旧fixtureが期待する`checkout_state_mismatch`と実装の安定code
`head_commit_mismatch`との差だけである。旧HEADは例外で正しく拒否されており、反証の本質は再成立しない。

## 4. RR-P1-004の再評価

`_tracked_changes`はworktree pathがsymlinkなら`os.readlink`でlink payloadを取得し、
`symlink:<payload SHA-256>`を記録する。通常fileは`file:<file SHA-256>`であり、index側はGit blob oidを
維持する。`os.readlink`は参照先fileを開かず、Reviewerのdangling symlink反証でも捕捉・差分導出が成立した。

base／candidateのpayload差は`content_identity`と`content_manifest_digest`の両方を変え、
`_state_delta_kinds`から`modify`へ導出される。RR-P1-004は解消した。前回までのRR-P1-001、
RR-P1-002、RR-P2-003を含め、review対象scopeのblocking Findingは0である。

## 5. Human境界、未実施、判定

- in-memory nested entryの値表現変更に留まり、top-level identity fields、新永続schema、
  `RECORD_KINDS`、禁止pathは変更していない。
- production APIはread-only Gitのままで、Test fixtureの変更操作は`tmp_path`内に限定されている。
- 耐久Binding、Verification Run、binding directory、TODO／checklist、Work 7A第2項checkboxは
  未実施である。
- push、tag、PR、amend、rebase、reset、履歴書換え、scope外実装変更は観測していない。
- Humanの修正承認後にREDを開始し、review request v3 commitでPilotが停止した境界は維持されている。

判定は`verified`。必須Evidence、RED履歴、変更範囲、成果物Digest、独立反証、対象・関連・公式全Test、
Human境界が一致し、RR-P1-004を含む受入条件を満たす。本resultは前駆sliceの完了レビュー根拠にできるが、
Human裁定どおりWork 7A第2項checkbox全体の完了根拠にはしない。

次はCloser（Codex）が別作業単位・別commitで完了EvidenceとTODO projectionを反映する。レビューと
完了projectionは本commitへ混在させない。
