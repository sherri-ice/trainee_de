select
     temp.city,
     count(case when customer.activebool = True then 1 end) as active_population,
     count(case when customer.activebool = False then 1 end) as inactive_population
from customer
join (
    select
        address.address_id, city.city_id, city.city
    from address
    join city on address.city_id = city.city_id
) as temp on temp.address_id = customer.address_id
group by temp.city
order by inactive_population desc;