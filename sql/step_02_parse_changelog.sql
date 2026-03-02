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

