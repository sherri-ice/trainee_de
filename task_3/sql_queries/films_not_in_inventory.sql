select
    film.film_id, film.title
from
    film
left join inventory on film.film_id = inventory.film_id
where inventory.film_id is null;