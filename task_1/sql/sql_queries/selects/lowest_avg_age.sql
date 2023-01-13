select
    avg(timestampdiff(YEAR , s.birthday, curdate())) as avg_age
from hostel.Students s
    join Rooms R on s.room = R.id
group by
    R.name
order by
    avg_age
limit
    5;