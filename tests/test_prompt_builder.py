from pathlib import Path

from automation.data_collection import DataCollector
from automation.prompt_generation import PromptBuilder


def test_prompt_builder_generates_expected_tools(tmp_path: Path) -> None:
    scenario_path = tmp_path / "scenario.json"
    scenario_path.write_text(
        '{"name": "Test Campaign", "goals": ["Increase sign-ups"], "target_audience": ["Developers"], '
        '"tone": "Inspirational", "platforms": ["youtube"], "call_to_action": "Join today"}'
    )
    media_path = tmp_path / "media.csv"
    media_path.write_text("asset_id,description,tags\nB1,Demo clip,product|demo")

    collector = DataCollector(tmp_path)
    scenario = collector.load_scenario(Path("scenario.json"))
    assets = collector.load_media_assets(Path("media.csv"))

    builder = PromptBuilder(scenario, assets)
    prompts = builder.build_all()

    assert {prompt.tool for prompt in prompts} == {"google_veo_3", "canva"}
    veo_prompt = next(prompt for prompt in prompts if prompt.tool == "google_veo_3")
    assert "CTA" in veo_prompt.payload["narrative"]
    assert "Join today" == veo_prompt.payload["call_to_action"]
