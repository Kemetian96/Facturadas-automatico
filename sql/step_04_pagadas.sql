DROP TABLE IF EXISTS tt_ultima_temporal;
CREATE TEMP TABLE tt_ultima_temporal AS
SELECT
    t2.id_orders,
    t2.uid_orders,
    colaborador AS usuario_que_confirma,
    documento AS documento_usuario_que_confirma,
    UPPER(
        TO_CHAR(
            ("main".f_u_cuid_to_datetime_v1(MIN(t1.cuid_updated)) AT TIME ZONE '-05'),
            'Day'
        )
    ) AS dia_pagadas,
    t4.order_status AS estado_pagada,
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
FROM ttt_orders_changelogs t1
INNER JOIN tt_confirmadas_reporte t2 ON t2.id_orders = t1.id_orders
INNER JOIN main.t_orders_statuses t4 ON t4.id_orders_statuses = t1.id_orders_statuses
WHERE t1.id_orders_statuses = 2
GROUP BY t2.uid_orders, t2.id_orders, colaborador, documento,
         dia_confirmada, estado, fecha_confirmada, hora_confirmada, t4.order_status;

