from src.components.data_validation import DataValidation
from src.core.exception import CustomException
from src.configs.paths import INGESTION_ARTIFACT_DIR_PATH
import sys


class DataValidationPipeline:
    def __init__(self):
        self.validation_artifact = None

    def run(self):
        try:

            validation_obj = DataValidation(ingestion_artifact_path=INGESTION_ARTIFACT_DIR_PATH)

            self.validation_artifact = validation_obj.run()

        except Exception as e:
            raise CustomException(error=e, error_detail=sys)


if __name__ == "__main__":
    pipeline = DataValidationPipeline()
    pipeline.run()
