# RQ2 paired trial 事前登録（正解表の封緘と独立プールの固定） v1

- 記録日：2026-08-17
- 記録者：Claude
- 根拠：利用者裁定「正解表v1を確定。論点2も事前登録形で確定。」（2026-08-17 chat）。
  形式は`records/development/2026-08-17-rq2-case-answer-key-v2.md` §6の論点2の推奨どおり
- 目的：**実起動の前に正解を封じ**、実験後に事後変更が無かったことをdigestで証明できるようにする。
  あわせて条件Cで混ぜる独立プールを固定する（裁定record §2）
- 状態：**実起動前**。本recordのcommitをもって実起動を開始できる

## 1. なぜ封じるのか【実測に基づく】

レビュアーの読取り許可は**本repositoryのフォルダに束縛**されており（事前走査
`records/development/2026-08-17-rq2-apparatus-prescan-v1.md` §0-2）、実験専用の別作業treeを
作る案は起動前に停止する。実験は本repositoryで走らざるを得ず、レビュアーはrepository内の
任意のfileを読める。正解表を作業treeに置いたままでは正解が読まれうる。

そこで**正解表の本体を作業treeから外し**、repositoryにはSHA-256だけを残す。

## 2. 封じた正解表

| 項目 | 値 |
| --- | --- |
| 正本 | 正解表v2（確定版） |
| 退避先 | `/Users/keno/.reviewcompass3-private/rq2-answer-key/2026-08-17-rq2-case-answer-key-v2.md`（repo外私有領域） |
| SHA-256 | `0d290876110440df6ac5f14bd2efcc3d3d8f244b66f5d19354c4e7bb98f8cb64` |
| 参考：v1（path改訂前） | `790f80c9c185805107bc56edc3adc38c64248559094310225fc41a8796095f6a` |

実験後、本体をrepositoryへ戻してcommitし、**上記SHA-256と一致すること**を機械照合する。
一致しなければ正解が事後変更されたことになり、実験結果は無効として扱う。

なお両版はgit履歴には残っている（`8161611`以降）。**汚染の遮断は作業treeから外すことで
成立する**（レビュアーは作業treeのfileを読むのであって履歴を読まない）。

## 3. 残留するrisk と その扱い【正直な記載】

repository内の設計・裁定recordには、答の一部が平文で残っている。例：

- `records/development/2026-08-17-rq2-measurement-and-pool-decision-v1.md` §2は、case-001の答
  （`dequeue`に`content`が無いこと）を交絡の実例として述べている。
- `records/development/2026-08-17-rq2-case-fixture-prescan-v1.md` §4は、case-002の設計意図を
  述べている。

これらを事前に消し切る方針は採らない（裁定・来歴のrecordを実験のために削るのは本末転倒である）。
かわりに**読まれたことを事後に機械検出**する。未加工応答の`step_update`に読取りfileの絶対path
が残るため（実測）、装置は各実行について次を記録する。

- reviewerが実際に開いたfileの一覧（`extract_read_paths`）
- 依頼recordと指定材料の外を読んだかどうか（`check_read_scope`）

**範囲外を読んだ実行は汚染として集計から外す**。この判定は機械であり、事後の言い訳が効かない。

## 4. 独立プール（条件Cで混ぜる無関係資料）

`docs/evaluation/rq2-pool/`。10 file・**113,976 byte**（計画v1の「10 file・計100KB超」を満たす）。
各fileの冒頭はケース材料と**byte一致の共通表示**である（機械確認済み）。

```text
7fcc05822017ca0b79c59732b382dcb8d07c1d1cc31f3dffc4fd14d57701df6c  docs/evaluation/rq2-pool/pool-01.md
1f490bec67ea7d4f1c654c9c975048268b75ade2a57b475de540e122c1ae22a4  docs/evaluation/rq2-pool/pool-02.md
c0a336182dfd91288a70ec7d4783da9ec17677c6051d7941cdf49064f424df27  docs/evaluation/rq2-pool/pool-03.md
bb9ff7af54c4bc50e59e7a83a263cf83658cb23cf63226af326e6a55a252c464  docs/evaluation/rq2-pool/pool-04.md
70d62f5d1565f1ace241a058e7e817ffaf6e2a5d90b5750b85c08200a15f3214  docs/evaluation/rq2-pool/pool-05.md
f4cfe9af7925cee8fd3ec2cf023777a08f669d2e79f95cf42561caca77f5c479  docs/evaluation/rq2-pool/pool-06.md
c3e758b85e4300877ee8d5efae0a6dc1bd9202dfb2bedb9fd56398c1b7074a40  docs/evaluation/rq2-pool/pool-07.md
eca6751986d6a6327b972a8802cdcaaaa0c3aa08b4e1c8939f44022a77c885eb  docs/evaluation/rq2-pool/pool-08.md
9eb89e279288f570dd6f73cf149f1c1fb9dd9ee217b3e0508796ee4aeaa80949  docs/evaluation/rq2-pool/pool-09.md
ecb596d986e40ca40c8dc7ec22adc573f79d3c71b9247e747cb2aa0b935e6d0e  docs/evaluation/rq2-pool/pool-10.md
```

### 4.1 選定の手続きと結果【実測】

裁定record §2の手順を実行した。

1. 候補＝`docs/concepts`・`docs/intent`・`docs/plan`・`docs/requirements`・`docs/design`配下の
   8KB〜30KBのMarkdown。
2. **一次足切り**：各ケースの期待Findingに固有の語で全文検索し、**該当0件**のものだけを残した。
   検索語：`dequeue`・`queue-operation`・`正準列`・`前置record`・`解釈非対応`・`補助分類`・
   `初回計測`・`rq1-apparatus`・`RQ1装置`・`e2e-010-007`・`e87d9f60`・`finding_set`・
   `reviewer_bridge`・`reviewer接続`・`Human承認境界`・`cdad55c`・`rq2`。
3. **二次足切り**：欠陥類型に触れうる語でも検索し、**該当0件**を確認した。検索語：
   `転記ミス`・`手転記`・`受入条件.*欠落`・`範囲内.*範囲外.*同一`・`session-log`・`record-run`・
   `前置`・`契約014`・`契約010`。
4. **意味の確認**：残った候補のうち、主題がケースから最も離れた10件を選んだ（並行作業の導入時期・
   TODO再仕分けの経路・デプロイ成果物の境界・source変更検証の同一性と時期・現在位置のprojection・
   issue取り込みv4・非機能要件の検証プロファイル・大規模設計の評価・外部送信ゲート・過剰設計の境界）。
5. 複製元は`docs/design`・`docs/concepts`等の実在文書であり、複製に共通表示を付けたうえで
   `docs/evaluation/rq2-pool/`へ固定した。

## 5. ケース一覧（答を含まない）

| ケース | 群 | 材料数 | 実行する条件 |
| --- | --- | --- | --- |
| case-001 | 実欠陥 | 2 | A・B・C・D |
| case-002 | 実欠陥 | 1 | B・C |
| case-003 | 実欠陥 | 2 | B・C |
| case-004 | 人工 | 1 | A・B・C |
| case-005 | 人工 | 1 | B・C・D |
| case-006 | 人工 | 1 | B・C |
| case-007 | 人工 | 1 | B・C |
| case-008 | 合格系 | 1 | A・B・C・D |
| case-009 | 合格系 | 1 | B・C |
| case-010 | 合格系 | 1 | B・C |

材料のdigestは正解表§1（封緘済み）にあり、実fileは`docs/evaluation/rq2-cases/`にある。

### 5.1 条件Dの縮退（実測に基づく設計上の断り）

条件Dは「必須材料を1件除く」である。**材料が1件しかないケース（case-005・case-008）では
除くと材料が0件になり、契約chainが`context_incomplete`で実行前に停止する**。これは起動を
消費しない正当なfail-closedであり、negative caseの結果として記録する（escalationの測定には
ならない）。materialが2件あるcase-001だけが、材料を減らした状態で実際に起動する。

## 6. 起動数の見込み

| 条件 | 起動数 |
| --- | --- |
| B | 10 |
| C | 10 |
| A（資料少・多） | 3ケース×2＝6 |
| D | 1（case-001のみ。case-005・case-008は起動前停止） |
| **合計** | **27**（計画の29以内。絶対上限35は不変） |

## 7. 実験後にやること

1. 正解表本体をrepositoryへ戻してcommitし、§2のSHA-256と機械照合する。
2. 汚染判定（§3）で範囲外読取りのあった実行を集計から外す。
3. RQ2集計とEvidence固定。
