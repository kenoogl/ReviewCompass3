"""構造化材料の意味分類に関する暫定テスト。

lifecycle: provisional
normative_status: non-normative
promotion_required: true
"""

import hashlib
import importlib


def _provenance(documents):
  return {
    identifier: {
      "commit": "a" * 40,
      "sha256": hashlib.sha256(content.encode()).hexdigest(),
    }
    for identifier, content in documents.items()
  }


def test_classifies_by_path_shape_and_fixed_provenance():
  structured = importlib.import_module(
    "tools.extraction.structured_materials"
  )
  documents = {
    "source:schemas/unit.schema.json": (
      '{"$schema":"x","type":"object","properties":{}}'
    ),
    "source:.reviewcompass/specs/units/intent.units.yaml": (
      "schema_version: v1\nunits: []\n"
    ),
    "source:.reviewcompass/state/gate-ledger.yaml": (
      "schema_version: v1\nentries: []\n"
    ),
    "source:.reviewcompass/approvals/send.yaml": (
      "approved_by: user\napproved_action: send\n"
    ),
    "source:.reviewcompass/evidence/exchanges/raw-output.yaml": (
      "model: test\nresponse: value\n"
    ),
    "source:.reviewcompass/evidence/reviews/result.yaml": (
      "verdict: OK\nfindings: []\n"
    ),
  }

  result = structured.classify_structured_materials(
    documents,
    _provenance(documents),
  )

  assert result.status == "complete"
  assert tuple(
    (item.identifier, item.kind)
    for item in result.items
  ) == (
    (
      "source:.reviewcompass/approvals/send.yaml",
      "approval",
    ),
    (
      "source:.reviewcompass/evidence/exchanges/raw-output.yaml",
      "raw_response",
    ),
    (
      "source:.reviewcompass/evidence/reviews/result.yaml",
      "generated_evidence",
    ),
    (
      "source:.reviewcompass/specs/units/intent.units.yaml",
      "canonical_spec",
    ),
    (
      "source:.reviewcompass/state/gate-ledger.yaml",
      "state",
    ),
    ("source:schemas/unit.schema.json", "schema"),
  )
  assert result.unresolved == ()
  assert len(result.digest) == 64


def test_blocks_unknown_shape_parse_failure_and_stale_provenance():
  structured = importlib.import_module(
    "tools.extraction.structured_materials"
  )
  documents = {
    "source:schemas/not-a-schema.json": '{"name":"value"}',
    "source:.reviewcompass/specs/broken.yaml": "key: [",
    "source:.reviewcompass/specs/stale.yaml": (
      "schema_version: v1\nrequirements: []\n"
    ),
  }
  provenance = _provenance(documents)
  provenance["source:.reviewcompass/specs/stale.yaml"]["sha256"] = (
    "b" * 64
  )

  result = structured.classify_structured_materials(
    documents,
    provenance,
  )

  assert result.status == "blocked"
  assert tuple(
    (item.identifier, item.reason)
    for item in result.unresolved
  ) == (
    (
      "source:.reviewcompass/specs/broken.yaml",
      "parse_failure",
    ),
    (
      "source:.reviewcompass/specs/stale.yaml",
      "stale_provenance",
    ),
    (
      "source:schemas/not-a-schema.json",
      "unknown_semantic_shape",
    ),
  )


def test_classifies_versioned_review_observations_and_scoped_approvals():
  structured = importlib.import_module(
    "tools.extraction.structured_materials"
  )
  documents = {
    "source:.reviewcompass/specs/f/reviews/run/sensitivity-check.yaml": (
      "schema_version: v1\n"
      "check_mode: independent\n"
      "results: []\n"
      "verdict: pass\n"
    ),
    "source:.reviewcompass/specs/f/reviews/run/observation.yaml": (
      "schema_version: v1\n"
      "status: complete\n"
      "method_findings: []\n"
      "triage: []\n"
    ),
    "source:.reviewcompass/specs/f/reviews/run/exception-approval.yaml": (
      "schema_version: v1\n"
      "approved_by: user\n"
      "approved_deviation: append_record\n"
      "approval_scope: one_run\n"
    ),
  }

  result = structured.classify_structured_materials(
    documents,
    _provenance(documents),
  )

  assert result.status == "complete"
  assert tuple(
    (item.identifier, item.kind)
    for item in result.items
  ) == (
    (
      "source:.reviewcompass/specs/f/reviews/run/"
      "exception-approval.yaml",
      "approval",
    ),
    (
      "source:.reviewcompass/specs/f/reviews/run/observation.yaml",
      "generated_evidence",
    ),
    (
      "source:.reviewcompass/specs/f/reviews/run/"
      "sensitivity-check.yaml",
      "generated_evidence",
    ),
  )
