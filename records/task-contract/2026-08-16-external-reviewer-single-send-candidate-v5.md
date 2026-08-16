# 外部レビュア一回送信の最小経路 作業契約候補 v5

- 契約ID：`TC-RC3-PRODUCT-EXTERNAL-REVIEWER-SINGLE-SEND-008`
- 契約版：5
- 契約種別：製品処理・G20（外部送信安全境界）の最初の縦切り
- 状態：`candidate_corrected_pending_human_approval`
- 作成日：2026-08-16
- 直前の製品契約：`TC-RC3-PRODUCT-ONE-ITEM-REVIEW-SAFE-PROJECTION-007 / v2`（受入済み）
- supersedes：`records/task-contract/2026-08-16-external-reviewer-single-send-candidate-v4.md`、SHA-256 `e41acfdf0ceb1f8cff0c112d21181cd60a856345de6b38e90e89d3aafa161325`
- 訂正根拠：実装開始後に発見した契約内矛盾。§11はnew moduleを`tools/egress/`配下へ置くと固定するが、
  §12.11が成功を要求する既存の敵対試験`tests/test_egress_adversarial.py`は「`tools/egress/`配下に通信手段が
  存在しない」（段階1の不変条件）を全fileへ検査するため、両立しない。既存試験の書換えはHuman承認事項の
  ため実装を停止した
- 訂正範囲：§11の置き場所だけを新package`tools/external_review/`へ変更（送信核・入口・対象試験の3 path）。
  旧egressの段階1不変条件（送信は型として不可能）は無傷のまま保たれ、承認済み送信路は本契約の管理下の
  別packageに住む。安全境界・schema・検査・台帳の定義は一切変更しない
- 利用者判断：2026-08-16の候補5（G20）選択、暫定Geminiレビュー体制、三帯方式の議論を経た
  「送信ごとの人の確認なし」設計の決定、宛先切り替えの指示
- 実装状態：未開始
- 危険度：最高
- 危険の理由：本repositoryで初めて通信（外部送信）と認証情報の環境値解決を持つ。送信は不可逆で、
  誤送信は取り消せない
- 内容識別値：本候補固定後、独立確認と利用者判断記録から参照する

「送信指示」は、利用者の指示の下でClaudeが用意する、一回の送信を指示する入力JSON一件である。
「送信台帳」は、送信の試行と応答を機械記録する、出力rootに着地するrecord群である。
「正準JSON」は、key昇順、区切り前後の空白なし、UnicodeをUTF-8の文字として保持する固定表現である。

## 1. 位置と縮小境界

【記録】G20は送信先・内容・目的・承認を結び、許可範囲だけを外部へ送る候補である。既存の暫定実装
（`tools/egress/`7 module、関連試験107件）は、送信係が「型として送信不可能」の段階1で保留されている。

【判断】本契約はG20全体ではない。**契約固定の送信規則の下で、commit済みfile由来のpayload一件を
外部レビュアAPI（3 providerから切り替え）へ一回送信し、未加工応答を保存し、送信台帳を着地させる最初の縦切り**である。

- 既存egress 7 moduleは変更しない。旧設計（出口設計v4）の3種payload型制限・関門との統合は後続契約で扱う。
- 応答の解析・整理（G02 organizeへの接続）、複数送信の一括、抜き取り監査の自動化、他宛先は行わない。
- 本契約の受入だけでは候補5（G20）を完了にしない。
- この縮小境界を採るかは、独立確認後に利用者が契約採用と同時に判断する。

## 2. Human承認境界（本契約の中心的な取り決め）

【記録】利用者は2026-08-16、次を決定した。

1. **送信ごとの人の確認は行わない**。従来のcodex exec方式（repository全域を読める外部agentを
   起動し、内容の確認なしにOpenAI APIへ送っていた）と同水準の運用とし、内容の守りは機械層に置く。
2. **行為の起点は利用者の指示**とする。送信は、利用者がchatで指示した作業（レビュー依頼など）または
   明示の自律実行指示の中でだけ起きる。Claudeが指示なく自発的に送ることを禁止する。
3. 外部送信のHuman承認は、**本契約の採用判断と、都度の作業指示の水準**で満たす。

【判断】この取り決めにより、機械層（§7〜§9：機微検査・path範囲・digest束縛・台帳・上限）が内容の守りの
実体であり、人の関与は契約採用・作業指示・事後の台帳確認・失効指示に置かれる。

**技術で防げない限界（原因3）**：操縦LLMと本moduleは同一のOS権限で動くため、着地後の台帳fileを操縦LLMが
削除・改名して不可視化する隠蔽は、権限分離を持たない本製品の機械層では防げない。緩和は、(1)台帳をcommitに
含める運用によりgit履歴へ残ること、(2)Humanによる台帳・履歴の事後確認、(3)権限分離の導入（後続のHuman判断）
である。この限界は操縦LLMの自己申告的誠実性に依存する部分として本契約が明示的に受容する（利用者の
「送信ごとの確認なし」決定と同じ水準の受容である）。

## 3. 権威、証拠

| 役割 | path | SHA-256 |
| --- | --- | --- |
| 暫定Geminiレビュー体制の決定 | `records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md` | `1a5fffc5792d17791f5c275b40183a0d4d076233d6d1b7a267cd91cf92174792` |
| 利用者の運用化目標 | `records/development/2026-08-16-accepted-parts-operationalization-goal-v1.md` | `c5f43f6c3b8eb7bc8b9c6b6dbb57f83039009ffcfe8127a481e04b3f8c7fb42a` |
| 次製品作業の候補一覧（候補5の定義） | `records/development/2026-08-15-post-safe-storage-next-product-work-candidates-v1.md` | `bcb4ba2947e32254edc547068728fa580bc6b7919fa0f04d9b9353ab6c7899ba` |
| 現行開発方針 | `docs/development/2026-08-02-development-policy.md` | `e3e6b0d2c7a1265f7cde2c2e00cc888f43d63ce0d1945c300b2b2e5f7730b559` |

【判断】上流不一致の明示：既存の出口設計v4は送信内容を3種の型（code断片・機械特徴量・承認済み定型文）に
制限し、自由文を型として通さない。本契約はこれと異なる「送信契約模型」（commit済みfile由来＋機微検査＋
digest束縛＋台帳を条件に自由文を送れる）を新設する。v4設計は暫定・非正式のまま変更せず、両模型の統合は
後続契約のHuman判断へ残す。v4の「送信前検査の単一実装」の趣旨は、本製品内の検査を新核一箇所へ集約する
ことで守る。

## 4. 実装方法の3案

| 案 | 内容 | 判断 |
| --- | --- | --- |
| A 手動貼り付けの継続 | 利用者がGemini画面へ手で貼る | 機械化なし。台帳・機微検査・digest束縛が働かず、運用化目標に反する。不採用 |
| B 既存egress 7 moduleの正式化＋送信段追加 | 旧gate・payload型へ送信を接続 | 3種型制限が目的（自由文レビュー依頼）と不適合で、7 module全体の正式化は過大。不採用 |
| C 狭い専用送信核 | 送信指示一件を検査し、由来fileからpayloadを機械構成し、一回送信・保存・台帳着地する新核 | 既存egress不変更・変更範囲最小。推奨 |

## 5. 範囲

### 5.1 範囲内

- 送信指示JSON一件（262,144 bytes以下）の安全読取り・機微検査・schema検査。
- 由来fileの読込み（repository内・§7.2 allowlist・宣言digest一致・各fileの機微検査）。
- 固定templateと由来fileからのpayload機械構成、size上限検査。
- 送信試行recordの着地（送信前）、選択providerのAPIへの一回のHTTPS送信（再試行なし）、未加工応答の保存、
  結果recordの着地、標準出力への結果一件。

### 5.2 範囲外

- 応答の解析・判定抽出・G02 organizeへの接続（後続。応答は未加工保存まで）。
- 複数送信の一括・並列、自動再試行、送信の取り消し、§7.1の3 provider以外の宛先。
- 既存egress 7 module・既存製品・要求資料の変更。抜き取り監査の自動化（台帳を材料に後続で扱う）。
- 実利用者要求資料（`records/requirements/`配下）の送信。
- Claudeの自発的な送信（利用者の指示なく本入口を起動すること）。

## 6. 固定再利用部品と保護基準

### 6.1 機微情報候補検査

`tools/session_logs/redaction.py`、SHA-256
`aa49774a447d84422ec885a908bb52c7a3732eb67ddb53dcc1c03fbc149245bd`の公開`default_pattern_rules`と
`find_high_entropy`だけを再利用する。既定patternは5件である。

### 6.2 保護対象

保護基準commitを`aac1f90c17e0a6bdd170fc6beef93ad928abfa22`とする。次を変更しない。

| path | SHA-256 |
| --- | --- |
| `tools/egress/__init__.py` | `8386033f1d8ef3999da06b8a17cd4a9a5282636dda1e77d7d80a4a8b354656fd` |
| `tools/egress/approval.py` | `cb8f97e1d2b05f0ec7e9bad9e045c80b8378a03167be2d623f13853c3236b243` |
| `tools/egress/dry_run.py` | `73c5c82dc1eeb24a75593c51cd8a6b01698498c4db0e7df8124124ee7dc207d2` |
| `tools/egress/gate.py` | `ec611dfa65c0ff8f8ccf586ed491e944430cf80952a797861ea3b06a7f1de0c1` |
| `tools/egress/payload.py` | `daeb48b1ef3c00f7ae14ba1debfaba7efe564387808e505d57e4c15a14d34a1f` |
| `tools/egress/prefilter.py` | `c0b6a2da30923802eb419817d55bf8c2eb1f2e6a9a580074b1f90cd77773bf43` |
| `tools/egress/sender.py` | `05286fe21ee5baf264c80fe8518eccef3602de1c7ada6041e121dd4a2b5bbef8` |

`tools/session_logs/redaction.py`、受入済み4製品（G02・G08・G24・実行器）とその試験、`tools/task_contract/`
5 fileも同commitから変更しない。

## 7. 契約固定の送信規則

### 7.1 宛先と経路（3 providerの切り替え式）

宛先は次の固定表の3 providerだけとし、送信指示の`destination_provider`で選ぶ。各providerのhost・経路・
認証headerは固定で、実装者・送信指示のどちらも変更できない。

| provider | host（HTTPSのみ） | 経路 | 認証 | 環境変数 | model名の形 |
| --- | --- | --- | --- | --- | --- |
| `gemini-api` | `generativelanguage.googleapis.com` | `POST /v1beta/models/{model}:generateContent` | header `x-goog-api-key` | `GEMINI_API_KEY` | `gemini-`で始まる`[a-z0-9.-]`列 |
| `openai-api` | `api.openai.com` | `POST /v1/chat/completions` | header `Authorization: Bearer` | `OPENAI_API_KEY` | `gpt-`または`o`で始まる`[a-z0-9.-]`列 |
| `anthropic-api` | `api.anthropic.com` | `POST /v1/messages`（`anthropic-version` header固定） | header `x-api-key` | `ANTHROPIC_API_KEY` | `claude-`で始まる`[a-z0-9.-]`列 |

- **環境値解決は上表の3変数だけに許可し、一回の実行で読むのは選択providerの1変数だけ**とする。
  keyはHTTP headerでだけ送り、URL・標準出力・台帳・応答保存・例外・logへ一切含めない。
- **独立性検査**：送信指示は操縦LLMのprovider（`pilot_provider`）を宣言し、`destination_provider`と同一の場合は
  停止する（自分と同じ系列のmodelへ「独立確認」を出す誤用を機械で防ぐ。例：Claudeが操縦中はanthropic-apiへ
  送れず、Codexが操縦中はopenai-apiへ送れない）。
- HTTP要求は一回だけ。timeoutは300秒固定。自動再試行をしない（再送は新しい送信指示＝新しい台帳記録を要する）。
- **リダイレクトへ追従しない**。3xx応答は`http_error`として扱い、応答を保存して停止する。
- **環境のproxy設定を使わない**。proxy関連の環境変数を読まず、直接接続だけを行う。
- **TLS証明書検証を無効化しない**。検証失敗は`network_failure`である。
- 切り替えの設計は先行実装（ReviewCompassの`tools/api_providers/providers.py`）を参考にし、codeはコピーしない。

### 7.2 由来fileのallowlist

送れるのは、repository内のcommit済みfileで、次のpath条件を満たすものだけである。

- 許可：`docs/`配下、`records/`配下、`tools/`配下、`tests/`配下、`config/`配下、
  root直下の`AGENTS.md`・`TODO_NEXT_SESSION.md`・`pyproject.toml`。
- 除外（許可より優先）：`records/requirements/`配下、名前が`.env`で始まるfile、`.git/`配下。
- 各fileは送信指示が宣言するSHA-256と実bytesの一致を要し、不一致は停止する。
- 各fileの内容は§6.1の機微検査に合格しなければならない（不合格は帯1として自動停止）。
- **限界の明示（SR-5）**：moduleが機械検査するのは宣言digestと実bytesの一致までである。
  「commit済みであること」の照合は、送信指示を作成する手続き（操縦LLMがGitで機械確認する）の義務であり、
  moduleはGitを使わない。台帳がrepository内に着地しcommitされること（§10）が事後の監査線になる。

### 7.3 上限と台帳root（SR-1）

- 一回の送信payloadは2,097,152 bytes（2 MiB）以下。由来fileは1〜64件。
- **台帳rootは`{repository_root}/.reviewcompass/egress-ledger/`へ契約固定**する。試行record・応答・結果は
  全てこの一箇所だけに着地する（送信指示で変更できない。これにより累計計数が一意になる）。
  台帳rootが存在しない場合は停止する（moduleはdirectoryを作成しない。初回はcommitで用意する）。
- 累計送信試行は台帳rootの試行record件数で数え、**100件**に達したら停止する。上限の変更は契約改定
  （Human承認）を要する。
- 応答は16,777,216 bytes（16 MiB）以下。超過は`response_size_exceeded`で停止する（SR-4）。
- 台帳fileはrepository内に着地するため、送信を含む作業単位の意味単位commitに含めて履歴へ固定する。

## 8. 送信指示の形式

rootは次の項目だけを持つ（同名項目・未知項目・浮動小数点・null・入れ子配列の禁止、ID・SHA-256・
絶対pathの規則、機微検査の順序は契約006 v4 §8の共通規則を引き継ぐ。§8.2相当の除外は
`/source_files/{index}/sha256`の正規SHA-256値、`/destination_provider`と`/pilot_provider`の固定3値、
`/destination_model`のうち選択providerのmodel名規則へ合格した値だけ）。

- `schema_version`：整数`1`。
- `order_identifier`：一般ID。台帳record名の一部になる。過去と同じIDは試行record既存で停止する
  （これが再送の暴走を防ぐ：再送は必ず新しいIDと新しい台帳記録を要する）。
- `human_approved`：`true`だけ。
- `destination_provider`：`gemini-api`、`openai-api`、`anthropic-api`だけ。
- `destination_model`：§7.1の該当provider規則へ合格する文字列だけ。
- `pilot_provider`：同じ3値だけ。操縦LLMの系列を宣言し、`destination_provider`と同一なら停止する。
- `purpose`：自由文1〜500文字。台帳へ記録される（機微検査対象）。
- `repository_root`：絶対path。由来fileの起点であり、台帳root（§7.3）の起点でもある。
  **実在検査（原因1）**：`{repository_root}/.git`が存在しない場合は`invalid_repository_root`（source `order`・
  終了コード2）で停止する。偽rootの指定による台帳の分散・累計上限の回避を機械で拒否する
  （`.git`を偽装したdirectoryまでは防げず、その残余は§2の限界に含まれる）。
- `source_files`：1〜64件。各項目は`path`（repository_rootからの相対path・§7.2の条件）と`sha256`だけ。
  **pathの構成要素規則（原因1）**：`path`は`/`区切りの相対pathとし、空・`.`・`..`の構成要素、先頭`/`、
  NUL文字、単独サロゲートを禁止する（repository外への遡上を型で拒否する）。

（v2にあった`output_root`は削除した。着地先は§7.3の固定台帳rootだけである。）

**識別子と高乱雑性検査（原因2の明示）**：`order_identifier`を機微検査から**除外しない**。除外すると、
一般ID規則に合格する鍵形式（例：`AKIA`＋16大文字英数字）を識別子として台帳・record名へ流し込み、commitされた
repositoryへ残す漏えい経路が生まれるためである（受入済みのG24・006も識別子を除外しない）。したがって
24文字以上の乱雑な識別子（UUID等）は`sensitive_data_remaining`で停止する。これは誤検知ではなく仕様であり、
識別子には24文字未満の可読形（例：`ORD-G20-REVIEW-001`）を用いる。

## 9. payloadの機械構成

payload本文は次の固定形の連結とする（この形だけが送られる）。

1. 固定前文（契約定義の定型文）：「あなたは独立したレビュアです。以下の資料を読み、資料内の依頼記述に
   従って判定を返してください。判定には根拠を付けてください。」
2. 各由来fileについて、区切り行`----- FILE: {path} (sha256={sha256}) -----`とfile内容（UTF-8文章として
   有効であること。無効は停止）。

payload全体のSHA-256を`payload_sha256`として台帳と結果へ記録する。自由文の追加入力欄はない
（前文は契約固定、資料はcommit済みfileだけ）。

### 9.1 provider別のHTTP要求本文の固定形（SR-2）

要求本文はJSONとし、埋め込むのは`{model}`と`{payload本文}`の2箇所だけとする。他の項目・値は固定で、
実装者・送信指示のどちらも追加・変更できない。

| provider | 要求本文の固定形 |
| --- | --- |
| `gemini-api` | `{"contents":[{"parts":[{"text":"{payload本文}"}]}]}`（modelは経路に埋める） |
| `openai-api` | `{"model":"{model}","messages":[{"role":"user","content":"{payload本文}"}]}` |
| `anthropic-api` | `{"model":"{model}","max_tokens":8192,"messages":[{"role":"user","content":"{payload本文}"}]}`。`max_tokens`は8192固定、header `anthropic-version: 2023-06-01`固定 |

## 10. 台帳・応答保存・結果

### 10.1 送信試行record（送信前に着地）

出力先事前検査（SR-6・原因1）：`{repository_root}/.git`が存在すること、台帳root（§7.3）が既存directoryで
あること、`{order_identifier}--attempt-v1.json`・`--response-v1.raw`・`--result-v1.json`の3名とその一時名が
いずれも存在しないことを、部品実行の前に確認する。

送信の**前**に、`{order_identifier}--attempt-v1.json`を台帳rootへ新規作成専用・一時名＋hard link
公開（契約006 v4 §7と同じ二段）で着地させる。項目：`status: attempt_recorded`、`schema_version: 1`、
`order`（identifier・sha256）、`destination_provider`、`destination_model`、`pilot_provider`、`purpose`、`source_files`（path・sha256の一覧）、
`payload_sha256`、`payload_bytes`、`attempted_at`（UTC・ISO 8601。**時刻取得は台帳の時刻記録だけに許可**）、
`external_send_approved: true`、`record_sha256`。

送信が通信段階で失敗しても試行recordは残り、累計上限（§7.3）に数えられる。届いたか不明な失敗を
「送っていない」と数えないための保守的な設計である。

### 10.2 応答保存と結果record

- 応答は`{order_identifier}--response-v1.raw`へ、HTTP本文bytesを無加工で新規作成保存し、再読込一致を確認する。
- 結果recordは`{order_identifier}--result-v1.json`（同じ二段着地）：`status: response_stored`、
  `schema_version: 1`、`order`（identifier・sha256）、`http_status`、`payload_sha256`、`response_sha256`、
  `response_bytes`、`completed_at`、`external_send_approved: true`、`record_sha256`。
- 標準出力へは結果recordと同一bytesを返す。終了コード0。標準エラー空。絶対path・API key・応答本文を
  標準出力へ含めない。

### 10.3 停止結果

停止は`status: stopped`、`reason`、`source`、`external_send_approved`（試行record着地後の停止だけ`true`、
それ以外`false`）だけの正準JSON一件とLF。主な停止：

| 違反 | `reason` | `source` | 終了コード |
| --- | --- | --- | ---: |
| 引数の不足・未知・重複／相対path | `invalid_arguments`／`invalid_path` | `arguments` | 2 |
| 送信指示fileの読取り・size・UTF-8・schema違反 | 契約006 v4 §11と同形 | `order` | 2 |
| 送信指示・由来fileの機微情報候補（乱雑な識別子を含む） | `sensitive_data_remaining` | `order`／`source_file` | 3 |
| `{repository_root}/.git`の不存在 | `invalid_repository_root` | `order` | 2 |
| allowlist外・構成要素規則違反・digest不一致・UTF-8無効の由来file | `source_file_rejected` | `source_file` | 2 |
| payload size超過・件数超過・累計上限到達 | `limit_exceeded` | `order`／`ledger` | 2 |
| 試行record既存（同一IDの再送） | `duplicate_order` | `ledger` | 2 |
| 選択providerの環境変数が未設定・空 | `missing_credentials` | `credentials` | 2 |
| `pilot_provider`と`destination_provider`が同一 | `reviewer_not_independent` | `order` | 2 |
| 台帳root不存在・非directory、§10.1の3 record名または一時名の既存、書込み失敗 | 契約006 v4 §11と同形（`invalid_output_root`／`record_write_failed`等） | `ledger` | 2／4 |
| HTTP応答が200以外（3xxを含む。応答は`--response-v1.raw`へ保存済み） | `http_error` | `network` | 7 |
| 応答が16 MiB超過（応答fileは作らず、試行recordは残存） | `response_size_exceeded` | `network` | 7 |
| 送信後の通信例外・TLS検証失敗（応答なし。試行recordは残存） | `network_failure` | `network` | 7 |
| 上記へ分類できない内部例外 | `internal_failure` | `none` | 4 |

## 11. 変更上限

1. 送信核`tools/external_review/gemini_send.py`（新規package `tools/external_review/`。既存egress 7 moduleは
   変更しない。旧packageの「配下に通信手段が存在しない」不変条件を保つため、承認済み送信路は別packageに置く）。
2. 入口`tools/external_review/gemini_send_entry.py`（新規）。`send --order <絶対path>`だけ。
3. `pyproject.toml`への実行名`reviewcompass3-gemini-send`一件。
4. 対象試験`tests/test_gemini_send.py`（通信は全て模擬。実送信を試験に含めない）。
5. Evidence、独立確認、受入判断、TODO更新。

module名`gemini_send`はv1由来の残名であり、実体は3 provider切り替え式である（機能への影響なし。
改名は後続の整理で扱ってよい）。

## 12. 受入条件

実装開始後は失敗試験を先に固定し、期待どおり失敗してから最小実装を行う。

1. 模擬通信の正例で、試行record→送信→応答保存→結果recordの順と、各内容識別値の独立oracle再計算を示す。
2. payload構成が§9の固定形どおりで、由来fileのdigest不一致・allowlist違反・UTF-8無効・構成要素規則違反
   （`..`遡上を含む）が停止する。`{repository_root}/.git`不存在が`invalid_repository_root`で停止し、
   台帳が固定root以外へ着地しない。乱雑な識別子（24文字以上）が仕様どおり停止する。
3. 送信指示・由来fileの機微情報候補（既定5 pattern＋高乱雑性）が停止し、正規SHA-256欄と固定model名だけが
   除外される。
4. 同一`order_identifier`の再実行が`duplicate_order`で停止し、二重送信が起きない。
5. 累計上限（契約固定の台帳root単位で一意に計数されること）・payload size上限・件数上限・応答size上限
   （`response_size_exceeded`）で停止する。
6. §7.1の3環境変数のいずれの値も結果・台帳・標準出力・例外・応答保存に現れないことを、鍵値の全出力走査で確認する。
7. 通信は固定host・固定経路への一回だけで、再試行・別経路・URLへの鍵混入がないことを模擬層で確認する。
   §9.1の要求本文が固定形どおりであること、リダイレクトへ追従しないこと（3xxで`http_error`停止・応答保存）、
   環境のproxy設定を読まないこと、TLS検証を無効化しないことを確認する。
8. 通信失敗・HTTP異常の各停止で、試行recordが残り、結果recordが作られないことを確認する。
9. 時刻取得が台帳の時刻記録だけに使われ、環境値解決が選択providerの1変数だけ（他providerの変数を読まない）で
    あることを確認する。3 providerそれぞれの模擬送信と、`pilot_provider`同一時の`reviewer_not_independent`停止を確認する。
10. 配布後の正式実行名を別の現在位置から実行しても（模擬層で）同じ判定系列を返す。
11. 既存egress 7 module・受入済み4製品・保護対象が基準commitから差分0で、既存試験
    （egress関連107件・受入済み各製品の対象試験・正規全試験）が各単独終了コード0で成功する。
12. 対象・関連・正規全試験の成功後、固定commitを独立レビュー（暫定体制：Gemini手動）が誤合格・未接続・
    禁止作用・上位目的への悪影響0件として確認する。
13. 利用者の指示の下で実送信E2Eを一回行い、試行record・応答保存・結果record・台帳計数を実環境で確認する
    （これが本repositoryで最初の承認済み外部送信となる）。
14. 利用者が「G20全体ではない最初の送信縦切りである」限界（応答解析・監査自動化・旧設計統合は後続）と
    実装結果を確認して製品処理を受け入れる。

## 13. 停止条件

- 送信内容の機械的守り（機微検査・allowlist・digest束縛・台帳）を一意に固定できない。
- 既存egress 7 module・受入済み製品の変更が必要になる。
- §7.1の3環境変数以外の認証情報・環境値・任意URL・再試行・並列送信が必要になる。
- 送信ごとの人の確認を前提にしないと安全を主張できない欠陥が見つかる。
- 対象、関連、正規全試験または独立確認が不合格になる。

## 14. 影響、未実施、次作業

【判断】受入後は、利用者の指示の下で、commit済み資料によるレビュー依頼を3 provider（Gemini・OpenAI・Anthropic）の
いずれかへ切り替え式に、機械的な守り
（機微検査・allowlist・digest束縛・台帳・上限）つきで送信できる。従来のcodex exec方式（全repo可読・
無検査・無台帳）より全層で厳しい経路が、初めて正式の外部送信路になる。開発レビューの運搬をHuman中継から
本経路へ移す判断、応答解析（G02 organize接続）、抜き取り監査、旧設計統合は後続に残る。

【未実施】契約採用、実装、実送信、既存成果物変更は行っていない。

次は本候補を固定commitへ記録し、暫定体制（利用者がGeminiへ手動運搬）で独立確認を受ける。`開始可`になった後、
利用者へ縮小境界の採用と実装開始を一判断として求める。
