import pymysql

def connectToMysql():
    db = pymysql.connect('localhost','root','youareBT','wlw')
    cursor = db.cursor()
    return cursor

def getNLocation(num):
    cursor = connectToMysql()
    cursor.execute("SELECT driver_id, car_id, longitude, latitude, oil_capacity, temperature, create_time FROM Drive_info ORDER BY create_time LIMIT "+ str(num))
    result = cursor.fetchall()
    resultDic = {}
    for row in result:
        DriverId = row[0]
        CarId = row[1]
        Longitude = row[2]
        Latitude = row[3]
        oil_capacity = row[4]
        temperature = row[5]
        create_time = row[6]
        resultDic[str(create_time)] = {DriverId,CarId,Longitude,Latitude,oil_capacity,temperature}
    cursor.close()
    return jsonify(resultDic)

print(getNLocation(5))