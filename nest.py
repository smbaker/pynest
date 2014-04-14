#! /usr/bin/python

"""
nest.py -- a python interface to the Nest Thermostat
"""

import sys
from optparse import OptionParser
from nest_thermostat import Nest

def create_parser():
   parser = OptionParser(usage="nest [options] command [command_options] [command_args]",
        description="Commands: fan temp",
        version="unknown")

   parser.add_option("-u", "--user", dest="user",
                     help="username for nest.com", metavar="USER", default=None)

   parser.add_option("-p", "--password", dest="password",
                     help="password for nest.com", metavar="PASSWORD", default=None)

   parser.add_option("-c", "--celsius", dest="celsius", action="store_true", default=False,
                     help="use celsius instead of farenheit")

   parser.add_option("-s", "--serial", dest="serial", default=None,
                     help="optional, specify serial number of nest thermostat to talk to")

   parser.add_option("-i", "--index", dest="index", default=0, type="int",
                     help="optional, specify index number of nest to talk to")


   return parser

def help():
    print( "syntax: nest.py [options] command [command_args]")
    print( "options:")
    print( "   --user <username>      ... username on nest.com")
    print( "   --password <password>  ... password on nest.com")
    print( "   --celsius              ... use celsius (the default is farenheit)")
    print( "   --serial <number>      ... optional, specify serial number of nest to use")
    print( "   --index <number>       ... optional, 0-based index of nest")
    print( "                                (use --serial or --index, but not both)")
    print()
    print( "commands:")
    print( "    temp <temperature>         ... set target temperature")
    print( "    fan [auto|on]              ... set fan state")
    print( "    mode [cool|heat|range|off] ... set mode state")
    print( "    away                       ... toggle away")
    print( "    show                       ... show everything")
    print( "    curtemp                    ... print current temperature")
    print( "    curhumid                   ... print current humidity")
    print( "    curmode                    ... print current mode")
    print( "    curtarget                  ... print current target temp")
    print()
    print( "examples:")
    print( "    nest.py --user joe@user.com --password swordfish temp 73")
    print( "    nest.py --user joe@user.com --password swordfish fan auto")

def main():
    parser = create_parser()
    (opts, args) = parser.parse_args()

    if (len(args)==0) or (args[0]=="help"):
        help()
        sys.exit(-1)

    if (not opts.user) or (not opts.password):
        print( "how about specifying a --user and --password option next time?")
        sys.exit(-1)

    if opts.celsius:
        units = "C"
    else:
        units = "F"

    n = Nest(opts.user, opts.password, opts.serial, opts.index, units=units)
    n.login()
    n.get_status()

    cmd = args[0]

    if (cmd == "temp"):
        if len(args)<2:
            print( "please specify a temperature")
            sys.exit(-1)
        n.set_temperature(int(args[1]))
    elif (cmd == "fan"):
        if len(args)<2:
            print( "please specify a fan state of 'on' or 'auto'")
            sys.exit(-1)
        n.set_fan(args[1])
    elif (cmd == "mode"):
        if len(args)<2:
            print( "valid modes are cool, heat, range, and off")
            sys.exit(-1)
        n.set_mode(args[1])
    elif (cmd == "away"):
        n.toggle_away()
    elif (cmd == "show"):
        n.show_status()
    elif (cmd == "curtemp"):
        n.show_curtemp()
    elif (cmd == "curmode"):
        n.show_curmode()
    elif (cmd == "curtarget"):
        n.show_target()
    elif (cmd == "curhumid"):
        print( n.status["device"][n.serial]["current_humidity"])
    else:
        print( "misunderstood command: %s" % cmd)
        print( "do 'nest.py help' for help")

if __name__=="__main__":
   main()
