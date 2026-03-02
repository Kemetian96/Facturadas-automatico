DROP TABLE IF EXISTS tt_confirmadas_reporte;
CREATE TEMP TABLE tt_confirmadas_reporte AS
SELECT
    t3.id_users,
    t1.id_orders,
    t1.uid_orders,
    t4.order_status AS estado,
    CONCAT_WS(' ', t3.first_name, t3.last_name) AS colaborador,
    t3.document AS documento,
    UPPER(
        TO_CHAR(
            ("main".f_u_cuid_to_datetime_v1(MIN(t1.cuid_updated)) AT TIME ZONE '-05'),
            'Day'
        )
    ) AS dia_confirmada,
    TO_CHAR(
        ("main".f_u_cuid_to_datetime_v1(MIN(t1.cuid_updated)) AT TIME ZONE '-05'),
        'YYYY-MM-DD'
    ) AS fecha_confirmada,
    TO_CHAR(
        ("main".f_u_cuid_to_datetime_v1(MIN(t1.cuid_updated)) AT TIME ZONE '-05'),
        'HH24:MI:SS'
    ) AS hora_confirmada
FROM ttt_orders_changelogs t1
INNER JOIN main.t_users t3 ON t3.id_users = t1.id_users_updated
INNER JOIN main.t_orders_statuses t4 ON t4.id_orders_statuses = t1.id_orders_statuses
WHERE t1.id_orders_statuses = 3
  AND t1.comment NOT IN ('Orden enviada a nubefact', 'Estado: Finalizada')
GROUP BY t1.id_orders, t3.id_users, t1.uid_orders, t4.order_status,
         t3.first_name, t3.last_name, t3.document
HAVING t3.id_users IN (
    236836, 1227370, 2023042906080574703, 2024081920474009937,
    2024021220010944881, 612222, 2025030814051779132, 2024080922041140780,
    2024041303072110864, 2024040420295926716, 2023071423591090268,
    2023081717330019273, 2025091603563803145, 3000995
);

