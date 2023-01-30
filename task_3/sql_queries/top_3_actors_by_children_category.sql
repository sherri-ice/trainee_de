SELECT
    film.film_id, film_category.category_id
INTO children_movies
FROM film
JOIN film_category
    ON film.film_id = film_category.film_id
WHERE
    film_category.category_id IN
    (SELECT category_id
     FROM category
     WHERE category.name LIKE 'Children');

SELECT
    actor.actor_id, actor.first_name, actor.last_name, temp.children_movies_count
FROM
    (SELECT film_actor.actor_id,
             count(children_movies.film_id) AS children_movies_count
      FROM children_movies
               JOIN film_actor
                   ON film_actor.film_id = children_movies.film_id
      GROUP BY
          film_actor.actor_id
      ORDER BY
          children_movies_count DESC
      LIMIT
          10
) AS temp
JOIN actor
    ON actor.actor_id = temp.actor_id;