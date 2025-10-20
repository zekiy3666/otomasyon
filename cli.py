"""Command line interface coordinating the automation pipeline."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from automation import (
    apply_post_processing,
    build_prompt,
    build_schedule,
    collect_media_assets,
    collect_user_scenario,
    generate_video,
)
from automation.video_generator import RenderResult
from seo import format_metadata, generate_keywords


def load_yaml(path: Path) -> Dict[str, Any]:
    """Load a minimal YAML file.

    A lightweight parser is implemented to avoid additional dependencies. The format
    supports mappings and nested dictionaries using spaces for indentation.
    """

    try:
        import yaml  # type: ignore

        return dict(yaml.safe_load(path.read_text(encoding="utf-8")))
    except ModuleNotFoundError:
        return _fallback_yaml_parser(path)


def _parse_scalar(value: str) -> Any:
    if value.isdigit():
        return int(value)
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    return value


def _fallback_yaml_parser(path: Path) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    current_section: str | None = None
    current_subkey: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line:
            continue
        indent = len(line) - len(line.lstrip())
        key, _, value = line.strip().partition(":")
        value = value.strip()

        if indent == 0:
            if value:
                data[key] = _parse_scalar(value)
                current_section = None
                current_subkey = None
            else:
                data[key] = {}
                current_section = key
                current_subkey = None
        elif indent == 2 and current_section:
            section_dict = data[current_section]
            if value:
                section_dict[key] = _parse_scalar(value)
                current_subkey = None
            else:
                section_dict[key] = {}
                current_subkey = key
        elif indent == 4 and current_section and current_subkey:
            subsection = data[current_section][current_subkey]
            subsection[key] = _parse_scalar(value)
        else:
            raise ValueError(f"Unsupported YAML structure near line: {raw_line}")
    return data


def orchestrate_pipeline(args: argparse.Namespace) -> Dict[str, Any]:
    scenario = collect_user_scenario(Path(args.scenario))
    media = collect_media_assets(Path(args.media_dir))

    platforms_config = load_yaml(Path(args.platform_config))
    publishing_config = load_yaml(Path(args.publish_config))

    engine = args.engine
    prompt = build_prompt(scenario, [str(m) for m in media], engine)
    render_result: RenderResult = generate_video(prompt, engine, Path(args.output_dir))
    post_process_path = apply_post_processing(render_result, overlays={"cta": scenario.call_to_action})

    keywords = generate_keywords(scenario, platforms_config.get("platforms", {}))
    metadata = {
        platform: format_metadata(
            platform,
            scenario.title,
            scenario.description,
            platform_keywords,
            platforms_config.get("requirements", {}),
        )
        for platform, platform_keywords in keywords.items()
    }

    schedule = build_schedule(
        base_time=datetime.fromisoformat(publishing_config["start_at"]),
        cadence=publishing_config.get("cadence", {}),
        platforms=list(keywords.keys()),
    )

    return {
        "prompt": prompt,
        "render": render_result.to_dict(),
        "post_process": str(post_process_path),
        "keywords": keywords,
        "metadata": {platform: meta.__dict__ for platform, meta in metadata.items()},
        "schedule": [
            {"platform": item.platform, "publish_at": item.publish_at.isoformat(), "notes": item.notes}
            for item in schedule
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the automation pipeline")
    parser.add_argument("--scenario", required=True, help="Path to scenario JSON file")
    parser.add_argument("--media-dir", required=True, help="Directory containing media assets")
    parser.add_argument("--platform-config", default="config/platforms.yml", help="Platform config YAML")
    parser.add_argument("--publish-config", default="config/publishing.yml", help="Publishing config YAML")
    parser.add_argument("--engine", default="google_veo_3", help="Video generation engine")
    parser.add_argument("--output-dir", default="build", help="Directory for rendered outputs")
    parser.add_argument("--dump", help="Optional path to dump orchestration results as JSON")

    args = parser.parse_args(argv)
    results = orchestrate_pipeline(args)

    if args.dump:
        Path(args.dump).write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
