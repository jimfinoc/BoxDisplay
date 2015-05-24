#This is My Nest but it will slowly be converted to superClock!
import urllib
import urllib2
import sys
import json
import time

# Make sure your higher level directory has the JSON file called passwordFile.json
# The file should contain the information in the JSON format. See below for an example
# {"username": "email@somewhere.com", "password": "yourSuperSecretPassword!!!"}
# all temps from the Nest site are stored in degrees Celsius 

fileData = open('../passwordFile.json')
usernameAndPassword = json.load(fileData)
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

print"My Nest Data"
n0 = Nest(usernameAndPassword['username'],usernameAndPassword['password'], None, 0) #Downstairs
n1 = Nest(usernameAndPassword['username'],usernameAndPassword['password'], None, 1) #Upstairs
print " Logging On"
n1.login()
n0.login()
print " Getting Status"
n1.get_status()

n0.get_status()

print""
print "Upstairs Temperature"
print  c_to_f(n1.status["shared"][n1.serial]["current_temperature"])
print "Upstairs Humidity"
print n1.status["device"][n1.serial]["current_humidity"]

print ""
print "Downstairs Temperature"
print  c_to_f(n0.status["shared"][n0.serial]["current_temperature"])
print "Downstairs Humidity"
print n0.status["device"][n0.serial]["current_humidity"]
