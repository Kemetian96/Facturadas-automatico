import logging
from pathlib import Path
from typing import Sequence

import psycopg2

from facturadas.config.settings import get_settings


LOGGER = logging.getLogger(__name__)
SQL_DIR = Path(__file__).resolve().parents[2] / "sql"


def _read_sql(name: str) -> str:
    return (SQL_DIR / name).read_text(encoding="utf-8")


class ReportRepository:
    def __init__(self) -> None:
        self.settings = get_settings()

    def fetch_confirmadas_vs_pagadas(
        self, cuid_desde: int, cuid_hasta: int
    ) -> tuple[list[tuple], list[str]]:
        step_queries: Sequence[tuple[str, str, tuple]] = (
            ("Paso 1", "step_01_orders_changelogs.sql", (cuid_desde, cuid_hasta)),
            ("Paso 2", "step_02_parse_changelog.sql", tuple()),
            ("Paso 3", "step_03_confirmadas.sql", tuple()),
            ("Paso 4", "step_04_pagadas.sql", tuple()),
        )

        with psycopg2.connect(**self.settings.db_config) as conn:
            conn.autocommit = True
            with conn.cursor() as cur:
                for step_name, sql_file, params in step_queries:
                    LOGGER.info("Executing %s", step_name)
                    cur.execute(_read_sql(sql_file), params)

                cur.execute(_read_sql("step_05_final_select.sql"))
                rows = cur.fetchall()
                cols = [column[0] for column in cur.description]
                return rows, cols

