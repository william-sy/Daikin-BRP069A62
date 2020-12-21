# Define a random string to send to the device
def randomString(stringLength=5):
    import string, random
    """
    Generate a random string of fixed length
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

# A function to read the heatpump data
def readHPOptions(daikinIP, daikinDevices):
    from websocket import create_connection
    import json, datetime, time
    import locale, calendar
    locale.setlocale(locale.LC_ALL, '')

    # Setup the connection
    ip = daikinIP
    ws = create_connection("ws://"+ip+"/mca")
    numerOfDevices = int(daikinDevices)
    daikinDeviceOptions = {}

    # Scan our options and put then in variables
    while numerOfDevices >= 0:
        daikinDeviceID = str(numerOfDevices)
        ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/"+daikinDeviceID+"/UnitProfile/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
        raw_data = json.loads(ws.recv())
        filter_data = raw_data["m2m:rsp"]["pc"]["m2m:cin"]["con"]
        # DDID = Daikin Device ID
        daikinDeviceOptions["DDID{0}".format(daikinDeviceID)] = filter_data
        numerOfDevices -= 1

    ws.close()
    # Debug the data your device sends your way
    print(daikinDeviceOptions)
    return daikinDeviceOptions

# A function to read the heatpump data
def readHPDetails(daikinIP,):
    from websocket import create_connection
    import json, datetime, time
    import locale, calendar
    locale.setlocale(locale.LC_ALL, '')

    # Setup the connection
    ip = daikinIP
    ws = create_connection("ws://"+ip+"/mca")

    # Get general Info about the device:
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_function = json.loads(ws.recv())
    #print(js_function)
    function = js_function["m2m:rsp"]["pc"]["m2m:cnt"]["lbl"]
    # device info
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNCSE-node/deviceInfo\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_deviceinfo = json.loads(ws.recv())
    #print(js_deviceinfo)
    brand = js_deviceinfo["m2m:rsp"]["pc"]["m2m:dvi"]["man"]
    model = js_deviceinfo["m2m:rsp"]["pc"]["m2m:dvi"]["mod"]
    duty = js_deviceinfo["m2m:rsp"]["pc"]["m2m:dvi"]["dty"]
    firmware = js_deviceinfo["m2m:rsp"]["pc"]["m2m:dvi"]["fwv"]
    software = js_deviceinfo["m2m:rsp"]["pc"]["m2m:dvi"]["swv"]
    dlb = js_deviceinfo["m2m:rsp"]["pc"]["m2m:dvi"]["dlb"]
    # Unit info:
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/UnitInfo/Version/IndoorSoftware/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_indoor_software = json.loads(ws.recv())
    #(js_indoor_software)
    indoor_software = js_indoor_software["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/UnitInfo/ModelNumber/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_indoor_model = json.loads(ws.recv())
    #print(js_indoor_model)
    indoor_model = js_indoor_model["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/UnitInfo/Version/IndoorSettings/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_indoor_eeprom = json.loads(ws.recv())
    #print(js_indoor_eeprom)
    indoor_eeprom = js_indoor_eeprom["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/UnitInfo/Version/OutdoorSoftware/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_outdoor_software = json.loads(ws.recv())
    #print(js_outdoor_software)
    outdoor_software = js_outdoor_software["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/UnitInfo/Version/RemoconSettings/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_user_eeprom = json.loads(ws.recv())
    #print(js_user_eeprom)
    user_eeprom = js_user_eeprom["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/UnitInfo/Version/RemoconSettings/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_user_software = json.loads(ws.recv())
    #print(js_user_software)
    user_software = js_user_software["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    # Power state
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/Operation/Power/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_power = json.loads(ws.recv())
    #print(js_power)
    power = js_power["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    # Operation state
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/Operation/OperationMode/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_operation = json.loads(ws.recv())
    #print(js_operation)
    operation = js_operation["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    # User defined name
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/UnitIdentifier/Name/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_given_name = json.loads(ws.recv())
    given_name = js_given_name["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    # Unit status
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/UnitStatus/ErrorState/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_us_ers_temp = json.loads(ws.recv())
    us_ers_temp = js_us_ers_temp["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/UnitStatus/InstallerState/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_us_is_temp = json.loads(ws.recv())
    us_is_temp = js_us_is_temp["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/UnitStatus/WarningState/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_us_ws_temp = json.loads(ws.recv())
    us_ws_temp = js_us_ws_temp["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/UnitStatus/EmergencyState/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_us_ems_temp = json.loads(ws.recv())
    us_ems_temp = js_us_ems_temp["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/0/Error/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_r_error = json.loads(ws.recv())
    r_error = js_r_error["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    # Did we manually change the temp on the thermostat or app?
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/UnitStatus/TargetTemperatureOverruledState/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_us_ttos_temp = json.loads(ws.recv())
    #print(js_us_ttos_temp)
    us_ttos_temp = js_us_ttos_temp["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    # Indoor Temp
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/Sensor/IndoorTemperature/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_indoor_temp = json.loads(ws.recv())
    indoor_temp = js_indoor_temp["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    # Outdoor temp
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/Sensor/OutdoorTemperature/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_outdoor_temp = json.loads(ws.recv())
    outdoor_temp = js_outdoor_temp["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    # Leaving Water Temp
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/Sensor/LeavingWaterTemperatureCurrent/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_lwtc_temp = json.loads(ws.recv())
    lwct_temp = js_lwtc_temp["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    # Target Temp
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/Operation/TargetTemperature/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_target_temp = json.loads(ws.recv())
    target_temp = js_target_temp["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    # ChildLock
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/ChildLock/LockedState/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_child_lock = json.loads(ws.recv())
    child_lock = js_child_lock["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/ChildLock/PinCode/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_child_lock_code = json.loads(ws.recv())
    child_lock_code = js_child_lock_code["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    # Holiday
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/Holiday/EndDate/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_holiday_end = json.loads(ws.recv())
    holiday_end = js_holiday_end["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/Holiday/StartDate/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_holiday_start = json.loads(ws.recv())
    holiday_start = js_holiday_start["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/Holiday/HolidayState/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_holiday_state = json.loads(ws.recv())
    holiday_state = js_holiday_state["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    # Weather WeatherDependentState
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/UnitStatus/WeatherDependentState/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_weather_state = json.loads(ws.recv())
    weather_state = js_weather_state["m2m:rsp"]["pc"]["m2m:cin"]["con"]

    # Active schedule:
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/Schedule/Active/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_active_schedule = json.loads(ws.recv())
    active_schedule = js_active_schedule["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    # Nested json :(
    js_active_schedule_id = json.loads(active_schedule)
    schedule_id = js_active_schedule_id["data"]["id"]
    # Upcomming schedule
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/Schedule/Next/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_next_schedule = json.loads(ws.recv())
    next_schedule = js_next_schedule["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    # Nested json :(
    js_next_schedule_data = json.loads(next_schedule)
    next_schedule_data_start = js_next_schedule_data["data"]["StartTime"]
    next_schedule_data_target = js_next_schedule_data["data"]["TargetTemperature"]
    # change number to day
    next_schedule_data_day = js_next_schedule_data["data"]["Day"]
    next_schedule_data_day = calendar.day_name[next_schedule_data_day]
    # Schedule data
    ws.send("{\"m2m:rqp\":{\"op\":2,\"to\":\"/[0]/MNAE/1/Schedule/List/Heating/la\",\"fr\":\"/\",\"rqi\":\""+randomString()+"\"}}")
    js_schedule_list = json.loads(ws.recv())
    schedule_list = js_schedule_list["m2m:rsp"]["pc"]["m2m:cin"]["con"]
    # Nested json :(
    js_schedule_list_uid = json.loads(schedule_list)
    schedule_list_uid = js_schedule_list_uid["data"]

    # Turning the heatpump on / off
    # Change to on / standby
    #{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Operation/Power","fr":"/S","rqi":"olpcx","ty":4,"pc":{"m2m:cin":{"con":"on","cnf":"text/plain:0"}}}}
    #{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Operation/Power","fr":"/S","rqi":"olpcx","ty":4,"pc":{"m2m:cin":{"con":"standby","cnf":"text/plain:0"}}}}
    # Set a different temperature
    # {"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Operation/TargetTemperature","fr":"/S","rqi":"","ty":4,"pc":{"m2m:cin":{"con":14,"cnf":"text/plain:0"}}}}
    # {"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Operation/TargetTemperature","fr":"/S","rqi":"","ty":4,"pc":{"m2m:cin":{"con":16,"cnf":"text/plain:0"}}}}
    # {"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Operation/TargetTemperature","fr":"/S","rqi":"","ty":4,"pc":{"m2m:cin":{"con":18,"cnf":"text/plain:0"}}}}
    # {"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Operation/TargetTemperature","fr":"/S","rqi":"","ty":4,"pc":{"m2m:cin":{"con":20,"cnf":"text/plain:0"}}}}


    # Change schedule to different one
    # Read:
    #{"m2m:rqp":{"op":2,"to":"/[0]/MNAE/1/Schedule/Active/la","fr":"/","rqi":""}}
    # Change:
    #{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Schedule/Active","fr":"/S","rqi":"","ty":4,"pc":{"m2m:cin":{"con": "{"data":{"path":"/mn-cse-5e639e61465efa001c09edc0/MNAE/1/schedule/List/Heating","id":2}}","cnf":"application/json:0"}}}}
    #Data:?: "{"data":{"path":"/mn-cse-5e639e61465efa001c09edc0/MNAE/1/schedule/List/Heating/la","id":2}}"
    #{"m2m:rqp":{"op":1,"to":"/[0]/MNAE/1/Schedule/Active","fr":"/S","rqi":"","ty":4,"pc":{"m2m:cin":{"con":20,"cnf":"text/plain:0"}}}}



    # Translate a 0 to yes or no
    #print(us_ttos_temp)
    if us_ttos_temp == 0:
        us_ttos_temp = "NO"
    else:
       us_ttos_temp = "YES"

    if child_lock == 0:
        child_lock = "NO"
    else:
        child_lock = "YES"

    if holiday_state == 0:
        holiday_state = "NO"
    else:
        holiday_state = "YES"

    print(f"User chosen schedule ID: {schedule_id}")
    print(f"Next schedule change: {next_schedule_data_day}, Time: {next_schedule_data_start}, temp will be set to: {next_schedule_data_target/10}")
    print(f"Complete schedule: {schedule_list_uid[schedule_id]}")
    print("=====================================================")
    print(f"Connected to Daikin on: {ip}")
    print(f"Device function: {function}")
    print(f"The device is currently: {power}, and the operation is: {operation}")
    print(f"Brand: {brand}, LAN adapter Model: {model}, Duty: {duty}, Firmware: {firmware}, Software: {software}, SerialNR: {dlb}")
    print(f"Given name by user: {given_name}")
    print("=====================================================")
    print(f"Indoor unit model: {indoor_model}, software: {indoor_software}, EEPROM: {indoor_eeprom}")
    print(f"Outdoor unit Softare: {outdoor_software}, User EEPROM: {user_eeprom}, User interface software: {user_software}")
    print("=====================================================")
    print(f"Current Errors: {us_ers_temp}, Current Warmings: {us_ws_temp}, Emergency state: {us_ems_temp},  Installer state: {us_is_temp}")
    print(f"Reported Errors: {r_error}")
    print("=====================================================")
    print(f"Did we manually override the scheduled temp: {us_ttos_temp}")
    print(f"Current indoor temp: {indoor_temp}")
    print(f"Current outdoor temp: {outdoor_temp}")
    print(f"Current water temp: {lwct_temp}")
    print(f"Current target temp: {target_temp}")
    print("=====================================================")
    print(f"Water temp is calculated based on: {weather_state}")
    print("=====================================================")
    print(f"Is child lock active: {child_lock}, Current pin is: {child_lock_code}")
    print("=====================================================")
    print(f"Holiday start: {holiday_start}, Holiday End: {holiday_end}, Holiday mode active?: {holiday_state}")
    print("=====================================================")
    ws.close()
