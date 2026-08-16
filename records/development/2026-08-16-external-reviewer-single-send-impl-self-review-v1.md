# 外部レビュア一回送信 実装の起草側自己レビューと文脈整理 v1

- 実施日：2026-08-16
- 担当：Claude（実装担当による起草側の事前点検。独立完了レビューの代替ではない）
- 対象：GREEN commit `2beb5c2`の実装（送信核・入口・対象試験49件）と契約v5の対応
- 方法：契約v5の§7〜§12を実装・試験と1条ずつ突き合わせ、誤合格・未接続・禁止作用・
  上位目的への悪影響の4類型で点検
- 位置づけ：外部レビュー5段手続きの第1段・第2段。独立完了レビュー依頼promptの文脈材料

## 1. 発見（軽微1件——機能への影響なし、レビュアへ開示する）

### SR-IMPL-1 応答保存呼出しに無意味な条件式が残る

【実測】`tools/external_review/gemini_send.py` 602行：
`_publish(data if data.endswith(b"") else data, ...)`。`data.endswith(b"")`は常に真であり、
実質は`_publish(data, ...)`と等価。応答bytesは無条件・無加工で保存されるため機能・安全への影響は
ない（正例試験が保存bytesの完全一致を確認済み）。見た目の乱れとして開示し、扱い（今回の指摘に含めるか
後続整理か）は独立レビューの判定に委ねる。

## 2. 契約対応の確認（主要な守りの実測点検）

【実測】次を実装・試験の両面で確認した。

1. **鍵の閉じ込め**：鍵はHTTP headerだけに置かれ、URL・台帳・標準出力・停止JSONへ現れない
   （試験`test_key_never_appears_in_outputs`が着地file全bytesと標準出力を走査）。
2. **環境値の限定**：環境読取りは選択providerの1変数だけ（`test_only_selected_provider_variable_is_read`が
   読取り名の完全一致`["GEMINI_API_KEY"]`を実測）。proxy環境変数は`ProxyHandler({})`で遮断。
3. **非追従・非再試行**：redirect handlerは`redirect_request`が常に`None`（3xxは`http_error`・応答保存）。
   HTTP要求は`_send_request`一回だけ（正例で呼出し回数1を実測）。timeout 300秒固定。TLS検証の無効化なし
   （openerへ独自SSL contextを渡していない）。
4. **台帳の順序と残存**：試行record→送信→応答保存→結果recordの順。通信失敗・HTTP異常・応答超過では
   試行recordが残り結果recordは作られない（試験3件で実測）。着地は新規作成専用一時名→bytes再読込照合→
   hard link公開→一時名削除の二段。
5. **重複と上限**：同一IDの再実行は2回目の送信なしで`duplicate_order`停止（呼出し回数1を実測）。
   累計・payload・応答sizeの各上限停止を実測。
6. **schemaの厳格さ**：root 9項目の完全一致、`schema_version`はboolを弾く厳密int、`human_approved`は
   `True`限定、NUL・単独サロゲート・`..`遡上の拒否、JSON重複keyの拒否（`object_pairs_hook`）。
7. **機微検査の範囲**：送信指示はJSONのkey名も含めて走査し、除外は正規SHA-256欄・provider固定3値・
   選択providerのmodel名合格値だけ。24文字以上の乱雑識別子は仕様どおり停止（試験で実測）。
8. **時刻の限定**：時刻取得は台帳の`attempted_at`・`completed_at`の2欄だけ。
9. **由来fileの読取り**：symlink拒否（`O_NOFOLLOW`）・通常file限定・読取り前後のstat一致検査・
   宣言digest一致・UTF-8有効・機微検査合格を全fileに要求。
10. **既存への不干渉**：egress 7 moduleは基準commitから差分0（digest固定試験）。敵対試験の不変条件
    「`tools/egress/`配下に通信手段なし」が回復（egress関連107件成功）。

## 3. 発見（限界の明示——設計どおりだがレビュアへ伝える）

- **模擬層の位置**：試験は`_send_request`関数の差し替えで通信を模擬する。実HTTP層（TLS・実redirect動作）は
  通らず、opener構成の直接検査（`test_opener_disables_proxy_and_redirects`）で代替している。実網の挙動は
  受入条件13の実送信E2E（利用者指示・未実施）で初めて実測される。
- **SR-5の分担**：「commit済みであること」の照合はmodule外（送信指示を作る手続きの義務）。moduleは
  宣言digestと実bytesの一致まで（契約§7.2の明示済み限界）。
- **台帳隠蔽の残余**：着地後の台帳fileを操縦LLMが削除する隠蔽は機械層で防げない（契約§2の受容済み限界）。

## 4. 文脈整理（依頼promptへ含める判断済み事項・範囲外）

- **判断済み（蒸し返し不要）**：送信ごとの人の確認なし（利用者決定・契約§2）。3 provider切り替えと
  独立性検査（利用者指示）。台帳のrepository内配置（v3訂正SR-1）。置き場所`tools/external_review/`
  （v5軽微訂正・利用者承認）。module名`gemini_send`の残名は契約§11が後続整理としている。
- **範囲外（「無い」という指摘は不要）**：応答の解析・判定抽出、監査自動化、旧egress設計との統合、
  複数送信・連鎖、実送信E2E（受入条件13・後続）、製品受入（受入条件14・後続）。
- **レビュアへ特に依頼する深掘り**：(1)誤合格——試験が実装の欠陥を見逃す構成になっていないか（特に模擬層の
  差し替え位置と、独立oracle再計算の実質）、(2)未接続——定義されたが呼ばれない検査・到達しない分岐、
  (3)禁止作用——契約が禁じる振る舞い（再試行・別経路・鍵混入・proxy・redirect追従・TLS無効化・時刻の
  他用途・任意環境値）の残存経路、(4)上位目的への悪影響——既存egress不変条件・受入済み4製品への影響。
