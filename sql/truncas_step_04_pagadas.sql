DROP TABLE IF EXISTS tt_truncas_final;
CREATE TEMP TABLE tt_truncas_final AS
SELECT
    t2.id_orders_shipments,
    colaborador AS usuario_que_confirma,
    documento AS documento_usuario_que_confirma,
    UPPER(
        TO_CHAR(
            ("main".f_u_cuid_to_datetime_v1(MIN(t1.cuid_updated)) AT TIME ZONE '-05'),
            'Day'
        )
    ) AS dia_pagadas,
    t4.order_shipment_status AS estado_pagada,
    dia_confirmada,
    estado AS estado_confirmadas,
    TO_CHAR(
        ("main".f_u_cuid_to_datetime_v1(MIN(t1.cuid_updated)) AT TIME ZONE '-05'),
        'YYYY-MM-DD'
    ) AS fecha_pagadas,
    fecha_confirmada,
    TO_CHAR(
        ("main".f_u_cuid_to_datetime_v1(MIN(t1.cuid_updated)) AT TIME ZONE '-05'),
        'HH24:MI:SS'
    ) AS hora_pagada,
    hora_confirmada
FROM ttt_shipments_changelogs t1
INNER JOIN tt_truncas_confirmadas t2 ON t2.id_orders_shipments = t1.id_orders_shipments
INNER JOIN main.t_orders_shipments_statuses t4
    ON t4.id_orders_shipments_statuses = t1.id_orders_shipments_statuses
WHERE t1.id_orders_shipments_statuses = 9
GROUP BY t2.id_orders_shipments, colaborador, documento,
         dia_confirmada, estado, fecha_confirmada, hora_confirmada, t4.order_shipment_status;
