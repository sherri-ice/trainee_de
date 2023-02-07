SELECT actor.first_name,
       actor.last_name,
       sum(actors.rental_duration) AS rental_duration
FROM (SELECT film_actor.actor_id,
             film.rental_duration
      FROM film
               JOIN film_actor
                    ON film_actor.film_id = film.film_id
      ORDER BY film.rental_duration
              DESC) AS actors
         JOIN actor on
    actor.actor_id = actors.actor_id
GROUP BY actor.actor_id
ORDER BY rental_duration
        DESC
LIMIT 10;