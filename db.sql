create table if not exists location (
  id integer primary key autoincrement,
  city varchar(225) not null,
  place varchar(225) not null
);
create table if not exists upload(

  id integer primary key autoincrement,
  img_url varchar(225) not null,
  category varchar(225) not null,
  latitude varchar(50) not null,
  longitude varchar(50) not null,
  rating integer not null,
  gender varchar(15) not null,
  ageCategory varchar(20) not null

);
