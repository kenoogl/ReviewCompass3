# 配置依存3箇所の解消（デプロイ方針4b-1）実行Evidence v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。選択文言「配置依存3箇所の解消を先に片づけてください」（2026-08-18 chat）
- 記録者：Claude
- 範囲固定：作業票`docs/development/2026-08-18-placement-root-resolution-work-ticket-v1.md`
- 事前走査：`records/development/2026-08-18-placement-root-resolution-prescan-v1.md`
- 基準commit：`bc0639b`（事前走査時）→文書commit `138858a`→証明書commit `0f2955c`→実装は本record
  と同一commit

## 1. 成果物

| file | 内容 | 変更後SHA-256 |
| --- | --- | --- |
| `tools/common/roots.py`【新設】 | `repo_root()`のみの一元化module（RC2 paths.py型） | `478476817a5fcc755c7e96f33cfe2a68f093e0a4dd26ae3405cbac2ff8d33791` |
| `tools/session_logs/entry.py` | 14行の遡りを、file位置読込み（`_load_roots`）経由の`repo_root()`委譲へ置換 | `9fd812b4b3934f167b21d8f78752487fba9a086e78f0ffe07473553c1aef159f` |
| `tools/session_logs/record_run.py` | 21行の遡りを`from tools.common import roots`＋`roots.repo_root()`へ置換 | `89c45318488cfcba9583f3626c3104803ea5b07d1f9a4284541cd350ff18e1c3` |
| `tools/deployment/trusted_claude_transport.py` | 73〜74行の`_source_root()`本体を`roots.repo_root()`へ置換 | `2d908160687d42d99c98ca8fa127c5d9ab774be43881056ff036cc4c0d9879e8` |
| `tests/test_common_roots.py`【新設】 | 一元化の構造固定＋値一致＋cwd非依存起動の6本 | `2ac8d7190a2d021685fafab4583f805fa8d240ca85b3ef78e1af871ef1f2c2ae` |

## 2. RED（実装前の失敗確認）【機械出力の転記】

```text
$ .venv/bin/python3 -m pytest tests/test_common_roots.py -q
5 failed, 1 passed in 0.06s
RED exit=1
```

失敗5本＝roots未存在によるImportError 4本＋構造固定（遡り3箇所が検出）1本。通過1本＝
cwd非依存起動の保護試験（現行挙動の保存確認であり、実装前に通るのは設計どおり）。

## 3. GREEN（実装後）【機械出力の転記】

| 対象 | 結果 | 終了コード |
| --- | --- | --- |
| `tests/test_common_roots.py` | 6 passed | 0 |
| `tests/test_trusted_claude_transport.py` | 17 passed | 0 |
| `tests/test_common_module_pins.py`（既存pin不変） | 5 passed | 0 |
| `tests/test_shared_function_sweep.py` | 25 passed | 0 |
| session_logs系file族（`tests/test_session_log*.py`＋`test_redaction_registration_preservation_path.py`） | 237 passed | 0 |
| session_logsに言及する全59試験file | 793 passed | 0 |

一元化の機械確認（出力そのまま・該当1件のみ）：

```text
$ grep -rn "parents\[" tools/ --include="*.py"
tools/common/roots.py:16:  return Path(__file__).resolve().parents[2]
```

`git diff --check`＝合格（終了コード0）。

注記：TODO記載の「session_logs系全域361件」は選別基準を再現できなかった（`-k "session_log"`＝
237・`-k "session"`＝354・言及file全域＝793）。本recordは再現可能なコマンドと件数で置き換える。

## 4. 正式再利用検索【機械出力の要旨】

- 証明書：`records/development/2026-08-18-placement-root-resolution-reuse-search-attestation-v1.json`
  （SHA-256 `fb253cca8270672f4f58d23c9da9733889972c78c5b43579a80e1e0623c23d28`）・
  `start_allowed: true`・reason `reuse_search_record_verified`
- 直接一致5件の裁定（再利用方法）：既存の共有根解決部品は**存在しない**。一致は置換対象自身の
  `trusted_claude_transport.py:_source_root`（統合＝新moduleへの委譲で解消）と、隣接の
  `tools/common/paths.py:within`系（境界判定であり責務が異なる。再利用せず併存）のみ。よって
  新設が妥当。

## 5. 手戻りの記録（手順の定めによる正直な記載）

正式再利用検索の初回実行で`--runtime-root`へ1階層深いpath（`…/reuse-search/projects/
reviewcompass3/development/data`）を渡し、私有領域内に入れ子の複製tree（`…/data/projects/…`・
4 file）を誤生成した。期待executor＝機械（コマンド転記）、実executor＝LLMの手入力引数、原因＝
手順書の`<repo外私有領域の絶対パス>`が正準値を固定しておらず、前例recordにも実値の記録が
無かったこと。対処＝正値`/Users/keno/.reviewcompass3-private/reuse-search`で再実行（new-only
停止→未commit証明書の除去→再実行）し、入れ子treeは4 file全部が当該誤実行の生成物であることを
時刻で機械確認のうえ除去した。機械化案＝手順書の該当引数へ正準値を明記する（route：本record）。

## 6. 受入条件の照合

| # | 条件 | 結果 |
| --- | --- | --- |
| 1 | RED：新設試験が実装前に失敗（単独終了コード非0） | 合格（§2・exit 1） |
| 2 | GREEN：新設＋session_logs系＋transport＋pins＋sweep 各単独0 | 合格（§3） |
| 3 | `parents[`がtools配下で`roots.py`の1件のみ | 合格（§3のgrep出力） |
| 4 | 挙動不変（3箇所の返す値が同一） | 合格（値一致3本＋cwd非依存起動1本が緑） |
| 5 | 証明書`start_allowed: true` | 合格（§4） |
| 6 | `git diff --check`・意味単位commit・`work_unit_transition`合格 | diff合格。commit・transitionは本record commit後に実施し、TODO反映commitで完結 |

## 7. Humanの確認が要る点（作業票§5の再掲・覆せる形）

1. `roots.py`を指紋pin（`test_common_module_pins.py`）へ追加するか——追加は状態固定試験の変更に
   あたり`ISSUE-TEST-GROWTH-STATE-PINNING-001`の限定再開条件に接触するため、本作業では行って
   いない。
2. `entry.py`の委譲形（file位置読込み）の採否——現状維持（parents[2]残置）へ戻す判断はあり得る。

## 8. 未実施

- TODO反映とcommit（本record commit直後に実施）。push（従前どおり利用者の運用に従う）。
- デプロイ方針4bの残り2点（deploy-manifest・絶対パス混入lint）は本作業の範囲外のまま。
