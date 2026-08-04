# Work 4A v3 Acceptance GREEN Evidence v1

## 対象

- 実装：`tools/development/work4a_rebuild_v3.py`
- Test：`tests/test_work4a_rebuild_v3_e2e.py`（22件）
- 正本設計：`docs/design/2026-08-04-work-4a-rebuild-design-v3-proposal.md`
- 承認：`DEC-WORK4A-REBUILD-DESIGN-003`
- RED：`records/development/2026-08-04-work-4a-v3-acceptance-red-evidence-v1.md`
- receipt：`records/development/2026-08-04-work-4a-v3-acceptance-green-test-receipt-v1.json`

## 結果

- Work 4A v3 acceptance：`22 passed`
- 全test：venv公式runner `685 passed`、Python 3.9.6、pytest 8.4.2、fallback false

REDからGREENの間にtestの期待を緩めていない。実装後もA〜Hの22件は初回作成時の内容のままである。

## 実装した不変条件

| 不変条件 | 実装 |
| --- | --- |
| Baseline・Decisionは外部を直接参照しない | `write_operational_decision`と`append_baseline`はAttestationのproject refだけを持つ |
| 外部位置情報はAttestation内のadvisory locatorに限定 | `_build_locator`はAttestation構築時にのみ呼ばれる |
| 外部file不在でもcurrentを確定 | `validate_current`のP0〜P6は外部を読まない。P7だけがlocatorを見る |
| 不在は非停止、改竄は停止 | `_collate_locator`が`locator_unresolved`を注記し、Digest不一致で`observation_tampered` |
| 異profileは照合しない | `_collate_locator`が`locator_profile_mismatch`を注記して照合を打ち切る |
| root重なりはPolicyより前に停止 | `resolve_data_root`がP1で`root_overlap`（`invalid_layout`分類）を送出 |
| new-only | `_write_new`が既存pathを`immutable_violation`にする。`append_baseline`は全path事前検査後に書く |
| currentは連番最大 | `_baseline_series`が欠番・重複を`baseline_series_broken`にする。可変pointer fileを作らない |
| 語彙はPolicyから取る | disposition語彙はPolicy recordから読む。呼出側の文字列で判定しない |
| `invalid_layout`はPolicy語彙外 | `_current_policy`がPolicyに`invalid_layout`が含まれる場合を拒否 |

## 独立確認

testとは別に、次を手動で確認した。

- Entry fileの内容を改竄すると`validate_current`が`digest_mismatch`で停止する。
- Baseline JSONに絶対pathもadvisory locatorも現れない。
- 外部が健全な場合、注記なしで検証が通る。

## 非対象

actual artifactは作成していない。対象routineの選定とHuman dispositionは未実施であり、
外部`DATA_ROOT`の初期化も行っていない。legacy Task Contractのhistorical移行も行っていない。
