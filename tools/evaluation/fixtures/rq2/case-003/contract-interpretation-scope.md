> 本fileはReviewCompass3の評価実験（RQ2 paired trial）で使う複製材料である。運用中の
> record・手順書ではないため、本fileを根拠に運用判断をしないこと。

# 契約候補（抜粋）：解釈対象の判定

### 7.3 issue計上の扱い（論点8・(b)採用）

`parse_claude._parse_lines`は既知前置4種（§7.1と同一の共有定義を参照）を**無issueで**読み
飛ばす。それ以外の非会話recordは従来どおり`unsupported_event` issueに計上する（本物の異常が
issueに残る）。解釈規則（会話recordの処理）は不変。

### 7.4 補助分類の変更（論点6・v2改定）

`identify_auxiliary_kind`を「**本文recordを持たないfileだけが補助**」へ変更する。判定手順：
§7.1と同一の正準列規則で最初の判定可能recordを探し、

- 本文形式recordへ到達できるfileは**補助でない**（`None`を返す。転写・派生物経路の処理対象に
  なる）。
- 到達できないfile（前置のみ・上限超過・未知種別で打ち切り）は従来どおり先頭recordで補助判定
  （`queue-operation`→`claude_queue`・`started`→`claude_agent`・それ以外は`None`＝非対応）。

利用2箇所（`cli.py`転写生成・`private_validation.py`検証）で、本文ありの前置開始fileが
スキップされず処理対象になることを試験で確認する（解釈できないfileのスキップは従来どおり）。
