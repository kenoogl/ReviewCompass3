# group C 現在地正本修正 範囲レビュー結果 v2

- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：scope（実装前の範囲レビュー）
- risk：`high`（Human確定済み）
- 判定：`reported_unverified`（要修正・RED開始不可）
- Finding：blocking 1件、non-blocking 0件、defer 0件
- model来歴：`~/.codex/config.toml`の実効値 `model = "gpt-5.6-sol"`、
  `model_reasoning_effort = "high"`

## 1. 固定対象と開始状態

- 対象：
  `records/session-handoffs/2026-08-10-claude-pilot-current-position-fix-scope-v2.md`
- 対象SHA-256：`5198895fc681ee124e4519240d1b2a998fac2a791d1b6ed2a5541695b164d729`
- 対象commit：`72b8389ac2cfb115a66c68e99ec67a3a953071c2`
- 対象commitの親：`994c07221e891e0ca3d2253a3c3bf1bcba188106`
- 先行scope：`183145038b94f166812948e61fc04b896e5fdbb1`
- 先行範囲レビュー：`994c07221e891e0ca3d2253a3c3bf1bcba188106`
- branch：`main`
- 許可範囲：本判定record 1件の新規作成と単独commit、読取り、決定的な照合
- 禁止範囲：scope v1・v2、code、test、既存record、config、schema、上流設計、TODO、
  checklistの変更、RED、GREEN、外部送信、push、履歴書換え
- 期待成果：指定5観点の判定、§11区分のFinding、先行blocking 2件の解消可否、
  model来歴を持つ本record 1件と、その単独commit
- 停止条件：固定対象不一致、許可範囲外の変更が必要な場合、blocking Finding

【実測】対象commitの変更pathは対象scope v2の新規追加1件だけで、親は先行範囲レビューcommitと
一致した。レビュー開始時のworktreeとindexはcleanで、対象commitの`git diff --check`は
終了コード0だった。

【実測】対象scope v2、scope v1、先行範囲レビューv1のSHA-256を内容から再計算した。scope v1
§3の固定入力5件と対象実装2件も再計算し、7／7で記載値と一致した。対象実装、code、test、
上流recordは変更していない。

【実測】本recordの予定pathに対する`git check-ignore --no-index`は終了コード1、作成前の
`test ! -e`は終了コード0だった。

## 2. 先行Finding 2件の解消可否

| Finding | 判定 | Evidence |
| --- | --- | --- |
| SR-C-SCOPE-001 | **解消** | v2 §2はH1〜H6・U1〜U4の10件を危険側へ列挙し、H3を実Gitの現在branchとの不一致、H6をUnicode空白による非正規行として受入条件に含める。BOM・CRLF読取り・必須3行の順序入替えは上流Findingでないため拒否対象に広げないと明記する |
| SR-C-SCOPE-002 | **解消** | v2 §3は変更可能testを`tests/test_todo_handoff_git_state.py`と`tests/test_todo_update_path.py`の2 fileに絞る。外した3 file、先行レビューが挙げた関連回帰4 file、直接呼出元1 moduleは「回帰確認のみ・変更しない」とし、変更が必要ならv1 §8-2でHumanへ停止する |

【記録】上流group C判定§4のH3は一時Git repositoryの実branchと異なるbranch記載、H6の
blocking根拠は全角空白で必須文を箇条書き外へ出す行構造逃れである。同じH6で試したBOM、
CRLF読取り、必須3行の順序入替えは合格した対照結果であり、上流Findingには含まれない。

【判断】v2 §2は上流の危険側10件と一致し、SR-C-SCOPE-001が要求した変種だけを補っている。
上流Findingに無い3変種への拡張はない。

【判断】v2 §3の変更許可と回帰確認の区別は明確である。変更可能pathの過大という
SR-C-SCOPE-002の原因は解消している。

## 3. v1とv2の統合照合

【判断】v2が不変とするv1 §1〜§4、§6、§8は、mode、risk `high`、固定入力、F-C1〜F-C5、
commit境界、使い捨て一時領域、変更可能path外でのHuman停止を維持する。v2 §2・§3との間に、
新しい上流設計・schema・外部操作・不可逆操作の追加やHuman境界の欠落はない。

【記録】包括承認recordはgroup Cのrisk確定、着手、RED開始、GREEN着手、レビュー依頼を
事前承認し、変更可能path外、上流設計・config・schema、既存recordの再計算・移行、
RED後のtest変更、完了レビューblocking後の修正、意味的裁定をHuman停止として残す。
範囲レビューが要修正の場合のscope改訂と再レビューも、Human停止に触れない限り承認済みである。

【判断】受入条件の危険側、変更可能test、回帰確認だけを見る限り、誤った合格を許す新しい欠陥は
見つからない。しかし、差し替え対象外として残した受入条件3と差し替え後の§7は、test file数と
参照先が一致しない。

## 4. Finding（`work-review-protocol.md` §11）

### SR-C-SCOPE-003 blocking／scope／§11.1類型4

【実測】v2冒頭は「§5受入条件1と§7変更可能pathのみを差し替える」とし、v2 §2末尾は
「v1 §5の2〜4は不変」とする。したがってv1 §5.3の
「対象既存test（§7の5 file）が更新・追加後の全件で合格」が残る。一方、差し替え後のv2 §3は
§7の変更可能testを2 fileとし、残る3 fileを「回帰確認のみ（変更しない）」とする。

【判断】統合後の文書では、受入条件3が参照する「§7の5 file」と、実際の§7の2 fileを同じ集合として
読めない。さらにv1 §6はREDの変更fileを「§7のtest fileのみ」とするため、REDで変更可能なtestを
2 fileと読む箇所と5 fileと読む箇所が併存する。v2 §3の明示的な変更禁止により外した3 fileを
実際に変更してよいとは読めないものの、範囲固定文書が変更可能test集合を一意に示せていない。
scope境界の不整合である§11.1類型4のblockingとする。

【判断】この不整合はv1では§5.3と§7がともに5 fileで一致しており、v2で§7だけを2 fileへ
差し替えた結果として初めて生じた。先行レビューで存在していた論点の後出しではなく、指定観点3の
「引き継いだ節と差し替え節を一体として読む」照合で検出したv2起因のFindingである。

### non-blocking／defer

【判断】0件。先行レビューで挙げなかった既存論点を追加せず、command option、正規化方法、
fixture構成などの実装方式には立ち入っていない。

## 5. 判定と次

判定：`reported_unverified`（要修正・RED開始不可）。

【判断】SR-C-SCOPE-001とSR-C-SCOPE-002はそれぞれ解消した。risk、上流Finding、Human境界、
禁止範囲、一時領域の規定にも新しい欠落はない。しかしSR-C-SCOPE-003により、v1とv2を統合した
変更可能test集合が一意でなく、範囲固定全体を`verified`にできない。報告と事後状態の競合はないため
`report_execution_mismatch`ではなく、正しい停止地点への到達を確認する段階でもないため
`blocked`ではない。

独立照合：文書reviewのためcode・testは実行していない。commit列、name-status、SHA-256、
ignore状態、`git diff --check`、固定入力Digest、上流H3・H6、統合後の節参照を独立に照合した。

Human境界：維持。包括承認により、PilotはHumanへ追加確認せずscope改訂版を新規commitして
再レビューを依頼できる。v1 §8または包括承認record §2へ触れる場合だけHumanへ戻る。

未実施：scope v1・v2、code、test、既存record、config、schema、上流設計、TODO、checklistの変更、
RED、GREEN、完了レビュー、Closer作業、外部操作、push、履歴書換え。

次：Pilotは、変更可能testを2 file、外した3 fileを回帰確認のみとする境界を変えず、v1 §5.3の
「§7の5 file」という残存参照だけを統合後の§7と一致させたscope改訂版を固定し、Codexへ
範囲再レビューを依頼する。
