# Scope prescan run

契約候補（範囲固定）を定義する前の事前走査の共通手順である。LLMは意味分析だけを行い、件数・digest・
検索・Git確認は機械処理を使う。結果は事前走査recordへ一元化し、意味単位commitで固定してから
契約候補の作成へ進む。

## 必読入力

- [文字列理解の失敗類型と対策原則（参照record）](../../../records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md)
  ——文書の機械解析・LLMの読み書き・外部送信メッセージを含む部品を扱う契約候補は、起草前に
  この原則（fail-closed・正準位置・本文を運ばない・raw先行保存・規模上限・敵対fixture等）へ
  照らす（利用者指示2026-08-17）。

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
     --plan <作業別計画（schema 2）のpath>
   ```

   - 保存先・方針file（universe・freshness policy）の版・時刻は**ツールが自動解決する**
     （保存先＝home基準の既定値、方針file＝数値最大版、時刻＝機械記録。2026-08-18のCLI既定値化。
     手組み立て誤指定事故＝`records/development/2026-08-18-placement-root-resolution-evidence-v1.md`
     §5の構造的再発防止）。上書き用の任意引数はあるが、通常は使わない。
   - 作業別計画（能力宣言）はHuman確認の下で作成し、確定commitへ先行commitしてから実行する。
   - `digest_mismatch`で停止した場合は、universe・freshness policyの方針参照が古い。正規writer
     （`write_source_universe`・`write_freshness_policy_v4`）で次版をnew-only生成して再実行する。
   - **生成された証明書（attestation）recordのpathとSHA-256を、契約候補の「権威、証拠」節へ必須で
     載せる**。`start_allowed`がtrueでない結果は実装開始の合格根拠にしない。
   - lifecycleと再利用方法（再利用・拡張・統合・分離）の裁定はHumanに残る。候補ごとの扱いは
     契約候補または作業Evidenceへ短く記す。
6. **一覧の一元化**：手順1〜5の結果（コマンド・件数・digest表・接続点・証明書参照・契約候補へ渡す
   論点）を事前走査recordへ固定し、意味単位commitする。

## 数値の記録規律（機械化の原則）

recordへ書く数値は機械出力の転記だけを認め、手作業の余地を残さない。

1. 数値には**再現コマンドを併記**する。併記できない数値はrecordへ書かない（併記の無い数値行は
   誤りの兆候として扱う）。
2. 数えるときは**数える専用コマンド**（`wc -l`・`grep -c`等）の**全出力**をそのまま転記する。
   `head`等で途中省略された表示から数字を書かない。省略された残りを推測で補わない。
3. 他recordの数字を**別の母集団へ流用しない**。母集団が変われば数え直す（実例：RQ2の「31実行の
   機械記録」＝実起動30＋起動前停止1をlaunch保存数と混同し「49（あり31）」と誤記。機械実測は
   48（30＋18）。`records/development/2026-08-18-operational-metrics-evidence-v1.md` §4）。
4. 抽出定義（正規表現等）を作る前に、対象corpus**全体**の形を機械調査する。目にした実例だけから
   定義しない（実例：承認文言行の定義が見出し形式を数え漏らし7→35。
   `records/development/2026-08-18-operational-metrics-v2-evidence-v1.md` §4）。
5. コマンド引数の正準値は、可能な限り**ツールの既定値へ実装して引数ごと消す**（実例：正式検索の
   保存先・方針版・時刻は自動解決済み）。それでも残る引数は手順書・recordから転記し、手で
   組み立てない。
6. 計測対象に自分の記録が入る**自己言及**（事前走査recordが検索語を含む等）は誤りではないが、
   毎版明記する。

## 根拠

- 手順5の位置づけ：`docs/development/2026-08-02-development-policy.md`（123行からの正式検索の定め。
  規則自体は2026-08-15の同型事象を根拠に制定済み）。
- 本手順書の新設：2026-08-17、正式検索の仕組みが存在するのに作業導線から参照されず未使用となる事象が
  再発し、利用者が導線接続を指示した（設計方針・改善候補は
  `records/development/2026-08-17-vertical-a-request-builder-reuse-search-attestation-v1.json`と
  同日の改善候補recordを参照）。
- 数値の記録規律の節と`--runtime-root`正準値の明記：2026-08-18、事前走査recordでの推測転記
  （母数誤り）・定義漏れ・引数誤指定が同日に3件重なり、利用者が「手作業の余地がないように機械化
  するのが正しいアプローチ」として追記を指示した（各事故の記録は節内の参照record）。
