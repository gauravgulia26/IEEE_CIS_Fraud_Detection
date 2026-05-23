# Intermediate Artifacts during stages
from typing import NamedTuple
import pandas as pd


class InterReadArtifact(NamedTuple):
    train_identity_df: pd.DataFrame
    test_identity_df: pd.DataFrame
    train_transaction_df: pd.DataFrame
    test_transaction_df: pd.DataFrame
    merged_final_df: pd.DataFrame


class InterSplitArtifact(NamedTuple):
    train_split_df: pd.DataFrame
    test_split_df: pd.DataFrame
