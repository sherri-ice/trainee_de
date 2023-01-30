WITH matchin_cities AS (SELECT *
                            FROM city
                            where upper(city.city) LIKE 'A%' or city.city LIKE '%-%'),
     matched_address AS (SELECT address.address_id
                         FROM matchin_cities as city
                                  JOIN address ON address.city_id = city.city_id),
     matched_customers AS (SELECT customer.customer_id
                           from matched_address
                                    join customer on matched_address.address_id = customer.address_id),
     matched_inventory AS (SELECT inventory_id,
                                  COALESCE(return_date, CURRENT_DATE) - rental_date as rental_duration -- consider films with no return_date are still in rental
                           from matched_customers
                                    join rental on rental.customer_id = matched_customers.customer_id),
     matched_film AS (SELECT film_id, sum(rental_duration) as sum_rental_duration
                      from matched_inventory
                               join inventory on matched_inventory.inventory_id = inventory.inventory_id
                      group by film_id),
     matched_category AS (SELECT category_id, sum(sum_rental_duration) as sum_rental_duration
                          from matched_film
                                   join film_category on matched_film.film_id = film_category.film_id
                          group by category_id)
SELECT category.category_id, category.name, matched_category.sum_rental_duration
from matched_category
         join category on matched_category.category_id = category.category_id
order by matched_category.sum_rental_duration desc;