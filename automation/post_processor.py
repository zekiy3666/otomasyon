"""Post processing helpers for rendered videos."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

from .video_generator import RenderResult


def apply_post_processing(render_result: RenderResult, overlays: Dict[str, str] | None = None) -> Path:
    """Apply final adjustments and return the updated output path.

    The function emulates editing by writing a sidecar note describing overlays and
    captions applied to the render output.
    """

    sidecar_path = render_result.output_path.with_suffix(".post.txt")
    notes = [f"Engine: {render_result.engine}"]
    if overlays:
        for key, value in overlays.items():
            notes.append(f"{key}: {value}")
    sidecar_path.write_text("\n".join(notes), encoding="utf-8")
    return sidecar_path
