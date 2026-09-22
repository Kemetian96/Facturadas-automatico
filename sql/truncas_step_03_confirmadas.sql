DROP TABLE IF EXISTS tt_truncas_confirmadas;
CREATE TEMP TABLE tt_truncas_confirmadas AS
SELECT
    t3.id_users,
    t1.id_orders_shipments,
    t4.order_shipment_status AS estado,
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
FROM ttt_shipments_changelogs t1
INNER JOIN main.t_users t3 ON t3.id_users = t1.id_users_updated
INNER JOIN main.t_orders_shipments_statuses t4
    ON t4.id_orders_shipments_statuses = t1.id_orders_shipments_statuses
WHERE t1.id_orders_shipments_statuses = 11
  AND t1.comment NOT IN ('Orden enviada a nubefact', 'Estado: Finalizada')
GROUP BY t1.id_orders_shipments, t3.id_users, t4.order_shipment_status,
         t3.first_name, t3.last_name, t3.document
HAVING t3.id_users IN (
    236836, 1505870, 3000995, 2025020720235394839, 2023071423591090268
);
