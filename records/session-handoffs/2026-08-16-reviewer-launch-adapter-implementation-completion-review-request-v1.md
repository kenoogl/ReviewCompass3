# 契約010実装 完了レビュー依頼record v1（headless起動対象・Claude→Reviewer）

- 作成日：2026-08-16
- 依頼元：Claude（操縦・実装担当）
- 依頼先：Reviewer（第1 backend `antigravity-cli`＝`agy`、許可model `gemini-3.1-pro-high`）
- 起動方式：`reviewcompass3-reviewer-launch launch`によるheadless機械起動（利用者の明示指示後）。
  fallbackは暫定手動体制（`records/development/2026-08-16-interim-gemini-review-regime-decision-v1.md`）
- レビュー種別：実装完了レビュー（契約010 §9-10。読取り専用・repositoryへの書込みなし）
- 実装基準commit：`6f3d55dd60284b4e07a58386d9aa83ee02e5cde6`

## 1. 対象と固定（SHA-256）

契約と判断record：

```text
7d159fdf093abad81481ae73eb3d95ad11efd04e2313d6df5a34c27fe583db0a  records/task-contract/2026-08-16-reviewer-launch-adapter-candidate-v2.md
351e57108293255989d345a9936cbdb122cc4f6695df7c52b4ff2856ded0a983  records/development/2026-08-16-reviewer-launch-adapter-contract-adoption-decision-v1.md
24377cd11ceae6e8182949dddd3dff3cd499e9bb1142b2746c3c5065c1b5e7b5  records/development/2026-08-16-reviewer-launch-allowed-models-approval-v1.md
9c7863e10f6fae2b654c85b17b0edb7493e47412f19218ae28ed5ee5d7ff58c5  records/development/2026-08-16-reviewer-launch-adapter-implementation-evidence-v1.md
```

実装実物：

```text
9a0f2c6136eea0c0af095f80c7e1836ba65f59c26595bd2dd27ed30007f93b83  tools/reviewer_launch/__init__.py
b1e362a7d0053404fae6366931ea0eb9e6d006bfec74bd326d9ed75a459873cf  tools/reviewer_launch/core.py
998c31d726c3aa37bd5021d83495590ad49015916ab4ca0572890465e495db8d  tools/reviewer_launch/record.py
217bf221ffa5836f1ee6c70071c90efc94b9c76c6a17ea0d8715b7fb323b8d14  tools/reviewer_launch/entry.py
ab0d29ba4cf804ad73e1b584cddc7542db5d0336c0f4d92bf67e84c437a91c21  tests/test_reviewer_launch.py
2cc7a1160adac78f71898f34e5f348ba70e4554880c4ed09b79b300be1317556  tools/operations/operation_contract_run.py
90d8932633bd3207e7aa195e075670b34632f79c5795c37ddc0599050e52e601  pyproject.toml
18c68bf4ed6f05090f9c22d0b245cf661e0b1a35c39efd424e67bec0d9529ab2  docs/development/prompts/reviewer-launch-run.md
f9300e4529745c066febb092333aee4fe57c2acabf5969850f829e95933df77b  AGENTS.md
```

## 2. 開始時の鮮度検査

起動promptが本recordのpathと期待SHA-256を渡す。`shasum -a 256`で本record自身を照合し、不一致
（mismatch）なら判定せず`freshness`へ記載して停止する。計算できない場合は`not_computable`と理由を
記載する。§1のdigest表は本record作成時点の固定値であり、対象fileの照合にも同じcommandを使ってよい。

## 3. Reviewer（あなた）への依頼：反証4点

あなたは独立したReviewerです。契約010（候補v2）の受入条件§9-1〜7に対する実装の完了レビューを、
次の4点で反証的に行ってください。各findingには根拠（file・関数名または節番号）を付けてください。

1. **受入条件と実物の対応**：契約§9-1〜7の各項が`tests/test_reviewer_launch.py`（32試験）と実装実物で
   実際に固定されているか。試験が緩い・実装と未接続・形だけの検査になっている箇所がないか。
2. **安全境界の実装抜け**：認証遮断（4環境変数）・固定引数（`--dangerously-skip-permissions`と
   `--mode`の不在検査を含む）・byte上限16,384・読み取り専用（書込みを許す引数を組み立てない）・
   raw／起動recordの上書き禁止保存・判定recordの単独commit照合について、`core.py`・`record.py`の
   実装行に即して抜け・騙し方（例：dirty樹での転記、既存record衝突、schema偽装、単独commit検査の迂回）
   が通らないかを反証する。
3. **保存分離**：未加工出力がrepository内へ置かれない実装か（`private_root_inside_repository`停止を
   含む）。commitされる判定recordには保存先種別・SHA-256・参照権限だけが載るか（`record.py`の転記）。
4. **範囲と保護**：変更が契約§8の上限内か。保護対象（契約§6）への変更が0か
   （`operation_contract_run.py`は登録9行のみが許可）。実装Evidenceの主張と実物に相違がないか。

## 4. 判定の形式

- headless起動時は、起動promptが指定するJSON schemaに完全に従う構造化出力だけで返す。
  `verdict`は5語彙（`verified`／`verified_with_findings`／`rejected`／`stale_target`／`unable`）、
  `blocking`は「製品受入を止めるべき所見」の意味、実施できなかった検査は`unexamined`配列へ明示、
  `summary`は日本語で書く。
- 手動fallback時は同じ項目（判定・findings・未検査・要旨）を日本語の文章で返し、冒頭にmodel名を記載する。

## 5. 判断済み・範囲外（蒸し返し不要）

- 実E2E（§9-8）が未実施であることは設計どおり（本レビューのheadless起動自体が実E2Eを兼ねる。
  採用judgment recordが実起動を別途の明示指示に留保している）。
- 許可model一覧は`gemini-3.1-pro-high`1件で利用者承認済み（承認record参照）。一覧の広さの当否は範囲外。
- 試験2件の出力バッファ訂正（StringIO→BytesIO）の理由は実装Evidence §1-4に記録済み。
- 契約範囲外の後続（claude-subagent／codex-cli backend・Tier 2／3受容・Reviewer書込み方式・縦A・縦C）の
  不在への指摘は不要。
- 契約§2承認境界と§7.4残余riskの最終受容は利用者の製品受入判断事項。妥当性への懸念はfindingsで
  示してよいが、受容判断そのものは本レビューの範囲外。

## 6. 手順（Human・Claude向け）

1. 利用者が実E2Eの実施を明示指示する（許可model承認は完了済み）。
2. Claudeが単体入口を実行する（外部起動はこの1回。停止時は同じ起動を繰り返さず報告する）：

```text
reviewcompass3-reviewer-launch launch \
  --repository /Users/Daily/Development/ReviewCompass3 \
  --request records/session-handoffs/2026-08-16-reviewer-launch-adapter-implementation-completion-review-request-v1.md \
  --expected-sha256 <本record commit後のSHA-256> \
  --private-root <repo外私有領域の絶対パス> \
  --run-id e2e-010-001
```

3. アダプタが未加工出力と起動recordを私有領域へ不変保存し、判定recordを
   `records/session-handoffs/2026-08-16-reviewer-launch-adapter-implementation-completion-review-verdict-v1.md`
   へ機械転記して単独commitし、事後照合4点を実行する。
4. Claudeが判定内容を利用者へ報告し、`verified`系なら製品受入（§9-11）を、blocking所見があれば対処を諮る。
