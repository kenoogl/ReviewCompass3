# 測定ブロック完全性guard 実行Evidence v1

- 記録日：2026-08-18
- 指示者：利用者（Human）。文言「コストを了解。guardの実装を再開してください。注意点として、
  デプロイ先の環境依存の点を考慮しなければならない」（2026-08-18 chat）
- 記録者：Claude
- 範囲固定：作業票`docs/development/2026-08-18-measurement-block-integrity-guard-work-ticket-v1.md`
- 事前走査・根因調査：同prescan v1・
  `records/development/2026-08-18-measurement-block-nondeterminism-investigation-v1.md`
- 基準commit：`2131ae5`→文書commit `9eb4cb3`→証明書commit `82e7766`→実装は本recordと同一commit

## 1. 成果物

- `tools/development/measurement_block.py`【強化】：二重実行guard（一致→従来互換の1回分記録＋
  「完全性：二重実行一致」／不一致→`non_deterministic`・両回全文記録・終了コード1）・
  実行体絶対path記録・実行環境記録（`platform.platform()`）。
- `tests/test_measurement_block.py`【拡張】：追加3本（一致記録・非決定検出・環境記録）＝計10本。
  既存7本は無変更。
- `docs/development/prompts/scope-prescan-run.md`【追記】：guard注記＋
  「**測定コマンドは読み取り専用に限る**」の要件化。
- 事故実例の差し替え：欠落を起こした宣言file（SHA-256 `c474a388…`）＋guard付き再生成の完全版
  measurement（対策2の事前走査入力として本recordと同時commit）。

## 2. RED→GREEN【terminal実測の転記（測定tool自身が対象のため例外）】

- RED：`3 failed, 7 passed`・単独終了コード1。
- GREEN：`10 passed`・単独終了コード0。`git diff --check`合格。

## 3. dogfooding（事故実例での実証）【機械出力の転記】

```text
{"entry_count": 4, "failed_count": 0, "incomplete_count": 0, "non_deterministic_count": 0, "output_path": "records/development/2026-08-18-plan-writer-prescan-measurements-v1.md", "schema_version": 1, "status": "ok"}
```

再生成物は全entry「完全性：二重実行一致」・実行環境`macOS-26.5.1-arm64-arm-64bit-Mach-O`を
自己申告し、計画record一覧は完全（欠落していた11件を含む）。

## 4. 受入条件の照合

| # | 条件 | 結果 |
| --- | --- | --- |
| 1 | RED：追加3本のみ失敗・既存7本緑 | 合格（§2） |
| 2 | GREEN：10本単独0 | 合格（§2） |
| 3 | dogfooding：事故宣言の再実行が0・全entry一致・一覧完全 | 合格（§3） |
| 4 | 手順書へ読み取り専用限定とguard注記 | 合格（§1） |
| 5 | 証明書`start_allowed: true` | 合格（commit `82e7766`。なお検索は退避前に`uncommitted_repository_state`で正しく停止＝fail-closedの実働確認を兼ねた） |
| 6 | diff・意味単位commit・transition | diff合格。commit・transitionは本record commit後に実施 |

## 5. 環境依存への対応（利用者指摘の反映）

生成物が**実行体の絶対path**と**実行環境（OS種別と版）**を自己申告するため、デプロイ先
（OS・PATH・同名別実装が異なる環境）で測定しても、「どの環境の・どの実体による事実か」が
record自体から機械判読できる。測定は環境に束縛された記録である、を構造で明文化した。

## 6. 未実施

- TODO反映とcommit。push（利用者の運用に従う）。対策2（計画JSON writer）の再開（Human指示ごと。
  事前走査の実測は本recordで完全版へ差し替え済み）。
