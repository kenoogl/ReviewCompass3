"""契約011 依頼組み立て器（2類型・雛形生成＋機械検査）の境界テスト。

契約：records/task-contract/2026-08-17-request-builder-candidate-v3.md
外部送信・外部起動は行わない（完全local）。
"""

import hashlib
import importlib
import io
import json
import subprocess as host_subprocess
from pathlib import Path

import pytest


TEST_DATE = "2026-08-17"
TEST_SLUG = "sample-target-review"
TEST_TITLE = "試験対象v1"


def _core():
    return importlib.import_module("tools.request_builder.core")


def _entry():
    return importlib.import_module("tools.request_builder.entry")


def _operations():
    return importlib.import_module(
        "tools.operations.operation_contract_run"
    )


def _sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _git(repository, *arguments):
    return host_subprocess.run(
        ("git", "-C", str(repository), *arguments),
        capture_output=True,
        text=True,
        check=True,
    )


@pytest.fixture()
def repository(tmp_path):
    repo = tmp_path / "repo"
    (repo / "records" / "session-handoffs").mkdir(parents=True)
    (repo / "records" / "development").mkdir(parents=True)
    host_subprocess.run(
        ("git", "init", "-q", str(repo)),
        capture_output=True,
        text=True,
        check=True,
    )
    _git(repo, "config", "user.name", "Test")
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "config", "commit.gpgsign", "false")
    target = repo / "records" / "development" / "target-a.md"
    target.write_text("# 対象A\n\n内容A\n", encoding="utf-8")
    second = repo / "records" / "development" / "target-b.md"
    second.write_text("# 対象B\n\n内容B\n", encoding="utf-8")
    _git(repo, "add", "records")
    _git(repo, "commit", "-q", "-m", "Add targets")
    return repo


def _targets(repository):
    return [
        "records/development/target-a.md",
        "records/development/target-b.md",
    ]


def _assemble(repository, **overrides):
    core = _core()
    values = {
        "repository": repository,
        "request_type": "contract_review",
        "record_date": TEST_DATE,
        "slug": TEST_SLUG,
        "title": TEST_TITLE,
        "target_paths": _targets(repository),
    }
    values.update(overrides)
    return core.assemble(**values)


def _fill_placeholders(repository, record_relative_path):
    path = Path(repository) / record_relative_path
    text = path.read_text(encoding="utf-8")
    filled = []
    for line in text.splitlines():
        if line.startswith("<<記入:反証点"):
            filled.append("1. 検査Aの一意性を反証する。")
            filled.append("2. 検査Bの網羅性を反証する。")
        elif line.startswith("<<記入:判断済み"):
            filled.append("- 判断済み：試験用の判断済み事項。範囲外：試験用の範囲外。")
        else:
            filled.append(line)
    path.write_text("\n".join(filled) + "\n", encoding="utf-8")
    return path


def _commit_record(repository, record_relative_path):
    _git(repository, "add", "--", record_relative_path)
    _git(repository, "commit", "-q", "-m", "Add request record")


def _ready_record(repository, **overrides):
    result = _assemble(repository, **overrides)
    relative = result["record_relative_path"]
    _fill_placeholders(repository, relative)
    _commit_record(repository, relative)
    return relative


# ---- assemble（§5.1-1・§5.1-2） ----


def test_assemble_generates_contract_review_draft(repository):
    result = _assemble(repository)
    relative = result["record_relative_path"]
    assert relative.startswith("records/session-handoffs/")
    assert "-request-" in relative
    body = (Path(repository) / relative).read_text(encoding="utf-8")
    for section in (
        "対象と固定",
        "開始時の鮮度検査",
        "反証点",
        "判定の形式",
        "判断済み・範囲外",
        "手順",
    ):
        assert section in body
    assert "<<記入:反証点" in body
    assert "<<記入:判断済み" in body
    assert "読み取り専用" in body
    assert result["digest_rows"] == 2
    for target in _targets(repository):
        digest = _sha256_file(Path(repository) / target)
        assert "%s  %s" % (digest, target) in body


def test_assemble_embeds_allowed_model_and_verdict_name(repository):
    from tools.reviewer_launch.core import ALLOWED_RESPONSE_MODELS
    from tools.reviewer_launch.record import verdict_record_relative_path

    result = _assemble(repository)
    body = (Path(repository) / result["record_relative_path"]).read_text(
        encoding="utf-8"
    )
    assert ALLOWED_RESPONSE_MODELS[0] in body
    assert (
        verdict_record_relative_path(result["record_relative_path"]) in body
    )


def test_assemble_completion_review_has_base_commit(repository):
    result = _assemble(
        repository,
        request_type="completion_review",
        slug="sample-completion-review",
    )
    body = (Path(repository) / result["record_relative_path"]).read_text(
        encoding="utf-8"
    )
    assert "実装基準commit" in body
    head = _git(repository, "rev-parse", "HEAD").stdout.strip()
    assert head in body
    assert "完了レビュー" in body


def test_assemble_unknown_type_stops(repository):
    core = _core()
    with pytest.raises(core.BuilderStop) as caught:
        _assemble(repository, request_type="free_form")
    assert caught.value.reason == "request_type_unknown"


def test_assemble_empty_targets_stops(repository):
    core = _core()
    with pytest.raises(core.BuilderStop) as caught:
        _assemble(repository, target_paths=[])
    assert caught.value.reason == "digest_table_empty"


def test_assemble_unreadable_target_stops(repository):
    core = _core()
    with pytest.raises(core.BuilderStop) as caught:
        _assemble(
            repository,
            target_paths=["records/development/absent.md"],
        )
    assert caught.value.reason == "request_target_unreadable"


def test_assemble_existing_output_stops(repository):
    core = _core()
    _assemble(repository)
    with pytest.raises(core.BuilderStop) as caught:
        _assemble(repository)
    assert caught.value.reason == "output_already_exists"


def test_assemble_invalid_slug_stops(repository):
    core = _core()
    with pytest.raises(core.BuilderStop) as caught:
        _assemble(repository, slug="Invalid_Slug")
    assert caught.value.reason == "invalid_slug"


# ---- check：正常系と再実行性（§7.2・SR-C11-2） ----


def test_check_passes_on_committed_filled_record(repository):
    core = _core()
    relative = _ready_record(repository)
    result = core.check(
        repository=repository, request_relative_path=relative
    )
    assert result["status"] == "ok"
    assert result["request"]["path"] == relative
    assert result["request"]["sha256"] == _sha256_file(
        Path(repository) / relative
    )
    assert result["digest_rows"] == 2


def test_check_before_commit_fails_only_with_uncommitted(repository):
    core = _core()
    result = _assemble(repository)
    relative = result["record_relative_path"]
    _fill_placeholders(repository, relative)
    with pytest.raises(core.BuilderStop) as caught:
        core.check(repository=repository, request_relative_path=relative)
    assert caught.value.reason == "request_record_uncommitted"


# ---- check：7項目の停止理由（§5.1-3・§7.2） ----


def test_check_missing_section_stops(repository):
    core = _core()
    relative = _ready_record(repository)
    path = Path(repository) / relative
    text = path.read_text(encoding="utf-8")
    head, _, _ = text.partition("## 5.")
    path.write_text(head, encoding="utf-8")
    _git(repository, "add", "--", relative)
    _git(repository, "commit", "-q", "-m", "Break sections")
    with pytest.raises(core.BuilderStop) as caught:
        core.check(repository=repository, request_relative_path=relative)
    assert caught.value.reason == "required_section_missing"


def test_check_placeholder_remaining_stops(repository):
    core = _core()
    result = _assemble(repository)
    relative = result["record_relative_path"]
    _commit_record(repository, relative)
    with pytest.raises(core.BuilderStop) as caught:
        core.check(repository=repository, request_relative_path=relative)
    assert caught.value.reason == "placeholder_remaining"


def test_check_broken_placeholder_fragment_stops(repository):
    # cr-011-001所見（evasion-placeholder-modification）の敵対試験
    core = _core()
    relative = _ready_record(repository)
    path = Path(repository) / relative
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "1. 検査Aの一意性を反証する。",
        "<記入: 反証点をあとで書く",
        1,
    )
    path.write_text(text, encoding="utf-8")
    _git(repository, "add", "--", relative)
    _git(repository, "commit", "-q", "-m", "Break placeholder")
    with pytest.raises(core.BuilderStop) as caught:
        core.check(repository=repository, request_relative_path=relative)
    assert caught.value.reason == "placeholder_remaining"


def test_check_empty_fill_stops(repository):
    core = _core()
    result = _assemble(repository)
    relative = result["record_relative_path"]
    path = Path(repository) / relative
    text = path.read_text(encoding="utf-8")
    filled = []
    for line in text.splitlines():
        if line.startswith("<<記入:反証点"):
            continue
        if line.startswith("<<記入:判断済み"):
            filled.append("- 判断済み：あり。")
        else:
            filled.append(line)
    path.write_text("\n".join(filled) + "\n", encoding="utf-8")
    _commit_record(repository, relative)
    with pytest.raises(core.BuilderStop) as caught:
        core.check(repository=repository, request_relative_path=relative)
    assert caught.value.reason == "fill_in_missing"


def test_check_duplicate_point_identifiers_stop(repository):
    core = _core()
    relative = _ready_record(repository)
    path = Path(repository) / relative
    text = path.read_text(encoding="utf-8").replace(
        "2. 検査Bの網羅性を反証する。",
        "1. 検査Bの網羅性を反証する。",
        1,
    )
    path.write_text(text, encoding="utf-8")
    _git(repository, "add", "--", relative)
    _git(repository, "commit", "-q", "-m", "Duplicate identifiers")
    with pytest.raises(core.BuilderStop) as caught:
        core.check(repository=repository, request_relative_path=relative)
    assert caught.value.reason == "request_point_identifiers_invalid"


def test_check_digest_mismatch_stops(repository):
    core = _core()
    relative = _ready_record(repository)
    target = Path(repository) / "records/development/target-a.md"
    target.write_text("# 対象A\n\n改変後\n", encoding="utf-8")
    _git(repository, "add", "--", "records/development/target-a.md")
    _git(repository, "commit", "-q", "-m", "Change target")
    with pytest.raises(core.BuilderStop) as caught:
        core.check(repository=repository, request_relative_path=relative)
    assert caught.value.reason == "digest_mismatch"


def test_check_missing_reference_stops(repository):
    core = _core()
    relative = _ready_record(repository)
    _git(repository, "rm", "-q", "records/development/target-b.md")
    _git(repository, "commit", "-q", "-m", "Remove target")
    with pytest.raises(core.BuilderStop) as caught:
        core.check(repository=repository, request_relative_path=relative)
    assert caught.value.reason == "digest_reference_missing"


def test_check_empty_digest_table_stops(repository):
    # cr-011-001所見（evasion-empty-digest-table）の敵対試験
    core = _core()
    relative = _ready_record(repository)
    path = Path(repository) / relative
    text = path.read_text(encoding="utf-8")
    lines = []
    in_table = False
    for line in text.splitlines():
        if in_table and line.strip() == "```":
            in_table = False
            lines.append(line)
            continue
        if line.strip() == "```text" and not in_table:
            in_table = True
            lines.append(line)
            continue
        if in_table:
            continue
        lines.append(line)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    _git(repository, "add", "--", relative)
    _git(repository, "commit", "-q", "-m", "Empty table")
    with pytest.raises(core.BuilderStop) as caught:
        core.check(repository=repository, request_relative_path=relative)
    assert caught.value.reason == "digest_table_empty"


def test_check_disallowed_model_stops(repository):
    from tools.reviewer_launch.core import ALLOWED_RESPONSE_MODELS

    core = _core()
    relative = _ready_record(repository)
    path = Path(repository) / relative
    text = path.read_text(encoding="utf-8").replace(
        ALLOWED_RESPONSE_MODELS[0], "gemini-3.5-flash-low"
    )
    path.write_text(text, encoding="utf-8")
    _git(repository, "add", "--", relative)
    _git(repository, "commit", "-q", "-m", "Change model")
    with pytest.raises(core.BuilderStop) as caught:
        core.check(repository=repository, request_relative_path=relative)
    assert caught.value.reason == "model_not_allowed"


def test_check_fence_unbalanced_stops(repository):
    core = _core()
    relative = _ready_record(repository)
    path = Path(repository) / relative
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n```\n")
    _git(repository, "add", "--", relative)
    _git(repository, "commit", "-q", "-m", "Break fence")
    with pytest.raises(core.BuilderStop) as caught:
        core.check(repository=repository, request_relative_path=relative)
    assert caught.value.reason == "fence_unbalanced"


def test_check_name_without_request_marker_stops(repository):
    core = _core()
    relative = _ready_record(repository)
    renamed = "records/session-handoffs/2026-08-17-sample-note-v1.md"
    _git(repository, "mv", relative, renamed)
    _git(repository, "commit", "-q", "-m", "Rename record")
    with pytest.raises(core.BuilderStop) as caught:
        core.check(repository=repository, request_relative_path=renamed)
    assert caught.value.reason == "request_name_invalid"


# ---- 機微検査（§7.3・§9-5） ----


def test_check_detects_default_pattern_secret(repository):
    core = _core()
    relative = _ready_record(repository)
    path = Path(repository) / relative
    text = path.read_text(encoding="utf-8").replace(
        "- 判断済み：試験用の判断済み事項。範囲外：試験用の範囲外。",
        "- 判断済み：AKIAIOSFODNN7EXAMPLE を含む。",
        1,
    )
    path.write_text(text, encoding="utf-8")
    _git(repository, "add", "--", relative)
    _git(repository, "commit", "-q", "-m", "Insert secret")
    with pytest.raises(core.BuilderStop) as caught:
        core.check(repository=repository, request_relative_path=relative)
    assert caught.value.reason == "sensitive_data_remaining"


def test_check_detects_high_entropy_noise(repository):
    core = _core()
    relative = _ready_record(repository)
    path = Path(repository) / relative
    text = path.read_text(encoding="utf-8").replace(
        "- 判断済み：試験用の判断済み事項。範囲外：試験用の範囲外。",
        "- 判断済み：Zx9Qp2Lm8Rt4Vw7Yb3Nd6Fg1Hk5Js0AcXe を扱う。",
        1,
    )
    path.write_text(text, encoding="utf-8")
    _git(repository, "add", "--", relative)
    _git(repository, "commit", "-q", "-m", "Insert noise")
    with pytest.raises(core.BuilderStop) as caught:
        core.check(repository=repository, request_relative_path=relative)
    assert caught.value.reason == "sensitive_data_remaining"


def test_check_allows_hex_digests_and_readable_names(repository):
    core = _core()
    relative = _ready_record(repository)
    path = Path(repository) / relative
    text = path.read_text(encoding="utf-8").replace(
        "- 判断済み：試験用の判断済み事項。範囲外：試験用の範囲外。",
        "- 判断済み：対象commitは"
        "0123456789abcdef0123456789abcdef01234567、内容識別値は"
        "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef、"
        "対象はrequest-builder-known-readable-sample-nameである。",
        1,
    )
    path.write_text(text, encoding="utf-8")
    _git(repository, "add", "--", relative)
    _git(repository, "commit", "-q", "-m", "Add hex mentions")
    result = core.check(
        repository=repository, request_relative_path=relative
    )
    assert result["status"] == "ok"


def test_known_pass_through_dummy_key_is_documented(repository):
    # cr-011-001所見（evasion-secret-matching-exclusion）：除外と同形の
    # ダミー鍵（64桁小文字hex）は通過する。契約§7.4-4の許容の可視化。
    core = _core()
    relative = _ready_record(repository)
    path = Path(repository) / relative
    dummy_key = "deadbeefcafe0123456789abcdef0123456789abcdef0123456789abcdef0123"
    text = path.read_text(encoding="utf-8").replace(
        "- 判断済み：試験用の判断済み事項。範囲外：試験用の範囲外。",
        "- 判断済み：値 %s を含む。" % dummy_key,
        1,
    )
    path.write_text(text, encoding="utf-8")
    _git(repository, "add", "--", relative)
    _git(repository, "commit", "-q", "-m", "Add dummy key")
    result = core.check(
        repository=repository, request_relative_path=relative
    )
    assert result["status"] == "ok"


def test_exclusion_constants_equal_contract_009(repository):
    core = _core()
    from tools.external_review import send

    assert (
        tuple(core.HIGH_ENTROPY_ALLOW_PATTERNS)
        == tuple(send._HIGH_ENTROPY_ALLOW_PATTERNS)
    )


# ---- G30操作登録と入口（§5.1-5） ----


def test_g30_operation_registered():
    operations = _operations()
    definition = operations._OPERATIONS["request_builder_check"]
    assert definition["input_names"] == ("request",)
    assert definition["binding_positions"] == {
        "request": ("request", "sha256"),
    }
    assert callable(definition["entry"])


def test_g30_check_outputs_binding(repository):
    entry = _entry()
    relative = _ready_record(repository)
    buffer = io.BytesIO()
    exit_code = entry.g30_main(
        [
            "check",
            "--input-root",
            str(repository),
            "--request",
            relative,
        ],
        output=buffer,
    )
    assert exit_code == 0
    payload = buffer.getvalue()
    assert payload.endswith(b"\n")
    result = json.loads(payload.decode("utf-8"))
    assert result["status"] == "ok"
    assert result["request"]["sha256"] == _sha256_file(
        Path(repository) / relative
    )


def test_entry_assemble_and_check_roundtrip(repository):
    entry = _entry()
    buffer = io.BytesIO()
    exit_code = entry.main(
        [
            "assemble",
            "--repository",
            str(repository),
            "--type",
            "contract_review",
            "--date",
            TEST_DATE,
            "--slug",
            "entry-roundtrip-review",
            "--title",
            "入口試験",
            "--target",
            "records/development/target-a.md",
        ],
        output=buffer,
    )
    assert exit_code == 0
    result = json.loads(buffer.getvalue().decode("utf-8"))
    relative = result["record_relative_path"]
    _fill_placeholders(repository, relative)
    _commit_record(repository, relative)
    buffer = io.BytesIO()
    exit_code = entry.main(
        [
            "check",
            "--repository",
            str(repository),
            "--request",
            relative,
        ],
        output=buffer,
    )
    assert exit_code == 0
    checked = json.loads(buffer.getvalue().decode("utf-8"))
    assert checked["status"] == "ok"


def test_entry_missing_arguments_exits_2():
    entry = _entry()
    buffer = io.BytesIO()
    exit_code = entry.main(["assemble"], output=buffer)
    assert exit_code == 2
    result = json.loads(buffer.getvalue().decode("utf-8"))
    assert result["status"] == "stopped"
