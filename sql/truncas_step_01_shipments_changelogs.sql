DROP TABLE IF EXISTS tt_shipments_changelogs;
CREATE TEMP TABLE tt_shipments_changelogs AS
SELECT id_orders_shipments, changelog, cuid_inserted AS uuid_short_modified
FROM main.t_orders_shipments_changelogs
WHERE cuid_inserted BETWEEN %s AND %s;
