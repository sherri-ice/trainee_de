select
    category.name, count(film_category.film_id) as films_number
from
    film_category
join category on film_category.category_id = category.category_id
group by
    category.name
order by
    films_number desc;
