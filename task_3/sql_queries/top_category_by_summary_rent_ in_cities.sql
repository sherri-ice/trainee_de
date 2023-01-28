select
    film.film_id,
    category.category_id,
    film.rental_duration
 FROM ((((category
     LEFT JOIN film_category ON ((category.category_id = film_category.category_id)))
     LEFT JOIN film ON ((film_category.film_id = film.film_id)))
     ))
# todo: уточнить условия