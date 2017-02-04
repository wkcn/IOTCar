#coding=utf-8
import MySQLdb
import time

'''
db = MySQLdb.connect("localhost", "root", "wk", "IOT")
cursor = db.cursor()
'''

def get_time():
    # Get current time
    # return a string %Y%m%d%H%M%S
    return time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))

def normalSQL(assign):
    attr = []
    value = []
    for name in assign.keys():
        attr.append(name)
        v = assign[name]
        if type(v) == str:
            value.append("'%s'" % v)
        else:
            value.append(str(v))
    return attr, value

def sql_insert(tableName, **assign):
    # example: sql_insert(GPS_INFO, long=2.0, lat=3.0)
    attr, value = normalSQL(assign)
    return "insert into %s(%s) values (%s);" % (tableName, ','.join(attr), ','.join(value))

def sql_select(tableName, attrName, condition = None):
    # example: sql_select(GPS_INFO, ["long, lat"])
    sql = "select (%s) from %s " % (','.join(attrName), tableName)
    if condition:
        sql += "where %s" % condition
    return sql

def sql_update(tableName, condition, **assign):
    c = ["%s = %s" % (a, v) for a,v in assign.items()]
    return "update %s set %s where %s" % (tableName, ','.join(c), condition)
    

sql = sql_insert("CarMileagesInfo", MobileID = 1, RecvTime = get_time(), Mileages = 10.0, OilCapacity = 2.3, Temperature = 37.3)
sql = sql_select("CarMileagesInfo", ["RecvTime"], "MobileID = 1")
sql = sql_insert("GPSState", GPSStateID = 1, GPSDescribe = "haha")
sql = sql_update("CarMileagesInfo", "MobileID = 1", OilCapacity = 100);
sql = sql_insert("GPSLog", GPSID = 0, MobileID = 1, GPSTime = get_time(), RecvTime = get_time(), Longitude = 128.0, Latitude = 32.2, Speed = 30, GPSStateID = 0, UserStateID = 0)
sql = sql_insert("TabGPS_DayRpt", MobileID = 1, DayRptTime = get_time(), CarCode = "hahacar", Distance = 0.0, MaxSpeed = 120.0, AvgSpeed = 60.0)
sql = sql_update("TabGPS_DayRpt", "MobileID = 1", Distance = 2.0)
sql = sql_insert("Mobile_Info", MobileID = 1, MobileType = 0, MobileSim = "hsim", DriverLicense = "123454321", VehicleName = "Car", VehicleRegistration = "Reg", VehicleType = "Type", VehicleColor = "Black", VehicleEngine = "D type", FixingTime = get_time(), ServiceTime = get_time(), OilBox = 380.0)
sql = sql_insert("Driver", DriverName = "laosiji", DriverLicense="123454321", Tel1 = "13312343212")
sql = sql_insert("OrderCheck_Info", OrderID = 0, OrderName = "park", OrderType = 0)
sql = sql_insert("SendCmdLog", MobileID = 0, SendTime = get_time(), UserID = 0, CmdType = 0, CmdContent = "gogo")
sql = sql_insert("CityRagne", CityName = "Guangzhou", MinLong = 0, MaxLong = 1, MinLat = 0, MaxLat = 1)
sql = sql_insert("AlarmOperation", AlarmID = 0, MobileID = 1, RecvTime = get_time(), GPSTime = get_time(), MsgStr = "alarm", MsgDescribe = "ahahahaha", Longitude = 1.0, Latitude = 2.0)
print (sql)
