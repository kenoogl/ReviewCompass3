# V4 Issue resolve tool 完了レビュー結果 v1

- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：completion（完了レビュー）
- risk：`high`（Human確定済み）
- 判定：`report_execution_mismatch`
- Finding：blocking 3件、non-blocking 0件

【実測】起動時に表示されたmodel名とreasoning effortは
`gpt-5.6-sol`／`high`だった。

## 1. 固定対象と開始状態

- レビュー依頼：`records/session-handoffs/2026-08-10-claude-pilot-issue-resolution-tool-review-request-v1.md`
- レビュー依頼commit：`fd2e09c5978bd13bbc2654610ce63d759259db3c`
- 有効scope：`records/session-handoffs/2026-08-10-claude-pilot-issue-resolution-tool-scope-v2.md`
- scope SHA-256：`ddc4b312ca529f58c38f2ad90127e0ec5ef065b03ffb1af17c1b10076eff2ee7`
- SCOPE v2のbase：`9d8667f3d6a559d12703747e130d7e1a7b58cc41`
- branch：`main`
- 許可範囲：本判定recordの作成と単独commit
- 禁止範囲：実装、Test、既存record、config、schema、実workflow台帳、TODO、checklist、
  実Issueの状態変更、外部操作、修復作業、次段作業
- 停止条件：固定入力不一致、Test不合格、受入条件の反証成立、Human境界違反、scope逸脱

【実測】レビュー開始時のworktreeとindexはcleanだった。依頼書は自分宛の最新review requestであり、
その親は申告GREEN commit `380e501900e432ab14e350ea801c0c86f6bcfc3e`と一致した。

## 2. Claimの分解

### 実施

【実測】SCOPE v2、範囲レビュー、RED、GREEN、review requestは直列のcommit列として存在する。
GREENは新規実装・Evidence・receiptだけ、review requestは依頼書だけを変更している。

### 結果

【実測】targeted 16件、関連回帰67件、公式全Test 1373件の合格はReviewer再実行でも一致した。
成果物4件のSHA-256も依頼書と一致した。ただし、追加反証により「非Human裁定を拒否」と
「失敗時の完全復元」は実挙動と一致しなかった。

### 判断

【記録】risk `high`、案B、遷移元`registered`限定、RED開始はHuman承認済みである。
【判断】toolの`verified`、実Issueへの適用、段完了を認める条件は満たしていない。

### 未実施

【実測】対象commit列に実workflow台帳、既存tool、config、schema、TODO、checklistの変更はない。
【記録】実Issueのresolveは未実施として依頼されている。今回のReviewerも実Issueを変更していない。

### 提案

修復方法は本レビューのscope外であり、実装変更は行っていない。

## 3. Git、成果物、固定入力の照合

【実測】commit列は次のとおりで、各親SHAも連続している。

| 役割 | commit | 変更path |
| --- | --- | --- |
| SCOPE v2 | `21daf5e21b84590bfaf512bdbf1be3c364c67667` | scope v2 1件 |
| 範囲レビュー | `f7c2255e32d1e75281ebcf7a6987ae4609a9cd7b` | 範囲レビューrecord 1件 |
| RED | `48bb6ad2264790d1d10bd484d8ea25a5f6544763` | `tests/test_issue_resolution_v4.py` 1件 |
| GREEN | `380e501900e432ab14e350ea801c0c86f6bcfc3e` | 実装、GREEN Evidence、receiptの3件 |
| review request | `fd2e09c5978bd13bbc2654610ce63d759259db3c` | review request 1件 |

【実測】RED commitには実装moduleが存在せず、REDからGREENまでTest差分はない。GREENの変更pathは
scope v2 §7の許可範囲内だった。`git diff --check 9d8667f..fd2e09c`は終了コード0だった。

【実測】scope v1の固定入力9件とscope v2追加2件は11／11でSHA-256が一致した。成果物の再計算値は
次のとおりで、依頼書記載値と4／4一致した。

| file | 再計算SHA-256 |
| --- | --- |
| `tools/development/issue_resolution_v4.py` | `c4b5c57dcfe69b8ce87c370361171f8eaba664f38186f1fd3db54d43c6405216` |
| `tests/test_issue_resolution_v4.py` | `29be67ce761ad0449f1adc2ba5d58e8a9a1d27ebaade4b2d7a7c8c8586e2e4a6` |
| GREEN Evidence | `5c7130f8e3576123fc7be28c3e8aed054c45c3bafddc911be94c28e650f17ef8` |
| 公式receipt | `a4887275f7074302b464020b171effdd1691d14011589cfea348588326341fe5` |

## 4. 独立再実行

### 4.1 Testとvalidator

次はすべて単独commandの終了コードで確認した。

| command | exit code | 結果 |
| --- | --- | --- |
| `.venv/bin/python3 -m pytest tests/test_issue_resolution_v4.py` | `0` | 16 passed |
| `.venv/bin/python3 -m pytest tests/test_issue_intake_v4.py tests/test_issue_intake_v4_single_candidate.py tests/test_issue_resolution_state.py` | `0` | 67 passed |
| `.venv/bin/python3 -m tools.development.policy_test_runner --suite full --receipt /private/tmp/2026-08-10-codex-issue-resolution-review-full-receipt.json` | `0` | 1373 passed、failed 0、status `passed` |

【実測】公式全TestのReviewer receiptはPython 3.9.6、pytest 8.4.2、fallback `false`だった。
合格Testだけでは、次の新作反証を検出しない。

### 4.2 Pilot fixtureにない反証：非Human裁定の受入れ

【実測】repository外の`TemporaryDirectory`に、既存intake Testの正規生成関数で合成台帳を作った。
裁定参照先の内容を`{"actor":"robot","decision":"automatic"}`、`human_id`を`robot-agent`、
`decided_at`を日時でない`not-a-timestamp`として、正しいfile SHA-256だけを渡した。
`.venv/bin/python3 -c <合成台帳作成とresolve_issue呼出し>`は終了コード0となり、結果は次だった。

```json
{
  "accepted": true,
  "decided_at": "not-a-timestamp",
  "human_id": "robot-agent",
  "state": "resolved"
}
```

【実測】`_verify_ruling`は`human_id`と`decided_at`が空でないこと、裁定参照fileが存在して
SHA-256が一致することだけを確認する。裁定recordの内容、Human主体、日時形式、入力値と
裁定recordの束縛は確認しない。既存負例はfile不在とSHA-256不一致だけであり、この入力はfixture外である。

### 4.3 同じ欠陥類型の掃討：部分書込みの2変種

【実測】同じ合成台帳で`Path.write_bytes`へ、先頭bytesを書いた後に`OSError`を送出する障害を注入した。
`.venv/bin/python3 -c <2箇所への部分書込み障害注入>`は終了コード0でprobe自体を完了し、次を観測した。

| 注入箇所 | toolの結果 | 事後状態 |
| --- | --- | --- |
| Issue recordの最初の書込み | 未処理`OSError` | 元bytesへ戻らず、19 byteの破損fileが残留 |
| 解決recordの書込み | `ResolutionError: resolution_record_write_failed` | Issueは復元したが、23 byteの部分recordが残留 |

【実測】Issue recordの最初の`write_bytes`は復元用`try`の外にある。解決record側は`OSError`時に
Issueだけを復元し、部分recordを削除しない。既存負例9は事後validator失敗だけを扱い、書込み途中の
失敗を扱っていない。scope外のdeferred #4である同時競合一般には拡張せず、今回の
「失敗時無変更・部分書込みなし」という受入条件だけを反証した。

## 5. Findings

### IR-COMP-001：非Human入力をHuman裁定として受け入れる

- 別：`blocking`
- 確認段階：`completion`
- §11.1類型：2（Human境界の欠落）、3（誤った合格を実証した検証欠陥）

【記録】上流改善候補は「Human裁定に基づく遷移」と「非Human裁定の拒否」をscopeに含む。
【実測】§4.2の自動処理recordと任意文字列だけで`resolved`遷移が成功した。
【判断】存在とSHA-256はfile identityしか証明せず、そのfileがHuman裁定であることを証明しない。
Human承認なしにterminal stateへ進めるためblockingである。

### IR-COMP-002：部分書込み失敗時に台帳の破損または部分recordが残る

- 別：`blocking`
- 確認段階：`completion`
- §11.1類型：1（承認済みscopeの無変更保証との矛盾）、3（合格Testが見逃す受入条件欠陥）

【記録】scope v2 §5.5、§6負例9、GREEN Claimは、失敗時にIssueと解決recordの変更を残さず
完全復元するとしている。【実測】§4.3の2変種はいずれかの残留を生じた。
【判断】守り役の書込み失敗が台帳破損として残るためblockingである。同じ類型の代表的な
書込み先2箇所を同じレビュー周回で確認した。

### IR-COMP-003：実config読み取り専用fixtureは固定scopeに一致しない

- 別：`blocking`
- 確認段階：`completion`
- §11.1類型：4（scope境界の破り）

【記録】scope v2 §6は`tmp_path`の「合成台帳・合成config・合成裁定recordのみ使用」と固定する。
【実測】Testの`CONFIG_V4`はrepository committedの
`config/development-issue-resolution-pilot-v4.json`を直接指し、fixtureはこれを
`intake.load_config`で読む。config bytesとGit差分には変更がなく、実台帳も参照していない。

【判断】読み取り専用であるためconfig破損や実台帳接触のside effectはなく、代表configとの整合確認には
有用である。しかしreview requestの注記は承認済みscopeを改定するauthorityではなく、Reviewerも
明記されたfixture境界を事後に読み替えられない。したがって現scopeへの適合としては**受容不可**である。
scopeをHumanが改定するか、Testを合成configへ合わせるまでは受入条件成立に数えない。

## 6. Workflow、Provenance、禁止事項

【実測】SCOPE v2→`high`範囲レビュー→RED→GREEN→review requestの順序は保たれている。
RED commitはTestだけで、GREENはTestを変更していない。固定入力と成果物Digestは一致した。

【記録】risk、案B、`registered`限定、RED開始のHuman承認はscopeとGREEN Evidenceに固定されている。
【判断】IR-COMP-001により、製品挙動上のHuman裁定境界は維持されていない。

【実測】対象commit列は許可pathだけを変更し、実workflow台帳、既存tool、config、schema、TODO、
checklistを変更していない。Reviewerの反証はrepository外の一時領域だけを使用した。
外部送信、実Issueのresolve、修復、Closer作業はReviewer未実施である。

## 7. 判定

判定：`report_execution_mismatch`

競合Evidence：

1. Claim「非Human裁定をfail-closedで拒否」に対し、自動処理record・`robot-agent`・不正日時で
   exit `0`、`resolved`遷移を実測した。
2. Claim「失敗時に完全復元し、部分書込みを残さない」に対し、Issueの19 byte破損と
   解決recordの23 byte残留を別々に実測した。

【判断】§4.7・§6の定義どおり、報告と実挙動が競合するため`report_execution_mismatch`とする。
GREEN Evidenceの「Human根拠のfail-closed」「完全復元」、完了候補、toolの`verified`可否をstaleとする。
targeted、関連回帰、公式全Testの合格という実行結果自体は維持するが、完了根拠には使わない。

変更範囲：commit列と許可pathは一致したが、fixture境界はscopeと不一致だった。

独立再実行：targeted 16、関連67、公式全1373は合格。Pilot fixture外の非Human裁定1件と、
部分書込み2変種を機械実行し、いずれも受入条件への反証が成立した。

Record照合：固定入力11件、成果物4件、commit列、Human承認、scope、GREEN Evidence、receiptを照合した。

Human境界：作業開始の承認は存在するが、toolの遷移時Human境界は欠落している。

未実施：実装修復、Test変更、scope改定、実Issueのresolve、TODO・checklist反映、Closer作業、
段完了承認、外部操作。

次：Humanが本判定を確認し、3件のblocking Findingを修復する再作業を開始するか判断する。

## 8. 反証probeの手戻り

【実測】部分書込みprobeの初回は、macOSの一時path表現が`/var/...`と`/private/var/...`で異なり、
注入対象のPath比較が一致せず、障害を注入できなかった。

- 対象操作：部分書込み障害の注入
- 期待executor／実executor：Reviewerの機械script／Reviewerの機械script
- 手作業理由：なし
- 事象とEvidence：初回は2例とも`unexpected_success`。対象path双方を`resolve()`して比較した再実行では、
  §4.3の19 byte破損と23 byte残留を再現した
- 機械処理候補・route：製品欠陥とは別のprobe実装上のpath正規化であり、改善候補化せず本recordに固定する
