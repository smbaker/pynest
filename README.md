 pynest -- a python interface for the Nest Thermostat
==================================
 by Scott M Baker, smbaker@gmail.com, http://www.smbaker.com/

API:
----

nest.py define Nest class which could be used to communicate with thermostat.

Comand-line tool:
--------------
 Usage:
    'nesttool.py help' will tell you what to do and how to do it

 Example:
    'nesttool.py --user joe@user.com --password swordfish temp 73'
         set the temperature to 73 degrees

    'nesttool.py --user joe@user.com --password swordfish fan auto'
         set the fan to automatic


COSM submission:
---------------

'nest_cosm.py' script could be used to submit thermostat data to COSM: http://cosm.com/ 

Usage:

        ./nest_cosm.py [-f <cfg file>] [-c] [-d]a

        -c -- log to console instead of log file
        -d -- dry-run mode. No data submitted.
        -f <cfg file> -- config file name. Default is 'cosm.cfg'
        -l <log file> -- config file name. Default is 'cosm.log'

Configuration file example:

    {
       "key":"your key"
       "feed":123,
        "nest_user":"user@example.com",
        "nest_password":"secret",
        "units":"C",
        "fields": {
            "current_temperature":{"datastream":1},
            "current_humidity":{"datastream":2},
            "fan_mode":{"datastream":3, 
                        "mapping":{
                            "off":-1,
                            "on":1,
                            "auto":0
                        }},
            "hvac_ac_state": {"datastream":4,"mapping":{
                "False":0,
                "True":1
            }},
            "hvac_heater_state":{"datastream":5,"mapping":{
                "False":0,
                "True":1
            }},
            "battery_level":{"datastream":100}
        }
    }
       
Sample feed: https://cosm.com/feeds/131118

    

Installation:
----------
    'python ./setup.py install' will install nesttool.py and nest_cosm.py to the right place,
    usually your /usr/bin directory.

Licensing:
---------
    This is distributed unider the Creative Commons 3.0 Non-commecrial,
    Attribution, Share-Alike license. You can use the code for noncommercial
    purposes. You may NOT sell it. If you do use it, then you must make an
    attribution to me (i.e. Include my name and thank me for the hours I spent
    on this)

Acknowledgements:
----------------
    Chris Burris's Siri Nest Proxy was very helpful to learn the nest's
       authentication and some bits of the protocol.

