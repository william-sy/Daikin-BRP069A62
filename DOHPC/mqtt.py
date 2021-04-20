# This file for now is a standalone script, will be tied in later
def startMQTT(daikinMqttBroker, daikinMqttPublishTempTimeOut, daikinMqttPublishDataTimeOut, daikinMqttExitFile, daikinIP, daikinDataBase, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinDevices):
    import paho.mqtt.client as mqtt
    import time, os, sys
    import sqlite3 as sl
    import DOHPC.sendHP as SH
    import DOHPC.readHP as RH

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        #print("Connected with result code "+str(rc))
        client.subscribe(
            [
                ("DHPW/RecvOperationPower",2),
                ("DHPW/RecvTargetTemperature",2),
                ("DHPW/RecvUpdateSchedule",2),
                ("DHPW/RecvChangeSchedule",2)
            ]
        )
        client.connected_flag = True

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, message):
        # depending on the message, take a action:
        if message.topic == "DHPW/RecvTargetTemperature":
            SH.sendHPvalues("T", message.payload.decode("utf-8"), daikinIP, daikinDataBase, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinDevices)
        elif message.topic == "DHPW/RecvOperationPower":
            SH.sendHPvalues("O", message.payload.decode("utf-8"), daikinIP, daikinDataBase, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinDevices)
        elif message.topic == "DHPW/RecvUpdateSchedule":
            SH.sendHPvalues("S", message.payload.decode("utf-8"), daikinIP, daikinDataBase, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinDevices)
        elif message.topic == "DHPW/RecvChangeSchedule":
            SH.sendHPvalues("I", message.payload.decode("utf-8"), daikinIP, daikinDataBase, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinDevices)
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
        while not os.path.exists(daikinMqttExitFile):
            # recieving data always runs on the background
            # Sleep for the spefified amount of time by the user
            time.sleep(int(daikinMqttPublishTempTimeOut))
            times_send = times_send + 1
            if times_send == int(daikinMqttPublishDataTimeOut) or start_program == True:
                # reset counter
                times_send = 0
                start_program = False
                # Read HeatPump
                RH.readHPDetails(daikinIP, daikinDataBase, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinDevices)
                # Get and send
                con = sl.connect(daikinDataBase)
                with con:
                    hp_details = con.execute("SELECT * from hp_data order by DATE DESC limit 1")
                for row in hp_details:
                    client.publish("DHPW/ChildLockState", row[27])
                    client.publish("DHPW/ChildLockCode", row[28])
                    client.publish("DHPW/HolidayStart", row[29])
                    client.publish("DHPW/HolidayEnd", row[30])
                    client.publish("DHPW/HolidayState", row[31])
                    client.publish("DHPW/UserGivenName", row[14])
                    client.publish("DHPW/SystemHeatingState", row[20])
                    client.publish("DHPW/HpUnitIndoorEprom", row[12])
                    client.publish("DHPW/HpUnitUserEprom", row[13])
                    client.publish("DHPW/HpIndoorSoftware", row[9])
                    client.publish("DHPW/HpOutdoorSoftware", row[10])
                    client.publish("DHPW/HpModelNumber", row[11])
                    client.publish("DHPW/ControllerFirmware", row[6])
                    client.publish("DHPW/ControllerSoftware", row[7])
                    client.publish("DHPW/ControllerSerial", row[7])
                    client.publish("DHPW/Brand", row[3])
                    client.publish("DHPW/Model", row[4])
                    client.publish("DHPW/Type", row[5])
                    client.publish("DHPW/DeviceFunction", row[2])
                    client.publish("DHPW/Errors", row[1])
                    client.publish("DHPW/ErrorState", row[15])
                    client.publish("DHPW/InstallerState", row[16])
                    client.publish("DHPW/WarningState", row[17])
                    client.publish("DHPW/EmergencyState", row[18])
            else:
                # Read HeatPump
                RH.readHPDetails(daikinIP, daikinDataBase, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinDevices)
                # Get and send
                con = sl.connect(daikinDataBase)
                with con:
                    hp_details = con.execute("SELECT * from hp_data order by DATE DESC limit 1")
                for row in hp_details:
                    client.publish("DHPW/IndoorTemperature", row[23])
                    client.publish("DHPW/LeavingWaterTemperatureCurrent", row[21])
                    client.publish("DHPW/WantedTemperature", row[22])
                    client.publish("DHPW/OutdoorTemperature", row[24])
                    client.publish("DHPW/SystemState", row[25])
                    client.publish("DHPW/OperatingMode", row[26])
                    client.publish("DHPW/OperatingMode", row[26])
                    client.publish("DHPW/CurrentActiveSchedule", row[36])
                    client.publish("DHPW/NextSchedule", row[33])
                    client.publish("DHPW/NextTemperatureGoal", row[34])

    except KeyboardInterrupt:
        print(" I was brutally interrupted, tis but a scratch!")

    # We reached the end, we can stop the loop
    client.loop_stop()
