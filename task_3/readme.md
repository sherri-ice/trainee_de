# Task 3. SQL queries.

## 

## Task 6. Group cities by number of active and inactive customers
The solution was implemented in two ways: subqueries and temporary tables.

### Subquery and joins
```sql 
SELECT temp.city,
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
```

The execution time of this query:

![img.png](addition/subquery_time.png)


### Temp table

```sql
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
```

The execution time of this query:

![img.png](addition/temp_table_time.png)

### Sum
Obviously, a temporary table on this data worked faster, but in the general case, the use of temporary tables does not guarantee
query execution is faster than sub queries and joins.

You need to play around to get the performance you expect, particularly for complex queries that are run on a regular basis.
In an ideal world, the query optimizer would find the perfect execution path. Although it often does, you may be able to find a way to get better performance.

[Source](https://stackoverflow.com/questions/11169550/is-there-a-performance-difference-between-cte-sub-query-temporary-table-or-ta/11169910#11169910)