# Work 4B最小試行 範囲提案 承認Decision v1

- decision ID：`DEC-WORK4B-MINIMAL-PILOT-SCOPE-001`
- decision maker：Human
- decided at：2026-08-07
- 指示：本sessionのHuman文言「承認。イシュー登録」（2026-08-07）

## 1. Humanの決定

Humanは、Work 4B最小試行の範囲提案v1を承認した。承認対象は提案§8の3点を含む提案全体である。

1. 範囲提案の承認（宣言→RED対応表とREDへ進んでよい）
2. 対象を「再利用検索記録helper自身の自己適用」とすること
3. 記録の置き場を`records/development/`とすること

なお同じ文言の「イシュー登録」は、直前の手戻り報告の機械処理候補（TODO検証の二段分離と
コミット時テストの終了コード判定）をIssueへ登録する指示であり、別作業単位で実施する。

## 2. 承認対象と実Digest

| 種別 | path | SHA-256 |
| --- | --- | --- |
| 範囲提案（承認対象） | `docs/design/2026-08-07-work-4b-minimal-pilot-scope-proposal.md` | `51eec963e5b7469110658a2a0b95f9d4effbe9279f078175076fe0e1dda2169a` |
| Current Plan | `docs/current/reviewcompass3-plan-current.md` | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` |
| Work 4A早期完了Decision | `records/development/2026-08-05-work-4a-early-completion-and-4b-decision-v1.md` | `68899660b1162b0fb00e5e2b604b3c3c4831c7cc0a32eebfe9541fd0d441a29e` |

## 3. 承認により許可されること

- 提案§4の規範宣言R1〜R7に対する宣言→RED対応表の作成と、「テストの無い宣言0件」の機械カウント
- REDテストの固定とcommit
- RED固定後、提案§5の手順3〜5（実検索の実行と最初の`reuse_search_record`生成、固定テストを
  変更しないGREEN実装、gate判定helperを含むWork 5Bへの引き継ぎ）

## 4. この決定が承認していないこと

- Entry・Relation・Baselineの台帳形式の確定と記録
- 共通部品への移行、旧実装の削除、helper新設以外の既存code変更
- LLMによる説明・Disposition Proposal
- 宣言→RED対応表照合の恒久tool化（対応表作成時にHumanへ判断点を提示する。TODO登録済みリマインド）
- Work 4B段完了、Work 5Bの開始
