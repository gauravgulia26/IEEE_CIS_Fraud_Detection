from src.components.data_ingestion import IngestData
from src.components.data_validation import DataValidation
from src.configs.managers import ConfigurationManager
from src.entity.artifacts import DataIngestionArtifact
from src.core.exception import CustomException
from rich import print
import sys

try:
    # Stage-1
    ingestion_cfg = ConfigurationManager()
    ingestion_obj = IngestData(configs=ingestion_cfg, artifacts=DataIngestionArtifact)
    ingestion_artifact = ingestion_obj.run()

    # Stage-2
    validation_obj = DataValidation(ingestion_artifact=ingestion_artifact)
    validation_artifact = validation_obj.run()

except Exception as e:
    err = CustomException(error=e, error_detail=sys)
    print(f"Error: {e} occured ")
    raise err
