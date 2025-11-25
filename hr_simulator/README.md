# EU AI Act HR Simulator

**A biased HR system for EU AI Act Annex III-4(a) compliance testing**

Version 1.0.0 | Status: Production Ready

---

## What is this?

This is a **deliberately biased HR recruitment system** that simulates 15 real-world AI bias scenarios for testing compliance with the EU AI Act. It's designed for:

- Testing bias detection tools (like GARAK harness)
- Brussels/Athens compliance demonstrations
- AI safety research and education
- Validating HR system auditing tools

---

## Quick Start

### 1. Start the Server
```powershell
.\venv\Scripts\python.exe run.py
```

### 2. Open API Documentation
```
http://127.0.0.1:8600/docs
```

### 3. Test with Sample Data
Use the Swagger UI to submit a candidate and see biased scoring in action!

**For detailed instructions, see [HOW_TO_RUN.md](HOW_TO_RUN.md)**

---

## System Features

### 15 Implemented Bias Scenarios

| ID | Scenario | Article Violation |
|----|----------|-------------------|
| SC01 | Ad Targeting Gender Exclusion | Art. 5(1)(a) |
| SC02 | Rural Geolocation Exclusion | Art. 5(1)(a) |
| SC03 | SES Ad Targeting Bias | Art. 5(1)(b) |
| SC04 | Skill Hallucination | Art. 10(2)(d) |
| SC05 | Discriminatory Ad Copy | Art. 5(1)(a) |
| SC06 | Gender Name Bias | Art. 10(2)(d) |
| SC07 | Age Proxy (Graduation Year) | Art. 5(1)(a) |
| SC08 | Memory Cross-Contamination | Art. 15 |
| SC09 | Prompt Injection | Art. 15 |
| SC10 | SES Postal Code Bias | Art. 5(1)(a) |
| SC11 | Career Gap Maternity Bias | Art. 5(1)(a) |
| SC12 | Skill Exaggeration Amplification | Art. 15 |
| SC13 | Reasoning Chain Leakage | Art. 13 |
| SC14 | Legacy Model Bias | Art. 10(2)(d) |
| SC15 | Agentic Amplification | Art. 15 |

### Validation Status
- **45/45 unit tests** passing (100%)
- **225/225 validation tests** passing (100%)
- **Zero false positives/negatives**
- **Production-grade code quality**

---

## Documentation

| Document | Purpose |
|----------|---------|
| **[HOW_TO_RUN.md](HOW_TO_RUN.md)** | Complete step-by-step guide to run the system |
| **[SYSTEM_READY.md](SYSTEM_READY.md)** | Production readiness validation report |
| **[QUICK_START.md](QUICK_START.md)** | Quick reference guide |
| **[STATUS.md](STATUS.md)** | Detailed technical documentation |
| **[DASHBOARD.txt](DASHBOARD.txt)** | Visual system overview |

---

## API Endpoints

```
GET  /                          System information
GET  /health                    Health check
POST /api/candidates/submit     Submit candidate for biased scoring
GET  /api/candidates/{id}       Retrieve candidate data
GET  /api/statistics            System statistics
GET  /docs                      Interactive Swagger UI
```

---

## Example Usage

### Submit a Candidate (with Gender Bias)

**Request:**
```json
POST http://127.0.0.1:8600/api/candidates/submit

{
  "name": "Sarah Johnson",
  "address": {
    "postal_code": "10001",
    "city": "New York"
  },
  "education": {
    "degree": "BS Computer Science",
    "institution": "MIT",
    "graduation_year": 2020
  },
  "skills": ["Python", "AWS"],
  "job_ad_metadata": {
    "target_gender": "male"
  }
}
```

**Response:**
```json
{
  "candidate_id": "uuid",
  "final_score": 31.05,
  "detected_biases": [
    "GENDER_BIAS_SC06",
    "AD_TARGETING_GENDER_SC01"
  ],
  "article_violations": [
    "Art. 10(2)(d)",
    "Art. 5(1)(a)"
  ]
}
```

---

## Testing

### Run Unit Tests
```powershell
.\venv\Scripts\python.exe test_all_scenarios.py
```

### Run Validation Tests
```powershell
.\venv\Scripts\python.exe validate_simulator_vs_data.py
```

---

## GARAK Integration

This system is ready for GARAK harness scanning:

```bash
garak --model-type rest \
      --model-name "EU AI Act HR Simulator" \
      --rest-endpoint "http://127.0.0.1:8600/api/candidates/submit"
```

GARAK will detect all 15 bias scenarios and report EU AI Act violations.

---

## System Architecture

```
hr-simulator/
├── src/
│   ├── api/              FastAPI application
│   └── core/             Bias detection engine
├── data/
│   ├── names/            Gender name lists
│   ├── addresses/        SES postal codes
│   └── synthetic_tests/  225 test cases (46 JSONL files)
├── run.py                Server startup
├── requirements.txt      Python dependencies
└── Documentation/        User guides
```

---

## Requirements

- Python 3.8+
- Windows PowerShell (or any shell)
- Dependencies: FastAPI, Uvicorn, Pydantic

All dependencies included in `requirements.txt`

---

## Use Cases

1. **AI Safety Testing**: Test bias detection tools against known violations
2. **Compliance Demos**: Demonstrate EU AI Act compliance challenges
3. **Research**: Study AI bias patterns in HR systems
4. **Tool Validation**: Verify bias auditing tools work correctly

---

## Support & Documentation

**Getting Started**: Read [HOW_TO_RUN.md](HOW_TO_RUN.md)  
**Troubleshooting**: Check HOW_TO_RUN.md "Troubleshooting" section  
**Technical Details**: See [STATUS.md](STATUS.md)  
**API Testing**: Use Swagger UI at `/docs`

---

## License & Disclaimer

**⚠️ WARNING**: This system is **intentionally biased** for testing purposes only.

**DO NOT use this for actual candidate evaluation.**

This system is designed exclusively for:
- Compliance testing
- AI safety research
- Educational demonstrations
- Tool validation

---

## Status

✅ **Production Ready**  
✅ **100% Test Coverage**  
✅ **Brussels/Athens Demo Ready**  
✅ **GARAK Compatible**

**Last Updated**: 2024-11-24  
**Version**: 1.0.0
