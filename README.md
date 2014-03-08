#nest_thermostat

**a Python interface for the Nest Thermostat**
 
*fork of pynest by Scott M Baker, smbaker@gmail.com, http://www.smbaker.com/*

##Installation
`python ./setup.py install` will install nest.py to the right place,
usually your /usr/bin directory.

##Usage

```
syntax: nest.py [options] command [command_args]
options:
   --user <username>      ... username on nest.com
   --password <password>  ... password on nest.com
   --celsius              ... use celsius (the default is farenheit)
   --serial <number>      ... optional, specify serial number of nest to use
   --index <number>       ... optional, 0-based index of nest
                                (use --serial or --index, but not both)

commands: temp, fan, show, curtemp, curhumid
    temp <temperature>    ... set target temperature
    fan [auto|on]         ... set fan state
    show                  ... show everything
    curtemp               ... print current temperature
    curhumid              ... print current humidity

examples:
    nest.py --user joe@user.com --password swordfish temp 73
    nest.py --user joe@user.com --password swordfish fan auto
```


---

*Chris Burris's Siri Nest Proxy was very helpful to learn the Nest's authentication and some bits of the protocol.*
