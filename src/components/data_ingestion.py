from src.core.logging import get_logger
from src.core.exception import CustomException
from src.entity.artifacts import DataIngestionArtifact
from src.entity.internal import InterReadArtifact
from src.configs.managers.manager import ConfigurationManager
from src.utils import load_yaml, load_artifact_json, save_artifact_json
from src.configs.paths import (
    INGESTION_LOG_DIR_PATH,
    PROJ_ROOT,
    INGESTION_COMP,
    COMPONENT_PARAM_FILE_PATH,
    INGESTION_ARTIFACT_DIR_PATH,
)
from pathlib import Path
import pandas as pd
import sys
from typing import Dict
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


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

    def _read_csv_with_progress(
        self,
        path,
        chunk_size: int = 100000,
    ) -> pd.DataFrame:

        self.logger.info(f"Reading File: {path.name}")

        total_rows = sum(1 for _ in open(path, "r")) - 1

        chunks = []

        with tqdm(
            total=total_rows,
            desc=f"Loading {path.name}",
        ) as pbar:

            for chunk in pd.read_csv(
                path,
                engine="c",
                chunksize=chunk_size,
                low_memory=False,
            ):

                chunks.append(chunk)

                pbar.update(len(chunk))

        df = pd.concat(chunks, ignore_index=True)

        self.logger.info(f"{path.name} Loaded Successfully")

        return df

    def __read_files(self) -> InterReadArtifact:

        try:

            self.logger.info("Started Reading Files")

            with ThreadPoolExecutor() as executor:

                future_identity = executor.submit(
                    self._read_csv_with_progress,
                    self.configs.train_identity_file_path,
                )

                future_transaction = executor.submit(
                    self._read_csv_with_progress,
                    self.configs.train_transaction_file_path,
                )

                train_identity = future_identity.result()

                train_transaction = future_transaction.result()

            self.logger.info("Merging Datasets")

            merged_df = pd.merge(
                train_transaction,
                train_identity,
                on="TransactionID",
                how="left",
            )

            merged_df["TransactionID"] = pd.to_numeric(
                merged_df["TransactionID"], errors="coerce"
            ).astype("int64")
            merged_df["isFraud"] = pd.to_numeric(merged_df["isFraud"], errors="coerce").astype(
                "int8"
            )
            merged_df["TransactionDT"] = pd.to_numeric(
                merged_df["TransactionDT"], errors="coerce"
            ).astype("int64")
            merged_df["TransactionAmt"] = pd.to_numeric(
                merged_df["TransactionAmt"], errors="coerce"
            ).astype("float32")

            self.logger.info("Dtypes Changed Successfully !!")

            obj = InterReadArtifact(
                train_identity_df=train_identity,
                train_transaction_df=train_transaction,
                merged_final_df=merged_df,
            )

            return obj

        except Exception as e:

            self.logger.exception(f"Error Occurred While Reading Files: {e}")

            raise CustomException(
                error=e,
                error_detail=sys,
            )

    def __save_files(self, artifact_object: InterReadArtifact) -> None:
        df_files = artifact_object
        try:
            file_save_path = Path(
                PROJ_ROOT,
                self.yaml_configs["merged_file_name"],
            )
            self.logger.info(f"Creating Directory: {file_save_path.parents[0]}")
            file_save_path.parents[0].mkdir(parents=True, exist_ok=True)

            df_files.merged_final_df.to_parquet(file_save_path, index=False, engine="pyarrow")
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

        obj = DataIngestionArtifact(
            ident_train_data_path=PROJ_ROOT / self.yaml_configs["train_identity_file"],
            ident_test_data_path=PROJ_ROOT / self.yaml_configs["test_identity_file"],
            trns_train_data_path=PROJ_ROOT / self.yaml_configs["train_transaction_file"],
            trns_test_data_path=PROJ_ROOT / self.yaml_configs["test_transaction_file"],
            merged_file_path=PROJ_ROOT / self.yaml_configs["merged_file_name"],
        )

        save_artifact_json(artifact=obj, file_path=INGESTION_ARTIFACT_DIR_PATH)
        self.logger.info("JSON Artifact Saved")
        return obj
