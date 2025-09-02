from __future__ import annotations
import os
from datetime import timedelta
import pandas as pd
from prefect import flow, task, get_run_logger
from prefect.task_runners import ConcurrentTaskRunner
from sklearn.linear_model import LinearRegression
import joblib
from src.config.settings import settings
from src.preprocessing.clean import basic_clean
from src.preprocessing.validate import validate_schema


@task
def load_training_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Training data not found: {path}")
    return pd.read_csv(path)


@task
def prepare_data(df: pd.DataFrame, target_col: str) -> tuple[pd.DataFrame, pd.Series]:
    df = basic_clean(df)
    validate_schema(df, {target_col: "numeric"})
    feature_cols = [c for c in df.columns if c != target_col]
    X = df[feature_cols]
    y = pd.to_numeric(df[target_col], errors="coerce")
    if y.isna().any():
        raise ValueError("Target column contains non-numeric values after coercion")
    return X, y


@task
def train_model(X: pd.DataFrame, y: pd.Series, model_dir: str) -> str:
    model = LinearRegression()
    model.fit(X, y)
    os.makedirs(model_dir, exist_ok=True)
    version = str(int(pd.Timestamp.utcnow().timestamp()))
    path = os.path.join(model_dir, f"model_{version}.joblib")
    joblib.dump(model, path)
    return path


@flow(name="retrain-model", task_runner=ConcurrentTaskRunner())
def retrain_flow(data_path: str | None = None, target_col: str = "target") -> str:
    logger = get_run_logger()
    csv_path = data_path or os.path.join(settings.data_dir, "train.csv")
    logger.info(f"Loading training data from {csv_path}")
    df = load_training_data(csv_path)
    X, y = prepare_data(df, target_col)
    logger.info("Training model...")
    model_path = train_model(X, y, settings.model_dir)
    logger.info(f"Saved model to {model_path}")
    return model_path


if __name__ == "__main__":
    print(retrain_flow())
