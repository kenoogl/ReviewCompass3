---
source_id: SRC-RC2-SHARED-ROUTINE-001
captured_at: 2026-08-02
source_kind: predecessor-project-approved-design-and-implementation
normative_status: predecessor-evidence
confidentiality_class: project-internal
raw_snapshot_retained: false
---

# ReviewCompass2共通ルーチン台帳の継承記録

## 1. 位置付け

ReviewCompass2で承認・運用された、新規関数または共通処理の作成前に既存実装を調べ、
重複実装を防止する方針を、ReviewCompass3のTask Contract中心設計へ継承するための
参照記録である。参照元をReviewCompass3の現行正本として複製せず、固定commit、観測path、
Digest、採用判断を保持する。

## 2. 参照元identity

- repository：`/Users/Daily/Development/ReviewCompass2`
- fixed commit：`d6bbb01500002872c713412bfbd63b702a291c99`
- commit日時：`2026-07-26T20:27:38+09:00`
- 観測日：`2026-08-02`

| artifact | Git blob | observed SHA-256 |
|---|---|---|
| `.reviewcompass/architecture/shared-routines.yaml` | `79b195c699705f97ec848820fde6fbcc7d86d300` | `56e06577a4c4ae5bc23f561eff28ffe7d4422d0c8ea5ef6962cf3ea3305cbc50` |
| `.reviewcompass/specs/intent.md` | `93fe8acfa02709c5c1aa0acda0b41aaa8aee8da7` | `a24c8888d4ee4dd474801f9d6d82b0cf747854950683803f6467abf79a00a1be` |
| `.reviewcompass/specs/requirements-f6.md` | `de88384ddda0b1912e1ba5c1009f151897f880a2` | `84de83e6d824e905546546f4bc2cb408831a14121411795236b437f5bd6aa59d` |
| `.reviewcompass/architecture/decision-points.yaml` | `6f41c929e869b78e405e3e290ec9610df80fcf66` | `493cff7cd052e6bc7f292b3a142a5caa3d74fd7ee3e468cafd38065c00b0cb5d` |
| `.reviewcompass/specs/feature-partitioning.md` | `770f167b6fa6a794fca1d873ca5ecfc67af1e585` | `fb46885aa211162a3d3e6d06ee256f26c7d353768eec5e6b2060d567d06a8892` |
| `.reviewcompass/specs/glossary.md` | `ee88e97a1630a67cc9433cd6321f3ea36f0c4d84` | `55f2a159378f0d690aabb996b888830fc172f8a543ac94a479f1859d96774485` |

元の要求は`docs/sessions/2026-07-23-claude-d1eafafd-ae3d-433c-8d32-d96d76183041.md`
にも残る。観測SHA-256は
`cae443b0c428165e1b9b8ed499a3e5ff4d957bbd5a26b32453f0e43d2875abcd`である。

## 3. ReviewCompass2で確定していた内容

- intent P-5として、実装前に台帳と実コードを照合する。
- 類似候補がある場合は`reuse / extend / merge / split_with_rationale`の閉じた語彙で
  判断する。
- LLMが候補と分類を提案し、Humanが意味判断を確認する。
- 判断と統廃合履歴を追記型で保持し、廃止済みルーチンの無断復活を禁止する。
- 最初は単一YAMLの最小手作業運用とし、有効性確認後にschema検証、原子的書込み、
  機械検査へ移す。
- 新規関数または共通処理を含む変更に判断記録がなければreviewを失敗させる。

## 4. ReviewCompass3へ維持して取り込むもの

- 台帳だけでなく、固定した実コードも必ず調査対象にする。
- 類似候補に対する4分類の語彙を変更しない。
- 判断をTask Contract、Design Decision、Test、Implementation、commitへ結ぶ。
- 判断と統廃合履歴を上書きせず、廃止済みroutineの復活を検出する。
- 初期はReviewCompass3自身のImplementation Task Contractへ適用し、効果と負担を
  Pilotで測ってから正式Runtime対象の拡大を判断する。

## 5. ReviewCompass3で補強するもの

ReviewCompass2の単一手作業台帳を、そのまま唯一の事実源にはしない。

- 実コードから機械生成する`Source Symbol Index`を事実層とする。
- 人が確認した責務、alias、状態、統廃合履歴を`Reusable Routine Ledger`へ置く。
- 類似候補の有無を`candidate_found | no_candidate`として先に記録する。
- `candidate_found`の場合だけ、ReviewCompass2由来の4分類を必須にする。
- Index、Ledger、Discovery Recordをsource tree、Task Contract、Work ItemのDigestへ束縛する。
- TDDのred確認後、green実装へ着手する前に判断gateを通す。
- stale Index、未確認判断、理由のない分離、廃止済みroutineの復活では実装permitを拒否する。

## 6. Evidenceの限界

参照元raw snapshotは本repositoryへ複製していない。固定commitのGit objectを取得できる間は
blobから再構成できるが、外部repositoryとobjectの双方を失った場合は原文全体を
`non_reconstructable`として扱う。本記録はReviewCompass2の運用効果を定量的に証明する
ものではないため、重複削減率、誤判定、Human負担はReviewCompass3のPilotで測定する。
