"""Simulated media production layer for external services."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List

from .prompt_generation import Prompt


@dataclass
class RenderJob:
    """Represents a rendering request sent to a media service."""

    prompt: Prompt
    status: str = "pending"
    artifact_path: str | None = None


class MediaProducer:
    """Generates render jobs for prompts and simulates execution."""

    def __init__(self) -> None:
        self.completed_jobs: List[RenderJob] = []

    def submit_jobs(self, prompts: Iterable[Prompt]) -> List[RenderJob]:
        jobs = [RenderJob(prompt=prompt) for prompt in prompts]
        for job in jobs:
            self._simulate_render(job)
        self.completed_jobs.extend(jobs)
        return jobs

    def _simulate_render(self, job: RenderJob) -> None:
        payload_hash = hash(tuple(sorted(job.prompt.payload.items())))
        job.status = "complete"
        job.artifact_path = f"renders/{job.prompt.tool}_{abs(payload_hash) % 10000}.mp4"

    def get_render_summary(self) -> Dict[str, str]:
        return {
            job.prompt.tool: job.artifact_path or "pending"
            for job in self.completed_jobs
        }
