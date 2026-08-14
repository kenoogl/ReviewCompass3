# Claude用：立て直し計画v5 第5段完了候補 読み取り専用全体レビュー指示書 v1

この指示書は利用者がClaudeへ手動で渡す。ReviewCompass3へ書き込まず、結論を前提にしない独立レビューを行うこと。

## 1. 目的

立て直し計画v5の第5段について、完了候補が次の事項を証拠付きで満たすかを全体として確認する。

1. 第5段の六作業と完了条件が、承認済みTask Contract、製品入口、利用者受入、正式・安定表示、独立確認、次作業候補へ一対一で対応すること。
2. 製品入口が人の転記で部品をつなぐ一時経路ではなく、導入後に使える正規実行名へ接続されていること。
3. 古い状態識別値に依存せず、訂正裁定後の根拠だけで現在状態を支持していること。
4. 第5段で触れた全成果物が列挙され、現在保証・履歴監査・両方・現在位置のいずれかへ説明可能であること。
5. 次作業候補が現在の製品機能から導かれ、未承認の保存機能、G26、暫定計画・要求を勝手に正式化または実装しないこと。

このレビューは第5段完了を承認しない。最終判断は利用者へ返す。

## 2. 開発物の機能と用途

対象の製品入口`reviewcompass3-session-artifact`は、利用者が許可したローカルSession記録一件を読み、伏字化した転写、要約、来歴を一回のJSONとして画面へ返す機能である。過去作業の確認、引継ぎ、レビュー、調査に使う。

対象形式はClaude JSONL、Codex公開JSON stream、Codex rolloutである。保存、探索、複数file処理、外部送信、network、外部process、Git操作は行わず、`external_send_approved: false`を返す。全ての機微情報を検出する保証ではなく、承認済み契約の既定規則、高乱雑性検査、絶対path最終検査の範囲を守る。

## 3. 固定観測点と固定材料

- 観測commit：`6fd2786dbf7a95f8e2b97bc12542e6dce6a6c98c`
- 第5段開始基準commit：`5fdff893b081637b987b0c3539fe7fdbc89a779f`

最初に各commitの実在と各fileのSHA-256を機械確認する。不一致があれば、その材料に依存する判断を停止して報告する。

| 材料 | SHA-256 |
| --- | --- |
| `docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md` | `8c814067511797e445d66779ad144f42ea0b139501ff6002a7d6c46e6706055c` |
| `records/development/2026-08-14-recovery-plan-v5-stage5-completion-candidate-v1.md` | `5e9e2adebe65372e2e315bd5fbedc07302f11451854e8ad1a52313425ed9b04a` |
| `records/development/2026-08-14-recovery-plan-v5-stage5-completion-candidate-independent-overall-review-v1.md` | `0ff20a88464ad6b7121842a21194c073034f5396bd59de7250e1b1f3b685eda4` |
| `records/task-contract/2026-08-14-g25-session-artifact-preparation-candidate-v1.md` | `20e4e0551c5b1357ba3e66d6ba849f19566da27c58c54ef98e8fa1db110fb72b` |
| `records/development/2026-08-14-stage5-g25-session-artifact-task-contract-definition-correction-review-v1.md` | `8f07d74cb03e4ab6134a1774af8b775e1d01c57d836f32720ad6296dd1099e91` |
| `records/development/2026-08-14-stage5-g25-session-artifact-task-contract-approval-decision-v1.md` | `dde3ad7be1a31f1c7f77e253a90fe952496950e5b6a402fcdf473388d211ae39` |
| `records/development/2026-08-14-stage5-g25-session-artifact-entry-claude-completion-review-result-v1.md` | `2eda7a0ac9f89d53df9a75298ad494d75a613b89606ecc20ca6f17bd251ee637` |
| `records/development/2026-08-14-stage5-g25-session-artifact-entry-receipt-binding-adjudication-v1.md` | `0479601e87114a438afaf0536f0327d321c87dd6e534a042907d6869dec7ae2f` |
| `records/development/2026-08-14-stage5-g25-session-artifact-product-entry-acceptance-decision-v1.md` | `57818c4390c02b866c55708b4292e965144d281a2349a5d12ad27bc4d31b7187` |
| `records/development/2026-08-14-stage5-g25-session-artifact-maturity-promotion-decision-v1.md` | `b0529f44d202c4b9c49600624417a54a611ad8eb77581ee9515c941291f850d1` |
| `records/development/2026-08-14-stage5-g25-session-artifact-maturity-promotion-evidence-v1.md` | `51df5b3b84ce3ca846fc7206b0c1c9ad290db6021bb0dbe91f5f2dd4297bd6a4` |
| `records/development/2026-08-14-stage5-g25-session-artifact-maturity-promotion-independent-completion-review-v1.md` | `3258ca6ea289852ef6a065bc5d103928fa654a15a4b56a455ee3e24741adfb92` |
| `docs/current/reviewcompass3-plan-current.md` | `1a73597605eafb65a2259ccf19431e3aba041564d03fdb279150042a9bd0962f` |
| `docs/requirements/remaining-feature-requirements.md` | `ec31ce53ce097a8ff8a59a4649d97e4af8d8dd0cbdb8a1a8c7d4e8d2a1f8bcf6` |

現在の主要成果物も確認する。

| 成果物 | SHA-256 |
| --- | --- |
| `tools/session_logs/read_only_entry.py` | `dd95f087833d4ff30fbb761193a3a2e7da5a2536954a766624aa9d7e77530d72` |
| `tests/test_session_log_read_only_entry.py` | `8152c5bb82ca235d723aac69fb519b2b6284a3f92cf6e2972328b4f479e5e053` |
| `pyproject.toml` | `ec771cd06e063d2f4b252ecfc9962d7f221effbf072169edbabfb7c8f71d3229` |

## 4. 必須確認

### 4.1 第5段の六作業

上位計画の第5段本文から六作業と完了条件を自分で抽出し、完了候補の対応表を使わず、固定材料とGit履歴へ個別に対応付ける。空欄、順序の逆転、利用者判断の代行がないかを確認する。

### 4.2 正規製品入口

`pyproject.toml`の実行名から`tools.session_logs.read_only_entry:main`、その先の処理までを読む。三形式の確認対象と同じ処理へ直接つながり、人が別関数を選び直したり結果を転記したりしないことを確認する。

配布物の独立確認記録は、導入済み実行名で代表形式を確認し、同じ接続先で三形式を確認したものである。「導入環境から三形式全てを個別実行した」という追加主張へ広げない。

### 4.3 契約、受入、正式表示

Task Contractの作成時表示と、その後の実装承認、製品受入、正式・安定表示への昇格を履歴順に分ける。作成時の候補表示を過去資料の改変で消していないこと、現在の正式表示が利用者判断と独立確認に基づくことを確かめる。

### 4.4 古い状態識別値の排除

古い状態識別値`4251a948...`を現在の合格根拠に使ってはならない。完了候補と固定材料から依存経路を検索し、訂正裁定後の履歴付き複製での独立実行、製品受入、昇格後確認だけで現在状態を支持できるか確認する。

### 4.5 正規全試験結果の再利用

昇格独立レビューは、履歴付き複製で対象12件、G25関連55件、正規全試験1,740件の成功を記録している。この独立実行後から観測commitまでの製品コード、試験、設定、配布入口に変更がないかをGitで機械確認する。

- 差分が0件なら、正規全試験を儀式として再実行せず、既存結果を利用する。
- 差分がある場合だけ、影響を特定し、必要な試験を実行する。
- 1,740件は観測値であり、恒久の合格値として扱わない。

### 4.6 全変更経路と役割

第5段開始基準commitから、完了候補が観測したcommit `515db1d78ab9afcae72a5edc3dcad7943b20e860`まで、次の二集合をGitから独立再生成する。

1. 終点間の差分path。
2. 履歴中の全commitで一度でも触れたpath。

期待値は、両集合が同じ20件、追加18・変更2・削除0である。完了候補の付録や集計を正本にせず、双方向差、重複、途中で消えたpathを確認する。

その20件を、製品コード1、試験1、実行名設定1、Task Contract 1、開発記録13、Claude受渡し指示2、現在位置の引継ぎ1へ独立分類する。各成果物について、利用先、守る性質、現在保証・履歴監査・両方・現在位置の別、役割終了時の扱いが説明できるかを見る。削減数を目的にしない。

### 4.7 次作業候補の導出と境界

次候補は「利用者が許可したSession記録一件と、現在の正式入口が作る伏字化結果を、安全な別領域へ保存して再読込みできる範囲」の二つ目のTask Contract候補を定義し、独立した定義挑戦を行うことである。

これは実装承認ではない。G26の既知の保存先境界欠陥を解消済みと扱わず、G26、暫定製品計画、暫定要求を正式化せず、保存・探索・削除・外部送信を実装しない境界を確認する。

### 4.8 第5段の最終判断

完了候補と内部レビューが`verified`でも、第5段完了は利用者だけが判断する。完了済み表示、TODOの完了更新、次作業の開始が先取りされていないことを確認する。

## 5. 反証の要件

中心判断を崩す反証を少なくとも一つ機械で試す。例は次のとおりである。

- 六作業のいずれかが記録だけで実体を欠く。
- 実行名と三形式の処理が別経路で、人の手作業でつながる。
- 古い状態識別値が別記録を経由して現在根拠へ戻る。
- 独立全試験後に製品コード、試験、設定、配布入口が変わっている。
- 終点差分が履歴途中で消えたpathを隠す。
- 次候補がG26や暫定上流文書を無承認で正式化する。

反証が成立しなければ、その結果も書く。反証のためだけの新試験、新機構、台帳、検査器、関門をリポジトリへ追加しない。

## 6. 比例原則と禁止事項

- 本質から外れた修正案を出さない。
- 問題が見つかった場合も、原因へ直接対応する最小訂正だけを示す。
- 製品コード、試験、設定、Task Contract、計画、TODO、既存記録を変更しない。
- file作成、stage、commit、push、履歴書換え、外部送信を行わない。
- 正規全試験を差分0件なら再実行しない。
- 次の保存契約を作成、承認、実装しない。
- G26を修正せず、暫定計画・暫定要求を正式化しない。
- 第5段完了を代行しない。

## 7. 回答形式

次の順で、平易に報告する。

1. **判定**：`verified`、`correction_required`、`reported_unverified`、`report_execution_mismatch`のいずれか。
2. **止める指摘**：件数、事象、根拠、最小訂正。なければ0件。
3. **報告不一致**：件数と影響。なければ0件。
4. **第5段の六作業と完了条件**：一対一対応の結果。
5. **製品入口の機能・用途・限界**：技術用語だけで済ませず説明する。
6. **正規入口、契約、受入、正式表示**：実体と順序の確認結果。
7. **古い状態識別値と試験結果の再利用**：排除と差分確認の結果。
8. **20経路と役割**：独立再生成、過不足、役割分類。
9. **次作業候補の導出と境界**：行うこと、まだ行わないこと。
10. **試した反証と結果**。
11. **利用者が判断する点**：第5段完了と次の定義挑戦を分ける。
12. **未実施事項**。

