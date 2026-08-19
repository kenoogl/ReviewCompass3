# 全体設計の機械検査不在 観測record v1

- 記録日：2026-08-19
- 記録者：Claude
- 種別：観測record（改善候補`IC-ARCHITECTURE-CONFORMANCE-CHECK-001`の出所）
- 提起：利用者（Human）。文言【記録】
  > 仕様駆動開発の枠組みでの課題として、全体設計がある。TDDの実装は局所的には適切であるが、
  > 全体を把握して進めることができない。現在RC3は、全体アーキテクチャの最適化はAIに委ねず、
  > 人に残す設計です。分断を解消するのではなく、分断を前提に判断を人へ寄せています。
  > モジュール構成の整合を機械で検査する仕組みはありません。この点を改善したい

## 1. 観測（根拠となる実測・記録）

1. **lifecycle宣言の分布**【実測・2026-08-19】：tools配下177 fileの先頭600字を機械集計した結果、
   `lifecycle: provisional`＝100・`lifecycle: stable`＝1（`read_only_entry.py`のみ）・
   **表示なし73**（tools/development 39件を含む）。再現＝各fileの先頭部の
   `lifecycle:`表示のgrep相当集計（本セッションのpython走査）。依存方向とlifecycle整合の
   機械検査は存在しない。
2. **横断語彙の分裂が機械検出されなかった実例**【記録】：終了コード語彙が同一部分系の3入口で
   並存し（partial=3と5、停止=4の逆向き意味）、RQ2実験のレビューが偶然表面化させた
   （`records/development/2026-08-18-rq2-adjudication-and-byproducts-v2.md` §5.3、統合＝
   `records/development/2026-08-19-read-only-entry-exit-code-unification-evidence-v1.md`）。
3. **複製の増殖が放置される実例**【記録】：試験のSHA-256補助関数14 file重複
   （`ISSUE-TEST-SHA256-FIXTURE-DUPLICATION-001`・未着手）。
4. **同型検査の先行実例**【記録】：`roots.py`一元化は「`parents[`の出現がroots.pyの1件のみ」
   というgrep検査で維持されている（`records/development/2026-08-18-operational-metrics-evidence-v1.md`
   §2）。配置allowlist（deploy-manifest）はデプロイ方針§4b-2の構想のまま未実装。

## 2. 提案の骨子（討議の要約）

全体最適化の判断は人に残したまま、**「人が決めた全体構造」を機械可読の宣言recordにし、
整合だけを機械検査する**：(1) アーキテクチャ宣言（層と依存方向・lifecycle制約・正本単一性の
概念一覧・配置規約）をHuman承認で固定、(2) 整合検査器（import解析等・違反はfail-closed列挙）、
(3) 作業単位の受入と事前走査へ組み込み（局所TDDのたびに全体整合を機械確認）、(4) 宣言の改定は
Human裁定。点在する先行部品（rootsのgrep検査・lifecycle表示・deploy-manifest構想）の集約であり、
構成の良し悪しの判断は宣言を書く人に残る（機械化しない）。

## 3. 位置づけ

デプロイ関連deferredの「コード管理機構の調査（lifecycle棚卸し）」と同枠で扱うと、棚卸し結果が
宣言初版の材料になる。改善候補への登録と仕分けは本record直後にwriter経由で実施。
