#!/usr/bin/env python2.7
"""
This script will read nest thermostat values and will post to COSM.com

It is using cosm.cfg which is JSON dictionary with following fields:

{
"key":"your key"
"feed":123,
 "nest_user":"user@example.com",
 "nest_password":"secret",
 "units":"C",
 "fields": {
          "current_temperature":1,
          "current_humidity":2,
          "fan_mode":3,
 }
}
"""

import json
import sys
import logging
import string
import getopt
import cosm
from nest import Nest

CFG_FILE="cosm.cfg"
COSM_LOGFILE="cosm.log"

def usage():
    print """
%s [-f <cfg file>] [-c] [-d] 

-c -- log to console instead of log file
-d -- dry-run mode. No data submitted.
-f <cfg file> -- config file name. Default is '%s'
-l <log file> -- config file name. Default is '%s'

"""  % (sys.argv[0],CFG_FILE,COSM_LOGFILE)

def read_config(cfg_fname):
    log.info("Reading config file %s" % cfg_fname)
    f=open(cfg_fname,"r")
    try:
        return json.load(f)
    finally:
        f.close()

def main():
    global log
    global debug_mode

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'dcf:l:', [])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    console = False
    debug_mode = False
    cfg_fname = CFG_FILE
    log_fname = COSM_LOGFILE
    
    for o, a in opts:
        if o in ['-d']:
            debug_mode = True
        elif o in ['-c']:
            console = True
        elif o in ['-f']:
            cfg_fname = a
        elif o in ['-l']:
            log_fname = a
        else:
            usage()
            sys.exit(1)

    log_format = '%(asctime)s %(process)d %(filename)s:%(lineno)d %(levelname)s %(message)s'
    if debug_mode:
        log_level=logging.DEBUG
    else:
        log_level=logging.INFO
    if console:
        logging.basicConfig(level=log_level, format=log_format)
    else:
        logging.basicConfig(level=log_level, format=log_format,
                            filename=log_fname, filemode='a')
    log = logging.getLogger('default')

    try:
        cfg = read_config(cfg_fname)
    except Exception, ex:
        log.error("Error reading config file %s" % ex)
        sys.exit(1)
        
    fields = cfg["fields"]

    try:
        n = Nest(cfg["nest_user"],cfg["nest_password"],units=cfg["units"])
        n.login()
        n.get_status()
        shared = n.status["shared"][n.serial]
        device = n.status["device"][n.serial]
        allvars = shared
        allvars.update(device)
    except Exception, ex:
        log.error("Error connecting to NEST: %s" % ex )
        sys.exit(100)

    data = ""
    for fname,fds in fields.items():
        if allvars.has_key(fname):
            data = data + string.join([str(fds),str(allvars[fname])],",")+"\r\n"
        else:
            log.warning("Field '%s' not found!", fname)
    try:
        if not debug_mode:
            log.info("Updating feed %s" % cfg["feed"])
            cosm.update_feed(cfg["feed"],cfg["key"],data)
        else:
            log.debug(data)
    except Exception, ex:
        log.error("Error sending to COSM: %s" % ex )
        sys.exit(102)
            
    log.debug("Done")


if __name__ == '__main__':
    main()
