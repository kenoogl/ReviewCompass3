# 参照Digest恒久検査器 再範囲レビュー結果 v2

- Reviewer model：`gpt-5.6-sol`
- reasoning effort：`high`
- レビュー日：2026-08-10
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- レビュー段階：scope（範囲レビュー）
- risk：`high`（Reviewer判断。Human確定前）
- 判定：`verified`
- execution state：`correctly_stopped_before_RED`
- Finding：blocking 0件、non-blocking 2件

【実測】起動時に表示されたmodel名とreasoning effortは
`gpt-5.6-sol`／`high`だった。

## 1. 固定対象と開始状態

- scope：`records/session-handoffs/2026-08-10-claude-pilot-reference-digest-checker-scope-v2.md`
- scope SHA-256：`c37b7742a05592f514fac85f5bed606c8e396410a9df7deeac22a7afe46f9172`
- SCOPE commit：`34f44da171e5edf40bef0b7f411870448dfc7fe2`
- base：`c7579fffcb3bf407df80084c7190b68098dc202e`
- branch：`main`
- 先行レビュー：
  `records/session-handoffs/2026-08-10-codex-scope-review-reference-digest-checker-v1.md`
  （SHA-256 `397a367f66d4809620dc967d24cd4ec4438560ee431a6b8f4ee8921a8e07e721`）
- 許可範囲：本判定recordの作成と単独commit
- 禁止範囲：実装、Test、既存record、TODO、checklist、Decisionその他の変更、外部操作、RED開始

【実測】SCOPE commitの親は申告baseと一致し、変更pathはscope 1件だけだった。レビュー開始時の
worktreeとindexはcleanだった。本record予定pathの`git check-ignore --no-index`は終了コード1で、
管理対象外ではなかった。`git diff --check c7579ff 34f44da`は終了コード0だった。

【実測】scopeに固定された13 fileのSHA-256は13／13一致した。scope自身と先行scope v1の
SHA-256も申告値に一致した。実装、Test、許可一覧宣言、GREEN Evidence、receipt、review requestの
予定6 fileはいずれも存在せず、RED以降が未着手であることを確認した。

## 2. SR-P1-001の解消

【記録】Humanは2026-08-10に先行Findingの選択肢を「(a)で確定」と裁定した。すなわち、正式Issueの
対象どおり、Human承認済みのkey許可一覧に限定したfront matter（文書冒頭の機械可読欄）の検査器として
deferred #5を進め、本文参照表の検査は本sliceへ含めない。

【実測】SCOPE v2 §1、§5〜§8は、次の正式authorityと一致する。

- 正式改善候補は、現在有効な上位文書を指すfront matter参照だけを`scope`とし、Markdown本文、
  JSON record、生成時点pin、不変Evidence、Task Contract固定入力、Test内pinを`non_scope`とする。
- 機械可読Human仕分けDecisionは、対象keyの許可一覧をHuman承認つきで先に宣言し、
  `in_progress`化をHuman判断まで開始しないよう要求する。
- 正式Issueは上記CandidateとDecisionのidentity、version、file SHA-256、content digestへ結ばれている。
- `DEC-FIXED-SOURCE-KIND-001`は、現在一致を要する参照と、後続改定によるDigest不一致が正常な
  `pinned_at_start`を区別する。

【判断】SCOPE v2は、本文参照表案を正式Issueの実装へ混入させず、本文検査の需要を既存の
改善候補経路へ後送している。正式Candidate／Decision／Issueのscope・non_scopeと
`DEC-FIXED-SOURCE-KIND-001`に整合し、先行Finding SR-P1-001の類型1、3、4は解消した。

## 3. 7 key許可一覧と時点固定pin

【実測】SCOPE v2の許可一覧は、正式改善候補が列挙した次の7 keyと過不足なく一致する。

```text
authority_order, operational_policy, policy_decision, related_design,
intent_ref, glossary_ref, reconciliation_ref
```

【実測】固定された実例2文書では、7 keyすべてが現れ、現在有効な参照は合計11件である。
チェックリストの8件はlist形式と単一mapping形式、現行Planの3件は単一mapping形式であり、
scopeが宣言する2つの期待形で表現できる。参照先9 fileのSHA-256を再計算し、重複参照を含む
11／11が記載値と一致した。

【実測】現行Planの`generated_from`にあるDevelopment Policyの記載Digestは`d37a60ab...3903ed46`、
現行bytesは`08bea1f9...a22ad1c`である。SCOPE v2は`generated_from`を許可一覧へ含めず、
許可一覧外keyを合否に使わない境界例を受入条件に置いている。

【判断】7 keyは上流Candidateの承認対象をそのまま機械可読化する最小集合として、範囲段階では妥当である。
`generated_from`等を非対象にしたことで、正常な時点固定pinを現行bytesとの不一致だけで誤拒否しない。
許可一覧からの追加・削除と期待形の拡張もHuman承認事項として停止条件に入っている。

## 4. riskとHuman境界

【判断】risk `high`提案は妥当である。参照Digestの一致を他文書の現在有効性の判定に使う守り役のcodeで、
誤りは「ずれの見逃し」または「正しい時点固定参照の誤拒否」として黙って現れるため、
`work-review-protocol.md` §3の既定`high`に該当する。

【実測】SCOPE v2は、次の3つをHumanへ残している。

1. risk `high`の確定。
2. 7 key許可一覧そのものの承認。
3. 合格した再範囲レビュー後のRED開始に対する再開承認。

【判断】上記は同一のHuman messageで承認できるが、いずれもPilotやReviewerの判断だけでは代替されない。
許可一覧の追加・削除、対象形の拡張、実文書の修復もHuman判断または別作業単位へ戻すため、Human境界は
維持されている。本recordの`verified`だけではREDを開始できない。

## 5. 停止条件

【判断】SCOPE v2 §10の停止条件は範囲段階として十分である。固定入力・base・worktreeの不一致、
許可path外変更、許可一覧で表せない実例、対象keyまたは形の拡張、未実装以外のRED失敗、既存実装でのGREEN、
Test・receipt・Digest照合の不合格、実文書修復の必要を停止にしている。§3、§6、§12と合わせて、
Humanのrisk確定・許可一覧承認・RED再開承認前も停止する。

## 6. 実装時確認事項

次の2件は`work-review-protocol.md` §11.2に従い、範囲レビューを止めない。

1. resolve後のpathがsymlinkを介してrepository外へ出る場合も拒否すること。
   - 分類：`non-blocking`
   - 確認段階：`implementation／completion`
2. 不正形、参照0件、file別・key別集計をJSONで区別し、集計結果と終了コードを一致させること。
   - 分類：`non-blocking`
   - 確認段階：`implementation／completion`

これらはSCOPE v2 §11にも引き継がれており、完了レビューで機械実行する。

## 7. commit `c7579ff`による先行レビュー§6の解消

【実測】commit `c7579ff`の変更pathは
`records/development/2026-08-09-role-neutral-mode-trial-metrics-v1.md` 1件だけで、11行追加、3行削除、
`git diff --check c7579ff^ c7579ff`は終了コード0だった。

【実測】訂正後は、scope固定からReviewer判定までが2026-08-09、Closer projection `86a1cd0`が
2026-08-10T06:27:47+09:00であり、§1の計測定義では2暦日にまたがると記載する。Git履歴と一致する。

【実測】訂正後は、比較元を§1と同じ「停止系判定の発生回数」に揃え、範囲2回と完了2回の合計4回から
low risk作業の0回への比較を`4→0`と記載する。後に再評価で`verified`へ訂正された範囲レビューv2も
発生回数へ含める規則を明記しており、§1の内訳と一致する。

【実測】repository内で独立再計算できないtoken 3値と2件の欠測は、訂正後も数値自体を検証済みにせず、
`reported_unverified`として比較・裁定の根拠から外している。

【判断】先行レビュー§6の競合2件は実状態に一致する値と計数規則へ訂正され、token値のEvidence不足も
正しい状態表示へ分離された。commit `c7579ff`は同節の指摘を解消している。

## 8. 独立確認と判定

【実測】次を単独commandで確認した。

- `python3 -m tools.development.todo_handoff TODO_NEXT_SESSION.md`：終了コード0、finding 0。
- `.venv/bin/python3 -m pytest`でV4のrepository decision集合とIssue集合の整合Testを指定：
  終了コード0、`2 passed`。
- SCOPE commitと訂正commitの`git diff --check`：各終了コード0。
- 固定入力13／13、scope、先行scopeのSHA-256：すべて一致。
- 実例の現在有効な参照11／11：SHA-256一致。

参考観測（Findingではない）：【実測】旧V3登録validatorを正式Candidateへ再実行すると、
作成時Evidenceのうち後に改定されたfileを
現行bytesと比較するため`Evidence reference is stale or unavailable`で終了コード1になった。一方、
Candidate自身の固定SHA-256、Candidate→Decision→Issueの指紋結線、現行V4 repository集合は一致し、
上記2 Testに合格した。

【判断】旧V3 validatorの結果は、作成時点Evidenceのpinを現行bytesへ再照合した結果であり、今回の
scope変更、正式recordのidentity結線、またはSCOPE v2の受入境界との不一致を示さない。§11.4に従い、
本sliceのblocking Findingにはしない。旧登録validatorで歴史Candidateを再検証する場合の扱いは
本scope外である。

判定：`verified`

変更範囲：SCOPE commitはscope record 1件だけで、申告base、Digest、固定入力と一致する。

Record照合：正式Candidate、Human triage Decision、Issue、`DEC-FIXED-SOURCE-KIND-001`、deferred裁定、
先行レビュー、Human裁定「(a)で確定」と照合した。

Human境界：維持。risk確定、7 key許可一覧承認、RED再開承認は未実施でありHumanに残る。

未実施：RED、実装、製品Test、Evidence、receipt、review request、実文書への適用・修復、TODO、
checklist、既存recordの変更、外部操作、次段作業。

次：Humanがrisk `high`、7 key許可一覧、RED開始の再開を明示承認する。
