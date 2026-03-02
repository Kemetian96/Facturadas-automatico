def ejecutar(cur, nombre: str, sql: str):
    try:
        print(f"▶ {nombre}")
        cur.execute(sql)
        print("✔ OK\n")
    except Exception as e:
        print(f"❌ ERROR en {nombre}: {e}")
        raise
