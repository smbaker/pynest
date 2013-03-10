import urllib
import urllib2

try:
   import json
except ImportError:
   try:
       import simplejson as json
   except ImportError:
       print "No json library available. I recommend installing either python-json"
       print "or simpejson."
       sys.exit(-1)

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

        #print "res.keys", res.keys()
        #print "res[structure][structure_id].keys", res["structure"][self.structure_id].keys()
        #print "res[device].keys", res["device"].keys()
        #print "res[device][serial].keys", res["device"][self.serial].keys()
        #print "res[shared][serial].keys", res["shared"][self.serial].keys()

    def show_status(self, serial=None):
        serial = serial or self.serial
        shared = self.status["shared"][serial]
        device = self.status["device"][serial]

        allvars = shared
        allvars.update(device)

        for k in sorted(allvars.keys()):
             print k + "."*(32-len(k)) + ":", allvars[k]

    def show_curtemp(self, serial=None):
        serial = serial or self.serial
        temp = self.status["shared"][serial]["current_temperature"]

        print "%0.1f" % temp

    def set_temperature(self, temp, serial=None):
        serial = serial or self.serial

        data = '{"target_change_pending":true,"target_temperature":' + '%0.1f' % temp + '}'
        req = urllib2.Request(self.transport_url + "/v2/put/shared." + serial,
                              data,
                              {"user-agent":"Nest/1.1.0.10 CFNetwork/548.0.4",
                               "Authorization":"Basic " + self.access_token,
                               "X-nl-protocol-version": "1"})

        res = urllib2.urlopen(req).read()

        print res

    def set_fan(self, state, serial=None):
        serial = serial or self.serial
        data = '{"fan_mode":"' + str(state) + '"}'
        req = urllib2.Request(self.transport_url + "/v2/put/device." + serial,
                              data,
                              {"user-agent":"Nest/1.1.0.10 CFNetwork/548.0.4",
                               "Authorization":"Basic " + self.access_token,
                               "X-nl-protocol-version": "1"})

        res = urllib2.urlopen(req).read()

        print res
    
    def toggle_away(self, structure_id=None):
        structure_id = structure_id or self.structure_id
        was_away = self.status['structure'][structure_id]['away']
        data = '{"away":%s}' % ('false' if was_away else 'true')
        req = urllib2.Request(self.transport_url + "/v1/put/structure." + structure_id,
                              data,
                              {"user-agent":"Nest/1.1.0.10 CFNetwork/548.0.4",
                               "Authorization":"Basic " + self.access_token,
                               "X-nl-protocol-version": "1"})

        res = urllib2.urlopen(req).read()

        print res

