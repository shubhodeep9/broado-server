drop table if exists location;
create table location (
  id integer primary key autoincrement,
  city varchar(225) not null,
  place varchar(225) not null
);
