from src.components.ingestion import IngestData
from src.custom_exception import CustomException
from src.configs.manager import ConfigurationManager
from src.entity.manager import ArtifactsManager
from rich import print
import sys

obj = IngestData(configs=ConfigurationManager(), artifacts=ArtifactsManager())
obj.run()
