# 原因分析：範囲固定の漏れが収束しない理由（Pilot自己申告）

- 作成日：2026-08-10
- 作成者：Claude（Pilot）
- 契機：Humanの問い「中々収束しない。漏れが多くないか？　原因は何？」
- 位置づけ：**Pilot自身の作業品質に関する自己申告**であり、Codexの独立レビュー対象。
  裁定record `records/development/2026-08-10-scope-prescan-rule-decision-v1.md`
  （Human裁定「恒久的な規約にする。あとでリマインドするように。」）の根拠でもある。

## 1. 事象（2026-08-10の守り役後追い修正4単位）

| 単位 | 範囲レビューでの要修正 | 実装中の停止 |
| --- | ---: | ---: |
| group E（外部送信・機微） | 4件（SR-EG-SCOPE-001〜004）＋RED定義改定1回 | 0 |
| group A（共通正本） | 1件（SR-CG-SCOPE-001＝指紋pin fileの欠落） | 0（完了レビューで反証testの偽陰性1件） |
| group B（公式検証oracle） | 0（v1で`verified`） | 2件（`conftest.py`の結線、Work 5B契約recordのpin）＋完了レビュー blocking 2件 |
| group C（現在地正本） | 3件（SR-C-SCOPE-001〜003） | 1件（CRLF破壊の実体が範囲外file） |

合計：範囲の作り直し**8回**、実装中の停止**4回**。

## 2. 実測（Reviewerが再実行できる形）

### 2.1 Digest固定の密度

```text
python3 - <<'PY'
import hashlib, pathlib, subprocess
mods = subprocess.run(["find","tools","-name","*.py","-not","-name","__init__.py"],
                      capture_output=True, text=True).stdout.split()
pinned = 0
for m in mods[:40]:
    d = hashlib.sha256(pathlib.Path(m).read_bytes()).hexdigest()
    if subprocess.run(["grep","-rl",d,"records","tests","config"],
                      capture_output=True, text=True).stdout.strip():
        pinned += 1
print(pinned)
PY
```

- 実測：先頭40 moduleのうち**32件**の現在Digestがrepository内の別fileに書かれていた
  （2026-08-10、commit `5a67f5a`時点）。
- 実行時にDigestを再計算して照合するtestは**16 file**
  （`grep -rln "sha256(.*read_bytes\|_sha256(" tests`のうちassertとpin表を持つもの）。

### 2.2 group Cで停止した具体例

- 上流Finding（group C判定 F-C5）は対象を`tools/development/todo_update_path.py`と
  記していたが、CRLF→LF変換の実処理は
  `tools/development/todo_record_generation.py`の`build_todo_candidate`内
  （`path.read_text(encoding="utf-8")`）にある。

## 3. 原因（寄与の大きい順・Pilotの判断）

1. **欠陥の所在を上流Finding記載のmodule名で信じた**。codeを読んで確かめる手順が
   無かった（group C）。
2. **Digest固定の網を事前に調べていなかった**。§2.1の全文検索は実装前に可能で
   あったのに、手順に入れていなかった（group A・group B）。
3. **実運用への接続点を範囲へ入れていなかった**。「機能を作る」と「実際に効かせる」が
   別fileに分かれる場合を落とした（group Bの`conftest.py`）。
4. **同じ集合を2か所へ別々に書いた**。受入条件と変更可能pathを個別に直し、
   自ら不整合を作った（group C v2）。
5. **反証testの失敗理由を機械確認していなかった**。「失敗する」と「狙った欠陥で
   失敗する」を区別していなかった（group Aで指摘、group Cで自己検出2件）。

## 4. 構造要因との切り分け（Pilotの判断）

対象は守り役どうしが相互に監視する設計（testの指紋を契約recordが固定し、その契約を
testが検査する）であり、1 fileの変更が連鎖しやすい。これは意図された設計である。
したがって**設計の欠陥ではなく、網の形を事前に把握しないまま範囲を切ったPilotの
手順不足**が主因である、というのが本分析の主張である。

## 5. 対策（Human裁定により恒久規約化）

範囲固定を書く前に次を機械実行し、結果を範囲固定の一節として記録する。

1. 欠陥の所在をcodeで特定する（Finding記載のmodule名を信じない）
2. 対象fileをimportするtestを列挙する
3. 対象fileの現在のSHA-256で全文検索し、Digestを固定しているrecord・testを列挙する
4. 実運用への接続点を列挙する（hook登録・入口module・CLI・conftest）
5. 受入条件と変更可能pathを同じ一覧から書く

適用：group Cの範囲固定v4から即時適用。文書への必須節としての反映は別単位（未了）。

## 6. Reviewerへの確認観点

- §1の件数が実commit列と一致するか（`git log`とrecordの照合）。
- §2.1の実測がReviewerの独立再実行で再現するか（数値のずれは記録の誤りとして指摘可）。
- §2.2の所在特定が正しいか（実際に`todo_record_generation.py`が原因か）。
- §3の原因列挙に**欠落または誤帰属**が無いか。特に、Pilotが自分の手順不足へ
  帰しているが、**上流Findingの書き方（module名の粒度）にも原因があるのではないか**を
  独立に判断すること。
- §4の切り分け（設計要因ではなくPilot要因）が妥当か。
- §5の5手順で、§1の12件の事象が**実際に事前検出できたか**を、少なくとも
  group A（pin file）とgroup B（conftest・契約record）について機械的に検証すること。
  検出できない事象があれば、対策の不足として指摘すること。

## 7. 訂正（Codexレビュー反映）

Codexの完了レビュー（`records/session-handoffs/2026-08-10-codex-review-result-scope-omission-cause-analysis-v1.md`、
commit `ca747c1`、判定`report_execution_mismatch`）を受け、Human承認
（2026-08-10「分析と規約を指摘どおり修正せよ。5手順は『巻き添え防止』に限定し、
検査の正しさは別項目として立てよ」）に基づき本節で訂正する。**本節が§1・§2.1・§3・§5を
再置換する。**

### 7.1 §1の件数（CA-REVIEW-002）を単位ごとに分離

旧「範囲の作り直し8回・実装中の停止4回」は3種の数え方を混ぜていた。次の**4つの
別々の指標**へ分離する（いずれも守り役後追い修正4単位＝E/A/B/Cが対象）。

| 指標 | 定義 | 値 | 機械抽出 |
| --- | --- | ---: | --- |
| a. scope改訂commit数 | 各単位のscope v2以降の`Fix scope`commit | **7** | `git log --oneline`で E:2・A:1・B:2・C:2 |
| b. 範囲レビュー要修正回数 | scope reviewの判定が`要修正`だった回数 | **4** | egress v1・common v1・position v1・position v2 |
| c. 完了レビューblocking件数 | 完了レビューで出たblocking finding | **3** | group A完了v1:1（F-CG-COMP-001）、group B完了v1:2（F-C1・F-C2） |
| d. 実装中のHuman停止回数 | GREEN着手後にscope外事由で停止した回数 | **3** | group B `conftest`結線・group B契約pin・group C CRLF |

以後、この4指標を混ぜて総数で語らない。

### 7.2 §2.1のDigest照合test数（CA-REVIEW-003）を訂正

旧「16 file」は絞り込み条件を書いていなかった。実測を次へ訂正する。

- `grep -rln "read_bytes()).hexdigest()\|_sha256(" tests` → **35 file**（終了コード0）。
  これは**fixture用のDigest計算を含む**ため、pin照合testの数ではない。
- そのうち`assert`でpin期待値と比較する行を持つもの
  （`grep -q "assert.*==.*expected\|_PINS\|immutable_record\|fixed_sources"`）→ **23 file**。
- 「16」は独立再現できないため撤回する。**Digest照合を含むtestは広めに見て35、
  pin期待値との比較を持つものは23**とする。Digest密度32/40の主張は§2.1のscriptで
  再現し、維持する。

### 7.3 §3・§4の原因帰属（CA-REVIEW-004）を共同寄与へ改める

旧§3・§4は主因をPilotの手順不足に一元化していた。Codexは自らの記録も寄与したと
認めた。次へ改める。

- **Pilot側の寄与**（旧§3の1〜5）は維持する。
- **上流Finding側の寄与**を追加する：group C判定 F-C5は対象欄を
  `todo_update_path.py`と記したが、実処理は`todo_record_generation.py`にある
  （対象欄の誤帰属）。group B範囲レビューv1は`conftest.py`を発見しつつ
  「変更必須の固定値は無い」と判断し、結線を範囲へ入れなかった。
- ただしFinding recordは実装scopeを網羅すると宣言した文書ではない。
  したがって**Pilot要因・上流記録要因のいずれか一方を主因とは判定しない**（共同寄与）。
- §4の「設計要因ではない」は維持する（相互監視設計は意図されたもの）。

### 7.4 §5の対策（CA-REVIEW-001）を2本立てへ分離

5手順は**巻き添え防止**の手順であり、**検査の正しさ**（誤った合格の残存）は防げない。
これを混同して「全事象を事前検出できる対策」と扱わない。対策の確定形は
裁定record `records/development/2026-08-10-scope-prescan-rule-decision-v1.md`の
改訂版（同日）に置く。本分析は、5手順が**bのうち巻き添え型**（group Aのpin・
group Bのconftestと契約pin・group CのCRLF所在）を事前検出できることだけを主張し、
c（完了レビューblocking＝検査の正しさ）とREDの失敗理由は**対象外**と明記する。
