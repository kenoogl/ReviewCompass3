# 計画JSON writer（対策2）事前走査 v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。文言「対策2（計画JSON writer）に着手してください。事前走査から」→
  guard先行の裁定を経て「対策2（計画JSON writer）を再開してください」（2026-08-18 chat）
- 記録者：Claude
- 上位：精査record`records/development/2026-08-18-llm-machine-split-audit-v1.md` §4-2
- 基準commit：`0c5d1eb`（作業tree clean）
- 実測：測定ブロック
  `records/development/2026-08-18-plan-writer-prescan-measurements-v1.md`（**完全性guard付きで
  再生成済みの完全版**。中断前の初回生成は非決定的欠落を含み破棄——観測・調査recordを参照）

## 1. 実測と読解から確定した事実

1. 既存の正規writer前例＝`work4a_rebuild_v3.py`（universe・policyのnew-only版生成）。
2. 検索側の計画検証は`formal_code_reuse_search._validate_plan(document, project_root)`に
   一元化されている（fields完全一致・digest一致・capability検証・attestation新規性まで）。
   **writerはこれを丸ごと再利用**でき、複製禁止と「writerで仕上げた計画は検索で落ちない」の
   両方を満たせる。
3. 正準digestは`tools.common.digests.canonical_content_digest`（work4a `_content_digest`は
   同関数への束ねであることを掃引試験が固定済み）。
4. 手書きheredocの実例母数＝committed計画record群（測定ブロックの完全一覧を参照。22件超）。
   本作業単位の計画1件が**最後の手書き**となる（writerが無いと作れないため）。

## 2. 設計（作業票へ渡す論点）

1. 新設：`tools/development/reuse_search_plan.py`。subcommand 2つ：
   - `finalize --plan <draft>`：`content_digest`の**無い**草稿を読み、digestを機械埋め込み→
     `_validate_plan`（検索と同一）→**合格時のみ**fileを書き換える（不合格時は無変更）。
     digest既存は`already_finalized`で停止（終了コード2）。
   - `verify --plan <path>`：完成計画の構造とdigestを照合。証明書（attestation）が既に存在する
     のは**検索実施済みの正常状態**として合格に含める（`output_already_exists`のみ許容。
     複数search計画では後続searchが未検証で終わる限界を明記）。
2. 出力は一行JSON・終了コード0／2／1（repo規約）。`--project-root`既定は`.`（cwd＝repository
   根元からのmodule起動の政策どおり。デプロイ先でも正しい側）。
3. 手順書`scope-prescan-run.md`手順5へ「計画はfinalizeで仕上げる（手書きscriptを使わない）」を
   追記。
4. dogfooding：committedの**全計画recordをverifyで機械照合**（読み取り専用＝測定ブロック適合）
   し、歴史的な手書きdigestに誤りが無いことを一括実証する。

## 3. 手順5：正式再利用検索

作業別計画の先行commit後、`--plan`のみで実行。証明書は
`records/development/2026-08-18-plan-writer-attestation-v1.json`へ固定。本計画のdigest埋め込みは
**最後の手書きscript実行**とし、GREEN後に本計画自身をverifyで機械照合する。

## 4. 未実施

- 手順5の実行、作業票の適用、RED、GREEN、手順書追記、dogfooding、Evidence、TODO・見取り図反映。
