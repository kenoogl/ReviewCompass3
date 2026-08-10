# group C 現在地正本修正 範囲レビュー結果 v3

- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：scope（実装前の範囲レビュー）
- risk：`high`（Human確定済み）
- 判定：`verified`
- Finding：blocking 0件、non-blocking 0件、defer 0件
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`

## 1. 固定対象と開始状態

- 対象：
  `records/session-handoffs/2026-08-10-claude-pilot-current-position-fix-scope-v3.md`
- 対象SHA-256：`44f46ae89a98d234aedffc45ffa44b5d30fdc040eaa8d864b45b80d607baf683`
- 対象commit：`c1edf4f6b3c36af329147a1466491faef2b2e0f3`
- 対象commitの親：`f9432514c2fd0b9854c2a41a635020c4ca549a2c`
- 先行scope：v1 `183145038b94f166812948e61fc04b896e5fdbb1`、
  v2 `72b8389ac2cfb115a66c68e99ec67a3a953071c2`
- 先行範囲レビュー：v1 `994c07221e891e0ca3d2253a3c3bf1bcba188106`、
  v2 `f9432514c2fd0b9854c2a41a635020c4ca549a2c`
- branch：`main`
- 許可範囲：本判定record 1件の新規作成と単独commit、読取り、決定的な照合
- 禁止範囲：scope v1〜v3、code、test、既存record、config、schema、上流設計、TODO、
  checklistの変更、RED、GREEN、外部送信、push、履歴書換え
- 期待成果：指定4観点の判定、§11区分のFinding、先行Finding 3件の解消可否、
  model来歴を持つ本record 1件と、その単独commit
- 停止条件：固定対象不一致、許可範囲外の変更が必要な場合、blocking Finding

【実測】レビュー開始時のHEADは対象commit、worktreeとindexはcleanだった。対象commitの親は
範囲レビューv2のcommitと一致し、変更pathは対象scope v3の新規追加1件だけだった。
`git diff --check c1edf4f^ c1edf4f`は終了コード0だった。

【実測】対象scope v3、scope v1、先行範囲レビューv1・v2、上流group C判定、包括承認を
再読込みした。scope v1 §3の固定入力5件と対象実装2件のSHA-256を再計算し、7／7で記載値と
一致した。`git diff --quiet cbc8709 c1edf4f -- <対象実装2件・変更候補test 5件>`は終了コード0で、
scope v1のbase以後に対象codeとtestが変更されていないことを確認した。

【実測】本recordの予定pathに対する`git check-ignore --no-index`は終了コード1、作成前の
`test ! -e`は終了コード0だった。

## 2. SR-C-SCOPE-003と統合後のtest集合

【記録】本レビューで適用する統合順は、v1 §1〜§4・§8を維持し、v1 §5・§6・§7と
v2 §2・§3をv3で置き換える、という依頼およびv3 §1の宣言である。したがって、v2 §4にある
「v1 §6は不変」はv2作成時点の記述であり、後続v3の明示的な置換後に旧§6を再び有効にしない。

【実測】統合後の変更可能test集合は次の2 fileだけである。

- `tests/test_todo_handoff_git_state.py`
- `tests/test_todo_update_path.py`

【実測】単独の`awk`照合は、v3 §2の受入条件が「§3の2 file」、v3 §3の変更可能testが
上記2 file、v3 §4のREDが「§3のtest 2 fileのみ」であることを確認し、
`acceptance_two=1 allowed_test_count=2 handoff=1 update=1 red_two=1`、終了コード0だった。

【実測】高リスクの独立反証として、実ファイルを変えず、受入条件の数だけをメモリ上で
2から5へ変えた負の対照を同じ照合へ入力した。結果は
`mutated_acceptance=5 allowed_test_count=2 red=2 consistency=0`、終了コード1であり、
旧不整合と同型の入力を合格させなかった。

【判断】受入条件、変更可能path、RED定義は同じ2 fileを一意に指す。旧v1 §5〜§7は
置換対象であり、v2の残存記述も新しい置換規則を覆さない。SR-C-SCOPE-003は解消した。

## 3. SR-C-SCOPE-001・002の解消維持

【実測】v3 §2の危険側表を単独の`awk`照合で抽出した結果は
`counterexample_count=10 exact_H1_H6_U1_U4=1`、終了コード0だった。H1〜H6・U1〜U4が
各1回あり、H3の実branch不一致とH6のUnicode空白による非正規行を含む。

【記録】上流group C判定§4は、この10件をF-C1〜F-C5の反証として固定する。同じH6で試された
BOM、CRLF読取り、必須3行の順序入替えは上流Findingではない。

【判断】v3は上流Findingの10件をすべて拒否対象とし、H6の対照3変種へ拒否対象を広げない。
SR-C-SCOPE-001の「危険側反証の不足」は解消した状態を維持している。

【実測】v3 §3は変更可能testを直接対象の2 fileだけに限定する。外した3 file、先行レビューv1が
挙げた関連回帰4 file、直接呼出元1 moduleは回帰確認だけとし、変更が必要ならv1 §8-2に従って
Humanへ停止する。

【判断】別契約を検査するtestへ変更許可を広げず、上流Findingの対象2 moduleと直接testへ閉じている。
SR-C-SCOPE-002の「変更可能testの過大」は解消した状態を維持している。

## 4. scope境界、Human境界、受入条件

【記録】包括承認recordはgroup Cのrisk `high`、着手、RED開始、GREEN着手、レビュー依頼を
事前承認する。一方、変更可能path外、上流設計・config・schema、既存recordの再計算・移行、
RED後のtest変更、完了レビューblocking後の修正、意味的裁定をHuman停止として残す。

【判断】v1 §1〜§4はmode、risk、固定入力、F-C1〜F-C5の修正方向を維持し、v1 §8は固定入力不一致、
変更可能path外、実TODO正例の不成立、TODO書式・既存record、上流設計・config・schemaを
停止条件にする。v3 §3は回帰確認対象の変更をHuman停止へ戻し、v3 §4はRED後のtest変更に
Human承認を要求する。Human境界の欠落はない。

【判断】受入条件は、危険側10件の拒否、実TODOの正例、変更test 2 file、変更しない回帰test、
公式全Test、上流設計・config・schema・既存recordの不変を双方向に確認する。上流Findingを残したまま
合格できる条件、許可path外の変更を合格させる条件、新しいscope境界の破れは見つからない。

【判断】反証を使い捨ての一時領域だけで行い、実TODOと実Git索引に触れない境界も維持されている。
実装方式、command option、正規化関数、fixture構成には立ち入っていない。

## 5. 先行Finding 3件の解消可否

| Finding | §11区分 | 判定 | 根拠 |
| --- | --- | --- | --- |
| SR-C-SCOPE-001 | blocking／scope／§11.1類型1・3 | **解消** | 上流の危険側10件を過不足なく列挙し、H3・H6を含む |
| SR-C-SCOPE-002 | blocking／scope／§11.1類型4 | **解消** | 変更可能testを直接対象2 fileだけに限定し、他は変更しない回帰確認へ分ける |
| SR-C-SCOPE-003 | blocking／scope／§11.1類型4 | **解消** | 受入条件・変更可能path・RED定義が同じ2 fileを指し、負の対照も不一致として検出する |

## 6. Finding（`work-review-protocol.md` §11）

【判断】blocking 0件、non-blocking 0件、defer 0件。先行レビューで挙げなかった論点を
後出しせず、範囲レビューの高度を越える実装方式にも立ち入っていない。

## 7. 判定と次

判定：`verified`。

【判断】必須Evidenceが揃い、対象commitと事後状態が一致する。SR-C-SCOPE-001〜003はすべて解消し、
統合後の変更可能test集合は一意である。上流Finding、scope境界、Human境界、禁止範囲、受入条件、
一時領域規定に新たな欠落はないため、本scopeをRED開始の根拠にできる。

独立照合：commit・親・変更path、SHA-256、ignore状態、`git diff --check`、固定入力、
対象code・testの不変、3か所のtest集合、危険側10件、数だけを変えた負の対照を単独commandで
照合した。範囲レビューでありcode・testは実行していない。

Human境界：維持。既存の包括承認がrisk確定とRED開始を含む。v1 §8、v3 §3・§4、
包括承認record §2に触れる場合はHumanへ停止する。

未実施：scope v1〜v3、code、test、既存record、config、schema、上流設計、TODO、checklistの変更、
RED、GREEN、完了レビュー、Closer作業、外部操作、push、履歴書換え。

次：Pilotは既存の包括承認の範囲内で、本scope v3に従うREDへ進む。
