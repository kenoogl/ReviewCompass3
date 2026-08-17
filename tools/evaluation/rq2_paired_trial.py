"""RQ2（Context scalability）paired trial装置。

lifecycle: provisional
normative_status: non-normative
promotion_required: true

作業票：docs/development/2026-08-17-rq2-apparatus-work-ticket-v1.md
実験計画：records/development/2026-08-17-rq2-paired-trial-plan-v1.md（承認済み）
測定・プールの裁定：records/development/2026-08-17-rq2-measurement-and-pool-decision-v1.md

既存部品（task_contract・request_builder・reviewer_bridge・reviewer_launch）はすべて
読み取り専用で呼び、本moduleは製品本体へ手を入れない。外部起動はinjectable（launcher）で
あり、実起動系は`launch_guard`経由でのみ呼ぶ規約とする（試験はguardを禁止fakeへ差し替えて
「起動ゼロ」を機械確認できる）。
"""

import hashlib
import json
from pathlib import Path

from tools import task_contract as runtime
from tools.evaluation import reviewer_bridge
from tools.task_contract import contract as contract_module

CASE_ROOT = "docs/evaluation/rq2-cases"
POOL_ROOT = "docs/evaluation/rq2-pool"
# A1＝資料少（プール不在）、A2＝資料多（プール在）。どちらも「ディレクトリ全file」を
# 契約へ渡す基準条件だが、物理内容が違うため別条件として数える。
CONDITIONS = ("A1", "A2", "B", "C", "D")
ABSOLUTE_LAUNCH_LIMIT = 35
CONSECUTIVE_FAILURE_LIMIT = 3
UNABLE_RATIO_LIMIT = 0.30
JUDGMENTS = ("detected", "false_positive", "out_of_scope", "non_counting")

_REQUIREMENTS = tuple(sorted(contract_module.REQUIREMENT_OBLIGATIONS))


def _material(case_id, name):
    return "%s/%s/%s" % (CASE_ROOT, case_id, name)


CASES = (
    {
        "case_id": "case-001",
        "group": "real_defect",
        "materials": (
            _material("case-001", "contract-canonical-sequence.md"),
            _material("case-001", "observation-prefix-record-shapes.md"),
        ),
        "required_material": _material(
            "case-001", "observation-prefix-record-shapes.md"
        ),
        "conditions": ("A1", "A2", "B", "C", "D"),
    },
    {
        "case_id": "case-002",
        "group": "real_defect",
        "materials": (_material("case-002", "prescan-digest-record.md"),),
        "required_material": None,
        "conditions": ("B", "C"),
    },
    {
        "case_id": "case-003",
        "group": "real_defect",
        "materials": (
            _material("case-003", "contract-interpretation-scope.md"),
            _material("case-003", "procedure-result-reading.md"),
        ),
        "required_material": _material(
            "case-003", "contract-interpretation-scope.md"
        ),
        "conditions": ("B", "C"),
    },
    {
        "case_id": "case-004",
        "group": "seeded",
        "materials": (_material("case-004", "rq1-apparatus-work-ticket.md"),),
        "required_material": _material(
            "case-004", "rq1-apparatus-work-ticket.md"
        ),
        "conditions": ("A1", "A2", "B", "C"),
    },
    {
        "case_id": "case-005",
        "group": "seeded",
        "materials": (
            _material("case-005", "reviewer-launch-e2e-evidence.md"),
        ),
        "required_material": _material(
            "case-005", "reviewer-launch-e2e-evidence.md"
        ),
        "conditions": ("B", "C", "D"),
    },
    {
        "case_id": "case-006",
        "group": "seeded",
        "materials": (
            _material("case-006", "reviewer-bridge-work-ticket.md"),
        ),
        "required_material": None,
        "conditions": ("B", "C"),
    },
    {
        "case_id": "case-007",
        "group": "seeded",
        "materials": (
            _material("case-007", "contract-approval-boundary.md"),
        ),
        "required_material": None,
        "conditions": ("B", "C"),
    },
    {
        "case_id": "case-008",
        "group": "pass",
        "materials": (_material("case-008", "session-log-record-run.md"),),
        "required_material": _material(
            "case-008", "session-log-record-run.md"
        ),
        "conditions": ("A1", "A2", "B", "C", "D"),
    },
    {
        "case_id": "case-009",
        "group": "pass",
        "materials": (
            _material("case-009", "product-acceptance-decision.md"),
        ),
        "required_material": None,
        "conditions": ("B", "C"),
    },
    {
        "case_id": "case-010",
        "group": "pass",
        "materials": (
            _material("case-010", "launch-metrics-work-ticket.md"),
        ),
        "required_material": None,
        "conditions": ("B", "C"),
    },
)


def launch_guard(**arguments):
    """**実起動**が通る唯一の呼び出し口（試験は差し替えて禁止する）。

    injectableな`launcher`はここを通らない。実起動バッチが渡すlauncherだけが
    本関数を呼ぶため、試験でここを禁止fakeへ差し替えると「起動ゼロ」を機械で
    証明できる（reviewer_bridgeの`subprocess_guard`と同じ型）。
    """

    from tools.reviewer_launch import core as reviewer_launch

    return reviewer_launch.launch_review(**arguments)


def case_by_id(case_id):
    for case in CASES:
        if case["case_id"] == case_id:
            return case
    raise KeyError(case_id)


def directory_paths(*, project_root, case):
    """ケースディレクトリに物理的に存在するMarkdown fileを列挙する。"""

    directory = Path(project_root) / CASE_ROOT / case["case_id"]
    return tuple(
        sorted(
            "%s/%s/%s" % (CASE_ROOT, case["case_id"], path.name)
            for path in directory.glob("*.md")
        )
    )


def select_target_paths(*, project_root, case, condition):
    """条件ごとに契約へ渡す対象path集合を決める（事前走査§3の表）。"""

    if condition not in CONDITIONS:
        raise ValueError("unknown condition: %s" % condition)
    if condition.startswith("A"):
        return directory_paths(project_root=project_root, case=case)
    if condition in ("B", "C"):
        return tuple(case["materials"])
    required = case["required_material"]
    if required is None:
        raise ValueError("case has no required_material: %s" % case["case_id"])
    return tuple(path for path in case["materials"] if path != required)


def build_case_context(*, project_root, case, condition):
    """契約chainを読み取り専用で駆動し、(contract, context_manifest)を返す。"""

    target_paths = select_target_paths(
        project_root=project_root, case=case, condition=condition
    )
    binding = runtime.bind_requirements(
        project_root=project_root, requirement_ids=_REQUIREMENTS
    )
    snapshot = runtime.read_source_snapshot(
        project_root=project_root,
        target_paths=target_paths,
        base_commit="BASE",
        head_commit="HEAD",
    )
    contract = runtime.build_review_task_contract(
        contract_id="TC-RQ2-%s-%s" % (case["case_id"].upper(), condition),
        contract_version=1,
        requirement_binding=binding,
        target_paths=target_paths,
    )
    compile_verdict = runtime.compile_contract(
        contract=contract, requirement_binding=binding
    )
    context = runtime.build_context_manifest(
        contract=contract,
        plan_bundle=compile_verdict["plan_bundle"],
        source_snapshot=snapshot,
    )
    return contract, context


def selection_signature(context_manifest):
    """材料選択の件数と内訳（条件間で比較する量）。"""

    paths = sorted(
        item["relative_path"] for item in context_manifest["material_bundle"]
    )
    return {"count": len(paths), "paths": paths}


def build_case_request(*, project_root, case, condition, record_date):
    """依頼recordを機械組み立てし、repo相対pathを返す（commitは呼び出し側）。"""

    contract, context = build_case_context(
        project_root=project_root, case=case, condition=condition
    )
    request_body, decided_scope = reviewer_bridge.compose_request_body(
        contract, context
    )
    return reviewer_bridge.build_free_text_request(
        repository=project_root,
        record_date=record_date,
        slug="rq2-%s-%s" % (case["case_id"], condition.lower()),
        title="実験ケース%s（条件%s）の妥当性レビュー"
        % (case["case_id"], condition),
        target_paths=[
            item["relative_path"] for item in context["material_bundle"]
        ],
        request_body=request_body,
        decided_scope=decided_scope,
    )


def extract_usage(raw_text):
    """未加工応答から使用量を取り出す。

    `result`イベントのusageが**累計**であり正である（実測：cr-014-001で
    段別usageの合計と一致）。段別の足し上げは二重計上になるため使わない。
    resultイベントが無い応答ではNone（不能を偽値で埋めない）。
    """

    for line in str(raw_text).splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict) or event.get("event") != "result":
            continue
        usage = (event.get("result") or {}).get("usage")
        if isinstance(usage, dict) and "input_tokens" in usage:
            return {
                "input_tokens": usage["input_tokens"],
                "output_tokens": usage.get("output_tokens", 0),
            }
    return None


def extract_read_paths(raw_text, *, repository_root):
    """reviewerが読取り道具で開いたfileをrepo相対pathで列挙する（出現順）。

    実測：`step_update`の`tool_info.parameters.AbsolutePath`に絶対pathが残る。
    repository外のpathは対象外（起動promptが領域外アクセスを禁じているため
    通常は現れないが、現れた場合も相対化できないので数えない）。
    """

    prefix = str(repository_root).rstrip("/") + "/"
    found = []
    for line in str(raw_text).splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict) or event.get("event") != "step_update":
            continue
        parameters = (
            ((event.get("step_update") or {}).get("tool_info") or {})
            .get("parameters")
            or {}
        )
        value = parameters.get("AbsolutePath")
        if not isinstance(value, str) or not value.startswith(prefix):
            continue
        relative = value[len(prefix):]
        if relative not in found:
            found.append(relative)
    return tuple(found)


def check_read_scope(read_paths, *, allowed, request_relative_path):
    """依頼recordと指定材料の外を読んでいないかを機械判定する。

    範囲外を読んだ実行は**汚染**として集計から外す判断材料になる（repository内には
    設計・裁定recordが残っており、そこに答の一部が書かれているため）。
    """

    permitted = set(allowed) | {request_relative_path}
    outside = tuple(path for path in read_paths if path not in permitted)
    return {
        "clean": not outside,
        "read_count": len(read_paths),
        "outside": outside,
    }


def run_case(
    *,
    project_root,
    case,
    condition,
    record_date,
    launcher,
    commit,
    verify=None,
):
    """1ケース1条件を実行する。

    `commit`は依頼recordを固定する呼び出し側の手続き（起動前に作業treeを清浄に
    するため必須）。`verify`を与えた場合は依頼recordの事前検査を実行する
    （実起動では`request_builder.check`を渡す。試験では省略する）。
    """

    contract, context = build_case_context(
        project_root=project_root, case=case, condition=condition
    )
    request_relative_path = build_case_request(
        project_root=project_root,
        case=case,
        condition=condition,
        record_date=record_date,
    )
    commit("Add RQ2 request record for %s %s" % (case["case_id"], condition))
    if verify is not None:
        verdict = verify(
            repository=project_root,
            request_relative_path=request_relative_path,
        )
        if verdict.get("status") != "ok":
            return {
                "case_id": case["case_id"],
                "condition": condition,
                "group": case["group"],
                "status": "verification_failed",
                "request_relative_path": request_relative_path,
                "selection": selection_signature(context),
                "usage": None,
                "findings": [],
                "detail": verdict,
            }
    payload = (Path(project_root) / request_relative_path).read_bytes()
    expected_sha256 = hashlib.sha256(payload).hexdigest()
    outcome = launcher(
        request_relative_path=request_relative_path,
        expected_sha256=expected_sha256,
    )
    verdict = outcome.get("verdict") or {}
    finding_set = reviewer_bridge.convert_findings(
        verdict.get("findings", ()), context_manifest=context
    )
    raw_text = outcome.get("raw_text", "")
    read_paths = extract_read_paths(
        raw_text, repository_root=Path(project_root).resolve()
    )
    return {
        "case_id": case["case_id"],
        "condition": condition,
        "group": case["group"],
        "status": "succeeded",
        "request_relative_path": request_relative_path,
        "expected_sha256": expected_sha256,
        "selection": selection_signature(context),
        "usage": extract_usage(raw_text),
        "verdict": verdict.get("verdict"),
        "findings": finding_set["findings"],
        "run_id": outcome.get("run_id"),
        "read_scope": check_read_scope(
            read_paths,
            allowed=[
                item["relative_path"]
                for item in context["material_bundle"]
            ],
            request_relative_path=request_relative_path,
        ),
    }


def build_scoring_sheet(results):
    """採点対象のFindingを機械で一覧化する（判定はHuman／LLMの意味解析）。"""

    rows = []
    for result in results:
        for finding in result.get("findings", ()):
            target = finding.get("target_ref") or {}
            rows.append(
                {
                    "case_id": result["case_id"],
                    "condition": result["condition"],
                    "finding_id": finding["finding_id"],
                    "severity": finding["severity"],
                    "description": finding["description"],
                    "target_relative_path": target.get("relative_path", ""),
                }
            )
    return rows


def apply_judgments(scoring_sheet, judgments):
    """裁定（検出・誤検出・責務外・非加算）を集計する。未裁定は停止させる。"""

    scoring = {}
    for row in scoring_sheet:
        key = (row["case_id"], row["condition"])
        scoring.setdefault(
            key, {"detected": False, "false_positive": 0, "out_of_scope": 0}
        )
        judgment = judgments.get(
            (row["case_id"], row["condition"], row["finding_id"])
        )
        if judgment not in JUDGMENTS:
            raise ValueError(
                "unjudged finding: %s/%s/%s"
                % (row["case_id"], row["condition"], row["finding_id"])
            )
        if judgment == "detected":
            scoring[key]["detected"] = True
        elif judgment == "false_positive":
            scoring[key]["false_positive"] += 1
        elif judgment == "out_of_scope":
            scoring[key]["out_of_scope"] += 1
    return scoring


def _mean(values):
    return round(sum(values) / len(values), 4) if values else None


def aggregate(trials):
    """RQ2指標を機械集計する。分母0は偽値で埋めずNoneで申告する。"""

    by_condition = {}
    for condition in CONDITIONS:
        subset = [
            trial
            for trial in trials
            if trial["condition"] == condition
            and trial["status"] == "succeeded"
        ]
        if not subset:
            continue
        defects = [trial for trial in subset if trial["group"] != "pass"]
        detected = [
            trial for trial in defects if trial["scoring"]["detected"]
        ]
        inputs = [
            trial["usage"]["input_tokens"]
            for trial in subset
            if trial.get("usage")
        ]
        by_condition[condition] = {
            "trials": len(subset),
            "defect_cases": len(defects),
            "detection_rate": (
                round(len(detected) / len(defects), 4) if defects else None
            ),
            "false_positive_total": sum(
                trial["scoring"]["false_positive"] for trial in subset
            ),
            "out_of_scope_total": sum(
                trial["scoring"]["out_of_scope"] for trial in subset
            ),
            "input_tokens_mean": _mean(inputs),
            "selection_count_mean": _mean(
                [trial["selection"]["count"] for trial in subset]
            ),
        }

    selections = {}
    for trial in trials:
        if trial["condition"] in ("B", "C") and trial["status"] == "succeeded":
            selections.setdefault(trial["case_id"], {})[
                trial["condition"]
            ] = trial["selection"]["count"]
    differing = sorted(
        case_id
        for case_id, values in selections.items()
        if "B" in values and "C" in values and values["B"] != values["C"]
    )
    compared = sorted(
        case_id
        for case_id, values in selections.items()
        if "B" in values and "C" in values
    )
    return {
        "by_condition": by_condition,
        "selection_invariance": {
            "holds": not differing,
            "cases_compared": compared,
            "cases_differing": differing,
        },
    }


def evaluate_stop_conditions(
    trials,
    *,
    launched_count,
    absolute_limit=ABSOLUTE_LAUNCH_LIMIT,
    consecutive_failure_limit=CONSECUTIVE_FAILURE_LIMIT,
    unable_ratio_limit=UNABLE_RATIO_LIMIT,
):
    """計画§5-4の中断条件4種を機械判定する。"""

    reasons = []
    tail = 0
    for trial in reversed(trials):
        if trial.get("status") == "failed":
            tail += 1
        else:
            break
    if tail >= consecutive_failure_limit:
        reasons.append("consecutive_failures")
    if launched_count >= absolute_limit:
        reasons.append("absolute_limit_reached")
    if trials:
        unable = sum(
            1 for trial in trials if trial.get("status") == "unable"
        )
        if unable / len(trials) > unable_ratio_limit:
            reasons.append("unable_ratio_exceeded")
    if any(
        trial.get("status") == "verification_failed" for trial in trials
    ):
        reasons.append("post_verification_failed")
    return {"stop": bool(reasons), "reasons": reasons}
