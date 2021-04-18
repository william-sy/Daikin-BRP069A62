# This file for now is a standalone script, will be tied in later
def startMQTT(daikinMqttBroker, daikinMqttPublishTempTimeOut, daikinMqttPublishDataTimeOut, daikinMqttExitFile, daikinIP, daikinDataBase, daikinUrlError, daikinUrlBase, daikingUrlDisc, daikinDevices):
    import paho.mqtt.client as mqtt
    import time, os, sys
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe([("DHPW/R_D_Error",2),("DHPW/R_Info",2),("DHPW/R_D_I_Brand",2),("DHPW/R_D_I_Model",2),("DHPW/R_D_I_Duty",2),("DHPW/R_D_I_Firmware",2),("DHPW/R_D_I_software",2),("DHPW/R_D_I_Serial",2),("DHPW/R_U_I_Indoor_Software",2),("DHPW/R_U_I_Outdoor_Software",2),("DHPW/R_U_I_Model_Number",2),("DHPW/R_U_I_Indoor_Eeprom",2),("DHPW/R_U_I_User_Eeprom",2),("DHPW/R_U_I_Given_Name",2),("DHPW/R_U_S_Error_State",2),("DHPW/R_U_S_Installer_State",2),("DHPW/R_U_S_Warning_State",2),("DHPW/R_U_S_Emergency_State",2),("DHPW/R_U_S_TTOS",2),("DHPW/R_U_S_WeatherDependentState",2),("DHPW/R_LeavingWaterTemperatureCurrent",2),("DHPW/R_Heating_TargetTemperature",2),("DHPW/R_Heating_IndoorTemperature",2),("DHPW/R_Heating_OutdoorTemperature",2),("DHPW/R_Heating_OperationPower",2),("DHPW/R_Heating_OperationMode",2),("DHPW/R_ChildLock_State",2),("DHPW/R_ChildLock_Code",2),("DHPW/R_Holiday_StartDate",2),("DHPW/R_Holiday_EndDate",2),("DHPW/R_Holiday_HolidayState",2),("DHPW/R_Schedule_Active",2),("DHPW/R_Schedule_Next_Start",2),("DHPW/R_Schedule_Next_Target",2),("DHPW/R_Schedule_Next_Day",2),("DHPW/R_Schedule_List_ID",2),("DHPW/W_Heating_OperationPower",2),("DHPW/W_TargetTemperature",2),("DHPW/R_ScheduleDefault",2),("DHPW/W_ScheduleDefault",2)])
        client.connected_flag=True

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, message):
        #print("message topic=",message.topic)
        #print("message received " ,str(message.payload.decode("utf-8")))
        # depending on the message, take a action:
        if message.topic == "DHPW/temp":
            print("Set new temperature")

    start_program = True
    client = mqtt.Client("DHPW")
    client.connected_flag=False
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(daikinMqttBroker, port=1883, keepalive=60)

    # Start the loop, and wait for a connection
    client.loop_start()
    while client.connected_flag == False:
        print("We are not yet connected, please hold (2)")
        time.sleep(2)

    # Here we enter a while loop that can be terminated with a new file (graceful) or a key stroke (non graceful)
    try:
        while not os.path.exists(daikinMqttExitFile):
            times_send = 0
            if start_program == True:
                # start program send all data
                start_program = False
                print("Send all the data!")
            else:
                # recieving data always runs on the background
                # Sleep for the spefified amount of time by the user
                time.sleep(200)
                times_send = times_send + 1
                if times_send == daikinMqttPublishDataTimeOut:
                    # reset counter
                    times_send = 0
                    #send all the data
                else:
                    pass
    except KeyboardInterrupt:
        print(" I was brutally interrupted, tis but a scratch!")

    # We reached the end, we can stop the loop
    client.loop_stop()
