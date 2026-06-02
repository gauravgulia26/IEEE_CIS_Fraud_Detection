from pathlib import Path
import sys
import json
import pandas as pd

from src.entity.artifacts import ValidationArtifact
from src.core.logging import get_logger
from src.core.exception import CustomException

from src.configs.paths import (
    SCHEMA_PARAM_FILE_PATH as SCHEMA_FILE_PATH,
    VALIDATION_LOG_DIR_PATH,
    VALIDATION_REPORT_DIR_PATH,
    VALIDATION_COMP,
)
from src.constants import INGESTION_COMP
from src.configs.paths import VALIDATION_ARTIFACT_DIR_PATH

from src.utils import load_artifact_json, load_yaml, save_artifact_json


class DataValidation:

    def __init__(
        self,
        ingestion_artifact_path: str,
    ):
        self.ingestion_artifact_path = ingestion_artifact_path

        self.logger = get_logger(
            name=VALIDATION_COMP,
            log_dir_path=VALIDATION_LOG_DIR_PATH,
        )

    def __load_schema(self):
        return load_yaml(SCHEMA_FILE_PATH, key=INGESTION_COMP)

    def __load_data(self):
        artifact = load_artifact_json(self.ingestion_artifact_path)
        merged_path = artifact["merged_file_path"]

        df = pd.read_parquet(merged_path)
        return df, merged_path

    def __validate_required_columns(self, df, expected_cols):
        missing_cols = [col for col in expected_cols if col not in df.columns]
        return missing_cols

    def __validate_dtypes(self, df, expected_dtypes):
        dtype_errors = {}

        for col, dtype in expected_dtypes.items():
            if col in df.columns:
                if str(df[col].dtype) != dtype:
                    dtype_errors[col] = {
                        "expected": dtype,
                        "found": str(df[col].dtype),
                    }

        return dtype_errors

    def __save_validation_report(self, report: dict) -> Path:
        report_dir = Path(VALIDATION_REPORT_DIR_PATH)
        report_dir.mkdir(parents=True, exist_ok=True)

        report_path = report_dir / "validation_report_latest.json"

        with open(report_path, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        self.logger.info(f"Validation Report Saved at: {report_path}")
        return report_path

    def run(self) -> ValidationArtifact:
        try:
            self.logger.info("Data Validation Started")

            schema = self.__load_schema()
            df, file_path = self.__load_data()

            expected_columns = schema["required_columns"]
            expected_dtypes = schema["expected_dtypes"]

            # ✅ Only 2 validations
            missing_columns = self.__validate_required_columns(df, expected_columns)
            dtype_errors = self.__validate_dtypes(df, expected_dtypes)

            validation_status = len(missing_columns) == 0 and len(dtype_errors) == 0

            report = {
                "validation_status": validation_status,
                "file_path": file_path,
                "missing_columns": missing_columns,
                "dtype_errors": dtype_errors,
                "total_rows": df.shape[0],
                "total_columns": df.shape[1],
            }

            report_path = self.__save_validation_report(report)

            self.logger.info("Data Validation Completed")

            obj = ValidationArtifact(
                validation_status=validation_status,
                validated_file_path=Path(file_path),
                total_rows=df.shape[0],
                total_columns=df.shape[1],
                missing_columns=missing_columns,
                dtype_errors=dtype_errors,
                null_threshold_errors=[],
                allowed_value_errors=[],
                uniqueness_errors=[],
                range_errors=[],
                validated_columns=list(df.columns),
                schema_version="minimal",
                validation_message=f"Report Saved At: {report_path}",
            )

            self.logger.info(f"Data Validation Artifacts saved at: {VALIDATION_ARTIFACT_DIR_PATH}")
            save_artifact_json(artifact=obj, file_path=VALIDATION_ARTIFACT_DIR_PATH)

            return obj
        except Exception as e:
            self.logger.exception(f"Error During Data Validation: {e}")
            raise CustomException(error=e, error_detail=sys)
