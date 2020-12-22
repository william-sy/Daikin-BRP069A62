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
import argparse, time, sys, json
import DOHPC.readConfig as RC
import DOHPC.findIP as FI
import DOHPC.readHP as RH
import DOHPC.createDB as CDB

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
    parser.add_argument('-n','--number', nargs='+',
                    help='The ammount of daikin devices you have (need to be used with --ip or --fip)',
                    dest='number')
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
    parser.add_argument('-cdb','--create-database',
                    help='Creates a SQLITE database for you - takes filename as argument.(besure to update the config.ini)',
                    dest='cdataBase')
    parser.add_argument('-db','--database',
                    help='SQLITE file location.(besure to update the config.ini)',
                    dest='dataBase')
    args = parser.parse_args()

    if args.cdataBase:
        # we want to initialize a DB
        #print(args.cdataBase)
        CDB.createDatabase(args.cdataBase)
        sys.exit(1)

    if args.dataBase:
        # database is over written.
        daikinDataBase = args.dataBase
    else:
        daikinDataBase = ""

    if args.file:
        # User gave a config file
        givenConfig = args.file
        daikinSearch, daikinSerial, daikinIP, daikinDevices, daikinDataBase, daikinUrlError, daikinUrlBase, daikingUrlDisc = RC.readConfig(givenConfig)
        if daikinSearch == "True":
            # ^- need to convert to booleans
            DaikinIP = FI.findIP(daikinSerial)
            #print(DaikinIP)
        else:
            daikinIP = ""
    else:
        # Not pretty, but it works :)
        if args.IP:
            # You know the IP, no need to find it
            daikinIP = args.IP[0]
            if args.number:
                daikinDevices = args.number[0]
            else:
                daikinDevices = ""
        elif args.findIP:
            # You want to find the ip
            daikinSerial = args.findIP[0]
            daikinIP = FI.findIP(daikinSerial)
            if args.number:
                daikinDevices = args.number[0]
            else:
                daikinDevices = ""
        else:
            daikinIP = ""

    """
    From here we should have a IP to work with.
    Time to do some actual work with the heatpump.
    """
    # Read Heatpump values:
    if daikinIP == "" or daikinDevices == "" or daikinDataBase == "":
        print("There is no IP adress, or amount of devices specified, cannot read heatpump")
        sys.exit(1)
    elif daikinUrlError == "" or daikinUrlBase == "" or daikingUrlDisc == "":
        # In case still no config file is being used :(
        daikinUrlError = "/[0]/MNAE/"
        daikinUrlBase = "/[0]/MNCSE-node/"
        daikingUrlDisc = "/[0]/MNAE/0"
    else:
        # Read current settings from the heatpump
        RH.readHPDetails(daikinIP, daikinDataBase, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinDevices)
        # Run into a while loop here that does its magic.

if __name__ == "__main__":
    # Run program
    main()
