select
  room
from
  hostel.Students
group by
  room
having
  count(distinct sex) > 1