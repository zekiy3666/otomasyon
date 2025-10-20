# Otomasyon Video Pipeline

This repository demonstrates an end-to-end automation flow for producing marketing-ready videos using AI assisted tooling. The workflow collects user scenarios and media, crafts prompts for Google Veo 3 or Canva, generates draft outputs, performs post processing and prepares SEO metadata for publishing across major social networks.

## Features

- **Scenario & media collection** – Parse JSON scenarios and gather media files for production. (`automation.collector`)
- **Prompt generation** – Create engine-specific prompts for Google Veo 3 and Canva. (`automation.prompt_builder`)
- **Video rendering mock** – Persist render manifests to emulate video generation for tests. (`automation.video_generator`)
- **Post processing** – Append overlay notes and CTA instructions. (`automation.post_processor`)
- **Publishing scheduler** – Build calendar entries from configurable cadences. (`automation.scheduler`)
- **SEO toolkit** – Generate keywords and format metadata for YouTube, Instagram, TikTok and Facebook respecting platform requirements. (`seo` package)
- **CLI orchestration** – The `cli.py` module coordinates the complete flow with configuration driven inputs.

## Getting Started

### Prerequisites

- Python 3.11+
- (Optional) [PyYAML](https://pyyaml.org/) for full YAML support. A minimal parser is bundled for simple configurations.

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # if you decide to manage dependencies explicitly
```

### Running the Pipeline

Example command using the bundled demo assets:

```bash
python cli.py \
  --scenario examples/scenario.json \
  --media-dir examples/media \
  --platform-config config/platforms.yml \
  --publish-config config/publishing.yml \
  --engine google_veo_3 \
  --output-dir build \
  --dump build/results.json
```

The CLI prints a JSON summary including prompts, render manifests, SEO metadata and publishing schedule. When `--dump` is provided the same payload is saved to disk.

### Configuration Files

- `config/platforms.yml` – Platform specific keyword hints and SEO limits.
- `config/publishing.yml` – Defines the starting publish timestamp and cadence per platform.

### Examples

The `examples/` directory contains a sample scenario and placeholder media assets used by tests and quick demos.

## Testing

The test suite uses `pytest`. Execute the tests with:

```bash
pytest
```

## Development Notes

- The video rendering step writes manifests instead of real video files to keep tests deterministic.
- SEO rules follow the internal platform requirement table documented in `seo/formatter.py` comments.
- Extend `config/platforms.yml` and `config/publishing.yml` to cover more platforms or adjust cadence.

## License

This project is released under the [MIT License](LICENSE).
