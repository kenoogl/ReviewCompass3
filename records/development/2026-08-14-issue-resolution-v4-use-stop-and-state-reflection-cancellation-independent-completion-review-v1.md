# Issue解決処理v4の使用停止と状態反映中止 独立完了レビュー v1

- レビュー日：2026-08-14
- 対象commit：`cad1265c190f640f7c2797282568d776430fdf06`
- 親commit：`1dc636d71c743188e333a38ef2bf99f1a6d1c5f7`
- 対象Decision：
  `records/development/2026-08-14-issue-resolution-v4-use-stop-and-state-reflection-cancellation-decision-v1.md`
- 対象Decision SHA-256：`c20ee11c368145cab3103a802af2f5aa6f64649202b684976f535c6d97a640b1`
- 対象TODO：`TODO_NEXT_SESSION.md`
- 対象TODO SHA-256：`aafe25d4ac4f77842b8224463f2193c765cd9d3f7e0404ebf8e778402cc316d6`

## 1. 判定

【判断】`verified`。

【判断】利用者が明示した中止判断はDecisionとTODOへ過不足なく反映されている。修正案Cと正式利用を採用せず、
対象Issueを`registered`、対象処理を暫定・使用停止のまま維持し、G01の実装完了判断を変えずに第3段の
成果物整理へ戻る境界は成立している。

## 2. 利用者判断との一致

【記録】Decision §1は、利用者の次の判断を全文で保持する。

- 修正案CとIssue状態更新処理の正式利用を承認しない。
- 本作業を中止する。
- 対象Issueを`registered`、対象処理を暫定・使用停止のまま維持する。
- G01の実装完了判断を変更しない。
- 確認した欠陥と中止判断を証跡へ残す。
- TODO更新後に第3段の方針修正へ戻る。
- コード、試験、設定を変更しない。

【実測】Decision §2から§7は、この判断を状態、変更しない範囲、次の作業、未実施事項へ具体化している。
修正案C、別案、正式利用化、Issue状態反映を次の判断待ちに残しておらず、中止判断と矛盾しない。

## 3. 欠陥と固定記録

【実測】`IR-MAT-001`を記録した3文書のSHA-256は、Decisionの記載値と一致した。

| 対象 | SHA-256 | 確認内容 |
| --- | --- | --- |
| 成熟度精査Evidence | `8038ce27b0c3fa41e0ebdb70a860811d4bb7e1649847b16c0a88c25d5834d050` | 親フォルダ作成失敗でIssueだけが`resolved`に残る反証を記録 |
| 独立完了レビュー | `893fde2d1d05f438f47b87fe28ac5c5103081ac0eec127019a14f58c7b7aa1fd` | 別の使い捨て複製と独自の故障注入でも同じ片残りを再現 |
| 限定訂正レビュー | `7e69b63f1dc34b9920b92acb4a388f6610319670f08550e0aa6cc7870d854470` | 原因を生の`OSError`が既存復元処理へ入らないことに訂正し、`verified` |

【実測】現在の`resolve_issue`を構文木で照合すると、親フォルダ作成は255行目、これを囲む`try`は254行目で、
捕捉対象は`ResolutionError`だけだった。`OSError`は捕捉対象に無く、限定訂正後の原因説明と一致する。

【判断】中止Decisionは欠陥を解消済みとは扱わず、欠陥が残る処理を使用停止にする。確認済みの事実と利用者の
採否判断を混同していない。

## 4. Issue、対象処理、G01の状態

【実測】対象Issue
`.reviewcompass/workflow/issues-v4/issue-authority-reference-digest-check-001--v1.json`は、
issue version 1、state `registered`、SHA-256
`d260ed570598f56ada2cd6b4e54f15543bba0e792db65c14403a038f8100afbe`である。
単体検証とIssue台帳全体検証は終了コード0で合格した。`cad1265`の親commitとのbytes差分も0件だった。

【実測】`tools/development/issue_resolution_v4.py`の宣言は次のままである。

- `lifecycle: provisional`
- `normative_status: non-normative`
- `promotion_required: true`

【実測】対象コード、対象試験、対象設定のSHA-256は成熟度精査の固定値と一致した。

| 対象 | SHA-256 |
| --- | --- |
| `tools/development/issue_resolution_v4.py` | `770585427e6185730506ec6aa5da8004a79d77e2cee00e9b4210290d03a2bae8` |
| `tests/test_issue_resolution_v4.py` | `d1d09ab998ebed10a85a9f93613463ba756593052a214853d02b52aab749a4fb` |
| `config/development-issue-resolution-pilot-v4.json` | `ed274e487318d44baed701ffbc8a1130df3e9d81cadca96515848a2bea228a8e` |

【実測】3件とも`cad1265`の親commitから差分0だった。

【実測】G01独立完了レビューのSHA-256は
`c441ef796f34959cadf5a111826af50fa02e46a3e367f896768a417940f78515`で、判定`verified`、
止める指摘0件、報告不一致0件だった。同レビューはIssue状態反映をG01完了に含めていない。

【判断】Issue状態反映の中止はG01の完了判断を崩さない。DecisionとTODOがG01を完了のまま扱うことは、
G01独立完了レビューの境界と一致する。

## 5. TODOの機械確認

【実測】既存の構造化入力
`/private/tmp/reviewcompass_todo_projection_20260814.json`を既存の
`todo_handoff_projection.render_todo_handoff`で再描画し、`TODO_NEXT_SESSION.md`を再読込して比較した。
5,617 bytesが一字一句一致し、終了コード0だった。

【実測】正規入口`python3 -m tools.development.todo_handoff TODO_NEXT_SESSION.md`は、
`findings: []`、`status: passed`、終了コード0だった。参照先6件のSHA-256も実ファイルと一致した。

【実測】TODOの現役Issueは一件だけで、
`ISSUE-TEST-GROWTH-STATE-PINNING-001`、state `registered / 第3段整理を継続`である。
同Issueの正式recordもissue version 1、state `registered`だった。

【実測】次の一作業は、第3段開始時点から段完了候補までに追加・変更したコード、試験、文書を
機械列挙するための範囲を軽量作業票へ固定することに限定される。列挙結果の採否、削除、統合、コード、試験、
設定の変更は含まない。

【判断】Issue状態反映の枝を閉じ、第3段の方針修正へ戻る現在位置は、利用者判断とDecisionに一致する。

## 6. commitの変更範囲

【実測】`cad1265`の変更pathは次の2件だけだった。

1. `TODO_NEXT_SESSION.md`
2. `records/development/2026-08-14-issue-resolution-v4-use-stop-and-state-reflection-cancellation-decision-v1.md`

【実測】立て直し計画v5、第3段追補判断、第4段の二つの追補判断、対象コード、対象試験、対象設定、対象Issue、
G01独立完了レビューを親commitと比較し、差分0、終了コード0だった。現在のSHA-256は次のとおりである。

| 対象 | SHA-256 |
| --- | --- |
| 立て直し計画v5 | `5e0ab06b682939ab0c6e5804db02ee31952059a4404b8a21fe38ef07532514b3` |
| 第3段成果物整理の追補判断 | `181c74b9b325df9544ce195e3344aee60d0090cce61ab4f136f5d8c1f9da00db` |
| 第4段正式製品コード識別の追補判断 | `1e21e6af4be4898e98436206b950efed4e6cca825397fbc85a9030455e5e94e3` |
| 第4段軽量コード整理境界の追補判断 | `d54a486c93a6d0f25411765f99a7fdb669edfb1db84c7a9298a2d9b5dfb8e70a` |

【実測】`git diff --check cad1265^ cad1265`は終了コード0だった。

## 7. 止める指摘

【判断】0件。

## 8. 報告不一致

【判断】0件。

## 9. 試した反証

1. 【実測】中止Decisionと反対にIssueが`resolved`へ変わっている可能性を、JSON再読込、SHA-256、
   正規のIssue単体検証、親commitとの差分で確認した。version 1、`registered`、bytes不変で、反証は不成立だった。
2. 【実測】処理が既に正式利用可能な宣言へ変わっている可能性を、先頭宣言、SHA-256、親commitとの差分で確認した。
   `provisional`、`non-normative`、`promotion_required: true`のままで、反証は不成立だった。
3. 【実測】TODOが文章だけを手で合わせ、構造化入力とずれている可能性を再描画とbytes比較で確認した。
   一字一句一致し、正規検証にも合格したため、反証は不成立だった。
4. 【実測】G01完了判断がIssue状態反映を前提としている可能性を独立完了レビューで確認した。
   同レビューはIssue状態反映を完了範囲外と明記しており、反証は不成立だった。

【実測】Issue単体検証の最初の呼出しでは、検証関数が要求するリポジトリ相対pathではなく絶対pathを渡し、
`v4_issue_path_mismatch`で終了コード1になった。関数の契約を再読込し、相対pathで単独再実行すると終了コード0で
合格した。これは対象Issueの不一致ではなく、レビュー側の呼出し引数の誤りである。

## 10. 未実施

【未実施】コード、試験、設定、Issue、立て直し計画、第3段・第4段追補判断、G01成果物、既存Evidenceの変更、
修正案C、別修正案、正式利用化、状態反映、Human裁定JSON・解決記録、新しい機構・検査器・試験・関門、
第3段成果物の列挙・分類・整理、第3段・第4段の完了判断、外部送信、履歴書換えは行っていない。

【未実施】コード、試験、設定が変わっていないため、全試験は再実行していない。本レビューで行ったのは、
読み取り、内容識別値・差分・構文木の照合、既存のIssue検証、TODO再描画と正規検証だけである。
