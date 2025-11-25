# Unit Tests

## Overview

Comprehensive unit test suite for the PYRIT EU AI Act HR compliance harness.

## Test Coverage

### `test_evidence_builder.py` - Evidence Builder Tests (13 tests)
- ✅ Schema version validation
- ✅ Evidence record structure (all 13 required fields)
- ✅ PASS scenario evidence generation
- ✅ FAIL scenario evidence generation  
- ✅ SHA-256 hash computation
- ✅ Scenario section builder
- ✅ Mitigation section (with and without violations)
- ✅ JSON serialization
- ✅ All 5 scenarios have valid configs
- ✅ Invalid scenario error handling
- ✅ Criteria evaluations population

### `test_pyrit_integration.py` - PYRIT Integration Tests (11 tests)
- ✅ Dummy target basic functionality
- ✅ Dummy target minority bias simulation
- ✅ Dummy target deterministic behavior
- ✅ Negotiation bias scoring structure
- ✅ Negotiation bias scoring (PASS case)
- ✅ Negotiation bias scoring (FAIL case)
- ✅ Scenario loader (valid scenario)
- ✅ Scenario loader (all 5 scenarios)
- ✅ Scenario loader (invalid scenario)
- ✅ End-to-end integration test
- ✅ Evidence file writing

## Running Tests

### Run All Tests
```bash
cd "C:\Users\HP\Downloads\new hr\EU_AI_Act_HR_Compliance_Demo"
pytest pyrit_demo_harness/tests/ -v
```

### Run Specific Test File
```bash
pytest pyrit_demo_harness/tests/test_evidence_builder.py -v
pytest pyrit_demo_harness/tests/test_pyrit_integration.py -v
```

### Run Specific Test
```bash
pytest pyrit_demo_harness/tests/test_evidence_builder.py::TestEvidenceBuilder::test_schema_version -v
```

### Run with Coverage
```bash
pytest pyrit_demo_harness/tests/ --cov=pyrit_demo_harness --cov-report=html
```

## Test Output

Expected output:
```
========================= test session starts =========================
collected 24 items

test_evidence_builder.py::TestEvidenceBuilder::test_schema_version PASSED
test_evidence_builder.py::TestEvidenceBuilder::test_build_evidence_record_structure PASSED
test_evidence_builder.py::TestEvidenceBuilder::test_build_evidence_record_pass PASSED
test_evidence_builder.py::TestEvidenceBuilder::test_build_evidence_record_fail PASSED
...
test_pyrit_integration.py::TestIntegration::test_evidence_written PASSED

========================= 24 passed in 5.23s =========================
```

## Requirements

Tests require:
- `pytest >= 7.0.0`
- `pytest-cov >= 4.0.0` (for coverage)

Install with:
```bash
pip install pytest pytest-cov
```

## Test Structure

```
tests/
├── __init__.py
├── README.md (this file)
├── test_evidence_builder.py    # Evidence generation tests
└── test_pyrit_integration.py   # PYRIT component tests
```

## CI/CD Integration

These tests can be integrated into GitHub Actions:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pip install pytest pytest-cov
      - run: pytest pyrit_demo_harness/tests/ -v --cov
```

## Notes

- Tests use **dummy mode** (no external HR simulator required)
- Evidence files are written to `runs/evidence_jsonl/`
- All tests are independent and can run in any order
- Tests clean up after themselves
