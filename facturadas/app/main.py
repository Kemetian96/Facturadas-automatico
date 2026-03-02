import argparse
import logging
from datetime import datetime, timedelta

from facturadas.config.settings import get_settings
from facturadas.reports.confirmadas_service import (
    generar_reporte_confirmadas_vs_pagadas,
)


LOGGER = logging.getLogger(__name__)


def _default_dates() -> tuple[str, str]:
    hoy = datetime.now()
    ayer = hoy - timedelta(days=1)
    return ayer.strftime("%Y-%m-%d"), hoy.strftime("%Y-%m-%d")


def _parse_args() -> argparse.Namespace:
    default_inicio, default_fin = _default_dates()
    settings = get_settings()

    parser = argparse.ArgumentParser(
        description="Genera reporte de ordenes confirmadas vs pagadas."
    )
    parser.add_argument("--fecha-inicio", default=default_inicio, help="YYYY-MM-DD")
    parser.add_argument("--fecha-fin", default=default_fin, help="YYYY-MM-DD")
    parser.add_argument(
        "--output",
        default=settings.default_output_path,
        help="Ruta del archivo .xlsx de salida",
    )
    return parser.parse_args()


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    args = _parse_args()

    LOGGER.info("Fecha inicio: %s", args.fecha_inicio)
    LOGGER.info("Fecha fin: %s", args.fecha_fin)
    LOGGER.info("Salida: %s", args.output)

    generar_reporte_confirmadas_vs_pagadas(
        fecha_inicio=args.fecha_inicio,
        fecha_fin=args.fecha_fin,
        ruta_salida=args.output,
    )
    LOGGER.info("Reporte generado correctamente.")
    return 0

