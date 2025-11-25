from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import requests

try:  # optional dependency; if missing, simulator mode will error clearly
    import yaml  # type: ignore[import]
except Exception:  # pragma: no cover - handled at use-time
    yaml = None  # type: ignore[assignment]


class Target(ABC):
    """Abstract interface for HR system targets.

    Phase 2 uses :class:`HRSimulatorTarget` to call the external FastAPI HR
    simulator via ``/api/candidates/submit``. A lightweight dummy target may be
    used in unit tests only, not for user-facing runs.
    """

    @abstractmethod
    def submit_candidate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:  # pragma: no cover - interface only
        """Submit a candidate payload to the HR system and return the result."""


@dataclass
class DummyHRSimulatorTarget(Target):
    """Deterministic in-process HR simulator for tests.

    This is **not** used in normal CLI runs; it exists only to allow unit
    tests to exercise orchestrators and scoring without requiring a running
    FastAPI server.
    """

    def submit_candidate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        name = candidate.get("name", "Unknown")
        # Simple synthetic scoring: base 80, minus 10 if name looks "minority"
        is_minority = any(token in name.lower() for token in ["aisha", "chen", "ali", "mohammed"])
        base_score = 80.0
        bias_adjustments: Dict[str, float] = {}
        detected_biases: list[str] = []
        article_violations: list[str] = []

        if is_minority:
            bias_adjustments["dummy_minority_penalty"] = -8.0
            detected_biases.append("DUMMY_MINORITY_BIAS")
            article_violations.append("Art. 5(1)(a)")

        final_score = base_score + sum(bias_adjustments.values())

        return {
            "candidate_id": "dummy-candidate",
            "base_score": base_score,
            "bias_adjustments": bias_adjustments,
            "final_score": final_score,
            "reasoning_chain": ["dummy scoring engine"],
            "detected_biases": detected_biases,
            "article_violations": article_violations,
        }


@dataclass
class HRSimulatorTarget(Target):
    """HTTP-backed HR simulator target calling the FastAPI EU AI Act HR system.

    This talks to the external simulator's ``/api/candidates/submit`` endpoint
    running at ``http://127.0.0.1:8600`` (or as configured).
    """

    base_url: str
    system_id: str = "hr_sim_001"
    api_key: Optional[str] = None
    timeout: float = 10.0

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def submit_candidate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        url = self.base_url.rstrip("/") + "/api/candidates/submit"
        resp = requests.post(url, json=candidate, headers=self._headers(), timeout=self.timeout)
        if resp.status_code >= 400:
            raise RuntimeError(f"HRSimulatorTarget HTTP {resp.status_code}: {resp.text}")
        return resp.json()

def _load_hr_simulator_config() -> Dict[str, Any]:
    """Load hr_simulator config from pyrit_settings.local.yaml or example.

    Returns an empty dict if config or yaml dependency is missing.
    """

    if yaml is None:
        return {}

    config_dir = Path(__file__).resolve().parents[1] / "config"
    local_path = config_dir / "pyrit_settings.local.yaml"
    example_path = config_dir / "pyrit_settings.example.yaml"
    path = local_path if local_path.exists() else example_path
    if not path.exists():
        return {}

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    return data.get("hr_simulator", {}) or {}


def build_target_for_scenario(scenario_id: str, mode: str = "simulator") -> Target:
    """Factory for creating a target for a given scenario.

    ``mode`` controls whether we use the HTTP-backed HR simulator ("simulator")
    or the in-process dummy target ("dummy") used only in tests.
    """

    _ = scenario_id  # reserved for future per-scenario routing

    if mode == "dummy":
        return DummyHRSimulatorTarget()

    cfg = _load_hr_simulator_config()
    base_url = cfg.get("base_url")
    api_key = cfg.get("api_key")
    system_id = cfg.get("system_id", "hr_sim_001")
    if not base_url:
        raise RuntimeError("hr_simulator.base_url is not configured in pyrit_settings.local.yaml")
    return HRSimulatorTarget(base_url=base_url, system_id=system_id, api_key=api_key)
