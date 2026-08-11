# 無工具Claude疎通経路 範囲レビュー依頼 v1

- request_kind：`scope_review`
- collaboration_method：`pilot_specific_claude_codex`
- pilot：Codex主担当
- pilot_model：`gpt-5.6-sol`
- reviewer：Codexレビュー用サブエージェント
- reviewer_model：`gpt-5.6-terra`
- review_target_commit：`8fb50918c75bd7338a373fcf153ec917f35cf863`
- risk：`high`
- expected_outcome：未指定

## 1. レビュー対象

対象は次の範囲固定v2だけである。現在の作業treeではなく、指定commitのGit blobを正として読む。

| path | SHA-256 |
| --- | --- |
| `records/session-handoffs/2026-08-11-codex-pilot-approved-claude-send-path-scope-v2.md` | `aefa05876b38a5b192d923f43dc17609678053ca33a4936b992e8a6646845c82` |

対象commit、path、SHA-256のいずれかが一致しなければレビューを開始せず、`stale_input`として報告する。

## 2. 固定材料

| identity | path | SHA-256 |
| --- | --- | --- |
| 操縦者別連携 | `docs/development/pilot-specific-claude-codex-collaboration.md` | `aee8c8b72487e26395615c8442710b0695b035ec0aa129b4a777c6142864489d` |
| 共通レビュー | `docs/development/work-review-protocol.md` | `b7eb8f08c7b3f585d64d163a7a2f93e758e57e830bb973cc2441bfadbc98a3df` |
| 無工具段階選択 | `records/session-handoffs/2026-08-11-pilot-collaboration-no-tool-bootstrap-selection-human-decision-v1.md` | `3b29567232320f6751a2badd40d31b7f8ab321d731d7777f8fdd1b0f11afa0da` |
| 先行範囲レビュー | `records/session-handoffs/2026-08-11-claude-scope-review-approved-claude-send-path-v1.md` | `402b2f7af1b2b28c9dac497ec2624e6078e361cebf55730b12f8ee8784c1e1ff` |
| 外部送信設計資料 | `docs/design/2026-08-07-external-egress-gate-proposal-v4.md` | `3a82b3973f8abc947782c4bbf8e2d54713043e8e8591a543089a5824c57bcacd` |
| 旧用途の停止Decision | `records/development/2026-08-08-egress-method-conclusion-decision-v1.md` | `d9228be3ec17db82fbed694e7a6bf05b8a5d6fae52ff2353aad39aeac27dc6fc` |

固定材料の選定漏れや矛盾を調べるため、repository内の追加探索を許す。追加材料はpath、SHA-256、必要だった
理由を結果へ記録し、Humanの未承認判断をauthorityとして扱わない。

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

## 4. 判定規則

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

## 5. 禁止事項

- `NG-SR-CB-001`：対象、production code、test、TODO、既存recordを変更しない。
- `NG-SR-CB-002`：Claude Code、外部API、browser、network、認証操作、外部送信を使わない。
- `NG-SR-CB-003`：実装、RED作成、所見修正、Human判断の代行を行わない。
- `NG-SR-CB-004`：秘密値を読まず、表示せず、保存しない。
- `NG-SR-CB-005`：主担当の期待や先行レビューの結論をoracleとして採用しない。

## 6. 出力形式

日本語のMarkdownで、次をこの順に返す。

1. `verdict`、レビュー担当model、対象commit、対象Digest。
2. 実行した機械確認と、単独commandごとの終了code・要約。
3. `SR-CB-001`〜`SR-CB-008`ごとの結果とEvidence。
4. blocking所見。各所見は固有ID、段階、4類型、事象、機械反証、影響、必要な最小措置を持つ。
5. non-blocking所見。各所見は確認段階と理由を持つ。
6. 先行F1〜F4の各状態を`closed | open | superseded`の一つで示す。
7. 追加探索した材料とSHA-256。無ければ`なし`。
8. 実装、file変更、Claude起動、外部送信を行っていないことの確認。
9. 次に必要なHuman判断を一つだけ示す。

所見が無い場合も各節を省略せず`なし`と記す。結果fileを作らず、応答だけを返す。
