import hashlib
import importlib
import json
from pathlib import Path
import stat
import types


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _module():
    return importlib.import_module(
        "tools.deployment.installed.trusted_review_send_dispatch"
    )


def test_capabilities_add_only_fixed_claude_bootstrap_role():
    module = _module()
    base = {
        "status": "capabilities",
        "schema_version": "trusted-review-send-v1",
        "roles": {
            "post_write_small": {
                "model": "gpt-5.6-terra",
                "purpose": "post_write_small_independent",
                "topology": "post_write_independent_single",
            }
        },
    }

    result = module.with_claude_capability(base)

    assert result["roles"]["post_write_small"] == base["roles"]["post_write_small"]
    assert result["roles"]["claude_session_bootstrap"] == {
        "model": "claude-fable-5",
        "purpose": "codex-pilot-no-tool-claude-bootstrap",
        "topology": "same_session_two_payload",
    }
    assert base["roles"].get("claude_session_bootstrap") is None


def test_dispatch_accepts_only_fixed_claude_inputs(monkeypatch, capsys):
    module = _module()
    calls = []
    fake_bootstrap = types.SimpleNamespace(
        run_approved_no_tool_bootstrap=lambda digest, approval_id: calls.append(
            (digest, approval_id)
        )
        or {
            "schema_version": 1,
            "result": "succeeded",
        }
    )
    monkeypatch.setattr(module, "_load_bootstrap", lambda root: fake_bootstrap)

    exit_code = module.main(
        [
            "claude-bootstrap",
            "--workspace-root",
            str(PROJECT_ROOT),
            "--manifest-digest",
            "a" * 64,
            "--approval-id",
            "RC3-CB-APPROVAL-TEST",
        ],
        base_main=lambda argv: 99,
        base_capabilities=lambda: {},
    )

    assert exit_code == 0
    assert calls == [("a" * 64, "RC3-CB-APPROVAL-TEST")]
    assert json.loads(capsys.readouterr().out)["result"] == "succeeded"

    calls.clear()
    exit_code = module.main(
        [
            "claude-bootstrap",
            "--workspace-root",
            str(PROJECT_ROOT),
            "--manifest-digest",
            "a" * 64,
            "--approval-id",
            "RC3-CB-APPROVAL-TEST",
            "--model",
            "other",
        ],
        base_main=lambda argv: 99,
        base_capabilities=lambda: {},
    )

    assert exit_code == 2
    assert calls == []


def test_workspace_source_digest_mismatch_stops_before_loading(tmp_path, monkeypatch):
    module = _module()
    workspace = tmp_path / "workspace"
    source = workspace / "tools/development/claude_bootstrap.py"
    source.parent.mkdir(parents=True)
    source.write_text("approved source\n", encoding="utf-8")
    manifest = workspace / ".reviewcompass/project-manifest.json"
    manifest.parent.mkdir(parents=True)
    manifest.write_text(
        json.dumps({"project_id": "reviewcompass3"}),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        module,
        "PINNED_WORKSPACE_FILES",
        {
            "tools/development/claude_bootstrap.py": hashlib.sha256(
                b"different source\n"
            ).hexdigest()
        },
    )

    try:
        module._validate_workspace(workspace)
    except ValueError as error:
        assert str(error) == "trusted workspace source mismatch"
    else:
        raise AssertionError("tampered workspace source must be rejected")


def test_non_claude_commands_remain_owned_by_existing_trusted_sender():
    module = _module()
    calls = []

    exit_code = module.main(
        ["--manifest", "existing.yaml", "--dry-run"],
        base_main=lambda argv: calls.append(tuple(argv)) or 7,
        base_capabilities=lambda: {},
    )

    assert exit_code == 7
    assert calls == [("--manifest", "existing.yaml", "--dry-run")]


def test_administrator_install_is_fixed_backed_up_and_post_verified(
    tmp_path, monkeypatch
):
    installer = importlib.import_module(
        "tools.deployment.trusted_claude_transport"
    )
    source_root = tmp_path / "source"
    install_root = tmp_path / "installed"
    source_dispatch = (
        source_root
        / "tools/deployment/installed/trusted_review_send_dispatch.py"
    )
    source_wrapper = (
        source_root / "tools/deployment/installed/trusted-review-send"
    )
    target_dispatch = (
        install_root
        / "tools/api_providers/trusted_review_send_dispatch.py"
    )
    target_base = (
        install_root / "tools/api_providers/trusted_review_send.py"
    )
    target_wrapper = install_root / "trusted-review-send"
    for path, content in (
        (source_dispatch, b"approved dispatch\n"),
        (source_wrapper, b"approved wrapper\n"),
        (target_base, b"existing trusted sender\n"),
        (target_wrapper, b"legacy wrapper\n"),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    monkeypatch.setattr(
        installer,
        "EXPECTED_BASE_SENDER_SHA256",
        hashlib.sha256(target_base.read_bytes()).hexdigest(),
    )
    monkeypatch.setattr(
        installer,
        "EXPECTED_LEGACY_WRAPPER_SHA256",
        hashlib.sha256(target_wrapper.read_bytes()).hexdigest(),
    )

    before = installer.deployment_status(
        install_root=install_root,
        source_root=source_root,
    )
    result = installer.install_trusted_transport(
        install_root=install_root,
        source_root=source_root,
        effective_user_id=0,
    )
    after = installer.deployment_status(
        install_root=install_root,
        source_root=source_root,
    )

    assert before["state"] == "claude_capability_missing"
    assert result["state"] == "ready"
    assert after["state"] == "ready"
    assert target_dispatch.read_bytes() == source_dispatch.read_bytes()
    assert target_wrapper.read_bytes() == source_wrapper.read_bytes()
    assert (
        install_root / "trusted-review-send.pre-claude-bootstrap-v1"
    ).read_bytes() == b"legacy wrapper\n"
    assert stat.S_IMODE(target_dispatch.stat().st_mode) == 0o644
    assert stat.S_IMODE(target_wrapper.stat().st_mode) == 0o755


def test_install_refuses_unreviewed_existing_entry(tmp_path, monkeypatch):
    installer = importlib.import_module(
        "tools.deployment.trusted_claude_transport"
    )
    source_root = tmp_path / "source"
    install_root = tmp_path / "installed"
    paths = {
        source_root
        / "tools/deployment/installed/trusted_review_send_dispatch.py": b"dispatch\n",
        source_root / "tools/deployment/installed/trusted-review-send": b"wrapper\n",
        install_root
        / "tools/api_providers/trusted_review_send.py": b"base\n",
        install_root / "trusted-review-send": b"unknown wrapper\n",
    }
    for path, content in paths.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    monkeypatch.setattr(
        installer,
        "EXPECTED_BASE_SENDER_SHA256",
        hashlib.sha256(b"base\n").hexdigest(),
    )
    monkeypatch.setattr(
        installer,
        "EXPECTED_LEGACY_WRAPPER_SHA256",
        hashlib.sha256(b"different wrapper\n").hexdigest(),
    )

    try:
        installer.install_trusted_transport(
            install_root=install_root,
            source_root=source_root,
            effective_user_id=0,
        )
    except ValueError as error:
        assert str(error) == "installed trusted entry mismatch"
    else:
        raise AssertionError("unknown installed entry must not be overwritten")

    assert (install_root / "trusted-review-send").read_bytes() == b"unknown wrapper\n"


def test_transport_status_and_install_have_one_public_command_entry():
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert (
        'reviewcompass3-trusted-transport = '
        '"tools.deployment.trusted_claude_transport:main"'
    ) in pyproject
