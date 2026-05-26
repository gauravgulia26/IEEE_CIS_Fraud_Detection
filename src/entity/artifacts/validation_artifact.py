from typing import NamedTuple, Any
from pathlib import Path


class ValidationArtifact(NamedTuple):

    validation_status: bool

    validated_file_path: Path

    total_rows: int

    total_columns: int

    missing_columns: list[str]

    dtype_errors: list[dict[str, Any]]

    null_threshold_errors: list[dict[str, Any]]

    allowed_value_errors: list[dict[str, Any]]

    uniqueness_errors: list[dict[str, Any]]

    range_errors: list[str]

    validated_columns: list[str]

    schema_version: str

    validation_message: str
