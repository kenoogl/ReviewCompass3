# claude-subagent第2 backend（Tier 2／3受容機構）事前走査 v1

- 記録日：2026-08-17
- 指示者：利用者（Human）。選択文言：「claude-subagentの第2縦切りを採用する。事前走査から進めて」
  （2026-08-17 chat）
- 記録者：Claude
- 種別：契約候補定義前の事前走査（6手順。`docs/development/prompts/scope-prescan-run.md`の適用第2号）。
  契約定義・実装・既存文書の改定は含まない
- 範囲の基準：統合検討record §4.2（tier一般化の型）・§5（backend段階化）、契約010の範囲外
  （claude-subagent backend・Tier 2／3受容機構は第2縦切り）
- 基準commit：`3dc26788e861d6f383e2ad164313d9ee38e8b8eb`（HEAD・作業tree clean）

## 0. 一枚要約（人向け）

第2縦切り＝「backend登録形へ`claude-subagent`（同一プロバイダanthropic・Tier 3）を追加し、Tier 2／3を
機械が黙って許すのではなく**宣言＋Humanの明示受容がある場合だけ**起動を許す機構を作る」。主要な発見は
3つ。(1) **本縦切りは受入済み製品（縦B）の拡張契約になる**（前例：契約009が008の送信核を精密化）。
(2) **互換制約が2記号ある**：契約011（受入済み）が`ALLOWED_RESPONSE_MODELS`と
`verdict_record_relative_path`をimportしており、名称・意味を壊せない。(3) claude CLIの起動・stream解析は
**実行器に完全な前例**があり（読み取り専用の道具制限・model照合つき）、正式再利用検索でも直接一致54件
（`start_allowed: true`）。

## 1. 手順1：所在特定【実測】

| 部品・結合点 | 所在 | 状態 |
| --- | --- | --- |
| backend登録形（拡張対象） | `tools/reviewer_launch/core.py` 56行`BACKENDS`（現在agy 1件） | 定義は名・provider・executableのみ。引数組み立て（`build_arguments`）・stream解析（`_parse_stream`等）・許可model（41行`ALLOWED_RESPONSE_MODELS`）・禁止環境変数はagy固定で、**backend別化が必要** |
| tier判定（一般化対象） | 同 166-172行`judge_tier` | Tier 1以外は`reviewer_not_independent_tier`で無条件停止。宣言＋受容の枝が無い |
| g30 prepare操作のbackend固定 | `tools/reviewer_launch/entry.py` 86-87・108行 | `antigravity-cli`を直書き。126行のlaunch既定も同様 |
| claude CLI起動の前例 | `tools/development/claude_implementation_executor.py` | `_arguments`（466行〜。--print・--safe-mode・--tools・--allowedTools・--permission-mode dontAsk・--strict-mcp-config・stream-json・--model）、`ALLOWED_TOOLS`（21行。Read系＋Edit/Write——**レビュー用はRead系だけへ絞る**）、`FORBIDDEN_AUTH_ENVIRONMENT`（42-49行。ANTHROPIC系6種）、`_child_environment`（189行〜） |
| claude streamの解析前例 | 同 `_parse_stream`（302行〜） | type/system系event・model検証・permission_denied停止。**agyのevent形式と別**のためbackend別parserが必要 |
| claude CLIの現況 | `claude` 2.1.220【実測・helpのみ】 | `--print`・`--output-format stream-json`・`--allowedTools/--disallowedTools`・`--permission-mode`・`--model`・`--safe-mode`・`--disable-slash-commands`・`--no-chrome`の実在を確認。`--json-schema`相当は無し（構造化はprompt指示＋抽出で担保＝実行器前例） |
| Tier 2の前例 | `docs/development/pilot-specific-claude-codex-collaboration.md` §2.1 | モデル交差（sol⇄terra）＝同一プロバイダ・別modelの型 |
| 不変制約 | `docs/development/work-review-protocol.md` §5（143-144行） | 同一モデル系サブエージェントを`high`の唯一の独立oracleにしない→契約の受入条件で機械反証・決定的検査の併用を義務化（統合検討§4.2） |
| 受容の型の前例 | 契約008の「限界の明示的受容」（独立性二値検査）、契約010 §4.2表 | tierを判定・宣言し、受容をHuman承認に置く |

## 2. 手順2：import元【実測】

`tools.reviewer_launch`のimport元は4 file：`tools/operations/operation_contract_run.py`（g30登録）・
`tools/request_builder/core.py`・`tests/test_reviewer_launch.py`・`tests/test_request_builder.py`。

- **互換必須の公開記号**（契約011＝受入済み製品が使用）：`core.ALLOWED_RESPONSE_MODELS`
  （依頼recordの許可model検査の基準。tuple意味を維持する必要——per-backend化する場合は
  「全backendの許可modelの和集合」への一般化が有力）と`record.verdict_record_relative_path`（不変）。

## 3. 手順3：Digest固定の全文検索【実測】

| 語 | 一致file数 |
| --- | --- |
| claude-subagent | 13 |
| サブエージェント | 113 |
| Tier 2 | 9 |
| Tier 3 | 3 |
| tier | 26 |

- code層のtier実装は`tools/reviewer_launch/`（3 file）とその試験だけ。**拡張は縦B内に局所化**できる。

## 4. 手順4：接続点【実測】

1. **拡張契約の形**：契約012は受入済み縦B製品の変更を変更上限へ含む拡張契約（前例：009→008）。
   契約011の成果物（request_builder）は不変のまま互換を保つ。
2. **backend登録形の拡張**：backend定義へ「引数組み立て・stream解析・許可model一覧・禁止環境変数・
   requested model」の別を持たせる（agyの現行値は不変のまま移設）。
3. **tier受容機構**：`judge_tier`を「Tier 1＝従来どおり許可／Tier 2・3＝明示受容の入力がある場合だけ
   許可し、宣言をlaunch record・判定recordへ記載（既存の記載機構を流用）／受容が無ければ従来どおり
   停止」へ一般化。受容の機械形（起動引数での明示か、契約水準の常時受容か）は契約論点。
4. **claude起動**：実行器`_arguments`の設計流用。レビュー用は読み取り専用（`Read`系のみ・Edit/Write無し・
   `--permission-mode dontAsk`は書込み道具が無い前提で安全）。認証遮断は実行器の6種を流用。
5. **stream解析**：実行器`_parse_stream`前例のbackend別parser化。構造化判定はprompt指示＋JSON抽出
   （`--json-schema`相当が無いため）で、schema検証は既存`validate_verdict`を共用。
6. **g30 prepare**：backend固定（entry 86-108行）の引数化または既定維持（契約論点）。
7. **回帰**：縦B対象35件・契約011対象32件の全緑維持が受入条件。agy経路の実E2E再確認の要否は契約論点
   （外部送信を伴うため）。

## 5. 手順5：正式再利用検索【実測】

- 作業別計画（schema 2・能力5件）：
  `records/development/2026-08-17-claude-subagent-backend-reuse-search-plan-v1.json`（commit `57b9200`）
- 一操作入口の結果：`status: completed`・HEAD `57b9200…`・**`start_allowed: true`**・直接一致54件・
  手掛かり一致281件。証明書：
  `records/development/2026-08-17-claude-subagent-backend-reuse-search-attestation-v1.json`
  （commit `3dc2678`）
- 直接一致の要点：起動＝実行器`_arguments`／`_child_environment`＋縦B`launch_review`、解析＝実行器
  `_parse_stream`＋縦B抽出3関数、tier＝縦B`judge_tier`＋送信路の独立性検査、認証遮断＝縦B
  `_child_environment`。lifecycle・再利用方法の裁定はHumanへ残る（契約候補で扱う）。

## 6. digest表（契約候補v1の固定入力）【実測】

```text
d2c8130a0e6d3a8aab351225e7218931d405463f24ed3e84a06e835e421bd913  tools/reviewer_launch/core.py
998c31d726c3aa37bd5021d83495590ad49015916ab4ca0572890465e495db8d  tools/reviewer_launch/record.py
e7f6a71ef529a84f888a02635dae2aa19cea7c088672f7f1def56ddaa85bd0a7  tools/reviewer_launch/entry.py
8e0b5b9fb3422845b95771b69aecdb2734e3636f2ae694a751539c25ccdf1ef4  tools/request_builder/core.py
68421b3a7bc12b466f96682ec9f32ee16aaff5e7da18cf0aa5d2c83d5a26d2cc  tools/development/claude_implementation_executor.py
27e47832ddc52eeaccffacb73d152ef6ff74f9eaff8b2cfcee056d0766b1d933  tools/operations/operation_contract_run.py
aee8c8b72487e26395615c8442710b0695b035ec0aa129b4a777c6142864489d  docs/development/pilot-specific-claude-codex-collaboration.md
e768d32ed0a2b95fced5a744dd9b98734a2bc3b0c644f415af9dd508c5223d29  docs/development/work-review-protocol.md
be5b8be64aebbdb27c52b1933e2b06adbf3f492ffef523472e774e10419a532b  records/development/2026-08-17-claude-subagent-backend-reuse-search-plan-v1.json
bc37a5be2e2e182cd76985114f5ae9156039e5475282b1f2adf35c41feba230b  records/development/2026-08-17-claude-subagent-backend-reuse-search-attestation-v1.json
7d159fdf093abad81481ae73eb3d95ad11efd04e2313d6df5a34c27fe583db0a  records/task-contract/2026-08-16-reviewer-launch-adapter-candidate-v2.md
78adb15fc84be82acf8a934a1673370d1ccd45c69805d12ed924e6320288d516  records/development/2026-08-17-reviewer-launch-adapter-product-acceptance-decision-v1.md
146344498d7c5ce3c228a9eccb5f7a985f260691589688b6447385236273c6a1  records/task-contract/2026-08-17-request-builder-candidate-v3.md
```

## 7. 契約候補v1へ渡す論点（発見事項と推奨）

1. 【実測】互換の取り方：`ALLOWED_RESPONSE_MODELS`は**全backend許可modelの和集合として維持**を推奨
   （契約011のimportと検査意味が無変更で保たれる）。backend別のrequested modelは登録形の中へ。
2. 【記録】tier受容の機械形：**起動引数`--accept-tier <2|3>`の明示がある場合だけTier 2／3を許可**し、
   受容の根拠（利用者文言のrecord）をlaunch recordへ記載する案を推奨。契約水準の常時受容は
   採用判断で選べる形に。
3. 【判断】subagentの許可model：Tier 3（同一model系の別会話）かTier 2（別model。sol⇄terra型）かは
   利用者承認で確定（実E2E前。契約010の許可model承認と同じ型）。
4. 【実測】構造化出力：claude CLIに`--json-schema`相当が無いため、prompt指示＋出力JSON抽出（実行器
   前例）で担保し、schema検証は既存`validate_verdict`を共用する。
5. 【判断】回帰確認の深さ：縦B・縦A対象試験の全緑は必須。agy経路の実E2E再確認（外部送信1回）を
   受入条件へ含めるかは契約で確定。
6. 【記録】`high` risk作業でTier 2／3を唯一の独立oracleにしない不変制約を、受入条件へ機械反証・
   決定的検査の併用義務として明記（統合検討§4.2どおり）。

## 8. 未実施

- 契約候補v1（契約012）の作成、5段手続き、独立確認、実装。
- claude subagentの実起動（契約内の承認付き実測へ送る）。
