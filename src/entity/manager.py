from src.entity.artifacts import DataIngestionArtifact


class ArtifactsManager:
    """
    Artifact Manager to Output Each Component Availaible Artifacts
    """

    def get_ingestion_artifact(self):
        return DataIngestionArtifact
