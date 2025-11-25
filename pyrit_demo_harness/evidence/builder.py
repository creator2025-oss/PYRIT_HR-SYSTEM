"""
Evidence builder for EU AI Act Annex III-4 compliance.

Builds schema-compliant evidence records from PYRIT harness execution results.
"""

import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from .config_loaders import (
    get_scenario_metadata,
    get_test_case_metadata,
    get_system_metadata,
    get_config_stack,
    get_evaluation_rules_for_scenario,
    get_mitigation_template,
)


SCHEMA_VERSION = "annexIII4_evidence_v1.0"


def build_evidence_record(
    scenario_id: str,
    execution_id: str,
    timestamp: str,
    system_id: str,
    stack_id: str,
    computed_metrics: Dict[str, Any],
    violation_flags: Dict[str, bool],
    pass_fail: str,
    raw_results: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Build a schema-compliant evidence record.

    Args:
        scenario_id: Scenario identifier (e.g., "HR-02-SCEN-015")
        execution_id: Unique execution identifier
        timestamp: ISO 8601 timestamp
        system_id: System under test identifier
        stack_id: Configuration stack identifier
        computed_metrics: Dict of metric names to values
        violation_flags: Dict of violation flags to boolean values
        pass_fail: "PASS" or "FAIL"
        raw_results: Optional raw results from simulator

    Returns:
        Complete evidence record conforming to annexIII4_evidence_v1.0 schema
    """
    # Load metadata
    scenario_meta = get_scenario_metadata(scenario_id)
    if not scenario_meta:
        raise ValueError(f"Scenario {scenario_id} not found in config")

    test_case_id = scenario_meta.get("test_case_id")
    test_case_meta = get_test_case_metadata(test_case_id)
    if not test_case_meta:
        raise ValueError(f"Test case {test_case_id} not found in config")

    system_meta = get_system_metadata(system_id)
    if not system_meta:
        raise ValueError(f"System {system_id} not found in config")

    stack_meta = get_config_stack(stack_id)
    if not stack_meta:
        raise ValueError(f"Stack {stack_id} not found in config")

    eval_rules = get_evaluation_rules_for_scenario(scenario_id)
    if not eval_rules:
        raise ValueError(f"Evaluation rules for {scenario_id} not found in config")

    # Build record
    record = {
        "schema_version": SCHEMA_VERSION,
        "scenario": build_scenario_section(scenario_meta, scenario_id),
        "test_case": build_test_case_section(test_case_meta, test_case_id),
        "execution_context": build_execution_context_section(execution_id, timestamp),
        "system_under_test": build_system_under_test_section(system_meta, system_id),
        "configuration_stack": build_configuration_stack_section(stack_meta, stack_id),
        "test_steps_executed": build_test_steps_section(scenario_id, execution_id),
        "actual_results": build_actual_results_section(computed_metrics, raw_results),
        "evaluation": build_evaluation_section(
            eval_rules, computed_metrics, violation_flags, pass_fail
        ),
        "success_evidence": build_success_evidence_section(pass_fail, computed_metrics),
        "failure_evidence": build_failure_evidence_section(
            pass_fail, violation_flags, computed_metrics
        ),
        "mitigation": build_mitigation_section(violation_flags, pass_fail, timestamp),
        "provenance": build_provenance_section(execution_id, timestamp),
    }

    # Compute hash
    record_copy = record.copy()
    record_copy.pop("provenance", None)  # Exclude provenance from hash
    record_json = json.dumps(record_copy, sort_keys=True)
    record_hash = hashlib.sha256(record_json.encode()).hexdigest()
    record["provenance"]["record_hash"] = record_hash

    return record


def build_scenario_section(scenario_meta: Dict[str, Any], scenario_id: str) -> Dict[str, Any]:
    """Build scenario section."""
    return {
        "scenario_id": scenario_id,
        "title": scenario_meta.get("title", ""),
        "description": scenario_meta.get("description", ""),
        "objective": scenario_meta.get("objective", ""),
        "regulatory_scope": {
            "eu_ai_act_annex": scenario_meta.get("regulatory_scope", {}).get(
                "eu_ai_act_annex", "III-4"
            ),
            "risk_category": scenario_meta.get("regulatory_scope", {}).get(
                "risk_category", "high-risk"
            ),
            "applicable_articles": scenario_meta.get("regulatory_scope", {}).get(
                "applicable_articles", []
            ),
        },
        "scenario_type": scenario_meta.get("scenario_type", "bias_detection"),
        "tags": scenario_meta.get("tags", []),
    }


def build_test_case_section(test_case_meta: Dict[str, Any], test_case_id: str) -> Dict[str, Any]:
    """Build test_case section."""
    return {
        "test_case_id": test_case_id,
        "title": test_case_meta.get("title", ""),
        "description": test_case_meta.get("description", ""),
        "preconditions": test_case_meta.get("preconditions", []),
        "test_steps_planned": test_case_meta.get("test_steps_planned", []),
        "expected_results": test_case_meta.get("expected_results", {}),
        "pass_criteria": test_case_meta.get("pass_criteria", []),
        "fail_criteria": test_case_meta.get("fail_criteria", []),
        "acceptance_threshold": test_case_meta.get("acceptance_threshold", {}),
        "linked_requirements": test_case_meta.get("linked_requirements", []),
        "test_data_refs": test_case_meta.get("test_data_refs", []),
        "test_level": test_case_meta.get("test_level", "integration"),
    }


def build_execution_context_section(execution_id: str, timestamp: str) -> Dict[str, Any]:
    """Build execution_context section."""
    return {
        "execution_id": execution_id,
        "timestamp": timestamp,
        "executed_by": "pyrit_harness_v1.0",
        "execution_environment": "local_dev",
    }


def build_system_under_test_section(
    system_meta: Dict[str, Any], system_id: str
) -> Dict[str, Any]:
    """Build system_under_test section."""
    return {
        "system_id": system_id,
        "system_name": system_meta.get("system_name", ""),
        "system_version": system_meta.get("system_version", ""),
        "system_type": system_meta.get("system_type", "ai_model"),
        "vendor": system_meta.get("vendor", ""),
        "deployment_mode": system_meta.get("deployment_mode", "api"),
        "endpoint": system_meta.get("endpoint", ""),
        "model_family": system_meta.get("model_family", ""),
        "capabilities": system_meta.get("capabilities", []),
    }


def build_configuration_stack_section(
    stack_meta: Dict[str, Any], stack_id: str
) -> Dict[str, Any]:
    """Build configuration_stack section."""
    return {
        "stack_id": stack_id,
        "conversation_starter_config_id": stack_meta.get("conversation_starter_config_id", ""),
        "conversation_objective_config_id": stack_meta.get(
            "conversation_objective_config_id", ""
        ),
        "target_system_config_id": stack_meta.get("target_system_config_id", ""),
        "scoring_instruction_config_id": stack_meta.get("scoring_instruction_config_id", ""),
    }


def build_test_steps_section(scenario_id: str, execution_id: str) -> List[Dict[str, Any]]:
    """Build test_steps_executed section."""
    # For now, return a placeholder step since PYRIT doesn't expose detailed trace
    # In future, this would be populated from orchestrator execution trace
    return [
        {
            "step_id": 1,
            "action": f"Execute PYRIT scenario {scenario_id}",
            "status": "completed",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "result_summary": f"Execution {execution_id} completed",
        }
    ]


def build_actual_results_section(
    computed_metrics: Dict[str, Any], raw_results: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """Build actual_results section."""
    return {
        "raw_results": raw_results or {},
        "computed_metrics": computed_metrics,
    }


def build_evaluation_section(
    eval_rules: Dict[str, Any],
    computed_metrics: Dict[str, Any],
    violation_flags: Dict[str, bool],
    pass_fail: str,
) -> Dict[str, Any]:
    """Build evaluation section."""
    criteria_evaluations = []
    metric_mappings = eval_rules.get("metric_mappings", [])

    for mapping in metric_mappings:
        metric_name = mapping["metric_name"]
        metric_value = computed_metrics.get(metric_name)

        if metric_value is not None:
            criteria_evaluations.append(
                {
                    "criteria_id": mapping["criteria_id"],
                    "criteria_description": mapping["criteria_description"],
                    "measured_value": metric_value,
                    "threshold": mapping["threshold"],
                    "comparison_operator": mapping["comparison_operator"],
                    "outcome": mapping["outcome_on_trigger"],
                }
            )

    # Add violation flag evaluations
    for violation_key, is_violation in violation_flags.items():
        if is_violation:
            criteria_evaluations.append(
                {
                    "criteria_id": f"CRIT_{violation_key.upper()}",
                    "criteria_description": f"{violation_key} violation detected",
                    "measured_value": True,
                    "threshold": False,
                    "comparison_operator": "equals",
                    "outcome": "fail",
                }
            )

    return {
        "overall_result": pass_fail.lower(),
        "criteria_evaluations": criteria_evaluations,
    }


def build_success_evidence_section(
    pass_fail: str, computed_metrics: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Build success_evidence section."""
    if pass_fail == "PASS":
        return {
            "summary": "Test passed with no violations detected",
            "metrics_within_bounds": list(computed_metrics.keys()),
            "supporting_logs": [],
        }
    return None


def build_failure_evidence_section(
    pass_fail: str, violation_flags: Dict[str, bool], computed_metrics: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Build failure_evidence section."""
    if pass_fail == "FAIL":
        detected_violations = [k for k, v in violation_flags.items() if v]
        failing_metrics = []
        for metric_name, metric_value in computed_metrics.items():
            # Simple heuristic: if metric is > 0.5, consider it "failing"
            # (This should be replaced with proper threshold checks from eval rules)
            if isinstance(metric_value, (int, float)) and metric_value > 0.5:
                failing_metrics.append(metric_name)

        return {
            "summary": f"Test failed with {len(detected_violations)} violation(s) detected",
            "detected_violations": detected_violations,
            "failing_metrics": failing_metrics,
            "evidence_artifacts": [],
        }
    return None


def build_mitigation_section(
    violation_flags: Dict[str, bool], pass_fail: str, timestamp: str
) -> Dict[str, Any]:
    """Build mitigation section."""
    if pass_fail == "FAIL":
        detected_violations = [k for k, v in violation_flags.items() if v]
        if detected_violations:
            # Map violation flag to template key
            # E.g., "SELF_AMP_002" -> "SELF_violation"
            violation_flag = detected_violations[0]
            if violation_flag.startswith("SELF_"):
                template_key = "SELF_violation"
            elif violation_flag.startswith("NEG_"):
                template_key = "NEG_violation"
            elif violation_flag.startswith("DEM_"):
                template_key = "DEM_violation"
            elif violation_flag.startswith("EMO_"):
                template_key = "EMO_violation"
            elif violation_flag.startswith("INT_"):
                template_key = "INT_violation"
            else:
                template_key = "default"
            
            template = get_mitigation_template(template_key)

            # Build mitigation actions with due dates
            actions = []
            for action in template.get("mitigation_actions", []):
                due_offset_days = action.get("suggested_due_offset_days", 30)
                # Simple due date calculation (would use proper datetime in production)
                actions.append(
                    {
                        "action_id": f"MIT_{template_key}_{len(actions)+1}",
                        "description": action["description"],
                        "owner": action["default_owner"],
                        "due_date": f"T+{due_offset_days}d",  # Placeholder format
                        "status": "pending",
                    }
                )

            return {
                "mitigation_required": template["mitigation_required"],
                "mitigation_status": template["mitigation_status"],
                "mitigation_plan": template["mitigation_plan"],
                "mitigation_actions": actions,
            }

    # No mitigation needed
    template = get_mitigation_template("default")
    return {
        "mitigation_required": template["mitigation_required"],
        "mitigation_status": template["mitigation_status"],
        "mitigation_plan": template["mitigation_plan"],
        "mitigation_actions": template["mitigation_actions"],
    }


def build_provenance_section(execution_id: str, timestamp: str) -> Dict[str, Any]:
    """Build provenance section."""
    return {
        "generated_by": "pyrit_harness_evidence_builder_v1.0",
        "generated_at": timestamp,
        "record_hash": "",  # Filled in by build_evidence_record after hash computation
        "audit_trail": [
            {
                "timestamp": timestamp,
                "actor": "pyrit_harness",
                "action": "evidence_record_created",
                "execution_id": execution_id,
            }
        ],
    }
