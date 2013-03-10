 pynest -- a python interface for the Nest Thermostat
 by Scott M Baker, smbaker@gmail.com, http://www.smbaker.com/

 pyenest - the above, Altered
 by Eugene Efremov, eaefremov@gmail.com

 Usage:
    'nest.py' can be used from the command line exactly as before.
    It can also be imported and used programmatically, either exactly as Scott's version,
    or by passing parameters identifying specific structures and devices for setups where
    you have multiples or want to be agnostic.

 Example:
    'nest.py --user joe@user.com --password swordfish temp 73'
         set the temperature to 73 degrees

    'nest.py --user joe@user.com --password swordfish fan auto'
         set the fan to automatic

 Installation:
    'python ./setup.py install' will install nest.py to the right place,
    usually your /usr/bin directory.

 Licensing:
    This is distributed unider the Creative Commons 3.0 Non-commecrial,
    Attribution, Share-Alike license. You can use the code for noncommercial
    purposes. You may NOT sell it. If you do use it, then you must make an
    attribution to me (i.e. Include my name and thank me for the hours I spent
    on this)

 Acknowledgements:
    Chris Burris's Siri Nest Proxy was very helpful to learn the nest's
       authentication and some bits of the protocol.
    Scott Baker's nest.py, which I (Eugene Efremov) shamelessly bastardized, was irreplaceable
       and without it I likely wouldn't have done any of this.

