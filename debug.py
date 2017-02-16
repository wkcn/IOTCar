import pymysql
from flask import jsonify
def connectToMysql():
    db = pymysql.connect('localhost','root','youareBT','wlw')
    cursor = db.cursor()
    return cursor

def getNLocation():
    cursor = connectToMysql()
    sql = "SELECT car_id, name, tel, longitude, latitude, oil_capacity, temperature, max(create_time) FROM Drive_info JOIN Driver GROUP BY car_id"
    cursor.execute(sql)
    result = cursor.fetchall()
    resultDic = {}
    for row in result:
        CarId = row[0]
        DriverName = row[1]
        DriverTel = row[2]
        Longitude = row[3]
        Latitude = row[4]
        oil_capacity = row[5]
        temperature = row[6]
        create_time = row[7]
        resultDic[str(create_time)] = {"CarId":CarId,"DriverName": DriverName,"DriverTel": DriverTel,"Longitude":Longitude,"Latitude":Latitude,"oil_capacity":oil_capacity,"temperature":temperature}
    cursor.close()
    return resultDic

print(getNLocation())
