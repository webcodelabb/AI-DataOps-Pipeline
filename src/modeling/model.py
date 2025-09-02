from __future__ import annotations
import os
import time
import glob
import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
from src.config.settings import settings
from src.monitoring.metrics import metrics


class ModelService:
    def __init__(self) -> None:
        self.model_dir = settings.model_dir
        self._model: LinearRegression | None = None
        self._version: float = 0.0

    def _latest_model_path(self) -> str | None:
        files = sorted(glob.glob(os.path.join(self.model_dir, "model_*.joblib")))
        return files[-1] if files else None

    def load_or_initialize(self) -> None:
        os.makedirs(self.model_dir, exist_ok=True)
        path = self._latest_model_path()
        if path and os.path.exists(path):
            self._model = joblib.load(path)
            try:
                self._version = float(os.path.basename(path).split("_")[1].split(".")[0])
            except Exception:
                self._version = 0.0
        else:
            self._model = LinearRegression()
            self._model.coef_ = np.array([1.0])
            self._model.intercept_ = 0.0
            self._model.n_features_in_ = 1
            self._version = 0.0
        metrics.model_version.set(self._version)

    def predict(self, features: list[float]) -> float:
        if self._model is None:
            self.load_or_initialize()
        arr = np.array(features, dtype=float).reshape(1, -1)
        try:
            pred = float(self._model.predict(arr)[0])  # type: ignore[arg-type]
        except Exception:
            pred = float(arr.sum())
        return pred

    def save(self) -> str | None:
        if self._model is None:
            return None
        os.makedirs(self.model_dir, exist_ok=True)
        version = time.time()
        path = os.path.join(self.model_dir, f"model_{int(version)}.joblib")
        joblib.dump(self._model, path)
        self._version = version
        metrics.model_version.set(self._version)
        return path

    @property
    def model(self) -> LinearRegression | None:
        return self._model

    @property
    def version(self) -> float:
        return self._version
