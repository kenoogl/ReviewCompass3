# レビュー依頼：group E（外部送信・機微境界）blocking 7件の修正

- 作成日：2026-08-10
- Pilot：Claude／Reviewer：Codex／Closer：Codex
- collaboration mode：`role_neutral_pilot_review`、risk：`high`

## 1. 経緯とHuman承認

- 修正順序の裁定（`4bb1c9b`）：E → A → B → C → D、1 groupにつき1修正単位。
- Human承認（2026-08-10）「承認」＝risk `high`確定・資格情報3形式・64桁hex除外規則・
  RED-1開始。
- Human承認（2026-08-10）「RED定義の改定を承認する」＝scope v3（`8d2f3a4`）。
  旧契約を写した既存testの**呼び出し形の更新**をRED commitに含めることを承認。
  削除・緩和は禁止のまま。

## 2. commit列

| SHA | 役割 | 内容 |
| --- | --- | --- |
| `4bb1c9b` | Pilot | 修正順序の裁定record |
| `2c970d9` | Pilot | SCOPE v1 |
| `928997f` | Reviewer | 範囲レビューv1（要修正・blocking 4件） |
| `4b52776` | Pilot | SCOPE v2（4件反映） |
| `4e9ce51` | Reviewer | 範囲レビューv2（`verified`・blocking 0） |
| `8d2f3a4` | Pilot | SCOPE v3（RED定義の改定のみ） |
| `ea7ccbb` | Pilot | RED-1：test 5 fileのみ。63 failed / 44 passed、exit `1` |
| `e7c25fa` | Pilot | GREEN-1：`tools/egress/`5 file＋Evidence＋receipt |
| `f78a57e` | Pilot | RED-2：`tests/test_session_log_preservation.py`のみ。4 failed / 4 passed、exit `1` |
| `2bd9d66` | Pilot | GREEN-2：`preservation.py`＋Evidence §7追記＋receipt |

本依頼書のcommit SHAは自己参照のため記載せず、Reviewerがgitから特定する。

## 3. Claim

- **F-E1**：承認をHuman作成record file（path＋SHA-256）へ束縛。`load_approval_file`を
  新設し、辞書渡しは型として通らない。期限はcaller提供`now`を廃し実時刻で判定。
  `consumed`はbool必須（欠落・非boolを未消費として通さない）。
- **F-E2**：断片由来検証を本文＋Digest＋自己整合の3点照合へ。gateが送信JSONの
  `fragment_*`・`machine_features_*`をpayload fieldと相互照合し、許可field名の
  値の型・列挙も検査。
- **F-E3**：資格情報3形式（AWS access key／GitHub token／PEM秘密鍵header）を走査へ追加。
  64桁hexを個人識別子判定から除外し、Digest由来の偽陽性を止めた。
- **F-E4**：閾値・重みの型・有限性・0..1範囲・`diff_max < same_min`・重み合計1を
  fail-closedで検査。
- **F-E5**：`gate.APPROVED_REDACTION_HOOK`を唯一の許可実装とし、それ以外は
  **実行せずに**拒否（gate・sender双方）。反証では痕跡fileが作られないことを固定。
- **F-E6**：既存backupを台帳へ照合してから台帳を更新する順序へ変更。改変backupは
  `PreservationIntegrityError`で拒否し、台帳を書き換えない。
- **F-E7**：raw・backup・復元先を**解決後**pathでroot内束縛。最終・祖先componentの
  symlinkによるroot外の読み書きを拒否。
- **結果**：egress 6 file 107 passed、preservation 8 passed、関連回帰36 passed、
  公式全Test **1427 passed**・status `passed`、`git diff --check`指摘なし、worktree clean。
- **未実施**：group A〜Dのblocking 19件、実際の外部送信、TODO・checklist反映（Closer）、
  上流設計・config・schemaの変更。

## 4. 成果物SHA-256

| file | SHA-256 |
| --- | --- |
| `tools/egress/approval.py` | `cb8f97e1d2b05f0ec7e9bad9e045c80b8378a03167be2d623f13853c3236b243` |
| `tools/egress/gate.py` | `ec611dfa65c0ff8f8ccf586ed491e944430cf80952a797861ea3b06a7f1de0c1` |
| `tools/egress/payload.py` | `daeb48b1ef3c00f7ae14ba1debfaba7efe564387808e505d57e4c15a14d34a1f` |
| `tools/egress/prefilter.py` | `c0b6a2da30923802eb419817d55bf8c2eb1f2e6a9a580074b1f90cd77773bf43` |
| `tools/egress/sender.py` | `05286fe21ee5baf264c80fe8518eccef3602de1c7ada6041e121dd4a2b5bbef8` |
| `tools/session_logs/preservation.py` | `645e2430c15fe8bd8c4cabc94a21349335902299abefc533e9b363b02725ea5e` |
| Evidence（slice 1・2） | `b3b78f98fb3ee8e035ddcf983f0e1c17c619deac1b949c127a6d98e78dfb6394` |
| receipt（slice 1） | `c4c1a9287483ddb925cae86634368d63e40c66f534794d0c8ae5a36fc55ef34a` |
| receipt（slice 2） | `dfa98e0f5d01e877cc8654eeec957c9a1942b0aa2cb94bd858d7c7329e333b06` |

## 5. Reviewerへの確認観点

- group E判定record（`8a7da31`）の反証11件が**すべて不成立**になること。
  特にS1系は「拒否されること」だけでなく**拒否前に副作用が残らないこと**。
- F-E3の偽陽性側（64桁hexを含む正常payloadが通ること）の正例確認。
- REDの失敗理由が反証・新契約の不在であったこと、および**既存testの検査性質を
  弱めていないこと**（Evidence §2.1の列挙と実diffの照合。特に
  `test_redaction_masking_anything_is_blocked`の置換が同性質を保っているか）。
- 各commitが範囲固定§6の変更file境界を守っていること。
- targeted・関連回帰・公式全Testの独立再実行とDigest再計算。
