# RQ2実験計画の起草（データ取得順序4前段）事前走査 v1

- 記録日：2026-08-17
- 指示者：利用者（Human）。選択文言：「順序4の実験計画の起草に着手。範囲固定文書から進めて」
  （2026-08-17 chat）
- 記録者：Claude
- 種別：作業単位定義前の事前走査。**文書起草のみ**（コード変更なし——正式再利用検索は適用外。
  paired evaluation装置の実装は実験計画の承認後の別作業単位）
- 基準commit：`9c89b1a`（作業tree clean）

## 0. 一枚要約（人向け）

paired trial（RQ2）の技術前提（計測メタ・RQ1装置・reviewer接続）は順序1〜3で完了済み。
実験計画の起草に必要な実測を取った結果、**2つの制約**が判明した。
(1) **ケース素材の偏り**：既存の判定record 12件はverdictがほぼ合格系（findings計約35・blocking
1件のみ）で、**欠陥検出率（Finding recall）の測定には「見つけるべき欠陥があるケース」が不足**
する。対策候補＝実欠陥の再構成（例：契約014遡及実測1回目の`dequeue`見落とし——実開発で起きた
本物の欠陥）＋人工欠陥の注入（seeded defects——RC2で方法論調査済み・実欠陥から作る方針も同調査
に記録済み）。
(2) **費用規模**：1起動の実測＝input 57,567＋output 8,018＝**約6.6万トークン**（cr-014-001の
raw応答から機械抽出）。15ケース×4条件＝60起動なら約390万トークン、8ケース×2条件（B／C核心）
＝16起動なら約105万トークン。

## 1. 手順1：所在特定【実測】

| 材料 | 実態 |
| --- | --- |
| 判定record（ケース素材候補） | 12件。verdict＝verified系11・解析失敗1（手動fallback期の形式差とみられる）。findings計約35件・blocking 1件——合格系に偏る |
| 実欠陥の実例 | 契約014の遡及実測1回目不合格（`dequeue`のcontent欠落——正準列定義の実物不一致）が本日のEvidenceに固定済み。「実環境の実欠陥から作る」（RC2 seeded defects調査の妥当性対策）に合致する再構成候補 |
| 人工欠陥の方法論 | `docs/paper/survey`（RC2）＝Basili 1996系の設計（文書1本15〜29欠陥・欠陥分類・正解集合の改訂手順）を精読済み |
| 起動1回の費用 | 約6.6万トークン（実測）。時間・prompt bytesは順序1の計測メタで今後の起動から自動取得 |
| 4条件の実行手段 | B（Task Contract方式）＝bridge（順序3）。C（＋無関係資料）＝素材追加のみ。A（ベースライン固定prompt）・D（必要資料欠落）＝実験装置での条件組み立て（承認後の装置実装） |

## 2. 手順4：接続点【実測】

1. バッチ起動承認の形（順序3作業票で承認済み）：実験計画recordの事前承認をもってバッチ内起動を
   委任。**本作業（計画起草）はその承認対象の文書を作る**——起草と承認を分離する。
2. 実験recordの置き場：正式経路のまま`records/session-handoffs/`・slug `rq2-case-NNN-`系
   （順序3事前走査の推奨どおり）。
3. 正解Findingの固定は人手（利用者関与）が必要——計画に作業量を明示する。

## 3. digest表【実測】

```text
abcc1b57a2ba61a246a680539b8484ccd46152d65c204625fc1c89707f0b7be9  tools/evaluation/reviewer_bridge.py
30c22465607cb2e37be775d742028c22fcc6ee044c2f4000bbcc494ab018740a  tools/evaluation/rq1_contract_completeness.py
c666bdd7d0b5c44a8fbb876238a19c1d05ee245e693a2b104ceee514cdad55cb  docs/development/2026-08-17-evaluation-data-acquisition-plan-v1.md
d2668b6720b9578fd89382d943c1ec72225a6b781e20776455c8fd01f46f93d3  records/development/2026-08-17-evaluation-recoverability-map-v1.md
d49062602b7965eb64416d22b26bdcd81e0f685775a3c728a5aed52d81e44577  docs/design/2026-08-17-task-contract-architecture-import-v1.md
```

## 4. 作業票へ渡す論点【記録】

1. ケース供給の方針（実欠陥再構成＋seeded defectsの混合を推奨）とケース数（8〜12）。
2. 条件の規模（4条件フル vs B／C核心優先＋A／D縮小）。
3. 正解Finding固定の人手作業量と分担。
4. 費用・起動回数の上限。

## 5. 未実施

- 作業票v1の承認、実験計画recordの起草、（承認後の）装置実装・実起動バッチ。
