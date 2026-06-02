from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from pathlib import Path


class ValidationArtifact(BaseModel):

    validation_status: Optional[bool] = None

    validated_file_path: Optional[Path] = None

    total_rows: Optional[int] = None

    total_columns: Optional[int] = None

    missing_columns: Optional[List[str]] = None

    dtype_errors: Optional[Dict[str, Any]] = None

    null_threshold_errors: Optional[List[Dict[str, Any]]] = None

    allowed_value_errors: Optional[List[Dict[str, Any]]] = None

    uniqueness_errors: Optional[List[Dict[str, Any]]] = None

    range_errors: Optional[List[str]] = None

    validated_columns: Optional[List[str]] = None

    schema_version: Optional[str] = None

    validation_message: Optional[str] = None
