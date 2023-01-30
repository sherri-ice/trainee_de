SElECT
    category.name, count(film_category.film_id) as films_number
FROM
    film_category
JOIN category AS cat
    ON film_category.category_id = cat.category_id
GROUP BY
    category.name
ORDER BY
    films_number DESC;
