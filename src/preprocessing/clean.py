from __future__ import annotations
import pandas as pd


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out = out.drop_duplicates()
    out = out.dropna(how="all")
    return out


def coerce_numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in columns:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out
