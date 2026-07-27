"""構造化材料batchの完全解決に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
import importlib

import pytest


def test_recognizes_fixed_review_artifact_shapes_under_specs():
  structured = importlib.import_module(
    "tools.extraction.structured_materials"
  )
  documents = {
    "source:.reviewcompass/specs/units/intent.units.yaml": (
      "version: 1\nunits: []\n"
    ),
    "source:.reviewcompass/specs/f/reviews/run/approval.yaml": (
      "approved_by: user\napproved_action: apply\n"
    ),
    "source:.reviewcompass/specs/f/reviews/run/parsed/a.yaml": (
      "model: test\nfindings: []\nattempts: []\n"
    ),
    "source:.reviewcompass/specs/f/reviews/run/rounds.yaml": (
      "model_results: []\ntarget_files: []\n"
    ),
    "source:.reviewcompass/specs/f/reviews/run/target-manifest.yaml": (
      "run_id: run\ntarget_files: []\n"
    ),
    "source:.reviewcompass/specs/f/reviews/run/triage.yaml": (
      "triage_status: complete\nitems: []\n"
    ),
    "source:.reviewcompass/specs/f/reviews/run/review-execution-spec.yaml": (
      "schema_version: v1\nroles: []\ntarget_files: []\n"
    ),
  }
  provenance = {
    identifier: {
      "commit": "a" * 40,
      "sha256": hashlib.sha256(content.encode()).hexdigest(),
    }
    for identifier, content in documents.items()
  }

  result = structured.classify_structured_materials(
    documents,
    provenance,
  )

  assert result.status == "complete"
  assert tuple(item.kind for item in result.items) == (
    "approval",
    "generated_evidence",
    "canonical_spec",
    "generated_evidence",
    "generated_evidence",
    "generated_evidence",
    "canonical_spec",
  )


def test_resolves_extract_merge_and_reasoned_non_selection():
  batch_module = importlib.import_module(
    "tools.extraction.structured_batch"
  )
  batch = (
    "source:spec.yaml",
    "source:summary.yaml",
    "source:duplicate.yaml",
  )

  result = batch_module.resolve_structured_batch(
    batch,
    {
      "source:spec.yaml": "canonical_spec",
      "source:summary.yaml": "generated_evidence",
      "source:duplicate.yaml": "generated_evidence",
    },
    (
      {
        "candidate": "source:spec.yaml",
        "action": "extract",
        "essence_id": "ESS-0020",
        "rationale": "実行仕様の固定契約",
      },
      {
        "candidate": "source:summary.yaml",
        "action": "merge",
        "essence_id": "ESS-0021",
        "rationale": "同じレビュー証跡族へ統合",
      },
      {
        "candidate": "source:duplicate.yaml",
        "action": "not_selected",
        "essence_id": None,
        "rationale": "同一runの重複生成証拠",
      },
    ),
  )

  assert result.status == "complete"
  assert result.extracted == (("source:spec.yaml", "ESS-0020"),)
  assert result.merged == (("source:summary.yaml", "ESS-0021"),)
  assert result.not_selected == ("source:duplicate.yaml",)
  assert len(result.digest) == 64


@pytest.mark.parametrize(
  "resolutions",
  (
    (),
    ({
      "candidate": "source:a.yaml",
      "action": "merge",
      "essence_id": None,
      "rationale": "対象なし",
    },),
    ({
      "candidate": "source:a.yaml",
      "action": "not_selected",
      "essence_id": None,
      "rationale": "",
    },),
  ),
)
def test_rejects_incomplete_targetless_or_unreasoned_resolution(
  resolutions,
):
  batch_module = importlib.import_module(
    "tools.extraction.structured_batch"
  )

  with pytest.raises(batch_module.StructuredBatchError):
    batch_module.resolve_structured_batch(
      ("source:a.yaml",),
      {"source:a.yaml": "canonical_spec"},
      resolutions,
    )
