from src.custom_logger import get_logger
from src.custom_exception import CustomException
from src.entity.manager import ArtifactsManager
from src.configs.manager import ConfigurationManager
from src.configs.paths import INGESTION_LOG_DIR_PATH
from pathlib import Path
import pandas as pd
from typing import List


class IngestData:
    def __init__(
        self,
        configs: ConfigurationManager,
        artifacts: ArtifactsManager,
        component_name: str = "Ingestion",
        log_dir_path=INGESTION_LOG_DIR_PATH,
    ):
        self.configs = configs
        self.artifacts = artifacts
        self.log_dir_path = log_dir_path
        self.name = component_name
        self.logger = get_logger(name=component_name, log_dir_path=log_dir_path)

    def __validate_file_paths(self) -> None:
        self.logger.info("Checking File Paths")
        ingestion_config = self.configs.get_ingestion_config()
        file_paths = {
            ingestion_config.test_identity_file_path: Path(
                ingestion_config.test_identity_file_path
            ).exists(),
            ingestion_config.train_identity_file_path: Path(
                ingestion_config.train_identity_file_path
            ).exists(),
            ingestion_config.train_transaction_file_path: Path(
                ingestion_config.train_transaction_file_path
            ).exists(),
            ingestion_config.test_transaction_file_path: Path(
                ingestion_config.test_transaction_file_path
            ).exists(),
        }

        invalid_paths = [path.as_posix() for path, exist in file_paths.items() if not exist]
        if not invalid_paths:
            self.logger.info("All Paths are Valid")
        else:
            raise FileNotFoundError(f"{', '.join(invalid_paths)} is not a valid Path")

    def run(self):

        self.logger.info("Ingestion Started !!")
        self.__validate_file_paths()
        self.logger.info("Reading Files..")
        # df1 = pd.read_csv(self.configs.get_ingestion_config().train_identity_file_path)
        # df2 = pd.read_csv(self.configs.get_ingestion_config().test_identity_file_path)
        # df3 = pd.read_csv(self.configs.get_ingestion_config().train_transaction_file_path)
        # df4 = pd.read_csv(self.configs.get_ingestion_config().test_transaction_file_path)
