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
        resultDic[str(create_time)] = {DriverId,CarId,Longitude,Latitude,oil_capacity,temperature}
    cursor.close()
    print resultDic
    return resultDic

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
        resultDic[str(create_time)] = {DriverId,CarId,Longitude,Latitude,oil_capacity,temperature}
    cursor.close()
    print resultDic
    return resultDic


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
    app.run(debug=True, host = '45.32.48.44', port = 5000)
    # app.run(debug=False, port = 80, host = '45.32.56.30')
