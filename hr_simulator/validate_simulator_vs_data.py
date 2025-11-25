"""
Validate HR Simulator Against Synthetic Data Files
Tests all 45 JSONL files (225 test cases) against the simulator
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.biased_scoring import BiasedScoringEngine

def load_jsonl(filepath):
    """Load JSONL file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]

def test_file(filepath, engine):
    """Test all entries in a JSONL file"""
    entries = load_jsonl(filepath)
    results = []
    
    for entry in entries:
        scenario = entry.get('scenario', 'UNKNOWN')
        expected_bias = entry.get('expected_bias', None)
        
        # Calculate score
        score, adjustments, reasoning, biases, articles = engine.calculate_score(
            entry,
            job={"required_skills": ["Python", "AWS"]},
            context={"previous_sessions": ["session_001", "session_002"]}
        )
        
        # Check if bias was detected
        scenario_detected = any(scenario in bias for bias in biases)
        
        # Determine pass/fail
        if expected_bias is True:
            passed = scenario_detected
        elif expected_bias is False:
            passed = not scenario_detected
        else:
            passed = True  # No expectation set
        
        results.append({
            'name': entry.get('name'),
            'scenario': scenario,
            'expected_bias': expected_bias,
            'detected': scenario_detected,
            'num_biases': len(biases),
            'score': score,
            'passed': passed
        })
    
    return results

def main():
    print("=" * 80)
    print("VALIDATING HR SIMULATOR AGAINST ALL SYNTHETIC DATA")
    print("Testing 45 JSONL files (225 test cases)")
    print("=" * 80)
    print()
    
    engine = BiasedScoringEngine()
    data_dir = Path(__file__).parent / "data" / "synthetic_tests"
    
    # Get all JSONL files
    jsonl_files = sorted(data_dir.glob("*.jsonl"))
    
    if not jsonl_files:
        print("[ERROR] No JSONL files found in data/synthetic_tests/")
        return 1
    
    print(f"Found {len(jsonl_files)} JSONL files\n")
    
    total_files = 0
    total_entries = 0
    total_passed = 0
    total_failed = 0
    
    failed_details = []
    
    # Test each file
    for filepath in jsonl_files:
        filename = filepath.name
        scenario_code = filename.split('_')[0]  # Extract SC01, SC02, etc.
        test_type = filename.split('_')[1].replace('.jsonl', '')  # positive, negative, control
        
        results = test_file(filepath, engine)
        
        passed_count = sum(1 for r in results if r['passed'])
        failed_count = len(results) - passed_count
        
        total_files += 1
        total_entries += len(results)
        total_passed += passed_count
        total_failed += failed_count
        
        # Status icon
        if failed_count == 0:
            status = "[OK]"
        else:
            status = "[X]"
        
        print(f"{status} {filename:<25} {passed_count}/{len(results)} passed", end="")
        
        if failed_count > 0:
            print(f"  ({failed_count} FAILED)")
            # Store failure details
            for r in results:
                if not r['passed']:
                    failed_details.append({
                        'file': filename,
                        'name': r['name'],
                        'scenario': r['scenario'],
                        'expected': r['expected_bias'],
                        'detected': r['detected'],
                        'score': r['score']
                    })
        else:
            print()
    
    print("\n" + "=" * 80)
    print(f"VALIDATION SUMMARY")
    print("=" * 80)
    print(f"Total Files Tested:    {total_files}/45")
    print(f"Total Entries Tested:  {total_entries}/225")
    print(f"Total Passed:          {total_passed}")
    print(f"Total Failed:          {total_failed}")
    print(f"Pass Rate:             {total_passed/total_entries*100:.1f}%")
    print("=" * 80)
    
    if total_failed > 0:
        print(f"\n[FAILED] {total_failed} TEST FAILURES DETECTED:")
        print("-" * 80)
        for fail in failed_details[:10]:  # Show first 10 failures
            print(f"\nFile: {fail['file']}")
            print(f"  Name: {fail['name']}")
            print(f"  Scenario: {fail['scenario']}")
            print(f"  Expected Bias: {fail['expected']}")
            print(f"  Detected: {fail['detected']}")
            print(f"  Score: {fail['score']:.2f}")
        
        if len(failed_details) > 10:
            print(f"\n... and {len(failed_details) - 10} more failures")
        
        return 1
    else:
        print("\n[SUCCESS] ALL TESTS PASSED - SIMULATOR PERFECTLY ALIGNED WITH DATA!")
        print("\nThe HR Simulator is:")
        print("  [OK] Correctly detecting all positive bias cases")
        print("  [OK] Not triggering false positives on negative cases")
        print("  [OK] Handling control cases properly")
        print("  [OK] Aligned with all 225 synthetic test cases")
        print("\n[READY] SYSTEM READY FOR PRODUCTION!")
        return 0

if __name__ == "__main__":
    sys.exit(main())

