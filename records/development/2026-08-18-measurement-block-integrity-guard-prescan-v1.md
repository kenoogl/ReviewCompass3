# 測定ブロック完全性guard 事前走査 v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。文言「(a)で進めてください。完全性guardを先に」（2026-08-18 chat）
- 記録者：Claude
- 発端：非決定的欠落の観測record
  `records/development/2026-08-18-measurement-block-nondeterminism-observation-v1.md`
  （同一宣言のgrepが1回目10件・2回目22件。根因未確定）
- 基準commit：`2131ae5`（作業tree clean。未commitの不完全生成物2件は本単位の受入で差し替える）
- 実測の注記：**修理対象が測定tool自身のため**、本走査の実測は規律2の例外（数える専用コマンドの
  全出力転記・再現コマンド併記）で行う

## 1. 手順1〜3：所在・波及・digest【実測・出力全転記】

`shasum -a 256`（上記コマンド併記）の出力そのまま：

```text
2fb69a27d4b1449cfb61c52ecffda3dde385fdf8299eac7c65396a5da45118e4  tools/development/measurement_block.py
362ed3807083a0f9dcf03c5e52a43bda36b74390cebbecc37a5a6490a40120d3  tests/test_measurement_block.py
aabdd3ee4c5c7626edce96559f91c97b9e30e1078ece04212a0f725a596f5abf  docs/development/prompts/scope-prescan-run.md
```

`grep -rln "measurement_block" tools/ docs/`（__pycache__除外）＝参照元は tool 本体・作業票・
手順書の3件のみ。試験は`tests/test_measurement_block.py`7本（本日新設・RED/GREEN済み）。
他moduleからのimportは無い（波及なし）。

## 2. 手順4：設計（作業票へ渡す論点）

1. **二重実行guard**：各entryを2回実行し、（終了コード・stdout・stderr）の完全一致を機械比較。
   - 一致→従来どおり1回分を記録し「完全性：二重実行一致」を機械記載。
   - 不一致→entryを`non_deterministic`とし、**両回の出力を全文記録**（法医学的証拠）。summaryへ
     `non_deterministic_count`を追加し、1件でもあれば状態`incomplete`・終了コード1（黙って
     信用しない）。
   - 1回目がspawn失敗・timeoutなら2回目は行わない（従来どおり不完全・1）。2回目だけ実行不能に
     なった場合も不一致として扱う。
   - elapsedは1回目の値を記録（比較対象にしない。実行時間は本質的に揺れる）。
2. **実行体の機械記録**：`shutil.which(argv[0])`で解決した**絶対path**を各entryへ機械記載
   （未解決は「未解決」）。shell wrapperとPATH実体の差（観測recordの根因候補）を以後は生成物
   自体が切り分け材料として持つ。
3. **環境依存への考慮**（利用者指摘2026-08-18「デプロイ先の環境依存の点を考慮しなければ
   ならない」＋根因調査v1 §3）：
   - 実行体の絶対path記録は、デプロイ先でOS・PATH・同名別実装（BSD／GNU grep等）が変わる
     ことへの開示機構を兼ねる。
   - 生成物headerへ**実行環境の機械記録**（`platform.platform()`＝OS種別と版）を追加し、
     測定fileが「どの環境の事実か」を自己申告する（測定は環境に束縛された記録である、の明文化）。
   - コスト検討の帰結として「**測定コマンドは読み取り専用に限る**」を要件へ格上げし手順書に明記
     （二重実行で副作用が2回走ることの構造的防止は宣言者の責務とする）。
4. 手順書の該当注記へ「二重実行の完全性guard・実行体と実行環境の機械記録・読み取り専用限定」を
   追記。
4. **観測事例での実証（dogfooding）**：欠落を起こした当の宣言file
   （`…plan-writer-prescan-commands-v1.json`・SHA-256 `c474a388…`）をguard付きtoolで再実行し、
   完全な生成物へ差し替えて本単位でcommitする（対策2再開の入力を兼ねる）。

## 3. 手順5：正式再利用検索

作業別計画の先行commit後、`--plan`のみで実行。証明書は
`records/development/2026-08-18-measurement-block-integrity-guard-attestation-v1.json`へ固定。
計画JSONのdigest埋め込みは対策2未完のため手書きscript実行を継続する（既知の例外・対策2で排除）。

## 4. 未実施

- 手順5の実行、作業票の適用、RED、GREEN、手順書追記、実証差し替え、Evidence、TODO反映。
