"""Utilities for gathering and validating automation inputs."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence
import csv
import json


@dataclass
class Scenario:
    """High-level description of the video campaign."""

    name: str
    goals: Sequence[str]
    target_audience: Sequence[str]
    tone: str
    platforms: Sequence[str]
    call_to_action: str


@dataclass
class MediaAsset:
    """Existing media referenced in the scenario."""

    asset_id: str
    description: str
    tags: Sequence[str]


class DataCollector:
    """Loads scenario and media information from disk."""

    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path

    def load_scenario(self, scenario_file: Path) -> Scenario:
        path = self.base_path / scenario_file
        with path.open("r", encoding="utf-8") as handle:
            raw = json.load(handle)
        return Scenario(
            name=raw["name"],
            goals=raw.get("goals", []),
            target_audience=raw.get("target_audience", []),
            tone=raw.get("tone", ""),
            platforms=raw.get("platforms", []),
            call_to_action=raw.get("call_to_action", ""),
        )

    def load_media_assets(self, media_file: Path) -> List[MediaAsset]:
        path = self.base_path / media_file
        with path.open("r", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            return [
                MediaAsset(
                    asset_id=row["asset_id"],
                    description=row.get("description", ""),
                    tags=[tag.strip() for tag in row.get("tags", "").split("|") if tag.strip()],
                )
                for row in reader
            ]

    @staticmethod
    def summarize_assets(assets: Iterable[MediaAsset]) -> str:
        """Return a human-readable summary of assets for prompt scaffolding."""

        lines = [
            f"{asset.asset_id}: {asset.description} (tags: {', '.join(asset.tags)})"
            for asset in assets
        ]
        return "\n".join(lines)
