# 利用者による契約010の製品受入判断（§2承認境界と残余riskの受容） v1

- 判断日：2026-08-17
- 判断者：利用者（Human）
- 記録者：Claude
- 判断の種別：Task Contractの製品受入（契約010 §9-11）。残余riskの最終受容を含む

## 1. 承認文言【記録】

> 上記の議論をメモに残す。その上で、契約010を製品として受け入れる。§2承認境界と残余riskを受容する。

（2026-08-17 chat。「上記の議論」は設計方針メモとして先行固定済み：
`records/development/2026-08-17-review-path-design-principles-memo-v1.md`、
SHA-256 `8e6a3668107b6bef114c2073c445092be1c54919decc65484e9a3def4b20648e`、commit `c5cda44`）

## 2. 判断対象の束縛

| 対象 | path | SHA-256 |
| --- | --- | --- |
| 契約010候補v2（受入対象） | `records/task-contract/2026-08-16-reviewer-launch-adapter-candidate-v2.md` | `7d159fdf093abad81481ae73eb3d95ad11efd04e2313d6df5a34c27fe583db0a` |
| 実E2E成功Evidence（第7試行） | `records/development/2026-08-17-reviewer-launch-e2e-attempt7-success-evidence-v1.md` | `eca7ae8f534a467e4e16bf094416bc742aeebd85231558c2fca98033e6b15711` |
| 完了レビュー判定record（verified・findings 0） | `records/session-handoffs/2026-08-16-reviewer-launch-adapter-implementation-completion-review-verdict-v1.md` | `68757e8b8583199dab95ffb6f5f9a43609f94fcb7acde04b53ec6bfff0233a3a` |
| 実装Evidence（§9-1〜7） | `records/development/2026-08-16-reviewer-launch-adapter-implementation-evidence-v1.md` | `9c7863e10f6fae2b654c85b17b0edb7493e47412f19218ae28ed5ee5d7ff58c5` |
| 設計方針メモ（受入議論の固定） | `records/development/2026-08-17-review-path-design-principles-memo-v1.md` | `8e6a3668107b6bef114c2073c445092be1c54919decc65484e9a3def4b20648e` |

## 3. 本判断が確定する事項

1. 契約`TC-RC3-PRODUCT-REVIEWER-LAUNCH-ADAPTER-010 / v2`を**製品として受け入れる**。受入条件
   §9-1〜10の充足はEvidence（§2の表）に固定済みであり、本判断により§9-11が成立、契約は完了する。
2. **§2承認境界の受容**：起動の起点は利用者のchatによるレビュー実施指示とし、起動ごとの追加承認
   手続きは設けない。
3. **§7.4残余risk 3点の受容**：(1) repository読取り＝Googleへの内容送出（緩和：起点は利用者指示・
   commit済み依頼record限定・読取りはagy機械層でrepository配下に限定〔実測〕・起動record台帳）、
   (2) agy仕様変更への追随risk（緩和：安全側停止・自動切替なし・raw完全保存・手動体制fallback）、
   (3) Tier 1でも残るmodel依存（緩和：機械反証・決定的検査の併用を義務づける既存protocolの不変適用）。
4. 機微情報の扱い：縦Bへ検査関門を追加しない（設計方針メモ§1の裁定どおり。境界は「repositoryへ
   置かない」既存運用に一本化し、作成時検査は縦Aの契約定義時の論点へ持ち越す）。
5. 独立確認の標準経路：本受入により、headless機械起動（`reviewcompass3-reviewer-launch`）が
   レビュー実行の正式経路となる。暫定手動体制（Gemini手動・Human中継）は廃止せずfallbackとして残る。

## 4. 持ち越し事項（本判断に含まれない）

- 後続縦切りの順序選択（claude-subagent第2 backend・縦A依頼組み立て器・縦C合議）。
- 複数Reviewer同報の実装（設計方針メモ§2・§3の原則に従う）。
- 外部API直接送信経路の後続（pendingのまま）。
- codex CLIの疎通回復時の第3 backend追加。

## 5. 未実施

- 後続契約の定義・実装、TODO更新（本record直後に共通手順で実施）。
