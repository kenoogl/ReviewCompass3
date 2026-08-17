# claude-subagent第2 backend（Tier 2／3受容機構） 作業契約候補 v1

- 契約ID：`TC-RC3-PRODUCT-CLAUDE-SUBAGENT-BACKEND-012`
- 契約版：1
- 契約種別：受入済み縦B製品（契約010）の拡張縦切り（前例：契約009による008送信核の精密化）
- 状態：`candidate_pending_independent_review`
- 作成日：2026-08-17
- 直前の製品契約：`TC-RC3-PRODUCT-REQUEST-BUILDER-011 / v3`（受入済み）
- 入力：統合検討record §4.2・§5（agy訂正済み）、claude-subagent第2 backend事前走査v1、正式再利用検索
  （計画・証明書・start_allowed true）、利用者指示「claude-subagentの第2縦切りを採用する。事前走査から
  進めて」「契約候補v1（契約012）を作成して」（いずれも2026-08-17 chat）
- 実装状態：未開始
- 危険度：高
- 危険の理由：headless起動（実質の外部送信・課金）の対象を広げることに加え、**独立性の受容機構という
  レビュー統治の中心**に触れる。誤実装は「機械が黙って独立性を緩める」事故に直結する

## 1. 位置と縮小境界

【記録】縦B（契約010）はTier 1（別プロバイダ）だけを許可し、それ以外は無条件停止する。単一プロバイダ
環境や2 oracle突き合わせのためには、Tier 2／3（同一プロバイダ）の**宣言＋Human明示受容**の型
（統合検討§4.2。契約008の「限界の明示的受容」の型）が必要である。

【判断】本契約は第2縦切りとして、次だけを行う。

- backend登録形を**backend別定義**（provider・executable・宣言tier・引数組み立て・stream解析・
  許可model・禁止環境変数・requested model）へ拡張し、agyの現行値を**不変のまま移設**する。
- `claude-subagent` backend（provider `anthropic`・executable `claude`・**宣言Tier 3**）を1件追加する。
  Tier 2／3の区別は保守側へ倒し、同一プロバイダbackendは別modelを選んでも宣言Tier 3として扱う。
- tier判定を一般化する：Tier 1＝従来どおり許可。Tier 2／3＝**明示受容の入力がある場合だけ**許可し、
  宣言と受容根拠をrecordへ記載。受容が無ければ従来どおり`reviewer_not_independent_tier`で停止
  （既定の挙動は変えない）。
- 判定・転記・事後照合・G30登録・導線は既存のまま流用する（新設しない）。

## 2. Human承認境界

- 起動の起点は利用者のchatによるレビュー実施指示（契約010 §2の踏襲。起動ごとの追加承認手続きなし）。
- **Tier 2／3の起動はさらに明示受容を要する**：起動引数`--accept-tier <2|3>`が宣言tierと一致する場合
  だけ起動できる。受容の根拠（利用者の受容文言のrecord参照）を起動recordへ記載する。契約水準の常時
  受容へ緩めるかは将来のHuman判断とし、本契約では起動ごとの明示を既定とする。
- 機械層の守り：読み取り専用（Read系道具のみ・書込み道具を渡さない）・固定引数・commit済み依頼record
  だけ・byte上限・自動再試行なし・別model／別認証／別経路への自動切替なし（すべて契約010の型）。
- 契約内の初回実起動（§9-8）は利用者の明示指示＋Tier 3受容の明示を得てから行う。

## 3. 権威、証拠

| 役割 | path | SHA-256 |
| --- | --- | --- |
| 事前走査v1（6手順・結合点・論点） | `records/development/2026-08-17-claude-subagent-backend-prescan-v1.md` | `2939237e6e2435ba05561281a4dcf09c977bb77ee5e136d9f1802ab47bd548e2` |
| 正式再利用検索の作業別計画 | `records/development/2026-08-17-claude-subagent-backend-reuse-search-plan-v1.json` | `be5b8be64aebbdb27c52b1933e2b06adbf3f492ffef523472e774e10419a532b` |
| **正式再利用検索の証明書（start_allowed: true）** | `records/development/2026-08-17-claude-subagent-backend-reuse-search-attestation-v1.json` | `bc37a5be2e2e182cd76985114f5ae9156039e5475282b1f2adf35c41feba230b` |
| 統合検討（tier一般化の型§4.2・利用者確定） | `records/development/2026-08-16-review-tooling-formalization-study-v1.md` | `00b294afefa90de8cc8dc5141e9d08c23d40971d4338b9ca5021fe857f2daae0` |
| 拡張対象の契約010候補v2（受入済み） | `records/task-contract/2026-08-16-reviewer-launch-adapter-candidate-v2.md` | `7d159fdf093abad81481ae73eb3d95ad11efd04e2313d6df5a34c27fe583db0a` |
| 契約010の製品受入判断 | `records/development/2026-08-17-reviewer-launch-adapter-product-acceptance-decision-v1.md` | `78adb15fc84be82acf8a934a1673370d1ccd45c69805d12ed924e6320288d516` |
| 互換維持対象の契約011候補v3（受入済み） | `records/task-contract/2026-08-17-request-builder-candidate-v3.md` | `146344498d7c5ce3c228a9eccb5f7a985f260691589688b6447385236273c6a1` |

流用部品のcode・文書のdigestは事前走査v1 §6の表を正とする（固定commit時点の差分0を§9-9で確認する）。

## 4. 実装方法の3案

| 案 | 内容 | 判断 |
| --- | --- | --- |
| A 最小（既存機能のみ） | subagentレビューを人手で別session起動して運用する | 機械化なし・運搬と転記が手作業へ戻る。tier受容も口頭運用になり「黙って緩める」統制が作れない。不採用 |
| B backend登録形の拡張＋tier受容 | backend別定義へ一般化しclaude-subagentを追加。`judge_tier`を宣言＋明示受容の型へ一般化。互換記号は和集合として維持 | 変更が縦B内に局所化し、agy経路は値の移設だけで無変更。事前走査の直接一致54件をそのまま流用。推奨 |
| C 第2アダプタの新設 | 実行器設計を流用したsubagent専用アダプタを縦Bと並置する | 保存・転記・照合・導線が複製になり、縦Bのbackend登録形の設計意図に反する。不採用 |

## 5. 範囲

### 5.1 範囲内

1. **backend登録形の拡張**：backend定義を「provider・executable・宣言tier・引数組み立て関数・
   stream解析関数・許可model一覧・禁止環境変数一覧・requested model」へ一般化し、agyの現行値を
   不変のまま移設する（agy経路の既存試験は無変更で緑を維持）。
2. **claude-subagent backendの追加**：固定引数は実行器`_arguments`の設計流用で、読み取り専用へ絞る
   （§7.2）。stream解析は実行器`_parse_stream`の設計流用でclaude形式のmodel照合とJSON抽出を行う。
3. **tier受容機構**：`judge_tier`の一般化（Tier 1許可／Tier 2・3は`--accept-tier`一致時のみ許可・
   不一致と欠落は従来どおり停止）。宣言tier・受容根拠を起動recordへ、宣言tierを判定recordへ記載
   （記載機構は既存流用）。
4. **互換の維持**：`ALLOWED_RESPONSE_MODELS`は**全backend許可modelの和集合**として名称・tuple意味を
   維持（契約011の検査を無変更で保つ）。`verdict_record_relative_path`は不変。
5. **subagent許可model**：空の直書き定数で開始し（空の間はsubagent起動を`allowed_models_unfixed`で
   停止）、実E2E前に利用者承認recordで値を確定して固定する（契約010と同型）。
6. **対象試験（RED先行）**と、利用者指示＋Tier 3受容明示による実E2E 1回（§9-8）。
7. g30 prepare入口へ`--backend`任意引数を追加（既定`antigravity-cli`は不変）。

### 5.2 範囲外

- codex-cli backend（疎通回復後の追加縦切り）。縦C（合議・判定record比較の上位層）。自由文類型。
- 判定不一致時の自動裁定（2 oracleの不一致はHuman裁定。合議の機械化は縦C）。
- 転記・事後照合・保存・G30登録・導線の変更（既存流用）。契約011成果物（request_builder）の変更。
- 外部API直接送信経路の後続（pendingのまま）。歴史的recordの書き換え。

## 6. 固定再利用部品と保護基準

保護基準commitは本候補の固定commitとする。次を変更しない：`tools/request_builder/`（契約011成果）・
`tools/bootstrap/`・`tools/session_logs/redaction.py`・`tools/common/digests.py`・
`tools/development/claude_implementation_*`（実行器4 file。設計流用のみで本体不変）・
`tools/external_review/send.py`・egress・`tools/operations/operation_contract_run.py`・受入済み製品試験
のうち`tests/test_request_builder.py`。変更してよいのは§8の上限だけである。

## 7. 中心的な取り決め

### 7.1 backend別定義の固定形

backend定義は直書きの契約固定定数とし、設定file・環境変数・引数から追加・変更できない。agy定義の
値（引数・prompt・許可model・禁止環境変数）は本契約で一切変えない（移設のみ）。

### 7.2 claude-subagentの起動固定形

- 固定引数（実行器の設計流用・読み取り専用へ縮小）：`--print`・`--output-format stream-json`・
  `--tools Read,Glob,Grep`（**Edit・Write系を含めない**）・`--allowedTools Read(/**)`・
  `--disallowedTools`（実行器の禁止一覧を流用）・`--permission-mode dontAsk`・`--strict-mcp-config
  --mcp-config {"mcpServers":{}}`・`--disable-slash-commands`・`--no-chrome`・`--model <許可model>`・
  prompt（縦Bの固定prompt生成を流用。末尾位置引数）。
- 認証遮断：anthropic系6種（`ANTHROPIC_API_KEY`・`ANTHROPIC_AUTH_TOKEN`・`ANTHROPIC_BASE_URL`・
  `ANTHROPIC_FOUNDRY_API_KEY`・`ANTHROPIC_VERTEX_PROJECT_ID`・`AWS_BEARER_TOKEN_BEDROCK`）を
  **本契約の直書き定数**として宣言し（由来：実行器`FORBIDDEN_AUTH_ENVIRONMENT`。同値性を試験で固定）、
  検出時は起動前に停止する。認証は利用者のsubscription（`claude`ログイン状態）だけを使う。
- 構造化判定：claude CLIに`--json-schema`相当が無いため、prompt指示＋出力からのJSON抽出で担保し、
  schema検証は既存`validate_verdict`を共用する。抽出不能・不適合は`verdict_schema_nonconforming`で
  停止（raw保存済み）。

### 7.3 tier宣言と明示受容

- 機械判定：backend providerがpilot provider（`anthropic`固定）と異なればTier 1。同一なら
  backend定義の宣言tier（claude-subagentは3）。
- Tier 2／3は、起動入力`--accept-tier`が宣言tierと一致する場合だけ起動を許す。欠落・不一致は
  `reviewer_not_independent_tier`で停止（既定挙動の不変）。
- 起動recordへ宣言tier・受容入力・受容根拠（利用者文言のrecord参照）を記載し、判定record冒頭の
  tier記載（既存）と併せて由来を固定する。
- **不変制約**：`high` risk作業でTier 2／3を唯一の独立oracleにしない（work-review-protocol §5）。
  本契約の完了レビュー自体もagy（Tier 1）で行う（§9-10）。

### 7.4 残余risk（明示的に受容を諮る）

1. **Tier 3の独立性は限定的**：同一model系の別会話状態であり、見落としの相関が残り得る。緩和：
   唯一oracle禁止の不変制約＋機械反証・決定的検査の併用＋判定recordへのtier明記（stale判断可能）。
2. claude CLI仕様変更への追随risk（agyと同型。実挙動は実測が正）。緩和：安全側停止・raw完全保存。
3. subagent起動もanthropicへの内容送出を伴う。ただし操縦Claude自身が同一provider下で常時repository
   を読んでおり、**新規の露出先は増えない**（事実の明示）。緩和：起点は利用者指示・起動record台帳。
4. 2 oracleの判定不一致時の裁定は手動（Human）。合議の機械化は縦Cまで持ち越し。

## 8. 変更上限

1. `tools/reviewer_launch/core.py`（backend別定義への一般化・claude-subagent追加・tier受容）。
2. `tools/reviewer_launch/entry.py`（`--accept-tier`・g30 prepareの`--backend`任意引数）。
3. `tools/reviewer_launch/record.py`（起動record・転記への受容根拠記載が必要な場合の最小変更）。
4. `tests/test_reviewer_launch.py`（既存caseを維持したまま拡張）。
5. `docs/development/prompts/reviewer-launch-run.md`への追記（subagent起動とtier受容の使い方）。
6. Evidence、独立確認、受入判断、TODO更新。

## 9. 受入条件

実装開始後は失敗試験を先に固定し、期待どおり失敗してから最小実装を行う。

1. RED：backend別定義の一般化・tier受容（欠落／不一致停止・一致許可）・claude固定引数（読み取り専用・
   禁止道具不在）・認証遮断6種・claude stream解析（model照合・JSON抽出）・和集合互換の失敗試験を
   先に固定する。
2. agy互換：backend一般化後も**agy経路の既存試験caseが無変更で全緑**（値の移設だけであることの機械証明）。
3. tier受容：`--accept-tier`欠落・不一致でclaude-subagent起動が従来理由で停止し、一致時だけ起動へ進む。
   起動recordへ宣言tier・受容根拠が記載される。
4. claude固定引数：Read系のみで書込み道具・`--dangerously-skip-permissions`類が組み立てに存在しない
   （両向き試験）。
5. 認証遮断：6種の自前定数が実行器定数と同値（試験固定）で、存在時は起動前停止。
6. stream解析：claude形式の合成streamでmodel照合（許可外停止・raw保存）とJSON抽出・schema検証
   （不適合停止）が両向きで働く。
7. 互換：`ALLOWED_RESPONSE_MODELS`が和集合として維持され、**契約011対象32件が無変更で全緑**。
8. 実E2E 1回：利用者の明示指示＋Tier 3受容の明示の下、subagentで実対象1件（本契約の完了レビュー依頼
   record）のレビュー一往復を実環境で行う。**同一対象へのagy正式完了レビュー（§9-10）と並ぶ、初の
   2 oracle比較データを取得**する。不成立なら停止し、自動再試行・自動切替をしない。
9. 既存試験：縦B拡張後の対象試験・契約011の32件・G30 75件・正規全試験（禁止認証隔離条件）が各単独
   終了コード0。§6保護対象が基準commitから差分0。
10. 完了レビュー：**agy経路（Tier 1）**で実施し、`verified`系（blocking 0件）を得る（依頼recordは
    契約011の正式経路で組み立てる）。
11. 利用者が§7.4残余risk 4点を確認して製品処理を受け入れる。

## 10. 停止条件

- claude CLIのheadless起動が読み取り専用の固定引数で成立しない。
- 互換が保てない（契約011対象試験またはagy経路既存caseの変更が必要になる）。
- §6保護対象の変更が必要になる。
- 対象・関連・正規全試験または独立確認が不合格になる。

## 11. 影響、未実施、次作業

【判断】受入後は、同一依頼recordを**agy（Tier 1）とclaude-subagent（Tier 3・明示受容つき）の2 oracle**へ
投げる突き合わせが可能になり、単一プロバイダ環境でもレビューが回る。判定不一致の機械合議（縦C）と
codex復活時の第3 backendは、この登録形の上に載る。

【未実施】契約採用、実装、subagentの実起動、既存成果物の変更。

次は本候補の固定commit後、自己レビュー（5段手続き第1・2段）→依頼record組み立て（契約011の正式経路）→
機械検査→独立確認（agy headless起動。起動は利用者の明示指示による）→採用判断の順で進める。
