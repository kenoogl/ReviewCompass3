# 契約011 実運用E2E・完了レビューEvidence v1

- 記録日：2026-08-17
- 記録者：Claude
- 実施根拠：利用者の明示指示「E2Eを実施して（組み立てから起動e2e-011-001まで）」→blocking所見の報告後
  「所見2を修正して、e2e-011-002で再起動まで進めて」（いずれも2026-08-17 chat）
- 結果：**§9-8（実運用E2E）と§9-10（完了レビュー）が成立**。最終判定`verified`（findings＝確認型info
  3件・blocking 0件・unexamined空）

## 1. 一往復目（e2e-011-001）【実測】

- `reviewcompass3-request-builder assemble`が本契約自身の完了レビュー依頼recordを機械生成
  （digest表11行・基準commit・判定record導出名）。LLM記入は反証点4件と判断済み・範囲外のみ。
- 契約§7.2の再実行性を実測：commit前checkは`request_record_uncommitted`のみ→commit（`ab4c692`）→
  check全項目合格（sha256 `487ba7e9…`）→縦B起動→判定record機械転記・単独commit（`cc9b429`）・
  事後照合4点合格。**縦A出力→縦B入力の接続が本番完走**。
- 判定は`verified_with_findings`で、**blocking所見1件**（severity high）：checkの節・digest行解析が
  コードfenceの内外を区別しない（fence内の偽見出しで節解析が騙され、fence外のdigest行が数えられる）。
  引用行・関数名は正確で、起草側のコード再読でも実在を確認した。確認型所見3件（受入対応・流用保護・
  Evidence整合）は肯定的確認。

## 2. 再発類型の確認【記録・実測】

利用者の指摘により、本穴が**文書形式解析の再発類型**（API レビュー時代にも発生し議論済み）であることを
確認した。前例の実在を横repositoryで実測：ReviewCompass2の
`.reviewcompass/evidence/reviews/2026-07-25-ref-impl-enforced-rules.json`（実装
`tools/api_providers/trusted_review_send.py`）に`fence_unbalanced`・`fence_unshielded`・
「response must use one canonical YAML fence」の強制規則が存在する。原則は「構造要素は正準の位置だけを
正とし、それ以外は拒否する」であり、本修正はその RC3側適用である。

## 3. 修正（利用者採用）【実測】

- RED先行：騙し方2件（fence内偽見出し・fence外digest行）を失敗試験として固定し、修正前実装で
  2失敗を機械実証。
- 修正：行分類をfence状態追跡（`_classified_lines`／`_section_lines`）へ変更。見出し判定・反証点番号・
  記入内容はfence外だけを正、digest表はfence内だけを正とし、fence外のdigest行は
  `digest_row_outside_fence`で明示拒否。
- 検証：対象32件・関連123件・正規全試験2,442件 各単独終了コード0。commit `442b05f`。

## 4. 二往復目（e2e-011-002）【実測】

- 修正版builderで再レビュー依頼を再生成（digest表12行。前回判定recordを対象へ追加・基準commit
  `442b05f`）。旧依頼recordは修正でcore.py等のdigestが変わったため設計どおりstale。
  commit（`be47ec0`）→check合格（sha256 `f4cc56dd…`）→縦B起動。
- 判定：**`verified`**。3所見はすべて確認型（fence追跡と敵対試験の実効・回帰なし・前回確認事項の維持）、
  対象commitは修正commitを正しく参照、unexamined空。判定record機械転記・単独commit（`67349d7`）・
  事後照合4点合格。

## 5. 受入条件の充足状況

- §9-1〜7：実装Evidence（2026-08-17）＋本record §3（修正のRED→緑）で充足。
- §9-8：**成立**（assemble→記入→check→commit→起動→転記→照合の全経路を2往復で実測。Human運搬0回）。
- §9-9：全試験2,442件成功・終了コード0。保護対象は基準から差分0（許可されたG30登録9行のみ）。
- §9-10：**成立**（e2e-011-002の`verified`・blocking 0件）。
- §9-11：未実施。利用者の製品受入（§7.4残余risk 4点の最終受容）の判断待ち。
