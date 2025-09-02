from __future__ import annotations
from typing import Iterator
import pandas as pd


def chunk_dataframe(df: pd.DataFrame, chunk_size: int) -> Iterator[pd.DataFrame]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    n = len(df)
    for i in range(0, n, chunk_size):
        yield df.iloc[i:i + chunk_size]
