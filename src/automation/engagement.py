"""Engagement follow-up planning utilities."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List


@dataclass
class EngagementTask:
    platform: str
    action: str
    scheduled_for: datetime


class EngagementPlanner:
    """Creates follow-up actions such as comment moderation or live sessions."""

    def __init__(self, follow_up_delay_hours: int = 24) -> None:
        self.follow_up_delay = timedelta(hours=follow_up_delay_hours)

    def plan_tasks(self, platforms: List[str], publish_times: Dict[str, datetime]) -> List[EngagementTask]:
        tasks: List[EngagementTask] = []
        for platform in platforms:
            publish_time = publish_times.get(platform)
            if publish_time is None:
                continue
            tasks.append(
                EngagementTask(
                    platform=platform,
                    action="Respond to top comments",
                    scheduled_for=publish_time + self.follow_up_delay,
                )
            )
            tasks.append(
                EngagementTask(
                    platform=platform,
                    action="Share highlights on stories",
                    scheduled_for=publish_time + self.follow_up_delay / 2,
                )
            )
        return tasks

    @staticmethod
    def format_tasks(tasks: List[EngagementTask]) -> str:
        return "\n".join(
            f"{task.platform}: {task.action} at {task.scheduled_for.isoformat()}"
            for task in tasks
        )
