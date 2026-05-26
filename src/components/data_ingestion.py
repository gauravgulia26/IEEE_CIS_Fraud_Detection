from core.logging import get_logger
from core.exception import CustomException
from src.entity.artifacts import DataIngestionArtifact
from src.entity.internal import InterReadArtifact
from configs.managers.manager import ConfigurationManager
from src.utils import load_yaml
from src.configs.paths import (
    INGESTION_LOG_DIR_PATH,
    PROJ_ROOT,
    INGESTION_COMP,
    COMPONENT_PARAM_FILE_PATH,
    SCHEMA_PARAM_FILE_PATH,
)
from pathlib import Path
import pandas as pd
import sys
from typing import Dict


class IngestData:
    def __init__(
        self,
        configs: ConfigurationManager,
        artifacts: DataIngestionArtifact,
        component_name: str = "Ingestion",
        log_dir_path=INGESTION_LOG_DIR_PATH,
    ):
        self.configs = configs.get_ingestion_config()
        self.artifacts = artifacts
        self.log_dir_path = log_dir_path
        self.name = component_name
        self.logger = get_logger(name=component_name, log_dir_path=log_dir_path)
        self.yaml_configs: Dict = load_yaml(
            file_path=COMPONENT_PARAM_FILE_PATH, key=INGESTION_COMP
        )

    def __validate_file_paths(self) -> None:
        self.logger.info("Checking File Paths")
        file_paths = {
            self.configs.test_identity_file_path: Path(
                self.configs.test_identity_file_path
            ).exists(),
            self.configs.train_identity_file_path: Path(
                self.configs.train_identity_file_path
            ).exists(),
            self.configs.train_transaction_file_path: Path(
                self.configs.train_transaction_file_path
            ).exists(),
            self.configs.test_transaction_file_path: Path(
                self.configs.test_transaction_file_path
            ).exists(),
        }

        invalid_paths = [path.as_posix() for path, exist in file_paths.items() if not exist]
        if not invalid_paths:
            self.logger.info("All Paths are Valid")
        else:
            raise FileNotFoundError(f"{', '.join(invalid_paths)} is not a valid Path")

    def __validate_schema(self):
        pass

    def __read_files(self) -> InterReadArtifact:
        try:
            self.logger.info("Reading Files..")
            train_identity = pd.read_csv(self.configs.train_identity_file_path)
            train_transaction = pd.read_csv(self.configs.train_transaction_file_path)

            merged_df = pd.merge(train_identity, train_transaction, on="TransactionID", how="left")
        except Exception as e:
            err = CustomException(error=e, error_detail=sys)
            self.logger.exception(f"Error Occured: {e}")
            raise err

        obj = InterReadArtifact(
            train_identity_df=train_identity,
            train_transaction_df=train_transaction,
            merged_final_df=merged_df,
        )
        return obj

    def __save_files(self, artifact_object: InterReadArtifact) -> None:
        df_files = artifact_object
        try:
            file_save_path = Path(
                PROJ_ROOT,
                self.yaml_configs["merged_file_name"],
            )

            df_files.merged_final_df.to_csv(file_save_path, index=False)
            self.logger.info(f"Merged File Saved to: {file_save_path}")
            self.logger.info("Data Ingestion Completed !!")
        except Exception as e:
            err = CustomException(error=e, error_detail=sys)
            self.logger.exception(f"Error Occured: {e}")
            raise err

    def run(self) -> DataIngestionArtifact:

        self.logger.info("Ingestion Started !!")
        self.__validate_file_paths()
        artifact_object = self.__read_files()
        self.__save_files(artifact_object=artifact_object)

        return DataIngestionArtifact(
            ident_train_data_path=self.yaml_configs["train_identity_file"],
            ident_test_data_path=self.yaml_configs["test_identity_file"],
            trns_train_data_path=self.yaml_configs["train_transaction_file"],
            trns_test_data_path=self.yaml_configs["test_transaction_file"],
            merged_file_path=self.yaml_configs["merged_file_name"],
        )
