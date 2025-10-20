"""Scheduling helpers for publishing automation."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List


@dataclass
class ScheduleItem:
    platform: str
    publish_time: datetime
    reminder_time: datetime


class Scheduler:
    """Generates publication schedules and reminders."""

    def __init__(self, buffer_minutes: int = 30) -> None:
        self.buffer = timedelta(minutes=buffer_minutes)

    def build_schedule(self, recommendations: Dict[str, datetime]) -> List[ScheduleItem]:
        schedule: List[ScheduleItem] = []
        for platform, publish_time in recommendations.items():
            reminder = publish_time - self.buffer
            schedule.append(ScheduleItem(platform=platform, publish_time=publish_time, reminder_time=reminder))
        return schedule

    @staticmethod
    def format_schedule(schedule: List[ScheduleItem]) -> str:
        return "\n".join(
            f"{item.platform}: publish at {item.publish_time.isoformat()} (remind at {item.reminder_time.isoformat()})"
            for item in schedule
        )
