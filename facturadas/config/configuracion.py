import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


RAIZ_PROYECTO = Path(__file__).resolve().parents[2]
RUTA_SALIDA_POR_DEFECTO = (
    r"G:\Unidades compartidas\SAC - ADMIN\05.- Reportes\Post Venta\reporte_confirmadas.xlsx"
)


def _cargar_env() -> None:
    ruta_env = RAIZ_PROYECTO / ".env"
    if not ruta_env.exists():
        return

    for linea in ruta_env.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        clave = clave.strip()
        valor = valor.strip().strip('"').strip("'")
        if clave and clave not in os.environ:
            os.environ[clave] = valor


def _obligatoria(nombre: str) -> str:
    valor = os.getenv(nombre)
    if not valor:
        raise RuntimeError(f"Falta variable de entorno obligatoria: {nombre}")
    return valor


@dataclass(frozen=True)
class Configuracion:
    config_db: dict
    ruta_salida_por_defecto: str


@lru_cache(maxsize=1)
def obtener_configuracion() -> Configuracion:
    _cargar_env()
    config_db = {
        "host": _obligatoria("DB_HOST"),
        "dbname": _obligatoria("DB_NAME"),
        "user": _obligatoria("DB_USER"),
        "password": _obligatoria("DB_PASSWORD"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "sslmode": os.getenv("DB_SSLMODE", "require"),
        "connect_timeout": int(os.getenv("DB_CONNECT_TIMEOUT", "10")),
    }
    ruta_salida_por_defecto = os.getenv(
        "REPORT_OUTPUT_PATH", RUTA_SALIDA_POR_DEFECTO
    )
    return Configuracion(
        config_db=config_db, ruta_salida_por_defecto=ruta_salida_por_defecto
    )
