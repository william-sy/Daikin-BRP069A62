#!/usr/bin/env python3
# author(s):
__author__ = "William van Beek"
__copyright__ = ""
__credits__ = ["William van Beek"]
__license__ = "GPL-3.0-only"
__version__ = "0.1"
__maintainer__ = "William van Beek"
__email__ = ""
__status__ = "Testing"

# Imports:
import argparse, time, sys
import DOHPC.readConfig as RC
import DOHPC.findIP as FI
import DOHPC.readHP as RH

def main():
    # Get input form user
    parser = argparse.ArgumentParser(
        description='Daikin OpenSourece HeatPump Controller - (DOHPC)'
    )
    parser.add_argument('-fip','--find-ip', nargs='+',
                    help='If you want to automatically find the IP by mDNS, Must come with a serial number!',
                    dest='findIP')
    parser.add_argument('-ip','--ip', nargs='+',
                    help='You know your IP (nerd!), and want to just use it',
                    dest='IP')
    parser.add_argument('-f','--file',
                    help='The config file to use (./config.ini), this removes the need for other flags',
                    dest='file')
    parser.add_argument('-d','--display',
                    help='Just display all the info dont change a thing',
                    )
    parser.add_argument('-fd','--fancy-display','--thermostat',
                    help='Use NPYSCREEN to display the info and run as a thermostat',
                    )
    parser.add_argument('-w','--write',
                    help='Supply a configuration to the heatpump.\nUse other scripts to make this one update the heatpump.',
                    dest='writeFile')

    args = parser.parse_args()

    if args.file:
        # User gave a config file
        givenConfig = args.file
        daikinSearch, daikinSerial, daikinIP = RC.readConfig(givenConfig)
        if daikinSearch == "True":
            # ^- need to convert to booleans
            DaikinIP = FI.findIP(daikinSerial)
            print(DaikinIP)
        else:
            daikinIP = ""
    else:
        if args.IP:
            # You know the IP, no need to find it
            daikinIP = args.IP[0]
        elif args.findIP:
            # You want to find the ip
            daikinSerial = args.findIP[0]
            DaikinIP = FI.findIP(daikinSerial)
            print(DaikinIP)
        else:
            daikinIP = ""

    """
    From here we should have a IP to work with.
    Time to do some actual work with the heatpump.
    """
    # Read Heatpump values:
    if daikinIP == "":
        print("There is no IP adress specified, cannot read heatpump")
        sys.exit(1)
    else:
        RH.readHP()


    # Start TUI here with argument

if __name__ == "__main__":
    # Run program
    main()
