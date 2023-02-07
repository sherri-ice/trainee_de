create table if not exists hostel.Students (
  birthday date not null,
  id int auto_increment not null primary key,
  name varchar(300) not null,
  room int not null,
  sex char(1) not null,
  foreign key (room) references hostel.Rooms(id) on delete cascade
);
