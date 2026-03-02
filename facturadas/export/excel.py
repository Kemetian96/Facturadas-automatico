from pathlib import Path

import pandas as pd


OUTPUT_COLUMNS = [
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
    "DIFERENCIA",
]

SOURCE_TO_OUTPUT = {
    "id_orders": "ID_ORDERS",
    "uid_orders": "ORDEN",
    "usuario_que_confirma": "COLABORADOR",
    "documento_usuario_que_confirma": "DOCUMENTO",
    "dia_pagadas": "DIA PAGADA",
    "estado_pagada": "ESTADO",
    "dia_confirmada": "DIA CONFIRMADA",
    "estado_confirmadas": "ESTADO2",
    "fecha_pagadas": "FECHA PAGADA",
    "fecha_confirmada": "FECHA CONFIRMADA",
    "hora_pagada": "HORA PAGADA",
    "hora_confirmada": "HORA CONFIRMADA",
    "diferencia": "DIFERENCIA",
}


def exportar_excel(rows: list[tuple], cols: list[str], ruta: str) -> None:
    if len(cols) != len(SOURCE_TO_OUTPUT):
        raise ValueError(
            f"Unexpected number of columns. Expected {len(SOURCE_TO_OUTPUT)}, got {len(cols)}"
        )

    df = pd.DataFrame(rows, columns=cols)
    df = df.rename(columns=SOURCE_TO_OUTPUT)
    missing_columns = [col for col in OUTPUT_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing expected columns: {missing_columns}")
    df = df[OUTPUT_COLUMNS]

    df["FECHA CONFIRMADA"] = pd.to_datetime(
        df["FECHA CONFIRMADA"], errors="coerce"
    ).dt.strftime("%d/%m/%Y")
    df = df.astype(str)

    output_path = Path(ruta)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Reporte", freeze_panes=(1, 0))

