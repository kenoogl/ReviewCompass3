# 第5段 G25 Session記録 読取り専用入口 限定修正Evidence v1

- 実施日：2026-08-14
- 先行独立完了レビュー：
  `records/development/2026-08-14-stage5-g25-session-artifact-read-only-entry-independent-completion-review-v1.md`
- 先行レビューSHA-256：`798761ac4a77ff03c54327c0315f4687e8b149d287a0d6d78c6439f45609e5d7`
- 先行レビューcommit：`f6cf47b1d2b83e602c687f58bf8fcae807dfe967`
- 限定RED commit：`208276c2bcaa784e85ca944e59339e2550f8b033`
- 限定GREEN commit：`8d7abafba03871dbe050b3c685592105589c0289`
- 判定：`correction_complete_pending_one_time_review`

## 1. 修正した問題

【実測】先行独立レビューは次の二点を止める指摘とした。

1. `absolute path:/Users/example/project`と`file:///Users/example/project`を絶対pathとして検出せず、
   終了コード0、`status: ok`で転写と要約へ残した。
2. Human受入前なのに、新入口が`stable / normative / promotion_required: false`と表示していた。

【判断】二点とも先行レビューが示した最小範囲だけを修正した。新しい検査器、別試験file、G25既存10 path、
`pyproject.toml`、契約、上流候補は変更していない。

## 2. 限定RED

【実測】既存のparameter付き停止試験へ、先行レビューが実証した二つの入力例だけを追加した。別の試験関数や
試験fileは追加していない。

現行実装に対する対象試験の結果は、10件成功、追加二例だけ失敗、終了コード1だった。二例はどちらも、期待する
終了コード4に対して実際は終了コード0となり、先行レビューと同じ見逃しを再現した。

## 3. 限定GREEN

【実測】`tools/session_logs/read_only_entry.py`一件だけを次のように修正した。

- 絶対path検査の直前除外から`:`を外し、`path:/Users/...`を検出する。
- 検査前に`file://`を除去し、`file:///Users/...`を絶対pathとして検出する。
- 先頭の成熟度表示を`provisional / non-normative / promotion_required: true`へ戻す。

【実測】限定GREEN時の内容識別値は次のとおりである。

| path | SHA-256 |
| --- | --- |
| `tools/session_logs/read_only_entry.py` | `8d03610aaa677b9e4d6d4271fbb698ddd81928db95a72b14e7eb4e3588592c8a` |
| `tests/test_session_log_read_only_entry.py` | `8152c5bb82ca235d723aac69fb519b2b6284a3f92cf6e2972328b4f479e5e053` |

## 4. 修正後の試験

| 確認 | 結果 | 終了コード |
| --- | --- | --- |
| 新入口の対象試験 | 12件成功 | 0 |
| 対象12件＋G25直接関連55件 | 67件成功 | 0 |
| 正規全試験 | 1,740件成功、失敗0、error 0、skip 0 | 0 |

【実測】正規全試験はPython 3.13.14、pytest 8.4.2、runner版2、代替実行なしだった。リポジトリ外の受領記録は
`/private/tmp/reviewcompass-stage5-g25-correction-full-receipt.json`、SHA-256は
`706ea8c6e8a8330d0a724d42cf0b7129cc875dee50cdb2c1538a5f3e72b4f3b9`、状態識別値は
`4251a9480253624dadf3d763254ae9096d56b54fe875e8923927bc793d7df6ff`である。本Evidence追加前の
限定GREEN commit全体へ結び付く。

【判断】試験件数は追加した二反例を含む現在集合の観測値であり、恒久的な合格値または増加目標にはしない。

## 5. staleと次の確認

【判断】先行実装Evidence §5の「低い乱雑性の絶対pathが残れば成功成果を返さない」という主張と、同Evidenceの
完了候補表示は、先行レビューの`report_execution_mismatch`によりstaleである。本Evidenceと一回限りの
修正後レビューで二指摘の解消を確認するまで再利用しない。

【判断】次は、先行独立担当が二指摘だけを一回限り確認する。確認対象は、追加二例が固定停止結果になること、
成熟度表示がHuman受入前の状態へ戻ったこと、二pathだけの訂正、対象・関連・正規全試験と状態の結び付きである。
既に確認済みの三形式、配布入口、禁止副作用、G25境界は変更がないため全面再確認しない。

## 6. 未実施

【未実施】Human受入、正式・安定表示への昇格、第5段完了は行っていない。G25既存10 path、`pyproject.toml`、
G26、G30、他142 path、契約、上流候補、Issue、TODOは変更していない。新しい検査器、台帳、関門、別試験file、
保存、探索、外部送信、network、push、tag、amend、rebase、reset、履歴書換えは扱っていない。
