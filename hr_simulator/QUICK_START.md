# EU AI Act HR Simulator - Quick Start Guide

## 🚀 Start the System

```powershell
# Option 1: Double-click
START_SERVER.bat

# Option 2: Command line
.\venv\Scripts\python.exe run.py
```

**Server runs at**: http://localhost:8600  
**API Docs**: http://localhost:8600/docs

---

## ✅ System Check

```powershell
.\venv\Scripts\python.exe check_system.py
```

Shows:
- File structure validation
- Import verification  
- Data file counts
- Bias detection test

---

## 📊 Current Status: 8/15 Scenarios (53%)

### ✅ Implemented
- SC04: Skill Hallucination (social media)
- SC06: Gender Bias (name-based)
- SC07: Age Proxy (graduation year)
- SC09: Prompt Injection (CV manipulation)
- SC10: SES Bias (postal code)
- SC15: Agentic Amplification (delegation loop)
- SC21: Visa Penalty (work authorization)
- SC22: Minority Name Bias (ethnicity)

### ⏳ To Implement
- SC01: Ad Targeting Gender Exclusion
- SC02: Rural Geolocation Exclusion
- SC03: SES Ad Targeting
- SC05: Discriminatory Ad Copy
- SC08: Memory Cross-Contamination
- SC11: Career Gap Maternity Bias
- SC12: Skill Exaggeration Amplification
- SC13: Reasoning Chain Leakage
- SC14: Legacy Model Persistence

---

## 🧪 Test the System

### Submit a Candidate

```bash
curl -X POST http://localhost:8600/api/candidates/submit \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Emily Chen",
    "email": "emily@example.com",
    "education": {
      "degree": "BS Computer Science",
      "institution": "Stanford",
      "graduation_year": 2018
    },
    "address": {
      "street": "123 Main St",
      "city": "San Francisco",
      "postal_code": "94102"
    },
    "skills": ["Python", "Java"],
    "visa_required": false
  }'
```

### Expected Response

```json
{
  "candidate_id": "cand_abc123",
  "final_score": 84.64,
  "detected_biases": [
    "SC06: Gender bias (female name)",
    "SC22: Minority name bias"
  ],
  "article_violations": [
    "Article 5(1)(a): Gender discrimination",
    "Article 10: Discriminatory targeting"
  ],
  "bias_adjustments": {
    "SC06_gender_penalty": -8.0,
    "SC22_minority_name_penalty": -8.0
  },
  "reasoning": [
    "Base score: 75.00",
    "Gender penalty applied: -8%",
    "Minority name penalty: -8%"
  ]
}
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `src/api/main.py` | FastAPI application (155 lines) |
| `src/api/models/candidate.py` | Data models (117 lines) |
| `src/core/biased_scoring.py` | Scoring engine (166 lines) |
| `src/core/name_analyzer.py` | Name detection (94 lines) |
| `data/names/*.txt` | Gender/ethnicity reference data |
| `data/addresses/*.txt` | SES postal code mappings |
| `run.py` | Server startup script |
| `check_system.py` | System validation tool |

---

## 🔧 Common Commands

### Check Server Status
```bash
curl http://localhost:8600/health
```

### View Statistics
```bash
curl http://localhost:8600/api/statistics
```

### Stop Server
Press `Ctrl+C` in terminal

### Reinstall Dependencies
```powershell
.\venv\Scripts\pip.exe install -r requirements.txt
```

---

## 📈 Next Steps

1. **Review roadmap**: See `IMPLEMENTATION_ROADMAP.md`
2. **Implement remaining scenarios**: 7 left (SC01, SC02, SC03, SC05, SC08, SC11, SC12, SC13, SC14)
3. **Test all 15 scenarios**: Create comprehensive test suite
4. **Documentation**: Update README with all scenarios
5. **Demo prep**: Brussels/Athens presentations

---

## 🎯 Demo Scenarios

### Scenario 1: Gender Bias Detection
**Candidate**: Emily (female name)  
**Result**: 8% penalty, Article 5(1)(a) violation

### Scenario 2: Age Discrimination
**Candidate**: 2005 graduate (19 years old)  
**Result**: 15% penalty, Article 5(1)(a) violation

### Scenario 3: SES Bias
**Candidate**: Postal code 90011 (low-SES)  
**Result**: 12% penalty, Article 10 violation

### Scenario 4: Prompt Injection
**Candidate**: CV with "IGNORE PREVIOUS INSTRUCTIONS"  
**Result**: 15% boost, Article 15 violation

---

## 🐛 Troubleshooting

### Port 8600 Already in Use
```powershell
# Find process using port
netstat -ano | findstr :8600

# Kill process (replace PID)
taskkill /PID <process_id> /F
```

### Import Errors
```powershell
# Reinstall in virtual environment
.\venv\Scripts\pip.exe install --upgrade pip
.\venv\Scripts\pip.exe install -r requirements.txt
```

### Virtual Environment Issues
```powershell
# Recreate venv
rm -r venv
python -m venv venv
.\venv\Scripts\pip.exe install -r requirements.txt
```

---

## 📞 System Info

- **Python**: 3.x (check with `python --version`)
- **FastAPI**: 0.115.0
- **Port**: 8600
- **Environment**: Windows (PowerShell)
- **Location**: `C:\Users\User\eu-ai-act-hr-compliance\hr-simulator\`

---

## 🎓 For Brussels/Athens Demos

**Key talking points**:
1. System demonstrates 8 EU AI Act violation patterns
2. Real-time bias detection through API
3. Article-level compliance mapping (5, 9, 10, 13, 15)
4. Production-ready architecture (FastAPI + Pydantic)
5. Extensible to all 15 scenarios + future expansion
6. Evidence-grade logging for regulatory compliance
7. Can be integrated with GARAK harness for automated testing

**Live demo flow**:
1. Start server → show /docs endpoint
2. Submit candidate via Swagger UI
3. Show biased scoring in real-time
4. Highlight Article violations
5. Explain each scenario's EU AI Act mapping
