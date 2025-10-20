"""Keyword research utilities for social platforms."""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Sequence

from automation.collector import Scenario


def _normalize_hints(value: object) -> Sequence[str]:
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    if isinstance(value, Iterable):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def generate_keywords(scenario: Scenario, platform_requirements: Dict[str, Dict[str, object]]) -> Dict[str, List[str]]:
    """Return a keyword list per platform derived from scenario objectives and hints."""

    base_terms = {scenario.title.lower(), scenario.audience.lower(), scenario.call_to_action.lower()}
    objective_terms = {obj.lower() for obj in scenario.objectives}

    keywords: Dict[str, List[str]] = defaultdict(list)
    for platform, hints in platform_requirements.items():
        platform_terms = set(base_terms)
        platform_terms.update(objective_terms)
        platform_terms.update({hint.lower() for hint in _normalize_hints(hints.get("must_include"))})
        filtered = sorted({term for term in platform_terms if len(term) > 3})
        keywords[platform] = filtered[:10]
    return dict(keywords)
