"""
Configuration loaders for evidence builder.

Loads all YAML config files needed to populate evidence schema fields.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional


# Config directory path
CONFIG_DIR = Path(__file__).parent.parent / "config"


def load_scenarios_config() -> Dict[str, Any]:
    """Load scenarios configuration."""
    config_path = CONFIG_DIR / "scenarios.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_test_cases_config() -> Dict[str, Any]:
    """Load test cases configuration."""
    config_path = CONFIG_DIR / "test_cases.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_systems_config() -> Dict[str, Any]:
    """Load systems configuration."""
    config_path = CONFIG_DIR / "systems.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_config_stacks_config() -> Dict[str, Any]:
    """Load configuration stacks."""
    config_path = CONFIG_DIR / "config_stacks.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_evaluation_rules_config() -> Dict[str, Any]:
    """Load evaluation rules."""
    config_path = CONFIG_DIR / "evaluation_rules.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_mitigation_templates_config() -> Dict[str, Any]:
    """Load mitigation templates."""
    config_path = CONFIG_DIR / "mitigation_templates.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_scenario_metadata(scenario_id: str) -> Optional[Dict[str, Any]]:
    """Get scenario metadata by ID."""
    config = load_scenarios_config()
    return config["scenarios"].get(scenario_id)


def get_test_case_metadata(test_case_id: str) -> Optional[Dict[str, Any]]:
    """Get test case metadata by ID."""
    config = load_test_cases_config()
    return config["test_cases"].get(test_case_id)


def get_system_metadata(system_id: str) -> Optional[Dict[str, Any]]:
    """Get system metadata by ID."""
    config = load_systems_config()
    return config["systems"].get(system_id)


def get_config_stack(stack_id: str) -> Optional[Dict[str, Any]]:
    """Get configuration stack by ID."""
    config = load_config_stacks_config()
    return config["stacks"].get(stack_id)


def get_evaluation_rules_for_scenario(scenario_id: str) -> Optional[Dict[str, Any]]:
    """Get evaluation rules for a specific scenario."""
    config = load_evaluation_rules_config()
    scenario_rule_sets = config.get("scenario_rule_sets", {})
    scenario_set = scenario_rule_sets.get(scenario_id)
    
    if not scenario_set:
        return None
    
    # Build metric_mappings from scenario metrics
    rules = config.get("rules", {})
    metric_mappings = []
    
    for metric_name in scenario_set.get("metrics", []):
        rule = rules.get(metric_name)
        if rule:
            metric_mappings.append({
                "metric_name": metric_name,
                "criteria_id": f"{rule['criteria_id_prefix']}_{metric_name.upper()}",
                "criteria_description": rule["description"],
                "threshold": rule["threshold"],
                "comparison_operator": rule["operator"],
                "outcome_on_trigger": rule["criteria_type"],
            })
    
    return {"metric_mappings": metric_mappings}


def get_mitigation_template(violation_type: str) -> Dict[str, Any]:
    """Get mitigation template by violation type (e.g., 'SELF_violation')."""
    config = load_mitigation_templates_config()
    template = config["templates"].get(violation_type)
    if template:
        return template
    return config["default"]
