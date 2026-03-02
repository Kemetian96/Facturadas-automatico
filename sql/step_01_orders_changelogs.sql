DROP TABLE IF EXISTS tt_orders_changelogs;
CREATE TEMP TABLE tt_orders_changelogs AS
SELECT id_orders, changelog, cuid_inserted AS uuid_short_modified
FROM main.t_orders_changelogs
WHERE cuid_inserted BETWEEN %s AND %s;

