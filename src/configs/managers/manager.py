from src.configs.ingestion_config import DataIngestionConfig


class ConfigurationManager:
    """
    Configuration Manager to Get all availaible configurations
    """

    def get_ingestion_config(self):
        return DataIngestionConfig()
