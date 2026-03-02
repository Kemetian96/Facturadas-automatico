# Facturadas automatico

Generador de reporte `Confirmadas vs Pagadas` para PostgreSQL con salida en Excel.

## Estructura

```text
facturadas/
  app/        # Entrypoints (CLI)
  config/     # Carga de configuracion y .env
  db/         # Acceso a base de datos
  export/     # Adaptadores de salida (Excel)
  reports/    # Casos de uso del negocio
  utils/      # Utilidades comunes
sql/          # SQL externo versionado por pasos
```

## Configuracion

1. Copia `.env.example` a `.env`.
2. Completa credenciales de base de datos.

Variables principales:
- `DB_HOST`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_PORT`
- `DB_SSLMODE`
- `DB_CONNECT_TIMEOUT`
- `REPORT_OUTPUT_PATH`

## Ejecucion

```powershell
python app.py
```

Con parametros:

```powershell
python app.py --fecha-inicio 2026-03-01 --fecha-fin 2026-03-02 --output C:\temp\reporte.xlsx
```

## Build ejecutable

```powershell
python -m PyInstaller --onefile --windowed --icon=reporte.ico app.py
```

