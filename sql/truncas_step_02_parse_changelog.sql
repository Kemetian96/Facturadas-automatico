DROP TABLE IF EXISTS ttt_shipments_changelogs;
CREATE TEMP TABLE ttt_shipments_changelogs AS
SELECT
    id_orders_shipments,
    (changelog::jsonb ->> 'comment') AS comment,
    (changelog::jsonb ->> 'id_orders_shipments_statuses')::INT AS id_orders_shipments_statuses,
    (changelog::jsonb ->> 'id_users_updated')::BIGINT AS id_users_updated,
    (changelog::jsonb ->> 'cuid_updated')::BIGINT AS cuid_updated
FROM tt_shipments_changelogs
WHERE (changelog::jsonb ->> 'comment') LIKE 'Estado orden paquete:%';
