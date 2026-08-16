# Reviewer起動アダプタ 契約候補v2 独立確認依頼record v1（Claude→Gemini・Human中継）

- 作成日：2026-08-16
- 依頼元：Claude（操縦・契約候補v2の作成担当）
- 依頼先：Gemini（暫定体制。本repositoryのディレクトリを共有しており、対象fileを直接読める）
- 体制根拠：`records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md`
- レビュー種別：実装開始前の契約定義反証（読取り専用・repositoryへの書込みなし）

## 1. 対象と固定

- 対象契約候補：`records/task-contract/2026-08-16-reviewer-launch-adapter-candidate-v2.md`
  - SHA-256：`7d159fdf093abad81481ae73eb3d95ad11efd04e2313d6df5a34c27fe583db0a`
- 起草側自己レビュー（第1・2段。v1→v2の訂正根拠SR-C10-1〜4）：
  `records/development/2026-08-16-reviewer-launch-adapter-v1-self-review-v1.md`
  - SHA-256：`3fadb74967e52fb6bc9a19b3099db12324b2e52c983fc60207b7587534b8cd8f`
- 事前走査追補（agy実測。契約の環境前提）：
  `records/development/2026-08-16-vertical-b-prescan-agy-addendum-v1.md`
  - SHA-256：`2f5cdec3c2470ed54cd0df58cd46afa47353c6d159ba97c7494b19f65bf760f8`
- 参考（契約の入力。本依頼では鮮度検査不要）：統合検討
  `records/development/2026-08-16-review-tooling-formalization-study-v1.md`、縦B事前走査v1
  `records/development/2026-08-16-vertical-b-reviewer-launch-adapter-prescan-v1.md`
- 参考（流用元。本契約では変更しない）：`tools/development/claude_implementation_executor.py`、
  `tools/bootstrap/raw_review_store.py`、`tools/operations/operation_contract_run.py`

## 2. 開始時の鮮度検査（Gemini（あなた）が最初に行う）

1. §1の3 file（契約候補v2・自己レビュー・事前走査追補）のSHA-256を機械計算し
   （例：`shasum -a 256 <path>`）、本record記載値との一致を確認する。
2. 不一致の場合は、レビューせずその旨を判定文へ書いて停止する。

## 3. Gemini（あなた）への依頼：反証4点

あなたは独立したレビュアです。対象契約候補v2を読み、次の4点をそれぞれ反証的に検査し、判定を返して
ください。各主張には根拠（契約の節番号、必要なら流用元fileの関数名・行）を付けてください。

1. **機械層の一意性**：§7（起動の固定形・判定schema・事後照合4点）と§8（変更上限）に、実装者が後決め
   できる曖昧さ・矛盾・漏れがないか。特に自己レビューの訂正2件——SR-C10-1（`tier`をschemaから外し
   アダプタ判定へ一本化）とSR-C10-2（鮮度の硬い関門をアダプタの二重再計算とし、Reviewerの`freshness`へ
   `not_computable`を許容）——の反映後、§7.2と§7.3が食い違いなく一意に実装できる書き方になっているか。
2. **読み取り専用境界の抜け**：§2と§7.1の組（書込み禁止・`--dangerously-skip-permissions`使用禁止・
   書込みを許す`--mode`の禁止・禁止環境変数4種・起動prompt byte上限・自動再試行なし・別経路への自動
   切替なし）に、repositoryを読める外部agentのheadless起動の安全境界として漏れがないか（例：`--mode`
   既定値の挙動が書込みを許す形、環境変数以外の認証経路、sandbox扱いがRED実測待ちであることの間隙、
   あなたが考えるその他の形）。発見した形は§10停止条件またはRED実測項目への追加として提案してよい。
3. **残余riskと承認境界の妥当性**：§7.4の残余risk 3点（repository読取り＝Googleへの内容送出・agy実挙動の
   不確実性・Tier 1でも残るmodel依存）が記載の緩和とセットで受容可能な水準か。§2の承認境界（起動ごとの
   追加承認なし。起点は利用者のchat指示）が、契約008 v5 §2の前例と暫定体制の実績（利用者自身の手動
   Gemini利用）の下で妥当か。受容できないと考える場合は、運搬0回の実用を壊さない最小の追加統制
   （例：起動ごとのHuman承認）を提案する。
4. **縮小境界と上位整合**：Tier 1限定・読み取り専用・機械転記の方式が、統合検討§4.2（tier一般化の型）・
   §5（縦切り3本）・§6（横串3観点）およびwork-review-protocol §5（同一モデル系サブエージェントを
   `high`の唯一の独立oracleにしない）と矛盾しないか。第2縦切り（claude-subagent・Tier 2／3受容）への
   送り分けが明確か。受入条件11項、特に§9-8（実E2E 1回）で確かめる項目に不足がないか。

## 4. 判定の形式（あなたに求める出力）

- 判定：`開始可`または`修正要`
- `修正要`の場合：同じ原因の変種をまとめた最小数の停止原因と、各原因の最小修正案
- 実施できなかった検査があれば「未検査」として明示する
- 判定文の冒頭にあなたのmodel名を記載し、日本語で返す

## 5. 判断済み・範囲外（蒸し返し不要）

- 判断済み：縦Bの採用と第1 backend＝agy（利用者決定）。転記方式＝案B読み取り専用（3案比較で選定。
  契約§4）。Tier 1限定・Tier 2／3の受容機構は第2縦切り。gemini-cli→agyの訂正（利用者提供事実。
  統合検討§9）。判定基準（work-review-protocol）不変。暫定手動体制はfallbackとして残置。
- 範囲外（「無い」という指摘は不要）：依頼組み立て器（縦A）・prompt品質gate（縦C）・claude-subagent／
  codex-cli backend・Reviewer書込み方式・外部API直接送信経路の後続（pending）・実行段階台帳の一括実装・
  歴史的recordの書き換え。
- 判定recordの着地先は`records/session-handoffs/`（統合検討§6.3の利用者確定）。本sessionの手動体制で
  判定recordを`records/development/`へ置いた実績と異なるが、正式ツールの着地先として確定済みである
  （相違の指摘は不要）。
- 残余riskを0にすることは本契約の目的ではない（運搬0回の機械化と安全境界の均衡点を契約固定するのが
  目的。最終の受容判断は利用者が行う）。

## 6. 手順（Human・Claude向け）

1. 利用者がGeminiへ本依頼recordのpath
   （`records/session-handoffs/2026-08-16-reviewer-launch-adapter-v2-review-gemini-request-v1.md`）を伝える。
2. Geminiは§2の鮮度検査→§3の反証4点を行い、§4の形式で判定文を返す。
3. 利用者が判定文をClaudeへ貼り戻す。Claudeが判定record
   `records/development/2026-08-16-reviewer-launch-adapter-v2-independent-review-v1.md`へ転記・commitし、
   根拠と実物の整合を機械照合する。
4. `開始可`なら利用者へ縮小境界の採用と実装開始を一判断として求める。`修正要`なら停止して利用者へ諮る。
