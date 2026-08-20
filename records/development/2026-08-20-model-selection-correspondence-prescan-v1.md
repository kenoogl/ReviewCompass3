# 契約016（モデル選択＋照合＋登録定型化・全backend）事前走査 v1

- 記録日：2026-08-20
- 指示者：利用者（Human）。指示文言：「統合1本（契約016：モデル選択＋照合＋登録手続き定型化・
  全backend対象）で進めてください。事前走査から入り、契約候補の範囲案まで見せてください」
  （2026-08-20 chat）
- 記録者：Claude
- 種別：契約候補定義前の事前走査（6手順。`docs/development/prompts/scope-prescan-run.md`）。
  契約定義・実装・既存文書の改定は含まない。外部送信なし
- 範囲の基準：契約015受入record §4（terra起動選択機構＝小改定・`IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`
  ＝(b)独立小作業単位）、統合の利用者裁定（本record冒頭の指示文言＝両者を同一作業単位へ統合）、
  許可model承認record（2値・一覧変更は契約改定）
- 基準commit：`74baa561d1505c2a02b7cbc3be5d04ffb02073c1`（検索計画の先行commit。走査生成物は本record
  を含むcommitで固定）
- 実測の正本：測定ブロック
  `records/development/2026-08-20-model-selection-correspondence-prescan-measurements-v1.md`（宣言
  `records/development/2026-08-20-model-selection-correspondence-prescan-commands-v1.json`。
  9項目・二重実行一致・非決定0件）。本文の数値は同fileへの参照で示し転記しない

## 0. 一枚要約（人向け）

契約016＝「起動時のmodel選択（全backend・既定は現行どおり一覧先頭）＋依頼recordの記載と実行の
対応保証（IC消化）＋新model追加手続きの定型化」。主要な発見は4つ。

1. 【実測】依頼recordの「依頼先」行は**backend名がagy直書き・modelだけ差し込み**（雛形）で、
   検査は文書全体からの正規表現検索＋**和集合所属のみ**。backend対応の穴（IC）と、正準位置
   束縛の不在（文字列理解の原則2への未達）が同じ1行に同居している——**1箇所の改修で両方直る**。
2. 【実測】起動側のmodel選択点は`launch_review`の1箇所（一覧先頭固定）。入口は既存の任意旗
   機構（`--backend`等）に`--model`を足すだけの形。RQ2装置は明示旗列で起動しており任意旗の
   追加は無影響。
3. 【実測】import元は13 file（g30・RQ2装置・**RQ2運搬部品reviewer_bridge**・運用集計・試験群）。
   公開記号（`ALLOWED_RESPONSE_MODELS`・`verdict_record_relative_path`）と入口形を変えなければ
   波及しない。和集合記号は互換のため維持する。
4. 【実測】正式再利用検索は`start_allowed: true`・直接一致46件。正準位置解析の直接前例＝
   契約013の類型推定（冒頭固定行のみを正とする）とfence状態追跡（`_classified_lines`）が
   同一module内にある。

## 1. 手順1：所在特定【実測】

行番号の正本は測定ブロック各節。

| 部品・結合点 | 所在 | 状態 |
| --- | --- | --- |
| 依頼先行の雛形 | `tools/request_builder/core.py`（「依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、許可model `%s`）」） | backend直書き・model＝和集合先頭差し込み。**backend別差し込みへの拡張対象** |
| model検査 | 同`_MODEL_PATTERN`＋`check`内の所属検査 | `.search`（文書全体）＋和集合所属のみ。**正準位置束縛＋backend別所属へ強化対象** |
| 正準位置解析の前例 | 同：類型推定（契約013＝冒頭「レビュー種別」行のみを正とする）・`_classified_lines`（fence状態追跡） | 依頼先行の正準抽出に直接流用可 |
| 組み立て入口 | `tools/request_builder/entry.py`（`--type`・`--slug`・`--title`・`--target`＋機械既定） | `--backend`・`--model`任意旗の追加対象（不在は測定で固定） |
| 起動側の選択点 | `tools/reviewer_launch/core.py`（`requested_model = allowed_models[0]`の1箇所） | 任意入力（既定＝先頭）＋backend一覧所属検査へ |
| 起動入口 | `tools/reviewer_launch/entry.py`（`_LAUNCH_FLAGS`＋任意旗集合） | `--model`追加対象 |
| 起動時の記載照合の材料 | 起動核は依頼recordのbyteを既に読む（digest束縛） | 依頼先行の正準抽出を足せば**記載と実行の一致検査**が起動前に可能 |
| 登録簿とmodel一覧 | `tools/reviewer_launch/core.py`の`BACKENDS`＋backend別許可一覧（callable） | 契約015で深化済み。登録定型化の土台 |
| 試験の承認pin | `tests/test_reviewer_launch.py`（一覧literal pin 3本＋和集合pin 2本）・`tests/test_request_builder.py`（先頭・所属を使用） | データ駆動化の対象と、**残すべき承認pin**の仕分けが論点 |

## 2. 手順2：import元【実測】

全一致行は測定ブロック「両moduleのimport元」節。import元は13 file：`tools/operations/`（g30）・
`tools/evaluation/`（rq2_paired_trial・**reviewer_bridge**・operational_metrics）・両module内部・
試験4 file。互換必須の公開記号は`ALLOWED_RESPONSE_MODELS`（和集合。維持）・
`verdict_record_relative_path`（不変）。RQ2装置・運搬部品は入口形（旗列・check出力）を変えなければ
無影響の見立て【推測・契約のRED段で機械確認】。

## 3. 手順3：Digest固定の全文検索【実測】

主題語（許可model・ALLOWED_RESPONSE_MODELS・依頼先・requested_model）の一致file数は測定ブロック
「主題語の一致file数」節を正とする。読み：「許可model」「依頼先」の一致はsession-handoffs配下の
既存依頼record群に厚い——**既存recordは改修後も検査対象になり得る**ため、後方互換（agy既定記載の
recordが従来どおり合格すること）を受入条件に含める必要がある。自己言及（本record・計画・証明書が
主題語を含む）を明記する（規律6）。

## 4. 手順4：接続点【実測】

1. **同一行での統合**：依頼先行を「backend名＋許可model」のbackend別差し込みへ変え、検査を
   （正準位置の同行から抽出したbackend・model対）→（そのbackendの許可一覧所属）へ強化する。
   ICの穴と正準位置未達を1改修で消す。
2. **起動時の対応照合**：起動核が依頼先行を正準抽出し、実際の（backend・requested model）との
   一致を検査（不一致は停止）。「同一対象集合・別名record」の合議運搬型（契約012 SR-C12-2）とは
   矛盾しない（判定record名の1対1導出により、複数判定役は元々record別名が必須）。
3. **選択入力**：組み立て`--backend`（既定agy＝現行互換）・`--model`（既定＝そのbackendの一覧
   先頭）、起動`--model`（既定＝一覧先頭）。権威は従来どおりアダプタが起動record・判定recordへ
   刻印する値（契約010 SR-C10-1）。
4. **後方互換**：既存依頼record（agy記載）はagy起動と一致するため新検査でも合格。**過去の別名
   E2E record（agy記載でcodex起動した契約015のE2E型）は新規則では不一致停止になる**——今後の
   record組み立てから新形を使う移行整理を契約に明記する。
5. **登録定型化**：許可一覧の直書き原則は維持。試験を登録簿走査のデータ駆動＋backendごとの
   承認pin 1本へ整理し、model追加の差分を「定義1行＋承認pin 1行＋承認record」に固定。手順書へ
   「モデル追加手続き」節を追記。
6. **保護**：`record.py`（判定record命名・転記）・g30・session_logs・egress・RQ2装置本体は不変。
7. **E2E**：実E2E 1回＝`--backend codex-cli --model gpt-5.6-terra`指定の組み立て→起動が自然
   （選択機構の実証とterra初起動データを同時に取得）。完了レビューはagy（Tier 1）。

## 5. 手順5：正式再利用検索【実測】

- 作業別計画（schema 2・能力4件：起動時選択・記載対応照合・正準行解析・登録定型化）：
  `records/development/2026-08-20-model-selection-correspondence-reuse-search-plan-v1.json`
  （先行commit `74baa56`）
- 一操作入口の結果：`status: completed`・HEAD `74baa561…`・**`start_allowed: true`**。一致件数の
  正本は証明書record
  `records/development/2026-08-20-model-selection-correspondence-reuse-search-attestation-v1.json`
  （SHA-256は§6のdigest表）。lifecycle・再利用方法の裁定はHumanに残る（契約候補で扱う）。

## 6. digest表（契約候補v1の固定入力）【実測】

測定ブロック「契約候補が参照するfileのdigest固定」節（15 file）を正とし、本文へ複製しない。

## 7. 契約候補v1へ渡す論点（発見事項と推奨）

1. 【実測】統合の実装単位：依頼先行のbackend別差し込み・正準位置検査・起動時照合は同じ1行を
   軸にした3点セットであり、分割すると記載と実行の不一致が過渡状態として残る。統合が自然。
2. 【判断】不一致時の停止語彙：新reason（例：`request_backend_mismatch`・`request_model_mismatch`）
   を最小追加するか、既存`model_not_allowed`系へ寄せるかは契約で確定（推奨＝新2語彙。原因の
   切り分けが速い）。
3. 【判断】既存record互換：agy既定記載の既存recordは新検査でも合格（後方互換の受入条件）。
   別名E2E型の旧recordは再起動しない前提を契約へ明記。
4. 【実測】承認pinの維持：一覧literalのpin試験はbackendごと1本へ整理して**残す**（承認record
   との束縛が正本。データ駆動化は所属・先頭不変・網羅の側だけ）。
5. 【記録】危険度：中。外部送信の対象は増えない（送信は独立確認・E2E・完了レビューの起動のみ）。
   受入済み2製品（縦B・契約011成果物）を同時に改修するため、両suiteの無変更部分の全緑と
   後方互換recordの機械証明を受入条件の柱にする。

## 8. 未実施

- 契約候補v1（契約016）の作成、5段手続き、実装、E2E（terra初起動＝利用者の明示指示事項）。
