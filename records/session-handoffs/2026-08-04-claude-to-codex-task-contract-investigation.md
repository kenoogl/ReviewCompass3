# Claude → Codex：Task Contract 固定入力の調査結果

指示：`records/session-handoffs/2026-08-04-codex-to-claude-task-contract-investigation.md`
実施：読み取り専用調査のみ。commitしていない。Task Contract、Plan、Checklist、TODO、testは変更していない。

## 1. 確認した事実

### 1.1 Current Planを固定sourceに持つTask Contract

`records/task-contract/*.json`の全24 fileを走査した。`fixed_sources`を持つのは4件で、
Current Planを固定しているのは1件だけである。

| contract | status | fixed_sources | Current Plan | 現在の不一致 |
| --- | --- | --- | --- | --- |
| `issue-resolution-early-pilot-v1.json` | `active` | 9 | あり | 1件（Current Plan） |
| `session-transcript-eventual-preservation-v1.json` | `active` | 5 | なし | **1件（Development Policy）** |
| `issue-resolution-todo-compaction-implementation-v1.json` | status field無し | 3 | なし | 0 |
| `issue-resolution-todo-compaction-implementation-v2.json` | status field無し | 3 | なし | 0 |

残り20件は`task-contract-centered-documentation-v1`〜`v16`等で、`fixed_sources`を持たない。

### 1.2 同じ問題が別のactive contractで既に発生していた

`session-transcript-eventual-preservation-v1`（`active`）は
`docs/development/2026-08-02-development-policy.md`を固定しているが、
pinned `d37a60ab273520f8…`に対し実際は`9078276d7ba1f540…`で**既にstaleである**。

原因はWork 4A v1のrevert commit `3bca31c`で、`c6bbabf`が加えた記述を戻したことによる。
このcontractを検証するvalidatorが存在しないため、全testは通過し続けていた。
つまり今回のPlan更新は新しい問題を作ったのではなく、**検証範囲に入っている1件で同じ問題が
可視化された**にすぎない。

### 1.3 固定されたDigestはcommitへ一意に対応する

pinned `0ab828f4d940ab8a6a4d285479afbb1fdbc086afbb72fb993b885599f9bf2694`は
commit `c475bec`時点のblobと一致する。前後のcommitは別Digestである
（`601bbb1`は`911d0c49…`、`1968eee`は`0ae6bef9…`）。
したがって`Git commit + repository-relative path + SHA-256`による特定は、この対象で成立する。

### 1.4 contract自身がin-place書換えを停止条件にしている

`issue-resolution-early-pilot-v1`の`stop_conditions`に次がある。

> fixed predecessor, Plan, Requirement, Test, or Decision source would be rewritten in place

Current Planのin-place更新はこの停止条件に該当する。validatorの実装だけの問題ではなく、
contractが明示的に禁じた操作を行った状態である。

### 1.5 validatorと参照関係

- `tools/development/issue_resolution_pilot.py:202` `validate_task_contract_sources`が、
  contract IDとstatusを固定確認したうえで、9件の`fixed_sources`を
  `_validate_file_reference`（同124行）へ渡す。
- `_validate_file_reference`は`_require_exact_fields(reference, ("path","sha256"))`で
  **fieldを厳密に2つへ固定**し、working tree上のfileのSHA-256一致を要求する。
  commitやversionを受け付ける余地は現行schemaに無い。
- 同validatorは`validate_implementation_task_contract_v2`（333行）からも使われる。
- CLIは`issue_resolution_pilot.py:1491`で`fixed_source_count`を出力する。
- testは`tests/test_issue_resolution_pilot.py:163`の1箇所だけが
  `validate_task_contract_sources(...) == 9`を検査する。

### 1.6 後続Task Contractと状態記録

`issue-resolution-early-pilot-v1`の後続version（v2以降）は存在しない。
`records/task-contract/`にPilot関連は当該1 fileのみである。
状態記録は`records/development/`のcompletion evidence 3件が
`TC-RC3-ISSUE-RESOLUTION-EARLY-PILOT-2026-08-04-V1`の第2・第3作業単位の完了を述べているが、
contract file内の`current_work_unit`は第1作業単位のままである。
contract fileは作業進行に追随していない。

## 2. 根本原因

**更新され続ける文書を、不変の固定入力として、内容Digestだけで参照している。**

`docs/current/reviewcompass3-plan-current.md`は「現在の計画」を表す生きた文書であり、
承認のたびに更新される。一方Task Contractの`fixed_sources`は「この契約が受理された時点の入力」
を意味し、`_require_exact_fields`が`path`と`sha256`の2 fieldへ厳密に固定している。

この2つを同じ参照形式で結ぶと、次の二択しか無くなる。

- Current Planを更新しない（生きた文書の役割を失う）
- contractのDigestを書き換える（受理時点の来歴を失い、停止条件1.4にも反する）

参照形式に**時点を表す要素が無い**ことが原因である。`path`は場所、`sha256`は内容を表すが、
「どの時点の内容か」を表す項目が無いため、validatorは「現在のworking treeと一致するか」しか
判定できない。1.2のように、検証されていないcontractでは同じ破綻が静かに起きる。

## 3. 最小の恒久対応案

**固定入力の解決先をworking treeからGit blobへ移す。既存contract fileは変更しない。**

新しいrecord種別`task_contract_source_pin`を`records/development/`へnew-onlyで置き、
contract IDとpathの組に対して解決先commitを与える。

```json
{
  "record_kind": "task_contract_source_pin",
  "schema_version": 1,
  "pin_id": "TCSP-RC3-ISSUE-RESOLUTION-EARLY-PILOT-2026-08-04-V1-001",
  "task_contract_id": "TC-RC3-ISSUE-RESOLUTION-EARLY-PILOT-2026-08-04-V1",
  "task_contract_sha256": "<contract file自身のDigest>",
  "pins": [
    {
      "path": "docs/current/reviewcompass3-plan-current.md",
      "sha256": "0ab828f4d940ab8a6a4d285479afbb1fdbc086afbb72fb993b885599f9bf2694",
      "commit": "c475becb3ebf3f3cb9e362d64bab79606ed3719d",
      "reason": "fixed source at contract acceptance"
    }
  ],
  "content_digest": "<canonical digest>"
}
```

validatorの解決順序を次にする。

1. contractの`fixed_sources`を読む。schemaは`path`と`sha256`の2 fieldのまま変更しない。
2. 当該contract IDのpin recordを探す。
   - **ある場合**：`git cat-file blob <commit>:<path>`のDigestが`sha256`と一致することを要求する。
     working treeとの一致は要求しない。
   - **ない場合**：現行どおりworking treeとの一致を要求する（後方互換）。
3. pin recordの`task_contract_sha256`がcontract file自身のDigestと一致しなければ停止する。
   contractが差し替わったpinを流用させない。
4. commitが解決できない、blobが取得できない、gitが使えない場合は
   `pin_unresolvable`として**停止する**。working treeへ黙って落とさない。

この方式なら次を同時に満たす。

- 既存contract fileを1 byteも変更しない。停止条件1.4に触れない。
- 受理時点の入力を、commitとDigestの両方で検証できる（historic検証）。
- Current Planは更新できる。更新してもpinはcommit側を見るため影響しない。
- pin recordはnew-onlyで、後から別pinを足しても過去のpinを書き換えない。

`git`呼出の前例は`tools/development/work_unit_transition.py:54`にあり、新規依存ではない。
なお本validatorはdevelopment toolingであり、deployment実行時経路ではないため、
git依存の追加は配布境界に影響しない。

pin recordを持たないcontractは現行動作のままなので、1.2の
`session-transcript-eventual-preservation-v1`は本対応では自動的に解決しない。
同じ形式でpin recordを与えるか、staleとして別途裁定するかは、この対応の適用対象を
広げる判断であり、§5の一点に含める。

## 4. migration対象とvalidator／testへの影響

### 4.1 migration対象

| 対象 | 操作 | 変更の有無 |
| --- | --- | --- |
| `records/task-contract/issue-resolution-early-pilot-v1.json` | 変更しない | 無 |
| `records/task-contract/session-transcript-eventual-preservation-v1.json` | 変更しない | 無 |
| 新規 pin record（Pilot契約分、1件） | new-only作成 | 追加のみ |
| 新規 pin record（session-transcript契約分、1件） | §5の判断次第 | 追加のみ |
| `docs/current/reviewcompass3-plan-current.md` | 現在の未コミット変更を保持 | 既存の未コミット差分のみ |

過去commitのrevertもhistory書換えも不要である。

### 4.2 validatorの変更範囲

`tools/development/issue_resolution_pilot.py`のみ。

| 箇所 | 変更 |
| --- | --- |
| `_validate_file_reference`（124行） | commit解決経路を受け取れるよう引数を1つ増やす。`_require_exact_fields`の2 field固定は維持 |
| 新規 `_resolve_pinned_blob` | `git cat-file blob <commit>:<path>`のDigestを返す。失敗は`pin_unresolvable` |
| 新規 `load_task_contract_source_pin` | contract IDでpin recordを引き、`task_contract_sha256`を照合 |
| `validate_task_contract_sources`（202行） | pin recordの有無で解決先を切り替える |
| `validate_implementation_task_contract_v2`（333行） | 同じ解決経路を共有する（現状の呼出形は維持） |
| CLI（1491行） | 出力に`pin_resolved_count`を追加する程度。既存keyは変えない |

`tools/development/work4a_rebuild_v3.py`、Work 4A関連、layout、session_logsへの影響は無い。

### 4.3 testの変更範囲

既存testの期待値は変えない。`tests/test_issue_resolution_pilot.py:163`の
`== 9`はpin解決後もそのまま成立する。

追加が要るのは次の負例・正例である（本調査では作成していない）。

1. pin recordがある場合、working treeが変わっていても解決に成功する。
2. pin recordが無い場合、現行どおりworking tree一致を要求する。
3. pinのcommitに存在するblobのDigestが`sha256`と一致しなければ停止する。
4. pinのcommitが解決できない、またはgitが使えない場合に`pin_unresolvable`で停止する。
5. pin recordの`task_contract_sha256`がcontract file自身のDigestと一致しなければ停止する。
6. pin recordが同一pathへ複数の異なるcommitを与えた場合に停止する。

## 5. Human判断が必要な一点

**activeなTask Contractの固定入力を、working treeの現在値ではなく、受理時点のGit commitの
blobで満たしたものとみなしてよいか。**

これを承認すると、固定入力の意味が「今もこの内容であること」から
「受理時点にこの内容であったこと」へ変わる。Current Planのような生きた文書を
契約から独立して更新できるようになる一方、契約の入力が現在値と乖離していても検証は通る。

承認する場合の適用対象は、現在staleな2件（`issue-resolution-early-pilot-v1`のCurrent Plan、
`session-transcript-eventual-preservation-v1`のDevelopment Policy）とする。

承認しない場合は、Current Planの更新を差し戻すか、Pilot契約を停止条件1.4に基づき
明示的にstale裁定する必要がある。いずれもWork 4Aの進行より先に決める必要がある。
