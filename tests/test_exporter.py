from automation.editing_export import Exporter, PLATFORM_PROFILES
from automation.media_production import RenderJob
from automation.prompt_generation import Prompt


def test_exporter_creates_outputs_for_each_platform() -> None:
    prompt = Prompt(tool="google_veo_3", payload={"narrative": "CTA"})
    job = RenderJob(prompt=prompt, status="complete", artifact_path="renders/sample.mp4")
    exporter = Exporter()

    results = exporter.export([job], ["youtube", "instagram"])

    assert len(results) == 2
    platforms = {result.profile.platform for result in results}
    assert platforms == {PLATFORM_PROFILES["youtube"].platform, PLATFORM_PROFILES["instagram"].platform}
    for result in results:
        assert result.output_path.startswith("exports/renders/sample")
        assert result.output_path.endswith(".mp4")
