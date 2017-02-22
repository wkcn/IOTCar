--收费站信息
create table TollGate(
	id int primary key auto_increment,
	name varchar(50),
	longitude float,
	latitude float
);

--司机行驶记录
create table Drive_record(
	id int primary key auto_increment,
	driver_id int,
	dst_city varchar(50),
	longitude float,
	latitude float
);
