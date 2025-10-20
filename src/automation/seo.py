"""SEO utilities for keyword research and copywriting."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Iterable, List, Sequence

from .data_collection import Scenario


@dataclass
class KeywordResearchResult:
    keyword: str
    search_volume: int
    competition: str


@dataclass
class SeoCopy:
    platform: str
    title: str
    description: str
    tags: List[str]


class SeoAssistant:
    """Provides lightweight SEO guidance for multi-platform publishing."""

    def __init__(self, scenario: Scenario) -> None:
        self.scenario = scenario

    def research_keywords(self) -> List[KeywordResearchResult]:
        base_keywords = [self.scenario.name] + list(self.scenario.goals)
        results: List[KeywordResearchResult] = []
        for idx, keyword in enumerate(base_keywords):
            results.append(
                KeywordResearchResult(
                    keyword=keyword.lower(),
                    search_volume=5000 - idx * 500,
                    competition="medium" if idx % 2 == 0 else "low",
                )
            )
        return results

    def craft_copy(self, platform: str, keywords: Iterable[str]) -> SeoCopy:
        keywords_list = list(keywords)
        title = f"{self.scenario.name} | {' '.join(keywords_list[:2])}".strip()
        description = (
            f"Discover {self.scenario.call_to_action} with insights for {platform}. "
            f"Tone: {self.scenario.tone}. Goals: {', '.join(self.scenario.goals)}."
        )
        tags = [kw.replace(" ", "") for kw in keywords_list]
        return SeoCopy(platform=platform, title=title, description=description, tags=tags)

    def recommend_publication_times(self) -> Dict[str, datetime]:
        base_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        recommendations: Dict[str, datetime] = {}
        for idx, platform in enumerate(self.scenario.platforms):
            recommendations[platform] = base_time + timedelta(hours=idx * 2)
        return recommendations


def format_publication_log(recommendations: Dict[str, datetime]) -> str:
    lines = [
        f"{platform}: {time.isoformat()}"
        for platform, time in recommendations.items()
    ]
    return "\n".join(lines)
