# AGENTS.md

利用者の指示は重要な入力であるが、それだけで妥当とみなさない。目的、根拠、影響、既存方針との
整合、より単純な代替案を批判的に検討する。問題や反対根拠がある場合は迎合せず、作業前に平易に
説明して修正案を提案する。利用者が根拠を踏まえて判断した後は、その決定と合意範囲に従う。

本文書は入口と判断規則の最小集である。詳細は§4末尾の正本へ委譲する。規則の追加は実害または
根拠recordを要し、追加の前に既存規則への統合を検討する。記述が実装またはDecisionと食い違う
場合は実測を優先し、食い違いを観測として記録して本文書を更新する（根拠：2026-08-08の実害、
`records/development/2026-08-08-egress-name-contract-adjudication-v1.md`と同日の手戻り）。

## 1. 入口

- 指示を受けたら自分の理解で復唱し、作業開始前に作業項目を適切な粒度で示す。
- 立て直し期間の開発は`docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md`を入口とし、
  第1段から第4段は§5の軽量作業票と§6のレビュー手順で進める。採用判断は
  `records/development/2026-08-12-project-stall-recovery-plan-v5-adoption-decision-v1.md`に固定する。
- 作業の重要度と不確かさに応じて確認の深さを決めるときは、
  `docs/development/2026-08-13-risk-proportional-verification-method-note-v1.md`を判断補助の入口とする。
  軽い作業へ重い確認を一律に強制せず、既存計画の必須レビューと承認境界を優先する。
- `docs/development/2026-08-03-initial-development-checklist.md`は現在位置とEvidenceを確認する入力として使い、
  立て直し中の作業順は上記計画を優先する。checkboxだけを完了根拠にしない。
- `TODO_NEXT_SESSION.md`の読取・作成・更新・検証は`docs/development/prompts/todo-handoff-update.md`
  の共通手順だけを使う。
- 委譲した作業のレビューは`docs/development/work-review-protocol.md`を共通入口とする。ただし、立て直し計画の
  第1段から第4段では同計画§6を入口とし、§6.8が限定する深さで共通プロトコルを適用する。
- Pilot連携は`docs/development/prompts/pilot-collaboration-run.md`を共通入口とする。

## 2. 報告と判断の規則

- 報告は実施・結果・判断・提案・未実施を分け、実施・結果・判断にはpath、diff、Digest、
  command結果、commit SHA、receiptまたはDecisionを対応付ける。Evidenceの無い報告は
  `reported_unverified`、報告と事後状態の相違は`report_execution_mismatch`として完了判断を停止し、影響を受ける表示と判断をstaleにする。
- 事実の主張には【実測】【記録】【推測】のラベルを付け、人の判断に影響する主張は実測か記録だけで
  出す。主張の前に既存recordを先に探し、重要な主張は反証を1つ機械で試す。ラベルの無い主張には
  利用者が出どころを問い返してよい。
- 深掘りの停止：本線中の発見は記録し、その場で直さない。対処が必要なら3択（いま対処／候補として
  後回し／本線へ戻る）と現行Plan上の位置づけを併記して人へ渡す。連鎖の深さ2以上の対処は開始前に
  停止して人の判断を得る。本線外の対処は1作業単位に原則1本。未承認の設計変更・schema変更・
  既存Testの書換えが必要と判明した時点で止める。有用な発見ほど候補として記録し本線の区切りで扱う。
- 手戻りが発生したら、対象操作・期待executor・実executor・手作業理由・事象とEvidence・
  機械処理候補・routeを作業後報告に含める。
- 問題がある場合は、事象と原因を平易に説明する。
- Human裁定を求める前に、目的、固定根拠、判断基準、推奨案、承認した場合としない場合の影響を
  この順に平易に示す。機械処理と意味分析で先に候補を絞り、技術候補の全件判断をHumanへ渡さず、
  意味、risk、authorityなどHumanに残す必要がある最小判断へ圧縮する（根拠：2026-08-15の説明不足と
  `records/development/2026-08-15-safe-storage-capability-reuse-human-adjudication-decision-v1.md`）。

## 3. 機械規律

- LLMは文章操作と意味分析に限定し、決定的な変換・抽出・集計・照合・file操作・Test・Git確認・
  command実行は機械処理を使う。未整備なら手作業を常態化させず改善候補へrouteする。
- test・validatorの合否は**単独で実行したcommandの終了コード**で確認する。pipeや`;`連結の後段で
  合否を判定しない（根拠：2026-08-08、不合格コミット2件通過の実害）。
- `.reviewcompass/workflow/`配下の台帳recordは**対応する正規tool（検証器を含む）だけで作成・変更**
  する。雛形複製の手書きを禁止する（根拠：2026-08-08、台帳整合テスト不合格とrevertの実害）。

## 4. 開発と改善の要点

- 実装方法を選ぶときは、実装前に異なる3案を出し、少なくとも1案を既存機能・設定だけで
  済ませる最小案とする。単純さ、処理時間、メモリ使用量、頑健さ、変更範囲、保守負担、戻しやすさを
  短く比較し、選択理由を作業票または作業報告に残す。比較のためだけの新文書・Test・機構は作らない。
  実装方法の選択がない機械的な値更新、指定された原状回復、文言だけの訂正は対象外とする。
- SDDと小さなE2E縦切りを基本単位とする。振る舞いの変更は関連テストを実装前または同一変更内で
  用意し、変更が無ければ失敗することを確認する。赤テストだけのコミットは必須にしない。統合対象のコミットは原則緑。要求の誤解や設計変更が
  判明したら理由を記録してテストを修正できる。文書・試作・調査に赤緑サイクルを強制しない。
- 変異検査・実データ検証・独立レビューは高リスク境界に適用する。validatorまたは入力前提を変更したら
  旧合格をstaleとし、risk別の例と独立oracleを再実行する。成果物を書き換えたら再読込・関連validator・
  参照整合・stale閉包を確認する。
- Pythonは4スペース、他言語は標準フォーマッター。機能変更と無関係な一括整形をせず、変更時に段階的に合わせる。
- Human承認は方針変更・外部送信・不可逆操作・意味的裁定・段完了に要求する。
- 自己適用にはstable機能だけを使う。自己適用中の発見は改善候補（`improvement_candidate`）として
  記録し、safety・authority・Acceptance真偽・必須Provenance・identity・不可逆や外部side effectに
  影響する候補は現行Workを停止、それ以外はcheckpointで扱う。AIの分類とrouteは提案であり、
  上流改定・Issue昇格・risk受容・再開はHumanが判断する。採用候補はconsumerとOutcomeへ接続されるまでclosedにしない。
- 改善候補の登録は既存経路で行う：`OBS-`観測record→`source_identity`で束縛した`IC-`候補を
  `.reviewcompass/workflow/improvement-candidates/`へ置き、
  `.venv/bin/python3 -m tools.development.issue_resolution_pilot --config config/development-issue-resolution-pilot-v3.json record <path>`
  で検証する。仕分け判断は`records/development/`のDecision recordへ記録する。V4の置き場所は
  固定bundle参照に加えて単体形式N1を受け付ける（2026-08-06のN7改定。実例：
  `ISSUE-AUTHORITY-REFERENCE-DIGEST-CHECK-001`）。トリアージ決定は
  `tools/development/issue_intake_v4.py`の`build_human_triage_decision`で組み立て、台帳整合検証に
  合格させる。旧Pilotの置き場所は凍結のまま。候補記録の形式の作り直しを先に提案しない。
- 正本：開発方針の詳細＝`docs/development/2026-08-02-development-policy.md`。

## 5. コミット

- 正本は`DEC-SEMANTIC-COMMIT-MINIMAL-GUARDS-001`
  （`records/development/2026-08-05-semantic-commit-minimal-guards-decision-v1.md`）。最小条件——
  意味的に完結した単位（ファイル数だけで分割せず、途中状態が不整合やテスト失敗になる分割をしない）・明示pathだけのstage・`git diff --check`と該当test／validator合格・
  コミット後のread-only照合——を満たす通常コミットは、コミットごとの明示指示なしに行ってよい。
- 次は引き続き明示承認を要する：方針変更・段完了・意味的裁定・不可逆操作・外部送信、
  push・tag・amend・rebase・reset・force push・履歴書換え、sandboxやhost権限の迂回。
- 完了した作業単位を未コミットのまま次へ進めない。完了時と「次へ」相当の指示時に
  `.venv/bin/python3 -m tools.development.work_unit_transition --work-status completed`を実行し、
  `completed_work_unit_uncommitted`なら最小条件を満たす意味単位コミットの後に再実行する。
  満たせないときだけ停止して報告する。作業中のdirty差分だけではこの状態に分類しない。自己SHAやremote状態の転記だけを目的とする追加コミットを作らない。利用者がコミット方法を指定したらそれを優先する。
  guarded commitやhook等は導入せず、`stage_completion`など既存のHuman承認境界は緩めない。
