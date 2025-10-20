from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from automation.collector import collect_media_assets, collect_user_scenario
from automation.prompt_builder import build_prompt
from automation.scheduler import build_schedule
from automation.video_generator import generate_video
from cli import orchestrate_pipeline
from seo import format_metadata, generate_keywords


FIXTURE_DIR = Path(__file__).resolve().parent.parent / "examples"


def test_collect_and_prompt_flow(tmp_path: Path) -> None:
    scenario = collect_user_scenario(FIXTURE_DIR / "scenario.json")
    media = collect_media_assets(FIXTURE_DIR / "media")
    prompt = build_prompt(scenario, [str(path) for path in media], "google_veo_3")
    render = generate_video(prompt, "google_veo_3", tmp_path)

    assert "AI Workflow Automation Demo" in prompt
    assert render.output_path.exists()


def test_generate_keywords_and_metadata() -> None:
    scenario = collect_user_scenario(FIXTURE_DIR / "scenario.json")
    platforms_config = {
        "platforms": {
            "youtube": {"must_include": ["Tutorial"]},
            "instagram": {"must_include": ["Behind the scenes"]},
        },
        "requirements": {
            "youtube": {"title_limit": 50, "description_limit": 200, "hashtag_limit": 2},
            "instagram": {"title_limit": 150, "description_limit": 2200, "hashtag_limit": 3},
        },
    }

    keywords = generate_keywords(scenario, platforms_config["platforms"])
    assert "tutorial" in keywords["youtube"]

    metadata = format_metadata(
        "YouTube",
        scenario.title,
        scenario.description,
        keywords["youtube"],
        platforms_config["requirements"],
    )
    assert len(metadata.title) <= 50
    assert set(metadata.keywords).issubset(set(keywords["youtube"]))


def test_orchestrate_pipeline_end_to_end(tmp_path: Path) -> None:
    output_dir = tmp_path / "output"
    dump_file = tmp_path / "results.json"
    args = argparse.Namespace(
        scenario=str(FIXTURE_DIR / "scenario.json"),
        media_dir=str(FIXTURE_DIR / "media"),
        platform_config=str(Path("config/platforms.yml")),
        publish_config=str(Path("config/publishing.yml")),
        engine="google_veo_3",
        output_dir=str(output_dir),
        dump=str(dump_file),
    )

    results = orchestrate_pipeline(args)

    assert set(results["keywords"].keys()) >= {"youtube", "instagram", "tiktok", "facebook"}
    assert Path(results["render"]["output_path"]).exists()
    assert dump_file.exists() is False

    Path(tmp_path / "manual.json").write_text(json.dumps(results, indent=2), encoding="utf-8")


def test_schedule_builder_uses_cadence() -> None:
    base_time = datetime(2024, 1, 1, 9, 0, 0)
    cadence = {"default": 2, "youtube": 3}
    schedule = build_schedule(base_time, cadence, ["youtube", "instagram"])

    assert schedule[0].publish_at == base_time
    assert (schedule[1].publish_at - base_time).days == 2
