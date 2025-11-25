"""
EU AI Act Annex III-4 HR System Compliance Dashboard

Demonstrates live PYRIT harness execution against HR simulator
with schema-compliant evidence generation.
"""

import streamlit as st
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import harness components
from pyrit_demo_harness.pyrit_integration.pyrit_runner import run_with_pyrit
from pyrit_demo_harness.adapters.scenario_loader import load_scenario

# Page config
st.set_page_config(
    page_title="EU AI Act Compliance Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Scenarios configuration
SCENARIOS = {
    "HR-02-SCEN-015": {
        "name": "Self-Amplification Bias",
        "family": "agentic_reasoning_failure",
        "description": "Tests for self-reinforcing bias in agentic screening",
    },
    "HR-02-SCEN-017": {
        "name": "Emotion Misclassification",
        "family": "emotion_misclassification",
        "description": "Tests for inappropriate psychometric inference",
    },
    "HR-02-SCEN-019": {
        "name": "Demographic Leakage",
        "family": "demographic_leakage",
        "description": "Tests for proxy discrimination via address/accent",
    },
    "HR-02-SCEN-022": {
        "name": "Negotiation Bias",
        "family": "bias_fairness_recruitment_negotiation",
        "description": "Tests for compensation bias across demographics",
    },
    "HR-02-SCEN-025": {
        "name": "Intervention Bias",
        "family": "intervention_bias",
        "description": "Tests for unfair performance intervention patterns",
    },
}


def load_latest_evidence(scenario_id):
    """Load latest evidence record for a scenario."""
    evidence_dir = Path("pyrit_demo_harness/runs/evidence_jsonl")
    evidence_file = evidence_dir / f"{scenario_id}.jsonl"
    
    if not evidence_file.exists():
        return None
    
    # Read last line (latest record)
    with open(evidence_file, "r") as f:
        lines = f.readlines()
        if lines:
            return json.loads(lines[-1])
    return None


def run_scenario_live(scenario_id):
    """Execute scenario through real harness and simulator."""
    with st.spinner(f"🔄 Running {scenario_id} through PYRIT harness..."):
        try:
            # Run through actual harness (calls real simulator)
            result = run_with_pyrit(scenario_id, mode="simulator")
            st.success(f"✅ Scenario {scenario_id} completed!")
            return result
        except Exception as e:
            st.error(f"❌ Error running scenario: {str(e)}")
            return None


def render_sidebar():
    """Render sidebar navigation."""
    st.sidebar.title("🛡️ EU AI Act Compliance")
    st.sidebar.markdown("**Annex III-4 HR System Testing**")
    st.sidebar.divider()
    
    page = st.sidebar.radio(
        "Navigation",
        ["📊 Dashboard", "🔬 Run Scenarios", "📋 Evidence Explorer", "🔍 Scenario Deep-Dive"],
        label_visibility="collapsed"
    )
    
    st.sidebar.divider()
    st.sidebar.info(
        "**Live Components:**\n\n"
        "✅ HR Simulator (FastAPI)\n\n"
        "✅ PYRIT Harness\n\n"
        "✅ Evidence Builder\n\n"
        "✅ Schema Validator"
    )
    
    return page


def render_dashboard():
    """Render main dashboard overview."""
    st.title("📊 EU AI Act Compliance Dashboard")
    st.markdown("**Live testing harness for Annex III-4 HR systems**")
    
    # Load all latest evidence
    evidence_records = {}
    for scenario_id in SCENARIOS.keys():
        evidence = load_latest_evidence(scenario_id)
        if evidence:
            evidence_records[scenario_id] = evidence
    
    if not evidence_records:
        st.warning("⚠️ No evidence records found. Run scenarios first.")
        return
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    passed = sum(1 for e in evidence_records.values() if e.get("evaluation", {}).get("overall_result") == "pass")
    failed = len(evidence_records) - passed
    
    with col1:
        st.metric("Total Scenarios", len(evidence_records))
    with col2:
        st.metric("✅ Passed", passed, delta=None)
    with col3:
        st.metric("❌ Failed", failed, delta=None)
    with col4:
        compliance_rate = (passed / len(evidence_records) * 100) if evidence_records else 0
        st.metric("Compliance Rate", f"{compliance_rate:.0f}%")
    
    st.divider()
    
    # Scenario status table
    st.subheader("📋 Scenario Test Results")
    
    rows = []
    for scenario_id, meta in SCENARIOS.items():
        evidence = evidence_records.get(scenario_id)
        if evidence:
            eval_result = evidence.get("evaluation", {})
            result = eval_result.get("overall_result", "unknown").upper()
            criteria_count = len(eval_result.get("criteria_evaluations", []))
            mitigation_required = evidence.get("mitigation", {}).get("mitigation_required", False)
            timestamp = evidence.get("execution_context", {}).get("timestamp", "N/A")
            
            # Format timestamp safely
            if timestamp != "N/A" and isinstance(timestamp, str):
                last_run = timestamp[:19]
            else:
                last_run = "N/A"
            
            rows.append({
                "Scenario ID": scenario_id,
                "Name": meta["name"],
                "Family": meta["family"],
                "Result": result,
                "Criteria Evaluated": criteria_count,
                "Mitigation Required": "Yes" if mitigation_required else "No",
                "Last Run": last_run,
            })
    
    df = pd.DataFrame(rows)
    
    # Style the dataframe
    def color_result(val):
        if val == "PASS":
            return "background-color: #90EE90"
        elif val == "FAIL":
            return "background-color: #FFB6C1"
        return ""
    
    styled_df = df.style.applymap(color_result, subset=["Result"])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # Violations breakdown
    st.subheader("🚨 Detected Violations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Violation counts by type
        violation_counts = {}
        for evidence in evidence_records.values():
            failure_evidence = evidence.get("failure_evidence")
            if failure_evidence:
                for violation in failure_evidence.get("detected_violations", []):
                    violation_type = violation.split("_")[0]  # e.g., "SELF" from "SELF_AMP_002"
                    violation_counts[violation_type] = violation_counts.get(violation_type, 0) + 1
        
        if violation_counts:
            fig = px.bar(
                x=list(violation_counts.keys()),
                y=list(violation_counts.values()),
                labels={"x": "Violation Type", "y": "Count"},
                title="Violation Types Detected",
                color=list(violation_counts.values()),
                color_continuous_scale="Reds",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No violations detected across all scenarios")
    
    with col2:
        # Mitigation actions required
        mitigation_counts = sum(
            1 for e in evidence_records.values() 
            if e.get("mitigation", {}).get("mitigation_required")
        )
        
        fig = go.Figure(data=[go.Pie(
            labels=["Mitigation Required", "No Action Needed"],
            values=[mitigation_counts, len(evidence_records) - mitigation_counts],
            marker_colors=["#FF6B6B", "#51CF66"],
        )])
        fig.update_layout(title="Mitigation Status")
        st.plotly_chart(fig, use_container_width=True)


def render_run_scenarios():
    """Render scenario execution page."""
    st.title("🔬 Run Test Scenarios")
    st.markdown("Execute compliance tests against **live HR simulator** using **PYRIT harness**")
    
    st.info(
        "**How it works:**\n\n"
        "1. Select a scenario below\n"
        "2. Click 'Run Scenario' to execute through PYRIT\n"
        "3. Harness calls the HR simulator with test data\n"
        "4. Biased scoring engine processes candidate\n"
        "5. PYRIT scorer evaluates results against EU AI Act criteria\n"
        "6. Evidence builder generates schema-compliant audit record"
    )
    
    st.divider()
    
    # Scenario selection
    scenario_id = st.selectbox(
        "Select Scenario",
        options=list(SCENARIOS.keys()),
        format_func=lambda x: f"{x}: {SCENARIOS[x]['name']}",
    )
    
    scenario_meta = SCENARIOS[scenario_id]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**Description:** {scenario_meta['description']}")
        st.markdown(f"**Family:** {scenario_meta['family']}")
    
    with col2:
        if st.button("▶️ Run Scenario", type="primary", use_container_width=True):
            # Execute through real harness
            result = run_scenario_live(scenario_id)
            
            if result:
                st.session_state[f"last_result_{scenario_id}"] = result
    
    st.divider()
    
    # Show latest result if available
    result_key = f"last_result_{scenario_id}"
    if result_key in st.session_state:
        result = st.session_state[result_key]
        
        st.subheader("📊 Test Results")
        
        # Result summary
        eval_result = result.get("evaluation", {}).get("overall_result", "unknown")
        
        if eval_result == "pass":
            st.success(f"✅ **TEST PASSED** - System complies with EU AI Act requirements")
        else:
            st.error(f"❌ **TEST FAILED** - Compliance violations detected")
        
        # Key metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Overall Result", eval_result.upper())
        
        with col2:
            criteria_count = len(result.get("evaluation", {}).get("criteria_evaluations", []))
            st.metric("Criteria Evaluated", criteria_count)
        
        with col3:
            mitigation_required = result.get("mitigation", {}).get("mitigation_required", False)
            st.metric("Mitigation Required", "Yes" if mitigation_required else "No")
        
        # Criteria evaluations
        st.subheader("📋 Criteria Evaluations")
        criteria_evals = result.get("evaluation", {}).get("criteria_evaluations", [])
        
        for i, crit in enumerate(criteria_evals, 1):
            with st.expander(f"#{i}: {crit['criteria_id']} - {crit['outcome'].upper()}"):
                st.markdown(f"**Description:** {crit['criteria_description']}")
                st.markdown(f"**Measured Value:** {crit['measured_value']}")
                st.markdown(f"**Threshold:** {crit['threshold']}")
                st.markdown(f"**Operator:** {crit['comparison_operator']}")
        
        # Mitigation plan
        if result.get("failure_evidence"):
            st.subheader("🔧 Mitigation Plan")
            
            mitigation = result.get("mitigation", {})
            
            st.markdown(f"**Status:** {mitigation.get('mitigation_status', 'N/A')}")
            
            if mitigation.get("mitigation_plan"):
                st.markdown("**Plan:**")
                st.text(mitigation["mitigation_plan"])
            
            st.markdown("**Actions:**")
            for action in mitigation.get("mitigation_actions", []):
                st.markdown(
                    f"- **{action['action_id']}**: {action['description']} "
                    f"(Owner: {action['owner']}, Due: {action['due_date']})"
                )


def render_evidence_explorer():
    """Render evidence explorer page."""
    st.title("📋 Evidence Explorer")
    st.markdown("Browse schema-compliant evidence records")
    
    # Load all evidence
    evidence_records = {}
    for scenario_id in SCENARIOS.keys():
        evidence = load_latest_evidence(scenario_id)
        if evidence:
            evidence_records[scenario_id] = evidence
    
    if not evidence_records:
        st.warning("⚠️ No evidence records found. Run scenarios first.")
        return
    
    # Scenario selector
    scenario_id = st.selectbox(
        "Select Scenario",
        options=list(evidence_records.keys()),
        format_func=lambda x: f"{x}: {SCENARIOS[x]['name']}",
    )
    
    evidence = evidence_records[scenario_id]
    
    # Schema validation
    st.subheader("✅ Schema Compliance")
    
    required_fields = [
        "schema_version", "scenario", "test_case", "execution_context",
        "system_under_test", "configuration_stack", "test_steps_executed",
        "actual_results", "evaluation", "success_evidence", "failure_evidence",
        "mitigation", "provenance"
    ]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Schema Version", evidence.get("schema_version", "N/A"))
    with col2:
        present_fields = sum(1 for f in required_fields if f in evidence)
        st.metric("Required Fields", f"{present_fields}/{len(required_fields)}")
    with col3:
        st.metric("Record Hash", evidence.get("provenance", {}).get("record_hash", "N/A")[:16] + "...")
    
    st.divider()
    
    # Section viewer
    st.subheader("📄 Evidence Sections")
    
    tabs = st.tabs([
        "Scenario", "Test Case", "Execution", "System Under Test",
        "Evaluation", "Evidence", "Mitigation", "Provenance"
    ])
    
    with tabs[0]:
        st.json(evidence.get("scenario", {}))
    
    with tabs[1]:
        st.json(evidence.get("test_case", {}))
    
    with tabs[2]:
        st.json(evidence.get("execution_context", {}))
    
    with tabs[3]:
        st.json(evidence.get("system_under_test", {}))
    
    with tabs[4]:
        st.json(evidence.get("evaluation", {}))
    
    with tabs[5]:
        if evidence.get("success_evidence"):
            st.markdown("**Success Evidence:**")
            st.json(evidence["success_evidence"])
        if evidence.get("failure_evidence"):
            st.markdown("**Failure Evidence:**")
            st.json(evidence["failure_evidence"])
    
    with tabs[6]:
        st.json(evidence.get("mitigation", {}))
    
    with tabs[7]:
        st.json(evidence.get("provenance", {}))
    
    st.divider()
    
    # Download button
    st.download_button(
        label="📥 Download Evidence Record (JSON)",
        data=json.dumps(evidence, indent=2),
        file_name=f"{scenario_id}_evidence.json",
        mime="application/json",
    )


def render_deep_dive():
    """Render detailed scenario analysis."""
    st.title("🔍 Scenario Deep-Dive")
    
    scenario_id = st.selectbox(
        "Select Scenario for Analysis",
        options=list(SCENARIOS.keys()),
        format_func=lambda x: f"{x}: {SCENARIOS[x]['name']}",
    )
    
    evidence = load_latest_evidence(scenario_id)
    
    if not evidence:
        st.warning(f"No evidence found for {scenario_id}. Run the scenario first.")
        return
    
    scenario_meta = SCENARIOS[scenario_id]
    
    # Header
    st.markdown(f"## {scenario_meta['name']}")
    st.markdown(f"**{scenario_id}** | {scenario_meta['family']}")
    
    st.divider()
    
    # Test flow diagram
    st.subheader("🔄 Test Flow")
    st.markdown(
        """
        ```
        1. PYRIT Harness
           └─> Load Scenario JSON
           └─> Build Candidate Payload
        
        2. HR Simulator (FastAPI)
           └─> Biased Scoring Engine
           └─> Return Results + Violations
        
        3. PYRIT Scorer
           └─> Evaluate Against Criteria
           └─> Flag Violations
        
        4. Evidence Builder
           └─> Build Schema-Compliant Record
           └─> Write to JSONL
        ```
        """
    )
    
    st.divider()
    
    # What was tested
    st.subheader("🎯 What Was Tested")
    test_case = evidence.get("test_case", {})
    st.markdown(f"**Test Case:** {test_case.get('test_case_id', 'N/A')}")
    st.markdown(f"**Title:** {test_case.get('title', 'N/A')}")
    st.markdown(f"**Description:** {test_case.get('description', 'N/A')}")
    
    st.markdown("**Pass Criteria:**")
    for criterion in test_case.get("pass_criteria", []):
        st.markdown(f"- ✅ {criterion}")
    
    st.markdown("**Fail Criteria:**")
    for criterion in test_case.get("fail_criteria", []):
        st.markdown(f"- ❌ {criterion}")
    
    st.divider()
    
    # What the harness found
    st.subheader("🔍 What The Harness Found")
    
    evaluation = evidence.get("evaluation", {})
    result = evaluation.get("overall_result", "unknown")
    
    if result == "pass":
        st.success("✅ **PASSED** - No compliance violations detected")
    else:
        st.error("❌ **FAILED** - Compliance violations detected")
    
    # Detailed findings
    st.markdown("**Criteria Evaluations:**")
    for crit in evaluation.get("criteria_evaluations", []):
        outcome_icon = "✅" if crit["outcome"] == "pass" else "❌"
        st.markdown(
            f"{outcome_icon} **{crit['criteria_id']}**: {crit['criteria_description']} "
            f"(Measured: {crit['measured_value']}, Threshold: {crit['threshold']})"
        )
    
    # Failure details
    if evidence.get("failure_evidence"):
        st.divider()
        st.subheader("❌ Failure Details")
        
        failure = evidence["failure_evidence"]
        st.markdown(f"**Summary:** {failure.get('summary', 'N/A')}")
        
        st.markdown("**Detected Violations:**")
        for violation in failure.get("detected_violations", []):
            st.markdown(f"- 🚨 {violation}")
        
        st.markdown("**Failing Metrics:**")
        for metric in failure.get("failing_metrics", []):
            actual_value = evidence.get("actual_results", {}).get("computed_metrics", {}).get(metric)
            st.markdown(f"- 📊 {metric}: {actual_value}")
    
    st.divider()
    
    # How to fix
    if evidence.get("mitigation", {}).get("mitigation_required"):
        st.subheader("🔧 How To Fix")
        
        mitigation = evidence["mitigation"]
        
        st.markdown("**Mitigation Plan:**")
        st.info(mitigation.get("mitigation_plan", "N/A"))
        
        st.markdown("**Required Actions:**")
        for action in mitigation.get("mitigation_actions", []):
            with st.expander(f"{action['action_id']} - {action['owner']}"):
                st.markdown(f"**Description:** {action['description']}")
                st.markdown(f"**Due Date:** {action['due_date']}")
                st.markdown(f"**Status:** {action['status']}")


def main():
    """Main application entry point."""
    page = render_sidebar()
    
    if page == "📊 Dashboard":
        render_dashboard()
    elif page == "🔬 Run Scenarios":
        render_run_scenarios()
    elif page == "📋 Evidence Explorer":
        render_evidence_explorer()
    elif page == "🔍 Scenario Deep-Dive":
        render_deep_dive()


if __name__ == "__main__":
    main()
