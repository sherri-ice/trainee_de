SELECT film.film_id,
       film.title
FROM film
         LEFT JOIN inventory
                   ON film.film_id = inventory.film_id
WHERE inventory.film_id IS NULL;