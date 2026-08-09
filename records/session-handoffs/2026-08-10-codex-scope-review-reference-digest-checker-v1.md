# 参照Digest恒久検査器 範囲レビュー結果 v1

- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：scope（範囲レビュー）
- risk：`high`（提案は妥当。Human確定前）
- 判定：`reported_unverified`
- execution state：`correctly_stopped_before_RED`
- Finding：blocking 1件、non-blocking 2件

【実測】起動時に表示されたmodel名とreasoning effortは
`gpt-5.6-sol`／`high`だった。

## 1. 固定対象

- scope：`records/session-handoffs/2026-08-10-claude-pilot-reference-digest-checker-scope-v1.md`
- scope SHA-256：`00b02847dde7b602c87265863b52079f84f83abe36842aef4000c27eb06fce96`
- SCOPE commit：`8d2efd7cc772beec97fcc48150a4ab017a2905ef`
- base：`6eba2c4b3030aee4f4573e768f0f8ee0e067eca8`
- branch：`main`
- 許可範囲：本判定recordの作成と単独commit
- 禁止範囲：実装、Test、既存record、TODO、checklist、Decisionその他の変更、外部操作、RED開始

【実測】SCOPE commitの親は申告baseと一致し、変更pathはscope 1件だけだった。レビュー開始時の
worktreeとindexはcleanだった。scopeと本record予定pathの`git check-ignore --no-index`はそれぞれ
終了コード1で、管理対象外ではなかった。

【実測】scopeに固定された7 fileのSHA-256は7／7一致した。scope自身のSHA-256も依頼値と一致した。
`python3 -m tools.development.todo_handoff TODO_NEXT_SESSION.md`は終了コード0、finding 0で合格した。
`git diff --check 6eba2c4 8d2efd7`も終了コード0だった。

## 2. 上流authorityから独立導出した境界

Pilotの実装案とTest案をoracle（正しさを判断する基準）にせず、次を先に照合した。

- `.reviewcompass/workflow/improvement-candidates/ic-authority-reference-digest-check-001--v1.json`
  （SHA-256 `d4e801aa35e4bd1ad2c17917d0cfd57b60e7e1aec93e7d1259bf8321285824c6`）
- `.reviewcompass/workflow/triage-decisions-v4/dec-ic-authority-reference-digest-check-001--v1.json`
  （SHA-256 `919f9c8803301297ed8a20e52333029020b17a4f8c7e24329fab1cf90f4a46bb`）
- `.reviewcompass/workflow/issues-v4/issue-authority-reference-digest-check-001--v1.json`
  （SHA-256 `d260ed570598f56ada2cd6b4e54f15543bba0e792db65c14403a038f8100afbe`）
- `records/development/2026-08-07-fixed-source-kind-decision-v1.md`
  （`DEC-FIXED-SOURCE-KIND-001`、SHA-256
  `07f891b5885fd13bfd9c736fccc29013034f665f9d2bbd85fa073b73b5614929`）
- `records/development/2026-08-09-deferred-items-triage-decision-v1.md`
  （SHA-256 `0171453f6025451d955b1dc08083ed06d2ccc28e8f110a3bb951ff97c48e3c91`）

【記録】正式な改善候補とHuman仕分け判断が承認待ち境界として固定したのは、Markdownの
front matter（文書冒頭の機械可読欄）にある「現在有効な上位文書」を示すkeyの許可一覧を先に
Human承認し、その対象だけを現行bytesと照合することである。Markdown本文中の参照、JSON record、
生成時点へ固定した参照、不変Evidence、Task Contractの固定入力は、古いDigestが正しい場合があるため
明示的に対象外である。`DEC-FIXED-SOURCE-KIND-001`も、`immutable_record`は一致を要求する一方、
`pinned_at_start`は後続改定による不一致を正常として扱う区別をHuman決定として固定している。

【記録】commit `ed79e5b…`の後続裁定はdeferred #5「参照Digest恒久検査器」の着手を承認したが、
上記の対象・非対象またはHumanによる判別規則の承認境界を置き換える文言はない。

したがって上流から導出される最小受入境界は、次のとおりである。

1. 現在有効な参照と時点固定参照を、Human承認済みの機械可読規則で区別する。
2. 対象にした現在有効な参照では、pathの安全性、実在、現行bytesのDigest一致をfail-closedで検査する。
3. 時点固定参照を現行bytesとの不一致だけで失敗にしない。
4. 不一致を自動修正せず、Human判断と停止境界を保つ。

## 3. Finding

### SR-P1-001：承認済み対象を本文参照表へ置き換え、正しい時点固定参照を失敗にできる

- 分類：`blocking`
- 確認段階：`scope`
- blocking根拠：§11.1類型1（上流authorityとの矛盾）、類型3（誤った不合格を生む受入条件の欠陥）、
  類型4（scope境界の破り）

【実測】scope §6は、任意のMarkdown record本文から表形式またはlist形式のpath＋64桁hexを抽出し、
すべてを参照先の現行bytesと照合する。一方、正式候補の`non_scope`はMarkdown本文中の参照と
過去へ固定した参照を明示的に除外している。scopeの固定入力には、正式候補、正式Human仕分け判断、
正式Issue、`DEC-FIXED-SOURCE-KIND-001`のいずれも含まれていない。

【実測】scopeが宣言した表形式に相当する行を`records/**/*.md`から機械抽出し、現在bytesと照合する
反証では、209件の不一致を検出した。この数を209件の不具合とは扱わない。上流authorityが説明する
とおり、多くは作業時点を正しく固定した参照だからである。代表例として
`records/development/2026-08-03-work-1-fixed-input-evidence-v3.md` 34行の現行Plan候補は、
作業時点Digest `0ae6bef9…156f`を保持し、現在bytesは`1a735976…d0962f`である。scope §7の負例と
exit規則をそのまま適用すると、この正しい時点固定参照を`mismatched`、exit 5にする。

【判断】これは区切り文字、正規表現、JSON fieldなどの実装詳細ではない。何を現行一致の対象にするかという
製品範囲と合否の意味そのものである。Humanが本文参照表向けの別検査器へ対象変更を承認した記録、または
正式Issueの対象を置き換えたDecisionがないため、現scopeをdeferred #5の実装範囲として合格にできない。

必要な修復は、Humanが次のどちらを#5として扱うか裁定し、その結果をscope v2へ固定することである。

- 正式Issueどおり、Human承認済みkey／参照種別に限定したfront matter検査器にする。
- 本文参照表の検査器を別の作業範囲として明示承認し、現在有効な参照と時点固定参照の入力契約、
  対象record、非対象を固定する。

## 4. risk、既存tool、Human境界

### risk

【判断】`high`提案は妥当である。Digest一致を他のrecordの合否に使い、誤りが改竄・欠落・古い参照の
見逃し、または正しい時点固定参照の誤拒否として現れる守り役のcodeであり、
`work-review-protocol.md` §3の既定`high`に該当する。

### `todo_handoff`との役割

【実測】`tools/development/todo_handoff.py`はroot TODOのcommit安定Git欄を検査し、
`tools/development/todo_update_path.py::default_verify`を通じてTODOの圧縮条件、active Issue、
`## 最新のauthority／Evidence`節だけのlink型参照Digestを検査する。自由なMarkdown recordの
表形式参照や全本文を検査せず、対象fileもroot TODOに限定される。

【判断】scope案の「任意のMarkdown recordにある表／list形式の参照対を読み取り検査する」という責務は、
現行`todo_handoff`のTODO構造・限定節検査とは重複しない。`todo_handoff.py`を変更しない境界も妥当である。
ただし、この非重複はSR-P1-001の上流scope変更を承認する根拠にはならない。

### Human境界と停止条件

【実測】PilotはSCOPE commit後、RED、実装、Test、Evidenceを作らず停止している。scopeはrisk確定と
再開承認をHumanへ残し、変更可能path外が必要な場合、固定入力不一致、Test不合格を停止条件にしている。

【判断】RED前停止とrisk確定のHuman境界は維持されている。一方、現在有効な参照と時点固定参照の
意味的裁定、または本文参照表への対象変更のHuman承認が停止条件に無いため、Human境界の固定は不十分である。
SR-P1-001を解消したscope v2と再範囲レビューの合格後も、HumanがriskとRED再開を明示承認するまで
実装しない境界を維持する必要がある。

## 5. 実装時確認事項

次は§11.2の高度規則により、scopeを止める理由にせず完了レビューで確認する。

1. pathの字句検査だけでなく、symlinkを含む解決後pathがrepository外へ出ないこと。
2. 不正な参照表記、抽出0件、file単位集計をJSON上で区別し、各受入例の件数と終了コードが一致すること。

いずれも`non-blocking`、確認段階は`implementation／completion`である。

## 6. commit `6eba2c4`の整合確認

確認対象は`records/development/2026-08-09-role-neutral-mode-trial-metrics-v1.md`への§4追記だけである。
commit `6eba2c4…`の変更pathは同record 1件、追加33行、削除0行で、`git diff --check`は終了コード0だった。

### 整合した記載

【実測】deferred #7のcommit列は
`ed79e5b` → `91be5a9` → `7762c10` → `1711466` → `881a2f2` → `86a1cd0`
の直列である。仕分けとrisk確定のHuman文言2件、SCOPE、実装、review request、Reviewerの
`verified`／Finding 0、CloserのTODO projectionが各recordとGit履歴で解決した。対象129件、公式全1338件、
fixture同一性9／9もreview request、Evidence、review resultと一致した。

【実測】CLI橋渡しについては、読み取り確認1件と書込みを伴う4件に対応する記録があり、書込み4件は
`99e6285`、`2c710c0`、`881a2f2`、`86a1cd0`として各1 pathだけを変更している。3件のreview resultは
`verified`、CloserのTODOは統合validator合格状態である。したがって、5起動の種別と結果の方向は
Git履歴・session handoff recordと整合する。

### 不一致と未検証

【実測】§4.1の「経過：同日内」はGit履歴と競合する。SCOPEからReviewer判定までは
2026-08-09だが、Closer projection `86a1cd0`は2026-08-10T06:27:47+09:00である。
同record §1が定義する「scope固定〜完了projectionまで」の意味では2暦日にまたがる。

【実測】§4.1の比較文「停止系判定3→0」は、同record §1の元計測
「範囲2回＋完了2回」と一致しない。scope v2の停止判定は後に再評価されたため、有効な停止を3件と
数え直す解釈は可能だが、§1は発生回数として4件を数えている。比較値の計数規則が記録されていない。

【判断】上記2件により、commit `6eba2c4`の§4計測追記は全体として
`report_execution_mismatch`である。競合EvidenceはGit timestampと同record §1の計数であり、
§11.1の停止系判定規則に従い類型1〜4への該当を要しない。本scopeの実装承認根拠や方式の比較値としては
staleにし、訂正recordが固定されるまで使用しない。

【記録】tokenの正確な3値と2件欠測は、repository内では§4追記以外に数値receiptがない。
結果commitとの矛盾はないが、独立再計算できないため、この数値部分だけは`reported_unverified`である。

## 7. 判定

判定：`reported_unverified`

変更範囲：SCOPE commit自体は一致し、scope record 1件だけである。

独立確認：固定入力7／7、scope Digest、Git親子関係、TODO統合validator、diff check、既存tool責務、
本文参照の反証209件を機械照合した。実装前の範囲レビューなので製品Testと公式全Testは実行していない。

Record照合：上流Candidate、Human triage Decision、Issue、参照種別Decision、deferred裁定と照合した。

Human境界：RED前停止とrisk確定境界は維持。対象参照種別の意味的裁定が未固定である。

未実施：RED、実装、Test、Evidence、TODO、checklist、既存recordの修正、外部操作、次段作業。

次：HumanがSR-P1-001の二案から#5の対象を一つ裁定し、Pilotがscope v2を新規commitして停止した後、
Reviewerが再範囲レビューする。
