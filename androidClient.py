#coding=utf-8
try:
    import sl4a
except:
    import fakesl4a as sl4a 
import urllib.parse
import urllib.request
import time
import json

SERVER_ADDR = "http://45.32.56.30/"
#SERVER_ADDR = "http://127.0.0.1:5000/"
USER_NAME = "user1"
INTERVAL_SECONDS = 1

droid = sl4a.Android()
droid.startSensingTimed(1,500)
droid.startLocating(1, 1) # updateTime(milliseconds), minUpdateDistance(meters)

def SendData(name, data):
    headers = {'Content-Type': 'application/json'}
    jdata = json.dumps(data)
    bdata = bytes(jdata, "utf8")
    req = urllib.request.Request(url = SERVER_ADDR + name, data = bdata)
    req.add_header('Content-Type', 'application/json')
    urllib.request.urlopen(req)

def GetGPS():
    loc = droid.readLocation().result
    if len(loc) == 0:
        loc = droid.getLastKnownLocation().result
    return loc

while 1:
    '''
        sensors中的key解释:
        时间:
            time
        亮度:
            light
        陀螺仪:
            pitch, roll, azimuth
        磁力计:
            xMag, yMag, zMag
        加速度:
            xforce, yforce, zforce
        精度:
            accuracy
    '''


    sensors_data = [] 
    sensors_name = ["light", "pitch", "roll", "azimuth", "xMag", "yMag", "zMag", "xforce", "yforce", "zforce", "accuracy"]


    '''
    for name in sensors_name:
        if name in sensors:
            #r = {"name":name, "value":sensors[name]}
            r = (name, sensors[name])
        sensors_data.append(r)
    '''
    gpsdata = GetGPS()
    if len(gpsdata):
        print (gpsdata)
        time.sleep(1)

    '''
    SendData("dt_data_sensor", sdata)
    SendData("dt_data_entry", dtdata)
    print ("Success %d" % time.time())
    '''

droid.stopLocating()
droid.stopSensing()
