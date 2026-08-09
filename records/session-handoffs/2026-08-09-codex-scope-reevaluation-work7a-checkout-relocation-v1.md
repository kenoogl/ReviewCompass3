# Work 7A第2項 checkout relocation scope v2 再評価record v1

- recorded_at：2026-08-09
- Pilot：Claude
- Reviewer：Codex
- collaboration mode：`role_neutral_pilot_review`
- risk：`high`（変更なし）
- verdict：`verified`
- approval：`conditional`
- blocking finding count：`0`
- implementation state：`not_started`

## 1. 対象と訂正

- scope v2：`records/session-handoffs/2026-08-09-claude-pilot-work7a-checkout-relocation-scope-v2.md`
- scope v2 SHA-256：`f127351d05bc621af95a042506dc726790ca59ecc928cec4c34257ee23d473a8`
- scope v2 commit：`4990ba64c7035d06fa77e1e3a68fb5a8d36a59f6`
- 先行scope review v2：
  `records/session-handoffs/2026-08-09-codex-scope-review-work7a-checkout-relocation-v2.md`
- 先行scope review v2 commit：`eb4b59b31f0a9f0f0f173e0d6430569b3f2c82cf`

scope v2は、Work 7A第2項を閉じないread-only Git前駆sliceとして本質的な受入境界を満たしている。
先行scope review v2の`reported_unverified`を、次の2条件を伴う`verified`へ訂正する。scope v3は要求しない。

既存のscope review v1
`records/session-handoffs/2026-08-09-codex-scope-review-work7a-checkout-relocation-v1.md`は、scope v1に
対する当時の評価として変更せず保持する。scope v1、scope v2、先行scope review v2も書き換えない。

## 2. 条件

1. scope v2のroot commit由来`repository_id`は、本前駆sliceだけで使用する**暫定lineage ID**とする。
   耐久repository identityではなく、耐久Project Binding／repository identityの確定、保存、移行、
   Work 7A第2項checkbox完了の根拠に使用しない。
2. RED Testでbase Snapshotとcandidate Snapshotを別々に固定し、Change Setの
   `base_snapshot_id`／`candidate_snapshot_id`がその2つへ束縛されること、および不一致を拒否することを
   明示する。

この2条件はscope v2の前駆slice境界とHuman裁定「分割案1」を狭めて明確化するものであり、後続の耐久Binding、
Verification Run、Work 7A第2項未完了維持を変更しない。

## 3. blocking 0の実装時確認事項

次はscope開始を止めるFindingではなく、RED／GREENと事後レビューで確認する非blocking事項へ再分類する。

1. `--no-optional-locks`をGit global optionとして正しい位置で使用する。
2. path出力のNUL区切りとrename検出thresholdを明示し、Testで固定する。
3. identity導出へ影響する利用者Git configを隔離する。

不合格なら実装・Test段階で修正し、scope v3作成や追加の事前設計裁定は要求しない。

## 4. Human境界と次

- risk `high`、実装前Human再開承認、RED／GREEN、独立事後レビューの境界は維持する。
- 本recordはscope v2の範囲レビュー合格を固定するが、RED開始の再開指示そのものではない。
- 本recordを単独commitして停止し、HumanがClaudeへRED開始を明示した後にだけ実装へ進む。
