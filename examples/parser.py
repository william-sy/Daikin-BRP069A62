#!/usr/bin/env python3
# author(s):
__author__ = "William van Beek"
__copyright__ = ""
__credits__ = ["William van Beek"]
__license__ = "GPL-3.0-only"
__version__ = "1.2"
__maintainer__ = "William van Beek"
__email__ = ""
__status__ = "Testing"

import argparse
from dohpc import dohpc

def main():
    # Get input form user
    daikin_heat_pump = dohpc("./files/start.yml")
    parser = argparse.ArgumentParser(
        description='Daikin OpenSource HeatPump Controller - (DOHPC)'
    )
    parser.add_argument('-t','--temp', action='store_true',
                    help='Show indoor temperature!',
                    dest='i_temp')
    args = parser.parse_args()

    if args.i_temp:
        print(daikin_heat_pump.IndoorTemperature[1])


if __name__ == "__main__":
    # Run program

    main()
