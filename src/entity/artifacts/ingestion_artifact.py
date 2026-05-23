# Artifacts to output in stages

from typing import NamedTuple
from pathlib import Path


class DataIngestionArtifact(NamedTuple):
    ident_train_data_path: Path
    ident_test_data_path: Path
    trns_train_data_path: Path
    trns_test_data_path: Path
