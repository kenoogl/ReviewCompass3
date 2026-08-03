# Session Transcript Eventual Preservation RED Evidence V1

- evidence_id：`RC3-SESSION-TRANSCRIPT-EVENTUAL-PRESERVATION-RED-2026-08-04-V1`
- observed_at：`2026-08-04T00:00:23+09:00`
- Task Contract：`TC-SESSION-TRANSCRIPT-EVENTUAL-PRESERVATION-2026-08-03-V1`
- lifecycle：`test_first / red_verified`

## 固定Test

- path：`tests/test_session_log_eventual_preservation.py`
- SHA-256：`a41f69189d26760eeee9debdeb2da39a5e73328083039b71d5536008c7aac45c`
- Task Contract SHA-256：`981e7cb1e7344f576afe3dbaf9fee94462e353980e4944b7fd2bd33401e595cf`
- implementation Decision SHA-256：`1fe3c2a6cf8a3430ffb9a290a437dbc34777d2514beac910a26f52a419732262`

固定したAcceptanceは、初回と同一再実行、追記、部分行、中断復旧、source divergence、Git境界拒否、
Claude／Codex exec／Codex rollout、source missing／unknown、安全な手動CLI報告である。

## RED実行

```text
python3 -m pytest -q tests/test_session_log_eventual_preservation.py

11 failed in 0.16s
```

失敗理由は次の未実装に限定された。

- `tools.session_logs.eventual_preservation` module未実装：10件
- `collect-eventual` CLI入口未実装：1件

既存source parser、raw preservation、redaction、entryの既存commandに由来する別failureはなかった。
このREDを固定したまま最小実装へ進む。
