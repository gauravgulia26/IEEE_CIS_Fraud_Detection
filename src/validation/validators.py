from pathlib import Path
from src.utils import load_yaml
from src.core.logging import get_logger
from src.configs.paths import INGESTION_LOG_DIR_PATH, INGESTION_COMP
from typing import List
import pandas as pd


class SchemaValidator:
    def __init__(self, schema_file_path: Path, key_name: str, df_path: Path):
        self.schema_path = schema_file_path
        self.key = key_name
        self.schema_config = load_yaml(file_path=schema_file_path, key=key_name)
        self.df_path = df_path
        self.logger = get_logger(name=INGESTION_COMP, log_dir_path=INGESTION_LOG_DIR_PATH)

    def __read_df(self) -> pd.DataFrame:
        self.logger.info("Reading CSV........")
        return pd.read_csv(self.df_path, nrows=2)

    def __validate_key(self):
        df = self.__read_df()
        df_cols = df.columns.tolist()
        target_col = self.schema_config["foreign_key"]

        if "foreign_key" not in list(self.schema_config.keys()):
            self.logger.exception("Error While Reading Foreign Key in YAML")
            raise ValueError(
                f"[foreign_key] not present in Schema File at Path: {self.schema_path.as_posix()}"
            )

        if target_col not in df_cols:
            self.logger.exception("Error While Searching Foreign Key")
            raise ValueError(
                f"Foreign Key not Present in {self.df_path.stem}, Merging is not possible !!"
            )
        self.logger.info("Foreign Key Present, Validating Columns")

    def __validate_columns(self):
        required_cols = self.schema_config["required_columns"]
        df_cols = self.__read_df().columns.tolist()

        diff = set(df_cols) - set(required_cols)

        if diff:
            self.logger.exception("Error While Checking Columns")
            self.logger.info(f'REQUIRED COLUMNS: {",".join(required_cols)}')
            raise ValueError("One or More Columns is not present in Dataframe.")
        self.logger.info("Validation Completed ")

    def run(self):
        self.__validate_key()
        self.__validate_columns()
