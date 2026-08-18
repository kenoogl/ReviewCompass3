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


def test_check_fake_heading_inside_fence_does_not_count(repository):
    # e2e-011-001所見2（blocking）の敵対試験：実§6を削除し、fence内へ
    # 偽の「## 6. 手順」を置いた場合、見出しとして数えず
    # required_section_missingで停止しなければならない。
    core = _core()
    relative = _ready_record(repository)
    path = Path(repository) / relative
    text = path.read_text(encoding="utf-8")
    head, _, _ = text.partition("## 6.")
    forged = head + (
        "```text\n"
        "## 6. 手順（Human・Claude向け）\n"
        "```\n"
    )
    path.write_text(forged, encoding="utf-8")
    _git(repository, "add", "--", relative)
    _git(repository, "commit", "-q", "-m", "Forge heading in fence")
    with pytest.raises(core.BuilderStop) as caught:
        core.check(repository=repository, request_relative_path=relative)
    assert caught.value.reason == "required_section_missing"


def test_check_digest_row_outside_fence_stops(repository):
    # e2e-011-001所見2（blocking）の敵対試験：§1のfence外に置かれた
    # digest行（正しい値でも）は表として数えず、明示的に停止する。
    core = _core()
    relative = _ready_record(repository)
    path = Path(repository) / relative
    stray = "%s  records/development/target-a.md" % _sha256_file(
        Path(repository) / "records/development/target-a.md"
    )
    text = path.read_text(encoding="utf-8").replace(
        "## 2. 開始時の鮮度検査",
        stray + "\n\n## 2. 開始時の鮮度検査",
        1,
    )
    path.write_text(text, encoding="utf-8")
    _git(repository, "add", "--", relative)
    _git(repository, "commit", "-q", "-m", "Add stray digest row")
    with pytest.raises(core.BuilderStop) as caught:
        core.check(repository=repository, request_relative_path=relative)
    assert caught.value.reason == "digest_row_outside_fence"


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


# ---- 自由文類型（契約013） ----


FREE_TEXT_SLUG = "free-text-sample"
# 契約013 §9-3：既存2類型の生成結果の固定値（root・HEADを置換した正規化本文の
# SHA-256。2026-08-17の実装前実測を機械転記。値の変更は契約改定）。
GOLDEN_CONTRACT_REVIEW_SHA256 = (
    "876478a7c3d2b479af499ae66a9417398388739c1ee4cd5a7b1990a43b20d382"
)
GOLDEN_COMPLETION_REVIEW_SHA256 = (
    "4bd116c6b2f05ad068ac16651689ef408875620f1735a40f1cf52f4a562d67ff"
)


def _fill_free_text(repository, record_relative_path, content_lines=None):
    path = Path(repository) / record_relative_path
    text = path.read_text(encoding="utf-8")
    lines = (
        ["この2つの対象recordの整合を検査してほしい。"]
        if content_lines is None
        else list(content_lines)
    )
    filled = []
    for line in text.splitlines():
        if line.startswith("<<記入:依頼内容"):
            filled.extend(lines)
        elif line.startswith("<<記入:判断済み"):
            filled.append(
                "- 判断済み：試験用の判断済み事項。範囲外：試験用の範囲外。"
            )
        else:
            filled.append(line)
    path.write_text("\n".join(filled) + "\n", encoding="utf-8")
    return path


def test_assemble_free_text_generates_content_section(repository):
    result = _assemble(
        repository, request_type="free_text", slug=FREE_TEXT_SLUG
    )
    body = (Path(repository) / result["record_relative_path"]).read_text(
        encoding="utf-8"
    )
    assert "自由文レビュー" in body
    assert "<<記入:依頼内容" in body
    assert "反証点" not in body
    assert "実装基準commit" not in body


def test_check_free_text_record_passes_without_point_numbers(repository):
    result = _assemble(
        repository, request_type="free_text", slug=FREE_TEXT_SLUG
    )
    relative = result["record_relative_path"]
    _fill_free_text(repository, relative)
    _commit_record(repository, relative)
    outcome = _core().check(
        repository=repository, request_relative_path=relative
    )
    assert outcome["status"] == "ok"
    assert outcome["request_type"] == "free_text"


def test_check_free_text_empty_content_stops(repository):
    core = _core()
    result = _assemble(
        repository, request_type="free_text", slug=FREE_TEXT_SLUG
    )
    relative = result["record_relative_path"]
    _fill_free_text(repository, relative, content_lines=[])
    _commit_record(repository, relative)
    with pytest.raises(core.BuilderStop) as caught:
        core.check(repository=repository, request_relative_path=relative)
    assert caught.value.reason == "fill_in_missing"


def test_check_free_text_missing_content_section_stops(repository):
    core = _core()
    result = _assemble(
        repository, request_type="free_text", slug=FREE_TEXT_SLUG
    )
    relative = result["record_relative_path"]
    path = _fill_free_text(repository, relative)
    text = path.read_text(encoding="utf-8")
    path.write_text(
        text.replace("への依頼：依頼内容", "への依頼：依頼概要"),
        encoding="utf-8",
    )
    _commit_record(repository, relative)
    with pytest.raises(core.BuilderStop) as caught:
        core.check(repository=repository, request_relative_path=relative)
    assert caught.value.reason == "required_section_missing"


def test_check_type_inferred_from_canonical_line_only(repository):
    result = _assemble(repository)
    relative = result["record_relative_path"]
    path = Path(repository) / relative
    text = path.read_text(encoding="utf-8")
    filled = []
    for line in text.splitlines():
        if line.startswith("<<記入:反証点"):
            filled.append("1. 検査Aの一意性を反証する。")
        elif line.startswith("<<記入:判断済み"):
            filled.append(
                "- 判断済み：実装完了レビューは実施済みとして扱う。範囲外：試験用。"
            )
        else:
            filled.append(line)
    path.write_text("\n".join(filled) + "\n", encoding="utf-8")
    _commit_record(repository, relative)
    outcome = _core().check(
        repository=repository, request_relative_path=relative
    )
    assert outcome["request_type"] == "contract_review"


def test_check_free_text_digest_row_in_content_stops(repository):
    core = _core()
    result = _assemble(
        repository, request_type="free_text", slug=FREE_TEXT_SLUG
    )
    relative = result["record_relative_path"]
    _fill_free_text(
        repository,
        relative,
        content_lines=[
            "対象の照合値を本文へ書く。",
            "0" * 64 + "  records/development/target-a.md",
        ],
    )
    _commit_record(repository, relative)
    with pytest.raises(core.BuilderStop) as caught:
        core.check(repository=repository, request_relative_path=relative)
    assert caught.value.reason == "digest_row_outside_fence"


def test_check_free_text_fake_heading_inside_fence_ignored(repository):
    result = _assemble(
        repository, request_type="free_text", slug=FREE_TEXT_SLUG
    )
    relative = result["record_relative_path"]
    _fill_free_text(
        repository,
        relative,
        content_lines=[
            "次のfence内は引用であり構造ではない。",
            "```text",
            "## 5. 判断済み・範囲外（蒸し返し不要）",
            "```",
            "引用の後も依頼本文が続く。",
        ],
    )
    _commit_record(repository, relative)
    outcome = _core().check(
        repository=repository, request_relative_path=relative
    )
    assert outcome["status"] == "ok"


def _normalized_assemble_digest(repository, request_type, slug):
    result = _assemble(repository, request_type=request_type, slug=slug)
    body = (Path(repository) / result["record_relative_path"]).read_text(
        encoding="utf-8"
    )
    root_text = str(Path(repository).resolve())
    head = _git(repository, "rev-parse", "HEAD").stdout.strip()
    normalized = body.replace(root_text, "<ROOT>").replace(head, "<HEAD>")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def test_assemble_existing_types_output_bytes_unchanged(repository):
    assert (
        _normalized_assemble_digest(
            repository, "contract_review", "golden-contract"
        )
        == GOLDEN_CONTRACT_REVIEW_SHA256
    )
    assert (
        _normalized_assemble_digest(
            repository, "completion_review", "golden-completion"
        )
        == GOLDEN_COMPLETION_REVIEW_SHA256
    )


def test_entry_assemble_defaults_date_and_repository(repository, monkeypatch):
    entry = _entry()
    monkeypatch.chdir(repository)
    buffer = io.BytesIO()
    exit_code = entry.main(
        [
            "assemble",
            "--type",
            "contract_review",
            "--slug",
            "defaults-probe-review",
            "--title",
            "既定値試験",
            "--target",
            "records/development/target-a.md",
        ],
        output=buffer,
    )
    assert exit_code == 0
    result = json.loads(buffer.getvalue().decode("utf-8"))
    from datetime import datetime

    today = datetime.now().astimezone().date().isoformat()
    assert today in result["record_relative_path"]


def test_entry_check_defaults_repository(repository, monkeypatch):
    entry = _entry()
    relative = _ready_record(repository)
    monkeypatch.chdir(repository)
    buffer = io.BytesIO()
    exit_code = entry.main(
        ["check", "--request", relative],
        output=buffer,
    )
    assert exit_code == 0
    result = json.loads(buffer.getvalue().decode("utf-8"))
    assert result["status"] == "ok"
