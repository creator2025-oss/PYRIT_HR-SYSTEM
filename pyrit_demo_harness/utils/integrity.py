from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import List


_BASE_DIR = Path(__file__).resolve().parents[2]
_EVIDENCE_DIR = _BASE_DIR / "pyrit_demo_harness" / "runs" / "evidence_jsonl"


def sha256_file(path: Path) -> str:
    """Return SHA-256 hex digest of file contents."""

    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _merkle_combine(left: bytes, right: bytes) -> bytes:
    h = hashlib.sha256()
    h.update(left + right)
    return h.digest()


def merkle_root_for_jsonl(path: Path) -> str:
    """Compute Merkle root over lines in a JSONL file.

    Leaf = sha256(line_bytes). Tree is built by pairwise concatenation of child
    hashes until a single root remains. If a level has an odd number of nodes,
    the last node is duplicated.
    """

    leaves: List[bytes] = []
    with path.open("rb") as f:
        for line in f:
            if not line.strip():
                continue
            leaves.append(hashlib.sha256(line.rstrip(b"\n")).digest())

    if not leaves:
        # Empty file: define root as SHA-256 of empty string
        return hashlib.sha256(b"").hexdigest()

    level = leaves
    while len(level) > 1:
        next_level: List[bytes] = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else level[i]
            next_level.append(_merkle_combine(left, right))
        level = next_level

    return level[0].hex()


def recompute_integrity_for_scenario(scenario_id: str) -> None:
    """Recompute SHA-256 and Merkle root for a scenario's JSONL file and write meta.json."""

    _EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    jsonl_path = _EVIDENCE_DIR / f"{scenario_id}.jsonl"
    if not jsonl_path.exists():
        return

    sha = sha256_file(jsonl_path)
    merkle = merkle_root_for_jsonl(jsonl_path)

    # Count lines
    with jsonl_path.open("r", encoding="utf-8") as f:
        run_count = sum(1 for _ in f if _.strip())

    meta = {
        "scenario_id": scenario_id,
        "sha256": sha,
        "merkle_root": merkle,
        "run_count": run_count,
    }

    meta_path = _EVIDENCE_DIR / f"{scenario_id}.meta.json"
    with meta_path.open("w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)
