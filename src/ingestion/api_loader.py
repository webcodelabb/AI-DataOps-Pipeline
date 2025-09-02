from __future__ import annotations
from typing import Any, Dict, Optional
import requests
import pandas as pd


def fetch_json(url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> pd.DataFrame:
    resp = requests.get(url, params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, list):
        return pd.DataFrame(data)
    return pd.DataFrame([data])
