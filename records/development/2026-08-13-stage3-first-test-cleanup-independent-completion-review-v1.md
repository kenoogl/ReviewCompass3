# 第3段 最初の試験整理 独立完了レビュー v1

- レビュー日：2026-08-13
- 判定：`verified`
- 対象計画：`docs/development/2026-08-13-stage3-first-test-cleanup-implementation-plan-v2.md`
- 対象計画SHA-256：`c470da1e4ed3b19c548b64db0d817bdec2d1236b747d3388f50eeccf8c6d1147`
- 利用者承認：`records/development/2026-08-13-stage3-first-test-cleanup-implementation-approval-decision-v1.md`
- 利用者承認SHA-256：`de6e39ebad70ae55dd0693251c57df153226e81cd2dfee7009e24a3c65be8ccd`
- 実施Evidence：`records/development/2026-08-13-stage3-first-test-cleanup-implementation-evidence-v1.md`
- 実施Evidence SHA-256：`07a3dc91515fc27445e5180988e64a40bbcf705d86bfeb42c9175dceffebce14`
- 実施前commit：`9ddf8da1788707cdb4137f172e78eb69ca14969b`
- 観測commit：`77078e2f0df592c7f650a6c8b1a6005489b20daf`
- 危険度：中

## 1. 判定

**`verified`**。

【実測】利用者が承認した二試験と、その一方だけが使う二定数だけが試験コードから削除されている。
残る六試験は変更されておらず、対象試験と正規全試験は独立再実行で成功した。G11、製品コード、設定、
履歴資料は変更されていない。この整理結果は次の第3段作業の入力にできるが、第3段全体の完了を意味しない。

## 2. 変更範囲

【実測】実施前commitと観測commitの差分は次の二fileだけだった。

- `tests/test_claude_bootstrap_entrypoints.py`：28行削除、追加0行
- `records/development/2026-08-13-stage3-first-test-cleanup-implementation-evidence-v1.md`：実施記録の追加

【実測】Pythonの構文木（プログラムの構造を機械的に表したもの）で実施前と観測後を比較した結果は、
次のとおりだった。

- 試験数：八件から六件
- 削除された試験：計画指定の二件だけ
- 追加された試験：0件
- 残る六試験の構文木差分：0件
- 削除されたfile直下の定数名：`MAP_PATH`と`REQUIREMENT_IDS`だけ
- 追加されたfile直下の定数名：0件

【実測】G11三試験、G11専用補助処理、`tests/test_pilot_collaboration.py`の`TRACEABILITY`、`tools/`、
`config/`、`docs/`、実施Evidence以外の`records/`は、実施前commitと観測commitで差分0だった。

## 3. 現役利用とG11の境界

【実測】削除した二試験名と二定数をリポジトリ全体で検索した。試験名は過去の宣言対応表、作業記録、引継ぎ文書に
履歴参照として残るが、製品コード、設定、正規入口、他の現役試験からの利用は0件だった。同名の
`REQUIREMENT_IDS`は別fileにもあるが、削除した定数とは別物である。

【実測】現行`TRACEABILITY`はG11三試験を計七回参照したままであり、その三試験も
`tests/test_pilot_collaboration_entrypoints.py`に残っている。削除したG04二試験は現行`TRACEABILITY`から
参照されていない。したがって、v1計画で見つかったG11保証喪失は今回の限定範囲へ再発していない。

## 4. 独立した試験結果

対象fileを次の単独commandで実行した。

```text
.venv/bin/python3 -B -m pytest -q tests/test_claude_bootstrap_entrypoints.py
```

【実測】六件成功、失敗0件、終了コード0だった。

正規全試験を次の単独commandで実行した。

```text
.venv/bin/python3 -B -m tools.development.policy_test_runner \
  --suite full \
  --receipt /private/tmp/reviewcompass-stage3-first-test-cleanup-independent-review-full-receipt-v1.json
```

【実測】1,737件成功、失敗0件、エラー0件、除外0件、終了コード0だった。Pythonは3.13.14、
pytestは8.4.2、代替実行はなかった。独立結果記録のSHA-256は
`bd23f273788a131e08206f407cc04174fa4515c7b5f941e2c591016a49d54abd`である。

## 5. 状態識別値と試した反証

中心判断「結果記録が観測commitの状態を表す」を否定するため、公式処理の集計値を使わず、観測時の全fileから
状態識別値を独立再計算した。

【実測】実施時の結果記録が持つ`bfeb3a3e...`は、観測commit全体からは再構成できなかった。実施Evidence一件を
除外した状態から再計算すると完全一致した。これは全試験の後に実施Evidenceを書いた計画上の順序と一致し、
試験対象コードを後から変えた形跡ではない。ただし、その結果記録単独では観測commit全体を固定していない。

【実測】この不足を独立再実行で反証した。実施Evidenceを含む観測commitの状態識別値を再計算した結果は
`f451b7fb24d3927499d62f3888e8960b0e7c755784271a432c9ee1d98ec59525`であり、独立結果記録の状態識別値と
完全一致した。その状態で正規全試験は1,737件成功したため、中心判断は維持される。

## 6. 利用者承認境界

【記録】利用者承認は、案B、未承認だった宣言対応表試験の保証廃止、対象試験file一件・二試験・二定数という
範囲に限定されている。

【実測】実差分はこの承認範囲と一致する。G11の保証廃止、製品コード整理、設定変更、外部送信、履歴書換え、
第3段完了は行われていない。

## 7. 止める指摘と報告不一致

- 止める指摘：0件
- 報告不一致：0件

実施時の結果記録が実施Evidence追加前の状態を示す点は、実施順序どおりであり虚偽報告ではない。観測commitとの
結び付きは本レビューの独立結果記録で補った。

## 8. 引継ぎと未実施

【実測】現在の`TODO_NEXT_SESSION.md`は、まだ利用者承認待ち・削除前の内容であり、観測commit後の現在位置を
表していない。本実装の変更範囲ではないため本レビューでは変更しないが、操縦役は次の作業へ移る前に正規の
TODO更新手順で、承認・実施・本レビューの結果へ更新する必要がある。

本レビューでは、成果の修正、他群の整理、G11要求証拠の裁定、製品コード整理、第3段完了判断、Claude確認、
外部送信、push、履歴書換えを行っていない。次の一作業は、操縦役によるTODOの更新と、今回の結果を踏まえた
次候補の利用者提示である。
