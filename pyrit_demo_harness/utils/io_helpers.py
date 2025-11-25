from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any

from pyrit_demo_harness.utils.integrity import recompute_integrity_for_scenario


_BASE_DIR = Path(__file__).resolve().parents[2]
_EVIDENCE_DIR = _BASE_DIR / "pyrit_demo_harness" / "runs" / "evidence_jsonl"


def write_evidence_record(scenario_id: str, record: Dict[str, Any]) -> None:
    """Append a JSON line for the scenario and recompute integrity metadata."""

    _EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    jsonl_path = _EVIDENCE_DIR / f"{scenario_id}.jsonl"

    with jsonl_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    recompute_integrity_for_scenario(scenario_id)
