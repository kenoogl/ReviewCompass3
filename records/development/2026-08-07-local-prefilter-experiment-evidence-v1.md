# ローカル事前分類 実験Evidence v1

- record ID：`EXP-LOCAL-PREFILTER-001`
- 実施：2026-08-07
- 指示：Human発案（2026-08-07「特徴を並べたベクトルを作り近傍探索に入れる案」）と
  Human承認「テスト評価してみよう」「アルゴリズムとテスト結果を証跡として残し進める」
- 目的：外部LLMへの責務判定の送信前に、ローカル計算（外部送信ゼロ）の類似度分類で
  組をどれだけ枝刈りできるかの実現可能性を測る
- 性質：**実現可能性の実測であり、意味の結論ではない**。閾値・重みは本実験で仮置きした
  初期値であり、採否と値の確定はHuman判断事項

## 1. 入力（固定）

| 入力 | 所在 | SHA-256 |
| --- | --- | --- |
| Comparison Discovery（816 group） | runtime領域 `work4a/comparison-discoveries/80668a….json` | `b7758366bffc0b16a46008cdfaadbe8625ae331bfb441647c8fbe37aad5f5855` |
| Routine Profile（1,252関数） | runtime領域 `work4a/profiles/75b9bd3f….json` | `0354635de80b45906c638bde2b79ded1c42768688090ec06f6aac8907cb6eaa5` |
| 実順位表v2（748 group） | `records/development/2026-08-07-candidate-ranking-v2.json` | `ae1c4746ddfc13e6674d75a41c076eb97da289c192cf059c29723d93ee10ef56` |
| 対象範囲 | 順位表v2の上位20 group（member延べ186、一意186関数、2つ組1,415） | — |

runtime領域＝`/Users/keno/.reviewcompass3/projects/reviewcompass3/development/data/`（Layout v3）。

## 2. アルゴリズム

関数の組ごとに3つの類似度を計算し、合成して3帯に分類する。

1. **本文の字句類似度**（重み0.6）：`code_reference`の行範囲から本文を切り出し、
   識別子をsnake_case・CamelCaseで分解して小文字化したtoken集合を作り（言語の予約語と
   汎用語は除外）、Jaccard係数（2集合の共通部分÷和集合）で比較する
2. **関数名の字句類似度**（重み0.2）：symbol名のtoken集合のJaccard係数
3. **機械特徴の一致度**（重み0.2）：引数の個数・return数・raise数・投げる例外名の集合・
   分岐数の一致、行数の近さ（差が2行以内または20%以内）の6項目の一致率

分類の帯：合成類似度 ≥ 0.85 →「明らかに同じ」、≤ 0.45 →「明らかに別」、中間 →「曖昧」。
**外部LLMへ送るのは「曖昧」の組だけ**、という運用仮説を測る。

実行スクリプト全文（SHA-256 `6800a14d6ae6fdd20329f9242348c58a7114e344e06c1d29e79ff565c380983b`）：

```python
"""ローカル事前分類の実測実験（送信ゼロ）。

上位20 groupの全2つ組について、
- code本文の字句（識別子token）のJaccard類似度
- 機械特徴（引数数・行数・分岐・例外など）の一致度
- 関数名tokenの類似度
を計算し、閾値で「明らかに同じ／明らかに別／曖昧」に分けたときの
組数の分布を出す。外部送信が必要になるのは「曖昧」の組だけ、という
仮説の実現可能性を測る。
"""
import itertools
import json
import re
from pathlib import Path

REPO = Path("/Users/Daily/Development/ReviewCompass3")
DATA = Path(
  "/Users/keno/.reviewcompass3/projects/reviewcompass3/development/data/work4a"
)
DISCOVERY = DATA / "comparison-discoveries" / (
  "80668a77b51efd0eb0ed61e5f52283631f13c82091fe77860a0dc98e3b56a282.json"
)
PROFILE = DATA / "profiles" / (
  "75b9bd3f21a73732a3bf63f6927c3bf475b3012d824e615adf4a12ba18e4d71e.json"
)
RANKING = REPO / "records/development/2026-08-07-candidate-ranking-v2.json"

_CAMEL = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")
_IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_STOP = {
  "self", "the", "a", "an", "of", "and", "or", "in", "to", "is", "def",
  "return", "if", "else", "elif", "for", "while", "raise", "try",
  "except", "with", "as", "not", "none", "true", "false", "import",
  "from", "pass", "class", "dataclass", "dataclasses", "frozen", "str",
  "int", "bool", "float", "tuple", "list", "dict", "object", "optional",
}


def tokens(text):
  out = set()
  for ident in _IDENT.findall(text):
    for part in ident.split("_"):
      for word in _CAMEL.split(part):
        w = word.lower()
        if len(w) >= 2 and w not in _STOP:
          out.add(w)
  return out


def jaccard(a, b):
  if not a and not b:
    return 1.0
  if not a or not b:
    return 0.0
  return len(a & b) / len(a | b)


def code_text(routine):
  ref = routine["code_reference"]
  lines = (REPO / ref["relative_path"]).read_text(encoding="utf-8").splitlines()
  return "\n".join(lines[ref["start_line"] - 1 : ref["end_line"]])


def feature_match(ra, rb):
  """機械特徴の一致度（0..1）。"""
  score = 0
  total = 6
  if len(ra["signature"]["parameters"]) == len(rb["signature"]["parameters"]):
    score += 1
  if ra["return_count"] == rb["return_count"]:
    score += 1
  if ra["raise_count"] == rb["raise_count"]:
    score += 1
  if set(ra["raised_exception_names"]) == set(rb["raised_exception_names"]):
    score += 1
  if ra["branch_count"] == rb["branch_count"]:
    score += 1
  if abs(ra["line_count"] - rb["line_count"]) <= max(
    2, 0.2 * max(ra["line_count"], rb["line_count"])
  ):
    score += 1
  return score / total


def main():
  disc = json.loads(DISCOVERY.read_text())
  prof = json.loads(PROFILE.read_text())
  rank = json.loads(RANKING.read_text())
  byid = {r["symbol_id"]: r for r in prof["routines"]}
  groups = {g["group_id"]: g["member_symbol_ids"] for g in disc["groups"]}
  top = [e for e in rank["ranking"] if e["rank"] <= 20]

  bands = {"clearly_same": 0, "clearly_diff": 0, "ambiguous": 0}
  examples = {"clearly_same": [], "clearly_diff": [], "ambiguous": []}
  per_group = []
  cache = {}

  for entry in top:
    gid = entry["group_id"]
    members = [m for m in groups.get(gid, []) if m in byid]
    gb = {"clearly_same": 0, "clearly_diff": 0, "ambiguous": 0}
    for sa, sb in itertools.combinations(members, 2):
      ra, rb = byid[sa], byid[sb]
      for sid, r in ((sa, ra), (sb, rb)):
        if sid not in cache:
          body = code_text(r)
          cache[sid] = {
            "body": tokens(body),
            "name": tokens(sid.rsplit(":", 1)[-1]),
          }
      body_sim = jaccard(cache[sa]["body"], cache[sb]["body"])
      name_sim = jaccard(cache[sa]["name"], cache[sb]["name"])
      feat = feature_match(ra, rb)
      # 合成類似度：本文を主、名前と特徴を従に置く
      sim = 0.6 * body_sim + 0.2 * name_sim + 0.2 * feat
      if sim >= 0.85:
        band = "clearly_same"
      elif sim <= 0.45:
        band = "clearly_diff"
      else:
        band = "ambiguous"
      bands[band] += 1
      gb[band] += 1
      if len(examples[band]) < 4:
        examples[band].append(
          (round(sim, 2), round(body_sim, 2), sa, sb)
        )
    per_group.append(
      (entry["rank"], gid, entry["basis_kind"], len(members), gb)
    )

  total = sum(bands.values())
  print("=== 上位20 group・全2つ組の分類（合成類似度） ===")
  print(f"総組数: {total}")
  for k, v in bands.items():
    print(f"  {k}: {v} ({100 * v / total:.0f}%)")
  print()
  print("=== group別 (rank, group, 根拠, member数, 内訳) ===")
  for row in per_group:
    print(" ", row)
  print()
  print("=== 帯ごとの実例（合成類似度, 本文類似度, 組） ===")
  for band, rows in examples.items():
    print(f"[{band}]")
    for sim, bsim, sa, sb in rows:
      print(f"  {sim} (本文{bsim})")
      print(f"    {sa}")
      print(f"    {sb}")


if __name__ == "__main__":
  main()
```

## 3. 結果

### 3.1 全体（上位20 group、1,415組）

| 帯 | 組数 | 割合 |
| --- | --- | --- |
| 明らかに別（≤0.45） | 1,169 | 83% |
| 明らかに同じ（≥0.85） | 187 | 13% |
| **曖昧（外部判定が要る組）** | **59** | **4%** |

外部送信の見込み：1,415回 → 59回（96%削減）。3役の独立判定でも177回。

### 3.2 group別内訳（rank, group, member数 → 別/同/曖昧）

1: CG-STRUCT-0022, 28 → 375/0/3 ・ 2: CG-STRUCT-0030, 28 → 376/0/2 ・
3: CG-STRUCT-0019, 23 → 248/0/5 ・ 4: CG-STRUCT-0005, 17 → 0/136/0 ・
5: CG-STRUCT-0039, 13 → 77/0/1 ・ 6: CG-STRUCT-0058, 11 → 54/0/1 ・
7: CG-STRUCT-0033, 7 → 0/7/14 ・ 8: CG-STRUCT-0036, 7 → 0/0/21 ・
9: CG-STRUCT-0053, 7 → 0/21/0 ・ 10: CG-STRUCT-0064, 6 → 15/0/0 ・
11: CG-STRUCT-0003, 5 → 0/10/0 ・ 12: CG-STRUCT-0007, 5 → 10/0/0 ・
13: CG-STRUCT-0008, 4 → 0/3/3 ・ 14: CG-STRUCT-0024, 4 → 0/6/0 ・
15: CG-STRUCT-0025, 4 → 6/0/0 ・ 16: CG-STRUCT-0017, 4 → 0/3/3 ・
17: CG-STRUCT-0061, 4 → 3/0/3 ・ 18: CG-STRUCT-0015, 3 → 2/1/0 ・
19: CG-STRUCT-0018, 3 → 0/0/3 ・ 20: CG-STRUCT-0050, 3 → 3/0/0

上位20はすべて根拠`structural_exact_match`（構造完全一致）のgroupであった。

### 3.3 目視確認（妥当性の実例）

- **「別」が正しい例**：1位group（5行のデータ入れ物28個）は375組が「別」。
  `ReviewAssuranceReport`対`ReviewAssignment`は本文類似度0.08。構造完全一致でも
  責務が別のものを正しく落とした
- **「同じ」の中身**：4位groupの17個の`main`関数は本文類似度1.0の**逐語重複**。
  LLM判定不要でそのまま統合候補になる
- **「曖昧」の質**：残った59組は `BatchReassessmentResult`対`ReassessmentResult`、
  `ObligationSourceTrace`対`RequirementSourceTrace` など、判定の価値がある組だった

## 4. 限界（本実験が確定しないこと）

1. 閾値0.85／0.45と重み0.6/0.2/0.2は本実験で仮置きした初期値。境界付近の誤分類はあり得る
2. 「明らかに別」の中に**語彙だけ違って責務は同じ**組が紛れる見落としの可能性が残る。
   目的が価値ある統合の発見であれば完全網羅は不要という割り切りになるが、
   その割り切り自体はHuman承認事項
3. 正解データが無いため、評価は実例の目視確認による。定量的な精度は未測定
4. 対象は上位20 group（すべて構造完全一致）のみ。他の根拠種のgroupでの挙動は未測定

## 5. 境界

- 本recordは実測の固定であり、事前分類の採用・閾値・比べ方の規則を決めない（Human判断）
- 計算はすべてローカルで完結し、外部送信は0回
- スクリプトは本record内の全文が正本（scratchpadの実行copyは揮発）
