from __future__ import annotations
import pandas as pd
from pathlib import Path


def load_csv(path: str | Path) -> pd.DataFrame:
	p = Path(path)
	if not p.exists():
		raise FileNotFoundError(f"CSV not found: {p}")
	return pd.read_csv(p)
