# src/components/data_validation.py

from pathlib import Path
import sys
import json
from datetime import datetime

from src.entity.artifacts import (
    DataIngestionArtifact,
    ValidationArtifact,
)

from src.validation import SchemaValidator

from src.core.logging import get_logger
from src.core.exception import CustomException

from src.configs.paths import (
    SCHEMA_PARAM_FILE_PATH as SCHEMA_FILE_PATH,
    VALIDATION_LOG_DIR_PATH,
    VALIDATION_REPORT_DIR_PATH,
    VALIDATION_COMP,
)


class DataValidation:

    def __init__(
        self,
        ingestion_artifact: DataIngestionArtifact,
        schema_key: str = "ingestion",
    ):

        self.ingestion_artifact = ingestion_artifact

        self.schema_key = schema_key

        self.logger = get_logger(
            name=VALIDATION_COMP,
            log_dir_path=VALIDATION_LOG_DIR_PATH,
        )

    def __save_validation_report(
        self,
        artifact: ValidationArtifact,
    ) -> Path:

        report_dir = Path(VALIDATION_REPORT_DIR_PATH)

        report_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        report_path = (
            report_dir / f"validation_report_" f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        report = {
            "validation_status": artifact.validation_status,
            "validated_file_path": artifact.validated_file_path.as_posix(),
            "total_rows": artifact.total_rows,
            "total_columns": artifact.total_columns,
            "missing_columns": artifact.missing_columns,
            "dtype_errors": artifact.dtype_errors,
            "null_threshold_errors": artifact.null_threshold_errors,
            "allowed_value_errors": artifact.allowed_value_errors,
            "uniqueness_errors": artifact.uniqueness_errors,
            "range_errors": artifact.range_errors,
            "validated_columns": artifact.validated_columns,
            "schema_version": artifact.schema_version,
            "validation_message": artifact.validation_message,
        }

        with open(
            report_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                report,
                file,
                indent=4,
            )

        self.logger.info(f"Validation Report Saved at: " f"{report_path}")

        return report_path

    def run(
        self,
    ) -> ValidationArtifact:

        try:

            self.logger.info("Data Validation Started")

            validator = SchemaValidator(
                schema_file_path=SCHEMA_FILE_PATH,
                key_name=self.schema_key,
                df_path=self.ingestion_artifact.merged_file_path,
            )

            artifact = validator.run()

            report_path = self.__save_validation_report(
                artifact=artifact,
            )

            self.logger.info("Data Validation Completed Successfully")

            return ValidationArtifact(
                validation_status=artifact.validation_status,
                validated_file_path=artifact.validated_file_path,
                total_rows=artifact.total_rows,
                total_columns=artifact.total_columns,
                missing_columns=artifact.missing_columns,
                dtype_errors=artifact.dtype_errors,
                null_threshold_errors=artifact.null_threshold_errors,
                allowed_value_errors=artifact.allowed_value_errors,
                uniqueness_errors=artifact.uniqueness_errors,
                range_errors=artifact.range_errors,
                validated_columns=artifact.validated_columns,
                schema_version=artifact.schema_version,
                validation_message=(
                    f"{artifact.validation_message} | " f"Report Saved At: {report_path}"
                ),
            )

        except Exception as e:

            self.logger.exception(f"Error During Data Validation: {e}")

            raise CustomException(
                error=e,
                error_detail=sys,
            )
