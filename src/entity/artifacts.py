# Artifacts to output in stages
from pydantic import BaseModel, Field
from pathlib import Path


class DataIngestionArtifact(BaseModel):
    ident_train_data_path: Path = Field(
        description="Directory Containing the Identity Training Data"
    )
    ident_test_data_path: Path = Field(description="Directory Containing the Identity Test Data")
    trns_train_data_path: Path = Field(
        description="Directory Containing the Transaction Train Data"
    )
    trns_test_data_path: Path = Field(
        description="Directory Containing the Transactions Test Data"
    )
    