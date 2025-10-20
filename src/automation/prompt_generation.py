"""Prompt construction utilities for external creative tools."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Sequence

from .data_collection import MediaAsset, Scenario


@dataclass
class Prompt:
    """Represents a prompt for a creative tool."""

    tool: str
    payload: Dict[str, str]


class PromptBuilder:
    """Creates structured prompts for video generation services."""

    def __init__(self, scenario: Scenario, assets: Iterable[MediaAsset]):
        self.scenario = scenario
        self.assets = list(assets)

    def build_veo_prompt(self) -> Prompt:
        """Return a detailed prompt for Google Veo 3."""

        payload = {
            "narrative": self._compose_narrative(),
            "style": f"Tone: {self.scenario.tone}",
            "call_to_action": self.scenario.call_to_action,
            "references": self._format_asset_reference(),
        }
        return Prompt(tool="google_veo_3", payload=payload)

    def build_canva_prompt(self) -> Prompt:
        """Return a detailed prompt for Canva video templates."""

        payload = {
            "project_name": self.scenario.name,
            "visual_theme": ", ".join(self.scenario.goals),
            "audience": ", ".join(self.scenario.target_audience),
            "assets": self._format_asset_reference(separator="; "),
        }
        return Prompt(tool="canva", payload=payload)

    def build_all(self) -> Sequence[Prompt]:
        return [self.build_veo_prompt(), self.build_canva_prompt()]

    def _compose_narrative(self) -> str:
        lines = [f"Goal: {goal}" for goal in self.scenario.goals]
        audience = ", ".join(self.scenario.target_audience) or "broad digital audience"
        lines.append(f"Audience: {audience}")
        lines.append(f"CTA: {self.scenario.call_to_action}")
        return "\n".join(lines)

    def _format_asset_reference(self, separator: str = "\n") -> str:
        if not self.assets:
            return "No additional assets provided"
        return separator.join(
            f"{asset.asset_id}: {asset.description} [tags: {', '.join(asset.tags)}]"
            for asset in self.assets
        )
