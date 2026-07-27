"""第5段のbootstrap適合性監査契約に関する暫定テスト。"""

import hashlib
import importlib
import subprocess

import pytest


def _record(**overrides):
  value = {
    "requirement_id": "REQ-CONTEXT-001",
    "classification": "conformant",
    "target_design_id": "DES-CONTEXT",
    "implementation_evidence": (
      "tools/context.py",
    ),
    "test_evidence": (
      "tests/test_context.py",
    ),
    "rationale": "固定入力と拒否挙動を実装・試験済み",
    "gaps": (),
  }
  value.update(overrides)
  return value


def test_validates_evidence_backed_conformance():
  conformance = importlib.import_module(
    "tools.design.bootstrap_conformance"
  )

  result = conformance.validate_bootstrap_conformance(
    records=(_record(),),
    defined_requirement_ids=("REQ-CONTEXT-001",),
    defined_design_ids=("DES-CONTEXT",),
    defined_evidence_paths=(
      "tools/context.py",
      "tests/test_context.py",
    ),
    bootstrap_commit="a" * 40,
  )

  assert result.status == "complete"
  assert result.counts["conformant"] == 1
  assert len(result.digest) == 64


@pytest.mark.parametrize(
  "record",
  (
    _record(implementation_evidence=()),
    _record(test_evidence=()),
    _record(gaps=("未解決",)),
    _record(classification="unknown"),
    _record(target_design_id="DES-UNKNOWN"),
    _record(implementation_evidence=("tools/unknown.py",)),
  ),
)
def test_rejects_unsupported_conformant_classification(record):
  conformance = importlib.import_module(
    "tools.design.bootstrap_conformance"
  )

  with pytest.raises(conformance.BootstrapConformanceError):
    conformance.validate_bootstrap_conformance(
      records=(record,),
      defined_requirement_ids=("REQ-CONTEXT-001",),
      defined_design_ids=("DES-CONTEXT",),
      defined_evidence_paths=(
        "tools/context.py",
        "tests/test_context.py",
      ),
      bootstrap_commit="a" * 40,
    )


def test_requires_gap_for_nonconformant_classification():
  conformance = importlib.import_module(
    "tools.design.bootstrap_conformance"
  )

  with pytest.raises(conformance.BootstrapConformanceError):
    conformance.validate_bootstrap_conformance(
      records=(_record(
        classification="adapt",
        gaps=(),
      ),),
      defined_requirement_ids=("REQ-CONTEXT-001",),
      defined_design_ids=("DES-CONTEXT",),
      defined_evidence_paths=(
        "tools/context.py",
        "tests/test_context.py",
      ),
      bootstrap_commit="a" * 40,
    )


def test_validates_commit_blobs_test_run_design_map_and_gaps():
  conformance = importlib.import_module(
    "tools.design.bootstrap_conformance"
  )
  record = _record(
    classification="adapt",
    gaps=("GAP-CONTEXT-001",),
  )
  result = (
    conformance
    .validate_evidence_backed_bootstrap_conformance(
      records=(record,),
      requirement_design_map={
        "REQ-CONTEXT-001": "DES-CONTEXT",
      },
      evidence_manifest=(
        {
          "path": "tools/context.py",
          "blob_sha256": "1" * 64,
          "role": "implementation",
          "requirement_ids": ("REQ-CONTEXT-001",),
        },
        {
          "path": "tests/test_context.py",
          "blob_sha256": "2" * 64,
          "role": "test",
          "requirement_ids": ("REQ-CONTEXT-001",),
        },
      ),
      commit_blob_map={
        "tools/context.py": "1" * 64,
        "tests/test_context.py": "2" * 64,
      },
      test_run={
        "bootstrap_commit": "a" * 40,
        "command": "python3 -m pytest -q",
        "status": "passed",
        "passed_count": 1,
        "output_digest": "3" * 64,
      },
      gaps=(
        {
          "gap_id": "GAP-CONTEXT-001",
          "requirement_id": "REQ-CONTEXT-001",
          "category": "missing_gate",
          "component": "context_builder",
          "atomic_obligation_ids": (
            "REQ-CONTEXT-001#statement",
          ),
          "depends_on_gap_ids": (),
          "acceptance_test_ids": ("AT-CONTEXT-001",),
          "stop_condition": "gate remains absent",
        },
      ),
      requirement_dependencies=(),
      bootstrap_commit="a" * 40,
    )
  )

  assert result.status == "complete"
  assert result.gap_count == 1
  assert result.evidence_count == 2


def test_rejects_conformant_with_nonconformant_dependency():
  conformance = importlib.import_module(
    "tools.design.bootstrap_conformance"
  )
  provider = _record(
    requirement_id="REQ-PORTABLE-001",
    classification="adapt",
    target_design_id="DES-PORTABLE",
    implementation_evidence=(),
    test_evidence=(),
    gaps=("GAP-PORTABLE-001",),
  )
  consumer = _record()

  with pytest.raises(
    conformance.BootstrapConformanceError
  ):
    conformance.validate_evidence_backed_bootstrap_conformance(
      records=(provider, consumer),
      requirement_design_map={
        "REQ-PORTABLE-001": "DES-PORTABLE",
        "REQ-CONTEXT-001": "DES-CONTEXT",
      },
      evidence_manifest=(
        {
          "path": "tools/context.py",
          "blob_sha256": "1" * 64,
          "role": "implementation",
          "requirement_ids": ("REQ-CONTEXT-001",),
        },
        {
          "path": "tests/test_context.py",
          "blob_sha256": "2" * 64,
          "role": "test",
          "requirement_ids": ("REQ-CONTEXT-001",),
        },
      ),
      commit_blob_map={
        "tools/context.py": "1" * 64,
        "tests/test_context.py": "2" * 64,
      },
      test_run={
        "bootstrap_commit": "a" * 40,
        "command": "python3 -m pytest -q",
        "status": "passed",
        "passed_count": 1,
        "output_digest": "3" * 64,
      },
      gaps=(
        {
          "gap_id": "GAP-PORTABLE-001",
          "requirement_id": "REQ-PORTABLE-001",
          "category": "missing_boundary",
          "component": "portable_store",
          "atomic_obligation_ids": (
            "REQ-PORTABLE-001#statement",
          ),
          "depends_on_gap_ids": (),
          "acceptance_test_ids": ("AT-PORTABLE-001",),
          "stop_condition": "boundary remains absent",
        },
      ),
      requirement_dependencies=(
        {
          "provider_requirement_id": "REQ-PORTABLE-001",
          "consumer_requirement_id": "REQ-CONTEXT-001",
        },
      ),
      bootstrap_commit="a" * 40,
    )


def test_validates_approved_obligations_components_and_dependencies():
  conformance = importlib.import_module(
    "tools.design.bootstrap_conformance"
  )
  record = _record(
    classification="adapt",
    gaps=("GAP-CONTEXT-001",),
  )

  result = (
    conformance
    .validate_evidence_backed_bootstrap_conformance(
      records=(record,),
      requirement_design_map={
        "REQ-CONTEXT-001": "DES-CONTEXT",
      },
      evidence_manifest=(
        {
          "path": "tools/context.py",
          "blob_sha256": "1" * 64,
          "role": "implementation",
          "requirement_ids": ("REQ-CONTEXT-001",),
        },
        {
          "path": "tests/test_context.py",
          "blob_sha256": "2" * 64,
          "role": "test",
          "requirement_ids": ("REQ-CONTEXT-001",),
        },
      ),
      commit_blob_map={
        "tools/context.py": "1" * 64,
        "tests/test_context.py": "2" * 64,
      },
      test_run={
        "bootstrap_commit": "a" * 40,
        "command": "python3 -m pytest -q",
        "status": "passed",
        "passed_count": 1,
        "output_digest": hashlib.sha256(
          b"1 passed\n"
        ).hexdigest(),
      },
      gaps=(
        {
          "gap_id": "GAP-CONTEXT-001",
          "requirement_id": "REQ-CONTEXT-001",
          "category": "missing_gate",
          "component": "context_builder",
          "atomic_obligation_ids": (
            "REQ-CONTEXT-001#statement",
          ),
          "depends_on_gap_ids": (),
          "acceptance_test_ids": ("AT-CONTEXT-001",),
          "stop_condition": "gate remains absent",
        },
      ),
      requirement_dependencies=(),
      bootstrap_commit="a" * 40,
      approved_obligation_map={
        "REQ-CONTEXT-001#statement": (
          "REQ-CONTEXT-001"
        ),
      },
      design_component_map={
        "DES-CONTEXT": ("context_builder",),
      },
      requirement_acceptance_test_map={
        "REQ-CONTEXT-001": "AT-CONTEXT-001",
      },
      approved_requirement_dependencies=(),
      normalized_test_output="1 passed\n",
      expected_passed_count=1,
    )
  )

  assert result.status == "complete"


def test_rejects_blob_claim_not_backed_by_commit(
  tmp_path,
):
  conformance = importlib.import_module(
    "tools.design.bootstrap_conformance"
  )
  repository = tmp_path / "repository"
  repository.mkdir()
  subprocess.run(
    ("git", "init", "-q"),
    cwd=repository,
    check=True,
  )
  subprocess.run(
    ("git", "config", "user.email", "test@example.com"),
    cwd=repository,
    check=True,
  )
  subprocess.run(
    ("git", "config", "user.name", "Test"),
    cwd=repository,
    check=True,
  )
  (repository / "tools").mkdir()
  (repository / "tools/context.py").write_text(
    "fixed\n",
    encoding="utf-8",
  )
  subprocess.run(
    ("git", "add", "tools/context.py"),
    cwd=repository,
    check=True,
  )
  subprocess.run(
    ("git", "commit", "-q", "-m", "fixed"),
    cwd=repository,
    check=True,
  )
  commit = subprocess.run(
    ("git", "rev-parse", "HEAD"),
    cwd=repository,
    check=True,
    capture_output=True,
    text=True,
  ).stdout.strip()

  with pytest.raises(
    conformance.BootstrapConformanceError
  ):
    conformance.validate_commit_blob_claims(
      repository_root=repository,
      bootstrap_commit=commit,
      commit_blob_map={
        "tools/context.py": "0" * 64,
      },
    )


def test_strict_integrity_validator_requires_inputs():
  conformance = importlib.import_module(
    "tools.design.bootstrap_conformance"
  )

  with pytest.raises(TypeError):
    (
      conformance
      .validate_strict_evidence_backed_bootstrap_conformance()
    )


def test_integrity_input_digest_changes_with_content():
  conformance = importlib.import_module(
    "tools.design.bootstrap_conformance"
  )

  first = conformance.digest_integrity_input(
    {"REQ-CONTEXT-001#statement": "REQ-CONTEXT-001"}
  )
  second = conformance.digest_integrity_input({
    "REQ-CONTEXT-001#statement": "REQ-CONTEXT-001",
    "REQ-CONTEXT-001#inputs.001": "REQ-CONTEXT-001",
  })

  assert len(first) == 64
  assert first != second
