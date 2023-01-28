select
    film.film_id, film_category.category_id
into children_movies
from film
join film_category on film.film_id = film_category.film_id
where
    film_category.category_id in
    (select category_id
     from category
     where category.name like 'Children');

select
    actor.actor_id, actor.first_name, actor.last_name, temp.children_movies_count
from (select film_actor.actor_id,
             count(children_movies.film_id) as children_movies_count
      from children_movies
               join film_actor on film_actor.film_id = children_movies.film_id
      group by film_actor.actor_id
      order by children_movies_count desc
      limit 10
) as temp
join actor on actor.actor_id = temp.actor_id;