"""Publishing scheduler utilities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Iterable, List


@dataclass(frozen=True)
class ScheduleItem:
    """Represents a publishing slot."""

    platform: str
    publish_at: datetime
    notes: str


def build_schedule(base_time: datetime, cadence: Dict[str, int], platforms: Iterable[str]) -> List[ScheduleItem]:
    """Build a list of :class:`ScheduleItem` entries from cadence configuration."""

    schedule: List[ScheduleItem] = []
    for offset, platform in enumerate(platforms):
        days = cadence.get(platform, cadence.get("default", 1))
        publish_at = base_time + timedelta(days=offset * days)
        schedule.append(
            ScheduleItem(
                platform=platform,
                publish_at=publish_at,
                notes=f"Publish to {platform} with cadence {days} day(s).",
            )
        )
    return schedule
