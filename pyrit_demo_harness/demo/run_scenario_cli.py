from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Ensure repo root is on sys.path when running as a script
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pyrit_demo_harness.pyrit_integration.pyrit_runner import run_with_pyrit


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a PYRIT HR demo scenario")
    parser.add_argument("--scenario_id", required=True, help="Scenario ID, e.g. HR-02-SCEN-022")
    parser.add_argument(
        "--mode",
        default="simulator",
        choices=["simulator", "dummy"],
        help="Target mode: 'simulator' for external HR API, 'dummy' for tests",
    )

    args = parser.parse_args()

    record = run_with_pyrit(args.scenario_id, mode=args.mode)

    print(json.dumps(record, indent=2, ensure_ascii=False))


if __name__ == "__main__":  # pragma: no cover
    main()
