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
import DOHPC.sendHP as SH
import DOHPC.showHP as DHP

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
    parser.add_argument('-d','--display', action='store_true',
                    help='Just display all the info dont change a thing',
                    dest='display')
    parser.add_argument('-fd','--fancy-display','--thermostat',
                    help='Use NPYSCREEN to display the info and run as a thermostat',
                    dest='fdisplay')
    parser.add_argument('-cdb','--create-database',
                    help='Creates a SQLITE database for you - takes filename as argument.(besure to update the config.ini)',
                    dest='cdataBase')
    parser.add_argument('-db','--database',
                    help='SQLITE file location.(besure to update the config.ini)',
                    dest='dataBase')
    parser.add_argument('-s','--send',
                    help='argument can be (T) for temperature or (S) for schedule bust be paired with -v',
                    dest='sendType')
    parser.add_argument('-v','--value',
                    help='The value to send to the heatpump \n(int for temperature for schedule see DOCUMENTATION)',
                    dest='sendValue')
    parser.add_argument('-r','--read', action='store_true',
                    help='Set me and I will read the pump and put it in the DB ',
                    dest='readFlag')
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
        elif daikinIP == "":
            daikinIP = ""
        elif daikinIP != "":
            DaikinIP = daikinIP
        else:
            print("Error found in IP")
            sys.exit(1)
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
        if args.readFlag:
            RH.readHPDetails(daikinIP, daikinDataBase, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinDevices)
            if args.display:
                DHP.showHPDetails(daikinIP, daikinDataBase, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinDevices)
        elif args.display:
            DHP.showHPDetails(daikinIP, daikinDataBase, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinDevices)
        # Run into a while loop here that does its magic.
        #pass

    """
    Now that we have the valeus, time to do send a new temperature, or schedule to the heatpump
    """
    if args.sendType:
        # we want to send a value
        if args.sendValue:
            SH.sendHPvalues(args.sendType, args.sendValue, daikinIP, daikinDataBase, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinDevices)
        else:
            print("No data to send")
            sys.exit(1)

if __name__ == "__main__":
    # Run program
    main()
