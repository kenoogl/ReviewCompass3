---
source_id: SRC-RC-CONFORMANCE-001
captured_at: 2026-08-02
source_kind: predecessor-project-reverse-conformance-design-and-implementation
normative_status: predecessor-evidence
confidentiality_class: project-internal
raw_snapshot_retained: false
---

# ReviewCompass conformance-evaluationの継承記録

## 1. 位置付け

ReviewCompassで実装されていた、実装codeからrequirementsとdesignを推定し、既存仕様との
差分、仕様更新草案、reopen引き渡しを作る`conformance-evaluation`を、ReviewCompass3の
Task Contract方式へ適応するための参照記録である。参照元を現行正本として複製せず、
固定commit、Git blob、SHA-256、採用・置換・defer判断を保持する。

## 2. 参照元identity

- repository：`/Users/Daily/Development/ReviewCompass`
- fixed commit：`cab302d4b32af790628b811b3566f39d55781fa5`
- 観測日：`2026-08-02`

| artifact | Git blob | SHA-256 |
|---|---|---|
| `.reviewcompass/specs/conformance-evaluation/requirements.md` | `4260fc097e2170f968ad9cd7219a12d4de4b7881` | `7e8f93103e2da376d0f1d1d5c3a8008852f691722eb9dfd25f6cf31ac5e8d0cd` |
| `.reviewcompass/specs/conformance-evaluation/design.md` | `8ac334c94848a635f5de9dfeafa1adfc6655656b` | `bb59dcceb92b4c8a67a0315ab352fc3a4be95bdd745c0af1713a259abb058d72` |
| `tools/conformance_evaluation/generation_mode.py` | `871e60f7290a695b64e25590f1406d8d7d60aa70` | `f0f3bd11ff6410d897e30bfa86908835899c580d2f4301ae52bcf5c0c3c2b041` |
| `tools/conformance_evaluation/check_mode.py` | `f42c8fde0033b61ef091f112d1f2cea42681f916` | `47ddd2a8aa7a6445177da79d628a5d43eb3910ac38dd78934bb82b2dbd5d76a8` |
| `tools/conformance_evaluation/contract_ownership.py` | `ed03949bf711f18b207a12685e3a5f39b70b4da9` | `7fe5704f28aefda387697b82bfa0b290739786645af61d8b9f593a0d369129d7` |

## 3. ReviewCompassで保持されていた責務

- 実装から上流文書を推定する文書生成と、既存文書との照合チェックを分離する。
- 推定時に既存仕様を遮断し、後段で比較することで既存文書への追従biasを抑える。
- 推定根拠としてcode referenceと実行記録を保持する。
- 実装由来の契約を`spec-missing | code-missing | mismatch | implementation-detail |
  ownership-unclear`へ分類し、owner候補と仕様更新草案を作る。
- 草案を`draft_only`とし、requirements、design、tasks本文を直接変更しない。
- 正本変更が必要なgapをworkflow-managementのreopenとHuman判断へ引き渡す。
- 上流文書のない既存codebaseでは完全自動化せず、人間協働の初版生成として扱う。

## 4. ReviewCompass3へ維持して取り込むもの

- 実装由来の事実、差分、根拠、owner候補を構造化して保存する。
- 文書生成と適合判定を分離する。
- 派生文書から規範正本を直接更新しない。
- 意味変更候補をUpstream Revision Proposal、reopen、Human判断へ渡す。
- Provenanceを持たない既存codebase向けのHuman協働経路を残す。

## 5. Task Contract方式で置換するもの

管理下で開発したcodeでは、requirementsとdesignのLLM逆推定を通常経路にしない。
Task Contract、Test、Design Decision、Implementation、Source Symbol Index、Operational
Provenanceから機械可読なAs-Built Recordを決定的に生成し、人間向け文書をprojectionとして
導出する。大域的なDesign、Tasks、Implementation段階は復活させない。

Provenanceだけでは未記録実装を発見できないため、固定source tree、Source Symbol Index、
Testとの独立照合を残す。外部観測可能な未帰属実装はFindingとし、実装詳細はAs-Builtへ、
意味変更はUpstream Revisionへ分ける。旧code-only推定は標準経路ではなく、将来の
`legacy_reconstruction`またはProvenance完全性の独立監査へ位置付ける。

## 6. 初期適用範囲

As-Built projector、Markdown renderer、Documentation Conformance gate、legacy
reconstructionはReviewCompass3の初期開発へ入れない。初期Work 1〜8と最初のTask Contractは、
将来のprojectionに必要なidentity、relation、Digestを失わず記録するところまでを担う。
accepted Implementation Task Contractと実運用Provenanceを取得し、必要入力と欠測を実測した
後に、別Task Contractとして着手をHumanが判断する。

## 7. Evidenceの限界

参照元raw snapshotは本repositoryへ複製していない。固定commitのGit objectを取得できる間は
blobから再構成できるが、外部repositoryとobjectの双方を失った場合は原文全体を
`non_reconstructable`として扱う。参照した実装は責務と成果物形状の前身Evidenceであり、
Task Contract方式のprojection設計または効果を実証するものではない。
