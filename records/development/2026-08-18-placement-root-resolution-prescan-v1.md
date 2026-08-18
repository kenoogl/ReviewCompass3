# 配置依存3箇所の解消（デプロイ方針4b-1）事前走査 v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。選択文言「配置依存3箇所の解消を先に片づけてください」（2026-08-18 chat）
- 記録者：Claude
- 根拠authority：デプロイ方針record §3論点4b-1（先行小作業として独立着手可の裁定は§4）
  `records/development/2026-08-17-deployment-policy-decision-v1.md`
  （SHA-256 `ad3bbf84931f55d27c62e5243fede3fbfe2cc4c4d97cc87404ccab969e597671`）
- 改善候補record：無し。同record §4が本件を「任意・改善候補経路」の先行小作業として裁定済みで
  あり、利用者の直接指示を仕分け相当として着手する（副産物4件の委任実施と同型）
- 基準commit：`bc0639b`（作業tree clean）
- 必読入力の適用：文字列理解の失敗類型原則は「文書の機械解析・LLMの読み書き・外部送信メッセージを
  含む部品」に課される（scope-prescan-run.md）。本件はpath解決のみでいずれにも該当しない（適用外）

## 0. 一枚要約（人向け）

親ディレクトリ遡りはtools配下に**ちょうど3箇所**（機械検索で一覧を閉じた）。ただし想定と違う
事実が2つあった。

1. `tools/common/paths.py`は**既に存在する**が、役割は「path境界判定」（`within`）の正本であり、
   根の解決は未実装。同fileは指紋固定試験（`tests/test_common_module_pins.py`）とHuman承認事項
   （`DEC-SHARED-FUNCTION-POLICY-001`）の下にあるため**触らず**、新module
   `tools/common/roots.py`を新設する。
2. `entry.py`はhook・schedulerからfile直接起動されるcwd非依存入口で、package importの**前に**
   根をsys.pathへ入れる自前bootstrapを持つ。単純なimport置換は循環するため、file位置からの
   読込みで委譲する。

## 1. 手順1：所在特定【実測】

`grep -rn "parents\[" tools/ --include="*.py"`の出力そのまま（全件）：

```text
tools/session_logs/record_run.py:21:PROJECT_ROOT = Path(__file__).resolve().parents[2]
tools/session_logs/entry.py:14:PROJECT_ROOT = Path(__file__).resolve().parents[2]
tools/deployment/trusted_claude_transport.py:74:    return Path(__file__).resolve().parents[2]
```

デプロイ方針record 4b-1の3箇所と一致し、他に該当は無い。

流用元（型）：RC2 `/Users/Daily/Development/ReviewCompass2/tools/paths.py`
（SHA-256 `24abb990be50f35f2895dabee355a99c7a0721c7ba9a08233e0c1f97c10aa337`）。
`repo_root()`＋`app_dir()`の2関数で、遡りをmoduleへ一元化する型である。本作業は`repo_root()`
のみ移植する。`app_dir()`は配置規約（deploy-manifest＝4b-2）の領分であり対象外。

## 2. 手順2：import元と波及【実測】

- `record_run.py`：`PROJECT_ROOT`の使用は88行（subprocessのcwd）と186行（`--repository-root`
  既定値）。起動は`-m tools.session_logs.entry record-run`（手順書固定）または
  `entry._load_module`経由＝**package文脈のみ**。file直接起動は手順書・hooks・schedulerの
  いずれにも無く、政策`DEC-SHARED-FUNCTION-POLICY-001`の2が「path直接起動を前提にしない」と
  定める。
- `entry.py`：`PROJECT_ROOT`の使用は18行（sys.path bootstrap）**のみ**。`hooks.py` 38行・
  `scheduler.py` 56行等が`with_name("entry.py")`でfile直接起動commandを生成する（cwd任意）。
  よってentryは自前で根を解決する必要が残る。
- `trusted_claude_transport.py`：`_source_root()`の使用は93行・235行（`source_root`引数の
  既定値）。同fileは配布対象外（`TRUSTED_RUNTIME_FILES`に含まれない）かつ`-m`起動のみ
  （既に8行で`tools.common.digests`をimportしており、file直接起動は今日も不能）。配布済み
  dispatch（`tools/deployment/installed/trusted_review_send_dispatch.py`）は本fileをimport
  しない（機械検索）。
- 試験側：3fileの内部属性・ソース文言を固定する試験は**無い**（機械検索。
  `test_session_log_record_run.py`は公開関数を引数渡しで呼び、`test_trusted_claude_transport.py`
  は`source_root`を明示指定する）。`tests/test_common_module_pins.py`はtools/common既存5file
  （`__init__`・`digests`・`errors`・`paths`・`output`）の指紋を固定する——**roots.py新設は
  非該当で、既存pinは不変のまま**。

## 3. 手順3：digest表【実測】

`shasum -a 256`の出力そのまま：

```text
4578eee93de299b9a7b18793559186618c562c0af45a7b0a4ccdfae44df36112  tools/session_logs/entry.py
a3ddec9c2e2152cd72408bfa96da4b56a4810529f36846ed885f14a691ca220e  tools/session_logs/record_run.py
c34ed2ceb3ec37e36065cd43fb852d0bc2879bfbf184293e45f0ec3595fac0d2  tools/deployment/trusted_claude_transport.py
039512f579bf6e939d4086c1e75f848b0b4e5dba7f7170b63c21fd005b48e1ec  tools/common/paths.py
fc7dcde0b182b1ee0a8a57759f0c8bf240c5956e9258e63ae77e2c2d0cdd392e  tests/test_common_module_pins.py
```

保護対象の現状：session_logs系試験361件・単独終了コード0（TODO記載の2026-08-18実測。GREEN時に
再計測する）。

## 4. 手順4：接続点と選択肢

1. **新moduleの置き場＝`tools/common/roots.py`（新設）**。既存`paths.py`へ追記する案は、
   指紋pinの更新（＝状態固定試験の変更→`ISSUE-TEST-GROWTH-STATE-PINNING-001`の限定再開条件に
   接触）と正本変更のHuman承認を要するため採らない。新設なら既存pinに触れない。新moduleを
   pinへ**追加**するかはHumanの後続選択肢として残す（作業票§5）。
2. **entry.pyの委譲形＝file位置読込み**（`importlib.util.spec_from_file_location`で
   `../common/roots.py`を読み込み、`repo_root()`を呼ぶ）。root深度の知識（parents[2]）は
   roots.pyのみに残る。entry.pyに残るのは兄弟packageの位置（`../common/roots.py`）の知識で、
   hooks等の`with_name`型（既容認）と同類である。
3. **record_run.py・trusted_claude_transport.py＝通常のpackage import**（両者ともpackage文脈
   でのみ動く。手順2）。
4. **挙動不変**：3箇所が返す値は変更前後で同一（同じrepo rootの絶対path）。判定・schema・
   安全境界の変更なし。
5. 機械受入の形：`grep -rn "parents\[" tools/ --include="*.py"`の該当が
   `tools/common/roots.py`の1件だけになる。

## 5. 作業票へ渡す論点

1. `roots.py`新設（pin追加なし。pin追加はHumanの後続選択肢）。
2. entry.pyはfile位置読込みで委譲（bootstrap循環の解消形）。
3. record_run.pyのfile直接起動（今日も未使用・政策上前提外）はimport追加により非対応となる
   ——容認して範囲外に明記。
4. 全体で挙動不変のrefactorであり、契約は立てず軽量作業票＋RED先行で扱う。

## 6. 手順5：正式再利用検索

作業別計画（schema 2）の先行commit後に実行し、証明書を
`records/development/2026-08-18-placement-root-resolution-reuse-search-attestation-v1.json`へ
固定する（本記録時点では未実行。§7）。

## 7. 未実施

- 手順5の実行と証明書固定。
- 作業票の固定、RED、GREEN、Evidence、TODO反映。
