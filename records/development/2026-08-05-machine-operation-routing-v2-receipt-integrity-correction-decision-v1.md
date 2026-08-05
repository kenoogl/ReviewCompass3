# operation routing v2 receipt整合性 訂正Decision v1

- decision ID：`DEC-MACHINE-OPERATION-ROUTING-RECEIPT-INTEGRITY-001`
- decision maker：Human
- decided at：2026-08-05
- 対象Issue：`ISSUE-HTC-C9F6C917`
- 指示：`records/session-handoffs/2026-08-05-codex-to-claude-repair-operation-routing-receipt-integrity.md`

## 1. Humanが承認したこと

Humanは、operation routing v2のexecution receiptについて、**改竄を拒否できない問題の修正**を承認した。

修正前の実装は、Git metadataへの書込みを含むinventoryから作った正当なreceiptに対して、
receipt内のpreflight情報の`required_permissions`を空へ書き換え、そのDigestを計算し直すと
**受理してしまった**。原因は次の二つである。

1. `validate_permission_preflight()`が、`required_permissions`、`missing_permissions`、`verdict`を
   inventoryとhost attestationから**再計算していなかった**。申告された値をそのまま信じていた。
2. receiptがpreflightの**抜粋**しか持たず、validatorが完全なpreflight recordを再検証できなかった。

## 2. 既存Decisionと既存Evidenceの扱い

- 既存の`DEC-MACHINE-OPERATION-ROUTING-001`
  （`records/development/2026-08-05-machine-operation-routing-v2-approval-decision-v1.md`、
  SHA-256 `c73cdc69b3ca3251b9de9480867c9677e0de4312f7bedff138a407af297cd969`）は、
  Humanがv2提案§3の最小縦切りを承認したという**事実の記録**として変更しない。承認の範囲も変えない。
- 既存のv1 GREEN Evidence
  （`records/development/2026-08-05-machine-operation-routing-v2-green-evidence-v1.md`、
  SHA-256 `e4f8d9f865e6b6d35e7d00a21eba54c13b1ed331fca3183827b1262d285d88eb`）と、
  v1 GREEN receipt
  （`records/development/2026-08-05-machine-operation-routing-v2-green-test-receipt-v1.json`、
  SHA-256 `b6f55b5c7096b19106656403d9a7ad975f79debff61767827ac425be111d018a`）は、
  **削除も書換えもしない**。承認対象の実装結果を記録した履歴として残す。
- ただし、この二つはreceipt validatorの欠陥が見つかった時点で**stale**である。
  §3最小縦切りの有効な完了根拠は、本Decisionと訂正GREEN Evidence
  `records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-green-evidence-v1.md`
  へ置き換わる。

## 3. 修正の範囲

対象は、v2提案`docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal-v2.md`
（SHA-256 `7c812b68b4b4b0cd282af29b44ff117e78aa172b6f2b830f6d684856f9bf7a31`）の**§3だけ**であり、
承認範囲を広げない。

修正の内容は次のとおりである。

1. `validate_permission_preflight()`はinventoryを再検証し、必要権限を`required_permissions(inventory)`で
   **再計算**する。
2. `granted_permissions`をhost attestationの語彙として厳密に検証し、`missing_permissions`が
   「再計算した必要権限 − granted_permissions」と一致することを要求する。
3. verdictは、missingが空なら`granted`、そうでなければ`approval_required`だけを受理する。
   自己Digestが正しくても、意味が違えば拒否する。
4. execution receiptは抜粋ではなく、**完全な検証済みpreflight record**を保存する。
   receipt validatorはそれをinventoryに対して再検証し、`granted`でなければ拒否する。
5. receiptの構造が変わるため、**receipt recordだけ**のschema versionを2へ上げる。
   inventoryとpreflightのschema versionは1のままである。version 1のreceiptは明示的に拒否する。
6. receiptの`content_digest`、inventory identity、preflight identity、operation結果の順序・ID照合は
   従来どおり維持する。
7. 実行callbackは、`unknown`、`external`、権限不足、改竄preflightのいずれでも**一度も呼ばれない**。

新設した停止codeは`preflight_requirement_mismatch`と`preflight_verdict_mismatch`である。
いずれも`STOP_CODES`へ追加し、testで意味を固定した。

## 4. host境界

- 承認と取得済み権限の確認は**host側**に置く。project内は必要な権限種別を計算して出すだけである。
- `host attestation`はcallerが渡す入力である。moduleがOS、sandbox、Codex hostの権限を
  検査・付与・迂回することはない。今回の修正で、その申告値を**そのまま信じない**ようになった。
  申告が不正でも、inventoryから導いた必要権限と食い違えば拒否する。
- 必要な権限が未取得なら、最初の書込みを一度も試さず停止する。

## 5. 非対象

次はこの訂正に含まれない。着手しない。

- Git、shell、外部processの起動、外部送信
- host／sandbox権限の取得・迂回・自動承認
- cache rootの固定、構造化argv executor、既存直接shell操作の置換
- Codex hostのJavaScript tool構文、外部toolのAPI schemaへの対応
- operation inventoryのschema versionの変更（1のまま）
- V4 Issue recordのstate変更、Task Contractの新規作成、policy runnerの変更

`ISSUE-HTC-C9F6C917`のIssue recordは`registered`のままとする
（SHA-256 `66cfe50ce79136bca5e92b35b72502cedfb8b6f6f3e20ade1e027bcbf1fec0ed`）。
C9全体をclosedにしていない。後続のargv executor、cache root、既存操作移行は未実施のままである。

## 6. 修正後の実装物

| 種別 | path | SHA-256 |
| --- | --- | --- |
| module | `tools/development/operation_routing.py` | `0fb5636feac3e12c42104830cd710bdb2a6f9398b784edf211c57128e1cd9178` |
| 受入test | `tests/test_operation_routing_v2.py` | `369544e87bf673222ca6fec0306b55dc130b831094f51c93afa3e46c5fb075c5` |
