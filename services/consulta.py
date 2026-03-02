import psycopg2
from config.db import DB_CONFIG
from services.executor import ejecutar


def ejecutar_consulta_sql(cuid_desde, cuid_hasta):
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cur = conn.cursor()

    # PASO 1
    ejecutar(cur, "Paso 1", f"""
DROP TABLE IF EXISTS tt_orders_changelogs;
CREATE TEMP TABLE tt_orders_changelogs AS
SELECT id_orders, changelog, cuid_inserted AS uuid_short_modified
FROM main.t_orders_changelogs
WHERE cuid_inserted BETWEEN {cuid_desde} AND {cuid_hasta};
""")

    # PASO 2
    ejecutar(cur, "Paso 2", """
DROP TABLE IF EXISTS ttt_orders_changelogs;
CREATE TEMP TABLE ttt_orders_changelogs AS
SELECT
    id_orders,
    (changelog::jsonb ->> 'comment') AS comment,
    (changelog::jsonb ->> 'id_orders_statuses')::INT AS id_orders_statuses,
    (changelog::jsonb ->> 'id_users_updated')::BIGINT AS id_users_updated,
    (changelog::jsonb ->> 'cuid_updated')::BIGINT AS cuid_updated,
    (changelog::jsonb ->> 'uid_orders') AS uid_orders
FROM tt_orders_changelogs
WHERE (changelog::jsonb ->> 'comment') LIKE 'Estado orden:%';
""")

    # PASO 3
    ejecutar(cur, "Paso 3: tt_confirmadas_reporte", """
DROP TABLE IF EXISTS tt_confirmadas_reporte;
CREATE TEMP TABLE tt_confirmadas_reporte AS
SELECT
    t3.id_users, 
    t1.id_orders, 
    t1.uid_orders, 
    t4.order_status AS Estado,
    CONCAT_WS(' ', t3.first_name, t3.last_name) AS Colaborador,
    t3.document AS Documento,
    UPPER(TO_CHAR(
        ("main".f_u_cuid_to_datetime_v1(MIN(t1.cuid_updated)) AT TIME ZONE '-05'),
        'Day')) AS Dia_Confirmada,
    TO_CHAR(
        ("main".f_u_cuid_to_datetime_v1(MIN(t1.cuid_updated)) AT TIME ZONE '-05'),
        'YYYY-MM-DD') AS Fecha_Confirmada,
    TO_CHAR(
        ("main".f_u_cuid_to_datetime_v1(MIN(t1.cuid_updated)) AT TIME ZONE '-05'),
        'HH24:MI:SS') AS Hora_Confirmada
FROM ttt_orders_changelogs t1
INNER JOIN main.t_users t3 ON t3.id_users = t1.id_users_updated
INNER JOIN main.t_orders_statuses t4 ON t4.id_orders_statuses = t1.id_orders_statuses
WHERE t1.id_orders_statuses = 3
AND t1.comment NOT IN ('Orden enviada a nubefact', 'Estado: Finalizada')
GROUP BY 
    t1.id_orders, t3.id_users, t1.uid_orders, t4.order_status,
    t3.first_name, t3.last_name, t3.document
HAVING t3.id_users IN (
    236836,1227370,2023042906080574703,2024081920474009937,
    2024021220010944881,612222,2025030814051779132,2024080922041140780,
    2024041303072110864,2024040420295926716,2023071423591090268,
    2023081717330019273,2025091603563803145,3000995
);
""")

    # PASO 4
    ejecutar(cur, "Paso 4: tt_ultima_temporal", """
DROP TABLE IF EXISTS tt_ultima_temporal;
CREATE TEMP TABLE tt_ultima_temporal AS
SELECT  
    t2.id_orders, 
    t2.uid_orders, 
    Colaborador AS Usuario_que_confirma,
    Documento AS Documento_usuario_que_confirma,
    UPPER(TO_CHAR(
        ("main".f_u_cuid_to_datetime_v1(MIN(t1.cuid_updated)) AT TIME ZONE '-05'),
        'Day')) AS Dia_Pagadas,
    t4.order_status AS Estado_Pagada, 
    Dia_Confirmada,
    Estado AS Estado_Confirmadas, 
    TO_CHAR(
        ("main".f_u_cuid_to_datetime_v1(MIN(t1.cuid_updated)) AT TIME ZONE '-05'),
        'YYYY-MM-DD') AS Fecha_Pagadas,
    Fecha_Confirmada,
    TO_CHAR(
        ("main".f_u_cuid_to_datetime_v1(MIN(t1.cuid_updated)) AT TIME ZONE '-05'),
        'HH24:MI:SS') AS Hora_Pagada,
    Hora_Confirmada
FROM ttt_orders_changelogs t1
INNER JOIN tt_confirmadas_reporte t2 ON t2.id_orders = t1.id_orders
INNER JOIN main.t_orders_statuses t4 ON t4.id_orders_statuses = t1.id_orders_statuses
WHERE t1.id_orders_statuses = 2
GROUP BY 
    t2.uid_orders, t2.id_orders, Colaborador, Documento,
    Dia_Confirmada, Estado, Fecha_Confirmada, Hora_Confirmada,
    t4.order_status;
""")


    # QUERY FINAL
    cur.execute("""
SELECT
    id_orders,
    uid_orders,
    Usuario_que_confirma,
    Documento_usuario_que_confirma,
    Dia_Pagadas,
    Estado_Pagada,
    Dia_Confirmada,
    Estado_Confirmadas,
    Fecha_Pagadas,
    Fecha_Confirmada,
    Hora_Pagada,
    Hora_Confirmada,
(
    SELECT
    CASE
        WHEN segundos < 0 THEN
            '-' ||
            LPAD(FLOOR(ABS(segundos) / 3600)::text, 2, '0') || ':' ||
            LPAD(FLOOR(MOD(ABS(segundos), 3600) / 60)::text, 2, '0') || ':' ||
            LPAD(MOD(ABS(segundos), 60)::text, 2, '0')
        ELSE
            LPAD(FLOOR(segundos / 3600)::text, 2, '0') || ':' ||
            LPAD(FLOOR(MOD(segundos, 3600) / 60)::text, 2, '0') || ':' ||
            LPAD(MOD(segundos, 60)::text, 2, '0')
    END
    FROM (
        SELECT FLOOR(
            EXTRACT(EPOCH FROM (
                TO_TIMESTAMP(Fecha_Pagadas || ' ' || Hora_Pagada, 'YYYY-MM-DD HH24:MI:SS')
                -
                TO_TIMESTAMP(Fecha_Confirmada || ' ' || Hora_Confirmada, 'YYYY-MM-DD HH24:MI:SS')
            ))
        )::INT AS segundos
    ) s
) AS Diferencia
FROM tt_ultima_temporal;
""")

    rows = cur.fetchall()
    cols = [c[0] for c in cur.description]

    cur.close()
    conn.close()

    return rows, cols
