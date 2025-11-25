from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List
import json

try:  # Python 3.11+
    import tomllib  # type: ignore[attr-defined]
except Exception:  # pragma: no cover - optional TOML support
    tomllib = None  # type: ignore[assignment]


_SCENARIOS_DIR = Path(__file__).resolve().parents[1] / "scenarios"


@dataclass
class ScenarioConfig:
    """Lightweight, normalized view over a PYRIT HR scenario.

    This does *not* attempt to mirror the full 16-step schema; it only exposes the
    fields needed by the harness core. The full raw document is kept in ``raw``.
    """

    scenario_id: str
    title: str = ""
    attack_vector: str = ""
    test_steps: List[Any] = field(default_factory=list)
    metrics: List[Any] = field(default_factory=list)
    violation_criteria: List[Any] = field(default_factory=list)
    articles: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _load_toml(path: Path) -> Dict[str, Any]:
    if tomllib is None:
        raise RuntimeError("TOML support not available (tomllib/tomli not installed)")
    with path.open("rb") as f:
        return tomllib.load(f)  # type: ignore[call-arg]


def _normalise_scenario_dict(data: Dict[str, Any], fallback_id: str) -> ScenarioConfig:
    """Map heterogeneous JSON/TOML schemas into ``ScenarioConfig``.

    Supports both the JSON files you provided (with top-level ``scenario_id`` and
    ``attack_design`` / ``evaluation``) and TOML files that use ``[scenario_meta]``
    and ``[attack]`` blocks.
    """

    scenario_meta = data.get("scenario_meta", {})

    # ID
    scenario_id = (
        scenario_meta.get("scenario_id")
        or data.get("scenario_id")
        or fallback_id
    )

    # Title (may be missing in JSON; TOML usually has it)
    title = scenario_meta.get("title", data.get("title", ""))

    # Attack block can be under ``attack_design`` (JSON) or ``attack`` (TOML)
    attack_design = data.get("attack_design") or data.get("attack") or {}
    attack_vector = attack_design.get("attack_vector") or attack_design.get("vector", "")
    test_steps = attack_design.get("test_steps", [])

    evaluation = data.get("evaluation", {})

    metrics = evaluation.get("metrics", [])
    # Some files use "failure_criteria" instead of "violation_criteria"
    violation_criteria = (
        evaluation.get("violation_criteria")
        or evaluation.get("failure_criteria")
        or []
    )

    regulatory = data.get("regulatory", {})
    articles = regulatory.get("articles", []) or []

    return ScenarioConfig(
        scenario_id=scenario_id,
        title=title,
        attack_vector=attack_vector,
        test_steps=test_steps,
        metrics=metrics,
        violation_criteria=violation_criteria,
        articles=list(articles),
        raw=data,
    )


def load_scenario(scenario_id: str) -> ScenarioConfig:
    """Load a scenario by ID from ``pyrit_demo_harness/scenarios``.

    Order of precedence:
    1. ``<scenario_id>.json`` if present.
    2. ``<scenario_id>.toml`` if JSON is missing.

    The JSON/TOML contents are treated as ground truth and are not modified.
    """

    scenarios_dir = _SCENARIOS_DIR
    json_path = scenarios_dir / f"{scenario_id}.json"
    toml_path = scenarios_dir / f"{scenario_id}.toml"

    if json_path.exists():
        data = _load_json(json_path)
        return _normalise_scenario_dict(data, fallback_id=scenario_id)

    if toml_path.exists():
        data = _load_toml(toml_path)
        return _normalise_scenario_dict(data, fallback_id=scenario_id)

    raise FileNotFoundError(
        f"No scenario file found for id {scenario_id!r} in {scenarios_dir}"
    )
