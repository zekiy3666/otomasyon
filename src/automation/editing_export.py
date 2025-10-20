"""Post-processing and export helpers for platform-specific outputs."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List

from .media_production import RenderJob


@dataclass
class ExportProfile:
    platform: str
    aspect_ratio: str
    resolution: str
    duration_limit_s: int
    captions: bool
    file_format: str


PLATFORM_PROFILES: Dict[str, ExportProfile] = {
    "youtube": ExportProfile(
        platform="YouTube",
        aspect_ratio="16:9",
        resolution="3840x2160",
        duration_limit_s=43200,
        captions=True,
        file_format="mp4",
    ),
    "instagram": ExportProfile(
        platform="Instagram Reels",
        aspect_ratio="9:16",
        resolution="1080x1920",
        duration_limit_s=90,
        captions=True,
        file_format="mp4",
    ),
    "tiktok": ExportProfile(
        platform="TikTok",
        aspect_ratio="9:16",
        resolution="1080x1920",
        duration_limit_s=180,
        captions=True,
        file_format="mp4",
    ),
    "facebook": ExportProfile(
        platform="Facebook Feed",
        aspect_ratio="1:1",
        resolution="1080x1080",
        duration_limit_s=240,
        captions=False,
        file_format="mp4",
    ),
}


@dataclass
class ExportResult:
    job: RenderJob
    profile: ExportProfile
    output_path: str


class Exporter:
    """Transforms rendered videos into platform-ready outputs."""

    def export(self, jobs: Iterable[RenderJob], platforms: Iterable[str]) -> List[ExportResult]:
        results: List[ExportResult] = []
        for job in jobs:
            for platform_key in platforms:
                profile = self._get_profile(platform_key)
                output_path = self._derive_output_path(job.artifact_path, profile)
                results.append(ExportResult(job=job, profile=profile, output_path=output_path))
        return results

    def _get_profile(self, platform_key: str) -> ExportProfile:
        try:
            return PLATFORM_PROFILES[platform_key.lower()]
        except KeyError as exc:
            raise ValueError(f"Unknown platform: {platform_key}") from exc

    @staticmethod
    def _derive_output_path(artifact_path: str | None, profile: ExportProfile) -> str:
        base = artifact_path or "renders/unknown.mp4"
        stem = base.rsplit(".", 1)[0]
        normalized_platform = profile.platform.lower().replace(" ", "_")
        return f"exports/{stem}_{normalized_platform}.{profile.file_format}"
