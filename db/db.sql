create table Driver(
	id int primary key auto_increment,
	name varchar(20),
	tel varchar(15)
);

create table Car(
	id int primary key auto_increment,
	type varchar(50),
	car_num varchar(20)
);

create table Drive_info(
	id int primary key auto_increment,
	driver_id int,
	car_id int,
	longitude float,
	latitude float,
	oil_capacity float,
	temperature float,
	create_time datetime
);
