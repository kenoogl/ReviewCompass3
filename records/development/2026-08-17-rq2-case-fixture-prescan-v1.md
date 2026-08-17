# RQ2ケース材料fixture＋正解表起草（後続作業単位1）事前走査 v1

- 記録日：2026-08-17
- 指示者：利用者（Human）。選択文言：「RQ2実験計画v1を承認する。後続(1)材料fixture＋正解表起草
  から進めて」（2026-08-17 chat。承認＝最大35起動・約230万トークンのバッチ委任を含む）
- 記録者：Claude
- 種別：作業単位定義前の事前走査。**材料file（データ）とrecordの新設のみ**——製品コードの変更が
  ないため正式再利用検索は適用外（RQ2実験計画の事前走査v1と同じ扱い）
- 上位：`records/development/2026-08-17-rq2-paired-trial-plan-v1.md`（承認済み）§1・§4・§7-(1)
- 基準commit：`b5c83af`（作業tree clean）

## 0. 一枚要約（人向け）

材料の流用元はすべて実在を確認した（§3のdigest表）。一方で、**起動経路の実測から実験計画の
測定定義と材料配置に2つの是正点**が判明した。

1. **`prompt_bytes`は材料量を測れない**（計画§2「核心の観測」の測定定義の空振り）。起動promptは
   固定形式で、材料本文も依頼本文も含まない（§1-1）。無関係資料の影響を測る量は
   **reviewerの実入力トークン**（raw応答から機械抽出可）である。
2. **reviewerはrepository配下の任意fileを読める**（§1-2）。正解表を作業treeへ置いたまま実起動
   すると、正解が読まれて実験が汚染されうる。**本作業では実起動しない**ため現時点の汚染はない。

いずれも本作業（材料作成・正解表起草）の成果物には影響しないが、**後続(2)装置実装・(3)実起動の
前に利用者の裁定が要る**。§5に論点として出す。

## 1. 手順1・4：所在特定と接続点【実測】

### 1-1. 起動promptの構造（`tools/reviewer_launch/core.py` `build_prompt` 244〜290行）

生成されるpromptは固定形式で、可変部は次の4つだけである。

| 可変部 | 内容 |
| --- | --- |
| `repository_root` | 作業領域の絶対path |
| `request_relative_path` / 絶対path | 依頼recordのpath |
| `expected_sha256` | 依頼recordの期待digest |
| `read_tool_name` | 読取り道具名（既定`view_file`） |

docstringの明記：「自由文・依頼内容の複製を含めない」。したがって
**`launch.json`の`prompt_bytes`は材料の量・数と無関係**（pathの文字数でのみ変わる）。

**帰結**：計画§2「核心の観測」の「依頼recordの材料選択・prompt bytesが不変」のうち、
prompt bytes部分は条件B／Cの区別が原理的につかない。材料選択（context manifestの
`material_bundle`）の不変性は測れる。無関係資料の実効影響は**reviewerのinput tokens**で測る
（順序1の復元可能性表で「raw応答から機械復元可」と確定済み。cr-014-001実測＝input 57,567）。

### 1-2. reviewerの読取り範囲（同prompt本文）

promptは「対象repository配下の絶対pathだけを渡し、対象repositoryの外へは一切アクセスしない」と
指示する。すなわち**repository内は読取り自由**であり、依頼recordに列挙されない材料も物理的には
読める。この性質は条件C（無関係資料の追加）の設計前提でもあり、同時に正解表の配置riskでもある。

### 1-3. 材料の受け渡し経路

依頼record（`records/session-handoffs/`）→ reviewerが絶対pathで開く → 依頼record §1の材料表の
pathを辿って各材料を開く。**材料fileはrepository内の実fileである必要がある**（本作業で
`tools/evaluation/fixtures/rq2/`へcommitする理由）。

## 2. 手順2：流用元の構造【実測】

RQ1装置（`tools/evaluation/rq1_contract_completeness.py`）のfixtureは**Python関数で生成する
一時project**であり、file実体を持たない（`_project`が`tmp_path`配下へ書き出す形）。RQ2の材料は
reviewerが実pathで読む必要があるため**この形は流用できない**。RQ2は静的なfile群として置く
（`tools/evaluation/fixtures/rq2/case-NNN/`。計画§1の指定どおり）。

## 3. 手順3：複製元のdigest表【実測】

```text
4dd6796d179f76fa58930108146ab1a9a007838577365d8a1a118e455c34a3b1  records/task-contract/2026-08-17-session-log-prefix-interpretation-candidate-v2.md
5a7c174df53590e7c97f23506b48151331fefa8e18b8c38a4584fecbaa53251c  records/task-contract/2026-08-17-session-log-prefix-interpretation-candidate-v3.md
566c7b88fbd6a9bf6dac5ad93c28b876689977ab0f6393e314ad020632e55a9a  records/development/2026-08-17-session-log-prefix-interpretation-implementation-evidence-v1.md
53cfdcd39904d4ceb43e4d8e8e991c8a4201430d2ea47fb2af8d6fc0ecf03055  records/development/2026-08-17-session-log-prefix-interpretation-prescan-v1.md
759154984591f0479c505e4a2d01d6a86e2d9fd3a2c584b1187eb22f067e3a35  records/development/2026-08-17-session-log-prefix-interpretation-product-acceptance-decision-v1.md
9c1808fdbb8c730d4d3f843a76dfce8f202260e2870e385f37eae557f48b834d  docs/development/prompts/session-log-record-run.md
cce799197ae88c48f3591a0dfafd00f9924c9076772633f90b58d7717e039873  docs/development/2026-08-17-rq1-apparatus-work-ticket-v1.md
c3ac8e5a09fba51cb230dc7246181661929d05753b2aeca1f96fe26490d3ddec  docs/development/2026-08-17-reviewer-bridge-work-ticket-v1.md
3db49c0b74a581507d4076d06c7b1730308434b65893871695583de6bd40c2c7  docs/development/2026-08-17-launch-metrics-recoverability-work-ticket-v1.md
```

契約014以前の手順書（C03の旧仕様の出所）＝commit `0d3c992`の
`docs/development/prompts/session-log-record-run.md`（当時のfile digest
`e1a25223df1b3bc58749940150b6c4a79cda20e83b04cc20f20700d723b57893`）。

## 4. 材料設計の是正1点【実測に基づく設計判断】

計画§1のC02は「実fileと1文字違うdigestを混入」だが、**LLMはSHA-256を計算できない**ため、
file実体との照合による検出は原理的に不可能である。本日の実欠陥（d5→d6の手転記ミス）の
**検出可能な本質は「機械出力と転記表の食い違い」**であり、これは読解で検出できる。よって
C02の材料は、同一file内に(a)`shasum`の機械出力ブロックと(b)転記した表を併置し、表側を1文字
変える形で構成する。実欠陥の再構成という位置づけは保たれる（本記述は正解表へも明記する）。

## 5. 作業票へ渡す論点【記録】

1. **測定定義の是正**（推奨：計画の測定欄を`prompt_bytes`→`material_bundle`件数の不変性＋
   reviewer input tokensへ差し替え）。装置実装（後続2）の前に確定が要る。
2. **正解表の配置**（推奨：pre-registration形——正解本体はrepo外私有領域へ置き、repoには
   ケース一覧と正解表fileのSHA-256だけを封じたrecordを置く。実験後に本体をcommitしてdigest
   照合する）。汚染riskの遮断と事後変更の否定を同時に満たす。実起動（後続3）の前に確定が要る。
3. 材料の冒頭表示は**全10ケースで完全に同一の文言**とし、欠陥の有無・正解表の所在を一切示唆
   しない（合格系が識別可能になると実験が壊れるため）。

## 6. 未実施

- 作業票v1の固定、材料fixtureの作成、正解表の起草、正解表の**利用者確定**（計画§4-2）。
- 装置実装・実起動・RQ2集計（後続2〜4）。
