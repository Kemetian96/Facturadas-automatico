SELECT
    id_orders,
    uid_orders,
    usuario_que_confirma,
    documento_usuario_que_confirma,
    dia_pagadas,
    estado_pagada,
    dia_confirmada,
    estado_confirmadas,
    fecha_pagadas,
    fecha_confirmada,
    hora_pagada,
    hora_confirmada,
    (
        SELECT
            CASE
                WHEN segundos < 0 THEN
                    '-' ||
                    LPAD(FLOOR(ABS(segundos) / 3600)::TEXT, 2, '0') || ':' ||
                    LPAD(FLOOR(MOD(ABS(segundos), 3600) / 60)::TEXT, 2, '0') || ':' ||
                    LPAD(MOD(ABS(segundos), 60)::TEXT, 2, '0')
                ELSE
                    LPAD(FLOOR(segundos / 3600)::TEXT, 2, '0') || ':' ||
                    LPAD(FLOOR(MOD(segundos, 3600) / 60)::TEXT, 2, '0') || ':' ||
                    LPAD(MOD(segundos, 60)::TEXT, 2, '0')
            END
        FROM (
            SELECT FLOOR(
                EXTRACT(EPOCH FROM (
                    TO_TIMESTAMP(fecha_pagadas || ' ' || hora_pagada, 'YYYY-MM-DD HH24:MI:SS')
                    - TO_TIMESTAMP(fecha_confirmada || ' ' || hora_confirmada, 'YYYY-MM-DD HH24:MI:SS')
                ))
            )::INT AS segundos
        ) s
    ) AS diferencia
FROM tt_ultima_temporal;

