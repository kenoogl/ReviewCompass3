# 第5段 G25 Session記録 読取り専用入口 実装Evidence v1

- 実施日：2026-08-14
- Task Contract：`TC-RC3-PRODUCT-G25-SESSION-ARTIFACT-PREPARATION-001` version 1
- 契約SHA-256：`20e4e0551c5b1357ba3e66d6ba849f19566da27c58c54ef98e8fa1db110fb72b`
- 承認Decision：`DEC-STAGE5-G25-SESSION-ARTIFACT-TASK-CONTRACT-APPROVAL-2026-08-14-V1`
- 承認Decision SHA-256：`dde3ad7be1a31f1c7f77e253a90fe952496950e5b6a402fcdf473388d211ae39`
- 実装前commit：`8e339d8a2c09e9f8c5d87568be3b28e0107fa38a`
- RED commit：`85e4b9031ae79308dad36161eb1150a3a8666a94`
- RED訂正commit：`3e780c22f5222b5f2a1c6ce5600f63d6783a7f4b`
- GREEN commit：`1866d3863c7dab99bfae3649f189a50f2c8ec187`
- 判定：`implementation_complete_pending_independent_review_and_human_acceptance`

## 1. 何を実装したか

【実測】利用者が許可したローカルSession記録一件を読み取り、安全な項目だけから伏字化転写、要約、来歴を
JSON一件として返す製品入口を実装した。

変更した意味単位は、承認済みの次の三pathだけである。

| path | 変更 | SHA-256 |
| --- | --- | --- |
| `tools/session_logs/read_only_entry.py` | 新しい読取り専用入口 | `b88f256cab9df9c988541408579f3930311468f3cdc292d20bdacfa97c0e5c4f` |
| `pyproject.toml` | `[project.scripts]`へ実行名一件を追加 | `ec771cd06e063d2f4b252ecfc9962d7f221effbf072169edbabfb7c8f71d3229` |
| `tests/test_session_log_read_only_entry.py` | 入口固有の契約試験 | `9ccadd6e6782e74943cb6e47e3947f4b29ac2a7f058da529ddc9e62e51bdcfdf` |

【実測】G25の既存10 path、G26、G30、他142 path、既存試験、`config/`配下、上流候補は変更していない。

## 2. 利用方法と返す内容

【実測】配布後の実行名は`reviewcompass3-session-artifact`である。利用者は、読取りを許可する絶対pathの
`--raw-root`と、その中の一fileを示す絶対pathの`--raw-log`を渡す。

正常時は次を返す。

- `status: ok`
- 記録形式
- 伏字化した転写と要約
- 元記録の相対path、行範囲、各内容識別値、tool版を持つ来歴
- 転写と要約で適用した伏字規則のlabelと件数
- `external_send_approved: false`

解析上の注意がある場合は、入力由来の詳しい文章を除き、分類、行番号、block番号だけを返して
`status: partial`、終了コード3とする。停止時は入力本文、例外本文、pathを返さず、固定した停止理由だけを返して
終了コード4とする。

## 3. REDと試験入力の訂正

【実測】新入口と実行名が無い状態で対象試験を単独実行し、10件失敗、終了コード1だった。9件は
`ModuleNotFoundError`、1件は`pyproject.toml`の実行名欠落であり、未実装理由だけだった。

【実測】実装前の試験点検で、高乱雑性の例に使った`token=`は既定の`api_key_assignment`規則が正しく伏字化し、
未登録値の例にならないことを確認した。入力名だけを`value=`へ訂正すると既存G25が
`SensitiveDataRemaining`で停止した。実装に合わせた期待結果の変更ではなく、試験目的へ合わせた入力訂正として
RED訂正commitへ一行だけ固定した。訂正後も対象試験は同じ内訳で10件失敗、終了コード1だった。

## 4. GREENと既存処理への影響

【実測】RED訂正後の試験fileを変更せず、新入口と`pyproject.toml`だけを実装した。

| 確認 | 結果 |
| --- | --- |
| 新入口の対象試験 | 10件成功、終了コード0 |
| 対象10件＋G25直接関連14 fileの55件 | 65件成功、終了コード0 |
| 正規全試験 | 1,738件成功、失敗0、error 0、skip 0、終了コード0 |

【実測】正規全試験はPython 3.13.14、pytest 8.4.2、runner版2、代替実行なしだった。リポジトリ外の受領記録は
`/private/tmp/reviewcompass-stage5-g25-full-receipt.json`、SHA-256は
`aed31a73d1e6b6e14e84914bdc4eb494615b164d40206e989bbf1579d3821510`、状態識別値は
`a5905f583df8e6fdb73d1e1f7d210c1023b5a051711373ea3a27205739ac100d`である。この状態はGREEN commit全体であり、
本Evidence追加前の状態である。

## 5. 安全境界

【実測】対象試験で次を確認した。

- Claude、Codex公開JSON、Codex rolloutの三形式が成功する。
- 元fileのbytesは実行前後で同一である。
- root外の通常pathと、root内から外を指すsymlinkを読取り前に拒否する。
- 未伏字eventを出力せず、`PreparedArtifact`の全項目変換を使わない。
- 解析上の注意から入力由来の`detail`を除外する。
- 高い乱雑性を持つ未登録値と、低い乱雑性の絶対pathが残れば成功成果を返さない。
- 種別不明を既知形式と推測せず、入力の詳しい内容を返さない。
- 実行名の登録正本が`pyproject.toml`に存在する。

【記録】G25の既存55試験と第4段の独立反証は、G25到達処理が入力fileの読取り以外のfile操作、network、
外部process、権限変更、環境値解決へ到達しないことを固定している。新入口はpath確認、G25呼出し、安全な項目選択、
最終出力検査、標準出力だけを追加し、保存・探索・送信をimportしない。

## 6. 配布物と利用者向け合成例

【実測】GREEN commitをリポジトリ外へ展開してwheelを作成した。wheel作成は終了コード0、SHA-256は
`afe73dc274174525d471cb26cf02f547f91dda92b3af9fadf74b75366916b6a8`だった。wheel内の`console_scripts`に
次が存在した。

```text
reviewcompass3-session-artifact = tools.session_logs.read_only_entry:main
```

【実測】同wheelをリポジトリ外の新しい仮想環境へ導入し、導入済み実行名からClaude形式の合成記録一件を処理した。
終了コード0、`status: ok`、`source_kind: claude`、`external_send_approved: false`であり、入力の
`user@example.com`は転写と要約の双方で`[REDACTED:email]`になった。来歴の`source_path`は相対pathの
`session.jsonl`であり、絶対pathと未伏字emailは出力に無かった。

## 7. 限界

【判断】本入口は、既定規則、高い乱雑性の検査、絶対pathの最終検査で確認できる範囲を守る。その他の
低い乱雑性の機微情報をすべて検出する保証はなく、結果を外部送信許可済みとして扱わない。この限界は
Task Contractと利用者承認から変更していない。

## 8. 次の確認と未実施

【判断】次は、新しい独立担当が、契約への適合、三path境界、失敗から成功への移行、配布後の入口、
安全出力、禁止副作用、受領記録と状態の結び付きを反証する。完了レビューが止める指摘0件となった後、利用者が
実際の出力例と限界を確認して最初の製品処理の完成を判断する。

【未実施】本Evidenceは独立完了レビュー、利用者の実装完了承認、第5段完了を代行しない。G25既存10 path、G26、
G30、他142 path、上流候補、Issue、TODOは変更していない。実Session記録、外部送信、network、push、tag、amend、
rebase、reset、履歴書換えは扱っていない。
