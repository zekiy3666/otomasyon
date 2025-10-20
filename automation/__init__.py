"""Automation pipeline package."""

from .collector import collect_user_scenario, collect_media_assets
from .prompt_builder import build_prompt
from .video_generator import generate_video
from .post_processor import apply_post_processing
from .scheduler import build_schedule

__all__ = [
    "collect_user_scenario",
    "collect_media_assets",
    "build_prompt",
    "generate_video",
    "apply_post_processing",
    "build_schedule",
]
