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


# Query a location list of a car giving its mobile ID
@app.route('/get_location', methods=['GET'])
def getLocation():
    cursor = connectToMysql()
    MobileId = request.args.get('MId')
    cursor.execute("SELECT StickTime, Longitude, Latitude FROM CarStickTime WHERE MobileID="+MobileId)
    result = cursor.fetchall()
    resultDic = {"NULL":{}}
    for row in result:
        StickTime = row[0]
        Longitude = row[1]
        Latitude = row[2]
        resultDic[str(StickTime)] = {Longitude,Latitude}
    cursor.close()
    return jsonify(resultDic)


# Query the specific info of a car giving its mobile ID
@app.route('/get_mobile_info', methods=['GET'])
def getInfo():
    cursor = connectToMysql()
    MobileId = request.args.get('MId')
    cursor.execute("SELECT MobileType, DriverLicense, VehicleName FROM Mobile_Info WHERE MobileID="+MobileId)
    result = cursor.fetchall()
    resultDic = {"NULL":{}}
    for row in result:
        resultDic['MobileType'] = row[0]
        resultDic['DriverLicense'] = row[1]
        resultDic['VehicleName'] = row[2]
    cursor.close()
    return jsonify(resultDic)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=False, port = 80, host = '45.32.56.30')