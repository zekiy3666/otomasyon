"""Video generation orchestration."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict


@dataclass(frozen=True)
class RenderResult:
    """Represents the outcome of a rendered video."""

    engine: str
    prompt: str
    output_path: Path

    def to_dict(self) -> Dict[str, str]:
        return {
            "engine": self.engine,
            "prompt": self.prompt,
            "output_path": str(self.output_path),
        }


def generate_video(prompt: str, engine: str, output_dir: Path) -> RenderResult:
    """Generate a video using the provided engine.

    This implementation mocks the rendering by writing a JSON manifest that captures
    the request details. The manifest allows downstream steps and tests to confirm the
    process without requiring the actual rendering services.
    """

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / f"{engine}_render.json"
    manifest_path.write_text(json.dumps({"engine": engine, "prompt": prompt}, indent=2), encoding="utf-8")
    return RenderResult(engine=engine, prompt=prompt, output_path=manifest_path)
