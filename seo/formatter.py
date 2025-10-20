"""SEO metadata formatting helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List

# Platform requirements table reference (summarised from internal playbook):
#   Platform | Title limit | Description limit | Hashtags | Notes
#   ---------|-------------|-------------------|----------|--------------------------------------------
#   YouTube  | 100 chars   | 5000 chars        | 15       | Keep CTA early, include 2 branded keywords
#   Instagram| 150 chars   | 2200 chars        | 30       | First 125 chars must hook, mix emoji sparingly
#   TikTok   | 150 chars   | 2200 chars        | 33       | Focus on challenges + trending sound mentions
#   Facebook | 100 chars   | 63206 chars       | 30       | Lead with value prop, include location tag


@dataclass
class Metadata:
    """Metadata container for a platform."""

    title: str
    description: str
    keywords: List[str]


def format_metadata(
    platform: str,
    scenario_title: str,
    scenario_description: str,
    keywords: Iterable[str],
    requirements: Dict[str, Dict[str, int | str]],
) -> Metadata:
    """Format metadata according to platform requirements."""

    platform_key = platform.lower()
    requirement = requirements.get(platform_key, {})
    title_limit = int(requirement.get("title_limit", 100))
    description_limit = int(requirement.get("description_limit", 500))
    hashtag_limit = int(requirement.get("hashtag_limit", 10))

    title = scenario_title[:title_limit]
    description = scenario_description[:description_limit]

    keyword_list = list(keywords)[:hashtag_limit]
    hashtag_string = " ".join(f"#{kw.replace(' ', '')}" for kw in keyword_list)
    description_with_tags = f"{description}\n\n{hashtag_string}".strip()

    return Metadata(title=title, description=description_with_tags, keywords=keyword_list)
