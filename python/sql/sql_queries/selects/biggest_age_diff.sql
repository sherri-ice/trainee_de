select
    room,
    timestampdiff(YEAR, min(s.birthday), max(s.birthday)) as diff
from hostel.Students s
group by
    room
order by
    diff desc
limit 5;
