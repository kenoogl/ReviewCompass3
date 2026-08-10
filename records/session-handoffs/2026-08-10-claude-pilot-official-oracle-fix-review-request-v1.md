# レビュー依頼：group B（公式検証oracle）blocking 5件の修正

- 作成日：2026-08-10
- Pilot：Claude／Reviewer：Codex／Closer：Codex
- collaboration mode：`role_neutral_pilot_review`、risk：`high`

## 1. Human承認

1. 包括承認（`271826a`）：「組BからDまで自律的に実行。停止条件に触れたときと、
   修正の承認が要るときだけ止めよ」——risk `high`確定・着手・RED開始・GREEN着手。
2. 「conftest.pyの追加と既存テスト1件の更新を承認する」——scope v2（`4fda1a6`）の2点。
3. 「契約recordの照合値更新を承認する」——Work 5B契約recordの指紋1箇所。

## 2. commit列

| SHA | 役割 | 内容 |
| --- | --- | --- |
| `c5cd440` | Pilot | SCOPE v1 |
| `134fed4` | Reviewer | 範囲レビューv1（`verified`・blocking 0） |
| `34e8a59` | Pilot | RED：test 4 fileのみ。13 failed / 35 passed、exit `1` |
| `4fda1a6` | Pilot | SCOPE v2：停止事象の記録と2点の承認要請のみ |
| `e07183d` | Pilot | 修正RED：既存test 1件の契約更新のみ |
| `f8c01b5` | Pilot | GREEN：実装4 file＋`conftest.py`＋契約pin 1箇所＋Evidence＋receipt |

本依頼書のcommit SHAは自己参照のため記載せず、Reviewerがgitから特定する。

## 3. Claim

- **F-B1**：集計fileの実行前存在を`test_summary_stale`で拒否。実合格0件の
  公式`passed`を`test_summary_inconsistent`で拒否（skip・xfailのみのsuiteを排除）。
- **F-B2**：receipt pathをproject root内では`records/`配下限定とし、既存`.py`への
  出力とdirectory指定を拒否。sourceの上書き経路を断った。
- **F-B3**：nodeid＋段階の組で重複計上を排除（nodeidを持たないreportは従来どおり）。
  収集errorを`record_collect_report`でerrorsへ算入し、`conftest.py`へ
  `pytest_collectreport`を結線した。
- **F-B4**：`complete`を名乗る空対応表を拒否、`red_now`のbool型を強制、
  対象test fileの解決後pathをproject root内へ束縛。
- **F-B5**：porcelainが空でもHEADとのbytes差でblocked。`git rev-parse --show-toplevel`で
  要求rootとGit rootの同一実体を束縛し、別rootへの差し替えを拒否。
- **結果**：対象6 test file 48 passed（RED前34）、公式全Test **1465 passed**・
  status `passed`、`git diff --check`指摘なし、worktree clean。
- **未実施**：group C・Dの12件、TODO・checklist反映（Closer）、
  上流設計・config・schema・receipt schemaの変更。

## 4. 成果物SHA-256

| file | SHA-256 |
| --- | --- |
| `tools/development/policy_test_runner.py` | `0f7072ab8a7c4ab9093f394858c7629e2f60c1d2b774d5fd3b640622998e5b24` |
| `tools/development/pytest_summary.py` | `febbdc68d64048c2351a343f83e121b2d06823515741d33ee1216203533d22b4` |
| `tools/development/declaration_red_map_check.py` | `151d2ef80a3ebb0dad6999dc1db63c0790541575ef0e7d7efd9da9ac7a507a61` |
| `tools/development/work_unit_transition.py` | `91726ff02cc7f86318c139913ec75d464521d2d7f389ed26cc227a45c88cb97e` |
| `conftest.py` | `1705384a41206185c38bda731706bf3ada2a024dec6f6ba3eb9f207e2350bc16` |
| Evidence | `fe3c8a82e153eb2f23b83c95073bee98b28a676ec3104a025e8c55bddf044121` |
| 公式receipt | `e3bf3347bdb094fde6831dff51eeda04dd64d4b2fe1e34a6db09c2e4a1c9cd3e` |

## 5. Reviewerへの確認観点

- group B判定record（`46f2465`）§4の反証10件（P1〜P3・S1〜S2・D1〜D3・W1〜W2）が
  **すべて不成立**になること。
- **正例側**：本repositoryの正常な公式runが`passed`のままで、件数が実行実績と
  一致すること。収集error結線（`conftest.py`）が正常runの件数を歪めていないこと。
- 修正REDの当該既存testが、**修正前実装で失敗し修正後で合格**すること（独立再現）。
  検査性質を弱めていないこと。
- Evidence §2.1に記した**RED作成中の事故と復旧**（実欠陥の発火で
  `policy_test_runner.py`が上書きされ、`git checkout HEAD --`で復元。SHA-256一致を確認）が
  現在の成果物に痕跡を残していないこと。
- Evidence §5の契約pin更新が**v2の1箇所のみ**で、契約本文・受入条件・v1が
  不変であること。
- 各commitが範囲固定（v2差し替え後）の変更file境界を守っていること。
- targeted・公式全Testの独立再実行とDigest再計算。
