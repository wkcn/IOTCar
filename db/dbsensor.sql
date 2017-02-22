create table CarSensor(
	MobileID int,
	StickTime datetime,
	light float,
	pitch float,
	roll float,
	azimuth float,
	xMag float,
	yMag float,
	zMag float,
	xforce float,
	yforce float,
	zforce float,
	accuracy float,
	primary key (MobileID, StickTime)
);
