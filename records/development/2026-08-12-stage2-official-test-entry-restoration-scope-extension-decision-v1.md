# 第2段 公式試験入口の正常化 範囲追加判断 v1

- 判断ID：`DEC-STAGE2-OFFICIAL-TEST-ENTRY-RESTORATION-SCOPE-EXTENSION-001`
- 判断日：2026-08-12
- 状態：`approved_pending_independent_review`
- 置換後作業票：`docs/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-work-ticket-v2.md`
- 置換後作業票SHA-256：`6cbb24eae0397198f48bb25ba6bd56874c020119a8f443b6d5251ca04266d018`
- 置換前作業票：`docs/development/2026-08-12-stage2-official-test-entry-restoration-bootstrap-work-ticket-v1.md`
- RED commit：`354c57e1d7dd28eaa6b2e271ea3dae60ce949720`

## 1. 事象

【実測】v1のGREEN実装後に公式全試験を実行すると、1,735件中1,734件成功、1件失敗だった。
唯一の失敗は、削除済みの期限付き試験名を別の試験fileの対応表が参照していたことである。

【判断】v1の停止条件に従い、未承認のfileへ変更を広げず停止した。設定とrunnerの実装2 fileは
未コミットで保持し、対応表fileは変更しなかった。

## 2. 利用者判断

【記録】利用者へ次の三択を提示した。

1. 今対処する：`tests/test_pilot_collaboration.py`を追加し、対応表3か所だけを残した恒久試験2件へ付け替える。
2. 後回しにする：第2段を停止したままにする。
3. 元の方針へ戻る：期限付き試験の削除方針を見直す。

利用者は`1`を選択した。

## 3. 承認範囲

承認は、作業票v2が固定する`tests/test_pilot_collaboration.py`一件と`TRACEABILITY`の3 keyだけに限る。
要求本文、試験関数、製品コード、Python 3.13、第2段完了、外部送信は含まない。

技術的な開始は、異なる実行単位が作業票v2を`開始可`と判断した後とする。`修正要`なら対応表を変更せず、
レビュー結果を利用者へ返す。
