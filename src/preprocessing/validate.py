from __future__ import annotations
from typing import Dict
import pandas as pd


def validate_schema(df: pd.DataFrame, schema: Dict[str, str]) -> None:
	missing = [c for c in schema.keys() if c not in df.columns]
	if missing:
		raise ValueError(f"Missing columns: {missing}")
	for col, dtype in schema.items():
		if dtype == "numeric":
			if not pd.api.types.is_numeric_dtype(df[col]):
				raise TypeError(f"Column {col} must be numeric")
		elif dtype == "string":
			if not pd.api.types.is_string_dtype(df[col]):
				raise TypeError(f"Column {col} must be string")
