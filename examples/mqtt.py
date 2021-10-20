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

import paho.mqtt.client as mqtt
import time, os, sys, yaml
from dohpc import dohpc

#####
# This is a work in progress, as it needs to be rewritten to the new style.
#####

class dohpcmqtt():

    def __init__(self, config_file):
        self.config = ""
        self.config_file = config_file
        self._read_config(self.config_file)
        # Update to the latest data in the yml file.
        daikin_heat_pump = dohpc("./files/start.yml")

        # The callback for when the client receives a CONNACK response from the server.
        def on_connect(client, userdata, flags, rc):
            #print("Connected with result code "+str(rc))
            client.subscribe(
                [
                    ("DHPW/RecvOperationPower",2),
                    ("DHPW/RecvTargetTemperature",2),
                    ("DHPW/RecvOperationPowerful",2)
                    #("DHPW/RecvUpdateSchedule",2),
                    #("DHPW/RecvChangeSchedule",2)
                ]
            )
            client.connected_flag = True

        # The callback for when a PUBLISH message is received from the server.
        def on_message(client, userdata, message):
            # depending on the message, take a action:
            if message.topic == "DHPW/RecvTargetTemperature":
                daikin_heat_pump.ChangeTemp("1", "TargetTemperature", message.payload.decode("utf-8"))
            elif message.topic == "DHPW/RecvOperationPower":
                daikin_heat_pump.TurnOnOff("1", "Power", message.payload.decode("utf-8"))
            elif message.topic == "DHPW/RecvOperationPowerful":
                daikin_heat_pump.TurnOnOff("2", "Powerful", message.payload.decode("utf-8"))
            #elif message.topic == "DHPW/RecvUpdateSchedule":
            #    SH.sendHPvalues("S", message.payload.decode("utf-8"), daikinIP, daikinDataBase, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinDevices)
            #elif message.topic == "DHPW/RecvChangeSchedule":
            #    SH.sendHPvalues("I", message.payload.decode("utf-8"), daikinIP, daikinDataBase, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinDevices)
            else:
                pass

        start_program = True
        times_send = 0
        client = mqtt.Client("DHPW")
        client.connected_flag = False
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(daikinMqttBroker, port=1883, keepalive=60)

        # Start the loop, and wait for a connection
        client.loop_start()
        while client.connected_flag == False:
            #print("We are not yet connected, please hold (2)")
            time.sleep(2)

        # Here we enter a while loop that can be terminated with a new file (graceful) or a key stroke (non graceful)
        try:
            while not os.path.exists(self.config["mqtt"]["exit_file"]):
                # recieving data always runs on the background
                # Sleep for the spefified amount of time by the user
                time.sleep(int(self.config["mqtt"]["temp_timeout"]))
                times_send = times_send + 1
                if times_send == int(self.config["mqtt"]["data_timeout"]) or start_program == True:
                    # reset counter
                    times_send = 0
                    start_program = False
                    # Read YML file again
                    self._read_config(self.config_file)

                    client.publish("DHPW/ChildLockState", self.config[1]["childLockData"]["ChildLockState"])
                    client.publish("DHPW/ChildLockCode", self.config[1]["childLockData"]["ChildLockPin"])
                    client.publish("DHPW/HolidayStart", self.config[1]["unitholidaystart"])
                    client.publish("DHPW/HolidayEnd", self.config[1]["unitholidayend"])
                    client.publish("DHPW/HolidayState", self.config[1]["unitholidaystate"])
                    client.publish("DHPW/SystemHeatingState", self.config[1]["OperationData"]["Power"])
                    client.publish("DHPW/ErrorState", self.config[1]["unitstatusData"]["ErrorState"])
                    client.publish("DHPW/InstallerState", self.config[1]["unitstatusData"]["InstallerState"])
                    client.publish("DHPW/WarningState", self.config[1]["unitstatusData"]["WarningState"])
                    client.publish("DHPW/EmergencyState", self.config[1]["unitstatusData"]["EmergencyState"])
                    client.publish("DHPW/TargetTemperatureOverruledState", self.config[1]["unitstatusData"]["TargetTemperatureOverruledState"])
                else:
                    # Read HeatPump
                    self._read_config(self.config_file)

                    client.publish("DHPW/IndoorTemperature", self.config[1]["sensorData"]["IndoorTemperature"])
                    client.publish("DHPW/LeavingWaterTemperatureCurrent", self.config[1]["sensorData"]["LeavingWaterTemperatureCurrent"])
                    client.publish("DHPW/WantedTemperature", self.config[1]["sensorData"]["IndoorTemperature"])
                    client.publish("DHPW/OutdoorTemperature", self.config[1]["OperationData"]["TargetTemperature"])
                    client.publish("DHPW/OperatingMode", self.config[1]["OperationData"]["OperationMode"])

        except KeyboardInterrupt:
            print(" I was brutally interrupted, tis but a scratch!")
    # We reached the end, we can stop the loop
    client.loop_stop()

    def _read_config(self, config_file):
        """
        Read the config file.
        """
        with open(r'%s' % config_file) as file:
            self.config = yaml.full_load(file)
        return self.config

if __name__ == "__main__":
    dohpcmqtt("./files/start.yml")
