#This is My Nest but it will slowly be converted to superClock!
import urllib
import urllib2
import sys
import json
import time
import requests
from Adafruit_7SegmentPlus import SevenSegment
import myColorText


# Make sure your higher level directory has the JSON file called passwordFile.json
# The file should contain the information in the JSON format. See below for an example
# {"username": "email@somewhere.com", "password": "yourSuperSecretPassword!!!"}
# all temps from the Nest site are stored in degrees Celsius 

fileData = open('../passwordFile.json')
usernameAndPassword = json.load(fileData)
valueTimeDate = None
#print "username:" + str(usernameAndPassword['username'])
#print "password:" + str(usernameAndPassword['password'])

def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0

class Nest:
    def __init__(self, username, password, serial=None, index=0):
        self.username = username
        self.password = password
        self.serial = serial
        self.index = index

    def loads(self, res):
        if hasattr(json, "loads"):
            res = json.loads(res)
        else:
            res = json.read(res)
        return res

    def login(self):
        data = urllib.urlencode({"username": self.username, "password": self.password})
        req = urllib2.Request("https://home.nest.com/user/login",
                              data,
                              {"user-agent":"Nest/1.1.0.10 CFNetwork/548.0.4"})
        res = urllib2.urlopen(req).read()
        res = self.loads(res)
        self.transport_url = res["urls"]["transport_url"]
        self.access_token = res["access_token"]
        self.userid = res["userid"]
        
    def get_status(self):
        req = urllib2.Request(self.transport_url + "/v2/mobile/user." + self.userid,
                              headers={"user-agent":"Nest/1.1.0.10 CFNetwork/548.0.4",
                                       "Authorization":"Basic " + self.access_token,
                                       "X-nl-user-id": self.userid,
                                       "X-nl-protocol-version": "1"})
        res = urllib2.urlopen(req).read()
        res = self.loads(res)
        self.structure_id = res["structure"].keys()[0]
        if (self.serial is None):
            self.device_id = res["structure"][self.structure_id]["devices"][self.index]
            self.serial = self.device_id.split(".")[1]
        self.status = res

    def show_status(self):
        shared = self.status["shared"][self.serial]
        device = self.status["device"][self.serial]
        allvars = shared
        allvars.update(device)
        for k in sorted(allvars.keys()):
             print k + "."*(32-len(k)) + ":", allvars[k]

# This assumes you have two Nest Thermostats. If you have more than 2, the number, index, after "None" 
# below will increment accordingly. If you only have one, it should just be 0. You have to create an object 
# for each nest thermostat. You could also specify the thermostats by serial number instead of the index.

def displayTemperature(segment = SevenSegment(address=0x70), temperature = None):
    "this will display the temperature on the specific segment"
    segment.disp.clear()
    if (temperature==None):
        segment.writeDigit(4, 0xF)
        return False
    else:
        segment.writeDigit(0, int(temperature) / 10)      	# Tens
        segment.writeDigit(1, int(temperature) % 10, True)  	# Ones
        segment.writeDigit(3, int(temperature) * 10 % 10)	# Tenths
        segment.writeDigit(4, 0xF)					        # F
        return True

def displayHumidity(segment = SevenSegment(address=0x70), humidiity = None):
    "this will display the humidiity on the specific segment"
    segment.disp.clear()
    if (humidiity==None):
        segment.writeDigit(0, 0xF)
        return False
    else:
        segment.setSpecialH(0) # displays an H in the 0 position
#        segment.writeDigit(1, int(temperature) % 10, True)  	# blank
        segment.writeDigit(3, int(humidiity) / 10)	# Tens
        segment.writeDigit(4, int(humidiity) % 10) # Ones
        return True

def displayTime(segment = SevenSegment(address=0x70),valueTimeDate = None):
    "this will display the time on the specific segment"

def displayDayMonth(segment = SevenSegment(address=0x70),valueTimeDate = None):
    "this will display the day and month on the specific segment"

def displayYear(segment = SevenSegment(address=0x70),valueTimeDate = None):
    "this will display the year on the specific segment"

print "Initalizing the displays"
segmentLevelBase = SevenSegment(address=0x70)
segmentLevelZero = SevenSegment(address=0x72)
segmentLevelOne = SevenSegment(address=0x74)
print " Setting brightness"
segmentLevelBase.disp.setBrightness(10)
segmentLevelZero.disp.setBrightness(10)
segmentLevelOne.disp.setBrightness(10)

print ""
print "Trying to get data from the Nest Web"
try:
    print "My Nest Data"
    n0 = Nest(usernameAndPassword['username'],usernameAndPassword['password'], None, 0) #Level Zero
    n1 = Nest(usernameAndPassword['username'],usernameAndPassword['password'], None, 1) #Level One
    print " Logging On"
    n1.login()
    n0.login()
    print " Getting Status"
    n1.get_status()
    n0.get_status()
    levelOneTemperature = int(c_to_f(n1.status["shared"][n1.serial]["current_temperature"]))
    levelOneHumidity = n1.status["device"][n1.serial]["current_humidity"]
    levelZeroTemperature =  c_to_f(n0.status["shared"][n0.serial]["current_temperature"])
    levelZeroHumidity = n0.status["device"][n0.serial]["current_humidity"]
except:
    print "setting One and Zero to None"
    levelOneTemperature = None
    levelOneHumidity = None
    levelZeroTemperature = None
    levelZeroHumidity = None

print ""
print "Getting data from the internal web device"
try:
    print " getting the date from the site"
    r = requests.get("http://10.0.1.211")
    print " pulling values"
    levelBaseTemperature = float(r.json()["temperature"])
    levelBaseHumidity = float(r.json()["humidity"])
    levelBaseTime = str(r.json()["localTime"])
except:
    print " setting base to None"
    levelBaseTemperature = None
    levelBaseHumidity = None
    levelBaseTime = None

print""
print "Level One Temperature"
printColor(str(levelOneTemperature))
print "Level One Humidity"
print levelOneHumidity

print ""
print "Level Zero Temperature"
print levelZeroTemperature
print "Level Zero Humidity"
print levelZeroHumidity

print ""
print "Level Base Time"
print levelBaseTime
print "Level Base Temperature"
print levelBaseTemperature
print "The value of the webpage temp"
print levelBaseHumidity

print ""
print "sending temp data to the external displays"
displayTime(segmentLevelOne,valueTimeDate)
displayDayMonth(segmentLevelZero,valueTimeDate)
displayYear(segmentLevelBase, valueTimeDate)

print""
print "sleeping for 4 seconds"
time.sleep(4)
print "sending temp data to the external displays"
displayTemperature(segmentLevelOne,levelOneTemperature)
displayTemperature(segmentLevelZero,levelZeroTemperature)
displayTemperature(segmentLevelBase, levelBaseTemperature)

print ""
print "sleeping for 4 more seconds"
time.sleep(4)
print "sending humid data to the external displays"
displayHumidity(segmentLevelOne,levelOneHumidity)
displayHumidity(segmentLevelZero,levelZeroHumidity)
displayHumidity(segmentLevelBase, levelBaseHumidity)
print "sleeping for another 4 seconds"
time.sleep(4)

print ""
print "initial routine finished"

