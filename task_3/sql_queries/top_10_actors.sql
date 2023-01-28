select
    actor.first_name, actor.last_name, sum(actors.rental_duration) as rental_duration
from
(select
    film_actor.actor_id, film.rental_duration
from
    film
join
        film_actor on film_actor.film_id = film.film_id
order by
    film.rental_duration desc
) as actors
join
    actor on actor.actor_id = actors.actor_id
group by
    actor.actor_id
order by rental_duration desc
limit 10;