# Base directories
DATA_DIR = "data"
MODELS_DIR = "models"
REPORTS_DIR = "reports"

# Data subfolders
RAW_DATA_DIR = "raw"
INTERIM_DATA_DIR = "interim"
PROCESSED_DATA_DIR = "processed"
EXTERNAL_DATA_DIR = "external"

# Report subfolders
FIGURES_DIR = "figures"

# Log Folders

LOG_DIR = "logs"

# Raw Data Constants (static)

UNZIPPED_DIR = "unzipped"
TRAIN_TRANSACTION_FILE = "train_transaction.csv"
TRAIN_IDENTITY_FILE = "train_identity.csv"

TEST_TRANSACTION_FILE = "test_transaction.csv"
TEST_IDENTITY_FILE = "test_identity.csv"

# Components

INGESTION_COMP = "ingestion"
VALIDATION_COMP = "validation"

# YAML CONFIG

YAML_DIR = "config"
COMPONENT_PARAM_FILE_NAME = "component_params.yaml"
SCHEMA_PARAM_FILE_NAME = "schema.yaml"

# Artifacts Constants

ARTIFACTS_DIR = "artifacts"
INGESTION_ARTIFACT_DIR = "data_ingestion"
VALIDATION_ARTIFACT_DIR = "data_validation"
INGESTION_ARTIFACT_NAME = f"{INGESTION_ARTIFACT_DIR}.json"
VALIDATION_ARTIFACT_NAME = f"{VALIDATION_ARTIFACT_DIR}.json"
