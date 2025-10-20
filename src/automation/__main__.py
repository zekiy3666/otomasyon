"""Command line interface for running the automation workflow."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .workflow import run_workflow


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the content automation workflow")
    parser.add_argument("scenario", type=Path, help="Path to the scenario JSON file")
    parser.add_argument("media", type=Path, help="Path to the media CSV file")
    parser.add_argument("--base-path", type=Path, default=Path("."), help="Base path for assets")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = run_workflow(str(args.base_path), str(args.scenario), str(args.media))
    summary = {
        "prompts": [prompt.payload for prompt in output.prompts],
        "renders": [job.artifact_path for job in output.renders],
        "exports": [result.output_path for result in output.exports],
        "seo": output.seo_copy,
        "schedule": [
            {
                "platform": item.platform,
                "publish_time": item.publish_time.isoformat(),
                "reminder_time": item.reminder_time.isoformat(),
            }
            for item in output.schedule
        ],
        "engagement": [
            {
                "platform": task.platform,
                "action": task.action,
                "scheduled_for": task.scheduled_for.isoformat(),
            }
            for task in output.engagement_tasks
        ],
        "analytics": output.analytics_snapshot,
        "publication_log": output.publication_log,
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
