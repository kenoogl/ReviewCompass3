# 縦B（Reviewer起動アダプタ）事前走査 v1

- 記録日：2026-08-16
- 指示者：利用者（Human）。選択文言：「縦Bを採用する。事前走査から進めて」（2026-08-16 chat）
- 記録者：Claude
- 種別：契約候補定義前の事前走査（5手順：所在特定・import元・Digest固定の全文検索・接続点・一覧の一元化）。契約定義・実装・既存文書の改定は含まない
- 範囲の基準：統合検討record §5-B・§6・§7（digestは§5の表）
- 基準commit：`930a81214f5cc7abb61732dc858c25dc78d735db`（HEAD・作業tree clean）

## 0. 一枚要約（人向け）

縦B（backendを切り替えてReviewerを起動し、起動recordと未加工出力を保存し、判定recordを事後照合する
アダプタ）の流用部品と接続点を機械走査で固定した。主要な発見は3つ。(1) **gemini CLIは本環境に未導入**で
あり、gemini-cli backendは導入（Human作業）とheadless仕様実測が前提になる。(2) **claude-subagent backendは
流用部品が揃っており即着手可能**である（実行器の認証遮断・起動設計、raw保存を流用でき、一往復の機構実測に
成功した）。(3) 独立性検査の既存実装は送信路内の二値検査だけであり、tier判定・宣言はアダプタ側の新設になる。

## 1. 手順1：所在特定【実測】

| 部品（統合検討§5-Bの流用対象） | 所在 | 役割 |
| --- | --- | --- |
| Reviewer起動の前例（claude headless） | `tools/development/claude_implementation_executor.py` | `--print`起動、道具・権限の固定、stream-json解析、model検証、認証遮断（`FORBIDDEN_AUTH_ENVIRONMENT`） |
| 未加工出力の不変保存 | `tools/bootstrap/raw_review_store.py` | `store_raw_executions`。上書き禁止・digest付与 |
| 保存入力の型 | `tools/bootstrap/review_execution.py` | `ReviewAssignment(name, provider, model, route)`と`ReviewExecution` |
| 独立性検査の前例（契約008） | `tools/external_review/send.py` 329-330行 | `pilot == destination`で`reviewer_not_independent`停止（二値検査） |
| G30操作登録 | `tools/operations/operation_contract_run.py` 36-64行・431-433行 | `_OPERATIONS`辞書への登録と`_run_part`分岐。前例`one_item_review_prepare` |
| 判定取込み・事後照合の前例 | `tools/development/pilot_collaboration.py`（`prepare`／`ingest`／`status`） | 起動record検証、監査・判定の正規化、保存検証 |
| 固定起動promptの型 | `docs/development/pilot-driven-record-handoff.md` §3 | 役割宣言・対象・record path・単独commit・停止指示。model名記載＝判定の由来（provenance） |
| 保存分離とraw store再利用の明記 | `docs/development/pilot-specific-claude-codex-collaboration.md` §5.4 | raw＝repo外保護領域。commitする判定recordには保存先種別・SHA-256・参照権限だけを記録 |
| 能力設定の型 | 同 §6.1 | CLI版・model・認証・道具・パス・上限等を1記録へ固定し、実測との差分で停止 |
| 判定基準（不変） | `docs/development/work-review-protocol.md` §5（143-144行） | 「同じモデル系のサブエージェントによるレビューをhigh risk作業の唯一の独立oracleにしない」 |
| 依頼recordの命名実例 | `records/session-handoffs/` | `2026-08-16-*-gemini-request-v*.md` 8件（本sessionの手動体制の実績） |
| 判定recordの着地規約 | `records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md` §2-2 | Claudeが判定recordへ転記・commit。冒頭へReviewer・model名・中継方式を記載 |
| 導線配備先 | `pyproject.toml` `[project.scripts]`（23-37行）、`AGENTS.md` §1、`docs/development/prompts/` | 統合検討§6.3の受入形式（scripts登録・run入口・入口1行） |

外部CLIの導入状況【実測】（確認コマンド：`command -v`、npm global一覧、`~/.local/bin`・
`/opt/homebrew/bin`・`/usr/local/bin`・`~/.nvm`配下の列挙）：

```text
gemini: MISSING（上記いずれの場所にも無し）
codex: present (/Users/keno/.local/bin/codex) codex-cli 0.147.0
claude: present (/Users/keno/.local/bin/claude) 2.1.220 (Claude Code)
```

## 2. 手順2：import元【実測】

確認コマンド：
`grep -rn -E "from tools\.bootstrap\.(raw_review_store|review_execution) import|import (raw_review_store|review_execution)|from tools\.development\.claude_implementation_executor import|claude_implementation_executor" --include="*.py" tools/ tests/`

- `raw_review_store`のimport元：`tools/bootstrap/review_pipeline.py`・`review_resume.py`・
  `review_response_parser.py`・`review_assurance.py`（いずれもbootstrapレビュー系）。アダプタからは
  呼び出しを追加するだけで、既存import元の変更は不要。
- `review_execution`のimport元：`review_pipeline.py`・`review_resume.py`・`review_assurance.py`・
  `raw_review_store.py`。
- `claude_implementation_executor`の参照元：`claude_implementation_confirmation.py`・
  `claude_implementation_route.py`・`tools/deployment/trusted_claude_transport.py`（38・46・53行で
  実行器fileを保護対象pathsとして列挙）・`tools/deployment/installed/trusted_review_send_dispatch.py`・
  tests 4群。**実行器は信頼済み配備の保護対象**であり、実行器本体を書き換える流用は配備側の再固定を
  誘発する（§7-4の契約論点）。

## 3. 手順3：Digest固定の全文検索【実測】

確認コマンド：
`for t in gemini サブエージェント subagent backend 独立性; do grep -ril --exclude-dir=.git --exclude-dir=.venv --exclude-dir=__pycache__ --exclude-dir=node_modules -- "$t" . | wc -l; done`

| 語 | 一致file数 |
| --- | --- |
| gemini | 49 |
| サブエージェント | 111 |
| subagent | 28 |
| backend | 22 |
| 独立性 | 42 |

- code層（`tools/`・`tests/`）の`gemini`一致は`tools/external_review/send.py`と
  `tests/test_external_review_send.py`の2件だけ（契約008・009のAPI送信路の`gemini-api` provider）。
  **gemini-cli向けのコードは存在しない**。
- `subagent|サブエージェント`のcode層一致は`tools/task_contract/execution.py`・
  `tools/development/pilot_collaboration.py`とtests 3件。残りはdocs（work ticket類）とrecordsである。
- 含意：縦Bの新設コードは既存名と衝突しない。契約候補が参照すべきfileは本走査で閉じ、§5のdigest表へ固定した。

## 4. 手順4：接続点【実測】

1. **G30操作登録**：`_OPERATIONS`への1 entry追加（`entry`・`input_names`・`argument_names`・
   `binding_positions`）。入力束縛・順序保証・実行記録はG30側の既存機構をそのまま使う。特殊分岐が
   必要な場合の前例は`_run_part`の`one_item_review_prepare`分岐（431-433行）。
2. **起動**：実行器の流用点＝`FORBIDDEN_AUTH_ENVIRONMENT`（42-49行）・`_child_environment`
   （189-210行）・`_arguments`（466-500行。`--print --safe-mode --tools --allowedTools
   --disallowedTools --permission-mode dontAsk --strict-mcp-config --disable-slash-commands
   --no-chrome --output-format stream-json --model`）・`_parse_stream`のmodel検証と
   `permission_denied`停止。
3. **保存**：`store_raw_executions(storage_root, attempt_id, executions)`。入力は`ReviewExecution`の
   組。アダプタはbackend出力を`ReviewAssignment(name, provider, model, route)`へ写像すれば再利用でき、
   保存処理を複製しない（pilot-specific §5.4の明記と一致）。
4. **独立性tier**：既存は`send.py`の二値停止のみ。tier判定（1／2／3）・宣言・Human受容の型は
   アダプタ側の新設。判定recordへのtier・model記載は`ReviewAssignment`のprovider・model欄と
   handoff §3のprovenance記載慣行を延長する。
5. **事後照合**：handoff §2-6の3点（新record commitが判定対象より後・変更pathがそのrecord 1件だけ・
   判定内容の機械照合）と、`pilot_collaboration.ingest`の検証構造（起動record検証・正規化・保存検証）が前例。
6. **着地**：依頼record・判定record＝`records/session-handoffs/`（commit正本。命名実例あり）。
   起動record・未加工出力＝repo外私有領域（raw storeの保存境界）。
7. **導線**：`pyproject` scripts登録→`docs/development/prompts/`のrun入口→`AGENTS.md` §1への入口1行。

## 5. digest表（契約候補v1の固定入力）【実測】

`shasum -a 256`の出力（基準commit時点）：

```text
c2384f3b17a7c59572548a9195eb89924c6f42f087fc2e736975c7d0b8fcd602  records/development/2026-08-16-review-tooling-formalization-study-v1.md
1a5fffc5792d17791f5c275b40183a0d4d076233d6d1b7a267cd91cf92174792  records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md
46a415eb630266e23a87562e6083f873e2fe9790acd34a6699f59b30aee0b45e  records/development/2026-08-16-external-review-preparation-mechanization-goal-v1.md
68421b3a7bc12b466f96682ec9f32ee16aaff5e7da18cf0aa5d2c83d5a26d2cc  tools/development/claude_implementation_executor.py
b2699d5e90a38012935b6a747d76254f650e847d4f1f3a1680d4281dc991fe40  tools/bootstrap/raw_review_store.py
e33b0190f2e42ddadcb88770700de07252f652fbac5df005e0852475924a5612  tools/bootstrap/review_execution.py
fcecb2e35ffca0b6341cd7e102c4e6f0dc8b7b5871c36d87b8eae0a07a8d0197  tools/external_review/send.py
7ce02906cf5be3c6976ed602488516bdd9c4331fbe6193d16a2eb60bcc170a08  tools/operations/operation_contract_run.py
86d7c6b3604e8a61976b9e793255dee44d8578d006672271a2e901b2d81b3eb6  tools/development/pilot_collaboration.py
eb999d29947f973edbf0700c5cff97ec3bb4a46cbc66119f63a0c9a9b1ea275f  docs/development/pilot-driven-record-handoff.md
aee8c8b72487e26395615c8442710b0695b035ec0aa129b4a777c6142864489d  docs/development/pilot-specific-claude-codex-collaboration.md
e768d32ed0a2b95fced5a744dd9b98734a2bc3b0c644f415af9dd508c5223d29  docs/development/work-review-protocol.md
6a71137ad109bd3680e1b1b87d159a82fd65072480de1f0fc14e31d0b4f36c0f  AGENTS.md
b56851fa65aa9b30a98413c059d385b97daa874fdea960c93c01c0cde26e69d3  pyproject.toml
```

## 6. claude-subagentレビュー一往復の実測【実測】

- 実施：Claude Code環境のサブエージェント（読取り専用・model haiku・新規会話状態）へ、対象record path
  と期待SHA-256を渡し、(1) 開始時鮮度検査（`shasum -a 256`の実行と照合）、(2) 内容確認1点、
  (3) 固定JSON形式での返答、を依頼した。書込み・commit・repo外送信はさせていない。
- 結果（最終応答のverbatim転記）：

```json
{
  "freshness": "match",
  "digest_observed": "c2384f3b17a7c59572548a9195eb89924c6f42f087fc2e736975c7d0b8fcd602",
  "finding": "縦B行の依存・特性列に「要事前走査（GeminiCLI headless仕様・subagent実測）」と明記。事前走査への言及あり",
  "verdict": "verified"
}
```

- 計測：所要約22秒、subagent消費約21,761 token、道具使用2回。
- 判明：新規会話状態のsubagentが、record直接読取り・機械digest照合（鮮度検査）・固定形式返答の一往復を
  完了できる。統合検討§7の要調査「Claudeサブエージェントのレビュー一往復の実測」のうち機構部分に相当する。
- 未測定：レビュー品質、多往復、判定recordの書込み作成。また本実測はClaude Code環境のAgent tool経由で
  あり、CLI headless起動（`claude --print`）そのものではない。CLI経路は契約内のRED・実装段階で
  実行器設計の流用として扱う。

## 7. 契約候補v1へ渡す論点（発見事項と推奨）

1. 【実測】gemini CLI未導入。**gemini-cli backendは「導入（Human作業）＋headless仕様実測」が前提**で
   あり、導入前に受入条件を固定できない。
2. 【実測】claude-subagent backendは流用部品が揃い、即着手可能。
3. 【推奨】第1 backend＝`claude-subagent`（Tier 3の判定・宣言・Human受容の型を同時に作る）、
   第2 backend＝`gemini-cli`（導入後の追加縦切り）。統合検討§5の「最初はgemini-cli＋claude-subagent」の
   段階化を環境実測に基づき順序具体化する案であり、採否はHuman判断。
4. 【実測】実行器は信頼済み配備の保護対象paths（`trusted_claude_transport.py`）。流用は「実行器本体の
   改変」ではなく「設計の抽出・新設」を基本とし、共通module化の要否は契約で決める。
5. 【記録】work-review-protocol §5の不変制約により、Tier 2／3をhigh riskの唯一の独立oracleにしない。
   契約の受入条件へ機械反証・決定的検査の併用を明記する（統合検討§4.2どおり）。
6. 【記録】codexCLIトークン枯渇の現状確認は外部起動を要するため本走査では未実施。codex-cli backendは
   統合検討どおり疎通回復後の追加縦切りとする。

## 8. 未実施

- 契約候補v1の作成、5段手続き、独立確認（暫定Gemini体制）、実装。
- gemini CLIの導入とheadless仕様の実測。
- codexCLIトークン残量の現状確認（外部起動を要するため）。
