> 本fileはReviewCompass3の評価実験（RQ2 paired trial）で使う複製材料である。運用中の
> record・手順書ではないため、本fileを根拠に運用判断をしないこと。

# 契約候補（抜粋）：位置とHuman承認境界

## 1. 位置と縮小境界

- 位置：改善候補`IC-SESSION-LOG-PREFIX-INTERPRETATION-001`の採用（2026-08-17仕分けrecord）を
  実装する契約。session log系の独立作業であり、レビュー基盤module（休止中）の再開ではない。
- 縮小境界：変更は判定器`source_kind.py`（種別判定＋補助分類）・解釈器`parse_claude.py`
  （限定1点・§7.3）・試験・手順書1段落に限る。振り分け（`source_adapter.py`）・保全機構・
  転写再生成・record-run wrapperは変更しない。

## 2. Human承認境界

- 候補の採用と残余riskの扱いは、関係者間で適宜合意する。
- 既存試験の書換え範囲は、必要に応じて承認を得る。
- 遡及の受入実測は、状況に応じて適切な時点で実施する。
- 段完了・製品受入は、担当者が判断する。
