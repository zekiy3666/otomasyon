from pathlib import Path

from automation.workflow import run_workflow


def test_workflow_generates_expected_sections(tmp_path: Path) -> None:
    scenario_path = tmp_path / "scenario.json"
    scenario_path.write_text(
        '{"name": "Campaign", "goals": ["Goal"], "target_audience": ["Audience"], '
        '"tone": "Upbeat", "platforms": ["youtube", "tiktok"], "call_to_action": "Act now"}'
    )
    media_path = tmp_path / "media.csv"
    media_path.write_text("asset_id,description,tags\nA1,Clip,sample|tag")

    output = run_workflow(str(tmp_path), "scenario.json", "media.csv")

    assert len(output.prompts) == 2
    assert all(job.status == "complete" for job in output.renders)
    assert {result.profile.platform for result in output.exports} == {"YouTube", "TikTok"}
    assert set(output.seo_copy.keys()) == {"youtube", "tiktok"}
    assert len(output.schedule) == 2
    assert output.analytics_snapshot
    assert "youtube" in output.publication_log
