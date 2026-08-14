# 第3段 既知の正しい現在状態による試験誤拒否確認 実施Evidence v1

- 実施日：2026-08-14
- 観測commit：`72a6f4ac04839144289ea3b21f7af2c6ebcd482e`
- 作業票：`docs/development/2026-08-14-stage3-known-correct-state-witness-bootstrap-work-ticket-v1.md`
- 作業票SHA-256：`4751a59349bec3c912f90f90773abd25e5a29b12e822a25e5c84d64b0a00d459`
- 開始前レビュー：`records/development/2026-08-14-stage3-known-correct-state-witness-start-review-v1.md`
- 開始前レビューSHA-256：`e5a26de77fba1b4b7a85004dd30485903f5372fcb31494cac3d5ae1ee40a2507`
- 判定：`passed`

## 1. 実施範囲

【実測】観測commitをリポジトリ外のGit複製へ固定し、元repositoryのPython 3.13環境を一時的に参照させた。
構造化記録の再計算、正規収集、正規全試験をその複製だけで実行した。リポジトリ内の変更は本Evidence一件だけで、
コード、試験、設定、Issue、既存Decision・Evidence、TODO、計画、開発方針は変更していない。

【記録】確認対象は、承認済みの現在設計から次の二点だけである。

1. V4の登録済みIssueと候補は複数存在でき、最大一件の制約は活動中のIssueだけに適用される。
2. 候補参照は一括資料形式と単独記録形式の両方を許し、一括資料SHA-256の制約は一括資料形式だけに適用される。

## 2. 現在状態の機械再計算

【実測】JSONを機械読込みして、次を得た。commandは終了コード0だった。

```json
{
  "active_issue_count": 0,
  "active_issue_states": ["in_progress"],
  "candidate_files": 11,
  "candidate_record_kinds": {
    "historical_candidate_allowlist": 1,
    "improvement_candidate": 10
  },
  "decision_files": 49,
  "decision_ref_forms": {
    "bundle": 41,
    "single": 8
  },
  "issue_files": 8,
  "issue_ref_forms": {
    "bundle": 3,
    "single": 5
  },
  "issue_states": {
    "registered": 8
  },
  "maximum_active_issues": 1
}
```

【判断】開始前レビューの訂正に従い、候補file 11件を候補record 11件とは扱わない。内訳は、
`improvement_candidate` 10件と履歴allowlist 1件である。件数は現在状態の観測であり、新しい固定値または将来の
合格条件にはしない。複数の登録済み記録、活動中だけを最大一件にする設定、二つの参照形式の同居は再現できた。

## 3. 試験集合

【実測】Git履歴を含む最終一時複製で、次の正規収集commandを単独実行した。

```text
.venv/bin/python3 -B -m pytest --collect-only -q -p no:cacheprovider
```

終了コードは0、収集は1,728件だった。別の機械集計では1,728件、unique 1,728件、重複0件、
試験識別子一覧SHA-256は
`5a22372d02cf4708809a029603945a5b9ff4d5c7c06aea66468da198b60b62e1`で、作業票の固定値と一致した。

## 4. 正規全試験

【実測】観測commitへdetached checkoutしたGit複製を作業directoryとし、元repositoryの`.venv`を指す一時symlinkを
設けたうえで、次の正規入口を単独実行した。

```text
.venv/bin/python3 -B -m tools.development.policy_test_runner \
  --suite full \
  --receipt /private/tmp/reviewcompass-stage3-known-witness.pLkAnf/repo-git-full-receipt.json
```

結果は終了コード0、`passed` 1,728件、失敗0件、error 0件、skip 0件だった。Python 3.13.14、
pytest 8.4.2、runner版2、fallbackなしである。受領記録の`source_state_digest`は
`bc34c22c1da80a59c835d6c1d56102f6f86f97911cb6ea9e9baf180a752c30d1`、受領記録SHA-256は
`9787a0cf26a319d9fe7627d0327824d4b758f3d285ad00ae4da7b8b1bba7e9e4`である。受領記録はrepository外に置いた。

【判断】二つの承認済み現在状態を含む観測commitを、現役の1,728試験は不合格にしなかった。
この二点について、現在の正しい実装を古い期待結果が誤って拒否する事象は実証されなかった。

## 5. 手戻りと環境失敗

【実測】最終成功前に、一時環境の前提を二度取り違えた。いずれも二つの設計観点に関する試験不合格ではない。

1. 最初のarchive展開では`.venv`がなく、正規runnerが`configured_python_missing`で終了コード1となった。
   試験は開始されず、受領記録は作られなかった。
2. 元repositoryの`.venv`を参照させた二回目は、archive展開にGit履歴がなかった。正規runnerは
   1,703件成功・25件失敗・終了コード1となった。25件はすべて`git cat-file`等で固定commitを読む試験で、
   Git repositoryでないことを原因としていた。受領記録SHA-256は
   `5af5bd67555d59589b5a92448dbbc731a1cbe6d5ae94e032844c7d1286af3816`である。

【判断】対象操作は一時複製での正規全試験、期待executorと実executorはいずれも
`tools.development.policy_test_runner`だった。手作業が生じた理由は、作業票の「一時directoryへ展開」から、
runnerが必要とするPython環境と25試験が必要とするGit履歴を実行前に具体化しなかったためである。
回復は、新機構を作らず、Git履歴とPython環境を最初から備えた一つの一時複製へ置き換えた。
機械処理候補は、同種の実行ではarchiveでなく履歴付き一時複製を選ぶことだが、今回のための恒久script・検査器・
試験・関門は作らない。routeは本作業内の環境回復で閉じ、製品・開発支援コードの修正候補にはしない。

## 6. 限界と未実施

【判断】本確認が示すのは、二つの既知の正しい現在状態を観測commitの全試験が拒否しないことだけである。
現在設計が許すあらゆる将来実装、誤った実装の受理、守れない保証、安全方針に反する副作用を証明しない。

【実測】全試験、全Decision、全参照の人手精査、不完全な17件候補・495参照・旧参照文字列抽出の再利用、
新しい候補・Issue・入力の作成、コード・試験・設定の変更、試験削減、第3段完了判断、外部送信は実施していない。
