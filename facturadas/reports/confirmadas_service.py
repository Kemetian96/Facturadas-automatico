from facturadas.db.report_repository import ReportRepository
from facturadas.export.excel import exportar_excel
from facturadas.utils.cuid import fecha_a_cuid


def generar_reporte_confirmadas_vs_pagadas(
    fecha_inicio: str, fecha_fin: str, ruta_salida: str
) -> None:
    repo = ReportRepository()
    rows, cols = repo.fetch_confirmadas_vs_pagadas(
        fecha_a_cuid(fecha_inicio), fecha_a_cuid(fecha_fin)
    )
    exportar_excel(rows=rows, cols=cols, ruta=ruta_salida)

