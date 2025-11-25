# Quick Start Guide

## For Your Colleague (First Time Setup)

### Prerequisites
- Python 3.9+ installed
- Terminal/Command Prompt access

### Setup (5 Minutes)

1. **Download/Clone this folder** (`EU_AI_Act_HR_Compliance_Demo`)

2. **Open terminal in this directory**
   ```bash
   cd EU_AI_Act_HR_Compliance_Demo
   ```

3. **Install dependencies**
   - Windows: Double-click `SETUP.bat`
   - Or run: `pip install -r requirements.txt`

4. **Start the HR Simulator** (Keep this running!)
   - Windows: Double-click `RUN_SIMULATOR.bat`
   - Or run: `cd hr_simulator && python run.py`
   - Check it's running: Open browser to http://127.0.0.1:8600/health

5. **Start the Dashboard** (New terminal)
   - Windows: Double-click `RUN_DASHBOARD.bat`
   - Or run: `streamlit run pyrit_demo_harness/streamlit_app.py`
   - Dashboard auto-opens at http://localhost:8501

## Using the System

### Dashboard Overview

**4 Main Tabs:**

1. **📊 Dashboard** - See all test results, pass/fail rates, violations
2. **🔬 Run Scenarios** - Execute tests through live PYRIT harness
3. **📋 Evidence Explorer** - Browse schema-compliant evidence
4. **🔍 Scenario Deep-Dive** - Detailed analysis and mitigation plans

### Running Your First Test

1. Go to **"🔬 Run Scenarios"** tab
2. Select `HR-02-SCEN-015` (Self-Amplification Bias)
3. Click **"▶️ Run Scenario"**
4. Watch it execute through:
   - PYRIT Harness → HR Simulator → Scorer → Evidence Builder
5. See results immediately:
   - ✅ or ❌ Pass/Fail
   - Criteria evaluations
   - Mitigation plan (if failed)

### Available Test Scenarios

- **HR-02-SCEN-015**: Self-Amplification Bias
- **HR-02-SCEN-017**: Emotion Misclassification  
- **HR-02-SCEN-019**: Demographic Leakage
- **HR-02-SCEN-022**: Negotiation Bias
- **HR-02-SCEN-025**: Intervention Bias

### Understanding Results

**If Test PASSES ✅:**
- System complies with EU AI Act requirements
- No violations detected
- Evidence saved to `runs/evidence_jsonl/`

**If Test FAILS ❌:**
- Compliance violations detected
- See "Detected Violations" section
- Review mitigation plan
- Action items with owners and deadlines

### Evidence Files

All test runs generate evidence records at:
```
pyrit_demo_harness/runs/evidence_jsonl/
  ├── HR-02-SCEN-015.jsonl
  ├── HR-02-SCEN-017.jsonl
  └── ...
```

Each record is **schema-compliant** with 13 required sections per EU AI Act.

## Command Line Usage (Alternative)

### Run Single Scenario
```bash
python -c "from pyrit_demo_harness.pyrit_integration.pyrit_runner import run_with_pyrit; run_with_pyrit('HR-02-SCEN-015')"
```

### Run All Scenarios
```bash
python -c "
scenarios = ['HR-02-SCEN-015', 'HR-02-SCEN-017', 'HR-02-SCEN-019', 'HR-02-SCEN-022', 'HR-02-SCEN-025']
from pyrit_demo_harness.pyrit_integration.pyrit_runner import run_with_pyrit
for s in scenarios:
    print(f'Running {s}...')
    run_with_pyrit(s)
"
```

## Troubleshooting

### Simulator Won't Start
```bash
# Check if port 8600 is already in use
netstat -ano | findstr :8600

# Try different port in hr_simulator/run.py
```

### "Module not found" Error
```bash
# Re-run setup
pip install -r requirements.txt

# Or install individually
pip install streamlit plotly pyyaml requests fastapi uvicorn
```

### Dashboard Shows No Data
1. Make sure simulator is running (http://127.0.0.1:8600/health)
2. Run at least one scenario first
3. Check `pyrit_demo_harness/runs/evidence_jsonl/` exists

### Evidence Files Missing
```bash
# Create runs directory if it doesn't exist
mkdir pyrit_demo_harness\runs\evidence_jsonl
```

## Architecture Overview

```
┌─────────────────────┐
│  Streamlit          │  ← You interact here
│  Dashboard          │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  PYRIT Harness      │  ← Loads scenarios, orchestrates
│                     │
│  • Scenario Loader  │
│  • Orchestrator     │
│  • Scorer           │
│  • Evidence Builder │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  HR Simulator       │  ← Biased scoring engine
│  (FastAPI)          │
│                     │
│  Port: 8600         │
└─────────────────────┘
```

## What Gets Tested

Each scenario tests for specific EU AI Act violations:

1. **Self-Amplification** - Agentic reasoning loops
2. **Emotion Inference** - Psychometric profiling
3. **Demographic Leakage** - Proxy discrimination
4. **Compensation Bias** - Unfair salary decisions
5. **Intervention Bias** - Unfair performance actions

## Next Steps

1. ✅ Run all 5 scenarios through dashboard
2. ✅ Explore evidence in "Evidence Explorer" tab
3. ✅ Review mitigation plans in "Deep-Dive" tab
4. ✅ Download evidence records as JSON
5. ✅ Share results with compliance team

---

**Need help?** Check main `README.md` or simulator logs
