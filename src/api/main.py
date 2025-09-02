from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from prometheus_fastapi_instrumentator import Instrumentator
from loguru import logger
from src.config.settings import settings
from src.modeling.model import ModelService
from src.monitoring.metrics import metrics

app = FastAPI(title="AI DataOps Pipeline", description="Predict API with monitoring and feedback.")
model_service = ModelService()


class PredictRequest(BaseModel):
    features: list[float] = Field(..., description="Numeric feature vector", examples=[[1.0, 2.0, 3.0]])


class PredictResponse(BaseModel):
    prediction: float = Field(..., description="Predicted value", examples=[6.0])
    version: float = Field(..., description="Model version epoch")


class FeedbackRequest(BaseModel):
    features: list[float]
    label: float


@app.on_event("startup")
def _startup() -> None:
    Instrumentator().instrument(app).expose(app)
    model_service.load_or_initialize()
    metrics.model_version.set(model_service.version)
    logger.info("API started in {} mode", settings.environment)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "env": settings.environment}


@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest) -> PredictResponse:
    try:
        with metrics.request_latency.time():
            prediction = model_service.predict(payload.features)
            metrics.request_counter.inc()
            return PredictResponse(prediction=float(prediction), version=model_service.version)
    except Exception as exc:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=400, detail=f"Prediction error: {exc}")


@app.post("/feedback")
def feedback(payload: FeedbackRequest) -> dict:
    try:
        pred = model_service.predict(payload.features)
        error = abs(pred - payload.label)
        metrics.observe_feedback(prediction=float(pred), label=float(payload.label))
        return {"status": "recorded", "abs_error": error}
    except Exception as exc:
        logger.exception("Feedback processing failed")
        raise HTTPException(status_code=400, detail=f"Feedback error: {exc}")
