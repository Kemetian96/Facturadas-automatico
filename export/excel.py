import pandas as pd


def exportar_excel(rows, cols, ruta):
    df = pd.DataFrame(rows, columns=[
            "ID_ORDERS",
            "ORDEN",
            "COLABORADOR",
            "DOCUMENTO",
            "DIA PAGADA",
            "ESTADO",
            "DIA CONFIRMADA",
            "ESTADO2",
            "FECHA PAGADA",
            "FECHA CONFIRMADA",
            "HORA PAGADA",
            "HORA CONFIRMADA",
            "DIFERENCIA"
    ])

    df["FECHA CONFIRMADA"] = pd.to_datetime(
        df["FECHA CONFIRMADA"], errors="coerce"
    ).dt.strftime("%d/%m/%Y")

    df = df.astype(str)

    with pd.ExcelWriter(ruta, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="Reporte",
            freeze_panes=(1, 0)
        )
