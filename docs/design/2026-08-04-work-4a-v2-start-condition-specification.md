# Work 4A v2 Start-condition Specification

状態：`approved_by_v2_design`

## Policy artifact schema

配置は`.reviewcompass/policies/work4a-freshness-policy-v1.json`とする。必須fieldは
`record_kind` (`work4a_freshness_policy`)、`schema_version` (1)、`policy_id`、`policy_version`、
`development_policy_ref`（`path`、`file_sha256`）、`change_classes`、`revalidation_required_classes`、
`content_digest`である。`change_classes`は`ordinary`、`security`、`authority`、`irreversible`の完全一致、
後者はその部分集合かつ少なくとも`security`、`authority`、`irreversible`を含む。

Digestはv2のcanonical JSON規則、参照fileはbytes SHA-256を使う。Policy fileまたは参照Development Policyの
Digest不一致は`invalid`、revalidation classは`revalidation_required`として停止する。

## Source universe record schema

配置は`.reviewcompass/policies/work4a-source-universe-v1.json`とする。必須fieldは`record_kind`
(`work4a_source_universe`)、`schema_version` (1)、`source_universe_id`、`source_universe_version`、
`include_root` (`tools`)、`include_glob` (`**/*.py`)、`excluded_roots`、`path_encoding` (`posix_relative_utf8`)、
`content_digest`である。excluded rootsはv2 design 2章の列挙と完全一致する。

writerはこのrecordだけから対象pathを決める。callerが個別path列を渡してsource範囲を変更することはできない。
recordのID、versionまたはDigestが変われば、従来Baselineは`stale`とする。

## Revert map schema

配置は`records/development/2026-08-04-work-4a-v1-revert-map-v1.md`とする。各entryは、revert commit、
戻したsource commit群、対象path群、保持したcommit群、外部`DATA_ROOT`への操作有無を持つ。
revert commit subjectは説明補助であり、対象範囲の正本ではない。

## v2 REDの開始条件

この仕様とrevert mapがGitに存在し、v2設計のDecisionが参照できる時だけ、v1 E2E testをstaleとしてv2 RED testを作成する。
