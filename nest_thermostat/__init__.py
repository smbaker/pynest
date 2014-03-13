#! /usr/bin/python

"""
nest_thermostat -- a python interface to the Nest Thermostat
by Scott M Baker, smbaker@gmail.com, http://www.smbaker.com/
updated by Bob Pasker bob@pasker.net http://pasker.net
"""

import requests

try:
   import json
except ImportError:
   import simplejson as json

class Nest:
    def __init__(self, username, password, serial=None, index=0, units="F", debug=False):
        self.username = username
        self.password = password
        self.serial = serial
        self.units = units
        self.index = index
        self.debug = debug

    def login(self):

       response = requests.post("https://home.nest.com/user/login",
                                data = {"username":self.username, "password" : self.password},
                                headers = {"user-agent":"Nest/1.1.0.10 CFNetwork/548.0.4"})

       response.raise_for_status()

       res = response.json()
       self.transport_url = res["urls"]["transport_url"]
       self.access_token = res["access_token"]
       self.userid = res["userid"]
       # print self.transport_url, self.access_token, self.userid

    def get_status(self):
       response = requests.get(self.transport_url + "/v2/mobile/user." + self.userid,
                               headers={"user-agent":"Nest/1.1.0.10 CFNetwork/548.0.4",
                                        "Authorization":"Basic " + self.access_token,
                                        "X-nl-user-id": self.userid,
                                        "X-nl-protocol-version": "1"})

       response.raise_for_status()
       res = response.json()

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

    def temp_in(self, temp):
        if (self.units == "F"):
            return (temp - 32.0) / 1.8
        else:
            return temp

    def temp_out(self, temp):
        if (self.units == "F"):
            return temp*1.8 + 32.0
        else:
            return temp

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

    def show_target(self):
        temp = self.status["shared"][self.serial]["target_temperature"]
        temp = self.temp_out(temp)

        print temp

    def show_curmode(self):
        mode = self.status["shared"][self.serial]["target_temperature_type"]

        print mode

    def _set(self, data, which):
       if (self.debug): print json.dumps(data)
       url = "%s/v2/put/%s.%s" %  (self.transport_url, which, self.serial)
       if (self.debug): print url
       response = requests.post(url,
                                data = json.dumps(data),
                                headers = {"user-agent":"Nest/1.1.0.10 CFNetwork/548.0.4",
                                           "Authorization":"Basic " + self.access_token,
                                           "X-nl-protocol-version": "1"})

       if response.status_code > 200:
          if (self.debug): print response.content
       response.raise_for_status()
       return response

    def _set_shared(self, data):
       self._set(data, "shared")

    def _set_device(self, data):
       self._set(data, "device")

    def set_temperature(self, temp):
       return self._set_shared({
             "target_change_pending": True,
             "target_temperature" : self.temp_in(temp)
             })

    def set_fan(self, state):
       return self._set_device({
             "fan_mode": str(state)
             })

    def set_mode(self, state):
        return self._set_shared({
            "target_temperature_type": str(state)
        })

    def toggle_away(self):
        was_away = self.status['structure'][self.structure_id]['away']
        data = '{"away":%s}' % ('false' if was_away else 'true')
        response = requests.post(self.transport_url + "/v2/put/structure." + self.structure_id,
                                 data = data,
                                 headers = {"user-agent":"Nest/1.1.0.10 CFNetwork/548.0.4",
                                            "Authorization":"Basic " + self.access_token,
                                            "X-nl-protocol-version": "1"})
        response.raise_for_status()
        return response
