# Codex → Claude：operation routing v2 receipt整合性の修正指示

## 誰が何をするか

- **Human**は、operation routing v2のreceipt改竄を拒否できない問題の修正を承認した。
- **Codex**は、問題、修正の必須性、保持対象、検証条件をこの文書へ固定する。
- **Claude**は、TDDで改竄を再現し、validatorを修正し、新しい訂正Decision／Evidence／receiptを作成して一つのGREEN意味単位commitにする。

## 問題の再現事実

現行`tools/development/operation_routing.py`は、Git metadata writeを含むinventoryに対し、execution receipt内の
`preflight_ref.required_permissions`を空へ改竄し、そのDigestを再計算すると受理してしまう。

原因は二つある。

1. `validate_permission_preflight()`が、`required_permissions`、`missing_permissions`、`verdict`をinventoryとhost attestationから再計算していない。
2. receiptがpreflightの抜粋referenceだけを持ち、完全なpreflight recordをvalidatorが再検証できない。

これはreceiptの監査性に関わるため、既存GREEN Evidenceを有効な完了根拠として扱えない。

## 保持対象と非対象

- 既存`DEC-MACHINE-OPERATION-ROUTING-001`は、Humanが§3最小縦切りを承認した事実として変更しない。
- 既存v1 GREEN Evidenceとv1 GREEN receiptは削除・書換えしない。validator穴が見つかったためstaleであることを新しい訂正Evidenceへ記録する。
- operation inventoryのschema versionは変えない。
- Git、shell、subprocess、外部送信、host／sandbox権限の取得・迂回、cache root、argv executor、V4 Issue state、Task Contract、policy runnerは変更しない。

## 1. RED test

既存`tests/test_operation_routing_v2.py`を削除・弱化せず、次のtestを**先に**追加する。

1. Git metadata writeを含むinventoryから作った正当なreceiptで、完全なpreflightの必要権限を空へ改竄し、各Digestを改竄内容に合わせて再計算しても`receipt_identity_mismatch`または新設の`preflight_requirement_mismatch`で拒否する。
2. preflight単体の`required_permissions`をinventory由来の値と異なるものにし、自己Digestを再計算しても拒否する。
3. preflight単体の`missing_permissions`と`verdict`の組合せをhost attestationと異なるものにし、自己Digestを再計算しても拒否する。
4. 正当なread-only inventoryと、正当な混在write inventoryがGREENになることを維持する。
5. receiptが旧schema versionなら拒否し、今回の新schema versionの正当なreceiptだけを受理する。

REDを`.venv/bin/python3 -m pytest -q tests/test_operation_routing_v2.py`で確認する。RED testだけをcommitしない。

## 2. 実装

`tools/development/operation_routing.py`を次のように修正する。

1. `validate_permission_preflight(preflight, inventory=...)`は、inventoryを再検証し、必要権限を`required_permissions(inventory)`で再計算する。
2. preflightの`granted_permissions`をhost attestation vocabularyとして厳密に検証し、`missing_permissions`を「再計算した必要権限 − granted_permissions」と一致させる。
3. verdictはmissingが空なら`granted`、それ以外なら`approval_required`だけを受理する。自己Digestが正しくても、意味が違えば拒否する。
4. execution receiptには抜粋`preflight_ref`ではなく、**完全な検証済みpreflight record**を保存する。receipt validatorはこのpreflightをinventoryに対して再検証し、`granted`でなければ拒否する。
5. receiptの構造が変わるため、receipt recordだけのschema versionを2へ上げる。inventoryとpreflightのschema versionは1のままにする。v1 receiptは明示的に拒否する。
6. receiptの`content_digest`、inventory identity、preflight identity、operation結果の順序・ID照合を維持する。
7. 実行callbackは、`unknown`、`external`、権限不足、改竄preflightのいずれでも一度も呼ばれない。

停止codeは既存の語彙を優先して使う。新設する場合は、`STOP_CODES`へ追加し、意味とtestを固定する。

## 3. 訂正記録とEvidence

次を新規作成する。

1. `records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-correction-decision-v1.md`
   - decision ID：`DEC-MACHINE-OPERATION-ROUTING-RECEIPT-INTEGRITY-001`
   - Humanが改竄拒否の修正を承認したこと
   - 元v1 GREEN Evidence／receiptは承認対象の実装結果だが、receipt validatorの欠陥によりstaleとなったこと
   - §3の範囲、host境界、非対象を固定すること

2. `records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-green-evidence-v1.md`
   - RED再現、修正、GREEN、改竄拒否、callback 0回、receipt schema v2、既存v1 Evidenceのstale化を記録する。

3. `records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-green-test-receipt-v1.json`
   - 公式full testの実結果をpolicy runnerで保存する。

`docs/design/2026-08-05-machine-operation-routing-issue-plan-proposal-v2.md`には、§3の実装がreceipt schema v2で改竄検出を含むことを短い実施注記として追記する。提案時点の本文は改竄しない。

`docs/current/reviewcompass3-plan-current.md`、checklist、TODOを更新する。前のGREEN Evidenceを唯一の完了根拠として残さず、訂正Decision／GREEN Evidenceへ接続する。C9全体をclosedと書かず、後続のargv executor、cache root、既存操作移行は未実施のままにする。

## 4. 検証とcommit

1. `git diff --check`
2. 上記RED testの失敗を確認
3. 修正後、operation routing test全件と既存related testを実行
4. fault injectionを、改竄receipt・改竄preflight・unknown・external・権限不足で実行し、すべてcallback 0回を確認
5. TODO validator：

   `python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md`

6. 公式全test：

   ```text
   .venv/bin/python3 -m tools.development.policy_test_runner --suite full \
     --receipt records/development/2026-08-05-machine-operation-routing-v2-receipt-integrity-green-test-receipt-v1.json
   ```

7. 最終stage前にTODO validatorと`git diff --check`を再実行する。対象pathだけを明示列挙してstageし、`git add -A`／`git add .`を使わない。
8. 一つのGREEN意味単位commitを作る。messageは`Verify operation routing receipt integrity`とする。
9. commit後に`git status --short`と`python3 tools/development/work_unit_transition.py --work-status completed`をread-onlyで確認する。

push、tag、amend、rebase、reset、force push、外部送信をしない。

## Claudeの完了報告

commitに混ぜず、次をローカルに作る。Git ignore済みのためstageしない。

`records/session-handoffs/2026-08-05-claude-to-codex-repair-operation-routing-receipt-integrity.md`

報告にはcommit SHA、RED／GREEN数、改竄の再現と拒否結果、callback 0回の証拠、schema v2、stale化したv1 Evidence、非対象を記す。
