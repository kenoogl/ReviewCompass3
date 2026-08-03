# Session Transcript Source Formats RED Evidence V1

- evidence_id：`RC3-SESSION-TRANSCRIPT-SOURCE-FORMATS-RED-2026-08-03-V1`
- observed_at：`2026-08-03T23:18:14+09:00`
- Decision：`DEC-SESSION-TRANSCRIPT-SOURCE-FORMATS-2026-08-03-V1`
- lifecycle：`test_first / red_verified`

## 固定した契約

- Claude、`codex_exec_json`、`codex_rollout`を一つのsource adapterから識別・解析する。
- `codex_rollout`は`response_item`を正本とし、`event_msg` echoを重複採用しない。
- user、developer、assistant messageとtool call／resultの本文を縮約しない。
- reasoning暗号内容は会話本文にせず、raw保全境界に残す。
- 未知source、未知outer event、未知itemを別形式として推測せず報告する。
- 再生成も同じsource adapterを通す。

固定Test：

- `tests/test_session_log_source_kind.py`
- `tests/test_session_log_parse_codex_rollout.py`
- `tests/test_session_log_source_adapter.py`
- `tests/test_session_log_pipeline.py`
- `tests/test_session_log_regeneration.py`
- `tests/test_session_log_private_validation.py`

## RED実行

```text
python3 -m pytest -q \
  tests/test_session_log_source_kind.py \
  tests/test_session_log_parse_codex_rollout.py \
  tests/test_session_log_source_adapter.py \
  tests/test_session_log_pipeline.py \
  tests/test_session_log_regeneration.py \
  tests/test_session_log_private_validation.py

11 failed, 12 passed in 0.20s
```

失敗理由は次の実装欠落に限定された。

- 公開Codex形式のsource kindが旧名`codex`のまま：3件
- rollout形式を識別しない：1件
- rollout parser未実装：2件
- ClaudeとCodex 2形式の共通adapter未実装：2件
- rolloutをpipeline／regenerationへdispatchしない：2件
- private validation countが旧source kindだけを持つ：2件

複数の期待を同じTestが観測するため上記分類件数はpytest failure 11件と一対一ではない。既存Claude parserと
公開Codex parserの内容解析Testは合格しており、REDは新しいsource境界が未実装であることを示した。
