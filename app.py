from datetime import datetime, timedelta
from services.cuid import fecha_a_cuid
from services.consulta import ejecutar_consulta_sql
from export.excel import exportar_excel

def obtener_fechas_ayer():
    hoy = datetime.now()
    ayer = datetime.now() - timedelta(days=1)
    fecha_hoy = hoy.strftime("%Y-%m-%d")
    fecha_ayer = ayer.strftime("%Y-%m-%d")
    print(f"Fecha inicio: {fecha_ayer}")
    print(f"Fecha fin: {fecha_hoy}")
    return fecha_hoy,fecha_ayer

if __name__ == "__main__":
    try:
        fecha_hoy,fecha_ayer = obtener_fechas_ayer()

        rows, cols = ejecutar_consulta_sql(
            fecha_a_cuid(fecha_ayer),
            fecha_a_cuid(fecha_hoy)
        )

        ruta = rf"G:\Unidades compartidas\SAC - ADMIN\05.- Reportes\Post Venta\reporte_confirmadas.xlsx"
        exportar_excel(rows, cols, ruta)

    except Exception as e:
        # Para logs (no ventanas)
        print(f"ERROR: {e}")
