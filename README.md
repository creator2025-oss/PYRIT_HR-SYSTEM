# EU AI Act Annex III-4 HR Compliance Testing System

Complete demonstration system for testing HR systems against EU AI Act Annex III-4 requirements using PYRIT harness, live simulator, and interactive dashboard.

## 🎯 What This Does

- **Tests HR AI systems** for bias and compliance violations
- **Generates schema-compliant evidence** for regulatory audits
- **Interactive dashboard** to visualize test results and violations
- **Real biased simulator** that mimics problematic HR systems
- **5 pre-configured scenarios** covering key EU AI Act risks

## 📦 What's Included

```
EU_AI_Act_HR_Compliance_Demo/
├── pyrit_demo_harness/          # PYRIT testing harness
│   ├── config/                   # Test configurations (scenarios, eval rules, etc.)
│   ├── evidence/                 # Evidence builder (schema-compliant)
│   ├── pyrit_integration/        # PYRIT orchestrators, scorers, targets
│   ├── scenarios/                # 5 test scenarios (JSON + TOML)
│   ├── streamlit_app.py         # Interactive dashboard
│   └── runs/                     # Evidence output directory
│
├── hr_simulator/                 # FastAPI HR simulator (intentionally biased)
│   ├── src/                      # Biased scoring engine
│   ├── data/                     # Synthetic test data
│   └── run.py                    # Simulator server
│
├── SETUP.bat                     # One-click setup script
├── RUN_SIMULATOR.bat            # Start HR simulator
├── RUN_DASHBOARD.bat            # Start Streamlit dashboard
└── README.md                     # This file
```

## 🚀 Quick Start (3 Steps)

### 1. Install Dependencies

Double-click `SETUP.bat` or run:

```bash
pip install -r requirements.txt
```

### 2. Start HR Simulator

Double-click `RUN_SIMULATOR.bat` or run:

```bash
cd hr_simulator
python run.py
```

Simulator will run at **http://127.0.0.1:8600**

### 3. Start Dashboard

In a new terminal, double-click `RUN_DASHBOARD.bat` or run:

```bash
streamlit run pyrit_demo_harness/streamlit_app.py
```

Dashboard opens at **http://localhost:8501**

## 📊 Using the Dashboard

### **📊 Dashboard Tab**
- View all test results at a glance
- See pass/fail rates and compliance metrics
- Visualize violation types

### **🔬 Run Scenarios Tab**
- Select and run any of the 5 scenarios
- See live execution through PYRIT harness
- Real-time results with criteria evaluations
- View mitigation plans for failures

### **📋 Evidence Explorer Tab**
- Browse schema-compliant evidence records
- Validate against EU AI Act schema
- Download evidence as JSON

### **🔍 Scenario Deep-Dive Tab**
- Detailed analysis of each test
- What was tested, what failed, how to fix
- Complete mitigation action plans

## 🧪 Available Test Scenarios

| Scenario ID | Name | Tests For |
|------------|------|-----------|
| HR-02-SCEN-015 | Self-Amplification Bias | Agentic reasoning failures |
| HR-02-SCEN-017 | Emotion Misclassification | Inappropriate psychometric inference |
| HR-02-SCEN-019 | Demographic Leakage | Proxy discrimination (address/accent) |
| HR-02-SCEN-022 | Negotiation Bias | Compensation bias across demographics |
| HR-02-SCEN-025 | Intervention Bias | Unfair performance interventions |

## 🔧 How It Works

```
1. PYRIT Harness
   ↓
   Loads scenario → Builds candidate payload
   ↓
2. HR Simulator (FastAPI)
   ↓
   Biased scoring engine processes candidate
   ↓
3. PYRIT Scorer
   ↓
   Evaluates results against EU AI Act criteria
   ↓
4. Evidence Builder
   ↓
   Generates schema-compliant audit record
   ↓
5. Dashboard
   ↓
   Visualizes results, violations, and mitigation plans
```

## 📁 Key Files

### Configuration
- `pyrit_demo_harness/config/scenarios.yaml` - Scenario metadata
- `pyrit_demo_harness/config/test_cases.yaml` - Test case definitions
- `pyrit_demo_harness/config/evaluation_rules.yaml` - Pass/fail criteria
- `pyrit_demo_harness/config/mitigation_templates.yaml` - Mitigation plans

### Evidence
- `pyrit_demo_harness/runs/evidence_jsonl/*.jsonl` - Evidence records
- Schema version: `annexIII4_evidence_v1.0`
- 13 required top-level fields per EU AI Act Annex III-4

### Simulator
- `hr_simulator/src/core/biased_scoring.py` - Intentionally biased logic
- Implements 5 violation types: SELF, NEG, DEM, EMO, INT

## 🎓 For Your Colleague

### First Time Setup (5 minutes)

1. **Clone or download this folder**
2. **Open terminal in this directory**
3. **Run setup:** `SETUP.bat` (or `pip install -r requirements.txt`)
4. **Start simulator:** `RUN_SIMULATOR.bat` (keep this running)
5. **Start dashboard:** `RUN_DASHBOARD.bat` (opens browser automatically)

### Running Tests

**Option 1: Use Dashboard (Recommended)**
- Go to "🔬 Run Scenarios" tab
- Click "Run Scenario" button
- Watch live execution

**Option 2: Command Line**
```bash
python -c "from pyrit_demo_harness.pyrit_integration.pyrit_runner import run_with_pyrit; run_with_pyrit('HR-02-SCEN-015')"
```

### Viewing Results

- Dashboard shows all results automatically
- Evidence files saved to `pyrit_demo_harness/runs/evidence_jsonl/`
- Each scenario has its own `.jsonl` file

## 🛠️ Troubleshooting

### "Module not found" errors
```bash
# Make sure you're in the right directory
cd EU_AI_Act_HR_Compliance_Demo

# Re-run setup
pip install -r requirements.txt
```

### Simulator not responding
```bash
# Check if simulator is running
curl http://127.0.0.1:8600/health

# Or visit in browser: http://127.0.0.1:8600/health
# Should show: {"status": "healthy", ...}
```

### Dashboard not loading
```bash
# Make sure streamlit is installed
pip install streamlit plotly

# Run manually
streamlit run pyrit_demo_harness/streamlit_app.py
```

## 📚 Evidence Schema

All evidence records conform to `annexIII4_evidence_v1.0` schema with 13 required sections:

1. `schema_version` - Schema identifier
2. `scenario` - Test scenario metadata
3. `test_case` - Test case definition
4. `execution_context` - Execution metadata
5. `system_under_test` - Target system info
6. `configuration_stack` - PYRIT config stack
7. `test_steps_executed` - Execution trace
8. `actual_results` - Raw and computed results
9. `evaluation` - Criteria evaluations
10. `success_evidence` - Evidence for passing tests
11. `failure_evidence` - Evidence for failing tests
12. `mitigation` - Mitigation plans and actions
13. `provenance` - Audit trail + SHA-256 hash

## 💡 Use Cases

- **Compliance Testing** - Test HR systems before deployment
- **Regulatory Audits** - Generate compliant evidence
- **Risk Assessment** - Identify bias patterns
- **Client Demos** - Show testing capabilities
- **Training** - Teach EU AI Act compliance

## 📧 Support

For issues or questions, check the dashboard logs or simulator logs.

---

**Ready to test!** Start with `SETUP.bat` then `RUN_SIMULATOR.bat` and `RUN_DASHBOARD.bat`
