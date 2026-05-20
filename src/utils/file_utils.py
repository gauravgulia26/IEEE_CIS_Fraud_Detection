import zipfile
import os
from tqdm import tqdm
import yaml
from pathlib import Path


def unzip_util(zip_path: str, extract_dir: str):
    """
    Unzip a zip file into target directory with progress bar

    Args:
        zip_path (str): Path to zip file
        extract_dir (str): Destination directory
    """

    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"Zip file not found: {zip_path}")

    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        members = zip_ref.infolist()

        print(f"Extracting {len(members)} files...")

        for member in tqdm(members, desc="Unzipping", unit="file"):
            zip_ref.extract(member, extract_dir)

    print(f"Extraction completed at: {extract_dir}")


def load_yaml_key(file_path: str, key: str):
    """
    Load a YAML file and return the value for a specific key.

    Args:
        file_path (str): Path to the YAML file.
        key (str): Key whose value needs to be retrieved.

    Returns:
        Any: Value corresponding to the key.

    Raises:
        FileNotFoundError: If file does not exist.
        KeyError: If key is not present in YAML.
        yaml.YAMLError: If YAML parsing fails.
    """
    file = Path(file_path)

    if not file.exists():
        raise FileNotFoundError(f"YAML file not found: {file_path}")

    with open(file, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"YAML parsing error: {e}")

    if key not in data:
        raise KeyError(f"Key '{key}' not found in YAML")

    return data[key]
