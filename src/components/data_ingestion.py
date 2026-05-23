from core.logging import get_logger
from core.exception import CustomException
from src.entity.artifacts import DataIngestionArtifact
from src.entity.internal import InterReadArtifact
from configs.managers.manager import ConfigurationManager
from src.utils import load_yaml
from src.configs.paths import (
    INGESTION_LOG_DIR_PATH,
    PROCESSED_DATA_DIR_PATH,
    INGESTION_COMP,
    COMPONENT_PARAM_FILE_PATH,
)
from pathlib import Path
import pandas as pd
import sys


class IngestData:
    def __init__(
        self,
        configs: ConfigurationManager,
        artifacts: DataIngestionArtifact,
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

    def __read_files(self) -> InterReadArtifact:
        try:
            self.logger.info("Reading Files..")
            train_identity = pd.read_csv(
                self.configs.get_ingestion_config().train_identity_file_path
            )
            test_identity = pd.read_csv(
                self.configs.get_ingestion_config().test_identity_file_path
            )
            train_transaction = pd.read_csv(
                self.configs.get_ingestion_config().train_transaction_file_path
            )
            test_transaction = pd.read_csv(
                self.configs.get_ingestion_config().test_transaction_file_path
            )

            merged_df = pd.merge(train_identity, train_transaction, on="TransactionID", how="left")
        except Exception as e:
            err = CustomException(error=e, error_detail=sys)
            self.logger.error(f"Error Occured: {e}")
            raise err

        obj = InterReadArtifact(
            train_identity_df=train_identity,
            test_identity_df=test_identity,
            train_transaction_df=train_transaction,
            test_transaction_df=test_transaction,
            merged_final_df=merged_df,
        )
        return obj

    def __save_files(self, merged_file_name: str):
        df_files = self.__read_files()
        try:
            file_save_path = Path(
                PROCESSED_DATA_DIR_PATH,
                load_yaml(file_path=COMPONENT_PARAM_FILE_PATH, key=INGESTION_COMP)[
                    "merged_file_name"
                ],
            )

            df_files.merged_final_df.to_csv(file_save_path)
            self.logger.info(f"Merged File Saved to: {file_save_path}")
        except Exception as e:
            err = CustomException(error=e, error_detail=sys)
            self.logger.error(f"Error Occured: {e}")
            raise err

    def run(self):

        self.logger.info("Ingestion Started !!")
        self.__validate_file_paths()
        InterArtifact = self.__read_files()
