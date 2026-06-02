# Artifacts to output in stages

from pydantic import BaseModel
from pathlib import Path


class DataIngestionArtifact(BaseModel):
    ident_train_data_path: Path
    ident_test_data_path: Path
    trns_train_data_path: Path
    trns_test_data_path: Path
    merged_file_path: Path
