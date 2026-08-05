# TODO Evidence参照数の訂正記録 v1

- 対象：`TODO_NEXT_SESSION.md`の`## 最新のauthority／Evidence`節の参照数に関する現況主張
- 指示：人からの直接指示（報告・引継ぎの不整合だけを1作業単位で訂正する）
- この記録は、既存Evidenceと既存報告を**書き換えずに**訂正するためのものである。

## 1. 何が誤っていたか

境界訂正の作業単位で作った記録と報告に、Evidence節の参照数が`26件`と書かれている。
これを**現在の値として読むと誤り**である。現在の実値は`25件`である。

`26件`という数値そのものは、測定した時点では正しかった。誤りは、同じ作業単位の後半でTODOを
圧縮したにもかかわらず、測定時点の値をそのまま現況として残したことである。

## 2. 原因（機械で確認した増減）

境界訂正commit `1ca15ed`のTODO差分を機械で数えた結果は次である。

| 項目 | 件数 |
| --- | --- |
| 訂正前commit（`1ca15ed^`）のTODOでの参照数 | 26 |
| 同commitで削除したEvidence link | 3 |
| 同commitで追加したEvidence link | 2 |
| 現在のTODOでの参照数 | 25 |

削除した3件。

- `定型記録生成 Plan承認Decision`
- `Work 5A 実Review受理 v2`
- `Provenance閉包 無効化record`

追加した2件。

- `定型記録生成 境界訂正GREEN Evidence（有効な完了根拠）`
- `境界訂正後の全test receipt`

26 − 3 + 2 = 25である。TODOが12,288 byteの上限を超えたため、更新規則に従って累積していた
中間Evidence linkを整理した。その整理の後に、測定済みの`26件`という記述を見直さなかった。

## 3. 正しい実値

現在の値は`25件`である。手計算ではなく、Evidence節に限定した機械処理
（`tools/development/todo_record_generation.py`の`collect_reference_digests()`）で数えた。

`## 最新のauthority／Evidence`節の範囲は、見出しの次行から次の`## `見出しの直前までである。
節外のlinkは数えない。

## 4. 訂正の対象

次の記述は**書き換えていない**。作成時点の測定として履歴に残す。現在の値として読まないこと。

| file | 該当箇所 |
| --- | --- |
| `records/development/2026-08-05-record-generation-todo-green-evidence-v1.md` | 「参照のSHA-256は全26件を…」「参照Digest照合｜26件一致」 |
| `records/development/2026-08-05-record-generation-todo-boundary-repair-green-evidence-v1.md` | 「実測：節内`26件`」「節外linkを足しても収集は`26件`のまま増えない」 |
| `records/session-handoffs/2026-08-05-claude-to-codex-repair-record-generation-todo-boundaries.md`（Git管理外のローカル報告） | 「節内`26件`」 |

これらはいずれも、測定した時点のTODOに対しては正しい。現況としての参照数は、本記録と
`TODO_NEXT_SESSION.md`の記載を正とする。

## 5. あわせて行った引継ぎの訂正

`TODO_NEXT_SESSION.md`について次を更新した。

- `## 現在位置`へ、Evidence参照が機械計測で25件であることと、本訂正記録のpathを記載した。
- `## 次に行う一作業`を、完了済みの「TODO最小縦切りをTest先行で実装する」から、
  「次の作業候補を提示し、人の選択を待つ」へ置き換えた。候補A〜Dを並べ、選択があるまで
  新しい実装へ着手しないことを明記した。

## 6. この訂正で変更していないもの

- code、test、config、Decision、Issue、Task Contract：いずれも変更していない。
- Work 4Aの実装code：触っていない。
- 既存Evidenceと既存報告の本文：書き換えていない。
- TODOの機械管理部分（「直近の全Test」行、Evidence節のSHA-256値）：値は変わっていない。
  test件数に影響する変更をしていないためである。
