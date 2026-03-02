from facturadas.db.repositorio_reporte import RepositorioReporte
from facturadas.export.excel import exportar_excel
from facturadas.utils.cuid import fecha_a_cuid


def generar_reporte_confirmadas_vs_pagadas(
    fecha_inicio: str, fecha_fin: str, ruta_salida: str
) -> None:
    repositorio = RepositorioReporte()
    rows, cols = repositorio.obtener_confirmadas_vs_pagadas(
        fecha_a_cuid(fecha_inicio), fecha_a_cuid(fecha_fin)
    )
    exportar_excel(rows=rows, cols=cols, ruta=ruta_salida)
