# セッションログ前置record解釈（IC-SESSION-LOG-PREFIX-INTERPRETATION-001）事前走査 v1

- 記録日：2026-08-17
- 指示者：利用者（Human）。選択文言：「Aで採用。仕分けrecordを作成し、事前走査から着手して」→
  作業別計画の提示後「計画を確認した。先行commit→正式検索→事前走査record固定まで進めて」
  （いずれも2026-08-17 chat）
- 記録者：Claude
- 種別：契約候補定義前の事前走査（6手順。`docs/development/prompts/scope-prescan-run.md`の
  適用第5号）。契約定義・実装・既存試験の書換えは含まない
- 範囲の基準：仕分けrecord
  `records/development/2026-08-17-session-log-prefix-interpretation-triage-decision-v1.md`
  （採用・Task Contract形態・範囲骨子3点＝前置4種の正準規則・敵対fixture・遡及再解釈）
- 必読入力：文字列理解の失敗類型と対策原則（§5 digest表に固定）——本主題は構造層（先頭record
  判定）の変更そのもの。正準位置の原則（§2-2）を「正準列」へ拡張する設計であり、敵対fixture
  （§2-8）が中心適用される
- 基準commit：`c0bc768`（証明書commit時点・作業tree clean）

## 0. 一枚要約（人向け）

主要な発見は3つ。
(1) **解釈器は変更不要の見込み**：Claude解釈器（`parse_claude.py`）は`type`が会話（user／
assistant）以外のrecordをissueとして読み飛ばす寛容な実装で、前置recordに既に耐性がある。
変更は判定側（`source_kind.py`）に局所化できる。
(2) **遡及は自然に起きる**：保全処理は毎回全fileで解釈を試行している（8/16実測：非対応68件が
毎回計上）。判定を拡張すれば次回の通常実行で非対応分が解釈済みへ遷移する。専用の遡及機構は
不要で、遷移の機械照合だけを受入条件にする。
(3) **既存試験5 fileに非対応・前置前提の検査**があり、期待値修正（fixture差し替え）の範囲を
契約候補に明示してHuman承認を得る必要がある。

## 1. 手順1：所在特定【実測】

| 部品・結合点 | 所在 | 状態 |
| --- | --- | --- |
| 判定（変更対象） | `tools/session_logs/source_kind.py` 12行`_identify_first_event`・41行`_first_record`・53行`identify_source_kind_bytes`・58行`identify_source_kind`・68行`identify_auxiliary_kind` | 先頭record 1個で判定。前置スキップの挿入点 |
| 振り分け（無変更見込み） | `tools/session_logs/source_adapter.py`（`_LOG_PARSERS`・`_BYTE_PARSERS`・`UnsupportedSourceKind`） | 判定結果で3解釈器へ振り分けるだけ |
| 解釈器（無変更見込み） | `tools/session_logs/parse_claude.py` 153行`_parse_lines` | `type`非会話recordを`unsupported_event` issueとしてスキップ済み（前置耐性）。前置はissue計上→`parse_issues` state（succeeded扱い）になる点は§6論点 |
| 呼び出し側（遡及の自然経路） | `tools/session_logs/eventual_preservation.py` 760行`reconcile_source_root` | 発見した全fileへ毎回`collect_source`→解釈試行。判定拡張だけで次回実行時に再解釈される |
| 転写再生成（受入確認対象） | `tools/session_logs/regeneration.py` 44行`regenerate_transcript`・107行`regenerate_artifact` | 保全済み範囲からの再解釈経路。CLI（`cli.py`）から利用 |
| 補助分類の利用（互換確認対象） | `tools/session_logs/private_validation.py` 145行・`tools/session_logs/cli.py` 360行 | `identify_auxiliary_kind`の全利用箇所（2箇所） |
| 前置4種の実物 | `queue-operation`（`operation`・`sessionId`・`content`）・`mode`（`{"type":"mode","mode":"normal","sessionId":…}`）・`custom-title`（`{"type":"custom-title","customTitle":…,"sessionId":…}`）・`started`（`agentId`・`key`） | 実物採取済み。正準列を実物基準で定義できる |
| 規模 | claude namespace台帳543件（成功475・非対応68。2026-08-16実測と一致）。新規はほぼ全件が前置開始（当project 26 file中queue-operation 24・mode 2・本文形式開始0） | 遡及対象と実害の規模 |

## 2. 手順2：import元【実測】

- `source_kind`のimport元：tools側7 file（`cli.py`・`eventual_preservation.py`・`pipeline.py`・
  `private_validation.py`・`read_only_entry.py`・`safe_storage.py`・`source_adapter.py`）、
  tests側7 file。
- `source_adapter`のimport元：tools側5 file（`eventual_preservation.py`・`pipeline.py`・
  `preservation_migration.py`・`read_only_entry.py`・`regeneration.py`）、tests側1 file。
- 保護試験：session_logs系関連215本（2026-08-17実測・全緑）＋`test_session_log_record_run.py`
  10本。判定の意味変更はこの全域に波及しうるため、契約のGREEN段で全session_logs系の緑維持を
  受入条件にする。

## 3. 手順4：接続点【実測】

1. 変更対象は`source_kind.py`に局所化（判定の意味変更）。`source_adapter.py`・`parse_claude.py`は
   無変更見込み（§6論点9の裁定次第で解釈器に限定的変更の可能性）。
2. **既存試験の期待値修正**：非対応・前置前提の検査が5 fileに分布
   （`test_session_log_source_kind.py` 1・`test_session_log_eventual_preservation.py` 3・
   `test_session_log_record_run.py` 1試験・`test_session_log_cli.py` 8＋auxiliary 1・
   `test_session_log_private_validation.py` 2）。書換え範囲を契約候補に明示しHuman承認を得る
   （AGENTS.md §2：未承認の既存Test書換えで停止、の事前解決）。
3. record-run wrapper（完了済み作業単位）：変更不要。ただし完了後は非対応件数が縮小（本文なし
   補助・未知種別のみ）するため、手順書`docs/development/prompts/session-log-record-run.md` §2の
   非対応説明の改定（1段落）が契約範囲に入る。
4. 補助分類の意味変化：「本文recordを持たないfileだけが補助」へ。利用2箇所の互換確認が能力2。
5. G30・レビュー基盤module：非対象（別module。休止決定と矛盾しない）。
6. 保全機構（raw先行保存）・一件用安全保存：不変。

## 4. 手順5：正式再利用検索【実測】

- 作業別計画（schema 2・能力3件：前置スキップ判定・補助分類整合・遡及確認）：
  `records/development/2026-08-17-session-log-prefix-interpretation-reuse-search-plan-v1.json`
  （先行commit `a12cc84`）
- 一操作入口の結果：`status: completed`・HEAD `a12cc84…`・**`start_allowed: true`（全能力）**・
  直接一致32件・手掛かり一致688件・比較群589件・検索材料なし能力0件・参照欠落0件
- 能力別直接一致：能力1＝5件（`source_kind.py` 4・`source_adapter.py` 1）、能力2＝3件
  （`cli.py`・`private_validation.py`・`source_kind.py`各1）、能力3＝24件
  （`eventual_preservation.py` 12・`regeneration.py` 4ほか）
- 証明書：`records/development/2026-08-17-session-log-prefix-interpretation-reuse-search-attestation-v1.json`
  （commit `c0bc768`。SHA-256は§5表）
- 直接一致の要点：3能力とも既存session_logs部品が直接の流用元（判定拡張は`_identify_first_event`・
  `_first_record`の拡張、遡及確認は`reconcile_source_root`＋`regeneration`の既存経路）。
  lifecycle・再利用方法の裁定はHumanに残る（契約候補で扱う）。

## 5. digest表（契約候補v1の固定入力）【実測】

```text
1d59c0eec54a68eeee6cb8dfa93d4dee963a0e29662cf3e9ce5ee89648ae2cd7  tools/session_logs/source_kind.py
5233b75a02a0f297d05ea45706711072a72979539378a5d7d592c7698814e652  tools/session_logs/source_adapter.py
f0a9aa7ce8ca6478a2c389c60b67b3fd13a6b00e9562f01c5b5e675889269b72  tools/session_logs/parse_claude.py
9a22242f64b3137849f3d39d25e2b450a7dce65938ed8e6f9f41379e329f3c18  tools/session_logs/eventual_preservation.py
bbd60e1c2232d245e67bd31c1ce87c17acb3355c5aea3cea37253ea8db76e7f8  tools/session_logs/regeneration.py
b06ac88722c79cb3671d9aa5a46188a118a5c8ec4250e2e36103214d499481fc  tools/session_logs/private_validation.py
ff1f3ebdb829eff58b60c60194ac891786a433af7a4d3df3cca153b05a200443  tools/session_logs/cli.py
a3ddec9c2e2152cd72408bfa96da4b56a4810529f36846ed885f14a691ca220e  tools/session_logs/record_run.py
b126447001c27abf9a3b435254e2743b668880896d19b3c5b4d338e2f0777e9b  tests/test_session_log_source_kind.py
641d7a040fe645a1f982f7d547e68cacfeff99410e837374f0632d55f05dd317  tests/test_session_log_parse_claude.py
68abf90cf8f04088a662f55d178d9af3a46f450df87e100d2072cd088b0f1fd5  tests/test_session_log_source_adapter.py
42a8574266c99ff24212e1cbc55b9c2b949942999235f19ce582f3467bdd7edf  tests/test_session_log_regeneration.py
9c753dc67143e40bb7016e0ed62a5f56f4ad84ed0d61aa60b7ba1ca482941b4a  tests/test_session_log_eventual_preservation.py
fce519ee3f217c768782ddafadb93d1db46e71d403ab558f8ccb7327d02e187c  tests/test_session_log_record_run.py
08ee865f82fb9f4506b7cdc4ef791c312e15da05cd9358ff9c10fa77557997b9  tests/test_session_log_cli.py
801aa743b2d267e6225b0b43c6acb265f8ac2a670def55d1716ccf990ea12a43  tests/test_session_log_private_validation.py
c80f9ae9ceca8e94ecf2ddcb67a425eee6551cfbe05ed0a5fb9fec932643d85a  records/development/2026-08-17-session-log-prefix-interpretation-gap-observation-v1.json
79df3764ddf4872883b16de1aad259672837be96e0c1baea89ac63f8f76ba196  .reviewcompass/workflow/improvement-candidates/ic-session-log-prefix-interpretation-001--v1.json
baf2bfa9a8ac2c91cf03b81410b5806e8c23d450fa6b287e7d8a031e6f95bffb  records/development/2026-08-17-session-log-prefix-interpretation-triage-decision-v1.md
ea482a3c7653b0966316012f43cc87ae426cdd5e429348a7f96c4e7f05ecd7b6  records/development/2026-08-17-text-interpretation-failure-principles-reference-v1.md
e1a25223df1b3bc58749940150b6c4a79cda20e83b04cc20f20700d723b57893  docs/development/prompts/session-log-record-run.md
e9680cf17eec303303673e6ddcb7b1206260d596179c675659ba3e488e47a96e  records/development/2026-08-17-session-log-prefix-interpretation-reuse-search-plan-v1.json
f17f9a951e99d4fe4d583b02389ba9c2d9370585631139c0379d89d64acc9eae  records/development/2026-08-17-session-log-prefix-interpretation-reuse-search-attestation-v1.json
```

## 6. 契約候補へ渡す論点【記録】

1. **正準列の定義**：既知前置4種の許容形（種別ごとの必須欄＝§1の実物基準）と、前置の連続数の
   扱い（無制限スキップにしない上限、または「最初の判定可能recordまで」の割り切り。fail-closedの
   範囲設計）。
2. 判定の互換：先頭が本文形式・Codex 2形式のfileは従来どおりの判定（変更なし）を試験で固定。
3. **前置偽装の敵対fixture**：本文recordを装う前置・前置を装う本文・未知種別の混入・前置のみで
   本文が無いfile等をRED段へ標準で含める（必読原則record §2-8）。
4. **既存試験の書換え範囲の承認**：§3-2の5 file。fixture差し替え（前置前提→本文なし補助・
   未知種別前提へ）の一覧を契約候補に明示する。
5. **遡及の受入条件**：実環境実行で非対応68件が「解釈済み＋残存（本文なし補助・未知種別）」へ
   遷移することの機械照合（record-run要約の非対応件数の前後比較を含む）。
6. 補助分類の意味の明文化：「本文recordを持たないfileだけが補助」。`mode`種別の登録有無も含む
   （現在`identify_auxiliary_kind`に未登録）。
7. 手順書`session-log-record-run.md` §2の非対応説明の改定（1段落）。
8. **前置recordのissue計上の扱い**：判定側だけの変更だと、前置recordは解釈時に
   `unsupported_event` issueとして計上され、ほぼ全fileが`parse_issues` state（succeeded扱い）に
   なる。(a)許容する／(b)解釈器も前置4種を無issueでスキップする（`parse_claude.py`への限定的
   変更が入る）——の設計裁定。
9. 命名・schema：判定の戻り値語彙（"claude"のまま）・新語彙の要否。

## 7. 未実施

- 契約候補v1の起草（範囲・受入条件・RED/GREEN段の定義→Human承認）、実装、既存試験の書換え。
