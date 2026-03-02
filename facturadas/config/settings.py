import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_PATH = (
    r"G:\Unidades compartidas\SAC - ADMIN\05.- Reportes\Post Venta\reporte_confirmadas.xlsx"
)


def _load_env_file() -> None:
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value


@dataclass(frozen=True)
class Settings:
    db_config: dict
    default_output_path: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    _load_env_file()
    db_config = {
        "host": _require_env("DB_HOST"),
        "dbname": _require_env("DB_NAME"),
        "user": _require_env("DB_USER"),
        "password": _require_env("DB_PASSWORD"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "sslmode": os.getenv("DB_SSLMODE", "require"),
        "connect_timeout": int(os.getenv("DB_CONNECT_TIMEOUT", "10")),
    }
    default_output_path = os.getenv("REPORT_OUTPUT_PATH", DEFAULT_OUTPUT_PATH)
    return Settings(db_config=db_config, default_output_path=default_output_path)

