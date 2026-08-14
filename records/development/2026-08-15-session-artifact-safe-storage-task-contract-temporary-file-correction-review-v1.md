# Session記録の安全保存 Task Contract候補 v3 一時file一点確認

- 記録ID：`REV-TC-RC3-PRODUCT-SESSION-ARTIFACT-SAFE-STORAGE-002-TEMPORARY-FILE-2026-08-15-V1`
- 実施日：2026-08-15
- 確認種別：v2で残った一時file指摘だけの一回限り確認
- v2：`records/task-contract/2026-08-15-session-artifact-safe-storage-candidate-v2.md`
- v2 SHA-256：`c42c36a1ec389409892cf990116055bee301a29008c44f4e9fed9d03d4811163`
- v2変更点レビュー：`records/development/2026-08-15-session-artifact-safe-storage-task-contract-definition-correction-review-v1.md`
- v2変更点レビューSHA-256：`6408d28e92fed3ebb62a2d8ea716d2b4af5d273a362b6d6437c15bd290f8cbb7`
- v3：`records/task-contract/2026-08-15-session-artifact-safe-storage-candidate-v3.md`
- v3 SHA-256：`38de71b1d8910f7cf05ae76a8f881235400d7522f81314f844d8cf1e0e52cfac`
- v3 commit：`45bf33c4214fa6d2109ab4c080e387d6b4f19903`
- 判定：`verified`

## 1. 判定

【判断】**開始可**である。v2で残った一時fileの止める指摘は解消した。

【判断】止める指摘は0件、報告不一致は0件である。本判定は、契約候補v3を利用者の採否判断材料にできるという意味であり、
契約採用、案Cの最終採用、実装開始または製品受入を代行しない。

## 2. 固定対象と変更範囲

【実測】v2、v2変更点レビュー、v3のSHA-256は全件申告値と一致した。v3 commitは実在し、追加したのはv3一件だけである。

【実測】v2からv3の意味変更は次に限定されている。

1. 一時fileの決定的一覧、操作情報、状態判定、書込み順、再試行、削除への接続。
2. 権限対象の語句を「各root」から「各保存root」へ限定する訂正。
3. 版、訂正根拠、後続レビューと利用者判断の表示更新。

【実測】製品コード、試験、設定、`pyproject.toml`、既存契約、TODOは変更されていない。
`source_path`除外、二root状態、削除確認値、値受渡し、案C、G26・上流候補の各節は、一時file接続に必要な追記以外に
意味変更がない。既に解消済みの内容は再審査していない。

## 3. 一時file指摘の解消確認

### 3.1 名前と許可一覧

【実測】v3 §7は、次の一時fileを全て列挙した。

- 機微情報用領域：`operation.json.tmp`、`raw.bin.tmp`。
- 通常データ領域：`operation.json.tmp`、`derived.json.tmp`、`manifest.json.tmp`、`commit.json.tmp`、`deleted.json.tmp`。

【実測】一時名は、対応する最終名へ`.tmp`を一つだけ付けて決定的に導出する。乱数名、時刻名、任意の接尾辞は
使わないと明記されている。root全体の走査をせず、記録IDとこの許可一覧だけで対象を決められる。

【判断】一時fileの対象集合は閉じた。

### 3.2 操作情報と自己参照

【実測】両rootの`operation.json`は、記録ID、操作識別値、schema版、状態、保持期限、全ての最終fileと一時fileの名前、
対応する最終名、期待する内容識別値を持つ。

【実測】`operation.json.tmp`は、自身のSHA-256を`operation.json`へ埋め込まない。同じ記録ID、操作識別値、schema版、
変更前後の状態を持つ完全な正準JSONであることにより検証する。この例外は、自身の内容識別値を自身へ書く循環を避け、
他の本文fileの内容照合を弱めない。

【判断】操作情報の検証定義に自己参照の循環はない。

### 3.3 機微な一時fileを書き始める順序

【実測】保存は、両rootへ同じ有効な`incomplete`の`operation.json`を置き、両方を再読込みした後にだけ、
`raw.bin.tmp`、`derived.json.tmp`、`manifest.json.tmp`を書き始める。

【判断】通常の契約経路では、機微な本文を含む一時fileが、有効な操作情報なしに生成されない。

### 3.4 状態、保持期限、再試行、削除

【実測】最終fileまたは一時fileが一つ以上あり、`deleting`、`deleted`、`committed`を満たさない記録は`incomplete`となる。
一時fileは対応する最終fileと同じ保持期限を持つ。

【実測】`store`再試行は、有効な`operation.json`と、記録済みの一時名、対応先、操作識別値、期待する内容識別値が
一致する場合だけ進む。`plan-delete`は一時fileの種類、対応、件数を削除確認値へ結び、`delete`は記録済みの一時fileを
本文fileより先に削除する。削除確認値と操作情報は本文の削除完了まで残る。

【判断】一時fileは状態判定、保持期限、保存再試行、削除計画、確認済み削除へ全て接続された。

## 4. 中心反証

### 4.1 `raw.bin.tmp`の書込み中に停止する

【実測】停止前に両rootの有効な`operation.json`が存在し、`raw.bin.tmp`の決定名、対応する`raw.bin`、期待する
内容識別値、保持期限が記録されている。

【判断】一時fileが期待値と一致すれば、同じ入力の`store`で再開できる。部分書込みなどで期待値と一致しなければ、
成功へ推測せず停止するが、同じ記録IDの`plan-delete`が実在する一時fileを計画へ含め、利用者が確認した`delete`で
当該一記録だけを削除できる。root走査、任意名の探索、推測削除は不要である。反証は不成立。

### 4.2 `operation.json.tmp`だけがあり、有効な`operation.json`がない

【実測】v3は、有効な`operation.json`がなく一時fileだけが存在する場合、その内容を推測して再開または削除せず停止する。
また、機微な本文一時fileを書き始めるのは、両rootの有効な最終`operation.json`を再読込みした後である。

【判断】この状態では通常の契約順序上、元記録本文を含む`raw.bin.tmp`はまだ生成されない。操作情報の一時fileだけを
権威として推測処理しないため、安全側に閉じる。反証は不成立。

### 4.3 確定状態と削除状態に一時fileが混入する

【実測】`committed`は、有効な`commit.json`、両rootの操作情報と全内容識別値の一致に加え、一時fileが0件であることを
要求する。したがって、一時fileを残したまま確定済みと表示できない。

【実測】`deleted`は、本文file、本文一時file、`commit.json`、`commit.json.tmp`がなく、有効な`deleted.json`がある
場合だけ成立する。`deleting`は、有効な`operation.json`または`operation.json.tmp`のどちらか一つでも
`deleting`なら最優先となる。記録済みの一時fileは、確認値を持つ操作情報を残したまま削除される。

【判断】削除途中に一時fileが残っても通常読込みへ戻らず、同じ確認値で削除再試行できる。反証は不成立。

## 5. 権限語句と既確認境界

【実測】v2 §5の「各root」は、v3で「各保存rootと記録directory」へ訂正された。mode 0700相当を要求する対象は
`sensitive_root`と`data_root`であり、境界確認用の`repository_root`へ要求しない。現在のrepositoryが0755であることを
理由に誤拒否する読みは解消した。

【実測】次の既確認境界はv2から維持されている。

- 保存用派生物、manifest、再出力、削除後監査からの`provenance.source_path`除外。
- 二root不一致時の安全側状態、削除確認値を失わない順序、`prepare_safe_result`による値受渡し。
- 案Cの変更範囲、G26全体を正式化しない境界、上流候補を暫定のまま保つ境界。
- 契約採用と実装開始を、v3作成承認とは別に利用者が判断する境界。

【判断】これらは変更がないことだけを確認し、全体再審査は行っていない。

## 6. 報告不一致と止める指摘

【判断】報告不一致は0件である。固定SHA-256、v3 commitの変更path、未変更対象は申告どおりだった。

【判断】止める指摘は0件である。v2で残った一時fileの指摘は、v3の決定的一覧、操作情報、先行書込み順、状態判定、
保持期限、再試行、削除計画、確認済み削除への接続で解消した。

## 7. 利用者が判断する点

1. 本レビューを材料に、契約候補v3を第2のTask Contractとして採用するか。
2. 契約採用とは別に、案Cの実装開始を承認するか。

【判断】本レビューは、いずれの利用者判断も代行しない。

## 8. 未実施

【未実施】契約、製品コード、試験、設定、`pyproject.toml`、既存契約、TODO、G26、上流候補は変更していない。
契約採用、実装開始、製品実装、対象試験、全試験、新機構、台帳、検査器、追加試験、実Session記録の使用、
保存root作成、外部送信、network、外部process、push、tag、履歴書換えは行っていない。
本確認はv2で残った一時file一点、v2からの変更範囲、指定された反証だけを読み取りで確認した。
