SELECT  c.name, count(id) AS store_count
FROM stores_store s INNER JOIN stores_country c
ON s.my_country_id = c.code
GROUP BY c.name
ORDER BY store_count DESC
;