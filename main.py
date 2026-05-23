from components.data_ingestion import IngestData
from src.core.exception import CustomException
from configs.managers import ConfigurationManager
from entity.artifacts import DataIngestionArtifact
from rich import print
import sys

obj = IngestData(configs=ConfigurationManager(), artifacts=ArtifactsManager())
obj.run()
