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

CREATE TABLE IF NOT EXISTS `hotels` (
`id` integer primary key autoincrement,
  `hotel_name` varchar(225) NOT NULL,
  `hotel_price` int(11) NOT NULL,
  `hotel_rating` varchar(10) NOT NULL,
  `hotel_facilities` varchar(225) NOT NULL,
  `hotel_review` varchar(225) NOT NULL,
  `hotel_type` varchar(100) NOT NULL,
  `hotel_city` varchar(225) NOT NULL
) ;

--
-- Dumping data for table `hotels`
--

INSERT INTO `hotels` (`id`, `hotel_name`, `hotel_price`, `hotel_rating`, `hotel_facilities`, `hotel_review`, `hotel_type`, `hotel_city`) VALUES
(1, 'The Atria Hotel', 3000, '4.4', 'Free Wifi, 24x7 Laundary service, Free Breakfast ', 'Best Hotel within budget', 'normal', 'Bangalore'),
(2, 'Ginger hotel whitefield', 4500, '4.3', 'Buffet, Swimming Pools, Spa, Massage', 'Very nice service, will visit again.\r\n-Vignesh', 'high', 'Bangalore'),
(3, 'Sheraton Bangalore at Brigade Gateway', 2500, '4.9', 'Free Breakfast, Free laundary', 'Must come again. Nice environment.\r\n-Utkarsh', 'normal', 'Bangalore'),
(4, 'Hotel IBIS', 5500, '4.6', 'Luxurious view, 24 hours room service, Free Wifi, Bar, Restaurant', 'Awesome hotel.\r\n-Girish', 'hogh', 'Bangalore'),
(5, 'Radisson Blu', 7500, '4.8', 'Luxurious view, 24 hours room service, Free Wifi, Bar, Restaurant', 'Very luxury hotel. Best hotel here.\r\n-Garvit', 'high', 'Chennai');
