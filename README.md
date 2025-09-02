## AI DataOps Pipeline (Python)

End-to-end ML lifecycle: ingestion → preprocessing → model serving → monitoring → retraining → CI/CD.

---

### Overview

This project provides a modular, production-ready pipeline for machine learning operations, including data ingestion, preprocessing, model training and serving, monitoring, automated retraining, and CI/CD integration.

---

### Requirements

- Python 3.9+
- Docker & Docker Compose

---

### Quickstart

1. **Install dependencies**
    ```bash
    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    ```

2. **Run API locally**
    ```bash
    uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
    ```

3. **Run full stack (API + Prometheus + Grafana)**
    ```bash
    docker compose up --build
    ```

---

### Configuration

- Environment variables: see `.env.example` or set directly in your environment.
- YAML configs: `config/` directory.
- Docker Compose: `docker-compose.yml` for service orchestration.

---

### Layout

- `src/` — core modules: ingestion, preprocessing, modeling, API, monitoring, workflows
- `config/` — YAML configs, `.env` for secrets
- `docker/` — Docker, Prometheus, Grafana configs
- `.github/workflows/` — CI/CD pipelines

---

### Features

- **Data ingestion:** CSV, PDF, API sources
- **Preprocessing:** cleaning, schema validation, chunking
- **Modeling:** sklearn baseline, persisted with joblib, versioned
- **Serving:** FastAPI endpoints (`/predict`, `/health`, `/metrics`)
- **Monitoring:** Prometheus metrics, Grafana dashboards
- **Retraining:** Prefect flow, scheduled or manual
- **Deployment:** Docker Compose, GitHub Actions CI/CD
- **API Docs:** [Swagger UI](http://localhost:8000/docs) (when running)
- **Security:** Environment-based config, no secrets in code

---

### Example Usage

**Request:**
```bash
curl -X POST http://localhost:8000/predict \
  -H 'Content-Type: application/json' \
  -d '{"features": [1.2, 3.4, 5.6]}'
```

**Response:**
```json
{"prediction": 0}
```

---

### Testing

Run unit tests:
```bash
pytest
```

---
  
### Contributing

Contributions welcome! Please open issues or pull requests.

---

### License

MIT
