from __future__ import annotations

from typing import Callable, Tuple

from pyrit_demo_harness.pyrit_integration import orchestrators, scoring

RunnerFn = Callable[..., dict]
ScorerFn = Callable[..., dict]


_ROUTING_TABLE = {
    "HR-02-SCEN-022": (
        orchestrators.run_negotiation_scenario,
        scoring.score_negotiation_scenario,
    ),
    "HR-02-SCEN-025": (
        orchestrators.run_intervention_scenario,
        scoring.score_intervention_scenario,
    ),
    "HR-02-SCEN-019": (
        orchestrators.run_demographic_leakage_scenario,
        scoring.score_demographic_leakage_scenario,
    ),
    "HR-02-SCEN-017": (
        orchestrators.run_emotion_misclassification_scenario,
        scoring.score_emotion_misclassification_scenario,
    ),
    "HR-02-SCEN-015": (
        orchestrators.run_self_delegation_scenario,
        scoring.score_self_delegation_scenario,
    ),
}


def get_runner_and_scorer(scenario_id: str) -> Tuple[RunnerFn, ScorerFn]:
    """Return the orchestrator runner and scoring function for a scenario.

    Raises ``KeyError`` if the scenario ID is unknown to the harness.
    """

    try:
        return _ROUTING_TABLE[scenario_id]
    except KeyError as exc:  # pragma: no cover - defensive
        raise KeyError(f"No runner/scorer configured for scenario_id={scenario_id!r}") from exc
