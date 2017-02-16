from flask import Flask, request, jsonify, render_template
import pymysql
import dbconf

def connectToMysql():
    db = pymysql.connect(dbconf._IPaddress,dbconf._username,dbconf._password,dbconf._dbname)
    cursor = db.cursor()
    return cursor

app = Flask(__name__)

# Insert a new car location info into the database
@app.route('/add_new_location', methods = ['POST'])
def postInfo():
    cursor = connectToMysql()
    jsonInfo = request.json
    sql = """INSERT INTO CarStickTime(MobileID, StickTime, Longitude, Latitude) 
        VALUES ('%s',%s','%f','%f')""" % (jsonInfo["MobileID"], jsonInfo['StickTime'], float(jsonInfo['Longitude']), float(jsonInfo['Latitude']))
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
    sql = '''SELECT car_id, name, tel, longitude, latitude, oil_capacity, temperature, create_time
    FROM Drive_info as t1
    Join 
    (SELECT car_id, max(create_time) as create_time from Drive_info group by car_id) as t2
    ON t1.car_id = t2.car_id AND t1.create_time = t2.create_time
    Join
    Driver as t3
    On t1.driver_id = t3.driver_id'''
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
    # app.run(debug=True, host = '45.32.48.44', port = 5000)
    app.run(debug=True, host = '127.0.0.1', port = 5000)
    # app.run(debug=False, port = 80, host = '45.32.56.30')
