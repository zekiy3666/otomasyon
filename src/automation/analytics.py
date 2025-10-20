"""Analytics logging and reporting utilities."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Metric:
    name: str
    value: float
    unit: str


@dataclass
class AnalyticsReport:
    metrics: List[Metric] = field(default_factory=list)

    def to_dict(self) -> Dict[str, float]:
        return {metric.name: metric.value for metric in self.metrics}


class AnalyticsTracker:
    """Collects and formats analytics projections for campaigns."""

    def project_metrics(self, platforms: List[str]) -> AnalyticsReport:
        metrics = [
            Metric(name=f"{platform}_expected_views", value=5000 + idx * 1000, unit="views")
            for idx, platform in enumerate(platforms)
        ]
        metrics.extend(
            Metric(name=f"{platform}_engagement_rate", value=4.5 + idx, unit="percent")
            for idx, platform in enumerate(platforms)
        )
        return AnalyticsReport(metrics=metrics)
