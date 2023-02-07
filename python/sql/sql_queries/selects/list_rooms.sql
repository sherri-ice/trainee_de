select
    room.name as name,
    count(*) as students_number
from hostel.Rooms room
    join Students S on room.id = S.room
group by name
order by students_number desc;
