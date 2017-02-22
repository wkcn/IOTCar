#coding=utf-8

class Sensor:
    sensors_name = ["light", "pitch", "roll", "azimuth", "xMag", "yMag", "zMag", "xforce", "yforce", "zforce", "accuracy"]
    @property
    def result(self):
        res = {}
        for name in Sensor.sensors_name:
            res[name] = 0.0
        return res

class Location:
    @property
    def result(self):
        return {"longitude":117, "latitude":32, "speed":3}

class Android:
    Android = 0
    def startSensingTimed(self, a, b):
        print ("START FAKE SL4A")
    def stopSensing(self):
        print ("STOP FAKE SL4A")
    def readSensors(self):
        return Sensor()
    def startLocating(self, a = 0, b = 0):
        print ("START FAKE LOCATING")
    def stopLocating(self):
        print ("STOP FAKE LOCATING")
    def readLocation(self):
        return Location()
    def getLastKnownLocation(self):
        return Location()
