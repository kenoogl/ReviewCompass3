# レビュー実行体制の正式ツール化 統合検討 v1

- 記録日：2026-08-16
- 指示者：利用者（Human）
- 記録者：Claude
- 種別：利用者指示による検討の固定（後続契約定義の入力）。実装・契約採用は含まない
- 利用者の確定：「この統合検討で確定」（2026-08-16 chat）

## 0. 一枚要約（人向け）

ClaudeがCodexへレビューを依頼する既存の仕組み（Pilot起動・record正本方式）を、**Antigravity CLI（agy。旧Gemini CLIの後継）と
サブエージェントも起動先に選べる正式ツール**へ広げる。作る縦切りは3本——**A：依頼promptの
機械組み立て器、B：Reviewer起動アダプタ、C：prompt品質gate**——で、どの縦切りにも共通の
横串3観点（機械処理化・手続きの機械化・導線配備）を受入条件として入れる。判定基準
（work-review-protocol）は変えない。単一プロバイダ環境では独立性の段階（tier）を宣言して
Human受容の下でサブエージェントレビューを許す。

## 1. 利用者の指示（2026-08-16 chat・要旨）

1. Claudeパイロット（利用者はClaudeとだけ会話し、ClaudeがCodexへレビュー依頼・回答取得・提示）の
   既存の仕組みを、**CodexCLIに加えGeminiCLIも対象**にしたい。本sessionの手動Gemini中継の実績を踏まえる。
   （2026-08-16訂正：Gemini CLIは2026-06-18に提供終了。後継のAntigravity CLI（agy）を対象と読み替える。§9）
2. レビュー依頼の**プロンプト作成の改善**を、機械化目標record
   （`records/development/2026-08-16-external-review-preparation-mechanization-goal-v1.md`）を参考に図る。
   まずClaudeパイロットで開発し、後にCodexパイロット・Geminiパイロットも対応したい。
3. 3社アカウント所有が前提だが利便性が高く、Task Contract以外の自由文レビューにも使えるため
   **正式ツールとして実装**したい。
4. 追加検討：**単一プロバイダ環境**では独立性の多少の低下を許容し、**サブエージェントによるレビュー**も
   同じ枠組みで扱う。
5. 追加確認：機械化目標の元指示（**機械処理化・手続きの機械化・導線配備**）を検討へ含める。

## 2. 既存文書の分析（3層構造）

| 層 | 文書 | 現状 |
| --- | --- | --- |
| 判定基準（不変の層） | `docs/development/work-review-protocol.md` | 実行者非依存の順序・判定・比例原則。**本検討で変更しない** |
| 役割分担 | `docs/development/pilot-specific-claude-codex-collaboration.md`（現行入口）、`legacy-pilot-review-collaboration.md`（役割・risk表の設計資産） | pilot: claude／codexの非対称分担。§5.1機械検査・§5.2段階台帳・§5.4保存分離は多くが`specified_only` |
| 受け渡し経路 | `docs/development/pilot-driven-record-handoff.md`（codex exec起動・試運転成功）、`codex-claude-collaboration.md`（Human中継fallback） | 機械化済みはcodex exec経路のみ。**codexCLIはトークン枯渇で停止中** |

**含意**：Antigravity CLI（agy）・サブエージェントの追加は経路層だけの拡張で成立し、判定基準・役割規則は不変のまま。

## 3. 現在地と本sessionの実証【実測】

- 暫定Gemini体制（依頼record作成→利用者が手動でpath伝達→判定持ち帰り）を本sessionで**8回**実運用。
  Geminiはディレクトリ共有でのrecord直接読取り・digest照合（鮮度検査）・書込み（権限許可後）・
  実用水準の判定（契約009の指摘3件は全て正当）を実証した。
- 残る空白は**起動の機械化だけ**（headless起動できれば、handoff方式の固定起動promptを流用して
  Human運搬0回のGeminiレビューが成立する）。
- 5段手続き（自己レビュー→文脈整理→依頼作成→依頼点検→送信）を手作業で2周し、依頼promptの
  「効く構造要素」を実測で確立した：役割宣言／対象と固定（digest表）／開始時鮮度検査の埋め込み／
  対象に応じた反証点の類型／判定形式の固定（verdict語彙・blocking区別・未検査の明示要求）／
  判断済み・範囲外の列挙（蒸し返し防止）／事実の明示（誤指摘の予防）／実行環境の注意
  （書込み承認の許可指示）。

## 4. 設計概念：backend抽象と独立性tier

### 4.1 backend抽象

Reviewer起動先を`codex-cli`／`antigravity-cli`（agy）／`claude-subagent`（将来`codex-subagent`等）として抽象化する。
起動方法が違うだけで「依頼recordを読ませ→レビューさせ→判定を得る→事後照合」の流れは全backend共通。

### 4.2 独立性tier（3段）

| tier | Reviewerの形 | 前例 |
| --- | --- | --- |
| Tier 1 | 別プロバイダ（cross-provider） | 契約008の独立性検査、本sessionのGeminiレビュー |
| Tier 2 | 同一プロバイダ・別モデルのサブエージェント | pilot-specific §2.1のモデル交差（sol⇄terra） |
| Tier 3 | 同一プロバイダ・同一モデルの別会話状態 | Claude Code環境のサブエージェント |

- 独立性検査の一般化：契約008の「pilot≠宛先」二値検査を「tierの機械判定＋宣言」へ一般化する。
  単一プロバイダ環境では**機械が黙って緩めるのではなく、tierを判定・宣言し、その受容をHuman承認に置く**
  （008で確立した「限界の明示的受容」の型）。
- risk補強条件：`work-review-protocol.md` §5「同じモデル系のサブエージェントレビューをhighの唯一の
  独立oracleにしない」は不変。`high`ではTier 2/3に機械反証・決定的検査の併用を受入条件で義務づける。
- 判定recordへtierとmodel名をprovenanceとして記録し、後の再レビュー差し替え・stale判断に使う。

## 5. 縦切り3本（一括で作らない）

| 縦 | 内容 | 機械化目標の段 | 依存・特性 |
| --- | --- | --- | --- |
| **A：依頼組み立て器** | 5段手続きの型の機械化：§3の構造要素を固定形にした雛形生成＋機械検査（§5.1.1の7項目を流用：存在・commit済み・digest一致・必須項目・識別子・参照実在・囲み記号）＋`git check-ignore`検査 | (1)(2)(3) | **起動方式と独立**。手動運搬のままでも全レビューの品質が上がる |
| **B：Reviewer起動アダプタ** | backend切り替え起動＋独立性tier＋起動record・未加工出力保存＋事後照合（判定recordの単独commit・鮮度・根拠照合） | (5)(6)の入口 | 要事前走査（agy headless仕様・subagent実測）。codexCLI停止blockerの回避になる |
| **C：prompt品質gate** | 監査役・判定役の多周確認の自動化（pilot-specific §5.1.2の設計流用） | (4) | A・Bの後（Bのbackend抽象の上で自動周回） |

- AとBは直交し、どちらを先にしても他方を妨げない。**順序はHuman判断**（A先行＝品質を先に、
  B先行＝運搬の手間削減を先に）。
- 実装するbackendは段階化：最初は`antigravity-cli`（agy）＋`claude-subagent`（codex-cliは疎通回復後の
  追加縦切り。利用者決定により第1縦切りは`antigravity-cli`、第2縦切りは`claude-subagent`）。

## 6. 横串3観点（全縦切りの契約に入る共通要件）

### 6.1 機械処理化（LLM／機械の分担線）

| 工程 | 機械処理（決定的） | LLMに残る（意味） |
| --- | --- | --- |
| (1)自己レビュー | 対象digest固定・変更一覧の機械生成（§5.3流用）・checklist存在検査 | 反証の発想 |
| (2)文脈整理 | 判断済みDecision recordの機械列挙 | 蒸し返し不要事項の選定 |
| (3)依頼組み立て | 雛形生成・digest表自動計算・機械検査7項目 | 反証点の文案 |
| (4)品質gate | 検査再実行・所見識別子の全件照合 | 監査役・判定役の所見 |
| (5)起動 | 起動・起動record・鍵の環境渡し | なし（完全機械） |
| (6)判定取り込み | 判定recordの存在・単独commit・鮮度・根拠と実物の機械照合 | 判定要旨の確認 |

本sessionで毎回書き捨てのcommandとして打ったdigest計算・照合・全文検索が、固定入口へ昇格すべき
機械処理の実測一覧である。

### 6.2 手続きの機械化（既存G30導線へ載せる）

新しい状態機械を作らず、受入済みのG30運用契約実行（`reviewcompass3-operation-run`）の**操作として
登録**する二段構え（単体入口＋G30操作登録）。前例：G02 prepareの`one_item_review_prepare`。
工程の順序保証・入力束縛・実行記録はG30側の既存機構を使い、複製しない。pilot-specific §5.2の
実行段階台帳（`specified_only`）は一括実装せず、G30実行記録で不足が実測された時に縦切りで扱う。

### 6.3 導線配備（受入条件へ含める）

- 正式実行名：`pyproject`のscripts登録＋別の現在位置からの実行確認（G30・008の受入形式）
- 入口文書：`docs/development/prompts/`のrun入口＋`AGENTS.md` §1への入口1行（手順書は入口へ縮み、
  実体はtoolへ）
- 着地境界：依頼・判定recordは`records/session-handoffs/`（commit正本）。起動record・未加工出力は
  repo外私有領域とし、保存は`tools/bootstrap/raw_review_store.py`を再利用して複製しない
  （pilot-specific §5.4の明記どおり）
- 部品間受け渡し：G02 prepare（材料固定）→組み立て器の入力、判定取り込み→将来のG02 organize接続

## 7. 危険度と前提

- 危険度は`high`想定：repositoryを読めるagentのheadless起動＝実質の外部送信（課金・データ送出）。
  起動のHuman承認境界（都度か契約水準か）は各契約で定める（008の前例に倣う）。
- 要調査（契約定義前の事前走査）：Antigravity CLI（agy）のheadless実行仕様（非対話起動・sandbox／
  書込み権限・認証引き継ぎ・終了コードと出力の機械取得）、Claudeサブエージェントのレビュー一往復の実測
  （`claude_implementation_executor`の能力設定・認証遮断の設計を流用）、codexCLIトークン枯渇の現状。
- pendingとの関係：外部APIレビュー（契約008・009の経路の機械化）はpendingのまま。本検討のCLI／
  subagent経路はそれと別経路・補完関係であり、pendingの対象外として進める（利用者指示による新規取組）。

## 8. 次作業

1. 縦AまたはBの選択（Human判断）
2. 選択された縦の事前走査（5手順：所在特定・import元・digest固定の全文検索・接続点・一覧の一元化）
3. 契約候補v1の作成→5段手続き→独立確認（暫定Gemini体制）→採用判断→実装

【未実施】契約候補の作成、実装、既存文書の改定、事前走査。
（2026-08-16追記：縦Bの選択と事前走査は完了した。
`records/development/2026-08-16-vertical-b-reviewer-launch-adapter-prescan-v1.md`と同追補を参照）

## 9. 訂正履歴

- 2026-08-16：利用者提供の事実（Gemini CLIは2026-06-18に提供終了。後継はAntigravity CLI（agy））と
  実測（agy 1.1.13導入済み・headless旗一覧）に基づき、backend名`gemini-cli`を`antigravity-cli`（agy）へ
  訂正した（§0・§1-1注記・§4.1・§5・§7）。承認文言：「追補recordを作成し、統合検討recordもagyへ
  訂正して。契約候補v1は第1 backend＝agyで作成に進んで」（2026-08-16 chat）。実測の詳細は
  `records/development/2026-08-16-vertical-b-prescan-agy-addendum-v1.md`。§3の実証記録（手動Gemini
  中継の8回実運用）は歴史的事実としてそのまま維持する。
