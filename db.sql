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
create table if not exists hotels(
  id integer primary key autoincrement,
  hotel_name varchar(225) not null,
  hotel_price integer not null,
  hotel_rating varchar(5) not null,
  hotel_facilities varchar(225),
  hotel_review varchar(225),
  hotel_type varchar(225)
);
