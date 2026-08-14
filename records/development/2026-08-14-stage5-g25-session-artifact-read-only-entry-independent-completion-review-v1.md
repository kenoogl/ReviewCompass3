# 第5段 G25 Session記録 読取り専用入口 独立完了レビュー v1

- レビュー日：2026-08-14
- 対象Task Contract：`TC-RC3-PRODUCT-G25-SESSION-ARTIFACT-PREPARATION-001` version 1
- 契約SHA-256：`20e4e0551c5b1357ba3e66d6ba849f19566da27c58c54ef98e8fa1db110fb72b`
- Human承認Decision SHA-256：`dde3ad7be1a31f1c7f77e253a90fe952496950e5b6a402fcdf473388d211ae39`
- 実装Evidence SHA-256：`d6b125a5b6a62f8a6eef0854c4394c3e87f5a400dc8b75c11814dcd1f03823af`
- 観測commit：`2f62c664ec15b66b1438b92d5f997a4e459735b0`
- 判定：`changes_required`

## 1. 判定

【判断】**完了候補としては未確認**である。三pathの実装、失敗から成功への移行、配布後の実行名、
禁止した外部作用へ到達しない正常処理、対象・関連・通常全試験の成功は確認できた。しかし、契約が明記する
絶対pathの停止境界に実反例が一件あり、入口の状態表示もHuman受入前の状態より進んでいる。止める指摘二件を
限定修正して再確認するまで、製品処理の完成およびHuman受入へ進めない。

本レビューは、第5段完了またはHuman受入を代行しない。

## 2. 固定対象と変更範囲

【実測】契約、Human承認Decision、実装EvidenceのSHA-256は上記申告値と全件一致し、指定されたcommit
`8e339d8`、`85e4b90`、`3e780c2`、`1866d38`、`2f62c66`はすべて実在した。

【実測】実装前`8e339d8`から観測`2f62c66`までの変更は次の四pathだけだった。実装Evidenceを除く意味変更は、
承認済みの三pathに閉じている。

- `tools/session_logs/read_only_entry.py`：追加
- `pyproject.toml`：実行名一件の追加
- `tests/test_session_log_read_only_entry.py`：追加
- `records/development/2026-08-14-stage5-g25-session-artifact-read-only-entry-implementation-evidence-v1.md`：追加

【実測】G25の既存10 pathは実装前と観測commitで差分0だった。群内pathについて
`mode type object-id<TAB>path<LF>`をpath順に連結して再計算したtree SHA-256は、両点とも契約値
`f476cbf6df63bc2accfb188764b2b8216aefdb7c446572b40b56b2cbcab861e4`と一致した。

## 3. 失敗から成功への移行

【実測】各commitをGit archiveでリポジトリ外へ展開し、現在の編集可能な作業ツリーを読み込まない隔離条件で
対象試験を再実行した。

| 状態 | 結果 | 終了コード |
| --- | --- | --- |
| RED `85e4b90` | 10件失敗。全件が新moduleまたは実行名の未実装理由 | 1 |
| RED訂正 `3e780c2` | 10件失敗。同じ未実装理由 | 1 |
| GREEN `1866d38` | 10件成功 | 0 |

【実測】REDからRED訂正への変更は、高乱雑性の試験入力を`token=`から`value=`へ替えた一行だけだった。
既定規則は`token=`を先に正しく伏字化するため、未登録の高乱雑性値を作る試験目的には`value=`が適切である。
訂正後も10件すべてが未実装理由で失敗したため、実装への期待合わせではない。

【実測】訂正RED、GREEN、観測commitにおける対象試験のGit物体識別値はすべて
`242e101c58f3d4c9b66932655b468ca7326e3b01`で一致した。GREENで試験を弱めていない。

## 4. 止める指摘

### ST5-G25-COMP-001：絶対pathの表記によっては成功結果へ漏れる

【実測】現在の入口は`work=/Users/example/project`を停止するが、次の二表記を絶対pathとして検出しなかった。

- `absolute path:/Users/example/project`
- `file:///Users/example/project`

前者をClaude形式の合成記録一件へ入れ、製品入口を実行した。結果は終了コード0、`status: ok`となり、
転写と要約の双方へ`/Users/example/project`がそのまま出た。後者も同じ結果だった。

【判断】契約§2、§7.3、§8.5、§8.6は、低い乱雑性を含む絶対pathが出力候補に残れば成功成果を返さず
停止すると定める。今回の反例は、検査の正規表現が直前の`:`を除外条件に含め、`file://`の連続slashも
拾わないため成立する。外部送信を許可しない表示だけでは、契約した出力境界の代わりにならない。

【判断】最小訂正は、既存の`_contains_absolute_path`だけを修正し、既存のparameter付き停止試験へ上記二表記を
追加することである。新しい検査器、台帳、別試験file、G25既存10 pathの変更は不要である。

### ST5-G25-COMP-002：Human受入前に正式・安定済みと表示している

【実測】新入口の先頭は次を宣言する。

- `lifecycle: stable`
- `normative_status: normative`
- `promotion_required: false`

一方、Human承認Decision §4は実装完了判断ではないと明記し、実装Evidenceの判定も
`implementation_complete_pending_independent_review_and_human_acceptance`である。契約§8.12も、利用者による
出力例の確認と製品処理としての受入を未完の受入条件としている。

【判断】実装開始の承認は得ているが、実装完了と製品受入は得ていない。したがって現時点の三表示は状態を
先取りしている。特に`promotion_required: false`は、残るHuman受入と本レビューの止める指摘に反する。

【判断】最小訂正は、新入口一fileの三表示を、完了レビューとHuman受入が済むまで
`provisional`、`non-normative`、`promotion_required: true`へ戻すことである。新しい状態機械や昇格機構は作らない。

## 5. 安全な項目、入力境界、禁止作用

【実測】絶対path反例を除く次の境界は、対象試験と独立実行で成立した。

- Claude、Codex公開JSON、Codex rolloutの三形式を別々に処理する。
- 正常結果は選択した項目だけを返し、`events`、raw bytes、規則patternを返さない。
- 解析上の注意は`kind`、行番号、block番号だけを返し、入力由来の`detail`を返さない。
- root外の通常pathと、root内から外を指すsymlinkを読取り前に固定語彙で拒否する。
- 高い乱雑性の未登録値を固定語彙`sensitive_data_remaining`の停止結果で閉じる。
- 種別不明と内部例外は入力本文、例外本文、絶対pathを停止結果へ入れない。
- 正常実行前後の合成raw file SHA-256は
  `77b183896004eda49e8be28d73141e8602dede8dc49b2ffb0134f73fb6697615`で不変だった。

【実測】正常処理に対し、`Path`の書込み系操作、`socket`、`subprocess`、`os.system`、環境規則解決、
home・host値の解決を、呼ばれたら失敗する監視へ置き換えた。それでも終了コード0で成功し、監視への到達は
0回だった。静的な呼出し確認でも、新入口からG25の`prepare_artifact`を経て到達する処理はraw fileの読取り、
メモリ上の解析・伏字化・要約・来歴生成、標準出力に閉じ、書込み、network、外部process、Git、環境値解決を
呼ぶ枝へは到達しない。

## 6. 配布物と導入後の入口

【実測】GREEN commitをリポジトリ外へ展開し、`pyproject.toml`を正本としてwheelを独立作成した。
wheel内の`console_scripts`には次が存在した。

```text
reviewcompass3-session-artifact = tools.session_logs.read_only_entry:main
```

【実測】同wheelを新しいリポジトリ外の仮想環境へ導入し、導入済み実行名からClaude形式の合成記録一件を
処理した。終了コード0、`status: ok`、`source_kind: claude`、`external_send_approved: false`であり、
入力emailは転写と要約の双方で`[REDACTED:email]`となった。来歴のsource pathは`session.jsonl`で、実行前後の
raw SHA-256は不変だった。

## 7. 試験と状態の結び付き

【実測】観測commitの現在状態で独立再実行した。

| 確認 | 結果 | 終了コード |
| --- | --- | --- |
| 新入口10件＋G25直接関連55件 | 65件成功 | 0 |
| 正規全試験 | 1,738件成功、失敗0、error 0、skip 0 | 0 |

【実測】正規全試験はPython 3.13.14、pytest 8.4.2、runner版2、代替実行なしだった。独立受領記録は
リポジトリ外の`/private/tmp/reviewcompass-stage5-g25-independent-full-receipt.json`、SHA-256は
`5a0034677ae8f2d2953250c3abbea492e7421c597263f3b142ef033a5b0f6991`である。受領記録の状態識別値
`ad508ebcb03eed0ac45fc650eb1258ba9ba54b6e316154b9cd4faf16fe8f8c89`を現在状態から同じ規則で再計算し、
一致した。

【実測】実装Evidenceが固定する元の受領記録もリポジトリ外に現存し、申告SHA-256
`aed31a73d1e6b6e14e84914bdc4eb494615b164d40206e989bbf1579d3821510`、1,738件成功、終了コード0を再読込した。
ただし、全試験成功は既存試験にない絶対path表記の反例を否定しない。

## 8. 報告不一致

【実測】一件ある。実装Evidence §5の「低い乱雑性の絶対pathが残れば成功成果を返さない」という一般化は、
§4の反例と実状態が一致しない。この安全境界に依存する実装完了候補表示を`report_execution_mismatch`として
staleにし、限定修正後の再確認まで完成根拠に使わない。

【判断】状態表示の先取りは、実装Evidence自身のpending表示と新入口の三表示の不一致であり、
`ST5-G25-COMP-002`として同じく完了判断を止める。

## 9. 試した反証

1. **変更範囲外の混入**：実装前から観測commitまでの全path差分とG25 10 pathのtree SHAを照合した。
   実装三pathとEvidence以外の意味変更はなく、反証不成立。
2. **REDが製品欠陥または環境差で失敗しただけ**：履歴状態を隔離して再実行した。二つのREDは10件すべて
   未実装理由、GREENは同一試験物体で10件成功し、反証不成立。
3. **安全でない内部項目が出力される**：三形式、解析上の注意、root外、symlink、高乱雑性値、種別不明を
   実行した。`events`、`detail`、raw断片、例外本文は出ず、反証不成立。
4. **絶対pathなら表記によらず停止する**：`:`直後と`file://`を投入した。終了コード0で転写・要約へ残り、
   **反証成立**。中心判断を崩した。
5. **読取り専用入口から禁止作用へ到達する**：禁止作用を失敗監視へ替えた正常実行と静的呼出し確認を行った。
   到達0回で、反証不成立。
6. **配布後に実行名が無い、または作業ツリーを偶然読んだだけ**：GREEN commitからwheelを作り、別仮想環境へ
   導入し、リポジトリ外から実行した。合成例が成功し、反証不成立。
7. **完了前表示が慎重側である**：契約§8.12、Human承認Decision §4、実装Evidenceのpending判定と比較した。
   `stable / normative / promotion_required: false`だったため、**反証成立**。
8. **上流暫定候補が正式要求へ昇格した**：実装差分と契約の権威・候補分離を照合した。上流候補、G26、G30、
   他142 pathに変更はなく、契約の低乱雑性機微情報と外部送信非承認の限界も残っており、反証不成立。

## 10. 必要な限定修正

1. `tools/session_logs/read_only_entry.py`の既存絶対path検査を、`:`直後と`file://`に含まれる絶対pathも
   停止するよう訂正する。
2. `tests/test_session_log_read_only_entry.py`の既存parameter付き停止試験へ、この二例を加える。別試験fileは
   作らない。
3. 同じ入口file先頭の三表示を、Human受入まで
   `provisional / non-normative / promotion_required: true`へ訂正する。
4. 対象試験と、この二指摘だけの限定再レビューを行う。G25既存10 path、契約、上流候補、設定、TODOは
   変更しない。

## 11. 未実施

【未実施】成果物コード、試験、設定、`pyproject.toml`、Task Contract、TODO、実装Evidence、G25既存10 path、
G26、G30、他142 path、上流候補、Issueは変更していない。新しい検査器、台帳、関門、別試験fileは作成して
いない。実Session記録、外部送信、network、push、tag、amend、rebase、reset、履歴書換え、第5段完了、
Human受入は扱っていない。レビュー用の展開、合成入力、wheel、仮想環境、受領記録はすべてリポジトリ外に
置いた。
