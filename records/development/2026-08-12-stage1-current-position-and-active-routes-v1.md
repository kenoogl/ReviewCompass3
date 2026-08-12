# 第1段 現在位置・利用経路表 v1

- 記録ID：`RC3-STAGE1-CURRENT-POSITION-AND-ACTIVE-ROUTES-2026-08-12-V1`
- 作成日：2026-08-12
- 状態：`completion_review_pending`
- 観測対象コミット：`cc2f0476f92291a766071a98247e58ee84e98ad3`
- 履歴確認の開始コミット：`c24e3b4152ce981993afa83bf279878961a73c6f`
- 作業開始コミット：`5674484c554bd336c0306929e0b911ed4ec3c628`
- 作業票：`docs/development/2026-08-12-stage1-current-position-bootstrap-work-ticket-v1.md`
- 作業票SHA-256：`2428853615325add53155f108b608cb81b19ab4bc0bf51ebe9367670379531c0`
- 開始承認：`records/development/2026-08-12-stage1-current-position-bootstrap-start-decision-v1.md`
- 開始承認SHA-256：`55816e66e935f22b6532250a7e59b934fe1bed07f870547c84cde371d8fe0203`

## 1. 対象と方法

本記録は、観測対象コミットにおけるReviewCompass3の現在位置と主要な利用経路を示す。実行して
使用可否を判定する調査ではない。Gitの追跡パス、対象期間の件名と変更パス、`pyproject.toml`の
実行入口、案内文書、直接参照、既存DecisionとEvidenceを確認した。全コミット、全コード、全試験、
全記録は精読していない。

分類は次のとおりである。

| 分類 | 本記録での判定 |
| --- | --- |
| `現役` | 現行の案内、採用判断、実行規則から利用され、使用停止の判断がない |
| `使用停止` | 処理または候補は存在するが、現行計画が再確認または修復まで使わないと明記する |
| `未確認` | 存在または参照は確認できるが、現在使ってよい根拠、接続、昇格、実行結果のいずれかが不足する |
| `履歴のみ` | 現在の入口と主要経路から使わず、過去の経緯または後続候補として保持する |

分類が混在する領域は経路を分けた。必須の`使用停止`部分に依存する上位経路も`使用停止`とし、
依存関係を確認できないものは`未確認`とした。

## 2. 機械列挙の全体像

【実測】観測対象コミットの追跡パスは1,780件である。上位配置別の件数は、`records/` 1,165件、
`tests/` 245件、`tools/` 153件、`.reviewcompass/` 113件、`docs/` 83件、その他21件である。
対象期間は175コミット、変更された固有パスは221件だった。変更パスの内訳は、`records/` 157件、
`tests/` 28件、`tools/` 19件、`docs/` 13件、ルート4件である。

【判断】対象期間の変更は記録が中心である。一方、現在使う入口を件数だけでは決めず、案内、採用判断、
接続状態、使用停止判断を各経路で確認した。

## 3. 五領域の要約

| 領域 | 現在位置 | 主な分類 | 第2段へ渡す事項 |
| --- | --- | --- | --- |
| 製品本体 | Task Contract中心の製品本線は再開していない。統合Intent、用語集、計画は候補として存在する | `使用停止`と`未確認`が混在 | 最初の製品入口と、三つの統合候補をいつ有効入力にするかを選ぶ |
| 最小信頼基盤 | Gitと記録保存、立て直し入口、TODO引き継ぎ、試験入口は案内に接続する。レビュー用コードの統括経路は未接続 | `現役`、`未確認`、`履歴のみ`が混在 | 履歴、コード、試験、レビューの四領域で各一つの正規入口を選び、未レビューの守り役コードへの依存を確認する |
| LLM連携 | 役割文書と複数の実行入口は存在するが、未完了の実送信、認証、応答解析、配置更新は現行計画で停止中 | `使用停止` | 安全に使う一経路を選ぶか、人を介した一時経路として作業票へ固定する |
| 実験 | Issue Resolution早期Pilot、過去の連携試行、評価記録が多数残るが、製品本線または現行レビュー入口ではない | 原則`履歴のみ`。開発用Issue受付だけ`現役` | 現役の開発用台帳と、過去の試行Evidenceを分離する |
| 履歴 | Git、`records/`、Decision、Evidenceは現在の再開根拠として使う。Session Logの製品入口は暫定で、現行案内から直接到達しにくい | `現役`と`未確認`が混在 | Gitと記録を現役の履歴入口として維持し、Session Log群を採用するか別途評価する |

## 4. 主要経路表

| 領域 | 案内文書 | 正規入口または候補入口 | 主要部品 | 設定・保存先 | 接続方法 | 分類 | 根拠 | 未確認事項 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 立て直しの開発入口 | `AGENTS.md`、`docs/README.md` | `docs/plan/2026-08-12-project-stall-review-and-recovery-proposal-v5.md` | 計画§5、§6、§11、採用Decision | `docs/development/`、`records/development/` | 人が入口を読み、Gitと機械検証へつなぐ一時的な中継 | `現役` | `AGENTS.md`と文書索引がv5を入口とし、`DEC-RC3-RECOVERY-PLAN-V5-ADOPTION-001`が採用済み | 第2段以降の正規ツールは未選定 |
| 製品の目的・用語・計画候補 | `README.md`、`docs/README.md` | `docs/current/`の三文書 | Intent、Glossary、製品・開発Plan候補 | `docs/current/`、生成元Decisionとsource record | 文書参照 | `未確認` | 三文書は存在し案内されるが、各front matterは`provisional`、`promotion_required: true` | どのHuman判断で有効化するか、立て直しv5との不一致解消 |
| 製品実行経路 | `README.md`、統合Plan候補 | 該当する製品向け実行入口なし | Task Contract、Workflow、Provenance候補 | `.reviewcompass/`、`records/` | 未接続 | `使用停止` | 立て直し計画v5は第5段まで製品本線を再開しない。TODOにもTask Contract `none` | 最初の製品処理と正規入口は第4・第5段で選ぶ |
| Gitによる履歴・コード管理 | `AGENTS.md`、開発方針 | `git` | commit、tree、diff、status | `.git/`と追跡ファイル | 機械接続 | `現役` | 作業票、Decision、Evidence、現在位置がコミットとSHA-256へ結び付く。現行規則もGit実測を要求 | push状態は本記録の分類対象外 |
| TODO引き継ぎ | `AGENTS.md`、`CLAUDE.md` | `python3 -m tools.development.todo_handoff TODO_NEXT_SESSION.md` | `todo_handoff.py`、`todo_compaction.py`、`todo_handoff_projection.py`、`work_unit_transition.py` | ルートTODO、`records/session-handoffs/` | 文書入口から検証までは機械接続、意味更新は人とLLMの中継 | `現役` | 共通手順が単一入口を指定し、観測対象時点のTODOも直近検証合格を記録 | 守り役コードの独立レビュー未実施Issueが残る |
| 公式試験 | `README.md` | `python3 -m tools.development.policy_test_runner --suite full --receipt <path>` | `policy_test_runner.py`、`.venv/bin/python3`、pytest | `config/development-test-runner.json`、receipt | 機械接続 | `現役` | READMEが公式入口を明記し、版付き設定がPython、pytest、fallback禁止、receipt必須を固定 | runnerは未レビュー守り役の対象。第2段で代表正常処理と独立根拠を再確認する |
| 開発用Issue受付 | `AGENTS.md` | `python3 -m tools.development.issue_resolution_pilot ... record <path>` | `issue_resolution_pilot.py`、`issue_intake_v4.py` | `.reviewcompass/workflow/`、`config/development-issue-resolution-pilot-v3.json` | LLMの意味提案、Human判断、機械検証の組合せ | `現役` | 現行規則が候補登録とDecision組立ての入口を指定し、観測対象にはV4 Issue 8件が全て`registered`で存在 | 台帳の守り役コードは未レビューIssueの対象。製品機能ではなく開発用暫定経路 |
| ブートストラップ中のレビュー手順 | `AGENTS.md` | 立て直し計画v5 §6 | `docs/development/work-review-protocol.md`の限定部分、Git、SHA-256、関連検証 | `records/development/` | 人による一時的な中継と機械証拠 | `現役` | 採用Decisionと`AGENTS.md`が第1〜第4段の入口をv5 §6へ固定 | レビュー実行を一括する恒久な運用経路は選定前 |
| 旧ブートストラップ・レビュー実装 | 文書上は`records/development/2026-08-10-review-protocol-overview-v1.md` | `tools/bootstrap/review_pipeline.py`候補 | closure、payload、contract、execution、parser、triage | private raw、Git内triage候補 | 部品間はコード接続、通常運用へは未接続 | `履歴のみ` | 同記録が統括を呼ぶのは自身の試験のみで、運用経路からの呼出しなしと明記。Git参照検索でも`tools/`外の呼出しを確認できない | 第2段で再利用候補にするか判断するまで現役にしない |
| 機械的レビュー計画 | `docs/development/prompts/review-plan-run.md` | `reviewcompass3-review-plan` | `review_plan_cli.py`、`review_plan.py` | Git差分から一行JSON | 機械接続 | `未確認` | `pyproject.toml`と専用案内は一致するが、立て直しv5 §6はこの生成器を必須入口にしていない | 現行レビューで使うか、過去Pilotだけの部品か未確定 |
| Session Log保存 | READMEと統合Plan候補から概念へ到達 | `reviewcompass3-session-logs` | `tools/session_logs/` 39ファイル | private root、派生記録、配置設定 | CLIから部品へ機械接続 | `未確認` | `pyproject.toml`に入口はあるが、そのmodule自身が`provisional`。主要案内文書とprompt群にコマンド名がなく、未レビュー守り役Issueの対象 | 現在の配置、private root、代表正常処理、運用案内を第2段で確認する |
| Claude/Codex連携の準備・取込み | `CLAUDE.md`、`docs/development/prompts/pilot-collaboration-run.md` | `reviewcompass3-pilot`、`reviewcompass3-claude-implementation`、`reviewcompass3-claude-confirmation` | prepare、ingest、status、二turn確認運転 | private root、`records/session-handoffs/`、一時worktree | 部分的に機械接続。外部実行を含む完成経路は停止 | `使用停止` | 立て直し計画v5 §12が未完了の実送信、認証、応答解析、配置更新を分類まで使用停止とする | 安全に利用できる接続方法を第2段以降で一つ選ぶ。外部送信は別承認が必要 |
| 信頼済み外部送信配置 | `pyproject.toml`のみから入口名を確認 | `reviewcompass3-trusted-transport`と配置先`trusted-review-send` | `trusted_claude_transport.py`、installed wrapper、dispatch | `/usr/local/libexec/reviewcompass/` | 管理者配置を伴う機械接続候補 | `使用停止` | 立て直し計画v5 §12の配置更新停止に該当し、主要案内8文書に`reviewcompass3-trusted-transport`の直接案内がない | 観測対象のホスト配置状態は実行しておらず未確認 |
| Issue Resolution早期Pilot | 初期開発チェックリストの過去工程 | `issue_resolution_pilot.py`の旧Plan・Challenge・Verdict経路 | `.reviewcompass/workflow/`の旧形式と多数のEvidence | `.reviewcompass/workflow/`、`records/development/` | 機械処理とHuman判断 | `履歴のみ` | 早期Pilotは完了記録として保持され、立て直し中の作業順はv5が置換した | 開発用Issue受付として現役の部分は別行に分離済み |
| 過去の抽出・評価・再利用試行 | `docs/README.md`の生成元・設計資料 | `tools/extraction/`、Work 4A/4B関連処理、各種実験record | extraction 23ファイル、記録と試験 | `records/extraction/`、`records/development/` | 主に履歴参照。現在入口への接続なし | `履歴のみ` | 立て直しv5は第1段で現在位置を作り、第2段で資産を選ぶ。旧作業順をそのまま現役にしない | 第2段の採用条件で個別評価する |
| パッケージ導入 | `pyproject.toml`と`setup.py` | Python package install | `setuptools`、console scripts | 環境のscript配置 | 機械接続候補 | `未確認` | `pyproject.toml`は7入口、`setup.py`は2入口だけを宣言し、入口集合が一致しない。実際の導入は実行していない | 採用する一つのpackage正本と、生成される入口集合を確認する |

## 5. 古い記述または競合

1. 【実測】観測対象の`README.md`は「第5段の設計・ブートストラップ適合性監査までの候補成果」を
   現在地とし、次に最小E2E縦切りへ進むと案内する。採用済み立て直し計画v5は第1段から作業順を
   置き換えるため、この現在地表示は古い。
2. 【実測】観測対象の`TODO_NEXT_SESSION.md`は、無工具Claude疎通の範囲固定v3と失敗するテストの
   開始判断を次作業とする。同じ観測対象に採用された立て直し計画v5 §12は、未完了の実送信、認証、
   応答解析、配置更新を第1段の分類まで使用停止とする。TODOは状態正本ではなく、この表示は古い。
3. 【実測】`docs/README.md`と`AGENTS.md`は立て直し計画v5を現在入口としており、上記二文書より
   新しい作業順を示す。案内文書間で現在位置が一致していない。
4. 【実測】`docs/current/`の三文書は名称に`current`を含むが、front matterは全て`provisional`かつ
   `promotion_required: true`である。名前だけで現役authorityと判断できない。
5. 【記録】`records/development/2026-08-10-review-protocol-overview-v1.md`は、レビュー部品と統括処理が
   実装・試験済みでも、closure、contract、厳格解析、triage等が運用へ未接続とする。コードの存在と
   現役の利用経路が一致しない。
6. 【実測】`pyproject.toml`のconsole scriptは7件、`setup.py`は2件である。どちらを導入の正本とするか、
   観測対象の案内だけでは確定できない。
7. 【実測】主要案内文書と`docs/development/prompts/`の計8文書では、`reviewcompass3-pilot`、
   `reviewcompass3-claude-implementation`、`reviewcompass3-claude-confirmation`、
   `reviewcompass3-review-plan`は直接案内される。一方、`reviewcompass3-session-logs`、
   `reviewcompass3-bootstrap-review`、`reviewcompass3-trusted-transport`はコマンド名による案内がない。

本作業では、これらの文書、設定、入口を修正していない。

## 6. 第2段へ渡す未確認範囲

1. 履歴保存：Gitと`records/`を現役入口として採ることは説明できる。Session Log群を最小信頼基盤へ
   採る場合は、案内、配置、private root、代表正常処理、未レビュー守り役コードを確認する。
2. コード管理：Gitは現役である。`.reviewcompass/`内の台帳と各検査器は、開発用暫定経路と製品候補を
   分け、未レビュー守り役Issueへの依存を確認する。
3. 試験管理：公式入口と版付き設定は接続している。第2段では、案内から実行しreceiptが作られる代表
   正常処理と、runner自身の誤合格を防ぐ独立根拠を確認する。
4. レビュー：第1〜第4段の人向け正規入口は立て直しv5 §6である。旧レビューコード群をそのまま
   現役にせず、必要最小限を選ぶ。作業担当と異なる実行単位による一回の完了レビューは維持する。
5. 製品本体：最初の製品向け処理、Task Contract、入口は未選定である。統合三文書は候補のままなので、
   第4段まで自動的にauthorityへ昇格しない。
6. LLM連携：外部送信、認証、応答解析、配置更新は使用停止を維持する。第2段で信頼基盤として必要に
   なった場合だけ、安全に使える一経路または人を介した一時経路を作業票へ固定する。

## 7. 機械処理の結果

合否は各コマンドを単独で実行した終了コードで確認した。以下の内容識別値は、末尾改行を含む列挙結果の
SHA-256である。

| 目的 | 実行内容 | 終了コード | 結果 |
| --- | --- | --- | --- |
| 追跡パス列挙 | `git ls-tree -r --name-only cc2f0476...` | 0 | 1,780件、SHA-256 `bb2b53ebbe2fe1f4e3663f5838e498019f6f49ba95c40a71a272594b9a10217e` |
| 対象期間のcommit件数 | `git rev-list --count c24e3b41^..cc2f0476` | 0 | 175件 |
| 対象期間の件名列挙 | `git log --reverse --format=%H%x09%s c24e3b41^..cc2f0476` | 0 | 175行、SHA-256 `aefdda6ea359ab96a0d8a620a0c4450c1d940040edef4ac6b354468b6435f617` |
| 対象期間の変更パス列挙 | `git log --format= --name-only c24e3b41^..cc2f0476`を固有化・整列 | 0 | 221件、SHA-256 `41f499b6c6fd208438179f2bb1005e8b4742080cd7d2cc13d324a0b0ee6f4705` |
| 公開scriptとmodule存在照合 | `pyproject.toml`の`project.scripts`を抽出し`git cat-file -e`で照合 | 0 | 7入口、対応module 7件すべて存在 |
| V4 Issue状態列挙 | `issues-v4/*.json`を観測対象から読込み | 0 | Issue 8件、すべて`registered` |
| 旧レビュー統括の運用呼出し反証 | `tools/`から`review_pipeline`の外部呼出しを`git grep` | 1 | 一致0件。試験側には1件存在するため、「運用へ未接続」という既存記録と整合 |
| 開始時作業ツリー | `git status --short --branch` | 0 | `main`、変更なし、`origin/main`より594 commit先行 |

参照した主要ファイルは観測対象コミットから`git show <commit>:<path>`で読んだ。主な内容識別値は次の
とおりである。

| path | 観測対象でのSHA-256 |
| --- | --- |
| `README.md` | `299e5ca658c452ec2d0fa354585ca5519b90f66d8d885fd62b0ea9c410b9c094` |
| `docs/README.md` | `9227fb0be525c06e74dc68d53eafd8ecc332786b9816d98b61cd092fcc081d07` |
| `AGENTS.md` | `fdff28a865371207dabefd7a3adaa251f0b39447b23bbdb6342b7f5e5d159993` |
| `TODO_NEXT_SESSION.md` | `c04a180081d142922c274061d5c8edfb3d1ba6519a2606a79f0b0b533943b4de` |
| `pyproject.toml` | `cc8750ef2c1a159504dc5c402df1223154d51ca36d807df424118f1f34f208a4` |
| `docs/development/2026-08-03-initial-development-checklist.md` | `4bf42b4bce858bdc2e299a08582e94411698db2e143a0af4b47840712756f38c` |
| `docs/development/2026-08-02-development-policy.md` | `08bea1f9d5937ba5c212512ad041a0d03583d743dcc27742ad77c8741a22ad1c` |
| `docs/development/work-review-protocol.md` | `b7eb8f08c7b3f585d64d163a7a2f93e758e57e830bb973cc2441bfadbc98a3df` |
| `records/development/2026-08-10-review-protocol-overview-v1.md` | `4baca7fa473dd9880598eb8742e7aa4705db435793352f7429988ddde607fb0d` |
| `.reviewcompass/workflow/issues-v4/issue-unreviewed-work-review-backlog-001--v1.json` | `a23f7c20101e610d7b828079b93f57f1d80cb6c7015f9408be3661e0ead00e14` |

## 8. 未実施と次の一作業

【未実施】コード、試験、設定、計画、TODO、既存記録は変更していない。主要入口を実行して使用可否を
確認していない。外部送信、認証、ホスト配置確認、全試験、全記録の精読、第2段の採用判断も行っていない。

【次】本成果物を作業担当と異なる実行単位が変更せずに一回だけ独立レビューする。確認対象は、資料範囲、
各分類のGit根拠、接続方法、入口導線、対象外の維持、第2段の入力としての有用性である。技術的判定が
`verified`となっても、第1段の完了は利用者が別に判断する。
