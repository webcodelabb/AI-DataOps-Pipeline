import pandas as pd
from src.ingestion.csv_loader import load_csv
from src.preprocessing.clean import basic_clean
from src.modeling.model import ModelService


def test_basic_clean():
	df = pd.DataFrame({"a": [1, 1, None], "b": [2, 2, None]})
	out = basic_clean(df)
	assert len(out) == 2


def test_model_predict_sum_fallback():
	svc = ModelService()
	pred = svc.predict([1.0, 2.0, 3.0])
	assert isinstance(pred, float)
