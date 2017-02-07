--收费信息记录
create table CarFare(
    id int primary key auto_increment,
    carId int,
    date datetime,
    tollGateId int,
    fare float
);

--物流信息记录
create table LogisticsInfo(
    id int primary key auto_increment,
    carId int,
    runType varchar(40),
    outDate datetime,
    runDate datetime,
    miles float,
    carryMass float,
    totalMass float,
    figure float,
    driverId int,
);

--路线信息记录
create table LineAndCarItem(
    id int primary key auto_increment,
    lineId int,
    carId int,
    driverId int,
    planArriveTime datetime,
    actualArriveTime datetime,
);
