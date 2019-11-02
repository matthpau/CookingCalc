SELECT OSM_storetype_id, count(id) AS store_count
FROM stores_store 
GROUP BY OSM_storetype_id
ORDER BY store_count DESC
;