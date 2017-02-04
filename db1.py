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

'''
def insert_CarMileagesInfo(MobileID, Mileages, OilCapacity, Temperature):
    return "insert into CarMileagesInfo(MobileID, RecvTime, Mileages, OilCapacity, Temperature) values (%d, %s, %f, %f %f);" % (MobileID, get_time(), Mileages, OilCapacity, Temperature)

def select_CarMileagesInfo(MobileID):
    return "selct (MobileID, RecvTime, Mileages, OilCapacity, Temperature) from CarMileagesInfo where MobileID = %d;" % (MobileID)

def insert_GPSLog(GPSID, MobileID, GPSTime, RecvTime, L
'''

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
print (sql)
