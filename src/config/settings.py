from pydantic import BaseModel
import os
from dotenv import load_dotenv
import yaml


class AppSettings(BaseModel):
    environment: str = "dev"
    model_dir: str = "./models"
    data_dir: str = "./data"
    log_level: str = "INFO"
    prometheus_port: int = 8000

    @classmethod
    def load(cls) -> "AppSettings":
        # .env
        load_dotenv()
        # base from env vars
        settings = cls(
            environment=os.getenv("ENV", "dev"),
            model_dir=os.getenv("MODEL_DIR", "./models"),
            data_dir=os.getenv("DATA_DIR", "./data"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            prometheus_port=int(os.getenv("PROMETHEUS_PORT", "8000")),
        )
        # optional YAML override
        config_path = os.getenv("CONFIG_YAML", "config/config.yaml")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                for key, value in data.items():
                    if hasattr(settings, key):
                        setattr(settings, key, value)
        return settings


settings = AppSettings.load()
