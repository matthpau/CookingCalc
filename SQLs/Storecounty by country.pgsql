SELECT  my_country_id, count(id) AS store_count
FROM stores_store 
GROUP BY  my_country_id
ORDER BY store_count DESC
;