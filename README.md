# ieee_fraud_detection

This project builds a **production-oriented machine learning pipeline** to detect fraudulent financial transactions using the **IEEE-CIS Fraud Detection** dataset.

The current repository structure is organized around a modular pipeline architecture with clear separation of:

- **configuration**
- **data ingestion**
- **data validation**
- **artifacts and reports**
- **logging**
- **pipeline stages**
- **modeling utilities**

The project also uses **DVC** for pipeline reproducibility and data workflow tracking.

## Current Project Structure

```text
├── LICENSE
├── Makefile
├── README.md
├── artifacts
│   ├── data_ingestion
│   │   └── data_ingestion.json
│   └── data_validation
│       └── data_validation.json
├── config
│   ├── component_params.yaml
│   └── schema.yaml
├── data
│   ├── external
│   ├── interim
│   ├── processed
│   │   └── merged_data
│   │       └── Merged_Data.parquet
│   └── raw
│       ├── unzipped
│       │   ├── sample_submission.csv
│       │   ├── test_identity.csv
│       │   ├── test_transaction.csv
│       │   ├── train_identity.csv
│       │   └── train_transaction.csv
│       └── zipped
│           └── ieee-fraud-detection.zip
├── docs
│   ├── README.md
│   ├── docs
│   │   ├── getting-started.md
│   │   └── index.md
│   └── mkdocs.yml
├── dvc.lock
├── dvc.yaml
├── logs
│   ├── ingestion
│   └── validation
├── main.py
├── models
├── notebooks
│   ├── 0.1-Roc-Curve.ipynb
│   ├── 1-Data-Intilaisation.ipynb
│   ├── 2-Eda.ipynb
│   └── 3-Json_pyandtic.ipynb
├── pyproject.toml
├── references
├── reports
│   ├── figures
│   └── validation
│       └── validation_report_latest.json
├── requirements.txt
├── setup.cfg
├── src
│   ├── __init__.py
│   ├── components
│   │   ├── data_ingestion.py
│   │   └── data_validation.py
│   ├── configs
│   │   ├── __init__.py
│   │   ├── ingestion_config.py
│   │   ├── managers
│   │   │   ├── __init__.py
│   │   │   └── manager.py
│   │   └── paths.py
│   ├── constants
│   │   └── __init__.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── exception.py
│   │   └── logging.py
│   ├── entity
│   │   ├── __init__.py
│   │   ├── artifacts
│   │   │   ├── __init__.py
│   │   │   ├── ingestion_artifact.py
│   │   │   └── validation_artifact.py
│   │   └── internal
│   │       ├── __init__.py
│   │       └── ingestion_internal.py
│   ├── modeling
│   │   ├── __init__.py
│   │   ├── predict.py
│   │   └── train.py
│   ├── pipeline
│   │   ├── __init__.py
│   │   ├── stage_01_ingestion.py
│   │   └── stage_02_validation.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── file_utils.py
│   │   └── project_utils.py
│   └── validation
│       ├── __init__.py
│       └── validators.py
└── tests
    └── test_data.py
```

## Repository Overview

### Root Files

- `Makefile` : Shortcut commands for common development and pipeline tasks.
- `pyproject.toml` : Project metadata and tool configuration.
- `requirements.txt` : Python dependencies.
- `setup.cfg` : Tooling configuration such as linting.
- `main.py` : Pipeline entry point.
- `dvc.yaml` / `dvc.lock` : DVC pipeline definitions and locked stage metadata.

## Directory Breakdown

### `artifacts/`
Stores generated outputs from pipeline stages.

- `data_ingestion/` : Ingestion stage outputs and metadata.
- `data_validation/` : Validation stage outputs and reports.

### `config/`
Centralized project configuration files.

- `component_params.yaml` : Component-level parameters.
- `schema.yaml` : Dataset schema definition used for validation.

### `data/`
Organized data storage by lifecycle stage.

- `raw/` : Original downloaded dataset files.
- `interim/` : Intermediate transformation outputs.
- `processed/` : Final prepared datasets for downstream tasks.
- `external/` : Third-party data sources if required.

### `docs/`
Project documentation powered by **MkDocs**.

- `docs/docs/index.md` : Main documentation page.
- `docs/docs/getting-started.md` : Setup and onboarding notes.
- `docs/mkdocs.yml` : MkDocs configuration.

### `logs/`
Execution logs organized by stage.

- `logs/ingestion/` : Data ingestion execution logs.
- `logs/validation/` : Data validation execution logs.

### `models/`
Reserved for trained models, serialized artifacts, and future model outputs.

### `notebooks/`
Exploratory analysis and experimentation notebooks.

- ROC analysis
- data initialization
- EDA
- schema/Pydantic-related experimentation

### `reports/`
Generated reports and diagnostic outputs.

- `figures/` : Visual outputs.
- `validation/` : Validation reports such as `validation_report_latest.json`.

### `src/`
Main source package for the project.

#### `src/components/`
Pipeline components implementing business logic.

- `data_ingestion.py`
- `data_validation.py`

#### `src/configs/`
Configuration objects and path managers.

- ingestion configuration
- path definitions
- config manager utilities

#### `src/constants/`
Project-wide constants.

#### `src/core/`
Core infrastructure utilities.

- custom exception handling
- logging setup

#### `src/entity/`
Structured entities for internal communication across stages.

- `artifacts/` : Stage artifact classes
- `internal/` : Internal schemas and transport objects

#### `src/modeling/`
Training and inference code.

- `train.py`
- `predict.py`

#### `src/pipeline/`
Pipeline stage runners.

- `stage_01_ingestion.py`
- `stage_02_validation.py`

#### `src/utils/`
General helper functions for file and project operations.

#### `src/validation/`
Validation logic and reusable validators.

### `tests/`
Unit or integration tests for validating functionality.

## Implemented Pipeline Stages

At the current stage, the repository clearly includes:

1. **Data Ingestion**
   - raw dataset handling
   - zip extraction
   - ingestion metadata generation
   - ingestion logging

2. **Data Validation**
   - schema-based checks
   - validation reporting
   - validation artifact generation
   - validation logs

## Typical Workflow

```bash
# install dependencies
pip install -r requirements.txt

# run pipeline entry point
python main.py

# run DVC stages
dvc repro
```

## Design Notes

This structure is designed to support:

- modular pipeline development
- easier debugging through stage-specific logs
- reproducible workflows with DVC
- cleaner configuration management
- artifact tracking across ML lifecycle stages
- easier extension for future stages like transformation, training, evaluation, and deployment

## Future Extension Areas

The repository is already structured in a way that can be extended with:

- data transformation
- feature engineering
- model training pipelines
- experiment tracking
- API deployment
- CI/CD integration
- monitoring and drift detection

---

This README can later be expanded with:

- installation steps
- command reference
- DVC pipeline explanation
- architecture diagram
- contribution guide
