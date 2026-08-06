---
evidence_id: RC3-SESSION-TRANSCRIPT-CURRENT-CODEX-RECAPTURE-2026-08-06-V1
recorded_at: 2026-08-06T09:24:03+09:00
status: verified
workflow_state: reconciled
confidentiality_class: project-internal-value-safe
---

# Current Codex Session Recapture Evidence V1

## 1. 実施と判断

Humanの「修復と再承認後、codexのセッションログを記録する」という指示に基づき、Codexサブエージェントを
executorとして、承認済みの現行Codex rollout 1件だけをrepository外private archiveへmanual reconcileした。
Task Contract v2の固定source 5件、再承認Decision、source identity、既存rawのbyte-exact prefixを事前照合し、
すべて一致したため実行した。

初回は`updated / reconciled`、同一入力による直後の再実行は`unchanged / reconciled`だった。保存後の独立再読込、
再生成、Digest、Tool pair、permission、temporary file、Git境界の検証が合格したため、本作業を`verified`と判断する。

## 2. Authority

| artifact | path | SHA-256 |
| --- | --- | --- |
| Task Contract v2 | `records/task-contract/session-transcript-eventual-preservation-v2.json` | `d75049cb8f53dc0d7ae7429270c00ca539e90485133d1984edde07f61158355a` |
| Human Decision | `records/development/2026-08-06-session-transcript-repair-and-recapture-decision-v1.json` | `c6ff5904d86049f4e414e93dd3342b0ab793b1a50d0b4f664f507e2faf5c05a5` |
| Capture receipt | `records/development/2026-08-06-session-transcript-current-codex-recapture-receipt-v1.json` | `50b20407ffab16a7723d8f372681e63d9f08a2a89f6d25d633275cc28824af95` |

Task Contract v1と既存private artifactは削除、書換え、source-pinしていない。private absolute path、session本文、
prompt、response、Tool引数・結果本文はreceiptまたは本Evidenceへ記録していない。

## 3. Manual reconcile結果

| 項目 | 初回 | 直後の再実行 |
| --- | --- | --- |
| run ID | `manual-current-codex-first-20260806T092317973549+0900` | `manual-current-codex-rerun-20260806T092318443386+0900` |
| observed at | `2026-08-06T09:23:17.973549+09:00` | `2026-08-06T09:23:18.443386+09:00` |
| action | `updated` | `unchanged` |
| state | `reconciled` | `reconciled` |

- source kind：`codex_rollout`
- source identity：`619ff2b0e985199b0006a7166f12ed4b2af26c291ecb1662a9d41d093ac023df`
- capture前raw：19,305,386 bytes
- capture後raw：74,070,599 bytes
- 追加：54,765,213 bytes
- capture後verbatim：19,806,111 bytes
- JSON record：25,196件
- transcript event：8,458件
- parse issue：0件

二回目はraw byte数、event数、issue数を変えず、追加byteまたは重複eventを生じなかった。

## 4. 保存後の独立照合

| artifact | SHA-256 |
| --- | --- |
| raw | `4e7f0b5db5aa0f562958b7f540c90dafd6702cfeae5236d0a83b396df27c412c` |
| verbatim | `7e354804ffa0b9e3ebb709b36a07b219530630dd3feef05a28355b27ceeee312` |
| cursor | `834c330f5c0b15336ab8a4ab1db3f18d59d4a9f77d1c1c5dff7256e18bcaf04d` |
| Provenance | `c4ffdb965767d7ed67870b2af9accce0e12365cff925617fd130c87dfbf096f2` |
| ledger | `29cb46710ca0484d2a71cdc516a67a680803cd78e5b7a77cc864f6c330b17811` |

機械検証結果は次のとおりである。

- rawはUTF-8、末尾改行あり、全25,196非空行がJSON objectで、invalid JSON 0件だった。
- cursorのraw byte数、parse offset、event数、issue数、Digestは実fileと一致した。
- rawから再生成した逐語録は保存逐語録とbyte単位で一致した。
- cursor、Provenance、ledgerのsource、raw、parse、artifact identityとDigestは一致した。
- Tool Call 3,229件、Tool Result 3,229件、未対応Call 0件、未対応Result 0件だった。
- relevant directoryは`0700`、artifact fileは`0600`だった。
- temporary fileとlock fileの残留は0件だった。
- private archiveはrepository外であり、private artifactはGit管理対象に入っていない。

## 5. Testとrepository境界

- 関連Test：
  `python3 -m pytest -q tests/test_session_log_eventual_preservation.py tests/test_task_contract_source_resolution.py`
- 結果：`25 passed in 0.72s`、exit code 0
- 公式全Test：`python3 -m pytest -q`
- 結果：`1013 passed in 7.22s`、exit code 0

capture前後で、既存Work 6Aの次のdirty差分は同一だった。本作業では変更、stage、commitへ混入していない。

- `tools/development/session_log_bootstrap.py`
- `records/development/2026-08-06-work6a-projection-green-scope-decision-v1.md`
- `records/development/2026-08-06-work6a-projection-negative-green-evidence-v1.md`

## 6. 未実施

- historical Codex sessionの探索またはcapture
- Claude sessionのcapture
- redacted transcript生成
- hook、watcher、scheduler、background process、serviceの有効化
- 外部送信、push、PR、CI
- private artifactのGit保存
- retention削除、backup、application-layer暗号化
- Work 6A実装変更

以上により、現行Codex sessionのmanual reconcileと即時冪等再実行は`verified`である。
