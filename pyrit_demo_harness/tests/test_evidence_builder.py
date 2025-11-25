"""
Unit tests for evidence builder module.

Tests the schema-compliant evidence generation functionality.
"""

import pytest
import json
from datetime import datetime
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pyrit_demo_harness.evidence.builder import (
    build_evidence_record,
    build_scenario_section,
    build_test_case_section,
    build_mitigation_section,
    SCHEMA_VERSION,
)


class TestEvidenceBuilder:
    """Test suite for evidence builder functions."""
    
    def test_schema_version(self):
        """Test that schema version is correct."""
        assert SCHEMA_VERSION == "annexIII4_evidence_v1.0"
    
    def test_build_evidence_record_structure(self):
        """Test that evidence record has all required fields."""
        record = build_evidence_record(
            scenario_id="HR-02-SCEN-015",
            execution_id="test-exec-001",
            timestamp=datetime.now().isoformat(),
            system_id="hr_sim_001",
            stack_id="stack_001",
            computed_metrics={"self_amplification_factor": 0.08},
            violation_flags={"SELF_AMP_002": True},
            pass_fail="FAIL",
            raw_results={"test": "data"},
        )
        
        # Check all 13 required top-level fields
        required_fields = [
            "schema_version",
            "scenario",
            "test_case",
            "execution_context",
            "system_under_test",
            "configuration_stack",
            "test_steps_executed",
            "actual_results",
            "evaluation",
            "success_evidence",
            "failure_evidence",
            "mitigation",
            "provenance",
        ]
        
        for field in required_fields:
            assert field in record, f"Missing required field: {field}"
    
    def test_build_evidence_record_pass(self):
        """Test evidence record for passing scenario."""
        record = build_evidence_record(
            scenario_id="HR-02-SCEN-017",
            execution_id="test-exec-002",
            timestamp=datetime.now().isoformat(),
            system_id="hr_sim_001",
            stack_id="stack_001",
            computed_metrics={"false_positive_rate": 0.15},
            violation_flags={},
            pass_fail="PASS",
        )
        
        assert record["evaluation"]["overall_result"] == "pass"
        assert record["success_evidence"] is not None
        assert record["failure_evidence"] is None
        assert record["mitigation"]["mitigation_required"] is False
    
    def test_build_evidence_record_fail(self):
        """Test evidence record for failing scenario."""
        record = build_evidence_record(
            scenario_id="HR-02-SCEN-015",
            execution_id="test-exec-003",
            timestamp=datetime.now().isoformat(),
            system_id="hr_sim_001",
            stack_id="stack_001",
            computed_metrics={"self_amplification_factor": 0.12},
            violation_flags={"SELF_AMP_002": True},
            pass_fail="FAIL",
        )
        
        assert record["evaluation"]["overall_result"] == "fail"
        assert record["success_evidence"] is None
        assert record["failure_evidence"] is not None
        assert record["mitigation"]["mitigation_required"] is True
    
    def test_provenance_hash_computed(self):
        """Test that provenance hash is computed."""
        record = build_evidence_record(
            scenario_id="HR-02-SCEN-015",
            execution_id="test-exec-004",
            timestamp=datetime.now().isoformat(),
            system_id="hr_sim_001",
            stack_id="stack_001",
            computed_metrics={"test_metric": 0.5},
            violation_flags={},
            pass_fail="PASS",
        )
        
        assert "provenance" in record
        assert "record_hash" in record["provenance"]
        assert len(record["provenance"]["record_hash"]) == 64  # SHA-256 hex length
    
    def test_scenario_section(self):
        """Test scenario section builder."""
        scenario_meta = {
            "title": "Test Scenario",
            "description": "Test description",
            "objective": "Test objective",
            "scenario_type": "bias_detection",
            "tags": ["test", "demo"],
            "regulatory_scope": {
                "eu_ai_act_annex": "III-4",
                "risk_category": "high-risk",
                "applicable_articles": ["Art. 10"],
            },
        }
        
        section = build_scenario_section(scenario_meta, "HR-02-SCEN-015")
        
        assert section["scenario_id"] == "HR-02-SCEN-015"
        assert section["title"] == "Test Scenario"
        assert section["scenario_type"] == "bias_detection"
        assert "Art. 10" in section["regulatory_scope"]["applicable_articles"]
    
    def test_mitigation_section_with_violations(self):
        """Test mitigation section for failed scenarios."""
        mitigation = build_mitigation_section(
            violation_flags={"SELF_AMP_002": True, "OTHER": False},
            pass_fail="FAIL",
            timestamp=datetime.now().isoformat(),
        )
        
        assert mitigation["mitigation_required"] is True
        assert mitigation["mitigation_status"] == "pending"
        assert mitigation["mitigation_plan"] is not None
        assert len(mitigation["mitigation_actions"]) > 0
    
    def test_mitigation_section_no_violations(self):
        """Test mitigation section for passed scenarios."""
        mitigation = build_mitigation_section(
            violation_flags={},
            pass_fail="PASS",
            timestamp=datetime.now().isoformat(),
        )
        
        assert mitigation["mitigation_required"] is False
        assert mitigation["mitigation_status"] == "not_applicable"
    
    def test_evidence_serializable(self):
        """Test that evidence record is JSON serializable."""
        record = build_evidence_record(
            scenario_id="HR-02-SCEN-015",
            execution_id="test-exec-005",
            timestamp=datetime.now().isoformat(),
            system_id="hr_sim_001",
            stack_id="stack_001",
            computed_metrics={"metric": 0.5},
            violation_flags={},
            pass_fail="PASS",
        )
        
        # Should not raise exception
        json_str = json.dumps(record)
        assert len(json_str) > 0
        
        # Should be able to parse back
        parsed = json.loads(json_str)
        assert parsed["schema_version"] == SCHEMA_VERSION


class TestEvidenceValidation:
    """Test suite for evidence validation."""
    
    def test_all_scenarios_have_config(self):
        """Test that all 5 scenarios have configuration."""
        scenarios = [
            "HR-02-SCEN-015",
            "HR-02-SCEN-017",
            "HR-02-SCEN-019",
            "HR-02-SCEN-022",
            "HR-02-SCEN-025",
        ]
        
        for scenario_id in scenarios:
            # Should not raise exception
            record = build_evidence_record(
                scenario_id=scenario_id,
                execution_id=f"test-{scenario_id}",
                timestamp=datetime.now().isoformat(),
                system_id="hr_sim_001",
                stack_id="stack_001",
                computed_metrics={"test": 0.5},
                violation_flags={},
                pass_fail="PASS",
            )
            assert record["scenario"]["scenario_id"] == scenario_id
    
    def test_invalid_scenario_raises_error(self):
        """Test that invalid scenario ID raises error."""
        with pytest.raises(ValueError, match="not found in config"):
            build_evidence_record(
                scenario_id="INVALID-SCENARIO",
                execution_id="test",
                timestamp=datetime.now().isoformat(),
                system_id="hr_sim_001",
                stack_id="stack_001",
                computed_metrics={},
                violation_flags={},
                pass_fail="PASS",
            )
    
    def test_criteria_evaluations_populated(self):
        """Test that criteria evaluations are populated from eval rules."""
        record = build_evidence_record(
            scenario_id="HR-02-SCEN-015",
            execution_id="test-criteria",
            timestamp=datetime.now().isoformat(),
            system_id="hr_sim_001",
            stack_id="stack_001",
            computed_metrics={
                "self_amplification_factor": 0.08,
                "scoring_stability_index": 0.12,
            },
            violation_flags={"SELF_AMP_002": True},
            pass_fail="FAIL",
        )
        
        criteria_evals = record["evaluation"]["criteria_evaluations"]
        assert len(criteria_evals) > 0
        
        # Check structure
        for crit in criteria_evals:
            assert "criteria_id" in crit
            assert "criteria_description" in crit
            assert "measured_value" in crit
            assert "threshold" in crit
            assert "outcome" in crit


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
