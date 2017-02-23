from flask import Flask, request, jsonify, render_template
import pymysql
import dbconf
import names
import time

db = None
def connectToMysql():
    global db
    db = pymysql.connect(dbconf._IPaddress,dbconf._username,dbconf._password,dbconf._dbname)
    cursor = db.cursor()
    return cursor

app = Flask(__name__)

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

# Insert a new car location info into the database
@app.route('/add_new_location', methods = ['POST'])
def postInfo():
    cursor = connectToMysql()
    jsonInfo = request.json
    sql = sql_insert("GPSLog", GPSID = jsonInfo["GPSID"], MobileID = jsonInfo["MobileID"], GPSTime = jsonInfo["GPSTime"], RecvTime = get_time(), Longitude = jsonInfo["Longitude"], Latitude = jsonInfo["Latitude"], Speed = jsonInfo["Speed"])
    try:
        cursor.execute(sql)
        db.commit()
        cursor.close()
        return "Successed"
    except:
        db.rollback()
        cursor.close()
        return "Failed"

# Insert a new car sensor info into the database
@app.route('/add_new_sensor', methods = ['POST'])
def postSensorInfo():
    cursor = connectToMysql()
    jsonInfo = request.json
    sql = sql_insert("CarSensor", MobileID = jsonInfo.get("MobileID", -1), StickTime = jsonInfo.get("StickTime", -1), light = jsonInfo.get("light", -1), pitch = jsonInfo.get("pitch", -1), roll = jsonInfo.get("roll", -1), azimuth = jsonInfo.get("azimuth", -1), xMag = jsonInfo.get("xMag", -1), yMag = jsonInfo.get("yMag", -1), zMag = jsonInfo.get("zMag", -1), xforce = jsonInfo.get("xforce", -1), yforce = jsonInfo.get("yforce", -1), zforce = jsonInfo.get("zforce", -1), accuracy = jsonInfo.get("accuracy", -1))
    try:
        cursor.execute(sql)
        db.commit()
        cursor.close()
        return "Successed"
    except:
        db.rollback()
        cursor.close()
        return "Failed"


# Query a location list of all cars
@app.route('/get_all_location', methods=['GET'])
def getAllLocation():
    cursor = connectToMysql()
    cursor.execute("SELECT driver_id, car_id, longitude, latitude, oil_capacity, temperature, create_time FROM Drive_info ORDER BY create_time DESC")
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
        resultDic[str(create_time)] = {"DriverId":DriverId,"CarId":CarId,"Longitude":Longitude,"Latitude":Latitude,"oil_capacity":oil_capacity,"temperature":temperature}
    cursor.close()
    return jsonify(resultDic)

# Query a location list of n latest drive info
@app.route('/get_n_location', methods=['GET'])
def getNLocation():
    cursor = connectToMysql()
    num = request.args.get('n')
    cursor.execute("SELECT driver_id, car_id, longitude, latitude, oil_capacity, temperature, create_time FROM Drive_info ORDER BY create_time DESC LIMIT "+ str(num))
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
        resultDic[str(create_time)] = {"DriverId":DriverId,"CarId":CarId,"Longitude":Longitude,"Latitude":Latitude,"oil_capacity":oil_capacity,"temperature":temperature}
    cursor.close()
    return jsonify(resultDic)

@app.route('/get_latest_location', methods=['GET'])
def getLatestLocation():
    cursor = connectToMysql()
    sql = 'SELECT t1.car_id, name, tel, longitude, latitude, oil_capacity, temperature, t1.create_time FROM Drive_info as t1 Join (SELECT car_id, max(create_time) as create_time from Drive_info group by car_id) as t2 ON t1.car_id = t2.car_id AND t1.create_time = t2.create_time Join Driver as t3 On t1.driver_id = t3.id'
    cursor.execute(sql)
    result = cursor.fetchall()
    resultDic = {}
    for row in result:
        CarId = row[0]
        DriverName =names.get_first_name(gender='male')
        DriverTel = row[2]
        Longitude = row[3]
        Latitude = row[4]
        oil_capacity = row[5]
        temperature = row[6]
        create_time = row[7]
        resultDic[str(CarId)] = {"CarId":CarId,"DriverName": DriverName,"DriverTel": DriverTel,"Longitude":Longitude,"Latitude":Latitude,"oil_capacity":oil_capacity,"temperature":temperature}
    cursor.close()
    return jsonify(resultDic)

@app.route('/get_latest_GPS', methods=['GET'])
def getGPSInfo():
    cursor = connectToMysql()
    n = request.args.get('n')
    cursor.execute("SELECT RecvTime, Longitude, Latitude FROM GPSLog Order By RecvTime ASC LIMIT "+ n)
    result = cursor.fetchall()
    resultDic = {}
    for row in result:
        resultDic[str(row[0])] = {'longitude':row[1], 'latitude':row[2]}
    cursor.close()
    return jsonify(resultDic)


@app.route('/get_latest_sensors', methods=['GET'])
def getSensorsInfo():
    cursor = connectToMysql()
    n = request.args.get('n')
    cursor.execute("SELECT StickTime, light, xforce, yforce, zforce, accuracy FROM CarSensor Order By StickTime ASC LIMIT "+ n)
    result = cursor.fetchall()
    resultDic = {}
    for row in result:
        resultDic[str(row[0])] = {'light':row[1], 'xforce':row[2], 'yforce':row[3], 'zforce':row[4], 'accuracy':row[5]}
    cursor.close()
    return jsonify(resultDic)

# Query the specific info of a car giving its  ID
@app.route('/get_car_info', methods=['GET'])
def getCarInfo():
    cursor = connectToMysql()
    CarId = request.args.get('CarId')
    cursor.execute("SELECT id, type, car_num FROM Car WHERE id="+CarId)
    result = cursor.fetchall()
    resultDic = {}
    for row in result:
        resultDic['id'] = row[0]
        resultDic['type'] = row[1]
        resultDic['car_num'] = row[2]
    cursor.close()
    return jsonify(resultDic)

# Query the specific info of a driver giving its  ID
@app.route('/get_Driver_info', methods=['GET'])
def getDriverInfo():
    cursor = connectToMysql()
    DriverId = request.args.get('DriverId')
    cursor.execute("SELECT id, name, tel FROM Driver WHERE id="+DriverId)
    result = cursor.fetchall()
    resultDic = {}
    for row in result:
        resultDic['id'] = row[0]
        resultDic['name'] = row[1]
        resultDic['tel'] = row[2]
    cursor.close()
    return jsonify(resultDic)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # app.run(debug=True, host ='45.32.48.44', port = 8386)
    app.run(debug=True, host = '127.0.0.1', port = 5000)
    # app.run(debug=False, port = 80, host = '45.32.56.30')
