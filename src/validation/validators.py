from pathlib import Path
from typing import Any

import pandas as pd

from src.utils import load_yaml
from src.core.logging import get_logger
from src.configs.paths import (
    INGESTION_LOG_DIR_PATH,
    INGESTION_COMP,
)


class SchemaValidator:

    def __init__(
        self,
        schema_file_path: Path,
        key_name: str,
        df_path: Path,
    ):

        self.schema_path = schema_file_path

        self.key = key_name

        self.df_path = df_path

        self.schema_config = load_yaml(
            file_path=schema_file_path,
            key=key_name,
        )

        self.logger = get_logger(
            name=INGESTION_COMP,
            log_dir_path=INGESTION_LOG_DIR_PATH,
        )

    def __read_df(
        self,
        nrows: int = 1000,
    ) -> pd.DataFrame:

        self.logger.info(f"Reading Dataframe: {self.df_path.name}")

        return pd.read_parquet(self.df_path, engine="pyarrow")

    def __validate_foreign_key(
        self,
        df: pd.DataFrame,
    ) -> None:

        foreign_key = self.schema_config.get("foreign_key")

        if foreign_key is None:

            raise ValueError("[foreign_key] not found in schema config")

        if foreign_key not in df.columns:

            raise ValueError(f"Foreign Key [{foreign_key}] " f"not found in dataframe")

        self.logger.info("Foreign Key Validation Passed")

    def __validate_required_columns(
        self,
        df: pd.DataFrame,
    ) -> None:

        required_columns = self.schema_config.get(
            "required_columns",
            [],
        )

        missing_columns = list(set(required_columns) - set(df.columns))

        if missing_columns:

            raise ValueError(f"Missing Required Columns: " f"{missing_columns}")

        self.logger.info("Required Column Validation Passed")

    def __validate_dtypes(
        self,
        df: pd.DataFrame,
    ) -> None:

        expected_dtypes: dict[str, str] = self.schema_config.get("expected_dtypes", {})

        dtype_errors = []

        for column, expected_dtype in expected_dtypes.items():

            if column not in df.columns:
                continue

            actual_dtype = str(df[column].dtype)

            if actual_dtype != expected_dtype:

                dtype_errors.append(
                    {
                        "column": column,
                        "expected": expected_dtype,
                        "actual": actual_dtype,
                    }
                )

        if dtype_errors:

            raise ValueError(f"Dtype Validation Failed: " f"{dtype_errors}")

        self.logger.info("Dtype Validation Passed")

    def __validate_allowed_values(
        self,
        df: pd.DataFrame,
    ) -> None:

        allowed_values: dict[str, list[Any]] = self.schema_config.get("allowed_values", {})

        invalid_values = []

        for column, allowed in allowed_values.items():

            if column not in df.columns:
                continue

            unique_values = df[column].dropna().unique().tolist()

            unexpected = list(set(unique_values) - set(allowed))

            if unexpected:

                invalid_values.append(
                    {
                        "column": column,
                        "invalid_values": unexpected,
                    }
                )

        if invalid_values:

            raise ValueError(f"Allowed Value Validation Failed: " f"{invalid_values}")

        self.logger.info("Allowed Value Validation Passed")

    def __validate_null_thresholds(
        self,
        df: pd.DataFrame,
    ) -> None:

        null_thresholds = self.schema_config.get(
            "null_thresholds",
            {},
        )

        threshold_errors = []

        for column, threshold in null_thresholds.items():

            if column not in df.columns:
                continue

            null_ratio = df[column].isnull().mean()

            if null_ratio > threshold:

                threshold_errors.append(
                    {
                        "column": column,
                        "threshold": threshold,
                        "actual": round(null_ratio, 4),
                    }
                )

        if threshold_errors:

            raise ValueError(f"Null Threshold Validation Failed: " f"{threshold_errors}")

        self.logger.info("Null Threshold Validation Passed")

    def __validate_ranges(
        self,
        df: pd.DataFrame,
    ) -> None:

        range_checks = self.schema_config.get(
            "range_checks",
            {},
        )

        range_errors = []

        for column, constraints in range_checks.items():

            if column not in df.columns:
                continue

            if "min" in constraints:

                if df[column].min() < constraints["min"]:

                    range_errors.append(f"{column} below minimum")

            if "max" in constraints:

                if df[column].max() > constraints["max"]:

                    range_errors.append(f"{column} above maximum")

        if range_errors:

            raise ValueError(f"Range Validation Failed: " f"{range_errors}")

        self.logger.info("Range Validation Passed")

    def __validate_uniqueness(
        self,
        df: pd.DataFrame,
    ) -> None:

        unique_columns = self.schema_config.get(
            "uniqueness_constraints",
            [],
        )

        duplicate_errors = []

        for column in unique_columns:

            if column not in df.columns:
                continue

            duplicated = df[column].duplicated().sum()

            if duplicated > 0:

                duplicate_errors.append(
                    {
                        "column": column,
                        "duplicate_count": int(duplicated),
                    }
                )

        if duplicate_errors:

            raise ValueError(f"Uniqueness Validation Failed: " f"{duplicate_errors}")

        self.logger.info("Uniqueness Validation Passed")

    def run(self) -> None:

        try:

            self.logger.info("Schema Validation Started")

            df = self.__read_df()

            self.__validate_foreign_key(df)

            self.__validate_required_columns(df)

            self.__validate_dtypes(df)

            self.__validate_allowed_values(df)

            self.__validate_null_thresholds(df)

            self.__validate_ranges(df)

            self.__validate_uniqueness(df)

            self.logger.info("Schema Validation Completed Successfully")

        except Exception as e:

            self.logger.exception(f"Schema Validation Failed: {e}")

            raise
