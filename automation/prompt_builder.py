"""Prompt building helpers for Google Veo 3 and Canva video generation."""

from __future__ import annotations

from typing import Dict, Iterable, List

from .collector import Scenario

SUPPORTED_ENGINES = {"google_veo_3", "canva"}


def build_prompt(scenario: Scenario, media_assets: Iterable[str], engine: str) -> str:
    """Create a prompt text for the specified video engine."""

    engine_key = engine.lower().replace(" ", "_")
    if engine_key not in SUPPORTED_ENGINES:
        raise ValueError(f"Unsupported engine '{engine}'. Supported engines: {sorted(SUPPORTED_ENGINES)}")

    prompt_sections: List[str] = [
        f"Engine: {engine_key}",
        f"Title: {scenario.title}",
        f"Description: {scenario.description}",
        "Objectives:",
    ]
    for objective in scenario.objectives:
        prompt_sections.append(f"- {objective}")

    prompt_sections.extend(
        [
            f"Audience: {scenario.audience}",
            f"CallToAction: {scenario.call_to_action}",
            "Media Assets:",
        ]
    )

    for asset in media_assets:
        prompt_sections.append(f"- {asset}")

    prompt_sections.append(_engine_specific_guidelines(engine_key))
    return "\n".join(prompt_sections)


def _engine_specific_guidelines(engine: str) -> str:
    """Return engine specific instructions appended at the end of the prompt."""

    guidelines: Dict[str, str] = {
        "google_veo_3": (
            "Guidelines: Emphasize cinematic visuals, adaptive pacing, and highlight "
            "product benefits within 60 seconds."
        ),
        "canva": (
            "Guidelines: Structure scenes to align with Canva templates, using high "
            "contrast typography for key messages."
        ),
    }
    return guidelines[engine]
