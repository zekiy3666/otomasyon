# Automation Workflow

This project provides a simulated end-to-end automation pipeline for generating social media video campaigns. The workflow orchestrates data collection, prompt creation, media generation, export, SEO guidance, scheduling, analytics projections, and engagement follow-up planning.

## Project Structure

```
src/automation/
├── __init__.py
├── __main__.py        # CLI entry point
├── analytics.py       # Analytics projections
├── data_collection.py # Scenario and media ingestion
├── editing_export.py  # Platform specific export profiles
├── engagement.py      # Engagement follow-up planning
├── media_production.py# Render job simulations
├── prompt_generation.py# Prompt builders for Google Veo 3 & Canva
├── scheduling.py      # Publication scheduling utilities
└── workflow.py        # End-to-end orchestration
```

Supporting assets live in `samples/`, and automated tests can be found in `tests/`.

## Installation

Create a virtual environment and install the project in editable mode:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

> The package uses only the Python standard library, so there are no additional dependencies.

## Sample Usage

Run the full workflow with the bundled sample inputs:

```bash
PYTHONPATH=src python -m automation samples/sample_scenario.json samples/sample_media.csv --base-path .
```

Example output (truncated):

```
{
  "prompts": [
    {
      "narrative": "Goal: Promote sustainable living\nGoal: Highlight smart thermostat\nAudience: Homeowners, Eco-conscious families\nCTA: Download the free efficiency checklist",
      "style": "Tone: Friendly and informative",
      "call_to_action": "Download the free efficiency checklist",
      "references": "BROLL01: Family adjusting smart thermostat [tags: home, energy, family]\nBROLL02: Solar panels on suburban roof [tags: solar, eco, exterior]\nAUDIO01: Upbeat acoustic background track [tags: music, acoustic]"
    },
    ...
  ],
  "renders": ["renders/google_veo_3_XXXX.mp4", "renders/canva_XXXX.mp4"],
  "exports": ["exports/renders/google_veo_3_XXXX_youtube.mp4", ...],
  "seo": {
    "youtube": "Title: Eco Home Energy Tips | eco home\nDescription: ...",
    ...
  },
  "publication_log": "youtube: 2024-06-01T09:00:00\ninstagram: 2024-06-01T11:00:00\n..."
}
```

Sample input files:

- `samples/sample_scenario.json`
- `samples/sample_media.csv`
- `samples/sample_output.json`

The CLI prints the automation summary to stdout, making it easy to redirect into a JSON file for auditing. A ready-made sample output is stored in `samples/sample_output.json`.

## Configuration

Key configuration points:

- **Base path**: Controls where scenario and media files are resolved.
- **Scheduling buffer**: Adjust via `Scheduler(buffer_minutes=...)` for reminder lead time.
- **Engagement follow-up delay**: Configure with `EngagementPlanner(follow_up_delay_hours=...)`.
- **Platform export profiles**: Modify `PLATFORM_PROFILES` in `editing_export.py` to tweak format requirements.

## Tests

Run the automated unit and integration tests with:

```bash
pytest
```

## Extending the Workflow

- Integrate real Google Veo 3 or Canva APIs by swapping the simulation layer in `media_production.py`.
- Persist analytics and scheduling artifacts to external systems (CRM, project management tools) by extending `AnalyticsTracker` and `Scheduler`.
- Add more platforms by defining new export profiles and updating the SEO utilities to include tailored copy templates.
