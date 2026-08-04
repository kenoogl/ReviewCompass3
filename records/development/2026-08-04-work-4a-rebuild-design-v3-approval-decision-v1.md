# DEC-WORK4A-REBUILD-DESIGN-003

## Decision

Humanは`docs/design/2026-08-04-work-4a-rebuild-design-v3-proposal.md`を承認し、Work 4A実装の正本をv3へ切り替えた。

## 承認範囲

- v3設計本体（Observation Attestation方式、project refとadvisory locatorの分離、validation順序、fail-closed条件、
  deployment連続性、v3 E2E acceptance）
- Policy artifactへの検証結果語彙（fail-closed code）と処置語彙（disposition）の追加
- `root_kind`／`root_selector`／`profile`をLayout v3の語彙と解決規則へ従属させること
- v2を`superseded_for_implementation`とすること

`invalid_layout`はPolicyのchange classに含めず、layout段階で常にfail-closedとする別枠の分類である
（v3設計§12.1）。したがってPolicy語彙追加の対象に含めない。

## v2残余の処分

破棄とrevertは復旧可能性が異なるため、同じ承認・同じ操作にまとめない。

| 対象 | 状態 | 処分 |
| --- | --- | --- |
| `tools/development/work4a_rebuild_v2.py`の未コミット差分 | 未コミット | Humanが破棄済み |
| `tests/test_work4a_rebuild_v2_contract.py` | 未追跡 | Humanが破棄済み |
| `tools/development/work4a_rebuild_v2.py`本体（`33218e0`） | commit済み | 対象commit・保持対象・影響を一度だけ提示し、Humanのrevert承認後に別作業単位でrevertする |
| `tests/test_work4a_rebuild_v2_e2e.py`（`df2bd3c`） | commit済み | 同上 |

commit済みv2のrevertは、v1と同じくhistoryを書き換えずrevert commitで戻し、revert対象・保持対象・理由を
対応表として`records/development/`へnew-only保存する。

## 自律実行の範囲

承認済み設計の範囲では、実装途中の細かな判断で停止せず自律実行する。次の場合だけは局所patchを行わず停止して報告する。

- 設計レベルの矛盾
- security、authority、不可逆操作に影響する問題
- actual artifactの対象routine選定とHuman disposition
- 破棄、revert、外部`DATA_ROOT`の初期化（対象と影響を示して承認を待つ）

## 禁止事項

v2試作へ継ぎ足して通すこと、局所patch、モグラたたき式の修正を禁じる。
`tools/development/work4a_rebuild_v2.py`と`tests/test_work4a_rebuild_v2_e2e.py`は実装正本ではなく、
v3実装はこれらを参照・import・拡張しない。

## 効力

- v1、v2は履歴として保持するが、実装正本ではない。
- v2試作moduleとv2 E2E testは、actual artifactまたはWork 4A完了の根拠に使わない。
- v3設計§18の実装開始条件はすべて充足した。

## 根拠

- Human approval：2026-08-04の会話における次の承認。

  > Work 4A v3設計を承認する。
  >
  > 承認範囲には、v3設計本体、Policy artifactへの検証結果・処置語彙の追加、
  > root_kind／root_selector／profileをLayout v3の語彙と解決規則へ従属させること、
  > v2をsuperseded_for_implementationとすることを含める。
  >
  > 未コミットのv2差分と未追跡testは、すでに破棄済みである。
  > コミット済みv2試作は、対象commit・保持対象・影響を一度だけ提示し、
  > 私がrevertを承認した後に別作業単位でrevertすること。
  >
  > 承認済み設計の範囲では、実装途中の細かな判断で止まらず自律実行する。
  > ただし、設計レベルの矛盾、安全性・authority・不可逆操作に影響する問題を見つけた場合は、
  > 局所patchを行わず停止して報告する。

- 対象設計：`docs/design/2026-08-04-work-4a-rebuild-design-v3-proposal.md`
- 先行Decision：`records/development/2026-08-04-work-4a-rebuild-design-v2-approval-decision-v1.md`
