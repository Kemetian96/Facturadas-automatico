import logging
from pathlib import Path
from typing import Sequence

import psycopg2

from facturadas.config.configuracion import obtener_configuracion


REGISTRO = logging.getLogger(__name__)
DIR_SQL = Path(__file__).resolve().parents[2] / "sql"


def _leer_sql(nombre: str) -> str:
    return (DIR_SQL / nombre).read_text(encoding="utf-8")


class RepositorioReporte:
    def __init__(self) -> None:
        self.configuracion = obtener_configuracion()

    def obtener_confirmadas_vs_pagadas(
        self, cuid_desde: int, cuid_hasta: int
    ) -> tuple[list[tuple], list[str]]:
        consultas_por_paso: Sequence[tuple[str, str, tuple]] = (
            ("Paso 1", "step_01_orders_changelogs.sql", (cuid_desde, cuid_hasta)),
            ("Paso 2", "step_02_parse_changelog.sql", tuple()),
            ("Paso 3", "step_03_confirmadas.sql", tuple()),
            ("Paso 4", "step_04_pagadas.sql", tuple()),
        )

        with psycopg2.connect(**self.configuracion.config_db) as conexion:
            conexion.autocommit = True
            with conexion.cursor() as cursor:
                for nombre_paso, archivo_sql, parametros in consultas_por_paso:
                    REGISTRO.info("Ejecutando %s", nombre_paso)
                    sql = _leer_sql(archivo_sql)
                    if parametros:
                        cursor.execute(sql, parametros)
                    else:
                        cursor.execute(sql)

                cursor.execute(_leer_sql("step_05_final_select.sql"))
                filas = cursor.fetchall()
                columnas = [columna[0] for columna in cursor.description]
                return filas, columnas
