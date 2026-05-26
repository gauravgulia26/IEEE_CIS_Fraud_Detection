# Intermediate Artifacts during stages
from typing import NamedTuple
import pandas as pd


class InterReadArtifact(NamedTuple):
    train_identity_df: pd.DataFrame = None
    test_identity_df: pd.DataFrame = None
    train_transaction_df: pd.DataFrame = None
    test_transaction_df: pd.DataFrame = None
    merged_final_df: pd.DataFrame = None


class InterSplitArtifact(NamedTuple):
    train_split_df: pd.DataFrame = None
    test_split_df: pd.DataFrame = None
