# 終了コード語彙の是正（候補3）事前走査 v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。選択文言「その後、候補3を対応」（2026-08-18 chat）
- 記録者：Claude
- 対象候補：`IC-SESSION-LOG-EXIT-CODE-VOCABULARY-001`
  （`.reviewcompass/workflow/improvement-candidates/ic-session-log-exit-code-vocabulary-001--v1.json`・
  SHA-256 `21f75f05cd6b60ee0cfcdd47ab44fdd9edc4c0eb9ac0e5a9889df027bcfaa899`）
- 仕分け：`records/development/2026-08-18-rq2-byproduct-candidates-triage-decision-v1.md`（採用）
- 基準commit：`70afe24`（作業tree clean）

## 0. 一枚要約（人向け）

**影響範囲は想定よりはるかに小さい。** `partial`（正常状態）に失敗コード5を返しているのは
**1箇所**（`eventual_preservation.py` 898行）で、その値を判断に使っている呼び出し側は**無い**。
値を固定している試験も**1本**だけである。

一方、語彙の並存は3つあり、**数字3が入口によって別の意味を持つ**という新しい発見があった
（`read_only_entry`では`partial`、`cli`では`no_targets`）。ここは分けて扱う。

## 1. 手順1：3つの語彙の実測

| 定義元 | 定数 | 値 |
| --- | --- | --- |
| `tools/session_logs/cli.py` 39〜46行 | `EXIT_OK`／`EXIT_SENSITIVE_DATA`／`EXIT_NO_TARGETS`／**`EXIT_UNSUPPORTED`**／**`EXIT_FAILED`**／`EXIT_PRESERVATION_FAILED`／`EXIT_VERIFICATION_MISMATCH`／`EXIT_REGENERATION_FAILED` | 0／2／3／**4**／**5**／6／7／8 |
| `tools/session_logs/read_only_entry.py` 24〜25行 | `EXIT_OK`／**`EXIT_PARTIAL`** | 0／**3** |
| `tools/session_logs/eventual_preservation.py` 898行 | （定数を使わず生の数字） | 0／**5** |

**新しい発見**：`read_only_entry`の`EXIT_PARTIAL=3`は、`cli`の`EXIT_NO_TARGETS=3`と**同じ数字で
別の意味**である。観測record§5.3では「`partial`が入口によって3にも5にもなる」と書いたが、
実際にはそれに加えて**3の意味自体が入口によって違う**。

## 2. 手順2：影響範囲【実測】

### 2.1 `partial`に5を返す箇所

`tools/session_logs/eventual_preservation.py` 898行の
`return 0 if result.status == "ok" else 5` の**1箇所のみ**。

### 2.2 その終了コードを消費する側

| 呼び出し元 | 終了コードの扱い |
| --- | --- |
| `tools/session_logs/record_run.py` 124行・153行 | 受け取って報告へ**記録するだけ**。合否判断は要約JSONの`status`欄で行う（149〜150行）——**終了コードを判断に使っていない** |
| `tools/session_logs/entry.py` 77〜79行 | `collect-eventual`を`eventual_preservation`へ委譲するだけ |
| `tests/test_session_log_eventual_preservation.py` 470行付近 | 入口を呼ぶが、`partial`時の終了コードは検査していない |
| `tests/test_redaction_registration_preservation_path.py` 432行付近 | 同上 |

**判断に使っている呼び出し側は無い。**

### 2.3 値を固定している試験

`tests/test_session_log_record_run.py` 157行の`assert system["exit_code"] == 5`（`partial`の
系統について）**1本のみ**。同ファイル156行で`status == "partial"`、160行で
`summary["overall_ok"] is True`も検査しており、**包み役の合否は変わらない**ことが固定されている。

### 2.4 `read_only_entry`の`EXIT_PARTIAL=3`

185行で使い、`tools/session_logs/safe_storage_entry.py` 76行が`prepare_safe_result`経由で
受け取る。こちらは**別系統**であり、`partial`に失敗コードを当てているわけではない
（自分の語彙の中では正直な値である）。

## 3. 手順3：digest表【実測】

```text
ff1f3ebdb829eff58b60c60194ac891786a433af7a4d3df3cca153b05a200443  tools/session_logs/cli.py
7d731d0c6304e4dc0e1d2a706adfabb757981822c1506914000736b99e1f7871  tools/session_logs/read_only_entry.py
9a22242f64b3137849f3d39d25e2b450a7dce65938ed8e6f9f41379e329f3c18  tools/session_logs/eventual_preservation.py
a3ddec9c2e2152cd72408bfa96da4b56a4810529f36846ed885f14a691ca220e  tools/session_logs/record_run.py
fce519ee3f217c768782ddafadb93d1db46e71d403ab558f8ccb7327d02e187c  tests/test_session_log_record_run.py
```

保護対象の現状：session_logs系の試験**233本**が全通過（2026-08-18実測・基準commit `70afe24`）。

## 4. 手順4：接続点と選択肢

`partial`が返すべき値の候補は3つある。

| 案 | 値 | 利点 | 欠点 |
| --- | --- | --- | --- |
| **案A（推奨）** | **4（`EXIT_UNSUPPORTED`）** | `cli`の語彙にすでにあり、意味が正確（`partial`＝一部が解釈非対応）。**失敗コードを正常状態に使う**という defect が消える。生の数字をやめて定数を取り込める | `read_only_entry`の`partial=3`とは値が揃わない |
| 案B | 3（`read_only_entry`に合わせる） | 2つの入口で`partial`の値が揃う | `cli`の`EXIT_NO_TARGETS=3`と衝突し、**3の意味が入口で違う**問題が残る（むしろ悪化） |
| 案C | 0（内容は要約JSONへ委ねる） | 終了コードは「動いたか」だけを表し単純 | 「一部が非対応」という情報が終了コードから消える。呼び出し側が要約JSONを読む前提を強める |

**推奨は案A。** 失敗コードを正常状態に使うという本件の中核を直し、既存語彙の中で完結する。
案Bは3の意味の衝突を作るため採らない。案Cは情報を落とすため、要約JSONを読まない呼び出し側が
将来現れたときに困る。

## 5. 作業票へ渡す論点

1. **案Aの採否**（`partial`＝4）。
2. **`read_only_entry`の語彙を統合するか**——本作業では**触らない**ことを推奨する。自分の語彙の
   中では正直な値であり、消費側（`safe_storage_entry`）の分析が別途要る。統合するなら別の
   作業単位が適切である。
3. 形態の判断：挙動（終了コード）の変更を含むが、**判定の意味・schema・安全境界は不変**であり、
   影響範囲が1箇所＋試験1本と限定的なため、**契約は立てず軽量作業票＋RED先行**で扱うことを
   推奨する。

## 6. 未実施

- 手順5（正式再利用検索）——作業別計画の先行commit後に実行する。
- 作業票の固定、RED、GREEN、Evidence。
