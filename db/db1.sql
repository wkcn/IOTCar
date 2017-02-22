/*
-- 对车辆进行定位(经纬度)和 GPS 状态(里程数)的确定
create table CarStickTime(
	MobileID int,
	StickTime datetime,
	Longitude float,
	Latitude float,
	GPSStateID smallint, -- 使用状态ID
	UserStateID smallint, -- 使用状态ID
	Mileages float,
	OilCapacity float,
	Temperature float,
	primary key (MobileID, StickTime)
);
*/

-- CarStickTime表被CarMileagesInfo和GPSLog表代替
-- 车辆里程信息
create table CarMileagesInfo(
	MobileID int,
	RecvTime datetime,
	Mileages float, -- 里程
	OilCapacity float, -- 油量
	Temperature float, -- 温度
	primary key (MobileID, RecvTime)
);

create table GPSState(
	GPSStateID smallint primary key,
	GPSDescribe varchar(16)
);

create table UserState(
	UserStateID smallint primary key,
	UserDescribe varchar(16)
);

-- 传感器信息
create table GPSLog(
	GPSID int,
	MobileID int,
	GPSTime datetime,
	RecvTime datetime,
	Longitude float,
	Latitude float,
	Speed float,
	GPSStateID smallint references GPSState(GPSState), -- 使用状态ID
	UserStateID smallint references UserState(UserStateID), -- 使用状态ID
	primary key (GPSID, MobileID, GPSTime)
);

-- 车牌号, 里程, 速度
create table TabGPS_DayRpt(
	DayRptID int auto_increment,
	MobileID int,
	DayRptTime datetime,
	CarCode varchar(16),
	Distance float,
	MaxSpeed float,
	AvgSpeed float,
	primary key (DayRptID) 
);

-- 车辆信息
create table Mobile_Info(
	ConsumerID int,
	MobileID int,
	MobileType int,
	MobileSIM varchar(20),
	DriverLicense varchar(20),
	VehicleName varchar(10),
	VehicleRegistration varchar(10),
	VehicleType varchar(5),
	VehicleColor varchar(5),
	VehicleEngine varchar(20),
	FixingTime datetime,
	ServiceTime datetime,
	OilBox float, -- 油箱油量
	primary key (Consumer_ID, Mobile_ID)
);

-- 驾驶员信息
create table Driver(
	DriverName varchar(10),
	DriverLicense varchar(20),
	Tel1 varchar(15),
	Tel2 varchar(15),
	Tel3 varchar(15),
	primary key (DriverLicense)
);

-- 指令编号名称
create table OrderCheck_Info(
	OrderID int,
	OrderName varchar(50),
	OrderType int,
	primary key (OrderID)
);

-- 指令发送记录
create table SendCmdLog(
	MobileID int,
	SendTime datetime,
	UserID int,
	CmdType int,
	CmdContent varchar(100),
	primary likey (MobileID, SendTime) 
);

-- 城市坐标
create table CityRange(
	CityName varchar(16),
	MinLong float,
	MaxLong float,
	MinLat float,
	MaxLat float,
	primary key (CityName)
);

-- 车辆报警事件的信息
create table AlarmOperation(
	AlarmID int auto_increment,
	MobileID int,
	RecvTime datetime, -- 发出警报的时间
	GPSTime datetime, -- 从GPS获得的时间
	MsgStr varchar(16), -- 报警名称
	MsgDescribe varchar(100), -- 报警事件对应的详细信息
	Longitude float,
	Latitude float,
	primary key (AlarmID)
);	

