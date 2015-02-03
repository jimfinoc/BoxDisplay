#This is My Nest!
import urllib
import urllib2
import sys
import json
import time

fileData = open('passwordFile.json')
usernameAndPassword = json.load(fileData)
#print "username:" + str(usernameAndPassword['username'])
#print "password:" + str(usernameAndPassword['password'])

def c_to_f(c):
        return c * 9.0 / 5.0 + 32.0


class Nest:
    def __init__(self, username, password, serial=None, index=0, units="F"):
        self.username = username
        self.password = password
        self.serial = serial
        self.units = units
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

    def show_curtemp(self):
        temp = self.status["shared"][self.serial]["current_temperature"]
        temp = self.temp_out(temp)

        print "%0.1f" % temp
    def temp_out(self, temp):
        if (self.units == "F"):
            return temp*1.8 + 32.0
        else:
            return temp


print"My Nest Data"
n0 = Nest(usernameAndPassword['username'],usernameAndPassword['password'], None, 0,"F") #Downstairs
n1 = Nest(usernameAndPassword['username'],usernameAndPassword['password'], None, 1,"F") #Upstairs
print " Logging On"
n1.login()
n0.login()
print " Getting Status"
n1.get_status()

n0.get_status()

print""
print""
#print "Upstairs Time Stamp"
#print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(n1.status["shared"][n1.serial]["$timestamp"]))
#print  n1.status["shared"][n1.serial]["$timestamp"]
print "Upstairs Temperature"
n1.show_curtemp()
print "Upstairs Humidity"
print n1.status["device"][n1.serial]["current_humidity"]


#print "Downstairs Time Stamp"
#print  n0.status["shared"][n0.serial]["$timestamp"]


print "Downstairs Temperature"
n0.show_curtemp()
print  c_to_f(n0.status["shared"][n0.serial]["current_temperature"])


print "Downstairs Humidity"
print n0.status["device"][n0.serial]["current_humidity"]

#print "SHARED"
#for d in n0.status["shared"][n0.serial]:
#    print d
#print ""
#print "DEVICE"
#for d in n0.status["device"][n0.serial]:
#    print d

#print n0.status["shared"][n0.serial]
#print n0.status["device"][n0.serial]
