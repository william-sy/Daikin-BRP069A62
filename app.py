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

# This is a small app, using the dohpc module
from dohpc import dohpc
# The start file is mandatory, and must contain either a IP or a serial number
daikin_heat_pump = dohpc("./files/start.yml")
print(f"Indoor:    {daikin_heat_pump.IndoorTemperature}")
