# Verification Guide

This project separates public review verification from full notebook reproduction. The repository keeps enough material to review the analytical flow, but the source UCI dataset must be provided locally for a full rerun.

## Verification Scope

| Area | Publicly Verifiable | Notes |
| --- | --- | --- |
| Public review artifacts | Yes | `scripts/check_public_artifacts.py` checks docs, summary images, automation guide, and pipeline entry point. |
| Pipeline entry-point syntax | Yes | CI compiles `run_pipeline.py` and the artifact checker. |
| Notebook sequence | Yes, structurally | `run_pipeline.py` executes the notebooks in order without modifying source notebooks. |
| Full notebook execution | Requires data | Needs `Online_Retail.csv` from UCI. |
| Campaign/segment interpretation | Yes | README and docs expose the decision logic and output interpretation. |

## Local Verification

Public review check:

```bash
python -m py_compile run_pipeline.py scripts/check_public_artifacts.py
python scripts/check_public_artifacts.py
```

Full notebook pipeline after placing the UCI CSV at `데이터셋/Online_Retail.csv`:

```bash
pip install -r requirements.txt
python run_pipeline.py --clear-artifacts --stop-on-error
```

## CI Verification

GitHub Actions runs:

```bash
python -m py_compile run_pipeline.py scripts/check_public_artifacts.py
python scripts/check_public_artifacts.py
```

## Data Boundary

- Required raw file: `데이터셋/Online_Retail.csv`.
- Raw CSV and generated analysis CSV files are excluded from Git.
- Public images and documents are tracked for review.

## Known Limits

- CI does not execute notebooks because the UCI CSV is not committed.
- Public verification checks artifact completeness and entry-point syntax, not statistical reruns.
- Segment thresholds should be revalidated if the business context or data period changes.
