# 文字列理解の失敗類型と対策原則（参照record） v1

- 作成日：2026-08-17
- 記録者：Claude
- 種別：参照record（契約起草・機械検査設計の必読入力。事前走査手順書
  `docs/development/prompts/scope-prescan-run.md`から接続）
- 採用根拠：利用者指示（2026-08-17 chat）
  > 推奨どおり：原則の参照recordを作成し、事前走査手順書へ必読として接続して。
  > fixture標準化は改善候補登録のみ

## 0. 問題の定義

メッセージ・record・文書に**書かれた文字が、読み手（機械解析器・LLM・人）に正しく伝わらず**、
解釈失敗・誤解釈・手戻りが生じる。初代ReviewCompass〜RC2のAPIレビュー運用で反復した失敗であり、
RC3でも契約011のfence騙され（三度目の再発）として現れた。新しい部品——文書を機械解析する検査器、
LLMが読み書きするrecord、外部へ送るメッセージ——を設計するときは、必ず本recordの原則へ照らす。

## 1. 失敗の3層と実例

| 層 | 何が起きたか（実測例） | 対策の方向 |
| --- | --- | --- |
| 運搬層（byteが壊れる） | 末尾空行・CRLF・BOMでdigest変動。バッククォートとshellの衝突で送信前失敗 | 決定的正規化・shell非経由・digest束縛 |
| 構造層（区切りが騙される） | fence内の偽見出しで節解析打ち切り。fence外の構造行を誤取得。応答全体のfence包みでparse失敗。本文中の契約見出しを誤認 | 正準位置のみ許可・構造lint・fence状態追跡・敵対fixture |
| 意味層（読み手が解釈できない） | 82KB×網羅観点で思考爆発・6連続失敗・成果ゼロ。LLMがYAML契約を守れない（未引用コロン・裸の配列） | 規模上限と分割・構造化出力の強制・fail-closed・raw先行保存 |

## 2. 対策原則（8項）

1. **fail-closed**：送る前・使う前に機械で検査し、不合格なら送らない・使わない。**自動変形で
   救済しない**（変形は新たな解釈差を生む）。
2. **正準位置の原則**：構造要素（見出し・digest行・fence）は正準の位置だけを正とし、それ以外の
   位置に現れたら拒否する。
3. **本文を運ばない**：可能な限り、内容そのものではなく**場所（path）＋照合値（SHA-256）**を渡し、
   読み手が自分の読取り道具で原本を読む。運搬層の問題は頑健化でなく方式の廃止で消す。
4. **決定的正規化と照合値束縛**：同一内容は常に同一byteへ（UTF-8・LF・末尾LF1個）。原本は
   digestで束縛し、不一致は停止（stale）。
5. **読み手の分離と構造化出力**：機械が読む部分（正準JSON）・LLMが読む部分・人が読む部分を
   分ける。LLMの出力はschema検証つき構造化出力を第一とし、自由文からの抽出は最後の手段。
6. **raw先行保存**：解釈・検証より**前に**未加工出力を保存する。解釈に失敗しても実物を持ち帰って
   再解析・裁定できる。解釈できない場合は黙って進まず、正直に申告して止まる（例：freshnessの
   `not_computable`申告）。
7. **規模上限と分割**：読み手の解釈力は入力規模×課題量に依存する。実測目安45KB以下。
   巨大単一文書×網羅観点の組合せを禁止し、超過は分割する。
8. **敵対fixtureの標準化**：既知の失敗類型（§3）を**先に失敗する試験**として固定してから対策を
   実装する。新しい解析器には騙し方fixtureを標準で付ける。

## 3. 既知失敗8類型（RC1 issue 2026-07-17の列挙より）

(1) 末尾空行・改行形式・BOM・行末空白によるbyte digest変動、(2) バッククォートとshell文字列の
衝突による検査開始前失敗、(3) **入れ子コードフェンスや本文中見出しを制御構造と誤認する境界解釈**、
(4) YAMLの未引用コロン・裸の配列・コードフェンス付き応答によるparse失敗、(5) raw byte差と意味同一の
区別欠如による不要な再実行、(6) server非対応schema語彙によるモデル実行前拒否、(7) 巨大単一Markdown×
網羅観点によるtimeout・思考token枯渇、(8) prompt本文・実行引数・表示用commandの同一文字列層への混在。

## 4. RC3での体現（2026-08-17時点。同日、契約013実装の反映を追記——e2e-013-001所見
SEC4-OUTDATED-FREE-TEXTの採用）

- 原則3：Reviewer起動はpath＋SHA-256だけを渡し、レビュー役が読取り道具で読む（契約010/012）。
  本文同梱方式は廃止済み。
- 原則1・2：依頼recordは機械生成（assemble）→LLM記入は限定2箇所→check（節構造・digest表・
  placeholder・機微・**fence状態追跡**）合格まで起動対象にしない（契約011）。**類型推定は正準位置
  （冒頭「レビュー種別」行）だけを正とし、本文中のlabel出現では判定しない**（契約013・SR-C13-1）。
- 原則4：依頼recordはcommit＋SHA-256束縛。起動時に不一致なら`request_record_stale`停止。
- 原則5：判定はJSON schema検証（`validate_verdict`）。抽出不能・不適合は
  `verdict_schema_nonconforming`停止。
- 原則6：未加工出力は照合・抽出より前にrepo外私有領域へ保存。判定recordは機械転記＋事後照合4点。
- 原則7：prompt byte上限16,384（対象本文は運ばないため小さい）。
- 原則8：fence騙され2形（fence内偽見出し・fence外digest行）と停止系fixtureを標準試験化。契約013で
  自由記入節への敵対fixture（fence内偽見出し・fence外digest行の拒否・他類型labelの本文混入で推定が
  騙されない）を追加。**類型網羅の体系化は未了**（改善候補`IC-ADVERSARIAL-FIXTURE-CATALOG-001`＝
  採用済み・縦C RED段要求へ組み込み）。

## 5. 系譜・出典（横repository。2026-08-17の横断検索で特定）

- 観測（初代ReviewCompass `/Users/Daily/Development/ReviewCompass/.reviewcompass/`）：
  `evidence/backlog/issues/issue-2026-07-06-output-contract-heading-false-positive-breaks-review-parsing.yaml`・
  `…/issue-2026-07-10-api-review-parse-failure-recovery-design.yaml`・
  `…/issue-2026-07-11-review-target-delivery-format-carries-failure-factor.yaml`・
  `backlog/issues/issue-2026-07-17-review-message-envelope-canonicalization-and-transport-contract.yaml`（8類型の初出）
- 形式設計（同上）：`specs/workflow-management/design.md` 328行〜（input-delivery／role-banking＝
  部分割45KB・送信前fence整合lint・fail-closed）・
  `stages/completed/reopen-procedure-2026-07-12-review-run-input-redesign.yaml`・
  `stages/completed/maintenance-2026-07-13-run-role-response-envelope-raw-first.yaml`（raw先行保存）・
  定量台帳`docs/notes/api-review-exchange-log-analysis/README.md`（45KB以下213回中失敗1・60KB超459回中18）
- 再構築設計（ReviewCompass2）：`docs/design/2026-07-23-review-method-variations.md`（方式が違っても
  同一成果物形式へ合流）・`docs/plan/2026-07-23-plan-c-rebuild-minimal-base.md` 119行〜・
  `.reviewcompass/specs/requirements-f2.md` R-F2-017〜022・`.reviewcompass/specs/design-f2.md`
  D-F2-010／D-F2-011（版つき正規化封筒・3層分離・shell非経由転送）・
  `.reviewcompass/evidence/reviews/2026-07-25-ref-impl-enforced-rules.json`（`fence_unbalanced`・
  `fence_unshielded`・正準単一fence）
- 運用適用（LLMGP）：`WindTurbineWake/LLMGP/.reviewcompass/specs/_cross_feature/reviews/2026-07-27-requirements-redraft-triad-review/api-review-criteria-three-features.md` 326行
- RC3での再発と修正：`records/development/2026-08-17-request-builder-e2e-evidence-v1.md` §2〜3
  （fence状態追跡・敵対試験2件・commit `442b05f`）

## 6. 未了・関連

- 敵対fixtureの類型網羅：`IC-ADVERSARIAL-FIXTURE-CATALOG-001`（Human仕分け待ち）。
- 記載modelと実行backendの対応検査：`IC-REQUEST-BUILDER-MODEL-CHECK-SCOPE-001`（登録済み）。
- 2つの読み手の判定不一致の裁定：縦C（合議）の領分。
