from __future__ import annotations

from typing import Any, Dict

from pyrit_demo_harness.adapters.scenario_loader import load_scenario
from pyrit_demo_harness.adapters.scenario_router import get_runner_and_scorer
from pyrit_demo_harness.pyrit_integration.targets import build_target_for_scenario, HRSimulatorTarget
from pyrit_demo_harness.utils.ids import new_execution_id, current_timestamp
from pyrit_demo_harness.utils.io_helpers import write_evidence_record
from pyrit_demo_harness.evidence import build_evidence_record


def run_with_pyrit(scenario_id: str, mode: str = "simulator") -> Dict[str, Any]:
    """High-level harness entrypoint.

    Orchestrates: load scenario → build target → run → score → evidence.
    Default ``mode`` uses the external FastAPI HR simulator; a "dummy" mode is
    available only for unit tests.
    """

    scenario = load_scenario(scenario_id)
    runner, scorer = get_runner_and_scorer(scenario_id)
    target = build_target_for_scenario(scenario_id, mode=mode)

    results = runner(scenario, target)
    score = scorer(results, scenario)

    # Generate execution metadata
    execution_id = new_execution_id()
    timestamp = current_timestamp()

    # Extract system_id and stack_id
    system_id = target.system_id if isinstance(target, HRSimulatorTarget) else "hr_sim_001"
    stack_id = "stack_001"  # Default stack, can be made configurable later

    # Build schema-compliant evidence record
    record = build_evidence_record(
        scenario_id=scenario.scenario_id,
        execution_id=execution_id,
        timestamp=timestamp,
        system_id=system_id,
        stack_id=stack_id,
        computed_metrics=score["metrics"],
        violation_flags=score["violation_flags"],
        pass_fail=score["pass_fail"],
        raw_results=results,
    )

    write_evidence_record(scenario.scenario_id, record)
    return record
