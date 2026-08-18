# 配置依存3箇所の解消（デプロイ方針4b-1）作業票 v1（範囲固定・軽量）

- 作成日：2026-08-18
- 指示者：利用者（Human）。選択文言「配置依存3箇所の解消を先に片づけてください」（2026-08-18 chat）
- 作成者：Claude
- 種別：範囲固定文書（軽量作業票）。**挙動不変のrefactor**——3箇所が返す根の値は不変で、
  判定の意味・schema・安全境界も不変。契約は立てない
- 固定入力：事前走査record
  `records/development/2026-08-18-placement-root-resolution-prescan-v1.md`
- 根拠authority：デプロイ方針record §3論点4b-1・§4（先行小作業・独立着手可）

## 1. 目的

repository rootの実行時解決（親ディレクトリ遡り）がtools配下の3fileに複製されている。配置同型性
の原則（開発時に配置を決め、デプロイで動かさない）に基づき、遡りをRC2 `paths.py`型の一元化module
へ集め、root深度の知識を1箇所だけにする。デプロイ版作成（合図待ち）の前提を先行して整える。

## 2. 正本範囲（成果物）

1. **`tools/common/roots.py`の新設**：`repo_root()`のみ（RC2 `repo_root()`の型を移植。標準
   libraryのみ・純関数・2スペースインデント）。親ディレクトリ遡りは以後この1箇所だけに置く。
2. **3箇所の置換**：
   - `tools/session_logs/record_run.py` 21行・`tools/deployment/trusted_claude_transport.py`
     73〜74行：通常のpackage importで`roots.repo_root()`へ委譲（両者はpackage文脈でのみ動く。
     事前走査§2）。
   - `tools/session_logs/entry.py` 14行：file位置読込み（`importlib.util.spec_from_file_location`
     で`../common/roots.py`を読み`repo_root()`を呼ぶ）。file直接起動（hook・scheduler）の
     bootstrap循環を避けつつ、root深度の知識をentry.pyから除く。
3. **試験の新設（RED先行）**：`tests/test_common_roots.py`。
   - (a) 構造固定：tools配下の`.py`で`parents[`を含むのが`tools/common/roots.py`の1件だけ。
   - (b) `repo_root()`がrepository root（`pyproject.toml`のあるdirectory）を返す。
   - (c) `record_run.PROJECT_ROOT`・`trusted_claude_transport._source_root()`が
     `roots.repo_root()`と一致する。
   - (d) cwd非依存の保護：任意cwdから`entry.py`をfile直接起動して`record-run --help`が
     終了コード0（entry.pyの改修で壊しやすい中核性質）。

## 3. 範囲外

- **既存`tools/common/paths.py`（境界判定の正本・指紋pin下）には触れない**。
- **`tests/test_common_module_pins.py`への`roots.py`のpin追加**（正本へ昇格させるかのHuman
  選択肢として残す。§5）。
- deploy-manifest（4b-2）・絶対パス混入lint（4b-3）・`app_dir()`の移植。
- hooks・schedulerの起動形の変更、pip導入、RC3版`next`（デプロイ版作成の作業単位の領分）。
- `record_run.py`へのfile直接起動対応の追加（今日も未使用で、政策
  `DEC-SHARED-FUNCTION-POLICY-001`の2が「path直接起動を前提にしない」と定める。import追加に
  より非対応となることを容認する）。

## 4. 受入条件

1. RED：新設試験が実装前に失敗（単独終了コード非0）。
2. GREEN：新設試験＋session_logs系全域（基準361件・TODO記載2026-08-18実測）＋
   `tests/test_trusted_claude_transport.py`＋`tests/test_common_module_pins.py`＋
   `tests/test_shared_function_sweep.py`が各単独終了コード0。
3. 機械確認：`grep -rn "parents\[" tools/ --include="*.py"`の該当が`tools/common/roots.py`の
   1件のみ。
4. 挙動不変：3箇所の返す値が変更前後で同一であること（§2-3(b)(c)(d)の試験で機械確認）。
5. 正式再利用検索の証明書（`start_allowed: true`）。
6. `git diff --check`・意味単位commit・`work_unit_transition`合格。

## 5. Humanの確認が要る点（覆せる形で残す）

1. **`roots.py`を指紋pin（`test_common_module_pins.py`）へ追加するか**。追加は状態固定試験の
   変更にあたり、`ISSUE-TEST-GROWTH-STATE-PINNING-001`の限定再開条件に接触するため、本作業では
   行わず選択肢として残す。
2. `entry.py`の委譲形（file位置読込み）の採否。より単純な「現状維持（parents[2]残置）」へ
   戻す判断はあり得る（その場合、受入条件3は2件残しへ緩む）。

## 6. 着手後の手続き

1. 作業別計画（schema 2）作成→先行commit（事前走査・本票と同一commit）。
2. 正式再利用検索→証明書固定→commit。
3. RED→失敗確認→GREEN→全緑→Evidence→commit。
4. TODO反映→検証→commit→`work_unit_transition`→完了報告。
