-- two ways to do this task, the comparison on performance is in task_3/readme.md

/* SELECT temp.city,
       count(CASE WHEN customer.activebool = TRUE THEN 1 END)  AS active_population,
       count(CASE WHEN customer.activebool = FALSE THEN 1 END) AS inactive_population
FROM customer
         JOIN (SELECT address.address_id,
                      city.city_id,
                      city.city
               FROM address
                        JOIN city
                             ON address.city_id = city.city_id) AS temp ON temp.address_id = customer.address_id
GROUP BY temp.city
ORDER BY inactive_population DESC;
*/

WITH address_city AS (
    (SELECT address.address_id,
            city.city_id,
            city.city
     FROM address
              JOIN city
                   ON address.city_id = city.city_id))
SELECT address_city.city,
       count(CASE WHEN customer.activebool = TRUE THEN 1 END)  AS active_population,
       count(CASE WHEN customer.activebool = FALSE THEN 1 END) AS inactive_population
FROM customer, address_city
WHERE address_city.address_id = customer.address_id
GROUP BY address_city.city
ORDER BY inactive_population DESC;
