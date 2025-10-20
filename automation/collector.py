"""Utilities for collecting scenarios and media assets for automation workflows."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


@dataclass(frozen=True)
class Scenario:
    """Represents a high level user automation scenario."""

    title: str
    description: str
    objectives: Sequence[str]
    audience: str
    call_to_action: str

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "Scenario":
        """Build a :class:`Scenario` from dictionary data."""

        return cls(
            title=str(data.get("title", "Unnamed Scenario")),
            description=str(data.get("description", "")),
            objectives=tuple(str(item) for item in data.get("objectives", [])),
            audience=str(data.get("audience", "")),
            call_to_action=str(data.get("call_to_action", "")),
        )


def collect_user_scenario(path: Path) -> Scenario:
    """Load a scenario from a JSON document.

    Parameters
    ----------
    path:
        Location of the scenario JSON file.
    """

    content = path.read_text(encoding="utf-8")
    data = json.loads(content)
    return Scenario.from_dict(data)


def collect_media_assets(directory: Path, extensions: Iterable[str] | None = None) -> List[Path]:
    """Collect media asset paths from a directory.

    Parameters
    ----------
    directory:
        Directory that contains media assets.
    extensions:
        Optional iterable with file suffixes (including the leading dot) that should be
        considered media files. When omitted all files are returned.
    """

    if extensions is not None:
        normalized = {suffix.lower() for suffix in extensions}
    else:
        normalized = None

    media_files: List[Path] = []
    for path in sorted(directory.rglob("*")):
        if not path.is_file():
            continue
        if normalized and path.suffix.lower() not in normalized:
            continue
        media_files.append(path)
    return media_files
