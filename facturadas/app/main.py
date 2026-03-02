import argparse
import logging
from datetime import datetime, timedelta

from facturadas.config.configuracion import obtener_configuracion
from facturadas.reports.servicio_confirmadas import (
    generar_reporte_confirmadas_vs_pagadas,
)


REGISTRO = logging.getLogger(__name__)


def _fechas_por_defecto() -> tuple[str, str]:
    hoy = datetime.now()
    ayer = hoy - timedelta(days=1)
    return ayer.strftime("%Y-%m-%d"), hoy.strftime("%Y-%m-%d")


def _parsear_argumentos() -> argparse.Namespace:
    fecha_inicio_defecto, fecha_fin_defecto = _fechas_por_defecto()
    configuracion = obtener_configuracion()

    parser = argparse.ArgumentParser(
        description="Genera reporte de ordenes confirmadas vs pagadas."
    )
    parser.add_argument(
        "--fecha-inicio", default=fecha_inicio_defecto, help="YYYY-MM-DD"
    )
    parser.add_argument("--fecha-fin", default=fecha_fin_defecto, help="YYYY-MM-DD")
    parser.add_argument(
        "--output",
        default=configuracion.ruta_salida_por_defecto,
        help="Ruta del archivo .xlsx de salida",
    )
    return parser.parse_args()


def main() -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    args = _parsear_argumentos()

    REGISTRO.info("Fecha inicio: %s", args.fecha_inicio)
    REGISTRO.info("Fecha fin: %s", args.fecha_fin)
    REGISTRO.info("Salida: %s", args.output)

    generar_reporte_confirmadas_vs_pagadas(
        fecha_inicio=args.fecha_inicio,
        fecha_fin=args.fecha_fin,
        ruta_salida=args.output,
    )
    REGISTRO.info("Reporte generado correctamente.")
    return 0
