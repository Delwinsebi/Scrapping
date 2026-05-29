# Scrapping (Portal Harvester)

A small Scrapy-based harvester for extracting inventory and notices from the MGU portal.

## Project layout

- `harvester_core/` — Scrapy project code (spiders, pipelines, settings).
- `harvester_core/spiders/mgu_portal.py` — main spider for the MGU portal.
- `requirements.txt` — Python dependencies.
- `local_archive/` — local data exports and templates.

## Prerequisites

- Python 3.8+ (3.10+ recommended)
- `virtualenv` or `venv` for isolated environments

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the spider

To run the main spider and write output (CSV/JSON) to a file, run:

```bash
scrapy crawl mgu_portal -o output.csv
```

Replace `output.csv` with `output.json` or another filename/format supported by Scrapy.

## Output and local archive

- The project previously stored exports under `local_archive/` (for example `data-export.csv`).
- Generated exports and reports (e.g., `Final_Inventory_Report.csv`) can be placed at the repository root or archived into `local_archive/`.

## Configuration

- Edit `harvester_core/settings.py` to adjust Scrapy settings (concurrency, user-agent, pipelines).
- Update pipelines in `harvester_core/pipelines.py` to control item processing and storage.

## Development notes

- The main spider lives at `harvester_core/spiders/mgu_portal.py`.
- If you add new dependencies, run `pip freeze > requirements.txt` to update the lockfile.

## Contributing

1. Create a feature branch.
2. Run the spider locally and include sample output in `local_archive/` when relevant.
3. Open a PR describing changes.

## License

This repository does not include a license file. 

