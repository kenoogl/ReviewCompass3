# 無工具Claude疎通経路 範囲レビュー依頼 v5

- request_kind：`scope_review`
- collaboration_method：`pilot_specific_claude_codex`
- pilot：Codex主担当
- pilot_model：`gpt-5.6-sol`
- reviewer：Codexレビュー用サブエージェント
- reviewer_model：`gpt-5.6-terra`
- review_target_commit：`32ab8950428650500a9b4d9b23d318c1f7de240c`
- risk：`high`
- expected_outcome：固定対象と固定材料の照合、各課題のEvidence、必要な所見、verdict、次のHuman判断一つを
  含む、変更を伴わない独立範囲レビュー報告。期待する判定値は事前指定しない
- supersedes：`records/session-handoffs/2026-08-11-no-tool-bootstrap-scope-review-request-v4.md`

## 1. レビュー対象と入力不一致時の停止

対象は次の範囲固定v3だけである。現在の作業treeではなく、指定commitのGit blobを正として読む。

| path | SHA-256 |
| --- | --- |
| `records/session-handoffs/2026-08-11-codex-pilot-approved-claude-send-path-scope-v3.md` | `02a4f6786875a9eeb87165e387ac1e65d520423930bf3849cb967249639861a7` |

対象commit、Git blob、現在file、path、記載SHA-256のいずれかが一致しない場合は、レビュー課題へ進まない。
`verdict: reported_unverified`、`stop_reason: stale_input`とし、未評価の課題を列挙して停止する。

## 2. 固定材料と不一致時の停止

| identity | source commit | path | SHA-256 |
| --- | --- | --- | --- |
| 操縦者別連携 | `8fb50918c75bd7338a373fcf153ec917f35cf863` | `docs/development/pilot-specific-claude-codex-collaboration.md` | `aee8c8b72487e26395615c8442710b0695b035ec0aa129b4a777c6142864489d` |
| 共通レビュー | `8fb50918c75bd7338a373fcf153ec917f35cf863` | `docs/development/work-review-protocol.md` | `b7eb8f08c7b3f585d64d163a7a2f93e758e57e830bb973cc2441bfadbc98a3df` |
| 外部経路選択 | `8fb50918c75bd7338a373fcf153ec917f35cf863` | `records/session-handoffs/2026-08-11-pilot-collaboration-external-route-selection-human-decision-v1.md` | `58d7809b547b339c3641f336cc23b2729aca6e09d7d50a109ed4c7f984de7983` |
| 無工具段階選択 | `8fb50918c75bd7338a373fcf153ec917f35cf863` | `records/session-handoffs/2026-08-11-pilot-collaboration-no-tool-bootstrap-selection-human-decision-v1.md` | `3b29567232320f6751a2badd40d31b7f8ab321d731d7777f8fdd1b0f11afa0da` |
| レビューmodel裁定 | `3ce9dc32f28f98f79c9be707a96dfd4bac1547be` | `records/session-handoffs/2026-08-11-no-tool-bootstrap-review-model-human-decision-v1.md` | `5a709bff5f814595284b7540ebd842c2dec2c702ac47be9e822488f544c974c7` |
| 指示文所見Human裁定 | `2aa13852aaba1f159385e1593db488a05a0d89d5` | `records/session-handoffs/2026-08-11-no-tool-bootstrap-scope-review-prompt-findings-human-decision-v1.md` | `e63e36f9323eb1b16382cc0d3d4c560aab26ff82678ab4b172a2f9f91299d7bb` |
| SR2所見Human裁定 | `cab848ab1fb9846b556f1db0ec5ade58af3a7349` | `records/session-handoffs/2026-08-11-no-tool-bootstrap-scope-review-prompt-sr2-human-decision-v1.md` | `296aa17ca1f31a19637fd9c4d32ca9f38376f64a0ade0513d645a8639356121e` |
| SR4所見Human裁定 | `a04c1fcd7458eb2aaf41378bf429acd4c653c6a0` | `records/session-handoffs/2026-08-11-no-tool-bootstrap-scope-review-prompt-sr4-human-decision-v1.md` | `80b2d2ba322c7c9c897418a16ce2dd8143617e2c68f42a0b15f6017f03833d59` |
| 範囲固定v2独立レビュー | `f14fc60676a07ba58a5e9f84434ba9aaec36d67e` | `records/session-handoffs/2026-08-11-no-tool-bootstrap-scope-review-v1.md` | `eef8ca1cd4964a56991ff1d99adacda11acd14c3a1a0b5738780d45e650616b0` |
| 範囲レビュー所見Human裁定 | `e54fcdaec38ab4b755f67371dbbdd20604447b95` | `records/session-handoffs/2026-08-11-no-tool-bootstrap-scope-finding-human-decision-v1.md` | `8b9300c035430606586c33aad9a0c02f95d0d3e503cd01b54eb8e30e5e077bca` |
| 先行範囲レビュー | `8fb50918c75bd7338a373fcf153ec917f35cf863` | `records/session-handoffs/2026-08-11-claude-scope-review-approved-claude-send-path-v1.md` | `402b2f7af1b2b28c9dac497ec2624e6078e361cebf55730b12f8ee8784c1e1ff` |
| 外部送信設計資料 | `8fb50918c75bd7338a373fcf153ec917f35cf863` | `docs/design/2026-08-07-external-egress-gate-proposal-v4.md` | `3a82b3973f8abc947782c4bbf8e2d54713043e8e8591a543089a5824c57bcacd` |
| 旧用途の停止Decision | `8fb50918c75bd7338a373fcf153ec917f35cf863` | `records/development/2026-08-08-egress-method-conclusion-decision-v1.md` | `d9228be3ec17db82fbed694e7a6bf05b8a5d6fae52ff2353aad39aeac27dc6fc` |

固定材料は、各行のsource commitでのGit blob、現在file、記載SHA-256、commit済み状態を全件照合する。
一件でも欠落または不一致なら追加探索へ進まず、`verdict: reported_unverified`、
`stop_reason: stale_input`とし、未評価の課題を列挙して停止する。

全件一致した場合だけ、材料の選定漏れや矛盾を調べるためrepository内を追加探索できる。追加材料はpath、
SHA-256、必要だった理由を結果へ記録し、Humanの未承認判断をauthorityとして扱わない。

## 3. 独立レビュー課題

- `SR-CB-001`：対象と固定材料のGit blob、現在file、記載SHA-256を機械照合する。
- `SR-CB-002`：Human authority、risk、実装前・送信前・段完了の各境界を上流から独立に導出する。
- `SR-CB-003`：先行F1〜F4が本質的に解消されたかを確認し、表現を変えただけの未解消を探す。
- `SR-CB-004`：AC-CB-001〜013、NG-CB-001〜007、ST-CB-001〜007、OUT-CB-001〜005が、誤った合格を
  防ぐ機械判定可能な条件になっているか確認する。
- `SR-CB-005`：単一の送信前検査、固定payloadと順序、道具無効化、秘密除外、保存、一回限り承認、process
  迂回検査の境界を独立に確認する。
- `SR-CB-006`：範囲レビュー段階に比例した安全な反証を最低一件作り、外部送信、認証、Claude prompt起動を
  行わずに機械実行する。
- `SR-CB-007`：変更可能path、禁止path、TDD順序、担当分離が上流と一致するか確認する。
- `SR-CB-008`：実装手段の細部や将来段階を、根拠なくblockingへ格上げしない。

## 4. 依頼自身の受入条件

- `AC-SR-CB-001`：§1と§2の全入力が一致した場合だけ`SR-CB-002`以降へ進み、不一致時は指定判定と
  停止理由で止まる。
- `AC-SR-CB-002`：`SR-CB-002`〜`SR-CB-005`と`SR-CB-007`を、主担当の結論でなく上流材料から独立に
  評価する。
- `AC-SR-CB-003`：`SR-CB-006`の安全な機械反証を最低一件実行し、command、終了code、観測を残す。
- `AC-SR-CB-004`：所見を§5の閉じた類型と段階へ対応付け、同類型の変種を同じ周回でまとめる。
- `AC-SR-CB-005`：`SR-CB-001`〜`SR-CB-008`、先行F1〜F4、追加材料、未実施、次のHuman判断を
  `OUT-SR-CB-001`〜`OUT-SR-CB-005`へ欠落なく報告する。

課題との対応は次のとおりである。

| 受入条件 | 対応課題 |
| --- | --- |
| `AC-SR-CB-001` | `SR-CB-001` |
| `AC-SR-CB-002` | `SR-CB-002`〜`SR-CB-005`、`SR-CB-007` |
| `AC-SR-CB-003` | `SR-CB-006` |
| `AC-SR-CB-004` | `SR-CB-008`と全所見 |
| `AC-SR-CB-005` | 全課題と出力 |

## 5. 判定規則

`docs/development/work-review-protocol.md`を共通入口とする。blocking所見には、確認段階`scope`と次の閉じた
4類型のいずれかを必ず付ける。

1. 上流authorityとの矛盾。
2. Human境界または必要な承認の欠落。
3. 誤った合格を示す受入条件・検証の欠陥。原則として機械反証を付ける。
4. 禁止事項、範囲、schema境界の破り。

列挙外はnon-blockingとし、確認すべき段階を示す。同じ欠陥類型の変種は同じ周回でまとめて確認する。
主担当の結論や期待判定を推測せず、上流材料から独立に判定する。

判定は次のいずれか一つとする。

- `verified`：必須証拠が揃い、blocking所見がなく、報告と事後状態が一致する。
- `reported_unverified`：blocking所見または必須証拠・再現条件の不足がある。
- `report_execution_mismatch`：報告と事後状態の競合Evidenceがある。

## 6. 禁止事項

- `NG-SR-CB-001`：対象、production code、test、TODO、既存recordを変更しない。
- `NG-SR-CB-002`：Claude Code、外部API、browser、network、認証操作、外部送信を使わない。
- `NG-SR-CB-003`：実装、RED作成、所見修正、Human判断の代行を行わない。
- `NG-SR-CB-004`：秘密値を読まず、表示せず、保存しない。
- `NG-SR-CB-005`：主担当の期待や先行レビューの結論をoracleとして採用しない。

## 7. 停止条件

- `ST-SR-CB-001`：§1または§2の一件でも不一致なら`reported_unverified`／`stale_input`で停止し、
  `SR-CB-002`以降を実行しない。
- `ST-SR-CB-002`：禁止操作なしに必要Evidenceを得られない場合は禁止操作を行わず、`reported_unverified`で
  停止する。
- `ST-SR-CB-003`：上流authorityが競合し、追加探索でも優先関係を解決できない場合は推測で埋めず、
  `reported_unverified`で停止する。
- `ST-SR-CB-004`：報告と事後状態の競合Evidenceを得た場合は、競合を列挙して
  `report_execution_mismatch`で停止する。

## 8. 出力要件

- `OUT-SR-CB-001`：`verdict`、`stop_reason`、レビュー担当model、対象commit、対象Digestを示す。
  正常完了時の`stop_reason`は`none`とする。
- `OUT-SR-CB-002`：実行した機械確認と、安全な反証を、単独commandごとの終了code・要約とともに示す。
- `OUT-SR-CB-003`：`SR-CB-001`〜`SR-CB-008`と`AC-SR-CB-001`〜`AC-SR-CB-005`ごとの結果と
  Evidenceを示す。
- `OUT-SR-CB-004`：blocking所見とnon-blocking所見を分ける。blocking所見は固有ID、段階、4類型、事象、
  機械反証、影響、必要な最小措置を持つ。所見がなければ`なし`と示す。
- `OUT-SR-CB-005`：先行F1〜F4を`closed | open | superseded`で示し、追加探索材料、file変更・Claude起動・
  外部送信の未実施確認、次に必要なHuman判断一つを示す。

日本語のMarkdownで`OUT-SR-CB-001`〜`OUT-SR-CB-005`の順に返す。結果fileを作らず、応答だけを返す。
