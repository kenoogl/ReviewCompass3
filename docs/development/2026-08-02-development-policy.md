# ReviewCompass3 開発方針

状態：現行方針

制定日：2026-08-02

改定日：2026-08-04

## 目的

ReviewCompass3の品質と追跡可能性を維持しながら、手続き自体の増大によって
利用可能なE2E成果への到達が遅れることを防ぐ。本方針は開発方法を定め、
製品のintent、requirements、designそのものとは分離する。

## 開発単位

- SDDを維持し、変更は小さなE2E縦切りを優先する。
- 新しい抽象、Schema、関門は、縦切りで具体的な不足が確認された場合に追加する。
- WIPを一つの縦切りへ制限し、完了前に並行する基盤拡張を増やさない。

## リスクベースのテストファースト

振る舞いを変更するコードには、実装前または同一変更内で関連テストを用意する。
テストは変更がなければ失敗することを、実行、既存履歴、差分検査など適切な方法で
確認する。

- `low`：関連する自動テストを実行する。
- `medium`：関連テストに加えて全テストを実行する。
- `high`：全テスト、変異検査または同等のfault injection、代表データ検証、
  独立レビューを行う。

保存、削除、機微情報、権限、状態遷移、外部送信、復旧は原則として`high`とする。
文書、試作、調査には形式的な赤緑サイクルを強制せず、整合性、知見、限界、
根拠を変更種別に応じて確認する。

test、validator、lint、schema検査も誤り得る実装として扱う。`medium`以上では変更対象の検査器に
既知の正例、負例、境界例を用意し、`high`ではmutationまたはfault injection、独立oracle、
代表実データを用いて、見つけるべき違反を検出できることを確認する。検査器または入力前提を
変更した場合、過去の合格結果をそのまま再利用しない。

成果物を書き換えた変更は、riskに応じて書込み結果を再読込し、関連validator、参照整合、stale
閉包を確認する。実行前の計画や生成成功だけを、書込み後の正しさの代用にしない。

赤テストだけのコミットは必須にしない。統合対象のコミットは原則として全テストが
緑の状態にする。要求の誤解や設計変更が判明した場合は、理由と変更後の期待動作を
記録してテストを修正できる。

## LLMと機械処理の責務分離

LLMが直接担う処理は、文章の作成・編集・要約と、意味分析、意味分類、判断候補の説明に限定する。
入力と規則から同じ結果を再生成できる決定的処理は、LLMが文章上で手計算・手転記・手探索せず、
版付きの機械処理へ渡す。

機械処理の対象には少なくとも次を含む。

- 構造化dataの抽出、変換、正規化、生成
- ID、version、Digest、参照、schema、coverage、staleの照合
- 件数、集合差、重複、sort、再生成一致の計算
- fileの読込み、書込み、再読込、配置検査
- Test、validator、lint、build、Git状態確認、command実行、receipt生成

機械処理の出力も誤り得るため、固定入力、版、Digest、正例・負例・境界例、post-write verificationを
riskに応じて要求する。機械処理は意味的裁定またはHuman承認を代替しない。

必要な機械処理が存在しない場合は、反復的な手作業を既定経路にせず、最小の決定的toolを作るか、
`manual_operation_candidate`として改善候補へrouteする。手作業に起因または起因が疑われる手戻りは
`manual_rework_candidate`とし、同じ作業内の軽微なやり直しとして隠さない。

## Human判断

Human承認を必須とするのは次の操作である。

- 方針変更
- 外部送信
- 不可逆操作
- 意味的な競合またはFindingの裁定
- 段完了

通常の実装、関連テスト、可逆なリファクタリング、機械検査には個別承認を要求しない。
Human判断は、機微情報検査、内容同一性、権限などの機械関門を免除しない。

## 段階的自己適用

ReviewCompass3自身へ適用する機能は、現行の契約とテストを満たし、`stable`と
明示されたものに限定する。`provisional`、`experimental`、未分類の機能を
自己適用の必須経路に置かない。自己適用能力そのものは製品要件として維持するが、
開発中の全機能を常時自己適用することは要求しない。

## 自己適用で得た改善候補の扱い

自己適用中に見つかった問題、改善案、新機能案は、現行のPlan、Task Contract、Testまたは
受入基準を直ちに書き換える理由にしない。まず改善候補（`improvement_candidate`）として、
発生元Work、固定source identity、観測Evidence、影響、提案を記録する。

候補は少なくとも、Implementation不良、Test／oracle不良、Task Contract不良、Requirement不良、
Intent競合、外部blocker、process改善、product ideaへ分類する。分類に応じて、current Work、
Upstream Revision、Dependency、Issue Resolution、checkpoint queue、defer、rejectまたはduplicateへ
routeする。候補はIssueへ自動昇格させず、consumerと後続Outcomeへ接続されるまでclosedにしない。

次に該当する候補は現行Workを`pause_and_triage`し、それ以外はcheckpointまで現行作業を継続してよい。

- safety、security、privacy、権限または許可の妥当性を損なう
- Acceptanceの真偽、必須Provenance、source／Test／Verdict identityを信頼できなくする
- 不可逆または外部side effect、開始permit、停止・復旧条件へ影響する

現行のAcceptanceの真偽を変える必要がある場合は、実装都合の軽微修正として扱わず、現行Workを
停止して版付きのUpstream Revisionへ移る。機械またはAIは必須field、identity、Digest、freshness、
重複の検査と分類・route候補の提示まで行えるが、Plan、Requirement、Task Contract、Test、permitを
自動変更しない。意味分類、停止、上流改定、Issue昇格、risk受容、再開はHuman判断とする。

意味分類、停止判定、route候補の説明とHuman裁定は実行チェックリストで運用し、Work 8で停止漏れ、
誤停止、route時間、未消費候補、重複、再発、記録負担を評価する。一方、必須field、identity、Digest、
freshness、重複の検査と記録生成は機械処理を使う。製品schema、正式state machine、permit連携、
自動Plan編集は手作業Pilot後の別Task Contractまで導入しない。詳細な分類と決定表は
`docs/design/2026-08-03-self-application-improvement-routing-memo.md`を参照する。

## 実施報告と実状態の照合

会話、TODO、checklistまたは最終報告に書かれた「実施した」という記述はClaimであり、それだけを
完了Evidenceにしない。後続状態を変える報告は、実施、結果、判断、提案、未実施へ分け、実施・結果・
判断Claimを対象identity、固定source、Evidence locator、観測した事後状態へ接続する。

EvidenceがないClaimは`reported_unverified`として未完了のまま残す。報告と事後状態が競合する場合は
`report_execution_mismatch`として完了判断を停止し、影響を受けるTODO、checkbox、Verdict、projectionを
staleにする。未実施作業は、提案または予定と区別して明記する。

file操作はpath、diff、再読込、Digest、必要なlink検査、Test実行はcommand、exit code、対象source、
結果、commitはcommit SHAと対象treeを照合する。外部または不可逆操作はreceiptと独立した事後状態を
確認する。詳細は`docs/design/2026-08-03-execution-claim-verification-memo.md`を参照する。

手戻りが発生した場合は、手作業との因果を必ず確認する。手作業が原因または原因候補である場合、
作業後報告へ次を含める。

- 対象操作
- 期待executorと実際のexecutor
- 手作業になった理由
- 手戻り事象とEvidence
- 機械処理へ移す候補
- current Work、改善候補、別Task Contract、defer等のroute

手戻りがなくても、本来機械処理すべき決定的操作をLLMが直接行った場合は
`manual_operation_candidate`として報告する。

## Commitとhandoffの原子性

### 作業単位終端のcommit reminder Pilot

完了した作業単位を未コミットのまま次の作業単位へ進めない。作業単位の完了時と次作業への移行要求時に、
完了状態とGit worktree状態を機械的に照合する。`completed`かつdirtyなら
`completed_work_unit_uncommitted`として次作業への遷移を停止し、Humanへコミットをリマインドする。
作業中のdirty差分だけではこの状態に分類しない。

通常の開発作業のコミットは、次の最小条件をすべて満たす場合、コミットごとのHuman明示指示なしに行う。
正本は`records/development/2026-08-05-semantic-commit-minimal-guards-decision-v1.md`
（`DEC-SEMANTIC-COMMIT-MINIMAL-GUARDS-001`）とする。

1. 一つの目的と確認結果を独立して説明できる、意味的に完結した作業単位である。
2. stage対象は明示したrepository-relative pathの列挙だけである。`git add -A`、`git add .`、
   範囲外fileの一括追加を使わない。
3. `git diff --check`と、変更に応じたtest／validatorを実行して合格している。
   `TODO_NEXT_SESSION.md`を含める場合は`python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md`も
   合格している。
4. commit後はread-onlyで状態を照合し、完了済み作業単位を未コミットのまま次の作業へ渡さない。

自律化するのは上記の**通常commitだけ**である。次は引き続きHumanの明示承認を必要とする。

- 方針変更、段完了、意味的裁定、不可逆操作、外部送信
- push、tag、amend、rebase、reset、force push、履歴書換え
- sandboxまたはhostの権限の迂回

**置換済みの旧制限**：「Pilotではコミットを自動実行せず、従来どおりHumanの明示指示を必要とする」という
旧方針は、上の最小ガードへ置換した。push、guarded commit、hook、amend、rebase、reset、履歴書換えを
対象外とする点は変更していない。guarded commit、hook、コミットごとの恒久的な承認file、巨大な
commit manifestは導入しない。遷移前の機械検査には
`python3 tools/development/work_unit_transition.py --work-status completed`を使用する。

最終コミットに`TODO_NEXT_SESSION.md`の引き継ぎ更新を含める場合、TODOのGit欄は、そのコミット完了と
同時に真になるcommit安定形式へコミット前に更新する。コミット後はGitの事後状態をread-onlyで照合し、
自己SHAまたはremote状態をTODOへ転記するためだけの追加コミットを作らない。

TODOのGit欄へ次のmutable snapshotを固定しない。

- TODO自身を含むコミットのSHAまたはHEAD値
- 数値付きahead／behind
- push済みまたはpush未実施というremote同期状態
- TODOだけが未コミットという一時的worktree状態

HEAD、upstream、ahead／behind、push状態の正本はGitとし、必要時に機械取得する。TODOには
`本handoffを含むcommit完了時点`というcommit境界と、Gitから機械取得する旨を記録する。最終stage前に
`python3 tools/development/todo_handoff.py TODO_NEXT_SESSION.md`を実行して検査する。commit SHAが必要な
Evidenceは、当該コミットと循環しない後続EvidenceまたはGit自体へ接続する。この運用にguarded commit、
post-commit amend、hookは要求しない。

## コード形式

Pythonは4スペースを使用する。その他の言語は標準フォーマッターに従う。
既存の2スペースPythonを方針変更だけのために一括整形せず、機能変更時に段階的に
合わせる。これにより、挙動変更と整形差分を混在させない。

## 評価指標

次の観測値で方針の有効性を確認する。

- 最小E2E縦切りまでのリードタイム
- 一変更のサイクルタイムと再作業量
- 手作業による手戻り件数、`manual_rework_candidate`、`manual_operation_candidate`、機械処理移行率
- 本番または受け入れ段階へ流出した欠陥
- source universeの大きさ、変更単位数、影響閉包、レビュー入力のbyte／token数
- 無関係な材料追加時の入力増加、広域scopeまたは全文整合reviewへの拡大率と理由
- レビューの実行時間、外部費用、Evidence Coverage、既知Findingの見逃し
- 必須Evidenceの消費率、材料不足、責務外Finding、post-write再検出
- validatorの既知違反検出率、正常例の誤停止、mutation生存数
- 改善候補の停止漏れと誤停止、route時間、未消費率、重複率、同種問題の再発
- 完了報告ClaimのEvidence接続率、`reported_unverified`、`report_execution_mismatch`、誤進行の件数
- 追加した文書、Schema、関門の維持費

コミット数、テスト数、記録数の増加だけを品質の代理指標にしない。

## 機械評価

`config/development-policy.json`を実行設定とし、
`tools.development.policy`が変更種別、リスク、Human承認対象、自己適用機能の成熟度を
決定的に評価する。呼出し側は検査器変更を`changes_validator`、検査入力の前提変更を
`changes_input_assumption`、成果物書込みを`writes_artifact`で明示する。前二者では返却値の
`prior_verdict_stale`が真となり、risk別のvalidator assuranceが必要になる。実行設定と本文が
競合する場合は本文を優先し、設定を修正する。

改善候補の意味分類、停止判定、route裁定は本文、実行チェックリスト、Human判断で運用する。
`config/development-policy.json`と`tools.development.policy`は、LLM許可操作、機械処理必須操作、
手作業による手戻りの報告項目を決定的に評価する。製品state machine、permit連携、自動Plan編集は
Work 8のPilotで必要性と境界を確認した後に判断する。

実施報告の文章化と意味分析はLLMが行えるが、path、Digest、Test、Git、receipt、Decisionとの対応確認は
機械処理する。報告Claimの製品内自動抽出と完了状態への自動結線は、Session Log BootstrapとWork 8の
評価後に別Task Contractで判断する。
