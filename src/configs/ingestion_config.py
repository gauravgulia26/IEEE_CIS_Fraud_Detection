# Ingestion Input Config
from src.utils import load_yaml
from src.configs.paths import COMPONENT_PARAM_FILE_PATH, PROJ_ROOT
from box import Box


class DataIngestionConfig:
    def __init__(self):
        __ingestion_yaml_file = Box(
            load_yaml(file_path=COMPONENT_PARAM_FILE_PATH, key="ingestion")
        )
        self.train_identity_file_path = PROJ_ROOT / __ingestion_yaml_file.train_identity_file
        self.test_identity_file_path = PROJ_ROOT / __ingestion_yaml_file.test_identity_file
        self.train_transaction_file_path = PROJ_ROOT / __ingestion_yaml_file.train_transaction_file
        self.test_transaction_file_path = PROJ_ROOT / __ingestion_yaml_file.test_transaction_file
