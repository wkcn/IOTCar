#coding=utf-8
try:
    import sl4a
except:
    import fakesl4a as sl4a 
import urllib.parse
import urllib.request
import time
import json
import random
import os
import datetime
import csv
import uuid

SERVER_ADDR = "http://45.32.48.44:5000/"
#SERVER_ADDR = "http://127.0.0.1:5000/"
#SERVER_ADDR = "http://192.168.3.52:5000/"
INTERVAL_SECONDS = 10

droid = sl4a.Android()
droid.startSensingTimed(1,500)
droid.startLocating(1, 1) # updateTime(milliseconds), minUpdateDistance(meters)

def SendData(name, data):
    #return
    #try:
    headers = {'Content-Type': 'application/json'}
    jdata = json.dumps(data)
    bdata = bytes(jdata, "utf8")
    print (SERVER_ADDR + name)
    req = urllib.request.Request(url = SERVER_ADDR + name, data = bdata)
    req.add_header('Content-Type', 'application/json')
    urllib.request.urlopen(req, timeout=5)
    #except:
    #    print ("send failed")

def get_time():
    # Get current time
    # return a string %Y%m%d%H%M%S
    return time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))

def GetID(name):
    w = str(uuid.uuid1()) + name
    code = 0
    x = 1
    for c in w:
        code += ord(c) * x
        x *= 10
    return code % 1e9 

# MobileID is a int
def GetMobileID():
    return GetID("MobileID")

def GetGPSID():
    return GetID("GPSID")

def GetGPS():
    loc = droid.readLocation().result
    if len(loc) == 0 and False:
        loc = droid.getLastKnownLocation().result
    return loc

MobileID = GetMobileID()
GPSID = GetGPSID()
print ("Your MobileID is %d" % GetMobileID())
print ("Your GPSID is %d" % GetGPSID())
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

    stime = get_time()
    gpsdata = GetGPS()
    if len(gpsdata):
        print(gpsdata)
        
        if "gps" in gpsdata and len(gpsdata["gps"]):
            gd = {
                "GPSID": GPSID,
                "MobileID": MobileID,
                "GPSTime": stime,
                "Longitude":gpsdata["gps"]["longitude"],
                "Latitude":gpsdata["gps"]["latitude"],
                "Speed":gpsdata["gps"]["speed"]
            }
            SendData("add_new_location", gd)

    sensors = droid.readSensors().result
    sensors["MobileID"] = MobileID
    sensors["StickTime"] = stime
    
    SendData("add_new_sensor", sensors)
    print (sensors)
    time.sleep(INTERVAL_SECONDS)

    '''
    SendData("dt_data_sensor", sdata)
    SendData("dt_data_entry", dtdata)
    print ("Success %d" % time.time())
    '''

droid.stopLocating()
droid.stopSensing()
