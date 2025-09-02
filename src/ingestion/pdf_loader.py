from __future__ import annotations
from pathlib import Path
import pdfplumber
import pandas as pd


def load_pdf_text(path: str | Path) -> pd.DataFrame:
	p = Path(path)
	if not p.exists():
		raise FileNotFoundError(f"PDF not found: {p}")
	texts: list[str] = []
	with pdfplumber.open(str(p)) as pdf:
		for page in pdf.pages:
			text = page.extract_text() or ""
			if text:
				texts.append(text)
	return pd.DataFrame({"text": texts})
