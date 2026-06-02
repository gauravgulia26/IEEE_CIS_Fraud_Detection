from src.components.data_ingestion import IngestData
from src.configs.managers import ConfigurationManager
from src.entity.artifacts import DataIngestionArtifact
from src.core.exception import CustomException
import sys


class DataIngestionPipeline:
    def __init__(self):
        self.config_manager = ConfigurationManager()
        self.ingestion_artifact = None

    def run(self):
        try:
            ingestion_obj = IngestData(
                configs=self.config_manager, artifacts=DataIngestionArtifact
            )

            self.ingestion_artifact = ingestion_obj.run()

        except Exception as e:
            raise CustomException(error=e, error_detail=sys)


if __name__ == "__main__":
    pipeline = DataIngestionPipeline()
    pipeline.run()
