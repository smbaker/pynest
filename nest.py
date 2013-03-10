#! /usr/bin/python

# nest.py -- a python interface to the Nest Thermostat
# by Scott M Baker, smbaker@gmail.com, http://www.smbaker.com/
#
# Usage:
#    'nest.py help' will tell you what to do and how to do it
#
# Licensing:
#    This is distributed unider the Creative Commons 3.0 Non-commecrial,
#    Attribution, Share-Alike license. You can use the code for noncommercial
#    purposes. You may NOT sell it. If you do use it, then you must make an
#    attribution to me (i.e. Include my name and thank me for the hours I spent
#    on this)
#
# Acknowledgements:
#    Chris Burris's Siri Nest Proxy was very helpful to learn the nest's
#       authentication and some bits of the protocol.

import urllib
import urllib2
import sys
from optparse import OptionParser

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

def create_parser():
   parser = OptionParser(usage="nest [options] command [command_options] [command_args]",
        description="Commands: fan temp",
        version="unknown")

   parser.add_option("-u", "--user", dest="user",
                     help="username for nest.com", metavar="USER", default=None)

   parser.add_option("-p", "--password", dest="password",
                     help="password for nest.com", metavar="PASSWORD", default=None)

   parser.add_option("-s", "--serial", dest="serial", default=None,
                     help="optional, specify serial number of nest thermostat to talk to")

   parser.add_option("-i", "--index", dest="index", default=0, type="int",
                     help="optional, specify index number of nest to talk to")


   return parser

def help():
    print "syntax: nest [options] command [command_args]"
    print "options:"
    print "   --user <username>      ... username on nest.com"
    print "   --password <password>  ... password on nest.com"
    print "   --serial <number>      ... optional, specify serial number of nest to use"
    print "   --index <number>       ... optional, 0-based index of nest"
    print "                                (use --serial or --index, but not both)"
    print
    print "commands: temp, fan, show, curtemp, curhumid, away"
    print "    temp <temperature>    ... set target temperature"
    print "    fan [auto|on]         ... set fan state"
    print "    away                  ... toggle away"
    print "    show                  ... show everything"
    print "    curtemp               ... print current temperature"
    print "    curhumid              ... print current humidity"
    print
    print "examples:"
    print "    nest.py --user joe@user.com --password swordfish temp 73"
    print "    nest.py --user joe@user.com --password swordfish fan auto"

def main():
    parser = create_parser()
    (opts, args) = parser.parse_args()

    if (len(args)==0) or (args[0]=="help"):
        help()
        sys.exit(-1)

    if (not opts.user) or (not opts.password):
        print "how about specifying a --user and --password option next time?"
        sys.exit(-1)

    n = Nest(opts.user, opts.password, opts.serial, opts.index)
    n.login()
    n.get_status()

    cmd = args[0]

    if (cmd == "temp"):
        if len(args)<2:
            print "please specify a temperature"
            sys.exit(-1)
        n.set_temperature(int(args[1]))
    elif (cmd == "fan"):
        if len(args)<2:
            print "please specify a fan state of 'on' or 'auto'"
            sys.exit(-1)
        n.set_fan(args[1])
    elif (cmd == "away"):
        n.toggle_away()
    elif (cmd == "show"):
        n.show_status()
    elif (cmd == "curtemp"):
        n.show_curtemp()
    elif (cmd == "curhumid"):
        print n.status["device"][n.serial]["current_humidity"]
    else:
        print "misunderstood command:", cmd
        print "do 'nest.py help' for help"

if __name__=="__main__":
   main()
