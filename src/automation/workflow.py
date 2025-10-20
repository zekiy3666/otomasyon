"""End-to-end orchestration for the content automation pipeline."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List

from .analytics import AnalyticsTracker
from .data_collection import DataCollector, MediaAsset, Scenario
from .editing_export import ExportResult, Exporter
from .engagement import EngagementPlanner, EngagementTask
from .media_production import MediaProducer, RenderJob
from .prompt_generation import PromptBuilder, Prompt
from .seo import SeoAssistant, format_publication_log
from .scheduling import Scheduler, ScheduleItem


@dataclass
class WorkflowOutput:
    prompts: List[Prompt]
    renders: List[RenderJob]
    exports: List[ExportResult]
    seo_copy: Dict[str, str]
    schedule: List[ScheduleItem]
    engagement_tasks: List[EngagementTask]
    analytics_snapshot: Dict[str, float]
    publication_log: str


class AutomationWorkflow:
    """Coordinates the automation modules to produce ready-to-publish media."""

    def __init__(self, base_path: Path) -> None:
        self.collector = DataCollector(base_path)
        self.producer = MediaProducer()
        self.exporter = Exporter()
        self.scheduler = Scheduler()

    def execute(self, scenario_path: Path, media_path: Path) -> WorkflowOutput:
        scenario = self.collector.load_scenario(scenario_path)
        assets = self.collector.load_media_assets(media_path)

        prompt_builder = PromptBuilder(scenario, assets)
        prompts = list(prompt_builder.build_all())

        render_jobs = self.producer.submit_jobs(prompts)

        exports = self.exporter.export(render_jobs, scenario.platforms)

        seo_assistant = SeoAssistant(scenario)
        keyword_results = seo_assistant.research_keywords()
        seo_copy = {}
        for platform in scenario.platforms:
            keywords = [result.keyword for result in keyword_results[:3]]
            copy = seo_assistant.craft_copy(platform, keywords)
            seo_copy[platform] = f"Title: {copy.title}\nDescription: {copy.description}\nTags: {', '.join(copy.tags)}"

        publication_times = seo_assistant.recommend_publication_times()
        publication_log = format_publication_log(publication_times)

        schedule = self.scheduler.build_schedule(publication_times)

        engagement_planner = EngagementPlanner()
        engagement_tasks = engagement_planner.plan_tasks(list(scenario.platforms), publication_times)

        analytics_tracker = AnalyticsTracker()
        analytics_snapshot = analytics_tracker.project_metrics(list(scenario.platforms)).to_dict()

        return WorkflowOutput(
            prompts=prompts,
            renders=render_jobs,
            exports=exports,
            seo_copy=seo_copy,
            schedule=schedule,
            engagement_tasks=engagement_tasks,
            analytics_snapshot=analytics_snapshot,
            publication_log=publication_log,
        )


def run_workflow(base_path: str, scenario_file: str, media_file: str) -> WorkflowOutput:
    workflow = AutomationWorkflow(Path(base_path))
    return workflow.execute(Path(scenario_file), Path(media_file))
