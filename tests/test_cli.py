from __future__ import annotations

import json
from pathlib import Path

from cli import main

FIXTURE_DIR = Path(__file__).resolve().parent.parent / "examples"


def test_cli_main_runs_end_to_end(tmp_path, capsys):
    output_dir = tmp_path / "renders"
    dump_path = tmp_path / "results.json"

    exit_code = main(
        [
            "--scenario",
            str(FIXTURE_DIR / "scenario.json"),
            "--media-dir",
            str(FIXTURE_DIR / "media"),
            "--platform-config",
            "config/platforms.yml",
            "--publish-config",
            "config/publishing.yml",
            "--engine",
            "canva",
            "--output-dir",
            str(output_dir),
            "--dump",
            str(dump_path),
        ]
    )

    assert exit_code == 0

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert Path(payload["render"]["output_path"]).exists()
    assert dump_path.exists()
    assert payload["render"]["engine"] == "canva"
