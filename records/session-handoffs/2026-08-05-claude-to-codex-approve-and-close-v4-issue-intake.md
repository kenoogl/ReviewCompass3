# Claude → Codex：Issue Intake V4の限定承認・検証閉鎖 完了報告

指示：`records/session-handoffs/2026-08-05-codex-to-claude-approve-and-close-v4-issue-intake.md`

指示の実施範囲をすべて完了した。承認・閉鎖は開発用・暫定の範囲に限られ、3正式IssueのPlan化・実装、
正式製品schema、UI、automation、Work 8評価は開始していない。

## commit

- commit SHA：`c87ec365a7eebdac562fa30ff29fb745ea7821fc`
- 内容：V4設計状態の訂正、承認Decision、閉鎖Evidence、Current Plan、checklist、TODO、
  V4閉鎖test receipt（計7file、288行追加・12行削除）
- `git diff --check`：stage前後とも合格
- commit後の追跡fileのworktree：clean（未追跡のまま残るのは、commitへ混ぜないsession-handoffsの
  完了報告13件のみ。本報告を含む）

## Decision IDと成果物path

| 種別 | path | SHA-256 |
| --- | --- | --- |
| 承認Decision `DEC-HISTORICAL-TODO-ISSUE-INTAKE-001` | `records/development/2026-08-05-historical-todo-issue-intake-v4-approval-decision-v1.md` | `019879235577b39489e4383cd0fa092c562631d3c1b1e1ffa311056c8d1d9f7c` |
| 閉鎖Evidence | `records/development/2026-08-05-historical-todo-issue-intake-v4-closure-evidence-v1.md` | `b942a9d17ea4c2818c6adb5f3ceabc0063f9b447c7ddb88ccc5baf3d1302d60e` |
| 閉鎖test receipt | `records/development/2026-08-05-historical-todo-issue-intake-v4-closure-test-receipt-v1.json` | `93a8bbf2d271067b3a5dbb5bcdd2c9f7875cc502a80656514fc4442eea93c087` |
| V4設計（状態訂正後） | `docs/design/2026-08-05-historical-todo-issue-intake-proposal.md` | `8475cd94b449e0709eb97e6d487b86cceef86e0307b3bbb7e78351d8f43147a9` |
| Current Plan | `docs/current/reviewcompass3-plan-current.md` | `57cff08c6624ffb86d94e18b22bb77c635329e9e140dec4f125704b327c33f50` |
| Initial Development Checklist | `docs/development/2026-08-03-initial-development-checklist.md` | `65f34c1094c5881cb46128ee1e81eb54f7904202ac0feebfe469adb077624bd1` |

## 1. 設計状態の訂正

`docs/design/2026-08-05-historical-todo-issue-intake-proposal.md`の状態を
`awaiting_human_approval`から`approved_for_development_use`へ更新し、冒頭に「実施状態注記（2026-08-05）」を
追加した。注記には、HumanがV4をdevelopment-only provisionalとして承認したこと、実装・GREEN Evidence・
41候補のHuman triageを完了したこと、現在のV4 Issueは3件でactive Issueは0件であること、正式製品schema・UI・
automation・Work 8評価・3 IssueのPlan化と実装が承認範囲外であることを明記した。

注記の直後に「以下は提案時点の本文である」と置き、既存節の過去形・将来形は一括書換えしていない。
`## 0. 先に報告すべき事実`以降の提案時点の説明はそのまま残している。差分は20行の追加・変更のみである。

## 2. 承認record

`DEC-HISTORICAL-TODO-ISSUE-INTAKE-001`として作成した。

- **承認の効力**：V4をdevelopment-only provisionalとして使用すること、複数の`registered` Issueの保持、
  作業中Issueを最大1件に制限すること、Human triage判断recordに基づくIssue昇格、候補bundleを
  観測として保持し`human_fields`を書き換えないこと。`pilot_mode: development_only_provisional`は維持する。
- **承認対象と実digest**：V4設計、V4 config、V4 validator（`tools/development/issue_intake_v4.py`）、
  V4 test（`tests/test_issue_intake_v4.py`）、GREEN Evidence 3件、候補bundle、
  V4 Human triage decision 41件（decision ID・candidate ID・disposition・file SHA-256の表）、
  V4 Issue 3件（issue ID・state・path・file SHA-256の表）をすべてpathと実SHA-256で固定した。
- **明示的な対象外**：3 IssueのPlan化・実装、正式製品schema、UI、hook、watcher、scheduler、
  background service、automation、Work 8評価、外部送信。

## 3. 閉鎖Evidence

閉じた対象は、旧Early Pilotのbootstrapではなく、その後に追加した**V4複数Issue受付の実地検証**である旨を
冒頭に明記した。閉鎖根拠として次を記録した。

- I1〜I9・J1〜J16に加え、K1〜K7とL1〜L6を含むGREEN Evidence 3件のpathとdigest。対象test fileは
  `tests/test_issue_intake_v4.py`で`38 passed`。
- 候補bundleのpath、SHA-256、候補数41、`human_fields`全件`null`、`promotion_status: none`、
  生成commit`3ef8759`以降このfileを変更したcommitが無いこと。
- 有効decision 41件、未判断0件、競合0件、disposition別の内訳。
- V4 Issue 3件の表（すべて`registered`、参照decisionは`blocking: false`）とactive Issue 0件。
- 設計・config・validator・testのpathとdigest、および参照の向き（Issue→decision→候補bundle、
  検証時は実fileから読み直す）。
- 残余riskと後続：3 IssueのPlan化はHumanが必要時に一件ずつ判断すること、V4を正式製品機能へ拡張しないこと、
  `pilot_mode`を維持すること、候補bundleと41 decision・3 Issueを上書き・削除しないこと。

## 4. Planとchecklistの整合

- Current PlanのInter-work表で、ReviewCompass Issue Resolution early Pilotのstateを
  `approved / bootstrap_in_progress`から`verified / limited_extension_completed`へ更新した。
  実施範囲にV4限定拡張（複数`registered` Issueの受付、過去TODO候補41件のHuman triage、
  active Issue最大1件）を追記し、未完了境界を正式製品schema、UI、automation、
  3正式IssueのPlan化・実装、Work 8評価とした。承認recordと閉鎖Evidenceのpathも記した。
- checklistの早期Pilot節は、既存の完了記録を消さずに残したまま、V4限定拡張の承認・閉鎖を1 checkboxと
  短い説明として追記し、承認Decisionと閉鎖EvidenceのpathとSHA-256を固定した。

## 5. 41候補／3 Issue／0 activeの確認

- V4 decision directoryのfile数は41件、`validate_triage_decision_repository()`の有効decisionも41件、
  競合0件。候補bundleの41候補のうち有効decisionが無いものは0件である。
- V4 Issueは3件（`ISSUE-HTC-BEB5E0BD`、`ISSUE-HTC-C9F6C917`、`ISSUE-HTC-66C3E6CA`）で、
  いずれも`state: registered`、参照decisionは`blocking: false`。`count_active_issues()`は0。
- 候補bundleのSHA-256は`e01c0feb082712f8ef0f77bfa4f031fbdc4530ed51f331f7dafbfd133d479a3e`のまま、
  `human_fields`は全件`null`である。
- `pilot_mode`は`development_only_provisional`のままである。
- 承認recordと閉鎖Evidenceに書いた全digest行を実fileと機械照合し、不一致0件を確認した。
  checklistの72件のSHA-256参照も不一致0件である。

## 6. policy runnerによる全test結果

指示のcommandで実行した。

```text
.venv/bin/python3 -m tools.development.policy_test_runner \
  --suite full \
  --receipt records/development/2026-08-05-historical-todo-issue-intake-v4-closure-test-receipt-v1.json
```

- status：`passed`、exit code：`0`、結果：`815 passed`
- Python 3.9.6、pytest 8.4.2、fallback false。raw pytestでreceiptを手書きしていない。

なお最初の実行は`1 failed, 814 passed`だった。原因はTODOが参照するCurrent Planとchecklistのdigestが、
本作業での更新により古くなったことである（`test_actual_post_write_and_isolated_restore_rehearsal`の
`TODO reference digest mismatch`）。指示§5の「Plan／checklist／TODOを書き換えた後に参照Digestを
再確認する」に従いTODOの2件のdigestを更新し、同一pathへ再実行して`passed`に置き換えた。
失敗receiptはcommitに残っていない。testもcodeも変更していない。

Plan／checklist／TODO更新後の確認として、TODOの参照digest30件の一致、commit安定Git節の合格、
9,677 bytesで上限内、active ID projectionが`ISSUE-PILOT-TODO-GROWTH-001`の1件のままであることを確認した。

## 7. 変更しなかった範囲

- 3正式IssueのPlan化・実装、Issueのstate変更：行っていない。3件とも`registered`のままである。
- V4のconfig、code、testの変更：行っていない。
- 正式製品schema、UI、hook、watcher、scheduler、background service、automation、Work 8評価：
  開始していない。
- 候補bundle、41 decision、既存3 Issue、旧Early PilotのVerdict・Evidence：変更していない。
  今回のcommitに含まれるのは設計・承認record・閉鎖Evidence・Plan・checklist・TODO・receiptだけである。
- 設計文書の既存節の一括書換え：行っていない。追記は冒頭の状態注記と状態行のみである。
- push、PR、外部送信：行っていない。
- 本完了報告はcommitに混ぜていない。
