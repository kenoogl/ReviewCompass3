# Scope prescan run

契約候補（範囲固定）を定義する前の事前走査の共通手順である。LLMは意味分析だけを行い、件数・digest・
検索・Git確認は機械処理を使う。結果は事前走査recordへ一元化し、意味単位commitで固定してから
契約候補の作成へ進む。

## 6手順

1. **所在特定**：流用候補の部品・接続先・前例recordの所在を機械検索で列挙する。
2. **import元**：流用候補のimport元を全文検索し、変更の波及範囲と保護要件を把握する。
3. **Digest固定の全文検索**：主題語で全repositoryを検索して対象fileの一覧を閉じ、契約候補が参照する
   fileのSHA-256表を`shasum -a 256`で機械生成する。
4. **接続点**：新設部品が既存機構（G30操作登録・実行名・入口文書・既存契約の保護境界）へ接続する点を
   列挙する。
5. **正式再利用検索**：実装開始の根拠として、一操作入口を実行する（開発方針123行の定め）。

   ```text
   .venv/bin/python3 -m tools.development.formal_code_reuse_search \
     --project-root . \
     --runtime-root <repo外私有領域の絶対パス> \
     --universe .reviewcompass/policies/work4a-source-universe-v<最新>.json \
     --policy .reviewcompass/policies/work4a-freshness-policy-v<最新>.json \
     --plan <作業別計画（schema 2）のpath> \
     --captured-at <UTC時刻>
   ```

   - 作業別計画（能力宣言）はHuman確認の下で作成し、確定commitへ先行commitしてから実行する。
   - `digest_mismatch`で停止した場合は、universe・freshness policyの方針参照が古い。正規writer
     （`write_source_universe`・`write_freshness_policy_v4`）で次版をnew-only生成して再実行する。
   - **生成された証明書（attestation）recordのpathとSHA-256を、契約候補の「権威、証拠」節へ必須で
     載せる**。`start_allowed`がtrueでない結果は実装開始の合格根拠にしない。
   - lifecycleと再利用方法（再利用・拡張・統合・分離）の裁定はHumanに残る。候補ごとの扱いは
     契約候補または作業Evidenceへ短く記す。
6. **一覧の一元化**：手順1〜5の結果（コマンド・件数・digest表・接続点・証明書参照・契約候補へ渡す
   論点）を事前走査recordへ固定し、意味単位commitする。

## 根拠

- 手順5の位置づけ：`docs/development/2026-08-02-development-policy.md`（123行からの正式検索の定め。
  規則自体は2026-08-15の同型事象を根拠に制定済み）。
- 本手順書の新設：2026-08-17、正式検索の仕組みが存在するのに作業導線から参照されず未使用となる事象が
  再発し、利用者が導線接続を指示した（設計方針・改善候補は
  `records/development/2026-08-17-vertical-a-request-builder-reuse-search-attestation-v1.json`と
  同日の改善候補recordを参照）。
