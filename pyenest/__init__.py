import json
import urllib
import urllib2

from data import Account, Structure, Device, clean_id

class Nest(object):
  def __init__(self, username, password):
    self.username = username
    self.password = password

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

    self.status = self.loads(res)

  @property
  def simple_status(self):
    user_id, user = self.status['user'].items()[0]
    account = Account(id=user_id, name=user['name'], device_keys=self.status['device'].keys(),
                      structure_keys=self.status['structure'].keys(), shared_keys=self.status['shared'].keys())

    for link in self.status['link'].values():
      structure_key = link['structure']
      structure_id = clean_id(structure_key)
      struct = self.status['structure'][structure_id]
      structure = Structure(id=structure_id, name=struct['name'], location=struct['location'], away=struct['away'],
                            num_thermostats=struct['num_thermostats'])
      account.structures.append(structure)

      for device_key in struct['devices']:
        device_id = clean_id(device_key)
        dev = self.status['device'][device_id]
        shared = self.status['shared'][device_id]
        device = Device(id=device_id, name=shared['name'], system_mode=dev['current_schedule_mode'],
                        scale=dev['temperature_scale'], temperature=shared['current_temperature'],
                        target=shared['target_temperature'], heater_on=shared['hvac_heater_state'],
                        ac_on=shared['hvac_ac_state'], fan_mode=dev['fan_mode'], fan_on=shared['hvac_fan_state'])

        structure.devices.append(device)
    return account

  def show_curtemp(self, serial):
    temp = self.status["shared"][serial]["current_temperature"]

    print "%0.1f" % temp

  def set_temperature(self, temp, serial):

    data = '{"target_change_pending":true,"target_temperature":' + '%0.1f' % temp + '}'
    req = urllib2.Request(self.transport_url + "/v2/put/shared." + serial,
                data,
                {"user-agent":"Nest/1.1.0.10 CFNetwork/548.0.4",
                 "Authorization":"Basic " + self.access_token,
                 "X-nl-protocol-version": "1"})

    res = urllib2.urlopen(req).read()

    print res

  def set_fan(self, state, serial):
    data = '{"fan_mode":"' + str(state) + '"}'
    req = urllib2.Request(self.transport_url + "/v2/put/device." + serial,
                data,
                {"user-agent":"Nest/1.1.0.10 CFNetwork/548.0.4",
                 "Authorization":"Basic " + self.access_token,
                 "X-nl-protocol-version": "1"})

    res = urllib2.urlopen(req).read()

    print res
  
  def toggle_away(self, structure_id):
    was_away = self.status['structure'][structure_id]['away']
    data = '{"away":%s}' % ('false' if was_away else 'true')
    req = urllib2.Request(self.transport_url + "/v1/put/structure." + structure_id,
                data,
                {"user-agent":"Nest/1.1.0.10 CFNetwork/548.0.4",
                 "Authorization":"Basic " + self.access_token,
                 "X-nl-protocol-version": "1"})

    res = urllib2.urlopen(req).read()

    print res
