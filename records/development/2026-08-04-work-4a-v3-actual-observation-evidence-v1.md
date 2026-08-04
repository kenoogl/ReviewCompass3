# Work 4A v3 Actual Observation Evidence v1

## 承認

2026-08-04の会話でHumanが、提示した段階1〜3（project内2 file、外部2 file）の作成を承認した。
候補routineの選定とHuman dispositionは承認範囲外であり、実施していない。

## project内に作成したartifact

| path | content_digest |
| --- | --- |
| `.reviewcompass/policies/work4a-source-universe-v1.json` | `652bf2d8bec5a09c2d765c07644b97508b3a08dc76216ad87ee20320e46c5856` |
| `.reviewcompass/policies/work4a-freshness-policy-v1.json` | `f5e2d6340c0e08a0a90a7f237bcc44fc8fd274360cafe204342f1ac32abf0c7d` |

source universeは`SRCU-WORK4A-TOOLS-PY-V1`、対象root `tools`、対象`**/*.py`、
除外`.git` `.reviewcompass` `.venv` `docs` `records` `tests`である。
Policyはchange class `ordinary`、再検証必須classは`security` `authority` `irreversible`、
disposition語彙は`reuse` `extend` `merge` `split` `new`である。
`invalid_layout`はPolicy語彙に含めない（v3設計§12.1）。

## 外部DATA_ROOTに作成したrecord

data root：`/Users/keno/.reviewcompass3/projects/reviewcompass3/development/data`

| 相対path | file SHA-256 |
| --- | --- |
| `work4a/observations/be323010fdcd343525ddcdb4d49b57c14913ec5a6baf2a4e586490646707be61.json` | `d5a36cb27bfbf7953b774e724d6e1a04f41f7951b15a7461ddecf24066f7a29f` |
| `work4a/candidates/c2df7640968a319da1cede5fc2ea00a2eb581486c3e3dcb9f896d72f88fed8d2.json` | `1ba17134fa7a11f91bb1d205b32a3e2d1d2ea73d7977159f57455d496c6e114d` |

## 観測の内容

| 項目 | 値 |
| --- | --- |
| `source_content_id` | `6c0d9ab2edd80b536084a078c11a3cc1efd126964a421cd09366fa75ca14243d` |
| `snapshot_id` | `be323010fdcd343525ddcdb4d49b57c14913ec5a6baf2a4e586490646707be61` |
| HEAD | `1fb48afe7d9229b1b95d6fcb05219ec50c382111` |
| tool version | `v3` |
| 採取時刻 | `2026-08-04T22:02:10+09:00` |
| 対象file数 | 101 |
| profile | `development` |

`source_content_id`はHEAD、採取時刻、絶対pathを含まない。同一内容の再採取では同じ値になる。

## 候補抽出の結果

| 項目 | 値 |
| --- | --- |
| `candidate_run_id` | `c2df7640968a319da1cede5fc2ea00a2eb581486c3e3dcb9f896d72f88fed8d2` |
| 候補件数 | 922 |
| 分類件数 | `new` 922（既存Entryが無いため全件new） |
| symbol ID一覧Digest | `517939e5afc05f25f1e2805447bf6c3febded7f42b01e68bc60a580fa1bd4e03` |

所属package別の内訳は`session_logs` 334、`development` 193、`extraction` 144、`bootstrap` 103、
`requirements` 102、`layout` 26、`design` 20である。

候補recordはsymbol IDと分類だけを持ち、source本文を保存しない。

## 停止条件に触れなかったこと

`root_overlap`、`unsafe_root`、`root_escape`、`path_traversal`、`non_regular_file`、`missing_record`、
`invalid_manifest`、`content_digest_mismatch`、`immutable_violation`、`write_verification_failed`、
`unknown_field`のいずれにも該当せず、全書込みが完了した。
`tools/`配下にsymbolic linkは0件、構文不正fileも0件であった。

## Test

- 全test：venv公式runner `681 passed`、Python 3.9.6、pytest 8.4.2、fallback false
- receipt：`records/development/2026-08-04-work-4a-v3-actual-observation-green-test-receipt-v1.json`

## 現在の停止点

Observation Attestation、Operational Human Decision、Entry、Relation、Baselineは作成していない。
候補922件からどのroutineを対象にするか、dispositionを何にするかはHumanの判断であり、未実施である。
