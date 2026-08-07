# LLMGP外部APIレビュー実運用資産 調査結果record v1

- record ID：`INV-LLMGP-EXTERNAL-REVIEW-ASSETS-001`
- 作成：2026-08-07
- 根拠：Human選定の案1（2026-08-07。まず最新1回分を精読し、把握してから調査範囲を判断する）
- 追加調査：Human指摘（2026-08-07「もしかすると、ReviewCompassにも同様の実装があるかもしれない」）を受け、固定（コミット）前に§2.7〜§2.8と関連箇所を追記した。初稿の§2.6は配備先コピーの状態を最新と誤認していた
- 前提観測：`records/development/2026-08-07-llmgp-external-review-assets-observation-v1.json`（SHA-256 `872c4736b33f4c314e1fc3bd22ffb52ce8be5de6b0dcfaca3b9841921ae6bc07`）

## 1. 調査の範囲と読んだもの

精読対象（合意済みの最新1回分）：

- `/Users/Daily/Development/WindTurbineWake/LLMGP/.reviewcompass/specs/_cross_feature/reviews/2026-07-27-requirements-redraft-triad-review/`
  - `main-preanalysis.md`（事前検討。判断項目D1〜D8、材料一覧、送信を避ける情報、監査2回の反映記録）
  - `api-review-criteria-three-features.md`（破棄版。冒頭に破棄の経緯と実使用版への参照を明記して保存されている）
  - `triad-review-summary.md`（実行記録と三段階トリアージ）
  - `target-*-masked.md` 3件（マスク済み審査対象）
  - `preanalysis-audit/`（監査3ラウンドの実行仕様・プロンプト・生応答・解析結果）

追随して読んだもの（精読対象が参照する正本と実行機構）：

- 実使用の機能別run：`/Users/Daily/Development/WindTurbineWake/LLMGP/.reviewcompass/specs/equation-fitting/reviews/2026-07-27-equation-fitting-requirements-review-run/`（`api-review-criteria.md`、`review-target-masked.md`、`findings-raw.yaml`、`real-review/rounds.yaml`）
- 手順の正本：`/Users/Daily/Development/WindTurbineWake/ReviewCompass/.reviewcompass/guidance/API_REVIEW_PROMPT_QUALITY.md`（9段階手順）
- 実行機構（配備先コピー）：`/Users/Daily/Development/WindTurbineWake/ReviewCompass/tools/api_providers/`（`run_review.py`、`external_api_approval.py`、`runner_gate.py` ほか）と `config/api-settings.yaml`（役組み合わせvariant定義）

Human指摘による追加調査の対象：

- **開発元**：`/Users/Daily/Development/ReviewCompass/`（VERSION 0.1.0、最終commit 2026-07-31）。WindTurbineWake配下は配備先コピーであり（`deploy-manifest.yaml`・`build/`を持つ）、開発元の`tools/api_providers/`には配備先に無いファイルが多数ある（`delivery_preflight.py`、`trusted_route.py`、`trusted_review_send.py`、`review_input_guard.py`、`source_scope_guard.py`、`risk_review_*`ほか）
- **RC3自身**：`tools/bootstrap/`（`closed_payload.py`、`review_pipeline.py`、`review_execution.py`、`review_contract.py` ほか17ファイル、計約2,500行）
- **ReviewCompass2**：該当実装なし（`external_api`・`delivery_preflight`・`trusted_route`の走査で0件）

LLMGPの成果物は一切コピーしていない。読み取りのみである。

## 2. 把握した仕組み

### 2.1 マスク済み対象の作り方

- 審査対象は**逐語コピー＋1種類の置換のみ**。作成者の計算機の絶対パス接頭辞を `<workspace>` へ置換する。
- 置換した事実を審査基準に宣言する（例：「equation-fittingに2回、他の2文書には出現なし。他は無変更」）。審査者が対象の改変を疑わずに済むための宣言である。
- 機械確認：本調査で masked 4ファイルに対し絶対パス（`/Users/`）の残存を走査し、**0件**を確認した。
- 事前分析に「送信を避ける情報」の節が必須で置かれる。項目は（1）絶対パス→`<workspace>`置換、（2）API keyなどの秘密値、（3）個人識別情報。含まれない場合も「含まれない」と明記する。
- 送信可能材料の基準（正本§5）：利用者の明示承認、秘密値なし、個人識別情報なし、第三者契約上の非公開情報なし、判断に必要な最小限。**「リポジトリ内の未公開情報であること」自体は送信禁止の理由にしない**という線引きが明文化されている。

### 2.2 レビュー基準（criteria）の構成

- 必須9要素：review task／why this review exists／user review requirements／required disciplines／review target／source materials／required checks／out of scope／finding policy。
- **criteriaとtargetの分離**が禁止事項として明文化されている（同一の要約を両方に渡す、target本文なしで実行する、等）。対象本文はcriteriaに再掲しない（「criteriaが対象と誤認されないため」）。
- review taskは**1プロンプト1問**。独立判断のまとめ込みは監査で `ERROR` になる（実例：3機能まとめ案が両役 `ERROR` で破棄され、1機能1プロンプト計4本へ分割された）。
- source materialsは**path-only禁止**。本文抜粋または全文を審査者が読める形で収録する。第3ラウンドでは「抜粋の選定という判断そのものを避ける」ため上流・隣接機能とも全文収録へ移行した。
- required checksは要求claimごとに分解（C1〜C8）。各checkは「何を成立させる主張か／どの材料で判定するか／何を欠陥とするか」を分けて書く。
- 利用者判断は**文言どおり**引用し、述べられていない理由を書かない。「理由の書き漏れとして指摘しないこと」まで審査者へ指示する。
- 出力契約：YAMLのみ。severity 4段（CRITICAL/ERROR/WARN/INFO）の判定条件を対象固有に定義。**所見0件のときは `pass_rationale`（check×文書ごとの合格根拠）を必須**とし、裸の `findings: []` は不完全なレビューとして扱う。

### 2.3 事前分析（main preanalysis）の役割

- 位置づけは「審査者に対する正解ではない。仮説であり、材料を見つけるための手がかり」。審査者にはsource materialsから**独立再構成**させ、その後で事前分析と突き合わせさせる。
- 内容：判断項目（何を成立させる主張か・判定材料・欠陥条件）、読んだ材料と使用目的、プロンプト分割の要否、収録すべき材料、送信を避ける情報、未解決事項（`open`／`resolved`／`superseded` の現在性区別付き）。
- 独立性規則：主査は操縦LLMと同系列にしない（操縦がOpus系なら主査はSonnet等。`AGENT_ENTRY.md` §10）。
- 「反映した」という起草側の申告を審査者は根拠として扱わない、と明記する（実際に第1回の反映が新たな欠落を生んだ実例に基づく）。

### 2.4 品質確認ループ（実行前の関門）

標準順序：事前分析→**事前検討十分性監査**（2役：敵対役・判定役）→criteria草案→セルフチェック→**prompt quality review**→実行。判定役が `findings: []` を返した場合だけ実行へ進める。

実測（本run）：監査3ラウンド、所見10＋10＋9件。第3ラウンドで利用者が打ち切りを判断した。この暴走の反省が記録されている：

- 監査を始める前に**ラウンド数の上限を決める**
- 直近に同じ段のレビューを通っているなら、その事実と日付を審査基準に書く
- **同じ形の指摘が2ラウンド続いたら、指摘の中身ではなく前提を疑う**（審査基準は485行→約1,400行へ膨張した）

### 2.5 実行機構と証跡

- 役組み合わせは `config/api-settings.yaml` のvariantとして定義。役（主査・敵対役・判定役）ごとにprovider・モデル・timeoutを固定し、`provider_constraint: all_roles_distinct`（3役とも提供元を別にする）を宣言できる。場面ごとの既定variantも設定で決まり、LLMが手作業で選ばない。
- 一部の役のAPIが応答しない場合、揃った少数で確定させず**人へエスカレート**する（`role_availability.on_incomplete_responses: escalate_to_human`）。同一系統内の代替は明示承認時のみ。
- 証跡：runディレクトリに `review-execution-spec.yaml`（使用criteria逐語＋出典SHA-256、対象manifest＋SHA-256、役ごとの出力パス）、`prompts/`・`raw/`・`parsed/`（ラウンド×役）、`rounds.yaml`、`model-result-summary.yaml`、`triage.yaml`、`review_summary.md`。何を・どのモデルへ・どの文面で送ったかが後から逐語で追える。
- 実行時間の実測：役ごと応答60〜260秒。timeoutは300〜3600秒で役ごとに設定。

### 2.6 外部送信の承認ゲート（`external_api_approval.py`）

`external-api-approval-v1` という承認recordの機械検証が実装されている。検証項目：

- `approved_by: user` であること
- `approved_action` が許可2種（`external_api_review`／`external_api_proxy_model`）のいずれか
- **provider・モデルの一致**（承認時と実行時で食い違えば拒否）
- **期限**（`expires_at`、timezone必須）と**一回性**（`consumed: true` なら拒否）
- `purpose` の一致、`allowed_prompt_globs` による**対象プロンプトの範囲限定**
- `material_policy` の3フラグ（秘密値走査必須・資格情報禁止・個人識別子禁止）が全てtrue
- 送信直前の文面に対する**正規表現走査**（API key・token・password・Bearer・`sk-`系、メールアドレス、電話番号様の数字列）

**配備先コピーの限界（開発元では解消済み）**：配備先コピーではこの検証を呼ぶのは `run_proxy_decision.py` のみで、レビュー実行の `run_review.py` には接続されていない。`run_review.py` 側の関門は別系統（criteriaの構造化要約6項目のpreflight、プロンプトmanifest監査、`runner_gate.py` の4条件）であり、承認record検証と秘密値走査は通らない。マスクも実行係が強制するのではなく、起草側が手で行い宣言する運用である。**この状態はLLMGPの6 runが実行された時点の姿であり、開発元ではその後§2.7の形へ発展している。**

### 2.7 開発元ReviewCompassの外部送信ゲート（Human指摘による追加発見）

開発元（最終commit 2026-07-31）では、初稿§2.6の限界がそのまま設計課題として解かれていた。出口の設計提案v2が答えようとした問いへの、より新しい実運用実装である。

- **送信前機械検査の単一実装**（`delivery_preflight.py`）：「`run_review.py`経由・`run_role.py`直接のどちらの呼び出しでも**外部送信の直前に必ず通る（二重実装禁止）**」と冒頭に明記。検査3項目：（1）入力規模の上限（役ごとに設定。既定は主役45KBでfail-closed＝超過時は送信せず停止）、（2）フェンス整合lint（コードフェンスの開閉対応と遮蔽）、（3）対象整合（target実在・manifestのSHA-256一致）。停止時は理由と**実行可能な復旧コマンド**を印字し、自動切り詰め・自動修正はしない
- **trusted送信経路**（`trusted_route.py`）：外部providerへの送信を管理された入口（`/usr/local/libexec/reviewcompass/trusted-review-send`）へ限定するroute resolver。manifestは**content-addressed**（ファイル名がその内容のSHA-256と一致しなければ拒否）。承認との結合fieldとして `operation_contract_ref`・`contract_digest`・`approval_stage`・`payload_digest` 等を持つ
- **承認の一回性の競合安全化**（開発元の`external_api_approval.py`）：承認recordの消費に排他claim（`.consume-claim`ファイルの排他生成）を導入し、同時実行での二重消費を防ぐ
- **trusted送信入口**（`trusted_review_send.py`）：送信先・provider・実行ファイルパスを定数で固定し、役→モデルの対応表と役→目的の対応表を持ち、無効化必須機能（plugins等）を宣言する。承認actionは `external_review_send`

### 2.8 RC3自身のbootstrapレビュー機構（Human指摘による追加確認）

RC3の`tools/bootstrap/`（provisional・non-normative）に、送信物を閉じるまでの機構が既に実装されている。

- 流れ：材料束の構築（`material_bundle.py`）→証拠閉包の判定（`evidence_closure.py`。不足なら`blocked`で停止）→**閉鎖payloadの生成**（`closed_payload.py`。束digest・対象digestに対する`PayloadApproval`を要求）→固定プロンプトと出力schemaの契約（`review_contract.py`、`bootstrap-review-v1`）→複数担当の実行境界（`review_execution.py`。担当ごとにprovider・モデル・route main/independentを持つ）→トリアージ・保存
- **外部への実送信の実装は無い**。`run_review_pipeline`は`runner`を外から注入する形で、通信ライブラリへの依存が0件であることを走査で確認した（`httpx`・`requests`・`urllib`・provider名の走査で0件）
- すなわちRC3は「送る物を閉じて承認へ結びつける」内側を既に持ち、欠けているのは**外へ出る瞬間の経路と関門**である。出口の設計提案v3は、この既存機構への接続として設計すべきであり、並行の新機構を発明すべきではない

## 3. 出口の設計提案v3で継承すべき点

1. **承認recordの機械検証様式**（§2.6）。v2の「承認の粒度」への実運用済みの答えがここにある：利用者承認・provider/モデル固定・期限・一回性・目的・対象glob・材料方針・送信直前走査。全経路への接続は開発元が§2.7の形（送信直前に必ず通る単一実装＋trusted入口への限定）で既に解いており、その形を継承する。
1-2. **開発元の出口設計そのもの**（§2.7）：送信前機械検査の単一実装（二重実装禁止の明記）、fail-closedと実行可能な復旧コマンドの印字、content-addressedなmanifest、承認消費の排他claim、送信入口の実行ファイル固定。v3の骨格はLLMGPの運用形（v1世代）ではなく、この新しい世代を土台にする。
1-3. **RC3既存機構への接続**（§2.8）：RC3は閉鎖payload・証拠閉包・契約・実行境界を既に持つ。v3は`runner`注入点から外への経路と関門を設計する。並行機構の新設は行わない。
2. **マスクの運用形**（§2.1）：逐語コピー＋最小置換＋**置換内容の宣言**＋機械確認。「何を変えたか」を審査基準に書くことで、マスクが対象の信頼性を損なわない。
3. **送信可能材料の基準**（§2.1末尾）：「未公開であること自体は禁止理由にしない」線引きと、禁止4条件＋最小限原則。RC3のC（内部の未公開情報）の定義の出発点になる。
4. **criteriaの必須9要素と出力契約**（§2.2）：特に criteria／target 分離、path-only禁止、1プロンプト1判断、`findings: []` に `pass_rationale` 必須。
5. **事前分析の位置づけ**（§2.3）：仮説であって正解ではない。送信を避ける情報の節を必須にする。所見の現在性区別（open/resolved/superseded）。
6. **実行前監査の歯止め**（§2.4）：ラウンド上限の事前決定、同形指摘2連続で前提を疑う。監査自体が暴走した実例と対策が既にある。
7. **証跡の形**（§2.5）：送った文面の逐語保存＋SHA-256固定＋役ごとの生応答保存。RC3の「外へ出た瞬間の完全な記録」要件はこの形で満たせる。
8. **役が揃わないときのエスカレート**（§2.5）：少数で確定させない。

## 4. v2の考案値の再検証材料

- **上限20件（グループ数）**：LLMGPに件数上限の運用は存在しない。実運用の答えは「**1プロンプト1判断**への分割」と「材料は抜粋選定を避けて全文収録」であり、量の上限ではなく判断単位の分割が品質を決めていた。v3では件数上限を主軸にしない再設計を検討する。
- **payload形状**：v2の発明ではなく、`review-execution-spec.yaml`＋criteria＋masked targetという実運用形を土台にする。
- **規模の実測**：criteria約43KB、監査bundle約200KB、審査基準485→1,400行（膨張の失敗例）。v3の見積もりに使う。

## 5. 調査範囲の判断（案1の後段）

最新1回分の精読と機構正本の確認で、継承すべき点の特定には足りると判断する。残る5 run（wave系・2026-07-28系）は同一機構の反復であり、wave系は役を単独variant（`review_wave_*_llmgp`）で分けて実行する変形にすぎない。追加精読は、提案v3の起草中に特定の論点（例：waveの横断段の材料構成）で必要が生じた場合に限る。

追加調査後の残課題：開発元`tools/api_providers/`の未精読分（`review_input_guard.py`、`source_scope_guard.py`、`risk_review_*`、`assurance_pipeline.py`等）は、v3起草時に出口の関門に関わる範囲だけ精読する。全ファイルの精読は本調査の範囲としない。

## 5.1 調査過程の教訓（記録）

初稿は、審査基準が参照する配備先コピー（WindTurbineWake配下）だけを読み、その状態を最新と誤認して§2.6の限界を断定した。開発元の存在はHumanの指摘で判明した。配備物を読むときは**開発元の所在と鮮度（最終commit日）を確認してから状態を断定する**。これは「記録が指す先まで確認を広げる」（前回session教訓）のさらに先、「指された物が写しなら原本まで遡る」である。

## 6. 境界

- 本recordは調査結果の固定であり、出口の設計提案v3の内容を決めない。
- LLMGPの審査対象はLLMGP自身の要件文書であり、RC3が扱う機密領域の実データとは機微の性質が異なる。継承するのは**仕組み**であり、何を出してよいかの判断基準そのものは流用しない。
- LLMGPの成果物のコピー・改変は行っていない。
- 提案v3の起草、規則の登録、C・Dの定義はいずれも本recordの範囲外（実施順序Decision `DEC-CONFIDENTIALITY-WORK-ORDER-001` に従う）。
