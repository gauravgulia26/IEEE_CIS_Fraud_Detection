import zipfile
import os
from tqdm import tqdm
import yaml
from pathlib import Path
from typing import Optional, Dict, Type
import pandas as pd
from pydantic import BaseModel
from box import Box


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


def load_yaml_key(file_path: str, key: str) -> Dict:
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


def fast_read_csv(
    file_path: str | Path,
    chunk_size: int = 100000,
    usecols: Optional[list[str]] = None,
    dtype: Optional[dict] = None,
    show_progress: bool = True,
    low_memory: bool = False,
) -> pd.DataFrame:
    """
    Efficient CSV reader with:
    - chunk loading
    - progress bar
    - lower memory usage
    - reusable architecture

    Parameters
    ----------
    file_path : str | Path
        CSV file path

    chunk_size : int
        Number of rows per chunk

    usecols : list[str]
        Specific columns to load

    dtype : dict
        Explicit dtype mapping

    show_progress : bool
        Whether to show tqdm progress bar

    low_memory : bool
        Pandas low_memory option

    Returns
    -------
    pd.DataFrame
    """

    file_path = Path(file_path)

    total_rows = sum(1 for _ in open(file_path, "r")) - 1

    chunks = []

    reader = pd.read_csv(
        file_path,
        chunksize=chunk_size,
        engine="c",
        usecols=usecols,
        dtype=dtype,
        low_memory=low_memory,
    )

    if show_progress:

        with tqdm(
            total=total_rows,
            desc=f"Loading {file_path.name}",
        ) as pbar:

            for chunk in reader:

                chunks.append(chunk)

                pbar.update(len(chunk))

    else:

        for chunk in reader:

            chunks.append(chunk)

    df = pd.concat(
        chunks,
        ignore_index=True,
    )

    return df


def save_artifact(artifact: BaseModel, file_path: Path) -> None:
    """
    Save Pydantic artifact to JSON file.

    Args:
        artifact: Pydantic BaseModel instance
        file_path: Path to save JSON
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_text(artifact.model_dump_json(indent=4))


def load_artifact(file_path: Path) -> Box:
    """
    Load JSON artifact as ConfigBox-like object (dot notation).

    Args:
        file_path: Path to artifact JSON

    Returns:
        Box object (dot-access dictionary)
    """
    return Box.from_json(filename=str(file_path))
